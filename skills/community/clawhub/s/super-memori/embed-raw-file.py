#!/usr/bin/env python3
"""
embed-raw-file.py — Embed any markdown file into Qdrant with custom metadata.

Usage: python3 embed-raw-file.py <filepath> <entry_type>

entry_type: learning, memory, correction, pattern, insight, knowledge_gap

Reuses the same embedding model and Qdrant endpoint as embed-file.py.
"""
import sys
import os
import hashlib
import json
import urllib.request
import urllib.error
from datetime import datetime

COLLECTION = "memories"
QDRANT_URL = "http://127.0.0.1:6333"


def get_embedding(text):
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("intfloat/multilingual-e5-small")
        return model.encode(text).tolist()
    except ImportError:
        print("⚠️ sentence-transformers not installed. Skipping embed.", file=sys.stderr)
        sys.exit(0)


def get_hash(filepath, mod_time):
    return hashlib.md5(f"{filepath}:{mod_time}".encode()).hexdigest()


def point_exists(point_id):
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/{point_id}",
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("result") is not None
    except Exception:
        return False


def upsert_point(point_id, vector, payload):
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points",
        data=json.dumps({
            "points": [{
                "id": point_id,
                "vector": vector,
                "payload": payload
            }]
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status == 200


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 embed-raw-file.py <filepath> <entry_type>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    entry_type = sys.argv[2]

    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filepath}", file=sys.stderr)
        return

    # Use file's modification time for stable hash
    mod_time = str(os.path.getmtime(filepath))
    point_id = get_hash(filepath, mod_time)

    if point_exists(point_id):
        print(f"  ⏭ Already indexed: {os.path.basename(filepath)}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return

    print(f"  📄 Embedding: {os.path.basename(filepath)} [{entry_type}]")

    # E5 model requires "passage: " prefix for documents
    vector = get_embedding(f"passage: {content}")
    content_snippet = content[:2000]

    payload = {
        "filepath": filepath,
        "file_type": entry_type,
        "content": content_snippet,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "filename": os.path.basename(filepath),
        "indexed_at": datetime.utcnow().isoformat()
    }

    if upsert_point(point_id, vector, payload):
        print(f"  ✅ Indexed: {os.path.basename(filepath)}")
    else:
        print(f"  ❌ Failed: {os.path.basename(filepath)}", file=sys.stderr)


if __name__ == "__main__":
    main()
