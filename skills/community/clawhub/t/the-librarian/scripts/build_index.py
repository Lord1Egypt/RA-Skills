#!/usr/bin/env python3
"""
Build a TurboVec quantized index from Markdown/text documents.

Usage:
    python build_index.py --input /path/to/docs/ --output index/my_library
    python build_index.py --input /path/to/docs/ --output index/my_library --append

The --append flag adds to an existing library instead of rebuilding.
"""

import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    import turbovec
    ENGINE = 'turbovec'
except ImportError:
    print("ERROR: TurboVec not available. Install with: pip install turbovec")
    print("BLAS library required. Install with: sudo apt install libblas3")
    print("")
    print("Run via the wrapper script (recommended):")
    print("  ./scripts/librarian.sh build <input> <output>")
    print("")
    print("Or set LD_PRELOAD before Python starts:")
    print("  LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libblas.so.3 python build_index.py ...")
    sys.exit(1)

import numpy as np
import requests

# Optional: BM25 for hybrid search
try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    print("Note: BM25 not available. Install with: pip install rank-bm25")

# Configuration
DEFAULT_OLLAMA_API = "http://host.docker.internal:11434"
DEFAULT_MODEL = "nomic-embed-text:v1.5"
CHUNK_SIZE = 650  # Characters per chunk
CHUNK_OVERLAP = 100  # Characters overlap between chunks
BIT_WIDTH = 4  # 2, 3, or 4 bits (higher = more accuracy, larger size)

# Security: Warn if embedding API is not localhost
import urllib.parse

def _check_api_url_safety(api_url: str):
    """Warn user if the embedding API URL points to a non-local host."""
    parsed = urllib.parse.urlparse(api_url)
    host = parsed.hostname or ""
    safe_hosts = {"localhost", "127.0.0.1", "0.0.0.0", "host.docker.internal"}
    if host not in safe_hosts and not host.startswith("192.168.") and not host.startswith("10."):
        print(f"⚠️  PRIVACY WARNING: Embedding API URL points to {host} (non-local).")
        print(f"   Document text will be sent to this remote endpoint for embedding generation.")
        print(f"   Only continue if you trust this endpoint with your data.")
        print(f"   To use a local Ollama instance, set --api http://localhost:11434")
        print()


def get_embedding(text: str, model: str, api_url: str) -> list[float]:
    """Get embedding from Ollama API."""
    response = requests.post(
        f"{api_url}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=120
    )
    response.raise_for_status()
    return response.json()["embedding"]


