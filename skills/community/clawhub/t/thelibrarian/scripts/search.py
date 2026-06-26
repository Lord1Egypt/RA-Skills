#!/usr/bin/env python3
"""
Search a TurboVec quantized document index with hybrid BM25 + Flashrank.

Usage:
    python search.py "attachment theory" --index index/my_library
    python search.py "secure base" --index index/my_library --expand 1 --top-k 5
    python search.py "habit formation" --index index/my_library --hybrid --rerank

The --expand N flag includes N chunks before and after each result for context.
The --hybrid flag combines vector search with BM25 keyword search.
The --rerank flag uses Flashrank to rerank results for better accuracy.
"""

import sys
import json
import time
import argparse
import pickle
from pathlib import Path

try:
    import turbovec
    ENGINE = 'turbovec'
except ImportError:
    print("ERROR: TurboVec not available. Install with: pip install turbovec")
    print("BLAS library required. Install with: sudo apt install libblas3")
    print("")
    print("Run via the wrapper script (recommended):")
    print("  ./scripts/librarian.sh search <query> <index>")
    print("")
    print("Or set LD_PRELOAD before Python starts:")
    print("  LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libblas.so.3 python search.py ...")
    sys.exit(1)

import numpy as np
import requests

# Optional: BM25 for hybrid search
try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False

# Optional: Flashrank for reranking
try:
    from flashrank import Ranker, RerankRequest
    FLASHRANK_AVAILABLE = True
except ImportError:
    FLASHRANK_AVAILABLE = False

# Configuration
DEFAULT_OLLAMA_API = "http://host.docker.internal:11434"
DEFAULT_MODEL = "nomic-embed-text:v1.5"


