#!/usr/bin/env python3
"""
RAG Pipeline Starter: Vector Store Manager
Manages vector store operations: create, update, search, and maintain indexes.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import hashlib


class VectorStore:
    """Simple in-memory vector store with file persistence."""
    
    def __init__(self, index_dir: str):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.docs_file = self.index_dir / "documents.json"
        self.metadata_file = self.index_dir / "metadata.json"
        self.documents = {}
        self.metadata = {}
        self._load()
    
    def _load(self):
        """Load index from disk."""
        if self.docs_file.exists():
            self.documents = json.loads(self.docs_file.read_text())
        if self.metadata_file.exists():
            self.metadata = json.loads(self.metadata_file.read_text())
    
    def _save(self):
        """Save index to disk."""
        self.docs_file.write_text(json.dumps(self.documents, indent=2))
        self.metadata_file.write_text(json.dumps(self.metadata, indent=2))
    
    def add_documents(self, chunks: Dict[str, str], metadata: Optional[Dict] = None):
        """Add documents to the index."""
        for doc_id, content in chunks.items():
            doc_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            self.documents[doc_id] = {
                'content': content,
                'hash': doc_hash,
                'id': doc_id
            }
            
            if metadata:
                self.metadata[doc_id] = metadata.get(doc_id, {})
        
        self._save()
        print(f"Added {len(chunks)} documents to index")
    
    def search(self, query: str, top_k: int = 5, embedding_model: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search the index. 
        In production, use actual embeddings. This is a simple keyword-based mock.
        """
        query_words = set(query.lower().split())
        
        results = []
        for doc_id, doc in self.documents.items():
            content = doc.get('content', '')
            doc_words = set(content.lower().split())
            
            # Simple keyword overlap scoring
            if query_words & doc_words:
                score = len(query_words & doc_words) / len(query_words | doc_words)
            else:
                score = 0.0
            
            if score > 0:
                results.append({
                    'doc_id': doc_id,
                    'score': score,
                    'content': content[:200] + "..." if len(content) > 200 else content,
                    'metadata': self.metadata.get(doc_id, {})
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        return {
            'total_documents': len(self.documents),
            'index_path': str(self.index_dir),
            'embedding_model': self.metadata.get('_config', {}).get('embedding_model', 'none'),
            'created': self.metadata.get('_config', {}).get('created', 'unknown')
        }
    
    def delete_document(self, doc_id: str):
        """Delete a document from the index."""
        if doc_id in self.documents:
            del self.documents[doc_id]
            if doc_id in self.metadata:
                del self.metadata[doc_id]
            self._save()
            print(f"Deleted document: {doc_id}")
        else:
            print(f"Document not found: {doc_id}")
    
    def clear(self):
        """Clear all documents from the index."""
        self.documents = {}
        self.metadata = {}
        self._save()
        print("Index cleared")


def load_chunks(chunks_dir: str) -> Dict[str, str]:
    """Load chunks from directory."""
    chunks = {}
    path = Path(chunks_dir)
    
    if not path.is_dir():
        return chunks
    
    for f in sorted(path.glob("*.txt")):
        doc_id = f.stem
        chunks[doc_id] = f.read_text(encoding='utf-8', errors='ignore')
    
    return chunks


def create_index(chunks_dir: str, index_dir: str, embedding_model: str):
    """Create a new vector store index from chunks."""
    print(f"Loading chunks from: {chunks_dir}")
    chunks = load_chunks(chunks_dir)
    
    if not chunks:
        print("Error: No chunks found")
        sys.exit(1)
    
    print(f"Loaded {len(chunks)} chunks")
    
    # Create vector store
    store = VectorStore(index_dir)
    
    # Add documents
    metadata = {
        '_config': {
            'embedding_model': embedding_model,
            'created': str(Path(__file__).stat().st_mtime)
        }
    }
    store.add_documents(chunks, metadata)
    
    print(f"Index created at: {index_dir}")
    return store


def search_index(index_dir: str, query: str, top_k: int):
    """Search the vector store."""
    store = VectorStore(index_dir)
    results = store.search(query, top_k)
    
    print(f"\n=== Search Results for: '{query}' ===\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [Score: {r['score']:.3f}] {r['doc_id']}")
        print(f"   {r['content']}\n")
    
    return results


def update_index(index_dir: str, chunks_dir: str):
    """Update index with new chunks."""
    store = VectorStore(index_dir)
    
    print(f"Loading new chunks from: {chunks_dir}")
    chunks = load_chunks(chunks_dir)
    
    if not chunks:
        print("No new chunks found")
        return
    
    # Get existing doc IDs
    existing_ids = set(store.documents.keys())
    new_chunks = {k: v for k, v in chunks.items() if k not in existing_ids}
    
    if new_chunks:
        store.add_documents(new_chunks)
        print(f"Added {len(new_chunks)} new documents")
    else:
        print("All chunks already in index")


def show_stats(index_dir: str):
    """Show index statistics."""
    store = VectorStore(index_dir)
    stats = store.get_stats()
    
    print("=== Index Statistics ===")
    print(f"Total documents: {stats['total_documents']}")
    print(f"Index path: {stats['index_path']}")
    print(f"Embedding model: {stats['embedding_model']}")


def main():
    parser = argparse.ArgumentParser(description="RAG Vector Store Manager")
    
    # Mutually exclusive operations
    ops = parser.add_mutually_exclusive_group(required=True)
    ops.add_argument("--create", action="store_true", help="Create new index")
    ops.add_argument("--search", action="store_true", help="Search index")
    ops.add_argument("--update", action="store_true", help="Update index with new documents")
    ops.add_argument("--stats", action="store_true", help="Show index statistics")
    ops.add_argument("--clear", action="store_true", help="Clear all documents")
    ops.add_argument("--delete", type=str, metavar="DOC_ID", help="Delete a specific document")
    
    # Common arguments
    parser.add_argument("--chunks", type=str, help="Directory with chunked text files")
    parser.add_argument("--index", type=str, required=True, help="Vector store directory")
    parser.add_argument("--embedding", type=str, default="sentence-transformers/all-MiniLM-L6-v2",
                        help="Embedding model to use")
    parser.add_argument("--query", type=str, help="Search query (for --search)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (for --search)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.create and not args.chunks:
        parser.error("--create requires --chunks")
    
    if args.search and not args.query:
        parser.error("--search requires --query")
    
    # Execute operation
    if args.create:
        create_index(args.chunks, args.index, args.embedding)
    
    elif args.search:
        search_index(args.index, args.query, args.top_k)
    
    elif args.update:
        if not args.chunks:
            parser.error("--update requires --chunks")
        update_index(args.index, args.chunks)
    
    elif args.stats:
        show_stats(args.index)
    
    elif args.clear:
        store = VectorStore(args.index)
        confirm = input("Clear all documents? (yes/no): ")
        if confirm.lower() == 'yes':
            store.clear()
        else:
            print("Cancelled")
    
    elif args.delete:
        store = VectorStore(args.index)
        store.delete_document(args.delete)


if __name__ == "__main__":
    main()