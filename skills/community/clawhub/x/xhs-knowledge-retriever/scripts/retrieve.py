#!/usr/bin/env python3
"""
xhs-knowledge-retriever

Semantic retrieval over the index built by xhs-knowledge-indexer.

Usage:
    python3 skills/xhs-knowledge-retriever/scripts/retrieve.py \
        --query "有娃家庭怎么选沙发"

    python3 skills/xhs-knowledge-retriever/scripts/retrieve.py \
        --query "有娃家庭怎么选沙发" \
        --top-k 5 \
        --output /tmp/retrieved.json
"""

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
_STANDARD_PATH_TAIL = ("workspace-xhs-agent", "products", "xhs-note-learning-cycle")


def get_knowledge_root(product_root):
    """Resolve the local XHS knowledge root without importing product helpers."""
    if "XHS_KNOWLEDGE_ROOT" in os.environ:
        return Path(os.environ["XHS_KNOWLEDGE_ROOT"])

    resolved = product_root.resolve()
    if len(resolved.parts) >= 3 and resolved.parts[-3:] == _STANDARD_PATH_TAIL:
        return resolved.parent.parent / "knowledge" / "xhs"

    raise RuntimeError(
        "Cannot infer the XHS knowledge root. Set XHS_KNOWLEDGE_ROOT to the "
        "local knowledge/xhs directory."
    )


_KNOWLEDGE = get_knowledge_root(_ROOT)
DEFAULT_INDEX_DIR = _KNOWLEDGE / "05-competitors" / "rag"


def load_index(index_dir):
    index_dir = Path(index_dir)
    index_info_path = index_dir / "index.json"
    embeddings_path = index_dir / "embeddings.npy"
    metadata_path = index_dir / "metadata.jsonl"

    if not index_info_path.exists():
        raise FileNotFoundError(f"Index not found at {index_dir}")

    index_info = json.loads(index_info_path.read_text(encoding="utf-8"))
    embeddings = np.load(embeddings_path)
    records = []
    with open(metadata_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if len(records) != embeddings.shape[0]:
        raise ValueError(
            f"metadata count ({len(records)}) != embeddings count ({embeddings.shape[0]})"
        )

    return index_info, embeddings, records


def check_index(index_dir):
    index_dir = Path(index_dir)
    required = {
        "index": index_dir / "index.json",
        "embeddings": index_dir / "embeddings.npy",
        "metadata": index_dir / "metadata.jsonl",
    }
    missing = [name for name, file_path in required.items() if not file_path.exists()]
    return {
        "status": "ready" if not missing else "missing_index_files",
        "indexDir": str(index_dir),
        "missing": missing,
        "files": {name: str(file_path) for name, file_path in required.items()},
    }


def retrieve(query, index_dir, top_k=5, model_name=None):
    from sentence_transformers import SentenceTransformer

    index_info, embeddings, records = load_index(index_dir)
    model = SentenceTransformer(model_name or index_info["model"])
    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )[0]

    # Cast to float64 to avoid Apple-Accelerate float32 matmul warnings.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        scores = embeddings.astype(np.float64) @ query_embedding.astype(np.float64)
    scores = scores.astype(np.float32)
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for rank, idx in enumerate(top_indices, start=1):
        record = records[idx]
        results.append(
            {
                "rank": rank,
                "score": float(scores[idx]),
                "chunk": record["text"],
                "metadata": {
                    k: v
                    for k, v in record.items()
                    if k not in ("text",)
                },
            }
        )
    return results, index_info


def main():
    parser = argparse.ArgumentParser(description="Retrieve XHS RAG chunks")
    parser.add_argument("--query", type=str, default="")
    parser.add_argument("--index-dir", type=str, default=str(DEFAULT_INDEX_DIR))
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    if args.check_only:
        print(json.dumps(check_index(args.index_dir), indent=2, ensure_ascii=False))
        return
    if not args.query.strip():
        parser.error("--query is required unless --check-only is used")

    results, index_info = retrieve(args.query, args.index_dir, args.top_k, args.model)
    output = {
        "query": args.query,
        "model": index_info["model"],
        "topK": args.top_k,
        "results": results,
    }

    json_output = json.dumps(output, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(json_output + "\n", encoding="utf-8")
        print(f"[retriever] wrote {len(results)} results to {args.output}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == "__main__":
    main()
