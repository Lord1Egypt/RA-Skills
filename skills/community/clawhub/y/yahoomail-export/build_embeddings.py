#!/usr/bin/env python3
"""
Embedding Index Builder - Creates vector index from filtered emails using Ollama.
Uses nomic-embed-text for local embeddings, stored in SQLite with sqlite-vec.
"""

import json
import sqlite3
import sys
import time
import requests
from pathlib import Path

# EDIT THIS: Set your base directory for the email purge project
BASE_DIR = Path("~/email-purge").expanduser()
DB_FILE = BASE_DIR / "vectors" / "email_index.db"
KEEP_FILE = BASE_DIR / "filtered" / "keep.jsonl"
REVIEW_FILE = BASE_DIR / "filtered" / "needs_review.jsonl"

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768  # nomic-embed-text output dimension

BATCH_SIZE = 50  # emails per embedding batch

def get_embedding(text):
    """Get embedding from Ollama."""
    resp = requests.post(OLLAMA_URL, json={
        "model": EMBED_MODEL,
        "prompt": text,
    })
    resp.raise_for_status()
    return resp.json()["embedding"]

def batch_embed(texts):
    """Get embeddings for a batch of texts."""
    embeddings = []
    for text in texts:
        emb = get_embedding(text)
        embeddings.append(emb)
        time.sleep(0.05)  # Small delay to avoid overwhelming Ollama
    return embeddings

def build_embedding_text(meta):
    """Build compact text for embedding from email metadata."""
    parts = []
    if meta.get("subject"):
        parts.append(f"Subject: {meta['subject']}")
    if meta.get("from"):
        parts.append(f"From: {meta['from']}")
    if meta.get("body_preview"):
        # Truncate body for embedding
        parts.append(f"Content: {meta['body_preview'][:1500]}")
    if meta.get("attachments"):
        parts.append(f"Attachments: {', '.join(meta['attachments'][:5])}")
    return "\n".join(parts)

def init_db():
    """Initialize SQLite database with vector support."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_FILE))
    
    # Try to load sqlite-vec
    try:
        conn.enable_load_extension(True)
        # sqlite-vec is usually loaded as vec0
        conn.load_extension("vec0")
        has_vec = True
    except Exception:
        has_vec = False
        print("Warning: sqlite-vec not available, storing embeddings as BLOBs only")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid INTEGER,
            folder TEXT,
            message_id TEXT,
            "from" TEXT,
            "to" TEXT,
            subject TEXT,
            date TEXT,
            has_attachments INTEGER,
            attachments TEXT,
            labels TEXT,
            body_preview TEXT,
            classification TEXT,
            score INTEGER,
            reasons TEXT,
            embedding BLOB
        )
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_date ON emails(date)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_from ON emails("from")
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_classification ON emails(classification)
    """)
    
    conn.commit()
    return conn, has_vec

def store_embedding(conn, row_id, embedding):
    """Store embedding as blob."""
    import struct
    blob = struct.pack(f'{len(embedding)}f', *embedding)
    conn.execute("UPDATE emails SET embedding = ? WHERE id = ?", (blob, row_id))

def load_emails(filepath):
    """Load emails from JSONL file."""
    emails = []
    if not filepath.exists():
        return emails
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                emails.append(json.loads(line))
    return emails

def main():
    print("=== Embedding Index Builder ===")
    
    conn, has_vec = init_db()
    
    # Load emails to index (keep + review)
    emails = load_emails(KEEP_FILE) + load_emails(REVIEW_FILE)
    print(f"Loaded {len(emails)} emails to index")
    
    if not emails:
        print("No emails to index. Run pre_filter.py first.")
        conn.close()
        return
    
    # Check existing count
    existing = conn.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
    print(f"Already indexed: {existing}")
    
    # Filter out already-indexed UIDs
    existing_uids = set()
    for row in conn.execute("SELECT uid FROM emails"):
        existing_uids.add(row[0])
    
    new_emails = [e for e in emails if e.get("uid") not in existing_uids]
    print(f"New emails to index: {len(new_emails)}")
    
    if not new_emails:
        print("Nothing new to index.")
        conn.close()
        return
    
    # Process in batches
    total = len(new_emails)
    indexed = 0
    
    for i in range(0, total, BATCH_SIZE):
        batch = new_emails[i:i + BATCH_SIZE]
        
        # Build embedding texts
        texts = [build_embedding_text(e) for e in batch]
        
        # Get embeddings
        try:
            embeddings = batch_embed(texts)
        except Exception as e:
            print(f"Error getting embeddings at batch {i}: {e}")
            # Skip this batch and continue
            continue
        
        # Insert into database
        for email_meta, embedding in zip(batch, embeddings):
            conn.execute("""
                INSERT INTO emails (uid, folder, message_id, "from", "to", subject,
                    date, has_attachments, attachments, labels, body_preview,
                    classification, score, reasons, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                email_meta.get("uid"),
                email_meta.get("folder"),
                email_meta.get("message_id"),
                email_meta.get("from"),
                email_meta.get("to"),
                email_meta.get("subject"),
                email_meta.get("date"),
                1 if email_meta.get("has_attachments") else 0,
                json.dumps(email_meta.get("attachments", [])),
                json.dumps(email_meta.get("labels", [])),
                email_meta.get("body_preview"),
                email_meta.get("classification"),
                email_meta.get("score"),
                json.dumps(email_meta.get("reasons", [])),
                None  # Will store embedding separately
            ))
            row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            store_embedding(conn, row_id, embedding)
        
        conn.commit()
        indexed += len(batch)
        
        if indexed % 500 == 0 or indexed == total:
            print(f"  Indexed {indexed}/{total} ({indexed/total*100:.1f}%)")
    
    # Create vector virtual table if sqlite-vec is available
    if has_vec:
        try:
            conn.execute(f"""
                CREATE VIRTUAL TABLE IF NOT EXISTS email_vec USING vec0(
                    id INTEGER PRIMARY KEY,
                    embedding float[{EMBED_DIM}]
                )
            """)
            # Populate vector table
            count = 0
            for row in conn.execute("SELECT id, embedding FROM emails WHERE embedding IS NOT NULL"):
                row_id, emb_blob = row
                if emb_blob:
                    conn.execute("INSERT OR REPLACE INTO email_vec (id, embedding) VALUES (?, ?)",
                               (row_id, emb_blob))
                    count += 1
                    if count % 500 == 0:
                        conn.commit()
            conn.commit()
            print(f"Vector table populated: {count} entries")
        except Exception as e:
            print(f"Vector table creation failed: {e}")
    
    final_count = conn.execute("SELECT COUNT(*) FROM emails").fetchone()[0]
    print(f"\n=== Done: {final_count} emails indexed ===")
    print(f"Database: {DB_FILE}")
    conn.close()

if __name__ == "__main__":
    main()
