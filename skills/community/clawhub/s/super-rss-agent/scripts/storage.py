"""
RSS Agent 存储层 - 博客与文章的 SQLite 数据库。
"""

import os
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(_SKILL_ROOT, "super_rss_agent.db")

_SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
PRAGMA busy_timeout=5000;

CREATE TABLE IF NOT EXISTS blogs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    url             TEXT NOT NULL,
    feed_url        TEXT NOT NULL UNIQUE,
    category        TEXT NOT NULL DEFAULT 'Uncategorized',
    scrape_selector TEXT,
    last_scanned    DATETIME
);

CREATE TABLE IF NOT EXISTS articles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id         INTEGER NOT NULL,
    title           TEXT NOT NULL,
    url             TEXT NOT NULL UNIQUE,
    summary         TEXT,
    content         TEXT,
    published_date  DATETIME,
    discovered_date DATETIME NOT NULL,
    is_read         INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (blog_id) REFERENCES blogs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_articles_blog_id ON articles(blog_id);
CREATE INDEX IF NOT EXISTS idx_articles_is_read ON articles(is_read);
CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_date);
CREATE INDEX IF NOT EXISTS idx_blogs_category ON blogs(category);

CREATE TABLE IF NOT EXISTS config (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

# 配置默认值（未写入数据库的 key 使用这些默认值）
_CONFIG_DEFAULTS = {
    'auto_purge': 'true',
    'auto_purge_days': '90',
}


class Storage:
    """基于 SQLite 的博客与文章存储。"""

    def __init__(self, db_path: str = DB_PATH):
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _ensure_schema(self):
        self._conn.executescript(_SCHEMA_SQL)

    # ------------------------------------------------------------------
    # 博客 CRUD
    # ------------------------------------------------------------------

    def add_blog(self, name: str, url: str, feed_url: str,
                 category: str = "Uncategorized",
                 scrape_selector: Optional[str] = None) -> int:
        """插入新博客，返回新博客 id。"""
        cur = self._conn.execute(
            "INSERT INTO blogs (name, url, feed_url, category, scrape_selector) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, url, feed_url, category, scrape_selector)
        )
        self._conn.commit()
        return cur.lastrowid

    def remove_blog(self, identifier: str) -> List[Dict]:
        """按名称或 feed_url 删除匹配的博客，返回已删除的博客列表。"""
        blogs = self._conn.execute(
            "SELECT * FROM blogs WHERE name = ? OR feed_url = ?",
            (identifier, identifier)
        ).fetchall()

        removed = [dict(b) for b in blogs]
        for b in blogs:
            self._conn.execute("DELETE FROM blogs WHERE id = ?", (b['id'],))
        self._conn.commit()
        return removed

    def get_blog(self, identifier: str) -> Optional[Dict]:
        """按名称、feed_url 或字符串 id 获取单个博客。"""
        row = self._conn.execute(
            "SELECT * FROM blogs WHERE name = ? OR feed_url = ?",
            (identifier, identifier)
        ).fetchone()

        if row is None:
            try:
                blog_id = int(identifier)
                row = self._conn.execute(
                    "SELECT * FROM blogs WHERE id = ?", (blog_id,)
                ).fetchone()
            except (ValueError, TypeError):
                pass

        return dict(row) if row else None

    def get_blog_by_id(self, blog_id: int) -> Optional[Dict]:
        row = self._conn.execute(
            "SELECT * FROM blogs WHERE id = ?", (blog_id,)
        ).fetchone()
        return dict(row) if row else None

    def list_blogs(self, category: Optional[str] = None) -> List[Dict]:
        if category:
            rows = self._conn.execute(
                "SELECT * FROM blogs WHERE category = ? ORDER BY name",
                (category,)
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM blogs ORDER BY name"
            ).fetchall()
        return [dict(r) for r in rows]

    def update_blog_last_scanned(self, blog_id: int, scanned_at: datetime):
        self._conn.execute(
            "UPDATE blogs SET last_scanned = ? WHERE id = ?",
            (scanned_at.isoformat(), blog_id)
        )
        self._conn.commit()

    def update_blog(self, blog_id: int, **fields):
        """更新博客的任意字段。"""
        if not fields:
            return
        allowed = {'name', 'url', 'feed_url', 'category', 'scrape_selector'}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [blog_id]
        self._conn.execute(
            f"UPDATE blogs SET {set_clause} WHERE id = ?", values
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # 文章 CRUD
    # ------------------------------------------------------------------

    def insert_articles(self, blog_id: int, articles: List[Dict]) -> int:
        """批量插入文章，通过 INSERT OR IGNORE 跳过重复项。
        每个 dict: {title, url, summary?, content?, published_date?}。
        返回新插入的文章数量。"""
        if not articles:
            return 0

        now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        inserted = 0

        with self._conn:
            for art in articles:
                pub_date = art.get('published_date')
                if isinstance(pub_date, datetime):
                    pub_date = pub_date.isoformat()

                try:
                    self._conn.execute(
                        "INSERT OR IGNORE INTO articles "
                        "(blog_id, title, url, summary, content, published_date, discovered_date) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (
                            blog_id,
                            art.get('title', 'No Title'),
                            art['url'],
                            art.get('summary'),
                            art.get('content'),
                            pub_date,
                            now,
                        )
                    )
                    if self._conn.execute("SELECT changes()").fetchone()[0] > 0:
                        inserted += 1
                except sqlite3.Error:
                    continue

        return inserted

    def list_articles(self, blog_id: Optional[int] = None,
                      category: Optional[str] = None,
                      include_read: bool = False,
                      limit: Optional[int] = None,
                      offset: Optional[int] = None,
                      since: Optional[str] = None) -> List[Dict]:
        """列出文章，支持可选过滤条件。
        since: ISO 日期时间字符串 — 仅返回在此之后发现/发布的文章。"""
        query = """
            SELECT a.*, b.name as blog_name, b.category as blog_category
            FROM articles a
            JOIN blogs b ON a.blog_id = b.id
        """
        conditions = []
        params = []

        if not include_read:
            conditions.append("a.is_read = 0")
        if blog_id is not None:
            conditions.append("a.blog_id = ?")
            params.append(blog_id)
        if category:
            conditions.append("b.category = ?")
            params.append(category)
        if since:
            conditions.append(
                "(COALESCE(a.published_date, a.discovered_date) >= ?)")
            params.append(since)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY a.discovered_date DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)
        if offset:
            query += " OFFSET ?"
            params.append(offset)

        rows = self._conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_article(self, article_id: int) -> Optional[Dict]:
        row = self._conn.execute(
            """SELECT a.*, b.name as blog_name, b.category as blog_category
               FROM articles a JOIN blogs b ON a.blog_id = b.id
               WHERE a.id = ?""",
            (article_id,)
        ).fetchone()
        return dict(row) if row else None

    def mark_read(self, article_id: int) -> bool:
        self._conn.execute(
            "UPDATE articles SET is_read = 1 WHERE id = ?", (article_id,)
        )
        changed = self._conn.execute("SELECT changes()").fetchone()[0] > 0
        self._conn.commit()
        return changed

    def mark_unread(self, article_id: int) -> bool:
        self._conn.execute(
            "UPDATE articles SET is_read = 0 WHERE id = ?", (article_id,)
        )
        changed = self._conn.execute("SELECT changes()").fetchone()[0] > 0
        self._conn.commit()
        return changed

    def mark_all_read(self, blog_id: Optional[int] = None,
                      category: Optional[str] = None) -> int:
        """将所有匹配的未读文章标记为已读，返回受影响的数量。"""
        if category and not blog_id:
            self._conn.execute(
                """UPDATE articles SET is_read = 1
                   WHERE is_read = 0 AND blog_id IN
                   (SELECT id FROM blogs WHERE category = ?)""",
                (category,)
            )
        elif blog_id:
            self._conn.execute(
                "UPDATE articles SET is_read = 1 WHERE is_read = 0 AND blog_id = ?",
                (blog_id,)
            )
        else:
            self._conn.execute(
                "UPDATE articles SET is_read = 1 WHERE is_read = 0"
            )

        count = self._conn.execute("SELECT changes()").fetchone()[0]
        self._conn.commit()
        return count

    def search_articles(self, keyword: str,
                        blog_id: Optional[int] = None,
                        category: Optional[str] = None,
                        include_read: bool = False,
                        limit: int = 50) -> List[Dict]:
        """按关键词搜索文章标题和摘要。"""
        query = """
            SELECT a.*, b.name as blog_name, b.category as blog_category
            FROM articles a
            JOIN blogs b ON a.blog_id = b.id
        """
        # 转义 LIKE 通配符，防止用户输入中的 % 和 _ 被当作通配符
        escaped = keyword.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
        like_pattern = f"%{escaped}%"
        conditions = ["(a.title LIKE ? ESCAPE '\\' OR a.summary LIKE ? ESCAPE '\\')"]
        params = [like_pattern, like_pattern]

        if not include_read:
            conditions.append("a.is_read = 0")
        if blog_id is not None:
            conditions.append("a.blog_id = ?")
            params.append(blog_id)
        if category:
            conditions.append("b.category = ?")
            params.append(category)

        query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY a.discovered_date DESC"
        query += " LIMIT ?"
        params.append(limit)

        rows = self._conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def count_articles(self, blog_id: Optional[int] = None,
                       category: Optional[str] = None,
                       include_read: bool = False) -> int:
        """统计匹配条件的文章总数。"""
        query = """
            SELECT COUNT(*) FROM articles a
            JOIN blogs b ON a.blog_id = b.id
        """
        conditions = []
        params = []

        if not include_read:
            conditions.append("a.is_read = 0")
        if blog_id is not None:
            conditions.append("a.blog_id = ?")
            params.append(blog_id)
        if category:
            conditions.append("b.category = ?")
            params.append(category)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return self._conn.execute(query, params).fetchone()[0]

    def purge_articles(self, days: int = 90,
                       blog_id: Optional[int] = None,
                       only_read: bool = True) -> int:
        """清理旧文章，返回删除条数。
        days: 清理多少天以前的文章。
        only_read: 为 True 时只清理已读文章。"""
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - \
            timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        query = "DELETE FROM articles WHERE COALESCE(published_date, discovered_date) < ?"
        params = [cutoff_str]

        if only_read:
            query += " AND is_read = 1"
        if blog_id is not None:
            query += " AND blog_id = ?"
            params.append(blog_id)

        self._conn.execute(query, params)
        count = self._conn.execute("SELECT changes()").fetchone()[0]
        self._conn.commit()
        return count

    def count_purge_candidates(self, days: int = 90,
                               blog_id: Optional[int] = None,
                               only_read: bool = True) -> int:
        """统计将要被清理的文章数量（预览用）。"""
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - \
            timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        query = """SELECT COUNT(*) FROM articles
                   WHERE COALESCE(published_date, discovered_date) < ?"""
        params = [cutoff_str]

        if only_read:
            query += " AND is_read = 1"
        if blog_id is not None:
            query += " AND blog_id = ?"
            params.append(blog_id)

        return self._conn.execute(query, params).fetchone()[0]

    def get_existing_article_urls(self, urls: List[str]) -> set:
        """返回数据库中已存在的文章 URL 集合。"""
        if not urls:
            return set()

        existing = set()
        # SQLite 参数上限约 999，按 900 分块
        for i in range(0, len(urls), 900):
            chunk = urls[i:i + 900]
            placeholders = ",".join("?" * len(chunk))
            rows = self._conn.execute(
                f"SELECT url FROM articles WHERE url IN ({placeholders})",
                chunk
            ).fetchall()
            existing.update(r['url'] for r in rows)

        return existing

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    def blog_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM blogs").fetchone()[0]

    def unread_count(self, blog_id: Optional[int] = None) -> int:
        if blog_id:
            return self._conn.execute(
                "SELECT COUNT(*) FROM articles WHERE is_read = 0 AND blog_id = ?",
                (blog_id,)
            ).fetchone()[0]
        return self._conn.execute(
            "SELECT COUNT(*) FROM articles WHERE is_read = 0"
        ).fetchone()[0]

    def get_stats(self) -> List[Dict]:
        """获取每个博客的统计信息：总文章数、未读数、最新文章日期。"""
        rows = self._conn.execute("""
            SELECT
                b.id, b.name, b.category, b.last_scanned,
                COUNT(a.id) as total_articles,
                SUM(CASE WHEN a.is_read = 0 THEN 1 ELSE 0 END) as unread_count,
                MAX(COALESCE(a.published_date, a.discovered_date)) as latest_article
            FROM blogs b
            LEFT JOIN articles a ON a.blog_id = b.id
            GROUP BY b.id
            ORDER BY b.category, b.name
        """).fetchall()
        return [dict(r) for r in rows]

    def db_size_bytes(self) -> int:
        """获取数据库文件大小（字节）。"""
        try:
            page_count = self._conn.execute("PRAGMA page_count").fetchone()[0]
            page_size = self._conn.execute("PRAGMA page_size").fetchone()[0]
            return page_count * page_size
        except Exception:
            return 0

    # ------------------------------------------------------------------
    # 配置
    # ------------------------------------------------------------------

    def get_config(self, key: str) -> str:
        """获取配置值，不存在则返回默认值。"""
        row = self._conn.execute(
            "SELECT value FROM config WHERE key = ?", (key,)
        ).fetchone()
        if row:
            return row['value']
        return _CONFIG_DEFAULTS.get(key, '')

    def set_config(self, key: str, value: str):
        """设置配置值（INSERT OR REPLACE）。"""
        self._conn.execute(
            "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
            (key, value)
        )
        self._conn.commit()

    def delete_config(self, key: str) -> bool:
        """删除配置值（恢复为默认值），返回是否有删除。"""
        self._conn.execute("DELETE FROM config WHERE key = ?", (key,))
        deleted = self._conn.execute("SELECT changes()").fetchone()[0] > 0
        self._conn.commit()
        return deleted

    def list_config(self) -> Dict[str, str]:
        """列出所有配置（合并默认值和数据库值）。"""
        result = dict(_CONFIG_DEFAULTS)
        rows = self._conn.execute("SELECT key, value FROM config").fetchall()
        for r in rows:
            result[r['key']] = r['value']
        return result

    def categories(self) -> List[str]:
        rows = self._conn.execute(
            "SELECT DISTINCT category FROM blogs ORDER BY category"
        ).fetchall()
        return [r['category'] for r in rows]

