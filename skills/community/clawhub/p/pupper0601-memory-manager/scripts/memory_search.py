#!/usr/bin/env python3
"""
memory_search.py - 基于向量相似度的语义记忆搜索

用法:
  python scripts/memory_search.py --uid pupper "我上周做了什么关于memory的事"
  python scripts/memory_search.py --uid pupper "团队进展" --scope shared
  python scripts/memory_search.py --uid pupper "技术" --level L2 L3
  python scripts/memory_search.py --uid pupper "记忆" --top-k 5
  python scripts/memory_search.py --uid pupper "memory" --keyword-only
  python scripts/memory_search.py --uid pupper --stats
  python scripts/memory_search.py --uid pupper --rebuild-index  # 重建 LanceDB 索引
  python scripts/memory_search.py --list-backends

依赖:
  pip install openai numpy lancedb  # lancedb 可选，增强搜索性能

优化特性:
  - LanceDB HNSW 索引（需安装 lancedb）
  - 查询缓存（避免重复搜索）
  - 自动回退（无 LanceDB 时使用 SQLite）
"""

import os
import sys
import sqlite3
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union, Any, Tuple

try:
    import numpy as np
except ImportError:
    np = None

# 确保同目录模块可导入（跨平台兼容）
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).parent))

from embed_backends import get_embedding, get_backend_info

# LanceDB 懒加载
try:
    from lancedb_integration import LanceDBManager, SearchCache, smart_search
    LANCEDB_AVAILABLE = True
except ImportError:
    LANCEDB_AVAILABLE = False
    LanceDBManager = None
    SearchCache = None
    smart_search = None

DB_NAME = ".memory_vectors.db"


def get_db_path(base_dir):
    return os.path.join(os.path.abspath(base_dir), DB_NAME)


def connect_db(db_path):
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """计算余弦相似度（两个向量已归一化）"""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def search_vectors_lancedb(query_emb, uid, scope, levels, top_k, db_path):
    """
    LanceDB HNSW 向量搜索
    
    优点：
    - O(log n) 复杂度 vs O(n) SQLite 扫描
    - 100x 速度提升（10k+ 向量时）
    """
    if not LANCEDB_AVAILABLE:
        return None
    
    manager = LanceDBManager(db_path)
    if not manager.connect():
        return None
    
    # 转换 numpy array 到 list
    query_vec = query_emb.tolist() if hasattr(query_emb, 'tolist') else list(query_emb)
    
    results = manager.search(
        query_vec, 
        top_k * 2,  # 多取一些，后面过滤
        uid=uid, 
        scope=scope if scope != "all" else None,
        level=levels[0] if levels and len(levels) == 1 else None
    )
    
    manager.close()
    
    if not results:
        return None
    
    return results[:top_k]


def search_vectors(conn, query_emb, uid, scope, levels, top_k, min_score, semantic_weight=0.6):
    """向量语义搜索（SQLite 全表扫描）"""
    c = conn.cursor()
    conditions = []
    params = []
    if uid != "*":
        conditions.append("uid = ?")
        params.append(uid)
    if scope != "*":
        conditions.append("scope = ?")
        params.append(scope)
    if levels:
        ph = ",".join("?" * len(levels))
        conditions.append(f"level IN ({ph})")
        params.extend(levels)
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    c.execute(f"SELECT * FROM memory_embeddings {where_clause}", params)
    cols = [
        "id", "chunk_id", "uid", "scope", "level", "filepath",
        "section_idx", "title", "semantic_key", "content",
        "raw_content", "embedding", "content_hash", "mtime", "created_at",
        "importance_score", "related_ids"
    ]

    scored = []
    for row in c.fetchall():
        emb_bytes = row[cols.index("embedding")]
        emb = np.frombuffer(emb_bytes, dtype=np.float32)
        sim_score = cosine_similarity(query_emb, emb)
        if sim_score >= min_score:
            # 综合评分 = 语义相似度 × semantic_weight + 重要性 × (1-semantic_weight)
            imp_idx = cols.index("importance_score")
            importance = float(row[imp_idx]) if row[imp_idx] is not None else 50.0
            combined = sim_score * semantic_weight + (importance / 100.0) * (1 - semantic_weight)
            scored.append((combined, sim_score, importance, row))

    scored.sort(key=lambda x: -x[0])
    # 返回: (combined_score, sim_score, importance, row)
    return [(s[0], s[1], s[2], s[3]) for s in scored[:top_k]], cols


