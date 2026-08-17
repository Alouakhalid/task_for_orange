from pathlib import Path

DATA_DIR = Path(__file__).parent / "Data"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
