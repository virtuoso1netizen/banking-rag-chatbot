import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from htmlTemplates import css, bot_template, user_template



def get_file_text(uploaded_files):

    text = ""

    for file in uploaded_files:

        # PDF FILES
        if file.name.endswith(".pdf"):

            pdf_reader = PdfReader(file)

            for page in pdf_reader.pages:

                if page.extract_text():
                    text += page.extract_text()

        # TXT FILES
        elif file.name.endswith(".txt"):

            text += file.read().decode("utf-8")

    return text


def get_text_chunks(text):

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)

    return chunks


def get_vectorstore(text_chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(
        texts=text_chunks,
        embedding=embeddings
    )

    return vectorstore



def get_conversation_chain(vectorstore):

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.9
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



def handle_user_query(user_question):

    response = st.session_state.conversation(
        {"question": user_question}
    )

    answer = response["answer"]

    # Store chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.session_state.chat_history.append(
        type(
            "msg",
            (),
            {
                "type": "human",
                "content": user_question
            }
        )
    )

    st.session_state.chat_history.append(
        type(
            "msg",
            (),
            {
                "type": "ai",
                "content": answer
            }
        )
    )



def display_chat_history():

    if "chat_history" not in st.session_state:
        return

    for message in st.session_state.chat_history:

        if message.type == "human":

            st.write(
                user_template.replace(
                    "{{MSG}}",
                    message.content
                ),
                unsafe_allow_html=True
            )

        else:

            st.write(
                bot_template.replace(
                    "{{MSG}}",
                    message.content
                ),
                unsafe_allow_html=True
            )



def main():

    load_dotenv()

    st.set_page_config(
        page_title="AI Banking Support Chatbot using RAG and LangChain",
        page_icon="🏦",
        layout="centered"
    )

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.title("AI Banking Support Assistant")
    st.header("Chat with your Documents 📄")

    
    user_question = st.text_input(
        "Ask a question about your documents:"
    )

    if user_question:

        if st.session_state.conversation:

            handle_user_query(user_question)

        else:

            st.warning(
                "Please upload and process documents first."
            )

   
    display_chat_history()

    
    with st.sidebar:

        st.subheader("Your Documents")

        uploaded_files = st.file_uploader(
            "Upload PDF or TXT files",
            type=["pdf", "txt"],
            accept_multiple_files=True
        )

        if st.button("Process Documents"):

            if uploaded_files:

                with st.spinner(
                    "Processing documents..."
                ):

                    # Extract text
                    raw_text = get_file_text(
                        uploaded_files
                    )

                    # Split into chunks
                    text_chunks = get_text_chunks(
                        raw_text
                    )

                    # Create vector store
                    vectorstore = get_vectorstore(
                        text_chunks
                    )

                    # Create conversation chain
                    st.session_state.conversation = (
                        get_conversation_chain(
                            vectorstore
                        )
                    )

                    st.success(
                        "Chatbot is ready!"
                    )

            else:

                st.warning(
                    "Please upload documents first."
                )


if __name__ == "__main__":
    main()