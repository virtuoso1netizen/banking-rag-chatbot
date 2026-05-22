import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_groq import ChatGroq


# LOAD ENV VARIABLES
load_dotenv()

# FASTAPI APP
app = FastAPI()

# GLOBAL CONVERSATION CHAIN
conversation_chain = None


# READ PDF + TXT FILES
def get_file_text(uploaded_files):

    text = ""

    for file in uploaded_files:

        # PDF FILE
        if file.filename.endswith(".pdf"):

            pdf_reader = PdfReader(file.file)

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

        # TXT FILE
        elif file.filename.endswith(".txt"):

            text += file.file.read().decode("utf-8")

    return text


# TEXT CHUNKING
def get_text_chunks(text):

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    return chunks


# VECTOR STORE
def get_vectorstore(text_chunks):

    from langchain_huggingface import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(
        texts=text_chunks,
        embedding=embeddings
    )

    return vectorstore

# CONVERSATION CHAIN
def get_conversation_chain(vectorstore):

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.7
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain


# ROOT ENDPOINT
@app.get("/")
def home():

    return {
        "message": "Backend is running"
    }


# HEALTH ENDPOINT
@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# UPLOAD ENDPOINT
@app.post("/upload")
async def upload_documents(
    files: list[UploadFile] = File(...)
):

    global conversation_chain

    raw_text = get_file_text(files)

    text_chunks = get_text_chunks(raw_text)

    vectorstore = get_vectorstore(text_chunks)

    conversation_chain = get_conversation_chain(
        vectorstore
    )

    return {
        "message": "Documents processed successfully"
    }


# CHAT REQUEST MODEL
class ChatRequest(BaseModel):

    question: str


# CHAT ENDPOINT
@app.post("/chat")
async def chat(request: ChatRequest):

    global conversation_chain

    if conversation_chain is None:

        return {
            "error": "Please upload documents first"
        }

    response = conversation_chain(
        {"question": request.question}
    )

    return {
        "answer": response["answer"]
    }