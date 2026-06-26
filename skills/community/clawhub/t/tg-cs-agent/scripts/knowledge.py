"""Knowledge base: load Markdown docs, vectorize, and search."""
import os
import glob
import logging
import chromadb
from chromadb.utils import embedding_functions

# Suppress model loading warnings
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)


class KnowledgeBase:
    def __init__(self, docs_dir: str):
        self.docs_dir = docs_dir
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="knowledge", embedding_function=self.ef
        )
        self._loaded = False

    def load(self):
        """Load all markdown files from docs_dir into vector store."""
        if self._loaded and self.collection.count() > 0:
            return

        md_files = glob.glob(os.path.join(self.docs_dir, "**/*.md"), recursive=True)
        if not md_files:
            print(f"[KB] No markdown files found in {self.docs_dir}")
            return

        ids, documents, metadatas = [], [], []
        for filepath in md_files:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Split by sections (## headers)
            chunks = self._split_by_sections(content, filepath)
            for i, chunk in enumerate(chunks):
                doc_id = f"{os.path.basename(filepath)}_{i}"
                ids.append(doc_id)
                documents.append(chunk["text"])
                metadatas.append({"source": filepath, "section": chunk["section"]})

        if ids:
            self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            print(f"[KB] Loaded {len(ids)} chunks from {len(md_files)} files")

        self._loaded = True

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Search knowledge base, return top_k relevant chunks."""
        if self.collection.count() == 0:
            return []

        results = self.collection.query(query_texts=[query], n_results=top_k)

        hits = []
        for i in range(len(results["ids"][0])):
            hits.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "section": results["metadatas"][0][i]["section"],
                "distance": results["distances"][0][i],
            })
        return hits

    def _split_by_sections(self, content: str, filepath: str) -> list[dict]:
        """Split markdown content by ## headers into chunks."""
        lines = content.split("\n")
        chunks = []
        current_section = os.path.basename(filepath)
        current_lines = []

        for line in lines:
            if line.startswith("## "):
                if current_lines:
                    text = "\n".join(current_lines).strip()
                    if text:
                        chunks.append({"section": current_section, "text": text})
                current_section = line.lstrip("# ").strip()
                current_lines = [line]
            else:
                current_lines.append(line)

        if current_lines:
            text = "\n".join(current_lines).strip()
            if text:
                chunks.append({"section": current_section, "text": text})

        # If no sections found, return whole file as one chunk
        if not chunks:
            chunks.append({"section": os.path.basename(filepath), "text": content.strip()})

        return chunks
