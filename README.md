# Government Schemes RAG Chatbot

![Vue.js](https://img.shields.io/badge/vue-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

A full-stack, voice-enabled Retrieval-Augmented Generation (RAG) chatbot designed to answer queries about Government Schemes. It leverages a **Local LLM** for natural language understanding, a **Neo4j Graph Database** for robust knowledge retrieval, and supports dual-language input/output in English and Marathi.

---

## ✨ Features

- **Knowledge Graph RAG:** Uses Neo4j to store government scheme data, allowing for complex, relationship-based queries instead of standard vector similarity searches.
- **Local LLM Integration:** Translates user questions into precise Cypher queries to extract data directly from the knowledge graph.
- **Bilingual Support (English & Marathi):**
  - Translates Marathi text to English using `deep-translator` before processing.
  - Generates responses and reads them out aloud.
- **Voice-Enabled:**
  - **Speech-to-Text (STT):** Uses the browser's native Web Speech API.
  - **Text-to-Speech (TTS):** Uses Python's `pyttsx3` for offline voice synthesis.
- **Modern UI:** Built with Vue 3 and Tailwind CSS, featuring chat session management, responsive design, and local storage persistence.

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Vue 3 + Vite
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Speech Recognition:** Web Speech API

### Backend
- **Framework:** Python + Flask
- **Database:** Neo4j Graph Database
- **NLP & Translation:** `langdetect`, `deep-translator`
- **Text-to-Speech:** `pyttsx3`

---

## 📁 Project Structure

```text
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── chatbot.py              # NLP, translation, and TTS logic
│   ├── cypher_generator.py     # Local LLM logic for generating Cypher queries
│   ├── graph_query.py          # Neo4j connection and query execution
│   ├── import_schemes.py       # Script to populate Neo4j from dataset.csv
│   ├── dataset.csv             # Government schemes dataset
│   └── examples.json           # Examples/Few-shot prompts for the LLM
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   └── Chat.vue        # Main chat UI and logic
    │   ├── App.vue
    │   └── main.js
    ├── index.html
    ├── package.json
    ├── tailwind.config.js
    └── vite.config.js
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- Python 3.8+
- Neo4j Desktop (or a running local instance)
- Ollama running locally with the `mistral` model:
  ```bash
  ollama run mistral
  ```

---

### 1. Database Setup (Neo4j)
1. Start your Neo4j database instance (e.g., from Neo4j Desktop).
2. Configure your Neo4j credentials (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASS`) inside `backend/import_schemes.py` and `backend/graph_query.py`.
3. Populate the database using the Python script (detailed in the Backend setup below).

---

### 2. Backend Setup
Navigate to the `backend` directory, create a clean Python virtual environment, install the required packages, and run the import script to seed the database:

```bash
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the clean dependency stack
pip install flask flask-cors neo4j deep-translator langdetect pyttsx3 pandas

# Seed the Neo4j database
python import_schemes.py

# Start the Flask app
python app.py
```
*The backend server will run on `http://127.0.0.1:5000`.*

---

### 3. Frontend Setup
Navigate to the `frontend` directory, install Node dependencies, and start the development server:

```bash
cd frontend
npm install
npm run dev
```
*The frontend interface will open on `http://localhost:5173` (or the port shown in the terminal).*

---

## ⚙️ Architecture & Technical Highlights (For Presentation)

### 1. Natural Language to Cypher Translation
The system uses **Few-shot Prompting** via Ollama (Mistral) to map complex English requests to Cypher. When a user asks:
> *"health schemes for women in bihar"*

The LLM translates it into:
```cypher
MATCH (s:Scheme)-[:HAS_LOCATION]->(sl:Location)
OPTIONAL MATCH (s)-[:DETAILS]->(desc:Description)
OPTIONAL MATCH (s)-[:HAS_OBJECTIVE]->(o:Objective)
OPTIONAL MATCH (s)-[:HAS_TAG]->(t:Tag)
WITH *
WHERE toLower(sl.name) CONTAINS toLower("bihar")
  AND (toLower(s.name) CONTAINS toLower("health") OR toLower(o.name) CONTAINS toLower("health"))
  AND (toLower(s.name) CONTAINS toLower("women") OR toLower(t.name) CONTAINS toLower("women"))
RETURN s.name, o.name, desc.text, sl.name
LIMIT 200
```

### 2. Scope Safety with `WITH *`
A common Neo4j issue occurs when `WHERE` is placed immediately after `OPTIONAL MATCH` statements, which restricts the scope of the filter to *only the optional relation* rather than the primary match (returning the entire database). 

Our query compiler automatically injects a `WITH *` statement before the `WHERE` clause. This merges the scopes and guarantees location filters are evaluated globally across the entire graph.

### 3. Language & Speech Pipeline
1. **Input:** Text/Voice (English/Marathi).
2. **Translation:** Detection using `langdetect` + translation using `deep-translator`.
3. **Synthesis:** Custom background thread utilizing `pyttsx3` for synchronous, non-blocking text-to-speech output.
