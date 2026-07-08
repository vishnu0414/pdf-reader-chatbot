<div align="center">

# 🤖 AI PDF Reader Chatbot

### Chat with Your PDF using Generative AI & Retrieval-Augmented Generation (RAG)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=25&duration=3500&pause=1200&color=00C6FF&center=true&vCenter=true&width=900&lines=Upload+PDFs+%F0%9F%93%84;Ask+Questions+%F0%9F%92%AC;AI+Generates+Context-Aware+Answers+%F0%9F%A4%96;Powered+by+LangChain+%26+Flask;Retrieval-Augmented+Generation+(RAG)" />

<br>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-00A67E?style=for-the-badge)
![NLTK](https://img.shields.io/badge/NLTK-154F9B?style=for-the-badge)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-AI-blueviolet?style=for-the-badge)

</div>

---

# 📖 Table of Contents

- 📌 Overview
- ✨ Features
- ⚙️ Tech Stack
- 🏗️ System Architecture
- 🔄 Workflow
- 📁 Project Structure
- 🚀 Installation
- ▶️ Usage
- 📈 Future Enhancements
- 🤝 Contributing

---

# 📌 Overview

The **AI PDF Reader Chatbot** is a Retrieval-Augmented Generation (RAG) application that enables users to upload PDF documents and ask questions in natural language.

Instead of searching manually through lengthy documents, users can simply ask questions and receive AI-generated responses based on the uploaded PDF.

---

# ✨ Features

✅ Upload PDF Documents

✅ Intelligent PDF Parsing

✅ Natural Language Question Answering

✅ Context-Aware Responses

✅ Retrieval-Augmented Generation (RAG)

✅ Fast Semantic Search

✅ Interactive Chat Interface

✅ Accurate Information Retrieval

---

# ⚙️ Tech Stack

### Programming Language

<p align="center">
<img src="https://skillicons.dev/icons?i=python"/>
</p>

---

### Frameworks & Libraries

<p align="center">

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>

</p>

<p align="center">

<img src="https://img.shields.io/badge/LangChain-00A67E?style=for-the-badge"/>

<img src="https://img.shields.io/badge/PyMuPDF-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/NLTK-154F9B?style=for-the-badge"/>

<img src="https://img.shields.io/badge/FAISS-005571?style=for-the-badge"/>

</p>

---

# 🏗️ System Architecture

```text
                📄 PDF Document
                       │
                       ▼
              Text Extraction
                (PyMuPDF)
                       │
                       ▼
             Text Chunking
                       │
                       ▼
          Embedding Generation
                       │
                       ▼
          Vector Database (FAISS)
                       │
                       ▼
          User Question 💬
                       │
                       ▼
          Semantic Search
                       │
                       ▼
            LangChain RAG
                       │
                       ▼
             AI Response 🤖
```

---

# 🔄 Workflow

```text
Upload PDF
     │
     ▼
Extract Text
     │
     ▼
Split into Chunks
     │
     ▼
Create Embeddings
     │
     ▼
Store in Vector Database
     │
     ▼
Ask Questions
     │
     ▼
Retrieve Relevant Chunks
     │
     ▼
Generate AI Response
```

---

# 📁 Project Structure

```text
pdf-reader-chatbot
│
├── app.py
├── requirements.txt
├── templates/
├── static/
├── uploads/
├── README.md
└── ...
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/vishnu0414/pdf-reader-chatbot.git
```

Move into the project

```bash
cd pdf-reader-chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

After running the command, open your browser at:

```
http://localhost:8501
```

If the browser doesn't open automatically, copy and paste the URL into your browser.

# 💬 How It Works

1️⃣ Upload a PDF document

              ⬇️

2️⃣ The application extracts text

              ⬇️

3️⃣ Text is converted into embeddings

              ⬇️

4️⃣ Relevant chunks are retrieved

              ⬇️

5️⃣ LangChain generates an intelligent answer

---

# 🎯 Use Cases

📚 Study Notes

📑 Research Papers

📄 Company Reports

⚖️ Legal Documents

🏥 Medical Reports

📘 Books

📃 Manuals

---

# 🚀 Future Enhancements

- 🌐 Multiple PDF Support
- 🔊 Voice Assistant
- 📄 PDF Summarization
- 🌍 Multi-language Support
- 📱 Responsive UI
- ☁️ Cloud Deployment
- 🔍 OCR for Scanned PDFs
- 🧠 Memory-based Conversations

---

# 🤝 Contributing

Contributions are welcome.

Feel free to fork the repository and submit a Pull Request.

---

# 📜 License

This project is licensed for educational and learning purposes.

---

<div align="center">

## ⭐ If you like this project, consider giving it a Star!

Made with ❤️ using Python, Streamlit & LangChain

</div>
