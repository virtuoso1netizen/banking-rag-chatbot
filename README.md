# 🏦 AI Banking Support Chatbot using RAG

An AI-powered Banking Support Chatbot built using **Retrieval-Augmented Generation (RAG)**, **FastAPI**, **LangChain**, **FAISS**, and **Groq LLMs**.  
The chatbot retrieves relevant information from uploaded banking-related documents and generates context-aware responses.

---

# 🚀 Features

✅ Conversational AI chatbot  
✅ Retrieval-Augmented Generation (RAG) pipeline  
✅ PDF and TXT document support  
✅ Semantic similarity search using FAISS  
✅ Context-aware conversational memory  
✅ FastAPI backend APIs  
✅ Groq LLM integration  
✅ Dockerized deployment  
✅ Cloud deployment using Render  

---

# 🧠 RAG Pipeline

The chatbot implements a complete RAG workflow:

1. Document Upload
2. Text Extraction
3. Text Chunking
4. Embedding Generation
5. Vector Database Storage
6. Semantic Retrieval
7. LLM-based Response Generation

---

# 🏗️ Architecture

```text
User Query
    ↓
FastAPI Backend
    ↓
FAISS Vector Database
    ↓
Semantic Retrieval
    ↓
Groq LLM (Llama 3.1)
    ↓
AI Generated Response
```

---

# 🛠️ Technologies Used

## Backend
- FastAPI
- Uvicorn
- Python

## AI / RAG
- LangChain
- FAISS
- Hugging Face Embeddings
- Sentence Transformers
- Groq API (Llama 3.1)

## Document Processing
- PyPDF2

## Deployment
- Docker
- Render

---

# 📂 Supported File Types

- PDF
- TXT

---

# 🔗 Live Deployment

## Backend API

```text
https://banking-rag-backend-5yen.onrender.com
```

## Swagger API Docs

```text
https://banking-rag-backend-5yen.onrender.com/docs
```

---

# 📡 API Endpoints

## 1️⃣ Health Check

```http
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

## 2️⃣ Upload Documents

```http
POST /upload
```

Uploads PDF/TXT documents and creates vector embeddings.

---

## 3️⃣ Chat Endpoint

```http
POST /chat
```

### Request Body

```json
{
  "question": "What is the interest rate for personal loans?"
}
```

### Response

```json
{
  "answer": "The interest rate is 10%."
}
```

---

# ⚙️ Local Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/virtuoso1netizen/banking-rag-chatbot.git
cd banking-rag-chatbot
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Create `.env` File

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 5️⃣ Run Backend

```bash
uvicorn backend:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# 🐳 Docker Deployment

## Dockerfile

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "10000"]
```

---

# ☁️ Deployment Approach

The backend was deployed using **Render** with Docker support.

### Deployment Steps

1. Push project to GitHub
2. Create Render Web Service
3. Add Dockerfile
4. Configure environment variables
5. Deploy backend service

---

# 🧪 Example Workflow

### Step 1 — Upload Document

Upload a banking-related PDF/TXT document using:

```http
POST /upload
```

---

### Step 2 — Ask Questions

```json
{
  "question": "What is the interest rate for education loans?"
}
```

---

### Step 3 — AI Response

```json
{
  "answer": "The education loan interest rate is 9%."
}
```

---

# 🔮 Future Improvements

- Persistent vector database storage
- Frontend deployment
- Redis caching
- Authentication system
- Streaming responses
- Reranking pipeline
- Multi-user support
- Conversation history database
- Prompt optimization

---

# ⚠️ Challenges Faced

- Python dependency conflicts
- Docker deployment debugging
- Tokenizers installation issues
- Render deployment optimization
- AI package compatibility management

---

# 📌 Conclusion

This project demonstrates a production-oriented implementation of a Retrieval-Augmented Generation (RAG) chatbot capable of answering banking-related customer queries using semantic retrieval and LLM-powered response generation.

The system combines FastAPI APIs, vector databases, embeddings, and modern LLM infrastructure into a deployable AI-powered banking assistant.

---

# 👩‍💻 Author

**Anika**  
GitHub: https://github.com/virtuoso1netizen
