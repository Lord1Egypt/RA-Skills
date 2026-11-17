#!/usr/bin/env python3
"""
记录向量索引工具 v2
SQLite 版本，支持增量更新
Embedding generation and retrieval for record-keeper skill
"""

import os
import sys
import json
import sqlite3
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

# ---- 可选依赖：numpy ----
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from openai import OpenAI

# =====================================================================
# 配置
# =====================================================================
CONFIG = {
    "api_key_env": "SILICONFLOW_API_KEY",
    "base_url": "https://api.siliconflow.cn/v1",
    "model": "BAAI/bge-m3",
    "dimension": 1024,
    "vectors_dir": Path.cwd() / "vectors",
    "records_dir": Path.cwd() / "records",
    "db_file": "embeddings.db",
    "index_file": "embeddings_index.json",  # 旧 v1 备份
}

# =====================================================================
# OpenAI 客户端 & 嵌入
# =====================================================================
def get_client():
    """获取 OpenAI 兼容客户端"""
    api_key = os.getenv(CONFIG["api_key_env"])
    if not api_key:
        raise ValueError(f"API KEY 未找到，请设置环境变量 {CONFIG['api_key_env']}")
    return OpenAI(api_key=api_key, base_url=CONFIG["base_url"])


def embed_text(text: str) -> list[float]:
    """生成文本嵌入向量，带 3 次重试
    
    如果文本过长，会自动截断到模型允许的最大长度。
    bge-m3 模型最大输入 8192 tokens，按 1 token ≈ 1.5 中文字符估算，
    保守截断到 20000 字符（约 13000 tokens）。
    """
    # 截断过长文本（bge-m3 最大 8192 tokens，实测上限约 15700 字符）
    MAX_CHARS = 15000
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]
    
    client = get_client()
    for attempt in range(1, 4):
        try:
            response = client.embeddings.create(
                model=CONFIG["model"],
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            if attempt < 3:
                import time
                time.sleep(1 * attempt)
                print(f"  ⚠️ API 调用失败，重试 {attempt}/3: {e}")
            else:
                raise


# =====================================================================
# 工具函数
# =====================================================================
def file_hash(path: Path) -> str:
    """SHA256 前 16 位"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def record_id(path: Path) -> str:
    """基于文件路径的 MD5 前 16 位"""
    return hashlib.md5(str(path).encode()).hexdigest()[:16]


def parse_category(filename: str) -> str:
    """从文件名解析类别：20260410-meeting-研发双周会.md -> meeting"""
    parts = filename.replace(".md", "").split("-", 2)
    # 第一个部分是日期，第二个部分是类别
    if len(parts) >= 2:
        return parts[1]
    return "unknown"


def extract_status_from_file(filepath: Path) -> str | None:
    """从 Markdown 文件提取状态字段（元信息表格中的「状态」行）
    
    返回归一化后的状态值（done/in_progress/pending/open/deferred），
    如果无法提取或无法归一化则返回 None。
    """
    import re
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 匹配 Markdown 表格行：| 状态 | xxx |
    patterns = [
        r"\|\s*状态\s*\|\s*([^|\n]+)\|",  # | 状态 | value |
        r"^\*\*状态\*\*[：:]\s*(.+)$",      # **状态**：value
        r"^状态[：:]\s*(.+)$",              # 状态：value
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
        if match:
            raw = match.group(1).strip()
            # 去掉 Markdown 链接、粗体等
            raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)  # [text](url) -> text
            raw = re.sub(r"\*\*([^*]+)\*\*", r"\1", raw)        # **text** -> text
            raw = raw.strip()
            
            # 归一化状态值
            # 导入 status.py 的归一化函数
            try:
                from status import normalize_status
                normalized = normalize_status(raw)
                if normalized:
                    return normalized
            except ImportError:
                pass
            
            # 如果无法归一化，尝试简单匹配
            raw_lower = raw.lower().replace("✅", "").strip()
            if "done" in raw_lower or "完成" in raw_lower or "已修复" in raw_lower:
                return "done"
            elif "progress" in raw_lower or "进行" in raw_lower or "处理" in raw_lower:
                return "in_progress"
            elif "pending" in raw_lower or "待" in raw_lower:
                return "pending"
            elif "open" in raw_lower or "未开始" in raw_lower:
                return "open"
            elif "deferred" in raw_lower or "延期" in raw_lower or "挂起" in raw_lower:
                return "deferred"
            
            # 无法归一化，返回 None
            return None
    
    return None


def extract_record_content(filepath: Path) -> str:
    """从记录文件提取用于嵌入的纯文本"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # 移除 Markdown 标记
    plain = (content
             .replace("#", "")
             .replace("*", "")
             .replace("`", "")
             .replace("-", "")
             .replace(">", ""))
    return plain


# =====================================================================
# 数据库
# =====================================================================
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS records (
    id         TEXT PRIMARY KEY,
    file       TEXT NOT NULL,
    filename   TEXT NOT NULL,
    date       TEXT NOT NULL,
    category   TEXT,
    file_hash  TEXT,
    mtime      REAL,
    preview    TEXT,
    embedding  BLOB NOT NULL,
    created_at TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_date      ON records(date);
CREATE INDEX IF NOT EXISTS idx_category  ON records(category);
CREATE INDEX IF NOT EXISTS idx_filename  ON records(filename);
"""


def get_db() -> sqlite3.Connection:
    """打开（或创建）SQLite 数据库"""
    CONFIG["vectors_dir"].mkdir(parents=True, exist_ok=True)
    db_path = CONFIG["vectors_dir"] / CONFIG["db_file"]
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(CREATE_SQL)
    conn.commit()
    return conn


def db_status(conn, rid: str) -> str | None:
    """查询已有 file_hash，不存在返回 None"""
    row = conn.execute("SELECT file_hash FROM records WHERE id = ?", (rid,)).fetchone()
    return row["file_hash"] if row else None


def db_upsert(conn, rec: dict):
    """INSERT OR REPLACE — 保留已有 status 字段"""
    # 更新时保留已有 status
    existing_status = None
    if rec.get("_update"):
        row = conn.execute("SELECT status FROM records WHERE id = ?", (rec["id"],)).fetchone()
        if row:
            existing_status = row["status"]

    conn.execute(
        """INSERT OR REPLACE INTO records
           (id, file, filename, date, category, file_hash, mtime, preview, embedding, created_at, updated_at, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            rec["id"], rec["file"], rec["filename"], rec["date"],
            rec["category"], rec["file_hash"], rec["mtime"],
            rec["preview"], rec["embedding_bytes"],
            rec["created_at"], rec["updated_at"],
            existing_status if existing_status else (rec.get("status") or "open"),
        ),
    )


# =====================================================================
# 向量编码 / 解码
# =====================================================================
def encode_embedding(embedding: list[float]) -> bytes:
    """list[float] -> bytes"""
    if HAS_NUMPY:
        return np.array(embedding, dtype="float32").tobytes()
    # 纯 Python fallback：每个 float 4 bytes, little-endian
    import struct
    return struct.pack(f"<{len(embedding)}f", *embedding)


def decode_embedding(raw: bytes) -> list[float]:
    """bytes -> list[float]"""
    if HAS_NUMPY:
        return np.frombuffer(raw, dtype="float32").tolist()
    import struct
    dim = len(raw) // 4
    return list(struct.unpack(f"<{dim}f", raw))


# =====================================================================
# init：增量生成索引
# =====================================================================
def cmd_init():
    """初始化或增量更新索引"""
    # 检查 v1 旧索引
    v1_path = CONFIG["vectors_dir"] / CONFIG["index_file"]
    has_v1 = v1_path.exists()
    if has_v1:
        print("⚠️  检测到旧版 JSON 索引，建议使用 `python3 embed.py migrate` 迁移\n")

    conn = get_db()
    now = datetime.now().isoformat()

    # 扫描所有记录文件
    record_files = sorted(
        f for f in CONFIG["records_dir"].rglob("*.md")
        if "archive" not in str(f)
    )

    if not record_files:
        print("⚠️  未找到任何记录文件")
        conn.close()
        return

    new_count = 0
    updated_count = 0
    skipped_count = 0

    print("🚀 开始生成向量索引（增量模式）...")

    for rf in record_files:
        rid = record_id(rf)
        fh = file_hash(rf)
        old_fh = db_status(conn, rid)

        if old_fh is None:
            status = "NEW"
        elif old_fh != fh:
            status = "UPDATED"
        else:
            status = "SKIPPED"

        if status == "SKIPPED":
            skipped_count += 1
            print(f"  ⏭️  SKIPPED: {rf.name} (未变更)")
            continue

        # 需要生成 / 更新嵌入
        try:
            plain_text = extract_record_content(rf)
            embedding = embed_text(plain_text)
        except Exception as e:
            print(f"  ❌ 处理失败 {rf.name}: {e}")
            continue

        embedding_bytes = encode_embedding(embedding)

        stat = rf.stat()
        rec = {
            "id": rid,
            "file": str(rf),
            "filename": rf.name,
            "date": rf.stem,
            "category": parse_category(rf.name),
            "file_hash": fh,
            "mtime": stat.st_mtime,
            "preview": plain_text[:200],
            "embedding_bytes": embedding_bytes,
            "created_at": now if status == "NEW" else None,
            "updated_at": now,
        }

        # 保持 created_at 和 status 不变
        if status == "UPDATED":
            old_row = conn.execute(
                "SELECT created_at, status FROM records WHERE id = ?", (rid,)
            ).fetchone()
            if old_row:
                rec["created_at"] = old_row["created_at"]
                if old_row["status"]:
                    rec["status"] = old_row["status"]

        # 从文件内容提取状态并同步到 SQLite
        file_status = extract_status_from_file(rf)
        if file_status:
            rec["status"] = file_status

        db_upsert(conn, rec)

        if status == "NEW":
            new_count += 1
            print(f"  ✅ NEW: {rf.name}")
        else:
            updated_count += 1
            print(f"  ✅ UPDATED: {rf.name}")

    conn.commit()
    conn.close()

    total = new_count + updated_count + skipped_count
    print(f"\n📊 新增: {new_count} | 更新: {updated_count} | 跳过: {skipped_count} | 总计: {total}")
    print(f"💾 索引已保存：{CONFIG['vectors_dir'] / CONFIG['db_file']}")


# =====================================================================
# sync-status：从文件内容同步状态到 SQLite（不重新生成 embedding）
# =====================================================================
def cmd_sync_status():
    """遍历所有记录文件，从文件内容提取状态并同步到 SQLite。
    不重新生成 embedding，仅更新 status 字段。"""
    conn = get_db()
    now = datetime.now().isoformat()

    record_files = sorted(
        f for f in CONFIG["records_dir"].rglob("*.md")
        if "archive" not in str(f)
    )

    if not record_files:
        print("⚠️  未找到任何记录文件")
        conn.close()
        return

    updated_count = 0
    skipped_count = 0
    no_status_count = 0

    print("🔄 开始同步文件状态到 SQLite...")

    for rf in record_files:
        rid = record_id(rf)

        # 查询 SQLite 中当前状态
        row = conn.execute(
            "SELECT status FROM records WHERE id = ?", (rid,)
        ).fetchone()

        if not row:
            # 文件未被索引，跳过
            continue

        current_status = row["status"] or "open"

        # 从文件提取状态
        file_status = extract_status_from_file(rf)

        if file_status is None:
            no_status_count += 1
            continue

        if file_status != current_status:
            conn.execute(
                "UPDATE records SET status = ?, updated_at = ? WHERE id = ?",
                (file_status, now, rid)
            )
            updated_count += 1
            print(f"  ✅ {rf.name}: {current_status} → {file_status}")
        else:
            skipped_count += 1

    conn.commit()
    conn.close()

    total = updated_count + skipped_count + no_status_count
    print(f"\n📊 更新: {updated_count} | 一致: {skipped_count} | 无状态字段: {no_status_count} | 总计: {total}")
    print(f"💾 索引已保存：{CONFIG['vectors_dir'] / CONFIG['db_file']}")


# =====================================================================
# migrate：v1 JSON → v2 SQLite
# =====================================================================
def cmd_migrate():
    """从 v1 JSON 索引迁移到 v2 SQLite"""
    v1_path = CONFIG["vectors_dir"] / CONFIG["index_file"]
    if not v1_path.exists():
        print("❌ 未找到旧版 JSON 索引，无需迁移")
        return

    # 先备份旧文件
    backup = v1_path.with_suffix(".json.bak")
    shutil.copy2(str(v1_path), str(backup))
    print(f"📦 已备份旧索引 → {backup.name}")

    with open(v1_path, "r", encoding="utf-8") as f:
        v1_data = json.load(f)

    v1_records = v1_data.get("records", {})
    if not v1_records:
        print("⚠️  旧索引中没有记录")
        return

    conn = get_db()
    now = datetime.now().isoformat()

    imported = 0
    for rid, rec in v1_records.items():
        # 尝试获取 file_hash（如果原文件还在）
        fp = Path(rec.get("file", ""))
        fh = file_hash(fp) if fp.exists() else ""
        mtime = fp.stat().st_mtime if fp.exists() else 0.0
        preview = rec.get("preview", "")[:200]

        embedding = rec.get("embedding", [])
        if not embedding:
            continue

        embedding_bytes = encode_embedding(embedding)

        conn.execute(
            """INSERT OR REPLACE INTO records
               (id, file, filename, date, category, file_hash, mtime, preview,
                embedding, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                rid,
                rec.get("file", ""),
                rec.get("filename", ""),
                rec.get("date", ""),
                parse_category(rec.get("filename", "")),
                fh,
                mtime,
                preview,
                embedding_bytes,
                v1_data.get("created", now),
                now,
            ),
        )
        imported += 1

    conn.commit()
    conn.close()

    print(f"✅ 已迁移 {imported} 条记录到 SQLite")
    print(f"💾 数据库：{CONFIG['vectors_dir'] / CONFIG['db_file']}")
    print(f"📦 旧索引已备份为 {backup.name}，确认无误后可手动删除")


# =====================================================================
# search：语义搜索
# =====================================================================
def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """计算余弦相似度"""
    if HAS_NUMPY:
        a = np.array(v1, dtype="float32")
        b = np.array(v2, dtype="float32")
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
    dot = sum(x * y for x, y in zip(v1, v2))
    n1 = sum(x * x for x in v1) ** 0.5
    n2 = sum(y * y for y in v2) ** 0.5
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


def cmd_search(query: str, top_k: int = 5):
    """语义搜索"""
    db_path = CONFIG["vectors_dir"] / CONFIG["db_file"]
    if not db_path.exists():
        # 回退：尝试 v1 JSON
        v1_path = CONFIG["vectors_dir"] / CONFIG["index_file"]
        if v1_path.exists():
            print("⚠️  未找到 SQLite 数据库，回退使用 v1 JSON 索引")
            return _search_v1(query, top_k)
        raise FileNotFoundError(
            "嵌入索引不存在，请先运行 `python3 embed.py init`"
        )

    # 检查数据库完整性
    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("SELECT COUNT(*) FROM records").fetchone()
    except Exception as e:
        conn.close()
        raise RuntimeError(
            f"数据库可能已损坏，请运行 `python3 embed.py init` 重建。错误: {e}"
        )

    # 获取所有记录
    rows = conn.execute("SELECT id, file, filename, date, category, preview, embedding FROM records").fetchall()

    if not rows:
        print("⚠️  数据库中没有记录")
        conn.close()
        return []

    # 生成查询嵌入
    print(f"🔍 正在搜索: \"{query}\"")
    query_vec = embed_text(query)

    # 计算相似度
    results = []
    for row in rows:
        emb = decode_embedding(row["embedding"])
        sim = cosine_similarity(query_vec, emb)
        results.append({
            "record_id": row["id"],
            "file": row["file"],
            "filename": row["filename"],
            "date": row["date"],
            "category": row["category"],
            "preview": row["preview"],
            "similarity": sim,
        })

    conn.close()

    # 排序 & 截断
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def _search_v1(query: str, top_k: int = 5) -> list:
    """v1 JSON 回退搜索"""
    v1_path = CONFIG["vectors_dir"] / CONFIG["index_file"]
    with open(v1_path, "r", encoding="utf-8") as f:
        index = json.load(f)

    query_vec = embed_text(query)
    results = []
    for rid, rec in index["records"].items():
        sim = cosine_similarity(query_vec, rec["embedding"])
        results.append({
            "record_id": rid,
            "file": rec["file"],
            "filename": rec["filename"],
            "date": rec["date"],
            "category": parse_category(rec["filename"]),
            "preview": rec.get("preview", ""),
            "similarity": sim,
        })
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


# =====================================================================
# search-recent：基于日期范围的记录查询
# =====================================================================
def cmd_search_recent(days: int = 7, categories: list = None):
    """按日期范围查询记录（不依赖向量语义，纯 SQL 过滤）"""
    from datetime import datetime, timedelta
    db_path = CONFIG["vectors_dir"] / CONFIG["db_file"]
    if not db_path.exists():
        raise FileNotFoundError(
            "嵌入索引不存在，请先运行 `python3 embed.py init`"
        )

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    # 计算日期范围
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")

    # date 字段是文件名 stem（如 20260528-task-xxx），前 8 位是 YYYYMMDD
    sql = "SELECT id, file, filename, date, category, preview, mtime FROM records WHERE substr(date, 1, 8) >= ?"
    params = [cutoff_date]

    if categories:
        placeholders = ",".join(["?"] * len(categories))
        sql += f" AND category IN ({placeholders})"
        params.extend(categories)

    sql += " ORDER BY date DESC"

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "file": row["file"],
            "filename": row["filename"],
            "date": row["date"],
            "category": row["category"],
            "preview": row["preview"],
            "mtime": row["mtime"],
        })

    return results


# =====================================================================
# search-range：按精确日期范围查询
# =====================================================================
def cmd_search_range(date_from: str = None, date_to: str = None, categories: list = None):
    """按精确日期范围查询记录（不依赖向量语义，纯 SQL 过滤）
    
    边界语义：
    - date_from：包含（>=），即从指定日期的 00:00:00 开始
    - date_to：包含（<=），即截止到指定日期的 23:59:59
    - 日期格式：YYYYMMDD（如 20260522）或 YYYY-MM-DD（如 2026-05-22）
    - date_from 默认值：7 天前
    - date_to 默认值：今天
    """
    db_path = CONFIG["vectors_dir"] / CONFIG["db_file"]
    if not db_path.exists():
        raise FileNotFoundError(
            "嵌入索引不存在，请先运行 `python3 embed.py init`"
        )

    # 规范化日期格式
    def normalize_date(d, fallback):
        if d is None:
            d = fallback
        d = d.replace("-", "")  # 2026-05-22 -> 20260522
        return d

    from datetime import datetime, timedelta
    today = datetime.now().strftime("%Y%m%d")
    d_from = normalize_date(date_from, (datetime.now() - timedelta(days=7)).strftime("%Y%m%d"))
    d_to = normalize_date(date_to, today)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    sql = "SELECT id, file, filename, date, category, preview, mtime FROM records WHERE substr(date, 1, 8) >= ? AND substr(date, 1, 8) <= ?"
    params = [d_from, d_to]

    if categories:
        placeholders = ",".join(["?"] * len(categories))
        sql += f" AND category IN ({placeholders})"
        params.extend(categories)

    sql += " ORDER BY date DESC"

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "file": row["file"],
            "filename": row["filename"],
            "date": row["date"],
            "category": row["category"],
            "preview": row["preview"],
            "mtime": row["mtime"],
        })

    return results, d_from, d_to


# =====================================================================
# CLI 入口
# =====================================================================
def main():
    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 embed.py init              # 初始化 / 增量更新索引")
        print('  python3 embed.py search "关键词" 5  # 语义搜索')
        print("  python3 embed.py search-recent --days 7 [--category task --category plan]  # 按最近 N 天查询")
        print("  python3 embed.py search-range --from 20260501 --to 20260531 [--category task]  # 按精确日期范围查询")
        print("  python3 embed.py migrate            # 从 v1 JSON 迁移到 v2 SQLite")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()

    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        results = cmd_search(query, top_k)
        if not results:
            print("  未找到相关记录")
            return
        print(f"\n🔍 找到 {len(results)} 条相关记录:\n")
        for r in results:
            print(f"  [{r['similarity']:.3f}] {r['filename']} ({r.get('category', '?')}) - {r['date']}")
            preview = (r.get("preview") or "")[:100]
            print(f"    {preview}...\n")

    elif cmd == "search-recent":
        # 解析参数
        days = 7
        categories = []
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--days" and i + 1 < len(sys.argv):
                days = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                categories.append(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        results = cmd_search_recent(days=days, categories=categories if categories else None)

        # JSON 输出（供 cron 提示词解析）
        output = {
            "query": {
                "days": days,
                "categories": categories,
            },
            "count": len(results),
            "results": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif cmd == "search-range":
        # 解析参数
        date_from = None
        date_to = None
        categories = []
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--from" and i + 1 < len(sys.argv):
                date_from = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--to" and i + 1 < len(sys.argv):
                date_to = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--category" and i + 1 < len(sys.argv):
                categories.append(sys.argv[i + 1])
                i += 2
            else:
                i += 1

        results, d_from, d_to = cmd_search_range(
            date_from=date_from, date_to=date_to,
            categories=categories if categories else None
        )

        # JSON 输出
        output = {
            "query": {
                "date_from": d_from,
                "date_to": d_to,
                "categories": categories,
                "boundary": "date_from 包含（>=），date_to 包含（<=）",
            },
            "count": len(results),
            "results": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif cmd == "migrate":
        cmd_migrate()

    elif cmd == "sync-status":
        cmd_sync_status()

    else:
        print(f"❌ 未知命令: {cmd}")
        print("可用命令: init, search, search-recent, search-range, sync-status, migrate")


if __name__ == "__main__":
    main()
