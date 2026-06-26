import os
import logging
import asyncio
import requests
from datetime import datetime, timezone
from typing import List, Dict
from bs4 import BeautifulSoup
 
from setup import get_chroma_lock   # FIX (concurrency): cross-process write lock
 
logger = logging.getLogger("openclaw.analytics")
 
 
# ==========================================
# HELPER FUNCTIONS
# ==========================================
 
def extract_h2s_from_html(html_content: str) -> List[str]:
    """Parses raw HTML and extracts all text within <h2> tags using BeautifulSoup."""
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, "html.parser")
    return [h2.get_text(strip=True) for h2 in soup.find_all("h2")]
 
 
def generate_embedding(text: str, config: dict) -> List[float]:
    """
    Generates a vector embedding for the given text.
    If Anthropic is selected, uses ChromaDB's default local embedding model 
    since Anthropic does not provide native embedding endpoints.
    """
    provider = config.get("EMBEDDING_PROVIDER", config.get("LLM_PROVIDER", "gemini")).lower()
 
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=config["OPENAI_API_KEY"])
        response = client.embeddings.create(input=[text], model="text-embedding-3-small")
        return response.data[0].embedding
 
    elif provider == "anthropic":
        # Use ChromaDB's built-in ONNX model (all-MiniLM-L6-v2) locally.
        # Environment variables (CHROMA_CACHE_DIR, HF_HOME) are now configured 
        # process-wide at startup in setup.py to prevent async race conditions.
        from chromadb.utils import embedding_functions
        default_ef = embedding_functions.DefaultEmbeddingFunction()
        return default_ef([text])[0]
 
    else:  # Default: Gemini
        import google.generativeai as genai
        genai.configure(api_key=config["GEMINI_API_KEY"])
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document"
        )
        return result["embedding"]
 
 
# ==========================================
# MONTHLY OPTIMIZATION ENGINE
# ==========================================
 
def detect_ctr_decay(gsc_data: List[dict]) -> List[dict]:
    """
    Identifies posts whose observed CTR is below 50 % of the expected CTR for
    their average SERP position.  Expected CTR benchmarks are conservative
    industry medians.
    """
    EXPECTED_CTR = {1: 0.28, 2: 0.15, 3: 0.10, 4: 0.07, 5: 0.05}
    DEFAULT_EXPECTED = 0.025  # positions 6-10
 
    decayed = []
    for row in gsc_data:
        pos = round(row["position"])
        expected = EXPECTED_CTR.get(pos, DEFAULT_EXPECTED)
        if row["ctr"] < (expected * 0.5):
            decayed.append({
                **row,
                "expected_ctr": expected,
                "decay_ratio": row["ctr"] / expected,
            })
    return decayed
 
 
def is_eligible_for_update(post: dict, gsc_row: dict, db_conn) -> tuple[bool, str]:
    """
    v5.1: Age gate uses content_updated_at, NOT published_at and NOT wp_modified_date.
 
    Age gates by SERP position band:
      position ≤ 10  → 120-day protection  (top-10 protection)
      position ≤ 20  → 90-day gate         (standard)
      position ≤ 40  → 45-day gate         (recovery-eligible)
      position > 40  → 30-day gate         (stalled — aggressive update)
    """
    baseline_str = post.get("content_updated_at") or post.get("published_at")
    if not baseline_str:
        return False, "No baseline date available — skipping"
 
    baseline = datetime.fromisoformat(baseline_str.replace("Z", "+00:00"))
    age_days = (datetime.now(timezone.utc) - baseline).days
    position = gsc_row.get("position", 100)
 
    if position <= 10:
        gate, label = 120, "top-10 protection"
    elif position <= 20:
        gate, label = 90, "standard gate"
    elif position <= 40:
        gate, label = 45, "recovery-eligible"
    else:
        gate, label = 30, "stalled — aggressive update"
 
    if age_days < gate:
        baseline_field = "content_updated_at" if post.get("content_updated_at") else "published_at"
        return False, (
            f"Too young ({age_days}d < {gate}d [{label}], position {position:.0f}). "
            f"Baseline: {baseline_field}"
        )
 
    return True, f"Eligible (age {age_days}d, gate {gate}d [{label}], position {position:.0f})"
 
 
