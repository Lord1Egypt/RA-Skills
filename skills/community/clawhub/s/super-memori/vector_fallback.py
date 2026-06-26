#!/usr/bin/env python3
"""
vector_fallback.py — Semantic search via Qdrant for memory-enhancement skill.
Usage: python3 vector_fallback.py "query text"
"""
import sys
import urllib.request
import urllib.parse
import json

COLLECTION = "memories"
QDRANT_URL = "http://127.0.0.1:6333"

def get_embedding(text):
    """Generate embedding via sentence-transformers (local model)."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("intfloat/multilingual-e5-small")
        return model.encode(text).tolist()
    except ImportError as e:
        print(f"⚠️ sentence-transformers not installed: {e}", file=sys.stderr)
        print("Install with: pip install sentence-transformers", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Embedding failed: {e}", file=sys.stderr)
        sys.exit(1)

def search_qdrant(vector, top_k=5, filter_type=None):
    """Search Qdrant collection for similar vectors."""
    payload = {
        "vector": vector,
        "limit": top_k,
        "with_payload": True
    }
    if filter_type:
        payload["filter"] = {
            "must": [{"key": "file_type", "match": {"value": filter_type}}]
        }
    data = json.dumps(payload).encode("utf-8")
    url = f"{QDRANT_URL}/collections/{COLLECTION}/points/search"
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            return result.get("result", [])
    except urllib.error.URLError as e:
        print(f"⚠️ Qdrant unavailable: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"⚠️ Qdrant search failed: {e}", file=sys.stderr)
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vector_fallback.py \"query text\"", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"Embedding query: {query}")
    
    # Step 1: Get embedding for the query (E5 model requires "query: " prefix)
    query_vector = get_embedding(f"query: {query}")
    
    # Step 2: Search Qdrant
    results = search_qdrant(query_vector, filter_type=filter_type)
    
    # Step 3: Output results
    if not results:
        print("No vector results found.")
        return
    
    print("--- VECTOR RESULTS (semantic) ---")
    for i, hit in enumerate(results, 1):
        point = hit.get("payload", {})
        score = hit.get("score", 0)
        filepath = point.get("filepath", "unknown")
        file_type = point.get("file_type", "unknown")
        content = point.get("content", point.get("text", ""))
        date = point.get("date", "unknown")
        
        # Truncate content for readability
        snippet = content[:200] + "..." if len(content) > 200 else content
        
        print(f"{i}. [{file_type}] {filepath} (score: {score:.3f})")
        print(f"   Date: {date}")
        print(f"   Snippet: {snippet}")
        print()

if __name__ == "__main__":
    main()