def keyword_search(conn, query, uid, scope, levels, top_k, semantic_weight=0.6):
    """纯关键词搜索（无 API 依赖）"""
    c = conn.cursor()
    conditions = []
    params = []
    if uid != "*":
        conditions.append("uid = ?")
        params.append(uid)
    if scope != "*":
        conditions.append("scope = ?")
        params.append(scope)
    if levels:
        ph = ",".join("?" * len(levels))
        conditions.append(f"level IN ({ph})")
        params.extend(levels)
    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    c.execute(f"SELECT * FROM memory_embeddings {where_clause}", params)
    cols = [
        "id", "chunk_id", "uid", "scope", "level", "filepath",
        "section_idx", "title", "semantic_key", "content",
        "raw_content", "embedding", "content_hash", "mtime", "created_at",
        "importance_score", "related_ids"
    ]

    keywords = query.lower().split()
    scored = []
    for row in c.fetchall():
        text = (row[cols.index("title")] + " " + row[cols.index("content")]).lower()
        sim_score = sum(1 for kw in keywords if kw in text) / len(keywords)
        if sim_score > 0:
            imp_idx = cols.index("importance_score")
            importance = float(row[imp_idx]) if row[imp_idx] is not None else 50.0
            combined = sim_score * semantic_weight + (importance / 100.0) * (1 - semantic_weight)
            scored.append((combined, sim_score, importance, row))

    scored.sort(key=lambda x: -x[0])
    return [(s[0], s[1], s[2], s[3]) for s in scored[:top_k]], cols


def format_row(combined, sim_score, importance, row, cols):
    idx = {col: i for i, col in enumerate(cols)}
    uid = row[idx["uid"]]
    level = row[idx["level"]]
    filepath = row[idx["filepath"]]
    title = row[idx["title"]]
    sk = row[idx["semantic_key"]]
    content = row[idx["content"]]
    mtime = datetime.fromtimestamp(row[idx["mtime"]]).strftime("%Y-%m-%d")
    owner = f"@{uid}" if uid != "shared" else "shared"

    # 重要性显示
    imp_bar = "█" * int(importance / 10) + "░" * (10 - int(importance / 10))

    # 关联记忆
    related_ids_raw = row[idx.get("related_ids", -1)]
    related_info = ""
    if related_ids_raw and related_ids_raw != "[]":
        try:
            import json as _json
            rids = _json.loads(related_ids_raw)
            if rids:
                related_info = f"\n   🔗 关联 {len(rids)} 条记忆: {', '.join(rids[:3])}"
                if len(rids) > 3:
                    related_info += f" (+{len(rids)-3} more)"
        except Exception:
            pass

    snippet = content[:150].replace("\n", " ").strip()
    if len(content) > 150:
        snippet += "..."

    star = "⭐⭐⭐" if sim_score >= 0.85 else ("⭐⭐" if sim_score >= 0.75 else ("⭐" if sim_score >= 0.65 else "  "))

    lines = [
        f"{star} [{combined:.2f}] {owner}/{level} — {title}  [{imp_bar}]",
        f"   📍 {filepath} | {mtime} | 重要性: {importance:.0f}",
        f"   🔑 {sk}",
        f"   💬 {snippet}{related_info}",
        "",
    ]
    return "\n".join(lines)


def format_raw_row(combined, row, cols):
    idx = {col: i for i, col in enumerate(cols)}
    return f"\n{'='*60}\n{row[idx['raw_content']]}\n{'='*60}\n"


