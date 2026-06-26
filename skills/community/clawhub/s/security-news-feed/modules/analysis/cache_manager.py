# modules/analysis/cache_manager.py
"""
SQLite-based caching layer for keyword statistics optimization.
Caches Notion API responses to minimize API calls.
"""
import sqlite3
import json
import os
import difflib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# Tracking parameters to remove for URL normalization (모듈 수준 상수)
TRACKING_PARAMS = {
    # Common tracking parameters
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'utm_id', 'utm_name', 'utm_keyword', 'utm_creative', 'utm_matchtype',
    # Social media tracking
    'fbclid', 'gclid', 'msclkid', 'dclid', 'yclid', 'fb_action_ids',
    'fb_action_types', 'fb_ref', 'fb_source',
    # General tracking
    'ref', 'source', 'ref_src', 'ref_url', 'referer', 'origin',
    'campaign', 'medium', 'content', 'term',
    # Analytics
    'ga_source', 'ga_medium', 'ga_campaign', 'ga_term', 'ga_content',
    'mc_cid', 'mc_eid', '_ga', '_gl',
    # Other common trackers
    'aff_id', 'aff_sub', 'click_id', 'clickid', 'clickref',
    'affiliate_id', 'partner_id', 'promo_code',
    # Hash and anchor tracking
    'hash', 'anchor', 'fragment',
    # Timestamp and session
    'timestamp', 'session_id', 'sid', 'sess_id',
    # Platform specific
    'igshid', 'share_id', 'story_id', 'highlight_id',
}

def _remove_tracking_params(query_string: str) -> str:
    """
    URL 쿼리 스트링에서 tracking parameter를 제거합니다.
    """
    if not query_string:
        return ''
    
    try:
        params = parse_qs(query_string, keep_blank_values=True)
        
        # Tracking parameter 제거 (대소문자 무시)
        filtered_params = {
            k: v for k, v in params.items()
            if k.lower() not in TRACKING_PARAMS
        }
        
        # 정렬된 쿼리 스트링 반환 (일관성 확보)
        # 키를 정렬하여 일관된 순서로 인코딩
        sorted_params = sorted(filtered_params.items())
        return urlencode(sorted_params, doseq=True)
    except Exception:
        return query_string

