#!/usr/bin/env python3
"""
数据缓存层 - VC投资筛选API调用缓存

设计原则：
1. 查询结果带TTL过期，避免用旧数据
2. 按数据源+接口+参数生成缓存key，精确匹配
3. 不同数据类型设置不同TTL（工商数据变化慢→长TTL，舆情→短TTL）
4. 命中缓存时跳过API调用，节省费用
5. 使用SQLite存储，支持百万级查询零压力

存储位置: ~/.openclaw/workspace/memory/vc-cache.db
"""

import os
import sys
import json
import sqlite3
import hashlib
import time
import threading

DB_PATH = os.path.expanduser("~/.openclaw/workspace/memory/vc-cache.db")

# 不同数据类型的缓存TTL（秒）
TTL_CONFIG = {
    # 天眼查 - 企业工商数据变化慢，缓存时间长
    "tianyancha:detail":           30 * 24 * 3600,   # 30天
    "tianyancha:team":             14 * 24 * 3600,   # 14天
    "tianyancha:shareholders":     14 * 24 * 3600,   # 14天
    "tianyancha:ip":               7 * 24 * 3600,    # 7天
    "tianyancha:financial_risk":   7 * 24 * 3600,    # 7天
    "tianyancha:judicial_risk":    3 * 24 * 3600,    # 3天（诉讼变化较快）
    "tianyancha:investment":       14 * 24 * 3600,   # 14天
    "tianyancha:changes":          7 * 24 * 3600,    # 7天
    "tianyancha:search":           1 * 24 * 3600,    # 1天
    "tianyancha:profile":          7 * 24 * 3600,    # 7天（聚合查询）

    # 人民数据 - 政策和舆情需要更频繁更新
    "people_data:policy":          1 * 24 * 3600,    # 1天
    "people_data:sentiment":       6 * 3600,         # 6小时
    "people_data:credit":          14 * 24 * 3600,   # 14天
    "people_data:industry":        3 * 24 * 3600,    # 3天

    # 默认
    "default":                     1 * 24 * 3600,    # 1天
}

_lock = threading.Lock()

def _get_db():
    """获取数据库连接"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _init_db():
    """初始化数据库表"""
    with _lock:
        conn = _get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_cache (
                cache_key TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                api_type TEXT NOT NULL,
                params TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                hit_count INTEGER DEFAULT 0,
                last_hit REAL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_expires 
            ON api_cache(expires_at)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_source 
            ON api_cache(source, api_type)
        """)
        conn.commit()
        conn.close()

def _make_cache_key(source, api_type, params):
    """生成缓存key"""
    raw = f"{source}:{api_type}:{json.dumps(params, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def get(source, api_type, params):
    """
    查询缓存
    
    Returns:
        dict/None: 命中返回缓存的响应数据，未命中返回None
    """
    _init_db()
    cache_key = _make_cache_key(source, api_type, params)
    now = time.time()
    
    with _lock:
        conn = _get_db()
        row = conn.execute(
            "SELECT response, expires_at, hit_count FROM api_cache WHERE cache_key = ?",
            (cache_key,)
        ).fetchone()
        
        if row and row["expires_at"] > now:
            # 命中缓存，更新命中计数
            conn.execute(
                "UPDATE api_cache SET hit_count = ?, last_hit = ? WHERE cache_key = ?",
                (row["hit_count"] + 1, now, cache_key)
            )
            conn.commit()
            conn.close()
            return json.loads(row["response"])
        
        conn.close()
    return None

def set(source, api_type, params, response):
    """
    写入缓存
    
    Args:
        source: 数据源（tianyancha / people_data）
        api_type: 接口类型（detail / search / policy 等）
        params: 请求参数 dict
        response: 响应数据 dict
    """
    _init_db()
    cache_key = _make_cache_key(source, api_type, params)
    now = time.time()
    ttl_key = f"{source}:{api_type}"
    ttl = TTL_CONFIG.get(ttl_key, TTL_CONFIG["default"])
    
    with _lock:
        conn = _get_db()
        conn.execute("""
            INSERT OR REPLACE INTO api_cache 
            (cache_key, source, api_type, params, response, created_at, expires_at, hit_count, last_hit)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
        """, (
            cache_key, source, api_type,
            json.dumps(params, sort_keys=True, ensure_ascii=False),
            json.dumps(response, ensure_ascii=False),
            now, now + ttl
        ))
        conn.commit()
        conn.close()