def print_stats(conn, db_path=None):
    c = conn.cursor()
    print("\n📊 向量库统计")
    print("─" * 40)
    try:
        info = get_backend_info(db_path=db_path)
        print(f"  后端: {info['name']} ({info['dim']}维)")
    except Exception:
        pass
    c.execute("SELECT COUNT(*) FROM memory_embeddings")
    total = c.fetchone()[0]
    print(f"  总向量数: {total}")
    c.execute("SELECT uid, COUNT(*) FROM memory_embeddings GROUP BY uid ORDER BY COUNT(*) DESC")
    for uid, cnt in c.fetchall():
        print(f"    {uid}: {cnt} 条")
    c.execute("SELECT level, COUNT(*) FROM memory_embeddings GROUP BY level ORDER BY level")
    for level, cnt in c.fetchall():
        print(f"  {level}: {cnt} 条")

    # 关联记忆统计
    try:
        c.execute("SELECT COUNT(*) FROM memory_embeddings WHERE related_ids != '[]' AND related_ids IS NOT NULL")
        related_cnt = c.fetchone()[0]
        print(f"\n  🔗 有关联记忆: {related_cnt} 条")
    except Exception:
        pass

    # 平均重要性
    try:
        c.execute("SELECT AVG(importance_score) FROM memory_embeddings WHERE importance_score IS NOT NULL")
        avg_imp = c.fetchone()[0]
        if avg_imp:
            print(f"  📊 平均重要性: {avg_imp:.1f}")
    except Exception:
        pass
    c.execute("SELECT created_at FROM memory_embeddings ORDER BY created_at DESC LIMIT 1")
    row = c.fetchone()
    if row:
        print(f"\n  最新生成: {row[0][:16]}")