async def apply_content_update(
    post: dict,
    diff: dict,
    new_html: str,
    new_schema: str,
    collection,       # ChromaDB collection
    db_conn,
    config: dict      # Passed in to supply provider keys for embedding
) -> bool:
    """
    Applies a content update via WP REST API PUT, then immediately:
      1. Upserts the new vector embedding in ChromaDB.
      2. Stamps content_updated_at in SQLite (age-gate clock reset).
      3. Mirrors wp_modified_date in SQLite (informational only —
         never used for age-gating).
    """
    wp_base = config["WP_URL"].rstrip("/")
    auth = (config["WP_USERNAME"], config["WP_APP_PASSWORD"])
    meta_key = config.get("WP_SEO_META_DESC_KEY", "_yoast_wpseo_metadesc")
 
    # --- Stage 1: PUT updated content to WordPress ---
    try:
        put_payload = {
            "content": new_html,
            "meta": {
                meta_key: (
                    diff.get("meta_change") or post.get("meta_description", "")
                )
            },
        }
        if diff.get("title_change"):
            put_payload["title"] = diff["title_change"]
 
        put_response = await asyncio.to_thread(
            requests.put,
            f"{wp_base}/wp-json/wp/v2/posts/{post['wp_post_id']}",
            auth=auth,
            json=put_payload,
            timeout=30
        )
        put_response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"WP PUT failed for post {post['wp_post_id']}: {e}")
        return False
 
    wp_modified = put_response.json().get(
        "modified", datetime.now(timezone.utc).isoformat()
    )
    now_utc = datetime.now(timezone.utc).isoformat()
 
    # --- Stage 2: Recalculate and upsert vector embedding ---
    new_h2s = extract_h2s_from_html(new_html)
    new_embedding_text = (
        f"{post['query']} {post.get('title', '')} {' '.join(new_h2s)}"
    )
 
    try:
        new_embedding = await asyncio.to_thread(generate_embedding, new_embedding_text, config)
 
        # FIX (concurrency): Acquire the cross-process file lock before writing to
        # ChromaDB. Without this, overlapping analytics runs corrupt the HNSW index.
        chroma_lock = get_chroma_lock(config.get("CHROMA_DB_PATH", "./chroma_db"))
 
        def _chroma_upsert():
            with chroma_lock:
                collection.upsert(
                    ids=[str(post["id"])],
                    embeddings=[new_embedding],
                    metadatas=[{
                        "url": post["wp_url"],
                        "query": post["query"],
                        "content_updated_at": now_utc,
                    }]
                )
 
        await asyncio.to_thread(_chroma_upsert)
        logger.info(f"ChromaDB upserted for post {post['id']} ({post['wp_url']})")
    except Exception as e:
        logger.error(
            f"ChromaDB upsert FAILED for post {post['id']}: {e}. "
            "Vector DB is now stale for this post — schedule manual upsert."
        )
 
    # --- Stage 3: Update SQLite — content_updated_at AND wp_modified_date ---
    def _update_sqlite_records():
        db_conn.execute("""
            UPDATE posts
            SET content_updated_at = ?,
                wp_modified_date   = ?,
                word_count         = ?,
                schema_types       = ?,
                last_modified_at   = ?
            WHERE id = ?
        """, (
            now_utc,
            wp_modified,
            diff.get("new_word_count", post.get("word_count", 0)),
            diff.get("new_schema_types", post.get("schema_types", "[]")),
            now_utc,
            post["id"]
        ))
        db_conn.commit()
 
    await asyncio.to_thread(_update_sqlite_records)
 
    logger.info(f"Content update complete for post {post['id']}. Age gate clock reset.")
    return True
 