#!/usr/bin/env python3
"""
memory_embed.py - 为记忆条目生成语义向量嵌入并存入 SQLite 向量库

用法:
  python scripts/memory_embed.py --uid pupper --rebuild        # 全量重建
  python scripts/memory_embed.py --uid pupper                  # 增量更新
  python scripts/memory_embed.py --uid pupper --scope shared   # 仅公共记忆
  python scripts/memory_embed.py --uid pupper --dry-run        # 预览不写入
  python scripts/memory_embed.py --uid pupper --delete         # 删除该用户所有向量
  python scripts/memory_embed.py --uid pupper --rebuild-index  # 重建 LanceDB 索引
  python scripts/memory_embed.py --list-backends              # 列出可用后端

后端配置:
  # 方式1：环境变量
  export EMBED_BACKEND=siliconflow        # openai / siliconflow / zhipu
  export SILICONFLOW_KEY=sk-xxx           # 对应后端的 API key

  # 方式2：配置文件（与 .memory_vectors.db 同目录）
  # .memory_config.json: {"backend": "siliconflow"}

依赖:
  pip install openai numpy lancedb  # lancedb 可选，增强搜索性能

优化特性:
  - 并行 embedding（多线程批量处理）
  - LanceDB 索引自动更新
"""

import os
import re
import sys
import json
import sqlite3
import hashlib
import argparse
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 统一 embedding 后端（确保同目录下的模块可被导入）
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from embed_backends import get_embeddings, get_embedding_dim, get_backend_info

DB_NAME = ".memory_vectors.db"
CFG_NAME = ".memory_config.json"


# ══════════════════════════════════════════════════════════════
#  并行 Embedding
# ══════════════════════════════════════════════════════════════

# 并行配置
PARALLEL_WORKERS = int(os.environ.get("PARALLEL_WORKERS", "4"))
EMBED_BATCH_SIZE = int(os.environ.get("EMBED_BATCH_SIZE", "20"))


def parallel_embed(texts: list, get_embeddings_func, workers: int = None, batch_size: int = None):
    """
    并行执行 embedding（多线程批量处理）
    
    Args:
        texts: 文本列表
        get_embeddings_func: embedding 函数 (接受 list 返回 list)
        workers: 并行线程数
        batch_size: 每批大小
        
    Returns:
        向量列表
        
    性能提升:
        - 4线程: ~2-3x 速度提升
        - 适合大批量数据 (>100 条)
    """
    if len(texts) < 10:
        # 数据量小，直接串行
        return get_embeddings_func(texts)
    
    workers = workers or PARALLEL_WORKERS
    batch_size = batch_size or EMBED_BATCH_SIZE
    
    # 分批
    batches = [texts[i:i+batch_size] for i in range(0, len(texts), batch_size)]
    
    print(f"  [Parallel] 分 {len(batches)} 批处理，每批 {batch_size} 条，{workers} 线程")
    
    results = [None] * len(batches)
    
    def process_batch(batch_idx, batch_texts):
        start = time.time()
        vectors = get_embeddings_func(batch_texts)
        elapsed = time.time() - start
        return batch_idx, vectors, elapsed
    
    batch_times = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(process_batch, i, batch): i 
            for i, batch in enumerate(batches)
        }
        
        for future in as_completed(futures):
            batch_idx, vectors, elapsed = future.result()
            results[batch_idx] = vectors
            batch_times.append(elapsed)
    
    # 合并结果
    all_vectors = []
    for vectors in results:
        all_vectors.extend(vectors)
    
    total_time = sum(batch_times)
    avg_time = total_time / len(batch_times) if batch_times else 0
    print(f"  [Parallel] 完成 {len(texts)} 条，总耗时 {total_time:.1f}s，平均每批 {avg_time:.2f}s")
    
    return all_vectors


# ══════════════════════════════════════════════════════════════
#  安全工具
# ══════════════════════════════════════════════════════════════

def safe_relpath(path, base):
    """安全获取相对路径，防止路径穿越攻击"""
    try:
        abspath = Path(path).resolve()
        basepath = Path(base).resolve()
        rel = abspath.relative_to(basepath)
        if str(rel).startswith(".."):
            return None
        return str(rel)
    except (ValueError, OSError):
        return None


