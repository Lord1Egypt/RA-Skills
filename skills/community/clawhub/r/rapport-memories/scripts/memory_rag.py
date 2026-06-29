#!/usr/bin/env python3
"""
Rapport Memories - SQLite and ChromaDB Memory RAG system
Provides semantic search capabilities over agent memory files.
"""

import os
import sys
import re
import json
import sqlite3
import hashlib
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

# Try to import chromadb, fallback to SQLite FTS if not present
try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


class MemorySearchResult:
    """Represents a semantic search result from the memory store."""
    def __init__(self, content: str, metadata: Dict[str, Any], score: float):
        self.content = content
        self.metadata = metadata or {}
        self.score = score

    def __repr__(self):
        return f"<MemorySearchResult score={self.score:.4f} taxonomy={self.metadata.get('taxonomy')}>"


class MemoryRAG:
    """Manages SQLite metadata registry and ChromaDB vector store for semantic memory."""
    def __init__(self, store_path: Optional[str] = None):
        # Determine database and vector store paths
        if not store_path:
            store_path = os.environ.get("RAPPORT_MEMORIES_STORE_PATH")
        if not store_path:
            store_path = "/workspace/.rapport-memories"

        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)

        self.db_path = self.store_path / "memory.db"
        self.chroma_path = self.store_path / "chroma"

        # Configuration variables
        self.embedding_model = os.environ.get(
            "RAPPORT_MEMORIES_EMBEDDING_MODEL",
            os.environ.get("OLLAMA_MODEL", "nomic-embed-text-v2-moe:latest")
        )
        self.ollama_host = os.environ.get(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )
        try:
            self.chunk_size = int(os.environ.get("RAPPORT_MEMORIES_CHUNK_SIZE", 500))
        except ValueError:
            self.chunk_size = 500

        # Initialize SQLite DB schema
        self._init_sqlite()

        # Initialize ChromaDB persistent client if available
        self.chroma_client = None
        self.collection = None
        if CHROMA_AVAILABLE:
            try:
                self.chroma_client = chromadb.PersistentClient(path=str(self.chroma_path))
                self.collection = self.chroma_client.get_or_create_collection(
                    name="rapport_memories"
                )
            except Exception as e:
                print(f"Warning: Failed to initialize ChromaDB ({e}). Falling back to SQLite FTS.", file=sys.stderr)
                self.chroma_client = None
                self.collection = None

    def _init_sqlite(self):
        """Initializes SQLite database schema and Full-Text Search virtual tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Track files processed and their hashes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS indexed_files (
            file_path TEXT PRIMARY KEY,
            file_hash TEXT,
            last_indexed TIMESTAMP
        )
        """)

        # Store general memory metadata
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            title TEXT,
            content TEXT,
            taxonomy TEXT,
            created_at TIMESTAMP
        )
        """)

        # Store chunks mapped to memories
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_id INTEGER,
            chunk_index INTEGER,
            content TEXT,
            chroma_id TEXT,
            FOREIGN KEY(memory_id) REFERENCES memories(id) ON DELETE CASCADE
        )
        """)

        # Create FTS5 virtual table for keyword search fallback
        try:
            cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content, 
                title, 
                taxonomy, 
                content_id UNINDEXED
            );
            """)
        except sqlite3.OperationalError:
            try:
                # FTS4 fallback if FTS5 is not compiled in sqlite
                cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts4(
                    content, 
                    title, 
                    taxonomy, 
                    content_id
                );
                """)
            except sqlite3.OperationalError:
                pass  # Fallback to standard LIKE matching if no FTS is available

        conn.commit()
        conn.close()

    def _get_db_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def sanitize_text(self, text: str) -> str:
        """Removes code blocks, JSON data, and system diagnostics to index clean content."""
        # Remove Markdown code blocks (```code```)
        text = re.sub(r'```[\s\S]*?```', '', text)

        lines = []
        for line in text.splitlines():
            stripped = line.strip()
            # Skip pure JSON lines
            if (stripped.startswith('{') and stripped.endswith('}')) or (stripped.startswith('[') and stripped.endswith(']')):
                try:
                    json.loads(stripped)
                    continue
                except ValueError:
                    pass

            # Skip lines containing secret credentials or environment variable defs
            if re.search(r'(api_key|token|password|credential|secret|auth|private_key)\s*[:=]', stripped, re.IGNORECASE):
                continue

            # Skip sandbox shell outputs or commands
            if stripped.startswith("Task id") or stripped.startswith("Task logs are available at"):
                continue

            lines.append(line)

        cleaned = "\n".join(lines)
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)  # Normalize empty lines
        return cleaned.strip()

    def split_into_chunks(self, text: str) -> List[str]:
        """Splits sanitised text into paragraph-aware chunks based on character limit."""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        current_chunk = []
        current_len = 0

        for p in paragraphs:
            p_len = len(p)
            if current_len + p_len > self.chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                # Add overlap of 1 paragraph if it is not too large
                if len(current_chunk[-1]) < self.chunk_size // 2:
                    current_chunk = [current_chunk[-1], p]
                    current_len = len(current_chunk[0]) + p_len + 2
                else:
                    current_chunk = [p]
                    current_len = p_len
            else:
                current_chunk.append(p)
                current_len += p_len + (2 if current_len > 0 else 0)

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    def _get_embedding(self, text: str) -> List[float]:
        """Generates embedding vector from Ollama API."""
        url = f"{self.ollama_host.rstrip('/')}/api/embeddings"
        data = json.dumps({"model": self.embedding_model, "prompt": text}).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                embedding = res_data.get("embedding")
                if not embedding:
                    raise ValueError("Empty embedding returned by Ollama server")
                return embedding
        except Exception as e:
            raise RuntimeError(f"Failed to fetch embeddings from Ollama model '{self.embedding_model}': {e}")

    def _delete_file_from_indices(self, file_path: Path):
        """Cleans out existing indexed records for a file path to prevent duplicates."""
        conn = self._get_db_connection()
        row = conn.execute("SELECT id FROM memories WHERE file_path = ?", (str(file_path),)).fetchone()
        if row:
            memory_id = row["id"]
            
            # Retrieve Chroma IDs associated with this memory
            chunk_rows = conn.execute("SELECT chroma_id FROM chunks WHERE memory_id = ?", (memory_id,)).fetchall()
            chroma_ids = [r["chroma_id"] for r in chunk_rows]

            # Delete from ChromaDB
            if self.collection and chroma_ids:
                try:
                    self.collection.delete(ids=chroma_ids)
                except Exception as e:
                    print(f"Warning: Failed to delete vector chunks from ChromaDB: {e}", file=sys.stderr)

            # Delete from SQLite Full Text Search
            try:
                conn.execute("DELETE FROM memories_fts WHERE content_id = ?", (memory_id,))
            except Exception:
                pass

            # Cascade delete in SQLite
            conn.execute("DELETE FROM chunks WHERE memory_id = ?", (memory_id,))
            conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))

        conn.execute("DELETE FROM indexed_files WHERE file_path = ?", (str(file_path),))
        conn.commit()
        conn.close()

    def index_memory_files(self, workspace_path: Optional[str] = None) -> Dict[str, int]:
        """Scans workspace directory for memory files and updates databases incrementally."""
        if not workspace_path:
            workspace_path = self.store_path.parent

        workspace_path = Path(workspace_path)
        files_to_index = []

        # Find MEMORY.md at root
        memory_md = workspace_path / "MEMORY.md"
        if memory_md.exists():
            files_to_index.append(memory_md)

        # Find markdown files inside /memory
        memory_dir = workspace_path / "memory"
        if memory_dir.exists() and memory_dir.is_dir():
            files_to_index.extend(memory_dir.glob("*.md"))

        # Find memory files inside agents subdirectory (agent-specific context)
        agents_dir = workspace_path / "agents"
        if agents_dir.exists() and agents_dir.is_dir():
            for agent_subdir in agents_dir.iterdir():
                if agent_subdir.is_dir():
                    agent_memory_md = agent_subdir / "MEMORY.md"
                    if agent_memory_md.exists():
                        files_to_index.append(agent_memory_md)
                    agent_memory_dir = agent_subdir / "memory"
                    if agent_memory_dir.exists() and agent_memory_dir.is_dir():
                        files_to_index.extend(agent_memory_dir.glob("*.md"))

        stats = {"indexed": 0, "skipped": 0, "errors": 0}

        for file_path in files_to_index:
            try:
                # Read content and calculate hash
                content = file_path.read_text(encoding="utf-8")
                file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

                # Check if hash hasn't changed
                conn = self._get_db_connection()
                row = conn.execute(
                    "SELECT file_hash FROM indexed_files WHERE file_path = ?", 
                    (str(file_path),)
                ).fetchone()

                if row and row["file_hash"] == file_hash:
                    conn.close()
                    stats["skipped"] += 1
                    continue

                # Content changed or new file; delete old instances
                self._delete_file_from_indices(file_path)

                # Clean text content
                cleaned_content = self.sanitize_text(content)
                if not cleaned_content:
                    conn.close()
                    stats["skipped"] += 1
                    continue

                # Detect taxonomy/type
                taxonomy = "memory"
                if "2026-" in file_path.name or "2025-" in file_path.name:
                    taxonomy = "daily-log"
                elif file_path.name == "MEMORY.md":
                    taxonomy = "long-term-memory"

                if "agents/" in str(file_path):
                    taxonomy = f"agent-{taxonomy}"

                title = file_path.stem
                created_at = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()

                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO memories (file_path, title, content, taxonomy, created_at) VALUES (?, ?, ?, ?, ?)",
                    (str(file_path), title, cleaned_content, taxonomy, created_at)
                )
                memory_id = cursor.lastrowid

                # Generate chunks and embeddings
                chunks = self.split_into_chunks(cleaned_content)
                for idx, chunk in enumerate(chunks):
                    chroma_id = f"chunk_{memory_id}_{idx}"

                    # Insert chunk metadata
                    cursor.execute(
                        "INSERT INTO chunks (memory_id, chunk_index, content, chroma_id) VALUES (?, ?, ?, ?)",
                        (memory_id, idx, chunk, chroma_id)
                    )

                    # Insert vector in Chroma
                    if self.collection:
                        try:
                            embedding = self._get_embedding(chunk)
                            self.collection.add(
                                ids=[chroma_id],
                                embeddings=[embedding],
                                metadatas=[{
                                    "file_path": str(file_path),
                                    "taxonomy": taxonomy,
                                    "created_at": created_at,
                                    "chunk_index": idx
                                }],
                                documents=[chunk]
                            )
                        except Exception as e:
                            print(f"Warning: Failed to index chunk {chroma_id} in Chroma ({e}). Storing in SQLite only.", file=sys.stderr)

                # Index in FTS Table
                try:
                    cursor.execute(
                        "INSERT INTO memories_fts (content, title, taxonomy, content_id) VALUES (?, ?, ?, ?)",
                        (cleaned_content, title, taxonomy, memory_id)
                    )
                except Exception:
                    pass

                # Store file hash
                cursor.execute(
                    "INSERT OR REPLACE INTO indexed_files (file_path, file_hash, last_indexed) VALUES (?, ?, ?)",
                    (str(file_path), file_hash, datetime.now().isoformat())
                )

                conn.commit()
                conn.close()
                stats["indexed"] += 1

            except Exception as e:
                print(f"Error indexing file {file_path}: {e}", file=sys.stderr)
                stats["errors"] += 1

        return stats

    def add_memory_entry(self, title: str, content: str, taxonomy: str, date_str: Optional[str] = None, workspace_path: Optional[str] = None) -> str:
        """Helper to create a markdown memory file structure and register it in the databases."""
        if not workspace_path:
            workspace_path = self.store_path.parent
        workspace_path = Path(workspace_path)

        memory_dir = workspace_path / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)

        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        sanitized_title = re.sub(r'[^\w\-]', '_', title.lower()).strip('_')
        filename = f"{date_str}_{sanitized_title}.md"
        file_path = memory_dir / filename

        # Wrap in Standard markdown headers
        markdown_body = f"""---
title: {title}
date: {date_str}
taxonomy: {taxonomy}
---

# {title}

{content.strip()}
"""
        file_path.write_text(markdown_body, encoding="utf-8")

        # Incrementally index
        self.index_memory_files(workspace_path=workspace_path)
        return str(file_path)

    def semantic_search(self, query: str, limit: int = 5, threshold: float = 0.5) -> List[MemorySearchResult]:
        """Performs a vector semantic search over memories with a fallback to SQLite keyword FTS."""
        results = []

        # Try Chroma vector store
        if self.collection:
            try:
                query_emb = self._get_embedding(query)
                chroma_res = self.collection.query(
                    query_embeddings=[query_emb],
                    n_results=limit
                )

                if chroma_res and chroma_res["ids"] and chroma_res["ids"][0]:
                    ids = chroma_res["ids"][0]
                    distances = chroma_res["distances"][0] if "distances" in chroma_res else [0.0] * len(ids)
                    documents = chroma_res["documents"][0]
                    metadatas = chroma_res["metadatas"][0]

                    for idx in range(len(ids)):
                        # Score calculation (1.0 / (1.0 + L2_distance))
                        distance = distances[idx]
                        similarity = 1.0 / (1.0 + distance)

                        if similarity >= threshold:
                            results.append(MemorySearchResult(
                                content=documents[idx],
                                metadata=metadatas[idx],
                                score=similarity
                            ))

                results.sort(key=lambda x: x.score, reverse=True)
                return results[:limit]

            except Exception as e:
                print(f"Warning: Semantic search failed ({e}). Falling back to SQLite Full Text Search.", file=sys.stderr)

        # Fallback keyword matching in SQLite
        conn = self._get_db_connection()
        cursor = conn.cursor()

        try:
            clean_query = re.sub(r'[^\w\s]', ' ', query).strip()
            if clean_query:
                rows = cursor.execute("""
                SELECT m.content, m.title, m.taxonomy, m.created_at, m.file_path
                FROM memories_fts f
                JOIN memories m ON m.id = f.content_id
                WHERE memories_fts MATCH ?
                LIMIT ?
                """, (clean_query, limit)).fetchall()

                for row in rows:
                    results.append(MemorySearchResult(
                        content=row["content"],
                        metadata={
                            "file_path": row["file_path"],
                            "taxonomy": row["taxonomy"],
                            "created_at": row["created_at"]
                        },
                        score=0.5  # Fixed score for keyword fallback
                    ))
        except sqlite3.OperationalError:
            # Table or feature missing, run standard LIKE
            like_query = f"%{query}%"
            rows = cursor.execute("""
            SELECT content, title, taxonomy, created_at, file_path
            FROM memories
            WHERE content LIKE ? OR title LIKE ?
            LIMIT ?
            """, (like_query, like_query, limit)).fetchall()

            for row in rows:
                results.append(MemorySearchResult(
                    content=row["content"],
                    metadata={
                        "file_path": row["file_path"],
                        "taxonomy": row["taxonomy"],
                        "created_at": row["created_at"]
                    },
                    score=0.5
                ))

        conn.close()
        return results

    def get_recent_context(self, tokens_limit: int = 1000) -> str:
        """Retrieves recently indexed chunks, formatted as a continuous context block."""
        char_limit = tokens_limit * 4
        conn = self._get_db_connection()
        rows = conn.execute("""
        SELECT c.content, m.title, m.created_at, m.taxonomy
        FROM chunks c
        JOIN memories m ON m.id = c.memory_id
        ORDER BY m.created_at DESC, c.chunk_index ASC
        """).fetchall()

        context_parts = []
        current_len = 0

        for row in rows:
            formatted = f"[{row['created_at']}][{row['taxonomy']}] {row['title']}:\n{row['content']}"
            if current_len + len(formatted) > char_limit:
                break
            context_parts.append(formatted)
            current_len += len(formatted) + 2

        conn.close()
        return "\n\n---\n\n".join(context_parts)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Provides database metrics and indexing statistics."""
        conn = self._get_db_connection()
        cursor = conn.cursor()

        files_count = cursor.execute("SELECT COUNT(*) FROM indexed_files").fetchone()[0]
        memories_count = cursor.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        chunks_count = cursor.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

        db_size_bytes = 0
        if self.db_path.exists():
            db_size_bytes = self.db_path.stat().st_size

        conn.close()

        return {
            "indexed_files": files_count,
            "stored_memories": memories_count,
            "total_chunks": chunks_count,
            "database_size_bytes": db_size_bytes,
            "chroma_available": CHROMA_AVAILABLE and self.collection is not None,
            "embedding_model": self.embedding_model
        }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Rapport Memories CLI - sqlite + vector database memory manager")
    parser.add_argument("--store-path", default=os.environ.get("RAPPORT_MEMORIES_STORE_PATH", "/workspace/.rapport-memories"),
                        help="Path to store SQLite database and ChromaDB vector files")
    parser.add_argument("--workspace", default=None,
                        help="Path to workspace containing memories (defaults to parent of store-path)")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands")

    # Command: init
    subparsers.add_parser("init", help="Initialize databases in path")

    # Command: index
    subparsers.add_parser("index", help="Scan and index memory files inside workspace")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a new memory record and index it")
    add_parser.add_argument("--title", required=True, help="Title of memory entry")
    add_parser.add_argument("--content", required=True, help="Content string of memory entry")
    add_parser.add_argument("--taxonomy", required=True, help="Category/Taxonomy tag (e.g. conversation, taxonomy, decision)")
    add_parser.add_argument("--date", help="Date in YYYY-MM-DD format (defaults to today)")

    # Command: search
    search_parser = subparsers.add_parser("search", help="Perform semantic search on stored memories")
    search_parser.add_argument("query", help="Text query to search for")
    search_parser.add_argument("--limit", type=int, default=5, help="Maximum results to return")
    search_parser.add_argument("--threshold", type=float, default=0.5, help="Minimum matching similarity threshold")

    # Command: stats
    subparsers.add_parser("stats", help="Get statistics of indexed database")

    args = parser.parse_args()

    # Create memory RAG client
    rag = MemoryRAG(store_path=args.store_path)

    if args.command == "init":
        print(f"Memory store initialized at: {args.store_path}")
        print(f"ChromaDB library available: {CHROMA_AVAILABLE}")
        sys.exit(0)

    elif args.command == "index":
        workspace_dir = args.workspace or rag.store_path.parent
        print(f"Indexing memory files under: {workspace_dir}")
        stats = rag.index_memory_files(workspace_path=workspace_dir)
        print("Indexing completed:")
        print(json.dumps(stats, indent=2))

    elif args.command == "add":
        workspace_dir = args.workspace or rag.store_path.parent
        print(f"Adding memory entry: '{args.title}'...")
        file_saved = rag.add_memory_entry(
            title=args.title,
            content=args.content,
            taxonomy=args.taxonomy,
            date_str=args.date,
            workspace_path=workspace_dir
        )
        print(f"Memory entry saved to: {file_saved}")
        print("Indexed successfully.")

    elif args.command == "search":
        print(f"Searching memory for: '{args.query}' (limit={args.limit}, threshold={args.threshold})")
        results = rag.semantic_search(query=args.query, limit=args.limit, threshold=args.threshold)
        if not results:
            print("No matching memories found.")
        else:
            for i, res in enumerate(results):
                print(f"\n--- Match #{i+1} [Similarity: {res.score:.4f}] ---")
                print(f"Source: {res.metadata.get('file_path')}")
                print(f"Taxonomy: {res.metadata.get('taxonomy')}")
                print(f"Created: {res.metadata.get('created_at')}")
                print(f"Content:\n{res.content}")

    elif args.command == "stats":
        stats = rag.get_memory_stats()
        print("Memory Store Metrics:")
        print(json.dumps(stats, indent=2))
