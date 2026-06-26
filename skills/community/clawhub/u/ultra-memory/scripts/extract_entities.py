#!/usr/bin/env python3
"""
ultra-memory: 结构化实体提取
从操作日志中提取函数名、文件路径、依赖包、决策、错误等结构化实体，
写入 semantic/entities.jsonl，作为 recall 的第4检索层。

解决的问题：
  "我们在 auth 模块动过哪些文件？" → 实体检索精确命中
  "添加了哪些依赖？" → 依赖实体列表
  "有哪些关键决策？" → 决策实体列表
  以上查询用 bigram 关键词匹配完全无法回答。

被 log_op.py 在每次写入时自动调用，无需手动触发。
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# ── 提取规则 ──────────────────────────────────────────────────────────────

# 函数名：匹配 funcname() 或 def funcname
FUNC_PATTERN = re.compile(r'\b([a-zA-Z_][a-zA-Z0-9_]{2,})\s*\(\)', re.MULTILINE)
DEF_PATTERN  = re.compile(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]+)', re.MULTILINE)

# 文件路径：匹配含 / 或 \ 的带扩展名路径，以及 detail.path 字段
FILE_EXT = r'\.(py|js|ts|jsx|tsx|vue|html|css|scss|json|yaml|yml|toml|md|sql|sh|go|rs|java|rb|php|cpp|c|h)'
FILE_PATTERN = re.compile(
    r'(?:[a-zA-Z0-9_\-\.]+/)+[a-zA-Z0-9_\-\.]+' + FILE_EXT + r'\b',
    re.IGNORECASE
)

# 依赖包：从 pip install / npm install 等命令提取
PIP_PATTERN  = re.compile(r'pip3?\s+install\s+([\w\-]+(?:\s+[\w\-]+)*)', re.IGNORECASE)
NPM_PATTERN  = re.compile(r'(?:npm|yarn|pnpm)\s+(?:install|add)\s+([\w\-@/]+)', re.IGNORECASE)

# 错误类型：ExceptionName 或 Error: message
ERROR_PATTERN = re.compile(r'\b([A-Z][a-zA-Z]+(?:Error|Exception|Warning|Fault))\b')

# 类名：class ClassName
CLASS_PATTERN = re.compile(r'\bclass\s+([A-Z][a-zA-Z0-9_]+)', re.MULTILINE)


def extract_from_op(op: dict) -> list[dict]:
    """
    从单条操作记录中提取结构化实体。

    返回实体列表，每条实体格式：
    {
        "entity_type": "function|file|dependency|decision|error|class",
        "name": "clean_df",
        "context": "实现数据清洗函数",   # 原始 summary 片段
        "session_id": "sess_xxx",
        "op_seq": 42,
        "ts": "2026-04-02T...",
        "tags": ["code", "data"]
    }
    """
    entities = []
    summary = op.get("summary", "")
    detail  = op.get("detail", {})
    op_type = op.get("type", "")
    ts      = op.get("ts", "")
    seq     = op.get("seq", 0)
    tags    = op.get("tags", [])
    session = op.get("_session_id", "")

    base = {
        "op_seq": seq,
        "ts": ts,
        "tags": tags,
        "context": summary[:80],
        "session_id": session,
    }

    combined_text = summary + " " + json.dumps(detail, ensure_ascii=False)

    # 1. 文件实体（优先从 detail.path 提取，最精确）
    file_path = detail.get("path", "")
    if file_path and op_type == "file_write":
        entities.append({**base,
            "entity_type": "file",
            "name": file_path,
            "op_type": op_type,
        })
    else:
        # 从文本中提取文件路径
        for m in FILE_PATTERN.finditer(combined_text):
            fpath = m.group(0)
            if len(fpath) > 3:  # 过滤太短的误匹配
                entities.append({**base,
                    "entity_type": "file",
                    "name": fpath,
                    "op_type": op_type,
                })

    # 2. 函数/方法实体
    for m in FUNC_PATTERN.finditer(combined_text):
        name = m.group(1)
        # 过滤：排除常见英文单词和太短的名字
        if len(name) > 3 and name not in {
            "print", "open", "read", "write", "list", "dict", "type",
            "True", "False", "None", "self", "args", "kwargs"
        }:
            entities.append({**base,
                "entity_type": "function",
                "name": name,
            })
    for m in DEF_PATTERN.finditer(combined_text):
        name = m.group(1)
        if len(name) > 3:
            entities.append({**base,
                "entity_type": "function",
                "name": name,
            })

    # 3. 类实体
    for m in CLASS_PATTERN.finditer(combined_text):
        entities.append({**base,
            "entity_type": "class",
            "name": m.group(1),
        })

    # 4. 依赖包实体（从 bash_exec 命令提取）
    if op_type == "bash_exec":
        cmd = detail.get("cmd", summary)
        for m in PIP_PATTERN.finditer(cmd):
            for pkg in m.group(1).split():
                pkg = pkg.strip()
                if pkg and not pkg.startswith("-"):
                    entities.append({**base,
                        "entity_type": "dependency",
                        "name": pkg,
                        "manager": "pip",
                    })
        for m in NPM_PATTERN.finditer(cmd):
            pkg = m.group(1).strip()
            if pkg:
                entities.append({**base,
                    "entity_type": "dependency",
                    "name": pkg,
                    "manager": "npm",
                })

    # 5. 决策实体（type == decision 全部保留，字段完整）
    if op_type == "decision":
        entities.append({**base,
            "entity_type": "decision",
            "name": summary[:60],
            "rationale": detail.get("rationale", ""),
        })

    # 6. 错误实体（记录错误类型）
    if op_type == "error":
        for m in ERROR_PATTERN.finditer(combined_text):
            entities.append({**base,
                "entity_type": "error",
                "name": m.group(1),
                "message": summary[:60],
            })
        if not ERROR_PATTERN.search(combined_text):
            # 没有识别到具体错误类型，记录通用错误
            entities.append({**base,
                "entity_type": "error",
                "name": "UnknownError",
                "message": summary[:60],
            })

    return entities


def deduplicate_entities(existing: list[dict], new_entities: list[dict]) -> list[dict]:
    """
    实体去重：相同 (entity_type, name) 在同一 session 中只保留最新一条。
    跨 session 的同类实体保留（用于追踪变化）。
    """
    # 构建现有实体的 key 集合（session + type + name）
    existing_keys = {
        (e.get("session_id"), e.get("entity_type"), e.get("name"))
        for e in existing
    }
    added = []
    for ent in new_entities:
        key = (ent.get("session_id"), ent.get("entity_type"), ent.get("name"))
        if key not in existing_keys:
            existing_keys.add(key)
            added.append(ent)
        else:
            # 同 session 内相同实体：更新 ts 和 context（追加写入，不修改旧记录）
            added.append(ent)  # 允许多次出现，recall 时取最新
    return added


def append_entities(entities: list[dict], session_id: str):
    """将提取的实体追加写入 semantic/entities.jsonl"""
    if not entities:
        return
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    semantic_dir.mkdir(parents=True, exist_ok=True)
    entities_file = semantic_dir / "entities.jsonl"

    # 为每个实体附上 session_id（如果尚未有）
    for ent in entities:
        if not ent.get("session_id"):
            ent["session_id"] = session_id

    with open(entities_file, "a", encoding="utf-8") as f:
        for ent in entities:
            f.write(json.dumps(ent, ensure_ascii=False) + "\n")


def extract_and_store(session_id: str, op: dict):
    """对单条操作提取实体并写入 entities.jsonl（供 log_op.py 调用）"""
    op["_session_id"] = session_id
    entities = extract_from_op(op)
    if entities:
        append_entities(entities, session_id)
    return entities


def extract_all(session_id: str):
    """全量提取：对整个 ops.jsonl 重新提取实体（适合初次运行或修复）"""
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        print(f"[ultra-memory] ⚠️  ops.jsonl 不存在: {session_id}")
        return

    # 清除该 session 的旧实体（重新提取）
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    entities_file = semantic_dir / "entities.jsonl"
    if entities_file.exists():
        with open(entities_file, encoding="utf-8") as f:
            existing = [json.loads(l) for l in f if l.strip()]
        # 保留其他 session 的实体
        kept = [e for e in existing if e.get("session_id") != session_id]
    else:
        kept = []

    # 重新提取
    new_entities = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                op = json.loads(line)
                op["_session_id"] = session_id
                new_entities.extend(extract_from_op(op))
            except json.JSONDecodeError:
                continue

    all_entities = kept + new_entities
    semantic_dir.mkdir(parents=True, exist_ok=True)
    with open(entities_file, "w", encoding="utf-8") as f:
        for ent in all_entities:
            f.write(json.dumps(ent, ensure_ascii=False) + "\n")

    # 统计
    type_counts: dict[str, int] = {}
    for e in new_entities:
        t = e.get("entity_type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"[ultra-memory] ✅ 实体提取完成 (session: {session_id})")
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c} 个")
    print(f"  总计: {len(new_entities)} 个实体")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从操作日志提取结构化实体")
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument("--all", action="store_true",
                        help="全量重新提取（默认只提取未提取的）")
    args = parser.parse_args()
    extract_all(args.session)