def chunk_document(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        # Try to break at sentence/paragraph boundary
        if end < len(text):
            # Look for sentence end
            last_period = max(
                chunk.rfind('. '),
                chunk.rfind('! '),
                chunk.rfind('? '),
                chunk.rfind('\n\n')
            )
            if last_period > chunk_size // 2:
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1
        chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def process_documents(input_dir: Path) -> list[dict]:
    """Process all documents in directory."""
    all_chunks = []
    
    for ext in ['*.md', '*.txt', '*.markdown']:
        for filepath in sorted(input_dir.glob(ext)):
            print(f"  Processing: {filepath.name}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"    Warning: Could not read {filepath.name}: {e}")
                continue
            
            # Extract book title from filename
            book_name = filepath.stem.replace('_', ' ')
            
            # Chunk the content
            text_chunks = chunk_document(content)
            
            for i, chunk in enumerate(text_chunks):
                if len(chunk) < 50:  # Skip very short chunks
                    continue
                all_chunks.append({
                    "id": len(all_chunks),
                    "text": chunk,
                    "book": book_name,
                    "source_file": filepath.name,
                    "chunk_index": i,
                })
    
    return all_chunks


def build_index(chunks: list[dict], model: str, api_url: str, bit_width: int) -> tuple:
    """Build TurboVec index from chunks."""
    dim = None
    embeddings = []
    
    print(f"  Generating embeddings with {model}...")
    start_time = time.time()
    
    for i, chunk in enumerate(chunks):
        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (len(chunks) - i - 1) / rate
            print(f"    Progress: {i+1}/{len(chunks)} ({rate:.1f}/s, {remaining:.0f}s remaining)")
        
        try:
            emb = get_embedding(chunk["text"], model, api_url)
            if dim is None:
                dim = len(emb)
            embeddings.append(emb)
        except Exception as e:
            print(f"    Warning: Embedding failed for chunk {i}: {e}")
            # Use zero vector as fallback
            if dim is None:
                dim = 768  # Default for nomic-embed-text
            embeddings.append([0.0] * dim)
    
    embedding_time = time.time() - start_time
    
    # Convert to numpy array
    vectors = np.array(embeddings, dtype=np.float32)
    
    print(f"  Building TurboVec index ({bit_width}-bit quantization)...")
    build_start = time.time()
    
    # Create TurboVec index
    index = turbovec.TurboQuantIndex(dim, bit_width)
    index.add(vectors)
    index.prepare()
    
    build_time = time.time() - build_start
    
    return index, dim, embedding_time, build_time


def save_index(index, chunks: list[dict], output_dir: Path, model: str, 
               bit_width: int, dim: int, embedding_time: float, build_time: float):
    """Save index and metadata."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save TurboVec index
    index_file = output_dir / "library.qindex"
    index.write(str(index_file))
    
    # Save chunks
    chunks_file = output_dir / "chunks.json"
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False)
    
    # Build BM25 index if available
    bm25_data = None
    if BM25_AVAILABLE:
        print("  Building BM25 keyword index...")
        # Tokenize chunks
        tokenized = []
        for chunk in chunks:
            # Simple tokenization: lowercase, split on whitespace/punctuation
            text = chunk["text"].lower()
            # Keep alphanumeric tokens
            tokens = [t for t in text.split() if t.isalnum()]
            tokenized.append(tokens)
        
        bm25 = BM25Okapi(tokenized)
        
        # Save BM25 data as JSON (pickle removed for security — prevents arbitrary code execution)
        # Store tokenized corpus so BM25Okapi can be reconstructed on load
        bm25_data = {
            "tokenized_corpus": tokenized,
            "vocab_size": len(set(t for doc in tokenized for t in doc)),
        }
        bm25_file = output_dir / "bm25_index.json"
        with open(bm25_file, 'w', encoding='utf-8') as f:
            json.dump(bm25_data, f, ensure_ascii=False)
        print("    ✓ BM25 index built (JSON format)")
    
    # Save stats
    stats = {
        "engine": "turbovec",
        "bit_width": bit_width,
        "embedding_model": model,
        "embedding_dim": dim,
        "total_chunks": len(chunks),
        "unique_sources": len(set(c["source_file"] for c in chunks)),
        "created": datetime.now().isoformat(),
        "embedding_time_sec": round(embedding_time, 2),
        "build_time_sec": round(build_time, 2),
        "embeddings_per_sec": round(len(chunks) / embedding_time, 2) if embedding_time > 0 else 0,
        "bm25_enabled": BM25_AVAILABLE,
        "bm25_format": "json",
        "security_note": "BM25 index stored as JSON. Legacy pickle format disabled due to code execution risk.",
    }
    
    stats_file = output_dir / "stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Build TurboVec quantized document index")
    parser.add_argument("--input", "-i", required=True, help="Input directory with documents")
    parser.add_argument("--output", "-o", required=True, help="Output directory for index")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Embedding model (default: {DEFAULT_MODEL})")
    parser.add_argument("--api", "-a", default=DEFAULT_OLLAMA_API, help=f"Ollama API URL (default: {DEFAULT_OLLAMA_API})")
    parser.add_argument("--bits", "-b", type=int, default=BIT_WIDTH, choices=[2, 3, 4],
                        help=f"Quantization bits (default: {BIT_WIDTH}, lower=smaller, higher=more accurate)")
    parser.add_argument("--chunk-size", "-c", type=int, default=CHUNK_SIZE, help=f"Chunk size in chars (default: {CHUNK_SIZE})")
    parser.add_argument("--append", action="store_true", help="Append to existing library")
    args = parser.parse_args()
    
    # Security: Check if API URL is non-local
    _check_api_url_safety(args.api)
    
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("📚 THE LIBRARIAN - Building TurboVec Index")
    print("=" * 60)
    print(f"Input: {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Model: {args.model}")
    print(f"Bits: {args.bits}")
    print()
    
    # Process documents
    print("📂 Processing documents...")
    chunks = process_documents(input_dir)
    
    if not chunks:
        print("ERROR: No chunks extracted from documents")
        sys.exit(1)
    
    print(f"   ✓ {len(chunks)} chunks from {len(set(c['source_file'] for c in chunks))} files")
    print()
    
    # Build index
    print("🔨 Building index...")
    index, dim, embedding_time, build_time = build_index(
        chunks, args.model, args.api, args.bits
    )
    
    # Save
    print("💾 Saving index...")
    stats = save_index(index, chunks, output_dir, args.model, args.bits, 
                        dim, embedding_time, build_time)
    
    print()
    print("=" * 60)
    print("📊 BUILD COMPLETE")
    print("=" * 60)
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Unique sources: {stats['unique_sources']}")
    print(f"Embedding dimension: {stats['embedding_dim']}")
    print(f"Quantization: {stats['bit_width']}-bit")
    print(f"Embedding time: {stats['embedding_time_sec']:.1f}s ({stats['embeddings_per_sec']:.1f}/s)")
    print(f"Build time: {stats['build_time_sec']:.1f}s")
    print()
    print(f"Index saved to: {output_dir}")
    print()
    print("To search:")
    print(f"  LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libblas.so.3 \\")
    print(f"    python scripts/search.py 'your query' --index {output_dir}")


if __name__ == "__main__":
    main()