# ══════════════════════════════════════════════════════════════
#  向量数据库层（SQLite + numpy）
# ══════════════════════════════════════════════════════════════

def get_db_path(base_dir):
    return os.path.join(os.path.abspath(base_dir), DB_NAME)


def get_cfg_path(base_dir):
    return os.path.join(os.path.abspath(base_dir), CFG_NAME)


def init_db(db_path):
    """初始化向量数据库表（含迁移：自动添加新列）"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL")

    # 新建表（首次）
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory_embeddings (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk_id       TEXT    UNIQUE NOT NULL,
            uid            TEXT    NOT NULL,
            scope          TEXT    NOT NULL,
            level          TEXT    NOT NULL,
            filepath       TEXT    NOT NULL,
            section_idx    INTEGER NOT NULL,
            title          TEXT    NOT NULL,
            semantic_key   TEXT    NOT NULL,
            content        TEXT    NOT NULL,
            raw_content    TEXT    NOT NULL,
            embedding      BLOB    NOT NULL,
            content_hash   TEXT    NOT NULL,
            mtime          REAL    NOT NULL,
            created_at     TEXT    NOT NULL,
            importance_score REAL  DEFAULT 50.0,
            related_ids    TEXT    DEFAULT '[]'
        )
    """)
    c.execute("CREATE INDEX IF NOT EXISTS idx_uid ON memory_embeddings(uid)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_scope ON memory_embeddings(scope)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_level ON memory_embeddings(level)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_content_hash ON memory_embeddings(content_hash)")

    # 迁移：如果表已存在，添加新列（v2.3 → v3.0）
    for col, col_type in [
        ("importance_score", "REAL DEFAULT 50.0"),
        ("related_ids", "TEXT DEFAULT '[]'"),
    ]:
        try:
            c.execute(f"ALTER TABLE memory_embeddings ADD COLUMN {col} {col_type}")
        except sqlite3.OperationalError:
            pass  # 列已存在

    conn.commit()
    return conn


def store_embedding(conn, row):
    """写入单条向量记录（upsert by chunk_id）"""
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO memory_embeddings
        (chunk_id, uid, scope, level, filepath, section_idx,
         title, semantic_key, content, raw_content, embedding, content_hash, mtime,
         created_at, importance_score, related_ids)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)
    conn.commit()


def delete_embeddings(conn, uid=None, scope=None):
    """删除向量记录"""
    c = conn.cursor()
    conditions = []
    params = []
    if uid:
        conditions.append("uid=?")
        params.append(uid)
    if scope:
        conditions.append("scope=?")
        params.append(scope)
    if conditions:
        c.execute(f"DELETE FROM memory_embeddings WHERE {' AND '.join(conditions)}", params)
    conn.commit()
    # VACUUM 释放空间
    c.execute("VACUUM")
    conn.commit()


def get_existing_records(conn, filepaths):
    """
    批量查询已有记录的 (content_hash, mtime_str) -> (chunk_id, filepath)
    用于增量判断。
    """
    if not filepaths:
        return {}
    c = conn.cursor()
    placeholders = ",".join("?" * len(filepaths))
    c.execute(
        f"SELECT content_hash, mtime, chunk_id, filepath FROM memory_embeddings WHERE filepath IN ({placeholders})",
        filepaths,
    )
    return {(row[0], str(row[1])): (row[2], row[3]) for row in c.fetchall()}


# ══════════════════════════════════════════════════════════════
#  记忆条目解析层
# ══════════════════════════════════════════════════════════════

def parse_sections(filepath):
    """解析 .md 文件，返回条目列表"""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    sections = []
    parts = re.split(r"(?=^## )", content, flags=re.MULTILINE)
    for idx, part in enumerate(parts):
        part = part.strip()
        if not part or len(part) < 10:
            continue
        lines = part.split("\nfrom typing import List, Dict, Optional, Union, Any, Tuple\n")
        raw_title = lines[0].strip().lstrip("#").strip()
        title_clean = re.sub(r"^\[\d{2}:\d{2}\]\s*", "", raw_title)
        semantic_key = title_clean if len(title_clean) <= 20 else title_clean[:17] + "..."
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        if len(body) < 5:
            continue
        sections.append({
            "title": raw_title,
            "semantic_key": semantic_key,
            "content": body,
            "raw_content": part,
            "section_idx": idx,
        })
    return sections


