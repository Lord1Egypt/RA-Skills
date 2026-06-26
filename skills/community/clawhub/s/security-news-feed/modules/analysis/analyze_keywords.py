import requests
import re
from collections import Counter
import sys
import os
import time
import concurrent.futures
import asyncio
import aiohttp
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional, Tuple

# Add current directory to Python path to allow imports from modules
# Add project root to Python path to allow imports from modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import NOTION_API_TOKEN, BOANISSUE_DATABASE_ID, KEYWORD_STATS_DATABASE_ID
from modules.notion_handler import get_data_source_info
from modules.resources.korean_stopwords import stop_words as korean_stop_words
from modules.resources.english_stopwords import stop_words as english_stop_words
from modules.analysis.cache_manager import KeywordCacheManager


# ========================
# Async API Client (Connection Pooling)
# ========================

class AsyncNotionClient:
    """
    비동기 Notion API 클라이언트
    연결 풀링 및 세션 재사용으로 성능 최적화
    """
    def __init__(self, api_token: str, max_connections: int = 10):
        self.api_token = api_token
        self.max_connections = max_connections
        self._session: Optional[aiohttp.ClientSession] = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2025-09-03"
        }

    async def __aenter__(self):
        """컨텍스트 매니저 진입"""
        timeout = aiohttp.ClientTimeout(total=120, connect=30)
        connector = aiohttp.TCPConnector(limit=self.max_connections)
        self._session = aiohttp.ClientSession(
            headers=self._headers,
            timeout=timeout,
            connector=connector
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        if self._session:
            await self._session.close()

    async def post(self, url: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """비동기 POST 요청"""
        if not self._session:
            raise RuntimeError("AsyncNotionClient not initialized. Use 'async with' statement.")

        async with self._session.post(url, json=json_data) as response:
            response.raise_for_status()
            return await response.json()

    async def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """비동기 GET 요청"""
        if not self._session:
            raise RuntimeError("AsyncNotionClient not initialized. Use 'async with' statement.")

        async with self._session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

    async def patch(self, url: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """비동기 PATCH 요청"""
        if not self._session:
            raise RuntimeError("AsyncNotionClient not initialized. Use 'async with' statement.")

        async with self._session.patch(url, json=json_data) as response:
            response.raise_for_status()
            return await response.json()


# ========================
# Async Helper Functions
# ========================

async def fetch_page_batch_async(
    client: AsyncNotionClient,
    data_source_id: str,
    start_cursor: Optional[str] = None,
    page_size: int = 100,
    date_filter: Optional[Dict[str, Any]] = None
) -> Tuple[List[Dict[str, Any]], Optional[str], bool]:
    """
    비동기로 페이지 배치를 가져옵니다.

    Returns:
        (페이지 목록, 다음 커서, has_more)
    """
    endpoint = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    payload = {"page_size": page_size}

    if date_filter:
        payload["filter"] = date_filter

    if start_cursor:
        payload["start_cursor"] = start_cursor

    data = await client.post(endpoint, payload)
    results = data.get("results", [])
    next_cursor = data.get("next_cursor")
    has_more = data.get("has_more", False)

    return results, next_cursor, has_more


async def fetch_all_titles_async(
    database_id: str,
    since_date: Optional[datetime] = None,
    use_cache: bool = True
) -> List[Dict[str, Any]]:
    """
    비동기로 모든 제목을 가져옵니다.
    """
    cache_manager = get_cache_manager() if use_cache else None

    # 캐시 확인
    if cache_manager and since_date:
        cached_titles = cache_manager.get_cached_titles(since=since_date)
        if cached_titles:
            print(f"[Cache] Hit! Found {len(cached_titles)} cached titles since {since_date.strftime('%Y-%m-%d')}")
            return cached_titles

    # 비동기 클라이언트로 데이터 가져오기
    async with AsyncNotionClient(NOTION_API_TOKEN) as client:
        # 데이터베이스 정보 가져오기
        headers = {
            "Authorization": f"Bearer {NOTION_API_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2025-09-03"
        }
        data_source_id, db_props = get_data_source_info(database_id, headers)
        if not data_source_id:
            return []

        # 속성 이름 찾기
        title_prop_name = None
        date_prop_name = None

        for pn, pinfo in db_props.items():
            if pinfo.get('type') == 'title':
                title_prop_name = pn
            elif pinfo.get('type') == 'date':
                date_prop_name = pn

        if not title_prop_name:
            return []

        # 날짜 필터 설정
        date_filter = None
        if date_prop_name and since_date:
            date_filter = {
                "property": date_prop_name,
                "date": {"on_or_after": since_date.isoformat()}
            }

        # 모든 페이지 비동기로 가져오기
        titles_data = []
        has_more = True
        start_cursor = None
        batch_count = 0

        while has_more:
            pages, next_cursor, has_more = await fetch_page_batch_async(
                client, data_source_id, start_cursor, 100, date_filter
            )

            for page in pages:
                props = page.get("properties", {})
                title_obj = props.get(title_prop_name, {}).get("title", [])
                if title_obj:
                    title_text = "".join([t.get("plain_text", "") for t in title_obj])
                    if title_text.strip():
                        titles_data.append({
                            "id": page.get("id"),
                            "title": title_text.strip()
                        })

            start_cursor = next_cursor
            batch_count += 1
            print(f"Async batch {batch_count}: Fetched {len(titles_data)} titles so far...")

        # 캐시 업데이트
        if cache_manager and titles_data:
            cache_manager.cache_titles(titles_data)

        return titles_data


def fetch_all_titles_async_wrapper(
    database_id: str,
    since_date: Optional[datetime] = None,
    use_cache: bool = True
) -> List[Dict[str, Any]]:
    """
    비동기 함수를 동기 코드에서 호출하기 위한 래퍼
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        fetch_all_titles_async(database_id, since_date, use_cache)
    )

# --- Configuration ---
# Target Database ID for Keyword Statistics
TARGET_STATS_DATABASE_ID = KEYWORD_STATS_DATABASE_ID

SOURCE_DATABASE_ID = BOANISSUE_DATABASE_ID

# Timestamp file for incremental updates
TIMESTAMP_FILE = ".keyword_last_run"

# Global cache manager
_cache_manager = None

def get_cache_manager():
    """Get or initialize the cache manager singleton."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = KeywordCacheManager()
    return _cache_manager

def get_last_run_timestamp():
    """
    Loads the last run timestamp from file.
    Returns datetime in UTC or None if file doesn't exist.
    """
    try:
        timestamp_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp_path = os.path.join(timestamp_dir, TIMESTAMP_FILE)
        with open(timestamp_path, 'r', encoding='utf-8') as f:
            timestamp_str = f.read().strip()
            return datetime.fromisoformat(timestamp_str)
    except FileNotFoundError:
        # First run: return 30 days ago
        return datetime.now(timezone.utc) - timedelta(days=30)
    except Exception as e:
        print(f"[WARN] Failed to load last run timestamp: {e}. Using 30 days ago.")
        return datetime.now(timezone.utc) - timedelta(days=30)

def save_last_run_timestamp():
    """
    Saves the current timestamp to file.
    """
    try:
        timestamp_dir = os.path.dirname(os.path.abspath(__file__))
        timestamp_path = os.path.join(timestamp_dir, TIMESTAMP_FILE)
        with open(timestamp_path, 'w', encoding='utf-8') as f:
            f.write(datetime.now(timezone.utc).isoformat())
    except Exception as e:
        print(f"[WARN] Failed to save last run timestamp: {e}")

def fetch_all_titles(database_id, since_date=None, use_cache=True):
    """
    Fetches titles from specified Notion database.
    [Optimized] If since_date is provided, only fetches titles after that date.
    [Cache] Uses local SQLite cache to reduce API calls.
    """
    print(f"Fetching titles from DB: {database_id}...")

    cache_manager = get_cache_manager() if use_cache else None

    # Try to fetch from cache first
    if cache_manager and since_date:
        cached_titles = cache_manager.get_cached_titles(since=since_date)
        if cached_titles:
            print(f"[Cache] Hit! Found {len(cached_titles)} cached titles since {since_date.strftime('%Y-%m-%d')}")
            return cached_titles
        else:
            print(f"[Cache] Miss. Fetching from Notion API...")

    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }

    data_source_id, db_props = get_data_source_info(database_id, headers)
    if not data_source_id:
        print("Failed to get data_source_id.")
        return []

    # Find title and date property names
    title_prop_name = None
    date_prop_name = None

    for pn, pinfo in db_props.items():
        if pinfo.get('type') == 'title':
            title_prop_name = pn
        elif pinfo.get('type') == 'date':
            date_prop_name = pn

    if not title_prop_name:
        print("Could not find a 'title' property in database.")
        return []

    endpoint = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"

    # Use provided since_date or default to 30 days ago
    if since_date is None:
        since_date = datetime.now(timezone.utc) - timedelta(days=30)

    print(f"[Optimization] Filtering titles from: {since_date.strftime('%Y-%m-%d')} (incremental)")

    titles_data = []
    has_more = True
    start_cursor = None

    while has_more:
        payload = {"page_size": 100}

        # Add date filter if date property exists
        if date_prop_name:
            payload["filter"] = {
                "property": date_prop_name,
                "date": {"on_or_after": since_date.isoformat()}
            }
        else:
            # If no date property found, warn and fetch all
            print("Warning: No 'date' property found. Fetching all titles.")

        if start_cursor:
            payload["start_cursor"] = start_cursor

        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            for page in data.get("results", []):
                props = page.get("properties", {})
                title_obj = props.get(title_prop_name, {}).get("title", [])
                if title_obj:
                    title_text = "".join([t.get("plain_text", "") for t in title_obj])
                    if title_text.strip():
                        titles_data.append({
                            "id": page.get("id"),
                            "title": title_text.strip()
                        })

            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
            print(f"Fetched {len(titles_data)} titles so far...")

        except Exception as e:
            print(f"Error fetching pages: {e}")
            break

    # Update cache
    if cache_manager and titles_data:
        cache_manager.cache_titles(titles_data)

    return titles_data

def tokenize_and_count(titles_data):
    """
    Tokenizes titles and counts keyword frequencies.
    Returns a dict: {keyword: {'count': int, 'pages': [page_id1, page_id2, ...]}}
    """
    print("Analyzing keywords...")
    keyword_stats = {} # {keyword: {'count': 0, 'pages': []}}
    
    # Use imported stop words and add symbols
    stop_words = korean_stop_words.union(english_stop_words).union({
        '-', ':', '[', ']', '(', ')', '!', '?', '.', ',', '"', "'",
        'to', 'in', 'for', 'of', 'a', 'the', 'and', 'on', 'at', 'with', 'by', 'from', 'up', 'about', 'into', 'over', 'after'
    })

    for item in titles_data:
        title = item['title']
        page_id = item['id']
        
        # Remove special characters but keep spaces and Hangul/English
        cleaned = re.sub(r'[^\w\s가-힣a-zA-Z]', ' ', title)
        tokens = cleaned.split()
        
        # Use a set to avoid counting the same keyword multiple times for the same title
        unique_tokens_in_title = set()
        
        for token in tokens:
            if len(token) > 1 and token.lower() not in stop_words: # Ignore single characters and stop words
                unique_tokens_in_title.add(token)
        
        for token in unique_tokens_in_title:
            if token not in keyword_stats:
                keyword_stats[token] = {'count': 0, 'pages': []}
            
            keyword_stats[token]['count'] += 1
            keyword_stats[token]['pages'].append(page_id)
                
    return keyword_stats

def update_keyword_page_content(keyword_page_id, source_page_ids, use_cache=True):
    """
    Updates content of a keyword page with links to source pages.
    [Optimized] Smart update: Only add new pages, don't delete existing blocks.
    [Cache] Uses local SQLite cache to reduce API calls.
    """
    cache_manager = get_cache_manager() if use_cache else None

    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }

    children_url = f"https://api.notion.com/v1/blocks/{keyword_page_id}/children"

    # 1. Try to get existing page IDs from cache
    existing_page_ids = set()

    if cache_manager:
        cached_children = cache_manager.get_cached_page_children(keyword_page_id)
        if cached_children:
            for child in cached_children:
                page_link_id = child.get("page_link_id")
                if page_link_id:
                    existing_page_ids.add(page_link_id)
            print(f"[Cache] Hit! Found {len(existing_page_ids)} cached children for page {keyword_page_id}")
        else:
            print(f"[Cache] Miss. Fetching children from Notion API...")

    # 2. If cache miss, fetch from Notion API
    if not existing_page_ids:
        has_more = True
        start_cursor = None

        try:
            while has_more:
                params = {"page_size": 100}
                if start_cursor:
                    params["start_cursor"] = start_cursor

                response = requests.get(children_url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    blocks = data.get("results", [])

                    cache_batch = []  # For cache update

                    for block in blocks:
                        if block.get("type") == "link_to_page":
                            page_id = block["link_to_page"].get("page_id")
                            if page_id:
                                existing_page_ids.add(page_id)
                                cache_batch.append({
                                    "block_id": block.get("id"),
                                    "page_link_id": page_id
                                })

                    # Update cache
                    if cache_manager and cache_batch:
                        cache_manager.cache_page_children(keyword_page_id, cache_batch)

                    has_more = data.get("has_more", False)
                    start_cursor = data.get("next_cursor")
                else:
                    break
        except Exception as e:
            print(f"[WARN] Failed to fetch existing blocks for page {keyword_page_id}: {e}")

    # 3. Identify new pages (not in existing)
    limit_top = source_page_ids[:50]  # Limit to top 50
    new_page_ids = [pid for pid in limit_top if pid not in existing_page_ids]

    if not new_page_ids:
        # No new pages to add, skip API call
        return

    # 4. Add only new page links
    new_blocks = []

    # Add a heading only if there are new pages
    new_blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": f"Related Articles ({len(limit_top)})"}}]
        }
    })

    for pid in new_page_ids:
        new_blocks.append({
            "object": "block",
            "type": "link_to_page",
            "link_to_page": {
                "type": "page_id",
                "page_id": pid
            }
        })

    # Batch append (Notion allows up to 100 blocks per request)
    try:
        payload = {"children": new_blocks}
        response = requests.patch(children_url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            print(f"[Optimization] Added {len(new_page_ids)} new links to keyword page {keyword_page_id}")
        else:
            print(f"[WARN] Failed to add blocks for page {keyword_page_id}: Status {response.status_code}")
    except Exception as e:
        print(f"[WARN] Error appending blocks for page {keyword_page_id}: {e}")


def update_stats_db(target_db_id, stats):
    """
    Updates the target Notion database with keyword statistics.
    stats: {keyword: {'count': int, 'pages': []}}
    """
    if target_db_id == "REPLACE_WITH_YOUR_TARGET_DATABASE_ID":
        print("Please set the TARGET_STATS_DATABASE_ID in the script.")
        return

    print(f"Updating target DB: {target_db_id}...")
    headers = {
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03"
    }

    # 1. Get Target DB Info
    data_source_id, db_props = get_data_source_info(target_db_id, headers)
    if not data_source_id:
        print("Failed to get target DB info.")
        return

    # 2. Find Property Names (Keyword: Title, Count: Number)
    keyword_prop_name = None
    count_prop_name = None
    
    for pn, pinfo in db_props.items():
        if pinfo.get('type') == 'title':
            keyword_prop_name = pn
        elif pinfo.get('type') == 'number':
            count_prop_name = pn
            
    if not keyword_prop_name or not count_prop_name:
        print(f"Target DB must have a Title property and a Number property. Found: Title={keyword_prop_name}, Number={count_prop_name}")
        return

    # 3. Fetch Existing Items to Update
    existing_items = {} # {keyword: page_id}
    endpoint = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    
    has_more = True
    start_cursor = None
    
    print("Fetching existing stats to update...")
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
            
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for page in data.get("results", []):
                props = page.get("properties", {})
                # Get Keyword
                k_obj = props.get(keyword_prop_name, {}).get("title", [])
                k_text = "".join([t.get("plain_text", "") for t in k_obj])
                if k_text:
                    existing_items[k_text] = page.get("id")
            
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        except Exception as e:
            print(f"Error fetching existing stats: {e}")
            break

    # 4. Update or Create
    print(f"Found {len(existing_items)} existing keywords.")
    
    # 4. Update or Create
    print(f"Found {len(existing_items)} existing keywords.")
    
    # Sort stats by count desc and take TOP 50
    sorted_stats = sorted(stats.items(), key=lambda item: item[1]['count'], reverse=True)[:50]
    
    current_top_keywords = set()
    
    # Helper function for parallel execution
    def process_keyword_update(item):
        keyword, data = item
        count = data['count']
        source_pages = data['pages']
        
        target_page_id = None
        
        if keyword in existing_items:
            # Update
            target_page_id = existing_items[keyword]
            print(f"Updating '{keyword}': {count}")
            update_url = f"https://api.notion.com/v1/pages/{target_page_id}"
            payload = {
                "properties": {
                    count_prop_name: {"number": count}
                }
            }
            try:
                requests.patch(update_url, headers=headers, json=payload)
            except Exception as e:
                print(f"Failed to update {keyword}: {e}")
        else:
            # Create
            print(f"Creating '{keyword}': {count}")
            create_url = "https://api.notion.com/v1/pages"
            payload = {
                "parent": {"type": "data_source_id", "data_source_id": data_source_id},
                "properties": {
                    keyword_prop_name: {"title": [{"text": {"content": keyword}}]},
                    count_prop_name: {"number": count}
                }
            }
            try:
                resp = requests.post(create_url, headers=headers, json=payload)
                if resp.status_code == 200:
                    target_page_id = resp.json().get("id")
            except Exception as e:
                print(f"Failed to create {keyword}: {e}")
        
        # Update content with links
        if target_page_id:
            update_keyword_page_content(target_page_id, source_pages)

    # Collect items for processing
    items_to_process = []
    for keyword, data in sorted_stats:
        current_top_keywords.add(keyword)
        items_to_process.append((keyword, data))

    # Run updates in parallel
    print(f"Updating {len(items_to_process)} keywords in parallel (max_workers=5)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_keyword_update, items_to_process)

    # 5. Cleanup Stale Keywords
    # Archive pages that are in existing_items but NOT in current_top_keywords
    print("Cleaning up stale keywords...")
    
    stale_items = []
    for keyword, page_id in existing_items.items():
        if keyword not in current_top_keywords:
            stale_items.append((keyword, page_id))
            
    def process_keyword_archive(item):
        keyword, page_id = item
        print(f"Archiving stale keyword: '{keyword}'")
        archive_url = f"https://api.notion.com/v1/pages/{page_id}"
        payload = {"archived": True}
        try:
            requests.patch(archive_url, headers=headers, json=payload)
        except Exception as e:
            print(f"Failed to archive {keyword}: {e}")

    if stale_items:
        print(f"Archiving {len(stale_items)} stale keywords in parallel...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_keyword_archive, stale_items)
    else:
        print("No stale keywords found.")

def run_keyword_analysis():
    """
    [Trigger-based] Only runs if new articles exist since last run.
    [Optimized] Uses incremental fetching and caching.
    """
    print("="*70)
    print("Keyword Analysis Trigger Check (Optimized)")
    print("="*70)

    # 1. Load last run timestamp
    last_run = get_last_run_timestamp()
    print(f"Last run timestamp: {last_run.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # 2. Check for new articles (incremental fetch)
    print("\nChecking for new articles...")
    titles_data = fetch_all_titles(SOURCE_DATABASE_ID, since_date=last_run, use_cache=True)
    print(f"New articles since last run: {len(titles_data)}")

    # 3. Trigger: Only run if new articles exist
    if not titles_data:
        print("\n[Trigger] No new articles found. Skipping analysis to save API calls.")
        print("[Trigger] Will check again in next scheduled run (6 hours).")
        print("="*70)
        return False  # Indicate no analysis was performed

    # 4. Proceed with analysis
    print(f"\n[Trigger] {len(titles_data)} new articles found. Starting analysis...")

    # 5. Analyze
    print("Analyzing keywords...")
    stats = tokenize_and_count(titles_data)

    # Merge with cached stats if exists
    cache_manager = get_cache_manager()
    cached_stats = cache_manager.get_cached_keyword_stats() if cache_manager else None

    if cached_stats:
        print(f"[Cache] Merging {len(cached_stats)} cached keywords with {len(stats)} new ones...")
        # Merge: update counts and combine page IDs
        for keyword, data in stats.items():
            if keyword in cached_stats:
                cached_stats[keyword]['count'] += data['count']
                cached_stats[keyword]['pages'].extend(data['pages'])
                # Deduplicate page IDs while preserving order
                seen = set()
                unique_pages = []
                for pid in cached_stats[keyword]['pages']:
                    if pid not in seen:
                        seen.add(pid)
                        unique_pages.append(pid)
                cached_stats[keyword]['pages'] = unique_pages
            else:
                cached_stats[keyword] = data
        stats = cached_stats
        print(f"[Cache] Merged total: {len(stats)} keywords")

    print("\nTop 20 Keywords:")
    # Sort for display
    sorted_display = sorted(stats.items(), key=lambda item: item[1]['count'], reverse=True)[:20]
    for k, v in sorted_display:
        print(f"{k}: {v['count']}")

    # 6. Update cache with merged stats
    if cache_manager:
        cache_manager.cache_keyword_stats(stats)
        cache_stats = cache_manager.get_cache_stats()
        print(f"\n[Cache Stats] Titles: {cache_stats.get('titles_count', 0)}, "
              f"Keywords: {cache_stats.get('keywords_count', 0)}, "
              f"Page Children: {cache_stats.get('page_children_count', 0)}")

    # 7. Push to Notion
    if TARGET_STATS_DATABASE_ID:
        print("\nUpdating stats database...")
        update_stats_db(TARGET_STATS_DATABASE_ID, stats)
    else:
        print("\n[INFO] TARGET_STATS_DATABASE_ID is not set.")

    # 8. Save current timestamp
    save_last_run_timestamp()
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    print(f"\nSaved current timestamp: {current_time}")

    # 9. Clean old cache entries
    if cache_manager:
        cache_manager.clear_old_cache(days=30)

    print("="*70)
    print("Keyword Analysis Complete (Optimized with Trigger)")
    print("="*70)
    return True  # Indicate analysis was performed

if __name__ == "__main__":
    run_keyword_analysis()
