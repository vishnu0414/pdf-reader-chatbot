import streamlit as st
import fitz
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
import tempfile
import os
from dotenv import load_dotenv

# Load secrets from .env (hidden)
load_dotenv()

# Disable telemetry
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["CHROMA_TELEMETRY"] = "False"

import time
import shutil
import glob

def close_vectordb(chat_data):
    vectordb = chat_data.get("vectordb")
    if vectordb is None:
        return
    try:
        if hasattr(vectordb, "delete_collection"):
            try:
                vectordb.delete_collection()
            except Exception as e:
                st.warning(f"Failed to delete collection: {e}")
        if hasattr(vectordb, "_client") and hasattr(vectordb._client, "close"):
            try:
                vectordb._client.close()
            except Exception as e:
                st.warning(f"Failed to close Chroma client: {e}")
    except Exception as e:
        st.warning(f"Failed to close vector DB: {e}")


def clear_all_dbs():
    try:
        st.cache_resource.clear()
    except Exception:
        pass  # Ignore if no cache
    
    # Close any open vectordb collections and clients
    for pdf_hash, chat_data in list(st.session_state.chats.items()):
        try:
            close_vectordb(chat_data)
            if "vectordb" in chat_data:
                del chat_data["vectordb"]
        except Exception as e:
            st.warning(f"Failed to close DB for {pdf_hash}: {e}")
    
    # Retriable delete of DB dirs (Windows-friendly)
    max_retries = 3
    for db_path in glob.glob("./doc_db_*"):
        for attempt in range(max_retries):
            try:
                shutil.rmtree(db_path)
                st.success(f"Deleted {db_path}")
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    st.error(f"Could not delete {db_path} (locked by process)")
            except Exception as e:
                st.error(f"Error deleting {db_path}: {e}")
                break


st.set_page_config(page_title="🚀 PDF Reader Chatbot", layout="wide")

# Initialize session state for ChatGPT-like features
if 'chats' not in st.session_state:
    st.session_state.chats = {}  # {pdf_hash: {"history": [], "db_path": str}}
if 'current_pdf_hash' not in st.session_state:
    st.session_state.current_pdf_hash = None
if 'current_chat_history' not in st.session_state:
    st.session_state.current_chat_history = []
if 'processed_pdfs' not in st.session_state:
    st.session_state.processed_pdfs = []

def show_temp_message(message, success=True):
    """Show message using Streamlit's toast for non-blocking feedback."""
    if success:
        st.toast(message, icon="✅")
    else:
        st.toast(message, icon="📖")


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@st.cache_resource
def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    os.environ["GROQ_API_KEY"] = api_key
    return ChatGroq(model=model, temperature=0)