class URLCacheManager:
    """
    Manages local SQLite cache for seen URLs to reduce Notion API calls.
    """
    def __init__(self, db_path: str = "data/url_cache.db"):
        # Resolve absolute path relative to repo root
        # Assuming this file is in modules/analysis/
        # Repo root is ../../
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_path = os.path.join(base_dir, db_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seen_urls (
                    url TEXT PRIMARY KEY,
                    title TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON seen_urls(url)")
            
            # Check if title column exists (for migration)
            cursor.execute("PRAGMA table_info(seen_urls)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'title' not in columns:
                try:
                    cursor.execute("ALTER TABLE seen_urls ADD COLUMN title TEXT")
                    print("[Cache] Added 'title' column to seen_urls table")
                except Exception as e:
                    print(f"[Cache] Error adding title column: {e}")

            conn.commit()

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        URL 정규화 - 중복 감지 향상을 위한 강화된 정규화
        
        1. http → https 변환
        2. www., m., mobile. 접두사 제거 (일관성)
        3. trailing slash 제거
        4. tracking parameter 제거 (utm_*, ref, source 등)
        5. fragment (#) 제거 (페이지 내 위치는 URL 고유성에 영향 없음)
        6. 소문자 도메인 변환
        7. 도메인별 URL 패턴 정규화 (NEW)
        """
        if not url:
            return ""
        try:
            parsed = urlparse(url)
            
            # 1. Enforce HTTPS
            scheme = parsed.scheme
            if scheme == 'http':
                scheme = 'https'
            
            # 2. Normalize netloc (lowercase, remove www/m/mobile)
            netloc = parsed.netloc.lower()
            if netloc.startswith('www.'):
                netloc = netloc[4:]
            elif netloc.startswith('m.'):
                netloc = netloc[2:]
            elif netloc.startswith('mobile.'):
                netloc = netloc[7:]
            
            # 3. Strip trailing slash from path
            path = parsed.path.rstrip('/')
            
            # 4. Remove tracking parameters from query
            clean_query = _remove_tracking_params(parsed.query)
            
            # 🆕 5. Domain-specific normalization
            # BoanNews: idx 파라미터 기반 통일된 URL 사용
            if 'boannews.com' in netloc and 'idx=' in url:
                import re
                idx_match = re.search(r'idx=(\d+)', url)
                if idx_match:
                    # 모든 BoanNews URL을 통일된 형식으로 변환
                    path = f"/article/{idx_match.group(1)}"
                    clean_query = ""
            
            # Reconstruct URL
            return urlunparse((scheme, netloc, path, parsed.params, clean_query, ''))
        except Exception:
            return url
    
    def exists(self, url: str) -> bool:
        normalized = self.normalize_url(url)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM seen_urls WHERE url = ?", (normalized,))
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"[Cache] Error checking URL: {e}")
            return False

    def add(self, url: str, title: str = ""):
        normalized = self.normalize_url(url)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO seen_urls (url, title, added_at) 
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(url) DO UPDATE SET title = excluded.title
                """, (normalized, title))
                conn.commit()
                # print(f"[Cache] Added: {normalized} ({title})")
        except Exception as e:
            print(f"[Cache] Error adding URL: {e}")

    def is_similar_title(self, title: str, threshold: float = 0.85) -> bool:
        """
        Check if a similar title exists in the cache (last 7 days).
        Returns True if a similar title is found.
        """
        if not title:
            return False
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Fetch titles from the last 7 days to optimize
                seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
                cursor.execute("""
                    SELECT title FROM seen_urls 
                    WHERE title IS NOT NULL 
                    AND title != ''
                    AND added_at >= ?
                """, (seven_days_ago,))
                
                cached_titles = [row[0] for row in cursor.fetchall()]
                
                for cached_title in cached_titles:
                    ratio = difflib.SequenceMatcher(None, title, cached_title).ratio()
                    if ratio >= threshold:
                        print(f"[Cache] Similar title found: '{title}' ~= '{cached_title}' (Score: {ratio:.2f})")
                        return True
                        
            return False
        except Exception as e:
            print(f"[Cache] Error checking similar title: {e}")
            return False

    def sync_from_notion(self, database_id: str, notion_token: str, batch_size: int = 100) -> dict:
        """
        Notion DB의 모든 URL을 로컬 캐시에 동기화합니다.
        에이전트 시작 시 호출하여 캐시 히트율을 높입니다.
        
        Args:
            database_id: Notion Database ID
            notion_token: Notion API Token
            batch_size: 한 번에 가져올 항목 수
            
        Returns:
            dict: {'synced': int, 'errors': int, 'total': int}
        """
        import requests
        
        result = {'synced': 0, 'errors': 0, 'total': 0}
        
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2025-09-03"
        }
        
        print(f"[Cache] Notion DB에서 URL 동기화 시작 (DB: {database_id[:20]}...)")
        
        try:
            # data_source_id 획득
            db_url = f"https://api.notion.com/v1/databases/{database_id}"
            db_resp = requests.get(db_url, headers=headers, timeout=30)
            
            if db_resp.status_code != 200:
                print(f"[Cache] DB 조회 실패: {db_resp.status_code}")
                return result
            
            data_sources = db_resp.json().get("data_sources", [])
            if not data_sources:
                print(f"[Cache] data_sources를 찾을 수 없음")
                return result
            
            data_source_id = data_sources[0].get("id")
            
            # data_source에서 properties 조회
            ds_url = f"https://api.notion.com/v1/data_sources/{data_source_id}"
            ds_resp = requests.get(ds_url, headers=headers, timeout=30)
            
            if ds_resp.status_code != 200:
                print(f"[Cache] data_source 조회 실패: {ds_resp.status_code}")
                return result
            
            props = ds_resp.json().get("properties", {})
            
            # URL 속성 찾기
            url_prop_name = None
            for prop_name, prop_info in props.items():
                if prop_info.get("type") == "url":
                    url_prop_name = prop_name
                    break
            
            if not url_prop_name:
                print(f"[Cache] URL 속성을 찾을 수 없음")
                return result
            
            print(f"[Cache] URL 속성 발견: '{url_prop_name}'")
            
            # 모든 페이지 조회 (페이지네이션)
            query_url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
            has_more = True
            start_cursor = None
            
            while has_more:
                query = {
                    "page_size": batch_size,
                    "sorts": [{"timestamp": "created_time", "direction": "descending"}]
                }
                
                if start_cursor:
                    query["start_cursor"] = start_cursor
                
                resp = requests.post(query_url, headers=headers, json=query, timeout=60)
                
                if resp.status_code != 200:
                    print(f"[Cache] Query 실패: {resp.status_code}")
                    result['errors'] += 1
                    break
                
                data = resp.json()
                pages = data.get("results", [])
                
                for page in pages:
                    result['total'] += 1
                    
                    # URL 추출
                    page_props = page.get("properties", {})
                    url_prop = page_props.get(url_prop_name, {})
                    url_value = url_prop.get("url")
                    
                    if url_value:
                        normalized = self.normalize_url(url_value)
                        if normalized:
                            # 캐시에 추가 (중복 무시)
                            try:
                                with sqlite3.connect(self.db_path) as conn:
                                    cursor = conn.cursor()
                                    cursor.execute("""
                                        INSERT OR IGNORE INTO seen_urls (url, title, added_at)
                                        VALUES (?, ?, CURRENT_TIMESTAMP)
                                    """, (normalized, ''))
                                    if cursor.rowcount > 0:
                                        result['synced'] += 1
                            except Exception as e:
                                result['errors'] += 1
                
                # 다음 페이지
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")
                
                if has_more:
                    print(f"[Cache] 동기화 진행 중... (현재: {result['total']}개)")
            
            print(f"[Cache] ✅ 동기화 완료: {result['synced']}개 추가, {result['errors']}개 오류, 총 {result['total']}개 조회")
            
        except Exception as e:
            print(f"[Cache] 동기화 중 오류: {e}")
            result['errors'] += 1
        
        return result

    def get_stats(self) -> dict:
        """
        캐시 통계 반환
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM seen_urls")
                total = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM seen_urls 
                    WHERE added_at >= datetime('now', '-7 days')
                """)
                recent_7d = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM seen_urls 
                    WHERE added_at >= datetime('now', '-30 days')
                """)
                recent_30d = cursor.fetchone()[0]
                
                return {
                    'total_urls': total,
                    'recent_7_days': recent_7d,
                    'recent_30_days': recent_30d
                }
        except Exception as e:
            print(f"[Cache] 통계 조회 오류: {e}")
            return {'total_urls': 0, 'recent_7_days': 0, 'recent_30_days': 0}

class KeywordCacheManager:
    """
    Manages local SQLite cache for keyword analysis data.
    """

    def __init__(self, db_path: str = ".keyword_cache.db"):
        """Initialize cache database."""
        # Use absolute path relative to this file
        cache_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(cache_dir, db_path)
        self._init_db()

    def _init_db(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS titles (
                    page_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keyword_stats (
                    keyword TEXT PRIMARY KEY,
                    count INTEGER NOT NULL,
                    page_ids TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS page_children (
                    page_id TEXT NOT NULL,
                    child_block_id TEXT NOT NULL,
                    page_link_id TEXT,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (page_id, child_block_id)
                )
            """)

            # 성능 최적화: 인덱스 추가
            # fetched_at 인덱스 (날짜 기반 쿼리 최적화)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_titles_fetched_at
                ON titles(fetched_at DESC)
            """)

            # count 인덱스 (정렬 최적화)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_keyword_stats_count
                ON keyword_stats(count DESC)
            """)

            # page_id 인덱스 (페이지 자식 조회 최적화)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_page_children_page_id
                ON page_children(page_id, fetched_at ASC)
            """)

            # page_link_id 인덱스 (역참조 최적화)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_page_children_link_id
                ON page_children(page_link_id)
            """)

            # VACUUM 및 ANALYZE로 쿼리 최적화
            cursor.execute("ANALYZE")

            conn.commit()

    def get_cached_titles(self, since: Optional[datetime] = None) -> Optional[List[Dict[str, str]]]:
        """
        Get cached titles since specified date.
        Returns None if no cache exists for the period.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if since:
                    cursor.execute("""
                        SELECT page_id, title, fetched_at
                        FROM titles
                        WHERE fetched_at >= ?
                        ORDER BY fetched_at DESC
                    """, (since.isoformat(),))
                else:
                    cursor.execute("""
                        SELECT page_id, title, fetched_at
                        FROM titles
                        ORDER BY fetched_at DESC
                    """)

                rows = cursor.fetchall()
                if not rows:
                    return None

                return [
                    {
                        "id": row[0],
                        "title": row[1],
                        "fetched_at": row[2]
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"[Cache] Error reading cached titles: {e}")
            return None

    def cache_titles(self, titles_data: List[Dict[str, str]]):
        """Update cache with new titles (upsert)."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for item in titles_data:
                    page_id = item.get("id")
                    title = item.get("title")

                    if page_id and title:
                        cursor.execute("""
                            INSERT OR REPLACE INTO titles (page_id, title, fetched_at)
                            VALUES (?, ?, CURRENT_TIMESTAMP)
                        """, (page_id, title))

                conn.commit()
                print(f"[Cache] Cached {len(titles_data)} titles")
        except Exception as e:
            print(f"[Cache] Error caching titles: {e}")

    def get_cached_keyword_stats(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Get all cached keyword statistics.
        Returns None if cache is empty.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT keyword, count, page_ids
                    FROM keyword_stats
                    ORDER BY count DESC
                """)

                rows = cursor.fetchall()
                if not rows:
                    return None

                stats = {}
                for row in rows:
                    keyword = row[0]
                    count = row[1]
                    page_ids = json.loads(row[2]) if row[2] else []

                    stats[keyword] = {
                        'count': count,
                        'pages': page_ids
                    }

                return stats
        except Exception as e:
            print(f"[Cache] Error reading keyword stats: {e}")
            return None

    def cache_keyword_stats(self, stats: Dict[str, Dict[str, Any]]):
        """Update cache with new keyword statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                for keyword, data in stats.items():
                    count = data.get('count', 0)
                    page_ids = data.get('pages', [])

                    cursor.execute("""
                        INSERT OR REPLACE INTO keyword_stats (keyword, count, page_ids, updated_at)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                    """, (keyword, count, json.dumps(page_ids)))

                conn.commit()
                print(f"[Cache] Cached {len(stats)} keyword statistics")
        except Exception as e:
            print(f"[Cache] Error caching keyword stats: {e}")

    def get_cached_page_children(self, page_id: str) -> Optional[List[Dict[str, str]]]:
        """
        Get cached children blocks for a page.
        Returns None if no cache exists.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT child_block_id, page_link_id, fetched_at
                    FROM page_children
                    WHERE page_id = ?
                    ORDER BY fetched_at ASC
                """, (page_id,))

                rows = cursor.fetchall()
                if not rows:
                    return None

                return [
                    {
                        "block_id": row[0],
                        "page_link_id": row[1],
                        "fetched_at": row[2]
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"[Cache] Error reading page children: {e}")
            return None

    def cache_page_children(self, page_id: str, children_data: List[Dict[str, str]]):
        """Update cache with page children blocks."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Clear old cache for this page
                cursor.execute("""
                    DELETE FROM page_children WHERE page_id = ?
                """, (page_id,))

                # Insert new data
                for child in children_data:
                    child_block_id = child.get("block_id")
                    page_link_id = child.get("page_link_id")

                    if child_block_id:
                        cursor.execute("""
                            INSERT INTO page_children (page_id, child_block_id, page_link_id, fetched_at)
                            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                        """, (page_id, child_block_id, page_link_id))

                conn.commit()
                print(f"[Cache] Cached {len(children_data)} children for page {page_id}")
        except Exception as e:
            print(f"[Cache] Error caching page children: {e}")

    def clear_old_cache(self, days: int = 30):
        """Remove cache entries older than specified days."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

                # Clear old titles
                cursor.execute("""
                    DELETE FROM titles WHERE fetched_at < ?
                """, (cutoff_date,))

                # Clear old page children
                cursor.execute("""
                    DELETE FROM page_children WHERE fetched_at < ?
                """, (cutoff_date,))

                # Clear old keyword stats (optional - keep stats longer)
                stats_cutoff = (datetime.now() - timedelta(days=days*2)).isoformat()
                cursor.execute("""
                    DELETE FROM keyword_stats WHERE updated_at < ?
                """, (stats_cutoff,))

                conn.commit()
                print(f"[Cache] Cleared cache entries older than {days} days")
        except Exception as e:
            print(f"[Cache] Error clearing old cache: {e}")

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about cache size."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                stats = {}

                cursor.execute("SELECT COUNT(*) FROM titles")
                stats['titles_count'] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM keyword_stats")
                stats['keywords_count'] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM page_children")
                stats['page_children_count'] = cursor.fetchone()[0]

                return stats
        except Exception as e:
            print(f"[Cache] Error getting cache stats: {e}")
            return {}
