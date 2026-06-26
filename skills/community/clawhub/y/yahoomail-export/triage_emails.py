#!/usr/bin/env python3
"""
Local Model Triage - Uses qwen3:4b-instruct to score emails for importance.
Reads from pre-filtered results, outputs JSON triage scores.
"""

import json
import sqlite3
import sys
import time
import re
import requests
from pathlib import Path

# EDIT THIS: Set your base directory for the email purge project
BASE_DIR = Path("~/email-purge").expanduser()
DB_FILE = BASE_DIR / "vectors" / "email_index.db"
TRIAGE_FILE = BASE_DIR / "filtered" / "triage_results.jsonl"
ESCALATE_FILE = BASE_DIR / "filtered" / "escalate.jsonl"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"

BATCH_SIZE = 1  # Process one at a time for quality

SYSTEM_PROMPT = """You are an email triage assistant. Score each email for importance and categorize it.

For each email, provide a JSON response with:
- importance: 0-100 (0=junk, 50=normal, 100=critical)
- reason: Brief explanation (1 sentence)
- category: One of: legal, client, deadline, medical, finance, personal, admin, junk
- needs_human_review: true if borderline or potentially important

Be concise. Only output valid JSON, no other text."""

def build_email_prompt(meta):
    """Build compact email representation for the model."""
    parts = []
    if meta.get("subject"):
        parts.append(f"Subject: {meta['subject']}")
    if meta.get("from"):
        parts.append(f"From: {meta['from']}")
    if meta.get("to"):
        parts.append(f"To: {meta['to']}")
    if meta.get("date"):
        parts.append(f"Date: {meta['date']}")
    if meta.get("has_attachments"):
        attachments = meta.get("attachments", [])
        parts.append(f"Attachments: {', '.join(attachments[:5]) if attachments else 'yes'}")
    
    # Include first 1500 chars of body
    body = meta.get("body_preview", "")[:1500]
    if body:
        parts.append(f"\nBody Preview:\n{body}")
    
    return "\n".join(parts)

def query_ollama(prompt):
    """Query Ollama for email triage."""
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temp for consistent scoring
                "num_predict": 300,  # Short response
            }
        }, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "")
    except Exception as e:
        print(f"  Ollama error: {e}")
        return None

def parse_triage_response(response):
    """Parse JSON response from the model."""
    if not response:
        return None
    
    # Try to extract JSON from response
    # Remove any thinking tags
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    response = re.sub(r'<思考>.*?</思考>', '', response, flags=re.DOTALL)
    
    # Try to find JSON in the response
    json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # Try the whole response
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    
    return None

def main():
    if not DB_FILE.exists():
        print(f"No database found at {DB_FILE}")
        print("Run build_embeddings.py first.")
        sys.exit(1)
    
    print("=== Local Model Triage ===")
    print(f"Model: {MODEL}")
    
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    
    # Get emails that need triage (not yet scored)
    emails = conn.execute("""
        SELECT id, uid, folder, message_id, "from", "to", subject, date,
               has_attachments, attachments, labels, body_preview,
               classification, score, reasons
        FROM emails
        WHERE (importance IS NULL)
        AND classification IN ('keep', 'review')
        ORDER BY score DESC
    """).fetchall()
    
    print(f"Emails to triage: {len(emails)}")
    
    if not emails:
        print("Nothing to triage.")
        conn.close()
        return
    
    # Add columns if they don't exist
    try:
        conn.execute("ALTER TABLE emails ADD COLUMN importance INTEGER")
        conn.execute("ALTER TABLE emails ADD COLUMN category TEXT")
        conn.execute("ALTER TABLE emails ADD COLUMN triage_reason TEXT")
        conn.execute("ALTER TABLE emails ADD COLUMN needs_human_review INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Columns already exist
    
    triage_count = 0
    escalate_count = 0
    
    with open(TRIAGE_FILE, "a") as triage_f, \
         open(ESCALATE_FILE, "a") as escalate_f:
        
        for i, row in enumerate(emails):
            meta = dict(row)
            meta["attachments"] = json.loads(meta.get("attachments", "[]"))
            meta["labels"] = json.loads(meta.get("labels", "[]"))
            meta["reasons"] = json.loads(meta.get("reasons", "[]"))
            
            # Build prompt
            email_text = build_email_prompt(meta)
            prompt = f"Score this email:\n\n{email_text}"
            
            # Query model
            response = query_ollama(prompt)
            result = parse_triage_response(response)
            
            if result is None:
                # Failed to parse, mark for human review
                result = {
                    "importance": 50,
                    "reason": "Failed to parse model response",
                    "category": "admin",
                    "needs_human_review": True
                }
            
            # Ensure required fields
            importance = max(0, min(100, result.get("importance", 50)))
            category = result.get("category", "admin")
            reason = result.get("reason", "")
            needs_review = result.get("needs_human_review", False)
            
            # Update database
            conn.execute("""
                UPDATE emails SET importance = ?, category = ?, 
                    triage_reason = ?, needs_human_review = ?
                WHERE id = ?
            """, (importance, category, reason, 1 if needs_review else 0, row["id"]))
            
            # Write triage result
            entry = {
                **meta,
                "importance": importance,
                "category": category,
                "triage_reason": reason,
                "needs_human_review": needs_review,
            }
            triage_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            triage_count += 1
            
            # Escalate high-importance or flagged emails
            if importance >= 70 or needs_review:
                escalate_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                escalate_count += 1
            
            # Progress
            if (i + 1) % 50 == 0:
                conn.commit()
                print(f"  Triage: {i + 1}/{len(emails)} ({(i + 1)/len(emails)*100:.1f}%)")
            
            # Small delay to avoid overwhelming Ollama
            if (i + 1) % 10 == 0:
                time.sleep(0.5)
    
    conn.commit()
    
    # Summary stats
    stats = conn.execute("""
        SELECT 
            COUNT(*) as total,
            AVG(importance) as avg_importance,
            SUM(CASE WHEN importance >= 70 THEN 1 ELSE 0 END) as high_importance,
            SUM(CASE WHEN needs_human_review = 1 THEN 1 ELSE 0 END) as needs_review
        FROM emails
        WHERE importance IS NOT NULL
    """).fetchone()
    
    print(f"\n=== Triage Results ===")
    print(f"Total triaged: {triage_count}")
    print(f"Escalated:     {escalate_count}")
    print(f"Avg importance:{stats['avg_importance']:.1f}")
    print(f"High (>=70):   {stats['high_importance']}")
    print(f"Needs review:  {stats['needs_review']}")
    print(f"\nResults: {TRIAGE_FILE}")
    print(f"Escalate:{ESCALATE_FILE}")
    
    conn.close()

if __name__ == "__main__":
    main()
