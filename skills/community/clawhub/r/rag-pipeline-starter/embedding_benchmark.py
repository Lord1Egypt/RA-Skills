#!/usr/bin/env python3
"""
RAG Pipeline Starter: Embedding Benchmark
Tests multiple embeddings on your data to find the best fit.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional

# Common embedding models (mock for demo - can be replaced with real implementations)
EMBEDDING_MODELS = {
    "sentence-transformers/all-MiniLM-L6-v2": {"dims": 384, "speed": "fast", "cost": "free"},
    "sentence-transformers/all-mpnet-base-v2": {"dims": 768, "speed": "medium", "cost": "free"},
    "openai/text-embedding-ada-002": {"dims": 1536, "speed": "fast", "cost": "paid"},
    "cohere/embed-english-v3.0": {"dims": 1024, "speed": "fast", "cost": "paid"},
    "bm25": {"dims": "sparse", "speed": "fast", "cost": "free"},
}


def load_chunks(chunk_dir: str) -> List[str]:
    """Load text chunks from directory."""
    chunks = []
    path = Path(chunk_dir)
    if path.is_dir():
        for f in sorted(path.glob("chunk_*.txt")):
            chunks.append(f.read_text().strip())
    return chunks


def compute_similarity__mock(text1: str, text2: str) -> float:
    """Mock similarity - in production, use actual embedding model."""
    # Simple word overlap for demo
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words1 or not words2:
        return 0.0
    return len(words1 & words2) / len(words1 | words2)


def benchmark_model(chunks: List[str], model_name: str) -> Dict[str, Any]:
    """Benchmark an embedding model on the given chunks."""
    model_info = EMBEDDING_MODELS.get(model_name, {"dims": 512, "speed": "unknown", "cost": "unknown"})
    
    results = {
        "model": model_name,
        "dimensions": model_info.get("dims"),
        "speed_tier": model_info.get("speed"),
        "cost": model_info.get("cost"),
    }
    
    if len(chunks) < 2:
        return {**results, "error": "Need at least 2 chunks for benchmark"}
    
    # Compute pairwise similarities
    similarities = []
    for i in range(min(20, len(chunks) - 1)):
        for j in range(i + 1, min(25, len(chunks))):
            sim = compute_similarity_mock(chunks[i], chunks[j])
            similarities.append(sim)
    
    if similarities:
        results["avg_similarity"] = sum(similarities) / len(similarities)
        results["min_similarity"] = min(similarities)
        results["max_similarity"] = max(similarities)
        results["pairs_tested"] = len(similarities)
    
    return results


def run_benchmark(chunks: List[str], models: List[str], output_path: Optional[str] = None) -> Dict[str, Any]:
    """Run benchmark on all specified models."""
    results = []
    
    for model in models:
        if model in EMBEDDING_MODELS:
            result = benchmark_model(chunks, model)
            results.append(result)
            print(f"✓ Tested: {model}")
        else:
            print(f"⚠ Unknown model: {model} - skipping")
    
    # Rank by separation power (higher max-min = better discrimination)
    ranked = sorted(results, key=lambda x: x.get("max_similarity", 0) - x.get("min_similarity", 0), reverse=True)
    
    summary = {
        "models_tested": len(results),
        "chunks_evaluated": len(chunks),
        "results": results,
        "recommendations": ranked[:3] if ranked else [],
    }
    
    if output_path:
        Path(output_path).write_text(json.dumps(summary, indent=2))
        print(f"Results saved to {output_path}")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="RAG Embedding Benchmark")
    parser.add_argument("--embeddings", type=str, nargs="+",
                        default=["sentence-transformers/all-MiniLM-L6-v2", "bm25"],
                        help="Embedding models to test (space-separated)")
    parser.add_argument("--data", type=str, required=True, help="Directory with chunked text files")
    parser.add_argument("--domain", type=str, help="Domain name for context (affects recommendations)")
    parser.add_argument("--output", type=str, help="Output file for results (JSON)")
    
    args = parser.parse_args()
    
    print(f"Loading chunks from: {args.data}")
    chunks = load_chunks(args.data)
    
    if not chunks:
        print("Error: No chunks found in directory")
        sys.exit(1)
    
    print(f"Loaded {len(chunks)} chunks")
    print(f"Testing {len(args.embeddings)} embeddings...")
    
    results = run_benchmark(chunks, args.embeddings, args.output)
    
    print("\n=== Results ===")
    for r in results.get("results", []):
        print(f"\n{r['model']}:")
        print(f"  Dimensions: {r.get('dimensions')}")
        print(f"  Avg similarity: {r.get('avg_similarity', 'N/A'):.3f}" if 'avg_similarity' in r else "  Avg similarity: N/A")
    
    if results.get("recommendations"):
        print(f"\n=== Top Recommendation ===")
        top = results["recommendations"][0]
        print(f"{top['model']} — best for {args.domain or 'general'} domain")


if __name__ == "__main__":
    main()