def make_content_hash(content: str) -> str:
    """基于内容生成哈希（SHA-256前32位）"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:32]


def smart_embed_text(semantic_key: str, content: str, max_len: int = 800) -> str:
    """
    智能文本截断：头+中+尾，保留语义完整性。
    比简单截断更好地捕获长记忆的完整语义。
    """
    if len(content) <= max_len:
        return f"{semantic_key}: {content}"
    head = content[:400]
    mid_start = max(300, len(content) // 2 - 100)
    middle = content[mid_start:mid_start + 200]
    tail = content[-200:]
    return f"{semantic_key}: {head} ... {middle} ... {tail}"


def make_chunk_id(content_hash: str, mtime: float, section_idx: int) -> str:
    """生成唯一 chunk_id"""
    raw = f"{content_hash}|{mtime}|{section_idx}"
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


def scan_memory_files(base_dir, uid, scope="all"):
    """
    扫描记忆文件，yield 待 embed 条目。
    base_dir: 仓库根目录（用于安全检查）
    """
    base_abs = os.path.abspath(base_dir)

    if scope in ("private", "all"):
        user_dir = os.path.join(base_abs, "users", uid)
        if os.path.exists(user_dir):
            for subdir, level in [
                (os.path.join(user_dir, "daily"), "L1"),
                (os.path.join(user_dir, "weekly"), "L2"),
                (os.path.join(user_dir, "permanent"), "L3"),
            ]:
                if not os.path.isdir(subdir):
                    continue
                for fname in sorted(os.listdir(subdir), reverse=True):
                    if not fname.endswith(".md"):
                        continue
                    fpath = os.path.join(subdir, fname)
                    rel = safe_relpath(fpath, base_abs)
                    if rel is None:
                        continue
                    mtime = os.path.getmtime(fpath)
                    sections = parse_sections(fpath)
                    if sections:
                        yield (fpath, rel, mtime, sections, level, uid, "private")

    if scope in ("shared", "all"):
        shared_dir = os.path.join(base_abs, "shared")
        if os.path.exists(shared_dir):
            for subdir, level in [
                (os.path.join(shared_dir, "daily"), "L1"),
                (os.path.join(shared_dir, "weekly"), "L2"),
                (os.path.join(shared_dir, "permanent"), "L3"),
            ]:
                if not os.path.isdir(subdir):
                    continue
                for fname in sorted(os.listdir(subdir), reverse=True):
                    if not fname.endswith(".md"):
                        continue
                    fpath = os.path.join(subdir, fname)
                    rel = safe_relpath(fpath, base_abs)
                    if rel is None:
                        continue
                    mtime = os.path.getmtime(fpath)
                    sections = parse_sections(fpath)
                    if sections:
                        yield (fpath, rel, mtime, sections, level, "shared", "shared")


# ══════════════════════════════════════════════════════════════
#  关联记忆 + 重要性计算
# ══════════════════════════════════════════════════════════════

def compute_related_memories(conn, uid, similarity_threshold=0.75):
    """
    计算所有记忆之间的语义关联。
    余弦相似度 > threshold 的两条记忆，互为 related_ids。

    关联存储在 related_ids 列（JSON 数组），每次 rebuild 时重新计算。
    关联数量无上限，但仅存 chunk_id，不存相似度分值（节省空间）。
    """
    try:
        import numpy as np
    except ImportError:
        print("  ⚠️  numpy 未安装，跳过关联计算")
        return

    c = conn.cursor()
    c.execute("""
        SELECT chunk_id, embedding, level, title
        FROM memory_embeddings
        WHERE uid = ? OR uid = 'shared'
    """, (uid,))
    rows = c.fetchall()

    if len(rows) < 2:
        return

    print(f"\n  🔗 计算 {len(rows)} 条记忆的关联关系（阈值: {similarity_threshold}）...")

    chunk_ids = [r[0] for r in rows]
    embeddings = [np.frombuffer(r[1], dtype=np.float32) for r in rows]

    # 预归一化，提升余弦相似度计算效率
    norms = [np.linalg.norm(e) for e in embeddings]
    normed = [e / n if n > 0 else e for e, n in zip(embeddings, norms)]

    # 建立 chunk_id → index 映射
    idx_map = {cid: i for i, cid in enumerate(chunk_ids)}

    # 计算关系（只存已存储的 chunk_id）
    related_map = {cid: [] for cid in chunk_ids}

    # 增量：只对本次 embed 的新 chunk 计算关系，已有关联保留
    existing_related = {}
    c.execute(f"SELECT chunk_id, related_ids FROM memory_embeddings WHERE uid = ?", (uid,))
    for cid, rids_json in c.fetchall():
        if rids_json and rids_json != "[]":
            try:
                existing_related[cid] = json.loads(rids_json)
            except Exception:
                existing_related[cid] = []

    for i, cid_i in enumerate(chunk_ids):
        if cid_i in existing_related:
            # 已有关联保留，新关联追加
            related_map[cid_i] = list(existing_related[cid_i])
        for j, cid_j in enumerate(chunk_ids):
            if i >= j:
                continue
            sim = float(np.dot(normed[i], normed[j]))
            if sim > similarity_threshold:
                for target_cid, source_cid in [(cid_i, cid_j), (cid_j, cid_i)]:
                    if target_cid not in related_map[target_cid]:
                        related_map[target_cid].append(source_cid)

    # 写回数据库
    updated = 0
    for cid, rids in related_map.items():
        if rids:  # 只更新有关系的
            c.execute(
                "UPDATE memory_embeddings SET related_ids = ? WHERE chunk_id = ?",
                (json.dumps(rids), cid)
            )
            updated += 1

    conn.commit()
    print(f"  ✅ 关联计算完成，{updated} 条记忆建立了关联关系")


def update_importance_scores(conn, uid):
    """
    从访问日志读取重要性评分，更新向量库。
    """
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from memory_access_log import get_all_importance_scores, calculate_importance_score
    except ImportError:
        return

    db_path = conn.execute("PRAGMA database_list").fetchone()[2]
    access_log_db = os.path.join(os.path.dirname(db_path), ".memory_access_log.db")
    if not os.path.exists(access_log_db):
        return

    stats = get_all_importance_scores(access_log_db, uid)
    if not stats:
        return

    c = conn.cursor()
    updated = 0
    for chunk_id, stat in stats.items():
        level_row = c.execute(
            "SELECT level FROM memory_embeddings WHERE chunk_id = ?", (chunk_id,)
        ).fetchone()
        if level_row:
            score = calculate_importance_score(
                access_log_db, uid, chunk_id, level_row[0]
            )
            c.execute(
                "UPDATE memory_embeddings SET importance_score = ? WHERE chunk_id = ?",
                (score, chunk_id)
            )
            updated += 1

    conn.commit()
    if updated > 0:
        print(f"  📊 重要性评分已更新（{updated} 条）")


# ══════════════════════════════════════════════════════════════
#  主流程
# ══════════════════════════════════════════════════════════════

def embed_all(base_dir, uid, scope, dry_run, rebuild):
    base_abs = os.path.abspath(base_dir)
    os.makedirs(base_abs, exist_ok=True)
    db_path = get_db_path(base_abs)
    conn = init_db(db_path)

    try:
        backend_info = get_backend_info(db_path)
        print(f"\n🔮 使用后端: {backend_info['name']} ({backend_info['dim']}维)")
    except Exception as e:
        print(f"\n⚠️  后端配置: {e}")
        print("   尝试使用默认配置...")

    if rebuild:
        print(f"🗑️  重建模式：清除 {uid} 的旧向量...")
        delete_embeddings(conn, uid=uid if scope != "all" else None,
                         scope=scope if scope == "shared" else None)
        existing_map = {}
    else:
        filepaths = [item[0] for item in scan_memory_files(base_abs, uid, scope)]
        existing_map = get_existing_records(conn, filepaths)

    print(f"\n📁 数据库: {db_path}")
    print(f"📦 范围: {scope} | 用户: {uid}\n")

    stats = {"total": 0, "new": 0, "skipped": 0, "errors": 0}
    batch_texts = []
    batch_rows = []

    for fpath, rel_path, mtime, sections, level, owner, sc in scan_memory_files(base_abs, uid, scope):
        for sec in sections:
            content_hash = make_content_hash(sec["content"])
            chunk_id = make_chunk_id(content_hash, mtime, sec["section_idx"])
            mtime_str = str(mtime)

            # 增量判断：content_hash + mtime 均相同才跳过
            if not rebuild and (content_hash, mtime_str) in existing_map:
                stats["skipped"] += 1
                continue

            embed_text = smart_embed_text(sec['semantic_key'], sec['content'])
            batch_texts.append(embed_text)
            batch_rows.append((
                chunk_id, uid, sc, level, rel_path, sec["section_idx"],
                sec["title"], sec["semantic_key"], sec["content"],
                sec["raw_content"], content_hash, mtime,
                # importance_score 和 related_ids 暂用默认值，写入后由 compute_related_memories 更新
                50.0, "[]",
            ))

    if not batch_texts:
        print("  ✅ 没有新内容需要 embed")
        print(f"  📊 统计: 跳过 {stats['skipped']} 条已有向量")
        conn.close()
        return

    print(f"  📦 准备 embed {len(batch_texts)} 条新条目...")

    try:
        start_time = time.time()
        # 使用并行 embedding（数据量大时自动启用）
        embeddings = parallel_embed(batch_texts, lambda texts: get_embeddings(texts, db_path=db_path))
        elapsed = time.time() - start_time
        print(f"  ⏱️  Embedding 完成，耗时 {elapsed:.2f}s ({len(batch_texts)/elapsed:.1f} 条/秒)")
    except Exception as e:
        print(f"  ❌ Embedding API 错误: {e}")
        conn.close()
        sys.exit(1)

    now = datetime.now().isoformat()
    for i, emb in enumerate(embeddings):
        (chunk_id, row_uid, sc, level, rel_path, section_idx,
         title, semantic_key, content, raw_content, content_hash, mtime) = batch_rows[i]

        store_row = (
            chunk_id, row_uid, sc, level, rel_path, section_idx,
            title, semantic_key, content, raw_content,
            emb.tobytes(), content_hash, mtime, now,
            50.0, "[]",
        )
        if not dry_run:
            store_embedding(conn, store_row)
        stats["new"] += 1

    conn.close()

    print(f"\n  ✅ 完成！新增向量: {stats['new']}")
    if stats["skipped"]:
        print(f"     跳过已有: {stats['skipped']}")
    if dry_run:
        print(f"     [DRY-RUN] 未实际写入数据库")

    # 关联记忆 + 重要性评分（写入完成后计算）
    if not dry_run and (stats["new"] > 0 or rebuild):
        conn2 = init_db(db_path)
        compute_related_memories(conn2, uid)
        update_importance_scores(conn2, uid)
        conn2.close()

    if not dry_run:
        print(f"\n💡 语义搜索: python scripts/memory_search.py --uid {uid} --scope private \"查询内容\"")
        print(f"💡 查看统计: python scripts/memory_search.py --uid {uid} --scope private --stats")


def main():
    parser = argparse.ArgumentParser(description="为记忆条目生成语义向量")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", required=True, help="用户ID")
    parser.add_argument("--scope", default="private", choices=["private", "shared", "all"],
                        help="嵌入范围")
    parser.add_argument("--rebuild", action="store_true", help="全量重建")
    parser.add_argument("--dry-run", action="store_true", help="预览，不写入数据库")
    parser.add_argument("--delete", action="store_true", help="删除该用户所有向量记录")
    parser.add_argument("--list-backends", action="store_true", help="列出可用后端")
    args = parser.parse_args()

    if args.list_backends:
        from embed_backends import list_backends
        print("\n可用 Embedding 后端:")
        for bid, info in list_backends().items():
            print(f"  {bid}: {info['name']} ({info['dim']}维)")
        return

    base_dir = os.path.abspath(args.base_dir)

    if args.delete:
        db_path = get_db_path(base_dir)
        if os.path.exists(db_path):
            conn = init_db(db_path)
            delete_embeddings(conn, uid=args.uid)
            conn.close()
            print(f"✅ 已删除用户 {args.uid} 的所有向量记录")
        else:
            print("数据库不存在，无需删除")
        return

    embed_all(base_dir, args.uid, args.scope, args.dry_run, args.rebuild)


if __name__ == "__main__":
    main()