def cached(source, api_type, params, fetch_fn):
    """
    带缓存的API调用：先查缓存，未命中则调用fetch_fn并缓存结果
    
    Args:
        source: 数据源名称
        api_type: 接口类型
        params: 请求参数
        fetch_fn: 无参数函数，返回API响应数据
    
    Returns:
        dict: API响应数据
    """
    # 先查缓存
    cached_data = get(source, api_type, params)
    if cached_data is not None:
        # 给响应加标记
        if isinstance(cached_data, dict):
            cached_data["_from_cache"] = True
        return cached_data
    
    # 缓存未命中，调用API
    fresh_data = fetch_fn()
    if fresh_data is not None:
        set(source, api_type, params, fresh_data)
        if isinstance(fresh_data, dict):
            fresh_data["_from_cache"] = False
    return fresh_data

def stats():
    """
    缓存统计信息
    
    Returns:
        dict: 缓存命中率、总条目数、各数据源统计等
    """
    _init_db()
    now = time.time()
    
    with _lock:
        conn = _get_db()
        
        total = conn.execute("SELECT COUNT(*) FROM api_cache").fetchone()[0]
        valid = conn.execute(
            "SELECT COUNT(*) FROM api_cache WHERE expires_at > ?", (now,)
        ).fetchone()[0]
        expired = total - valid
        total_hits = conn.execute(
            "SELECT COALESCE(SUM(hit_count), 0) FROM api_cache"
        ).fetchone()[0]
        
        by_source = conn.execute("""
            SELECT source, api_type, COUNT(*) as cnt, 
                   COALESCE(SUM(hit_count), 0) as hits,
                   COALESCE(SUM(CASE WHEN expires_at > ? THEN 1 ELSE 0 END), 0) as valid_cnt
            FROM api_cache 
            GROUP BY source, api_type
            ORDER BY hits DESC
        """, (now,)).fetchall()
        
        conn.close()
    
    return {
        "total_entries": total,
        "valid_entries": valid,
        "expired_entries": expired,
        "total_hits": total_hits,
        "hit_rate": f"{total_hits / max(total, 1) * 100:.1f}%" if total > 0 else "N/A",
        "by_source": [
            {
                "source": row["source"],
                "api_type": row["api_type"],
                "count": row["cnt"],
                "hits": row["hits"],
                "valid": row["valid_cnt"],
            }
            for row in by_source
        ],
        "db_size": f"{os.path.getsize(DB_PATH) / 1024:.1f} KB" if os.path.exists(DB_PATH) else "0 KB",
    }

def cleanup():
    """
    清理过期缓存
    """
    _init_db()
    now = time.time()
    
    with _lock:
        conn = _get_db()
        cursor = conn.execute(
            "DELETE FROM api_cache WHERE expires_at <= ?", (now,)
        )
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        conn2 = _get_db()
        conn2.execute("VACUUM")
        conn2.close()
    
    return {"deleted": deleted}

def clear_source(source=None):
    """
    清除指定数据源的所有缓存（用于强制刷新）
    
    Args:
        source: 数据源名称，None则清除全部
    """
    _init_db()
    
    with _lock:
        conn = _get_db()
        if source:
            cursor = conn.execute("DELETE FROM api_cache WHERE source = ?", (source,))
        else:
            cursor = conn.execute("DELETE FROM api_cache")
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        # VACUUM需要在事务外执行
        conn2 = _get_db()
        conn2.execute("VACUUM")
        conn2.close()
    
    return {"deleted": deleted}


# === CLI入口 ===

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("VC投资筛选 - 数据缓存管理")
        print("")
        print("用法:")
        print("  python3 scripts/cache.py stats          查看缓存统计")
        print("  python3 scripts/cache.py cleanup        清理过期缓存")
        print("  python3 scripts/cache.py clear          清除全部缓存")
        print("  python3 scripts/cache.py clear <source> 清除指定数据源缓存")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "stats":
        result = stats()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "cleanup":
        result = cleanup()
        print(f"已清理 {result['deleted']} 条过期缓存")
    elif cmd == "clear":
        source = sys.argv[2] if len(sys.argv) >= 3 else None
        result = clear_source(source)
        label = source or "全部"
        print(f"已清除 {label} 的 {result['deleted']} 条缓存")
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
