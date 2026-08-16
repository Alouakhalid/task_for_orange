<p align="center">
  <img src="https://img.shields.io/badge/Day%201-Document%20Ingestion-0d1117?style=for-the-badge&labelColor=58a6ff&color=0d1117" alt="Day 1">
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6F00?style=for-the-badge" alt="ChromaDB">
  <img src="https://img.shields.io/badge/Status-Complete-00c853?style=for-the-badge" alt="Status">
</p>

<h1 align="center">🏥 AI Clinical Decision Support — Document Ingestion Pipeline</h1>

<p align="center">
  <strong>Day 1 of the AI Clinical Decision Support Lite Hackathon</strong><br>
  A production-grade RAG ingestion pipeline that transforms WHO clinical guidelines into a semantically searchable vector index with full citation traceability.
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Pipeline Stages](#-pipeline-stages)
- [Quick Start](#-quick-start)
- [Configuration](#%EF%B8%8F-configuration)
- [Notebook Walkthrough](#-notebook-walkthrough)
- [Key Results](#-key-results)
- [Technical Decisions](#-technical-decisions)
- [Dependencies](#-dependencies)
- [What's Next — Day 2](#-whats-next--day-2)

---

## 🧠 Overview

Large language models generate fluent, confident clinical recommendations — even when they have **no real evidence** behind them. This project builds the **retrieval foundation** of a Retrieval-Augmented Generation (RAG) system that forces an LLM to answer *only* from verified clinical text.

**Day 1 delivers:**

| Capability | Description |
|:-----------|:------------|
| **PDF Parsing** | Structure-preserving extraction from WHO hypertension guidelines |
| **Section-Aware Chunking** | Intelligent text splitting that respects paragraph and sentence boundaries |
| **Citation Metadata** | Every chunk carries `document_name`, `page_number`, and `chunk_id` |
| **Semantic Embeddings** | 384-dimensional vectors via `all-MiniLM-L6-v2` sentence transformer |
| **Vector Index** | Persistent ChromaDB store with similarity search and relevance scoring |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENT INGESTION PIPELINE                  │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │          │    │          │    │          │    │          │  │
│  │  PDF     │───▶│  Chunk   │───▶│  Embed   │───▶│  Index   │  │
│  │  Parser  │    │  Engine  │    │  Model   │    │  Store   │  │
│  │          │    │          │    │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│   PyPDFLoader     Recursive       MiniLM-L6       ChromaDB     │
│   + Metadata      CharText        384-dim         Persistent   │
│   Normalization   Splitter        Vectors         Collection   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │                                              │
         ▼                                              ▼
   WHO Guidelines                              similarity_search()
   (Data/*.pdf)                              with relevance scores
```

---

## 📁 Project Structure

```
Day One/Task/
│
├── 📓 Day1_Task1_Document_Ingestion.ipynb   # Interactive walkthrough (all cells executable)
├── 🐍 ingest.py                             # Core pipeline module
├── ⚙️ config.py                              # Centralized configuration
├── 📦 requirements.txt                       # Python dependencies
├── 📖 README.md                              # This file
│
├── Data/
│   ├── WHO_Hypertension_Guideline_2021.pdf               # 13-page WHO guideline (CC BY-NC-SA 3.0)
│   ├── Guideline for the pharmacological treatment...pdf  # Full 61-page treatment guideline
│   └── README.md                                          # Data source documentation
│
├── chroma_db/                                # Persisted vector index (auto-generated)
│
├── Instructions.pdf                          # Task specification
└── Project Out Come.pdf                      # Expected deliverables checklist
```

---

## 🔬 Pipeline Stages

### Stage 1 — PDF Parsing & Metadata Normalization

```python
pages = load_pdfs(config.DATA_DIR)
```

- Reads every `*.pdf` in the data directory using `PyPDFLoader`
- Stamps each page with normalized metadata **before** chunking:
  - `document_name` → PDF filename (stem)
  - `page_number` → Human-friendly 1-indexed page number
- This ensures citation provenance survives through all downstream transformations

### Stage 2 — Section-Aware Chunking

```python
chunks = chunk_documents(pages)
```

- Uses `RecursiveCharacterTextSplitter` with a hierarchical separator strategy:

  ```
  Priority: "\n\n" → "\n" → ". " → " " → ""
  ```

- Chunk size: **1,200 characters** (~300 tokens × 4 chars/token)
- Chunk overlap: **200 characters** (~50 tokens × 4 chars/token)
- Each chunk receives a unique `chunk_id` for deterministic referencing

**Why not naive fixed-size splitting?**

| Metric | Naive (200-char) | Section-Aware (1200-char) |
|:-------|:----------------:|:-------------------------:|
| Total chunks | 994 | **217** |
| Respects sentence boundaries | ❌ | ✅ |
| Preserves paragraph context | ❌ | ✅ |
| Citation-ready boundaries | ❌ | ✅ |

### Stage 3 — Embedding Generation

```python
embed_fn = get_embedding_function()
```

- Model: **`sentence-transformers/all-MiniLM-L6-v2`**
- Output: **384-dimensional** dense vectors
- Runs locally — no API keys required, no data leaves the machine
- ~100 MB model, downloaded once and cached

### Stage 4 — Vector Index Construction

```python
vectordb = build_index(chunks)
```

- Stores all chunk embeddings + metadata in a persistent **ChromaDB** collection
- Supports `similarity_search_with_relevance_scores()` for ranked retrieval
- Persisted to `chroma_db/` — survives process restarts

---

## 🚀 Quick Start

### Prerequisites

- Python **3.10+**
- pip package manager

### Installation

```bash
cd "Day One/Task"
pip install -r requirements.txt
```

### Option A — Run the Pipeline Script

```bash
python ingest.py
```

```
Loaded 74 pages.
Created 217 chunks.
Vector index built and persisted.
```

### Option B — Run the Interactive Notebook

```bash
jupyter notebook Day1_Task1_Document_Ingestion.ipynb
```

Execute cells sequentially from top to bottom. Each stage includes checkpoints for validation.

---

## ⚙️ Configuration

All pipeline parameters are centralized in `config.py`:

| Parameter | Default | Description |
|:----------|:--------|:------------|
| `DATA_DIR` | `./Data` | Directory containing clinical guideline PDFs |
| `CHROMA_DIR` | `./chroma_db` | Persistent vector store location |
| `CHUNK_SIZE` | `300` | Target chunk size in tokens |
| `CHUNK_OVERLAP` | `50` | Overlap between consecutive chunks in tokens |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace sentence transformer model |

> **Tuning Tip:** Increase `CHUNK_SIZE` for longer clinical sections (e.g., dosage tables). Decrease for more granular retrieval at the cost of context.

---

## 📓 Notebook Walkthrough

The notebook mirrors the pipeline but exposes every intermediate result for inspection:

| Section | What You'll See |
|:--------|:----------------|
| **§0 Setup** | Config validation, PDF discovery |
| **§1 Why Grounding Matters** | Conceptual foundation for RAG in clinical AI |
| **§2 Parse the PDF** | Raw page extraction, metadata inspection |
| **§3 Compare Chunking** | Side-by-side: naive vs. section-aware chunk boundaries |
| **§4 Citation Metadata** | `chunk_id`, `document_name`, `page_number` on every chunk |
| **§5 Embedding Demo** | Cosine similarity proof — same meaning scores higher |
| **§6 Build Vector Index** | Full ChromaDB index construction |
| **§7 Real Query** | Clinical question → ranked results with citations |

---

## 📊 Key Results

### Embedding Semantic Similarity

| Comparison | Cosine Similarity |
|:-----------|:-----------------:|
| *"first-line treatment for hypertension"* vs *"initial therapy for high blood pressure"* | **0.764** |
| *"first-line treatment for hypertension"* vs *"recommended screening interval for breast cancer"* | 0.085 |

> The embedding model correctly identifies that different words can carry the same clinical meaning — this is the mechanism that powers semantic search.

### Query Retrieval

**Question:** *"What is the target blood pressure for a patient with cardiovascular disease?"*

| Rank | Score | Source | Page |
|:----:|:-----:|:-------|:----:|
| 1 | 0.481 | Guideline for the pharmacological treatment of hypertension in adults | 28 |
| 2 | 0.471 | WHO_Hypertension_Guideline_2021 | 5 |
| 3 | 0.467 | WHO_Hypertension_Guideline_2021 | 9 |

> Top result correctly retrieves **Section 3.6 — Target Blood Pressure** with full citation metadata.

---

## 🧩 Technical Decisions

| Decision | Rationale |
|:---------|:----------|
| **PyPDFLoader** over alternatives | Preserves page boundaries and basic structure; sufficient for text-heavy guidelines |
| **RecursiveCharacterTextSplitter** | Hierarchical separators maintain semantic coherence at chunk boundaries |
| **all-MiniLM-L6-v2** | Best balance of quality (384-dim) vs. speed; runs locally without GPU |
| **ChromaDB** | Lightweight, persistent, Python-native vector store; ideal for hackathon scope |
| **Metadata-first approach** | Stamping `document_name` + `page_number` before chunking guarantees citation survival |
| **Token-based sizing (×4 char estimate)** | Approximates token boundaries without requiring a tokenizer dependency |

---

## 📦 Dependencies

```
langchain>=0.2.0
langchain-community>=0.2.0
langchain-chroma>=0.1.0
chromadb>=0.5.0
pypdf>=4.0.0
sentence-transformers>=5.0.0
numpy
```

All inference runs **locally** — no OpenAI API key or external service required.

---

## 🔮 What's Next — Day 2

Day 2 picks up exactly where this pipeline ends:

- **Retrieval Tuning** — Optimize `top_k` and relevance thresholds
- **Embedding Benchmarking** — Compare `all-MiniLM-L6-v2` against larger models
- **Evaluation Metrics** — Measure retrieval quality with logged, reproducible numbers
- **Query Expansion** — Test multi-hop and complex clinical questions

---

<p align="center">
  <sub>Built for the <strong>AI Clinical Decision Support Lite Hackathon</strong> · Day 1 — Document Ingestion</sub><br>
  <sub>Data Source: WHO Guideline for the Pharmacological Treatment of Hypertension in Adults (2021) · CC BY-NC-SA 3.0 IGO</sub>
</p>
