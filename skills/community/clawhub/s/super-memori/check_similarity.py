#!/usr/bin/env python3
"""
check_similarity.py — Check if a semantically similar entry already exists in Qdrant learnings.
Usage: python3 check_similarity.py "text to check" [threshold]
Returns the similar text if found above threshold, empty string otherwise.
"""
import sys
import json
import urllib.request
from sentence_transformers import SentenceTransformer

COLLECTION = "memories"
QDRANT_URL = "http://127.0.0.1:6333"
DEFAULT_THRESHOLD = 0.90


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_similarity.py <text> [threshold]", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_THRESHOLD

    try:
        model = SentenceTransformer("intfloat/multilingual-e5-small")
        vector = model.encode(f"query: {text}").tolist()
    except ImportError:
        sys.exit(0)  # Model not installed — skip dedup, not blocking
    except Exception:
        sys.exit(0)  # Embedding failed — skip dedup

    payload = json.dumps({"vector": vector, "limit": 1, "with_payload": True, "score_threshold": threshold}).encode()
    req = urllib.request.Request(f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
                                 data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            results = data.get("result", [])
            if results:
                point = results[0].get("payload", {})
                print(point.get("content", point.get("text", "")))
    except Exception:
        pass  # Qdrant unavailable — skip dedup