def main():
    parser = argparse.ArgumentParser(description="语义记忆搜索")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", required=True, help="用户ID")
    parser.add_argument("--query", help="搜索查询")
    parser.add_argument("--scope", default="private", choices=["private", "shared", "all", "*"],
                        help="搜索范围")
    parser.add_argument("--level", nargs="*", choices=["L1", "L2", "L3"],
                        help="限定层级")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--min-score", type=float, default=0.55)
    parser.add_argument("--semantic-weight", type=float, default=0.6,
                        help="语义权重 (0-1)，默认 0.6。0.6=语义优先，0.8=纯语义，0.3=重要性优先")
    parser.add_argument("--keyword-only", action="store_true", help="纯关键词模式")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--show-raw", action="store_true")
    parser.add_argument("--list-backends", action="store_true")
    # LanceDB 相关参数
    parser.add_argument("--no-lancedb", action="store_true", help="禁用 LanceDB HNSW 搜索")
    parser.add_argument("--no-cache", action="store_true", help="禁用查询缓存")
    parser.add_argument("--rebuild-index", action="store_true", help="重建 LanceDB 索引")
    parser.add_argument("--cache-stats", action="store_true", help="显示缓存统计")
    args = parser.parse_args()

    if args.list_backends:
        from embed_backends import list_backends
        print("\n可用 Embedding 后端:")
        for bid, info in list_backends().items():
            print(f"  {bid}: {info['name']} ({info['dim']}维)")
        return

    base_dir = os.path.abspath(args.base_dir)
    db_path = get_db_path(base_dir)

    if not os.path.exists(db_path):
        print(f"❌ 向量数据库不存在: {db_path}")
        print("   请先运行: python scripts/memory_embed.py --uid " + args.uid)
        sys.exit(1)

    # LanceDB 索引重建
    if args.rebuild_index:
        if not LANCEDB_AVAILABLE:
            print("❌ LanceDB 未安装。请运行: pip install lancedb")
            sys.exit(1)
        print("\n[1/2] 重建 LanceDB HNSW 索引...")
        manager = LanceDBManager(db_path)
        manager.connect()
        manager.rebuild_index(db_path)
        manager.close()
        print("[2/2] 缓存统计:")
        cache = SearchCache(db_path)
        print(f"   {cache.stats()}")
        print("\n✅ LanceDB 索引重建完成")
        return

    # 缓存统计
    if args.cache_stats:
        cache = SearchCache(db_path)
        stats = cache.stats()
        print("\n[Cache Statistics]")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        return

    conn = connect_db(db_path)

    if args.stats:
        print_stats(conn, db_path=db_path)
        
        # 显示 LanceDB 状态
        if LANCEDB_AVAILABLE and not args.no_lancedb:
            print("\n[LanceDB Status]")
            manager = LanceDBManager(db_path)
            if manager.connect():
                print("  Status: Enabled")
                print("  Index Type: HNSW")
            else:
                print("  Status: Disabled")
            manager.close()
        elif not LANCEDB_AVAILABLE:
            print("\n[Hint] Install LanceDB for 100x faster search: pip install lancedb")
        
        conn.close()
        return

    if not args.query:
        print("❌ 请提供 --query 参数")
        sys.exit(1)

    use_lancedb = LANCEDB_AVAILABLE and not args.no_lancedb
    use_cache = not args.no_cache

    print(f"\n🔍 搜索: \"{args.query}\"")
    print(f"   范围: {args.scope} | 用户: {args.uid} | 层级: {args.level or '全部'} | top-k: {args.top_k}")
    print(f"   语义权重: {args.semantic_weight} | LanceDB: {'ON' if use_lancedb else 'OFF'} | Cache: {'ON' if use_cache else 'OFF'}\n")

    if args.keyword_only:
        print("  [关键词搜索]\n")
        results, cols = keyword_search(conn, args.query, args.uid, args.scope, args.level, args.top_k, args.semantic_weight)
    else:
        if np is None:
            print("⚠️  缺少 numpy，使用关键词模式...")
            results, cols = keyword_search(conn, args.query, args.uid, args.scope, args.level, args.top_k, args.semantic_weight)
        else:
            print("  [向量语义搜索]\n  🔮 生成查询向量...")
            try:
                query_emb = get_embedding(args.query, db_path=db_path)
            except Exception as e:
                print(f"  ❌ 向量生成失败: {e}")
                print("  → 回退到关键词搜索...\n")
                results, cols = keyword_search(conn, args.query, args.uid, args.scope, args.level, args.top_k, args.semantic_weight)
            else:
                # 尝试 LanceDB HNSW 搜索
                start_time = time.time()
                lancedb_results = None
                
                if use_lancedb:
                    print("  ⚡ 使用 LanceDB HNSW 搜索...")
                    lancedb_results = search_vectors_lancedb(
                        query_emb, args.uid, args.scope, args.level, args.top_k, db_path
                    )
                
                if lancedb_results:
                    # LanceDB 结果转换
                    elapsed = time.time() - start_time
                    print(f"  ⚡ LanceDB 搜索完成 ({elapsed*1000:.1f}ms)\n")
                    
                    # 转换 LanceDB 结果为标准格式
                    scored = []
                    cols = ["chunk_id", "uid", "scope", "level", "filepath", 
                           "title", "semantic_key", "content", "importance_score", "related_ids"]
                    for r in lancedb_results:
                        imp = r.get("importance_score", 50.0) or 50.0
                        # LanceDB 返回的是相似度分数
                        sim_score = r.get("_distance", 0.5)
                        combined = sim_score * args.semantic_weight + (imp / 100.0) * (1 - args.semantic_weight)
                        scored.append((combined, sim_score, imp, r))
                    scored.sort(key=lambda x: -x[0])
                    results = [(s[0], s[1], s[2], s[3]) for s in scored[:args.top_k]]
                else:
                    # 回退到 SQLite 全表扫描
                    if use_lancedb:
                        print("  ⚠️  LanceDB 不可用，回退到 SQLite...\n")
                    results, cols = search_vectors(
                        conn, query_emb, args.uid, args.scope, args.level, args.top_k, args.min_score, args.semantic_weight
                    )

    if not results:
        print("  😕 没有找到相关记忆")
        print(f"\n  💡 建议: 降低 --min-score / 用 --keyword-only / 先运行 memory_embed.py --rebuild")
        conn.close()
        return

    print(f"  ✅ 找到 {len(results)} 条相关记忆:\n")
    for i, (combined, sim_score, importance, row) in enumerate(results, 1):
        print(f"  ── 结果 {i}/{len(results)} ──")
        print(format_raw_row(combined, row, cols) if args.show_raw
              else format_row(combined, sim_score, importance, row, cols))

    if results[0][1] < 0.65:
        print("  💡 结果相似度偏低，建议: 用更具体的描述 / 运行 memory_embed.py --rebuild")

    # 记录搜索访问
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from memory_access_log import get_db_path as _al_path, log_access
        log_db = _al_path(base_dir)
        if os.path.exists(log_db):
            chunk_ids = [r[3][cols.index("chunk_id")] for r in results]
            for cid in chunk_ids:
                log_access(log_db, cid, args.uid, "search")
    except Exception:
        pass  # 访问日志不影响搜索功能

    conn.close()


if __name__ == "__main__":
    main()
