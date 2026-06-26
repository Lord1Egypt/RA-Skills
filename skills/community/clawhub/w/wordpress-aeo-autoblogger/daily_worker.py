import json
import asyncio
import logging
import requests
import re
import uuid
from datetime import datetime, timezone
from bs4 import BeautifulSoup, NavigableString
from pydantic import ValidationError
 
from setup import get_db_connection, get_vector_collection, get_chroma_lock, configure_global_environment
from logger import LLMSession, CostCapException
from analytics_worker import generate_embedding
 
# Updated: imported TaskReferenceFile, GeneratedContent, and SchemaBlock
from models import ContentOutline, TaskReferenceFile, GeneratedContent, SchemaBlock
 
import scraper
import schema_engine
 
logger = logging.getLogger("openclaw.daily")
 
FOOTER_HTML = (
    '<div style="text-align: center; font-size: 5pt; margin-top: 50px;">'
    '<a href="https://jamesjernigan.com" style="color: inherit; text-decoration: none;">'
    'made possible by jamesjernigan.com'
    '</a></div>'
)
 
 
# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
 
def _safe_json_loads(raw: str):
    """
    Resiliently extracts JSON from an LLM response by stripping markdown fences
    and using a stack-based bracket matcher to ignore conversational filler.
    """
    text = raw.strip()
    
    # Clean standard markdown fences first
    # Using `{3}` instead of literal backticks to prevent UI truncation issues
    fence_pattern = r'^`{3}(?:json)?\n?'
    text = re.sub(fence_pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    end_fence_pattern = r'\n?`{3}$'
    text = re.sub(end_fence_pattern, '', text, flags=re.MULTILINE).strip()
    
    # Try a direct parse (best-case scenario)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
        
    # Stack-based extraction to ignore trailing conversational filler
    start_brace = text.find('{')
    start_bracket = text.find('[')
    
    if start_brace == -1 and start_bracket == -1:
        raise ValueError(f"No JSON object or array found in response: {raw[:100]}...")
        
    if start_brace != -1 and (start_bracket == -1 or start_brace < start_bracket):
        start_char, end_char = '{', '}'
        start_idx = start_brace
    else:
        start_char, end_char = '[', ']'
        start_idx = start_bracket
        
    stack = 0
    for i in range(start_idx, len(text)):
        if text[i] == start_char:
            stack += 1
        elif text[i] == end_char:
            stack -= 1
            # When stack returns to 0, we've found the end of the primary JSON object
            if stack == 0:
                try:
                    return json.loads(text[start_idx:i+1])
                except json.JSONDecodeError as e:
                    raise ValueError(f"Extracted JSON block was invalid: {e}")
                    
    raise ValueError("Failed to locate balanced JSON brackets in response.")
 
 
async def _generate_with_retry(session: LLMSession, base_prompt: str, model_type: str, pydantic_model=None):
    """
    Generates JSON and maps it to a Pydantic model (optional). If the LLM hallucinates 
    an invalid structure or invalid JSON, it catches the error and feeds it back to the 
    LLM to self-correct.
    """
    MAX_RETRIES = 3
    current_prompt = base_prompt
    
    for attempt in range(MAX_RETRIES):
        try:
            response_str = await session.generate(current_prompt, model_type=model_type, is_json=True)
            data_dict = _safe_json_loads(response_str)
            
            if pydantic_model:
                return pydantic_model.model_validate(data_dict)
            return data_dict
            
        except (ValueError, json.JSONDecodeError) as e:
            logger.warning(f"JSON Parse Error (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            current_prompt = base_prompt + f"\n\nYOUR PREVIOUS ATTEMPT FAILED WITH THIS JSON PARSE ERROR: {e}\nPlease correct the formatting and output ONLY valid JSON without markdown formatting."
        except ValidationError as e:
            logger.warning(f"Schema Validation Error (Attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            current_prompt = base_prompt + f"\n\nYOUR PREVIOUS ATTEMPT FAILED SCHEMA VALIDATION WITH THESE ERRORS:\n{e}\nPlease correct the data structure to match the required schema exactly."
            
    raise Exception(f"Failed to generate valid structured data after {MAX_RETRIES} attempts.")
 
 
def _inject_internal_link_safe(html: str, phrase: str, url: str) -> str:
    """
    Safely injects an <a> tag around the first occurrence of `phrase` within
    text nodes only.  Never touches HTML tag names, attribute values, existing
    anchor content, <script>, <style>, <code>, or <pre> blocks.
    """
    soup = BeautifulSoup(html, "html.parser")
 
    for text_node in soup.find_all(string=True):
        if text_node.parent.name in {"script", "style", "a", "code", "pre"}:
            continue
 
        if phrase in str(text_node):
            parts = str(text_node).split(phrase, 1)
            
            # Use a dummy wrapper to safely build the new mixed-content structure
            wrapper = soup.new_tag("span")
            
            if parts[0]:
                wrapper.append(NavigableString(parts[0]))
                
            a_tag = soup.new_tag("a", href=url)
            a_tag.string = phrase
            wrapper.append(a_tag)
            
            if parts[1]:
                wrapper.append(NavigableString(parts[1]))
                
            # Replace the old node and unwrap the dummy container
            text_node.replace_with(wrapper)
            wrapper.unwrap() 
            
            return str(soup)
 
    return html
 
 
# ---------------------------------------------------------------------------
# STEP 1
# ---------------------------------------------------------------------------
 
async def step1_query_generation(session: LLMSession, config: dict) -> str:
    prompt = (
        f"You are an AEO keyword researcher. Given this niche: {config['TARGET_NICHE']}, "
        f"these seed keywords: {config['INITIAL_KEYWORDS']}, and this ideal customer avatar: "
        f"{config['IDEAL_CUSTOMER_AVATAR']}, "
        "generate ONE specific long-tail search query (10-20 words) that this person would use "
        "when they need a direct answer. "
        "Output ONLY the query string, no punctuation, no quotes, no explanation."
    )
    response = await session.generate(prompt, model_type="PRIMARY_MODEL")
    return response.strip(' "\'\n.!?')
 
 
# ---------------------------------------------------------------------------
# WORDPRESS API WRAPPER
# ---------------------------------------------------------------------------
 
async def _wp_api_request_with_retry(
    method: str, url: str, auth: tuple, json_payload: dict, timeout: int = 30
):
    """
    Wraps WP REST API calls with exponential-backoff retry logic.
    Raises on non-2xx HTTP status codes AND on missing expected keys in the
    response body.
    """
    MAX_RETRIES = 3
    BASE_DELAY = 5.0
 
    for attempt in range(MAX_RETRIES):
        try:
            if method.lower() == "post":
                response = await asyncio.to_thread(
                    requests.post, url, auth=auth, json=json_payload, timeout=timeout
                )
            elif method.lower() == "put":
                response = await asyncio.to_thread(
                    requests.put, url, auth=auth, json=json_payload, timeout=timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
 
            response.raise_for_status()
            return response
 
        except requests.exceptions.RequestException as e:
            if attempt == MAX_RETRIES - 1:
                logger.error(f"WP API {method.upper()} failed after {MAX_RETRIES} attempts: {e}")
                raise
 
            wait_time = BASE_DELAY * (2 ** attempt)
            logger.warning(
                f"WP API {method.upper()} error (attempt {attempt + 1}/{MAX_RETRIES}): "
                f"{e}. Retrying in {wait_time}s..."
            )
            await asyncio.sleep(wait_time)
 
 
# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------
 
async def run_pipeline(config: dict, run_id: str):
    db_conn = get_db_connection(config.get("SQLITE_DB_PATH", "openclaw.db"))
    collection = get_vector_collection(config.get("CHROMA_DB_PATH", "./chroma_db"))
    # FIX (concurrency): Acquire the cross-process file lock before any ChromaDB
    # write operation. Initialized here so it is available throughout the pipeline.
    chroma_lock = get_chroma_lock(config.get("CHROMA_DB_PATH", "./chroma_db"))
    session = LLMSession(config=config, db_conn=db_conn, run_id=run_id)
 
    try:
        # ---------------------------------------------------------
        # Step 1: Query Generation
        # ---------------------------------------------------------
        query = await step1_query_generation(session, config)
        logger.info(f"Generated Query: {query}")
 
        # ---------------------------------------------------------
        # Step 2: Exact Deduplication Check
        # ---------------------------------------------------------
        def _check_existing():
            return db_conn.execute("SELECT id FROM posts WHERE query = ?", (query,)).fetchone()
            
        existing = await asyncio.to_thread(_check_existing)
        if existing:
            raise Exception(
                f"Exact query '{query}' already exists in SQLite. Run aborted to avoid duplication."
            )
 
        # ---------------------------------------------------------
        # Step 3: Semantic Cannibalization Check
        # ---------------------------------------------------------
        query_embedding = await asyncio.to_thread(generate_embedding, query, config)
        count = await asyncio.to_thread(collection.count)
        if count > 0:
            results = await asyncio.to_thread(
                collection.query,
                query_embeddings=[query_embedding],
                n_results=1,
                include=["distances"]
            )
            if results["distances"] and len(results["distances"][0]) > 0:
                similarity = 1 - (results["distances"][0][0] / 2)
                if similarity >= config.get("SIMILARITY_THRESHOLD", 0.85):
                    raise Exception(
                        f"Semantic cannibalization detected (Score: {similarity:.2f}). Run aborted."
                    )
 
        # ---------------------------------------------------------
        # Step 4: High-Level Search Grounding
        # ---------------------------------------------------------
        grounding_prompt = (
            f"Provide a comprehensive overview, latest facts, and direct answers for the query: '{query}'. "
            "Provide reference URLs to the sources you used."
        )
        grounded_answer = await session.generate(
            grounding_prompt, model_type="PRIMARY_MODEL", grounded=True
        )
 
        # ---------------------------------------------------------
        # Steps 5 & 6: DOM & Schema Extraction (Competitor Scraping)
        # ---------------------------------------------------------
        extracted_urls = re.findall(r'(https?://[^\s)\]\'"]+)', grounded_answer)
        reference_links = list(dict.fromkeys(extracted_urls))[:3]
        if not reference_links:
            logger.warning("No URLs extracted from grounded answer. Competitor scraping will be bypassed.")
 
        semaphore = asyncio.Semaphore(2)
 
        async def bounded_scrape(url, cfg):
            async with semaphore:
                return await scraper.scrape_url(url, cfg)
 
        scrape_tasks = [bounded_scrape(url, config) for url in reference_links]
        competitors = await asyncio.gather(*scrape_tasks)
 
        # ---------------------------------------------------------
        # Step 7: Gap Analysis
        # ---------------------------------------------------------
        
        # Filter out failed scrapes to prevent passing errors to the LLM
        valid_competitors = [c for c in competitors if c.scrape_quality != "failed"]
        
        competitor_summaries = ""
        if valid_competitors:
            for i, comp in enumerate(valid_competitors):
                comp_title = comp.title or "Unknown Title"
                comp_summary = comp.content_summary or "No summary available"
                # Limiting each summary to 1500 chars to save tokens
                competitor_summaries += f"--- Competitor {i+1}: {comp_title} ---\n{comp_summary[:1500]}\n\n"
        else:
            competitor_summaries = "No usable competitor data was successfully scraped."
 
        gap_prompt = (
            f"Analyze the following grounded data and competitor summaries for '{query}'.\n"
            f"Grounded Data: {grounded_answer[:1500]}...\n\n"
            f"Competitor Data:\n{competitor_summaries}\n\n"
            "Identify 3 missing questions, statistics, or structural formats not covered. "
            'Return JSON: {"gaps": ["gap1", "gap2", "gap3"]}'
        )
        gap_analysis_dict = await _generate_with_retry(session, gap_prompt, model_type="REASONING_MODEL")
        gap_analysis_str = json.dumps(gap_analysis_dict)
 
        # ---------------------------------------------------------
        # Step 8: AEO Outline Creation
        # ---------------------------------------------------------
        outline_prompt = (
            f"Create a JSON content outline for '{query}' addressing these gaps: {gap_analysis_str}. "
            "Output strictly valid JSON matching this structure: {"
            '"target_query": "...", "primary_keyword": "...", "secondary_keywords": ["..."], '
            '"search_intent": "...", "page_title": "...", "meta_description": "...", "h1": "...", '
            '"sections": [{"h2": "...", "purpose": "...", "subsections": [], '
            '"content_type": "prose", "target_word_count": 300}], '
            '"answer_block": {"answer_text": "...", "answer_type": "definition", '
            '"contains_primary_keyword": true}, '
            '"schema_types_to_generate": ["Article"], "content_gaps_addressed": ["..."], '
            '"estimated_word_count": 1500'
            "}"
        )
        outline_model = await _generate_with_retry(
            session, outline_prompt, model_type="REASONING_MODEL", pydantic_model=ContentOutline
        )
 
        # ---------------------------------------------------------
        # Step 8.5: Task Reference File (TRF) Instantiation
        # ---------------------------------------------------------
        scrape_quality, scrape_score = scraper.calculate_trf_quality(competitors)
        combined_schemas = []
        for c in valid_competitors:
            combined_schemas.extend(c.schema_types_found)
        combined_schemas = list(set(combined_schemas))
 
        trf_model = TaskReferenceFile(
            run_id=run_id,
            query=query,
            search_intent=outline_model.search_intent,
            gemini_synthesized_answer=grounded_answer,
            gemini_reference_links=reference_links,
            competitors=competitors,  # Models validates full list including failures
            competitor_schema_types_combined=combined_schemas,
            overall_scrape_quality=scrape_quality,
            overall_scrape_quality_score=scrape_score
        )
        logger.debug(f"TRF Instantiated with quality '{scrape_quality}' and score {scrape_score}")
 
        # ---------------------------------------------------------
        # Step 9: Content Generation (Chunked)
        # ---------------------------------------------------------
        full_html_body = (
            "\n<div class='answer-block' itemscope itemtype='https://schema.org/Answer'>\n"
            f"<span itemprop='text'>{outline_model.answer_block.answer_text}</span>\n"
            "</div>\n\n"
        )
 
        for section in outline_model.sections:
            section_prompt = (
                f"Write the '{section.h2}' section for '{query}'. "
                f"Purpose: {section.purpose}. "
                "Return ONLY raw HTML (e.g. <h2>...</h2><p>...</p>)."
            )
            section_html = await session.generate(section_prompt, model_type="REASONING_MODEL")
            full_html_body += f"\n{section_html.strip()}\n\n"
 
        # ---------------------------------------------------------
        # Step 9.5: Semantic Internal Linking
        # ---------------------------------------------------------
        collection_count = await asyncio.to_thread(collection.count)
        injected_links = []
 
        if collection_count > 0:
            link_results = await asyncio.to_thread(
                collection.query,
                query_embeddings=[query_embedding],
                n_results=min(
                    collection_count, config.get("MAX_INBOUND_LINKS_PER_POST", 5) + 1
                ),
                include=["metadatas"]
            )
 
            target_links = []
            if link_results and link_results.get("metadatas") and link_results["metadatas"][0]:
                for metadata in link_results["metadatas"][0]:
                    if (
                        metadata["query"] != query
                        and len(target_links) < config.get("MAX_INBOUND_LINKS_PER_POST", 3)
                    ):
                        def _get_target_id(q):
                            return db_conn.execute(
                                "SELECT id FROM posts WHERE query = ?", (q,)
                            ).fetchone()
                        
                        target_db_row = await asyncio.to_thread(_get_target_id, metadata["query"])
                        
                        if target_db_row:
                            target_links.append({
                                "id": target_db_row["id"],
                                "url": metadata["url"],
                                "query": metadata["query"]
                            })
 
            if target_links:
                logger.info(f"Attempting to inject internal links to: {[l['url'] for l in target_links]}")
                linking_prompt = (
                    f"Given these target URLs and their topics: {target_links}\n"
                    "Find exact, verbatim short phrases (2-5 words) in the following HTML that are "
                    "highly relevant to act as anchor text for each URL. "
                    "Return ONLY a JSON array of objects strictly matching this structure: "
                    '[{"url": "...", "exact_phrase": "..."}]\n'
                    f"HTML:\n{full_html_body}"
                )
                try:
                    linking_data = await _generate_with_retry(session, linking_prompt, model_type="REASONING_MODEL")
 
                    # Type Guard: If the LLM wraps the array in an object (e.g., {"links": [...]})
                    if isinstance(linking_data, dict):
                        linking_data = next((v for v in linking_data.values() if isinstance(v, list)), [])
 
                    for item in linking_data:
                        if not isinstance(item, dict): 
                            continue
                            
                        url = item.get("url")
                        phrase = item.get("exact_phrase")
 
                        # Skip if already linked to this URL
                        if (
                            url
                            and phrase
                            and f'"{url}"' not in full_html_body
                            and f"'{url}'" not in full_html_body
                        ):
                            updated_html = _inject_internal_link_safe(full_html_body, phrase, url)
                            if updated_html is not full_html_body:
                                full_html_body = updated_html
                                target_id = next(
                                    (l["id"] for l in target_links if l["url"] == url), None
                                )
                                if target_id:
                                    injected_links.append({"target_id": target_id, "anchor": phrase})
 
                except Exception as e:
                    logger.warning(f"Internal linking injection failed or skipped: {e}")
 
        full_html_body += f"\n{FOOTER_HTML}\n"
 
        # ---------------------------------------------------------
        # Step 10: Quality Gate & Phase 1 WP Publish (Draft)
        # ---------------------------------------------------------
        
        # FIXED: BeautifulSoup parsing offloaded to prevent event loop blocking
        def _get_word_count(html):
            text = BeautifulSoup(html, "html.parser").get_text()
            return len(re.findall(r'\b\w+\b', text))
            
        final_word_count = await asyncio.to_thread(_get_word_count, full_html_body)
        min_word_count = config.get("MIN_WORD_COUNT", 1200)
 
        if final_word_count < min_word_count:
            raise Exception(
                f"Quality Gate Failed: Generated word count ({final_word_count}) "
                f"is below minimum required ({min_word_count})."
            )
 
        wp_auth = (config["WP_USERNAME"], config["WP_APP_PASSWORD"])
        wp_endpoint = f"{config['WP_URL'].rstrip('/')}/wp-json/wp/v2/posts"
        meta_key = config.get("WP_SEO_META_DESC_KEY", "_yoast_wpseo_metadesc")
 
        draft_payload = {
            "title": outline_model.page_title,
            "content": full_html_body,
            "status": "draft",
            "meta": {meta_key: outline_model.meta_description}
        }
 
        try:
            draft_response = await _wp_api_request_with_retry("post", wp_endpoint, wp_auth, draft_payload)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 400 and "meta" in e.response.text.lower():
                logger.warning(
                    f"WP API rejected the payload with HTTP 400. This is likely due to unregistered "
                    f"SEO meta keys ({meta_key}). Retrying draft creation without the meta payload."
                )
                del draft_payload["meta"]
                draft_response = await _wp_api_request_with_retry("post", wp_endpoint, wp_auth, draft_payload)
            else:
                raise
 
        try:
            draft_json = draft_response.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception(
                f"WordPress POST returned HTTP {draft_response.status_code} but response body "
                f"is not valid JSON. The request was likely blocked by a security plugin or WAF. "
                f"Raw response: {draft_response.text[:500]}"
            )
 
        if "id" not in draft_json:
            raise Exception(
                f"WordPress POST returned HTTP {draft_response.status_code} but response body "
                f"contains no 'id' key. The request was likely blocked by a security plugin or WAF. "
                f"Full response body: {draft_json}"
            )
        wp_post_id = draft_json["id"]
        canonical_url = draft_json["link"]
 
        # ---------------------------------------------------------
        # Step 11: Schema Generation & Phase 2 WP Publish (Final)
        # ---------------------------------------------------------
        
        # Now pass the populated TRF object to drive competitive gap schema generation
        unified_schema = schema_engine.generate_dynamic_schema(
            outline=outline_model,
            trf=trf_model,           
            canonical_url=canonical_url,
            config=config
        )
 
        full_html_body += f'\n<script type="application/ld+json">\n{unified_schema}\n</script>\n'
        
        # Validate schema structure and ensure exact alignment with the final Pydantic model payload
        schema_block_dict = schema_engine.validate_and_count_schema(unified_schema)
        schema_block_model = SchemaBlock(**schema_block_dict)
 
        generated_content = GeneratedContent(
            outline=outline_model,
            html_body=full_html_body,
            title_tag=outline_model.page_title,
            meta_description=outline_model.meta_description,
            schema_blocks=[schema_block_model],
            cta_injection_count=full_html_body.count(config.get("CTA_LINK", "")),
            word_count=final_word_count,
            readability_score=0.0,  # Stub for future readability analytics
            fact_check_passed=True,
            fact_check_notes="Automated run passed."
        )
        logger.info(
            f"GeneratedContent validated. Final Output: "
            f"{generated_content.word_count} words, {schema_block_dict['entity_count']} schema entities."
        )
 
        publish_payload = {
            "content": full_html_body,
            "status": config.get("PUBLISH_MODE", "publish")
        }
 
        publish_endpoint = f"{wp_endpoint}/{wp_post_id}"
        publish_response = await _wp_api_request_with_retry(
            "put", publish_endpoint, wp_auth, publish_payload
        )
 
        try:
            publish_json = publish_response.json()
        except requests.exceptions.JSONDecodeError:
            raise Exception(
                f"WordPress PUT returned HTTP {publish_response.status_code} but response body "
                f"is not valid JSON. The request was likely blocked by a security plugin or WAF. "
                f"Raw response: {publish_response.text[:500]}"
            )
 
        if "link" not in publish_json:
            raise Exception(
                f"WordPress PUT returned HTTP {publish_response.status_code} but response body "
                f"contains no 'link' key. Full response body: {publish_json}"
            )
        wp_post_url = publish_json["link"]
        logger.info(f"Successfully published to WP! ID: {wp_post_id} | URL: {wp_post_url}")
 
        # ---------------------------------------------------------
        # Step 12: Post Audit Record & Internal Linking Logging (Transactional)
        # ---------------------------------------------------------
        # FIX (stability): Replaced the post-INSERT SELECT by wp_post_id with
        # cursor.lastrowid.  Using lastrowid is atomic within the transaction and
        # eliminates the edge-case risk of fetching the wrong row if a duplicate
        # wp_post_id somehow exists (e.g. from a partial failed run).
        def _log_all_db_records():
            with db_conn:
                cursor = db_conn.execute("""
                    INSERT INTO posts (query, wp_post_id, wp_url, wp_status, embedding_text, published_at, run_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    query, wp_post_id, wp_post_url, "publish",
                    f"{query} {outline_model.page_title} {gap_analysis_str}",
                    datetime.now(timezone.utc).isoformat(), run_id
                ))
 
                # Capture the autoincrement ID directly from the INSERT cursor —
                # no secondary SELECT required.
                post_id = cursor.lastrowid
                
                for link in injected_links:
                    db_conn.execute("""
                        INSERT INTO internal_links (source_post_id, target_post_id, anchor_text)
                        VALUES (?, ?, ?)
                    """, (post_id, link["target_id"], link["anchor"]))
                    
                return post_id
                
        post_id_db = await asyncio.to_thread(_log_all_db_records)
 
        if injected_links:
            logger.info(f"Logged {len(injected_links)} internal links to database.")
 
        # ---------------------------------------------------------
        # Step 13: Indexing & Vectors
        # ---------------------------------------------------------
        # FIX (concurrency): Acquire the cross-process file lock before writing to
        # ChromaDB. Without this, two overlapping cron runs will corrupt the HNSW
        # vector index. Read-only calls (.count(), .query()) earlier in the pipeline
        # do not need the lock.
        def _chroma_add():
            with chroma_lock:
                collection.add(
                    ids=[str(post_id_db)],
                    embeddings=[query_embedding],
                    metadatas=[{"url": wp_post_url, "query": query}]
                )
 
        await asyncio.to_thread(_chroma_add)
 
        if config.get("INDEXNOW_KEY"):
            indexnow_payload = {
                "host": (
                    config["WP_URL"]
                    .replace("https://", "")
                    .replace("http://", "")
                    .rstrip("/")
                ),
                "key": config["INDEXNOW_KEY"],
                "urlList": [wp_post_url]
            }
            await asyncio.to_thread(
                requests.post,
                "https://api.indexnow.org/indexnow",
                json=indexnow_payload,
                timeout=10
            )
 
        def _mark_completed():
            db_conn.execute(
                "UPDATE run_log SET status = 'completed' WHERE run_id = ?",
                (run_id,)
            )
            db_conn.commit()
            
        await asyncio.to_thread(_mark_completed)
        logger.info(f"Run {run_id} completed successfully for query: {query}")
 
    except CostCapException as e:
        logger.error(f"Cost Cap Reached: {e}")
        def _mark_cost_cap():
            db_conn.execute(
                "INSERT INTO run_log (run_id, status, error_message) VALUES (?, 'halted_cost_cap', ?) "
                "ON CONFLICT(run_id) DO UPDATE SET status='halted_cost_cap', error_message=?",
                (run_id, str(e), str(e))
            )
            db_conn.commit()
        await asyncio.to_thread(_mark_cost_cap)
        raise
    except Exception as e:
        logger.error(f"Pipeline Failed: {e}", exc_info=True)
        def _mark_failed():
            db_conn.execute(
                "INSERT INTO run_log (run_id, status, error_message) VALUES (?, 'failed', ?) "
                "ON CONFLICT(run_id) DO UPDATE SET status='failed', error_message=?",
                (run_id, str(e), str(e))
            )
            db_conn.commit()
        await asyncio.to_thread(_mark_failed)
        raise
    finally:
        cost_summary = session.finalize()
        logger.info(
            f"Run {run_id} session closed. Total LLM calls: {cost_summary['llm_calls']}, "
            f"Cost: ${cost_summary['estimated_cost_usd']:.4f}"
        )
        db_conn.close()
 
 
if __name__ == "__main__":
    from config import DEFAULT_CONFIG
    
    # 1. Lock in the global environment variables synchronously before the event loop starts.
    configure_global_environment(DEFAULT_CONFIG.get("CHROMA_DB_PATH", "./chroma_db"))
    
    # 2. Generate run ID
    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    # 3. Spin up the async pipeline
    asyncio.run(run_pipeline(DEFAULT_CONFIG, run_id))
 