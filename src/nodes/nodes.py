"""LangGraph nodes for RAG workflow"""
from src.state.rag_state import RAGState

class RAGNodes:
    """Contains node functions for RAG workflow"""
    def __init__(self, retriever, llm):
        """
        Initialize RAG nodes
        """
        self.retriever = retriever
        self.llm = llm
    
    def retrieve_docs(self, state: RAGState) -> RAGState:
        """
        Retrieve relevant documents node
        """
        docs = self.retriever.invoke(state.question)
        return RAGState(
            question=state.question,
            retrieved_docs=docs
        )
    
    def generate_answer(self, state: RAGState) -> RAGState:
        """
        Generate answer from retrieved documents node
        """
        context = "\n\n".join([doc.page_content for doc in state.retrieved_docs])
        prompt = f"""Answer the question based on the context.
Context:
{context}

Question: {state.question}"""
        
        response = self.llm.invoke(prompt)
        return RAGState(
            question=state.question,
            retrieved_docs=state.retrieved_docs,
            answer=response.content
        )