def process_pdf(uploaded_file):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        documents = []
        try:
            with fitz.open(tmp_path) as doc:
                show_temp_message(f"📖 Found {len(doc)} pages", success=False)
                for page_num in range(len(doc)):
                    text = doc[page_num].get_text()
                    if text.strip():  
                        documents.append(Document(page_content=text.strip(), metadata={"page": page_num + 1, "source": uploaded_file.name}))
                show_temp_message(f"✅ Extracted text from {len(documents)} pages")
        finally:
            os.unlink(tmp_path)
        
        if documents:
            text_splitter = CharacterTextSplitter(
                separator="\n\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            texts = text_splitter.split_documents(documents)
            show_temp_message(f"✂️ Created {len(texts)} chunks")
            return texts
        else:
            st.error("❌ No text found in PDF. Try another file.")
            return []
    return []

# Reset button - Clear all chats and data
if st.sidebar.button("🗑️ **Clear All Chats & Data**", help="Delete all PDF chats and databases"):
    clear_all_dbs()
    # Reset session state
    st.session_state.chats = {}
    st.session_state.current_pdf_hash = None
    st.session_state.current_chat_history = []
    st.session_state.processed_pdfs = []
    st.rerun()

st.sidebar.markdown("**Fully automatic** - no config!")

st.sidebar.markdown("### 💬 **Chat History**")
if st.session_state.processed_pdfs:
    for pdf_hash in st.session_state.processed_pdfs:
        chat_data = st.session_state.chats.get(pdf_hash, {})
        history = chat_data.get("history", [])
        preview = ""
        if history:
            last_msg = history[-1]["content"][:47] + "..." if len(history[-1]["content"]) > 50 else history[-1]["content"]
            preview = f"💭 {last_msg}"
        if st.sidebar.button(f"📄 {pdf_hash[:8]}... {preview}", key=f"select_{pdf_hash}", use_container_width=True):
            st.session_state.current_pdf_hash = pdf_hash
            st.session_state.current_chat_history = chat_data["history"][:]
            st.rerun()
else:
    st.sidebar.info("No chats yet. Upload a PDF!")

if st.sidebar.button("✨ **New Chat**", help="Reset the active PDF chat and show a fresh page"):
    if st.session_state.current_pdf_hash:
        current_hash = st.session_state.current_pdf_hash
        if current_hash in st.session_state.chats:
            st.session_state.chats[current_hash]["history"] = []
        st.session_state.current_chat_history = []
        st.session_state.current_pdf_hash = None
        st.session_state["pdf_upload"] = None
        st.rerun()

# Dashboard
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("## 🚀")
    st.markdown("### PDF Reader Chatbot Dashboard")

uploaded_file = st.file_uploader("📁 **Upload PDF**", type="pdf", key="pdf_upload")

if st.button("🔥 **Process & Index PDF**", type="primary", use_container_width=True) and uploaded_file:
    with st.spinner("🔄 Processing..."):
        try:
            texts = process_pdf(uploaded_file)
            if texts:
                import hashlib
                pdf_hash = hashlib.md5(uploaded_file.name.encode()).hexdigest()
                db_path = f"./doc_db_{pdf_hash}"
                embeddings = get_embeddings()
                vectordb = Chroma.from_documents(texts, embeddings, persist_directory=db_path)
                st.session_state.chats[pdf_hash] = {"history": [], "db_path": db_path, "vectordb": vectordb}
                st.session_state.processed_pdfs.append(pdf_hash)
                st.session_state.current_pdf_hash = pdf_hash
                st.session_state.current_chat_history = []
                st.balloons()
                show_temp_message(f"🎉 Ready to chat with {uploaded_file.name}!")
            else:
                st.error("❌ Failed to process PDF. Please try another file.")
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")

if st.session_state.current_pdf_hash:
    # Display chat history with 3 dots
    st.subheader("💬 Chat History")
    for msg in st.session_state.current_chat_history:
        with st.chat_message(msg["role"]):
            full_text = msg["content"]
            display_text = full_text[:150] + "..." if len(full_text) > 150 else full_text
            st.write(display_text)
    
    context_window = st.slider("📏 **Context Size**", 2, 10, 4)
    chat_data = st.session_state.chats[st.session_state.current_pdf_hash]
    retriever = chat_data["vectordb"].as_retriever(search_kwargs={"k": context_window})
    
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("""
Context: {context}

Question: {question}

Answer:""")
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    query = st.chat_input("💬 Ask about the PDF...")
    
    if query:
        # Add user message to history
        user_msg = {"role": "user", "content": query}
        st.session_state.current_chat_history.append(user_msg)
        chat_data["history"].append(user_msg)
        
        with st.chat_message("user"):
            st.write(query)
        
        with st.chat_message("assistant"):
            with st.spinner("🧠..."):
                response = chain.invoke(query)
                response_text = response.content
                st.write(response_text)
                
                # Add assistant message to history
                ass_msg = {"role": "assistant", "content": response_text}
                st.session_state.current_chat_history.append(ass_msg)
                chat_data["history"].append(ass_msg)
            
            docs = retriever.invoke(query)
            with st.expander(f"📚 Sources ({len(docs)})", expanded=False):
                for doc in docs:
                    col1, col2 = st.columns([1, 8])
                    col1.caption(f"P{doc.metadata['page']}")
                    col2.caption(doc.page_content[:300] + "...")

