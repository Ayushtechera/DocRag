# 🔎 DocRag

> **A document-aware RAG system that turns your PDFs and web content into intelligent, grounded answers.**

## 📸 Demo

![DocRag Demo 1](assets/demo-1.png)

![DocRag Demo 2](assets/demo-2.png)

![DocRag Demo 3](assets/demo-3.png)

## 🚀 What it does

- 📄 Loads **PDFs, TXT files & URLs**
- ✂️ Splits documents into meaningful chunks
- 🔍 Retrieves relevant context from the knowledge base
- 🤖 Uses an **LLM + ReAct Agent** to generate answers
- 🌐 Uses **Wikipedia** when general knowledge is needed
- 📚 Shows the **source documents** used for the answer
- ⚡ Displays response time and recent searches

## 🧠 Architecture

```text
Documents / URLs
       ↓
Document Loader
       ↓
Text Splitting
       ↓
Embeddings + Retriever
       ↓
ReAct Agent
   ↙         ↘
Retriever   Wikipedia
   ↘         ↙
      LLM
       ↓
   Final Answer