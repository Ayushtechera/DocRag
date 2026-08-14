"""LangGraph nodes for RAG workflow + ReAct Agent inside generate_content"""
from typing import List, Optional
from src.state.rag_state import RAGState
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
class RAGNodes:
    """Contains node functions for RAG workflow"""
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
        self._agent = None
    def retrieve_docs(self, state: RAGState) -> RAGState:
        """Classic retriever node"""
        docs = self.retriever.invoke(state.question)
        return RAGState(
            question=state.question,
            retrieved_docs=docs
        )
    def _build_tools(self):
        """Build retriever and Wikipedia tools."""
        @tool
        def retriever_tool(query: str) -> str:
            """Fetch relevant passages from the indexed document corpus."""
            docs: List[Document] = self.retriever.invoke(query)
            if not docs:
                return "No documents found."
            merged = []
            for i, d in enumerate(docs[:8], start=1):
                meta = d.metadata if hasattr(d, "metadata") else {}
                title = (
                    meta.get("title")
                    or meta.get("source")
                    or f"doc_{i}"
                )
                merged.append(
                    f"[{i}] {title}\n{d.page_content}"
                )
            return "\n\n".join(merged)

        wiki = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(
                top_k_results=3,
                lang="en"
            )
        )

        @tool
        def wikipedia(query: str) -> str:
            """Search Wikipedia for general knowledge."""
            return wiki.run(query)
        return [retriever_tool, wikipedia]

    def _build_agent(self):
        """Build the ReAct agent with retriever and Wikipedia tools."""

        tools = self._build_tools()
        system_prompt = (
            "You are a helpful RAG agent. "
            "Use the retriever tool for questions about the user's documents. "
            "Use the wikipedia tool only when general knowledge is needed. "
            "Always provide the final answer to the user."
        )
        self._agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=system_prompt
        )

    def generate_answer(self, state: RAGState) -> RAGState:
        """Generate answer using the ReAct agent."""
        if self._agent is None:
            self._build_agent()
        result = self._agent.invoke(
            {
                "messages": [
                    HumanMessage(content=state.question)
                ]
            }
        )
        messages = result.get("messages", [])
        answer: Optional[str] = None
        if messages:
            answer_msg = messages[-1]
            answer = getattr(answer_msg, "content", None)
        return RAGState(
            question=state.question,
            retrieved_docs=state.retrieved_docs,
            answer=answer or "Could not generate answer."
        )