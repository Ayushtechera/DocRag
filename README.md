
# 🔎 DocRag - A document-based RAG system for intelligent, context-aware question answering.

> **A document-aware RAG system that turns your PDFs and web content into intelligent, grounded answers.**
[🚀 Live Demo](https://docrag-qhc25f5zfdmndiappvyxhmq.streamlit.app/)
<p align="center">
  <img width="698" height="428" alt="Screenshot 2026-08-14 140509" src="https://github.com/user-attachments/assets/db846a9e-023d-4e5d-b7c4-5ddfc1ebbb37" />
  <img width="654" height="421" alt="Screenshot 2026-08-14 140533" src="https://github.com/user-attachments/assets/d5279bb8-1a2a-441c-9784-efee17059317" />
  <img width="671" height="436" alt="Screenshot 2026-08-14 140552" src="https://github.com/user-attachments/assets/57323426-4a15-4265-818d-3a8d603aebb0" />
</p>

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
