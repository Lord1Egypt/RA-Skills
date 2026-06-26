#!/usr/bin/env python3
"""
embed-file.py — Embed a single memory file into Qdrant.
Usage: python3 embed-file.py <filepath> <collection_name> <qdrant_url>
"""
import sys
import os
import hashlib
import json
import urllib.request
import urllib.error
from datetime import datetime

def get_embedding(text):
    """Generate 384-dim embedding using multilingual-e5-small."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("intfloat/multilingual-e5-small")
        return model.encode(text).tolist()
    except ImportError:
        print(f"⚠️ sentence-transformers not installed. Skipping: {os.path.basename(filepath)}")
        sys.exit(0)

def ensure_collection(url, collection_name):
    """Create collection if it doesn't exist (384 dims, Cosine)."""
    req = urllib.request.Request(
        f"{url}/collections/{collection_name}",
        data=json.dumps({
            "vectors": {"size": 384, "distance": "Cosine"},
            "optimizers_config": {"memmap_threshold": 50000}
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except urllib.error.URLError:
        pass  # May already exist

def get_hash(filepath):
    return hashlib.md5(filepath.encode()).hexdigest()

def file_needs_update(url, collection_name, point_id):
    """Check if point already exists in Qdrant."""
    req = urllib.request.Request(
        f"{url}/collections/{collection_name}/points/{point_id}",
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("result") is None  # True if not found
    except Exception:
        return True

def upsert_point(url, collection_name, point_id, vector, payload):
    """Upsert a point into Qdrant."""
    req = urllib.request.Request(
        f"{url}/collections/{collection_name}/points",
        data=json.dumps({
            "points": [{
                "id": point_id,
                "vector": vector,
                "payload": payload
            }]
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True
    except Exception as e:
        print(f"⚠️ Failed to upsert {point_id}: {e}")
        return False

def extract_text_from_file(filepath):
    """Extract text content from a markdown file, skip metadata."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # Remove YAML front matter if present
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        return content
    except Exception as e:
        print(f"⚠️ Cannot read {filepath}: {e}")
        return ""

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 embed-file.py <filepath> <collection> <qdrant_url>")
        sys.exit(1)

    filepath = sys.argv[1]
    collection = sys.argv[2]
    qdrant_url = sys.argv[3]

    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filepath}")
        return

    point_id = get_hash(filepath)

    # Check if already indexed
    if not file_needs_update(qdrant_url, collection, point_id):
        print(f"  ⏭ Already indexed: {os.path.basename(filepath)}")
        return

    content = extract_text_from_file(filepath)
    if not content.strip():
        print(f"  ⏭ Empty file: {os.path.basename(filepath)}")
        return

    print(f"  📄 Embedding: {os.path.basename(filepath)}")
    
    try:
        # E5 model requires "passage: " prefix for documents
        vector = get_embedding(f"passage: {content}")
    except Exception as e:
        print(f"  ❌ Embedding failed: {e}")
        return

    # Determine file type from path
    rel_path = os.path.relpath(filepath, os.path.dirname(os.path.dirname(os.path.dirname(filepath))))
    file_type = rel_path.split("/")[1] if "/" in rel_path else "unknown"  # episodic, semantic, procedural

    payload = {
        "filepath": filepath,
        "file_type": file_type,
        "content": content[:2000],  # Limit payload size
        "date": os.path.basename(filepath)[:10] if "episodic" in filepath else "unknown",
        "filename": os.path.basename(filepath),
        "indexed_at": datetime.utcnow().isoformat()
    }

    if upsert_point(qdrant_url, collection, point_id, vector, payload):
        print(f"  ✅ Indexed: {os.path.basename(filepath)}")
    else:
        print(f"  ❌ Failed: {os.path.basename(filepath)}")

if __name__ == "__main__":
    main()