def get_embedding(text: str, model: str, api_url: str) -> list[float]:
    """Get embedding from Ollama API."""
    response = requests.post(
        f"{api_url}/api/embeddings",
        json={"model": model, "prompt": text},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["embedding"]


def load_index(index_dir: Path) -> tuple:
    """Load TurboVec index and chunks."""
    index_file = index_dir / "library.qindex"
    chunks_file = index_dir / "chunks.json"
    stats_file = index_dir / "stats.json"
    bm25_file = index_dir / "bm25_index.pkl"
    
    if not index_file.exists():
        raise FileNotFoundError(f"Index not found: {index_file}")
    
    if not chunks_file.exists():
        raise FileNotFoundError(f"Chunks not found: {chunks_file}")
    
    # Load TurboVec index
    index = turbovec.TurboQuantIndex.load(str(index_file))
    
    # Load chunks
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # Load stats
    stats = {}
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    
    # Load BM25 if available
    bm25 = None
    if bm25_file.exists():
        try:
            with open(bm25_file, 'rb') as f:
                bm25 = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load BM25 index: {e}")
    
    return index, chunks, stats, bm25


def expand_chunk(chunk_pos: int, chunks: list[dict], context: int = 1) -> dict:
    """Expand a chunk by including adjacent chunks from the same source."""
    if chunk_pos < 0 or chunk_pos >= len(chunks):
        return None
    
    target = chunks[chunk_pos]
    source_file = target["source_file"]
    
    # Collect adjacent chunks from same source
    before_chunks = []
    after_chunks = []
    
    # Look backwards
    for i in range(1, context + 1):
        prev_pos = chunk_pos - i
        if prev_pos >= 0 and chunks[prev_pos]["source_file"] == source_file:
            before_chunks.insert(0, chunks[prev_pos])
        else:
            break
    
    # Look forwards
    for i in range(1, context + 1):
        next_pos = chunk_pos + i
        if next_pos < len(chunks) and chunks[next_pos]["source_file"] == source_file:
            after_chunks.append(chunks[next_pos])
        else:
            break
    
    # Combine text
    expanded_text = "".join(c["text"] for c in before_chunks) + target["text"] + "".join(c["text"] for c in after_chunks)
    
    return {
        "expanded_text": expanded_text,
        "context_before": len(before_chunks),
        "context_after": len(after_chunks),
        "chunk_ids": [c["id"] for c in before_chunks] + [target["id"]] + [c["id"] for c in after_chunks],
        "has_more_before": chunk_pos > 0 and chunks[chunk_pos - 1]["source_file"] == source_file,
        "has_more_after": chunk_pos < len(chunks) - 1 and chunks[chunk_pos + 1]["source_file"] == source_file,
    }


def vector_search(query: str, index, chunks: list[dict], model: str, api_url: str,
                  top_k: int = 5) -> tuple:
    """Pure vector search with TurboVec."""
    # Get query embedding
    query_emb = get_embedding(query, model, api_url)
    query_vec = np.array([query_emb], dtype=np.float32)
    
    # Search
    start = time.time()
    distances, indices = index.search(query_vec, top_k)
    search_time = time.time() - start
    
    # Format results
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        
        idx = int(idx)
        chunk = chunks[idx]
        
        # Convert distance to similarity score
        score = 1.0 / (1.0 + float(dist) / 100.0)
        
        results.append({
            "book": chunk["book"],
            "source_file": chunk["source_file"],
            "text": chunk["text"],
            "score": round(score, 4),
            "distance": round(float(dist), 4),
            "chunk_id": chunk["id"],
            "chunk_pos": idx,
        })
    
    return results, search_time


def bm25_search(query: str, bm25, chunks: list[dict], top_k: int = 5) -> tuple:
    """Pure BM25 keyword search."""
    start = time.time()
    
    # Tokenize query
    query_tokens = [t for t in query.lower().split() if t.isalnum()]
    
    # Get BM25 scores
    scores = bm25.get_scores(query_tokens)
    
    # Get top-k indices
    top_indices = np.argsort(scores)[::-1][:top_k]
    
    search_time = time.time() - start
    
    # Format results
    results = []
    for idx in top_indices:
        if scores[idx] <= 0:
            continue
        
        chunk = chunks[idx]
        results.append({
            "book": chunk["book"],
            "source_file": chunk["source_file"],
            "text": chunk["text"],
            "score": round(float(scores[idx]) / max(scores) if max(scores) > 0 else 0, 4),
            "bm25_score": round(float(scores[idx]), 4),
            "chunk_id": chunk["id"],
            "chunk_pos": idx,
        })
    
    return results, search_time


def hybrid_search(query: str, index, chunks: list[dict], bm25, model: str, api_url: str,
                  top_k: int = 5, vector_weight: float = 0.5) -> tuple:
    """Combine vector and BM25 search."""
    # Get more results from each to merge
    fetch_k = top_k * 3
    
    # Vector search
    vector_results, vector_time = vector_search(query, index, chunks, model, api_url, fetch_k)
    
    # BM25 search
    bm25_results, bm25_time = bm25_search(query, bm25, chunks, fetch_k)
    
    # Combine scores
    combined = {}
    
    # Add vector results
    for r in vector_results:
        pos = r["chunk_pos"]
        combined[pos] = {
            **r,
            "vector_score": r["score"],
            "bm25_score": 0.0,
        }
    
    # Add/merge BM25 results
    max_bm25 = max((r["bm25_score"] for r in bm25_results), default=1.0)
    for r in bm25_results:
        pos = r["chunk_pos"]
        normalized_bm25 = r["bm25_score"] / max_bm25 if max_bm25 > 0 else 0
        
        if pos in combined:
            combined[pos]["bm25_score"] = normalized_bm25
        else:
            combined[pos] = {
                **r,
                "vector_score": 0.0,
                "bm25_score": normalized_bm25,
            }
    
    # Calculate combined scores
    for pos, result in combined.items():
        result["combined_score"] = (
            vector_weight * result["vector_score"] +
            (1 - vector_weight) * result["bm25_score"]
        )
    
    # Sort by combined score
    sorted_results = sorted(combined.values(), key=lambda x: x["combined_score"], reverse=True)[:top_k]
    
    # Set final score
    for r in sorted_results:
        r["score"] = r["combined_score"]
    
    return sorted_results, vector_time + bm25_time


def rerank_results(query: str, results: list[dict], top_k: int = 5) -> tuple:
    """Rerank results using Flashrank."""
    if not FLASHRANK_AVAILABLE:
        print("Warning: Flashrank not available. Install with: pip install flashrank")
        return results, 0.0
    
    start = time.time()
    
    # Load reranker (small, fast model)
    reranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
    
    # Prepare passages
    passages = [{"id": r["chunk_pos"], "text": r["text"], "title": r["book"]} for r in results]
    
    # Rerank
    rerank_request = RerankRequest(query=query, passages=passages)
    reranked = reranker.rerank(rerank_request)
    
    # Reorder results by reranked scores
    final_results = []
    for item in reranked[:top_k]:
        idx = item["id"]
        for r in results:
            if r["chunk_pos"] == idx:
                r["rerank_score"] = item["score"]
                r["score"] = item["score"]  # Use rerank score as final score
                final_results.append(r)
                break
    
    rerank_time = time.time() - start
    return final_results, rerank_time


def format_results(query: str, results: list[dict], search_time: float, 
                   show_text: bool = True, search_type: str = "vector"):
    """Format results for display."""
    print("=" * 70)
    print(f"🔍 Query: {query}")
    print(f"⏱️ Search time: {search_time*1000:.1f}ms ({search_type})")
    print("=" * 70)
    
    if not results:
        print("No results found.")
        return
    
    for i, r in enumerate(results, 1):
        score_label = "Rerank" if "rerank_score" in r else "Score"
        print(f"\n[{i}] {score_label}: {r['score']:.4f}")
        if "vector_score" in r:
            print(f"    Vector: {r['vector_score']:.4f} | BM25: {r['bm25_score']:.4f}")
        print(f"    📖 Book: {r['book']}")
        print(f"    📄 File: {r['source_file']}")
        
        if show_text:
            text = r.get("expanded_text", r["text"])
            if len(text) > 500:
                text = text[:500] + "..."
            
            if "context_before" in r:
                print(f"    📝 Text (expanded: {r['context_before']} before, {r['context_after']} after):")
            else:
                print(f"    📝 Text:")
            print(f"    {text[:300]}{'...' if len(text) > 300 else ''}")


def main():
    parser = argparse.ArgumentParser(description="Search TurboVec document index")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--index", "-i", required=True, help="Index directory")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Embedding model (default: {DEFAULT_MODEL})")
    parser.add_argument("--api", "-a", default=DEFAULT_OLLAMA_API, help=f"Ollama API URL (default: {DEFAULT_OLLAMA_API})")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--expand", "-e", type=int, default=0, help="Expand chunks with N context chunks on each side")
    parser.add_argument("--hybrid", action="store_true", help="Use hybrid vector + BM25 search")
    parser.add_argument("--vector-weight", type=float, default=0.5, help="Weight for vector scores in hybrid (default: 0.5)")
    parser.add_argument("--rerank", action="store_true", help="Rerank results with Flashrank")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--no-text", action="store_true", help="Hide text in output")
    args = parser.parse_args()
    
    index_dir = Path(args.index)
    
    try:
        # Load index
        index, chunks, stats, bm25 = load_index(index_dir)
        
        # Get model from stats if available
        model = stats.get("embedding_model", args.model)
        
        # Check BM25 availability
        if args.hybrid and bm25 is None:
            print("Warning: BM25 index not found. Using pure vector search.")
            args.hybrid = False
        
        # Search
        if args.hybrid:
            results, search_time = hybrid_search(
                args.query, index, chunks, bm25, model, args.api,
                top_k=args.top_k * 2 if args.rerank else args.top_k,  # Fetch more for reranking
                vector_weight=args.vector_weight
            )
            search_type = "hybrid"
        else:
            results, search_time = vector_search(
                args.query, index, chunks, model, args.api,
                top_k=args.top_k * 2 if args.rerank else args.top_k
            )
            search_type = "vector"
        
        # Rerank if requested
        if args.rerank and len(results) > 0:
            results, rerank_time = rerank_results(args.query, results, args.top_k)
            search_time += rerank_time
            search_type = "hybrid+rerank" if args.hybrid else "vector+rerank"
        
        # Limit to top_k after reranking
        results = results[:args.top_k]
        
        # Expand if requested
        if args.expand > 0:
            for r in results:
                if "chunk_pos" in r:
                    expanded = expand_chunk(r["chunk_pos"], chunks, context=args.expand)
                    if expanded:
                        r["expanded_text"] = expanded["expanded_text"]
                        r["context_before"] = expanded["context_before"]
                        r["context_after"] = expanded["context_after"]
        
        # Output
        if args.json:
            output = {
                "query": args.query,
                "engine": "turbovec",
                "search_type": search_type,
                "bit_width": stats.get("bit_width", 4),
                "search_time_ms": round(search_time * 1000, 2),
                "total_results": len(results),
                "expand_context": args.expand,
                "results": results,
            }
            print(json.dumps(output, indent=2))
        else:
            format_results(args.query, results, search_time, show_text=not args.no_text, search_type=search_type)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Run 'python scripts/build_index.py' first to create the index.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()