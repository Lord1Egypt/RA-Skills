#!/usr/bin/env python3
"""
ultra-memory: 结构化事实提取引擎 (Evolution Engine Phase 1)
从操作日志中提取 (subject, predicate, object) 三元组结构化事实，
写入 evolution/facts.jsonl。

与 extract_entities.py 的关系：
  实体层(entity)回答"什么名字/哪个文件/哪个函数"
  事实层(fact)回答"它做什么/它依赖什么/它的行为是什么"

事实提取不依赖 LLM API，使用正则谓词模式 + 统计共现计算置信度。

被 log_op.py 在每次写入后异步调用（subprocess.Popen，背景执行，不阻塞主流程）。
"""

import os
import sys
import re
import json
import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# ── 谓词模式目录 ────────────────────────────────────────────────────────────
# 每个条目：(compiled_regex, predicate_label, source_type_filter_or_None)
# regex 必须包含 named group: (?P<subj>...) 和 (?P<obj>...)
# source_type_filter: None 表示所有类型都匹配

PREDICATE_PATTERNS = [
    # 行为/方法类谓词
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:fill|fills|filling)\s+(?:null|nuls?)\s+with\s+(?P<obj>.+)', re.IGNORECASE),
     "fills_nulls_with", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:return|returns|returning)\s+(?P<obj>.+)', re.IGNORECASE),
     "returns", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:use|uses|using)\s+(?P<obj>.+)', re.IGNORECASE),
     "uses", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:accept|accepts|accepting)\s+(?P<obj>.+)', re.IGNORECASE),
     "accepts", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:raise|raises|raising)\s+(?P<obj>.+)', re.IGNORECASE),
     "raises", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:skip|skips|skipping)\s+(?P<obj>.+)', re.IGNORECASE),
     "skips", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:block|blocks|blocking)\s+(?P<obj>.+)', re.IGNORECASE),
     "blocks", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:fail|fails|failing)\s+(?:when|if|on)?\s*(?P<obj>.+)', re.IGNORECASE),
     "fails_on", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:parse|parses|parsing)\s+(?P<obj>.+)', re.IGNORECASE),
     "parses", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:export|exports|exporting)\s+(?P<obj>.+)', re.IGNORECASE),
     "exports", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:validate|validates|validating)\s+(?P<obj>.+)', re.IGNORECASE),
     "validates", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:encode|encodes|encoding)\s+(?P<obj>.+)', re.IGNORECASE),
     "encodes", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:decode|decodes|decoding)\s+(?P<obj>.+)', re.IGNORECASE),
     "decodes", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:read|reads|reading)\s+(?P<obj>.+)', re.IGNORECASE),
     "reads", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:write|writes|writing)\s+(?P<obj>.+)', re.IGNORECASE),
     "writes", None),

    # 依赖类谓词
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:depend|depends|depending)\s+on\s+(?P<obj>.+)', re.IGNORECASE),
     "depends_on", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:require|requires|requiring)\s+(?P<obj>.+)', re.IGNORECASE),
     "requires", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:install|installs|installing)\s+(?P<obj>.+)', re.IGNORECASE),
     "installed_as", "bash_exec"),

    # 配置/设置类谓词
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:set|sets|setting)\s+(?P<obj>.+)', re.IGNORECASE),
     "sets", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:default|defaults?)\s+(?:is|are)?\s*(?P<obj>.+)', re.IGNORECASE),
     "defaults_to", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:enabled|disabled)\s+by\s+(?P<obj>.+)', re.IGNORECASE),
     "enabled_by", None),
    (re.compile(r'(?P<subj>\b[\w\.]+)\s+(?:config|configure|configures)\s+(?P<obj>.+)', re.IGNORECASE),
     "configured_as", None),

    # 用户偏好/行为类谓词（从 summary 推断）
    (re.compile(r'用户[以]?\s*(?:prefer|prefers|倾向|喜欢)\s+(?P<obj>\w.+)', re.IGNORECASE),
     "user_prefers", None),
    (re.compile(r'用户[以]?\s*(?:not|不想|不愿意|不要)\s+(?P<obj>\w.+)', re.IGNORECASE),
     "user_avoids", None),
    (re.compile(r'采用[了]?\s+(?P<obj>\w.+)', re.IGNORECASE),
     "adopted", None),
    (re.compile(r'选择[了]?\s+(?P<subj>\w.+)', re.IGNORECASE),
     "chose", None),
]

# 数值占位符和路径占位符（用于 object 归一化）
NUMERIC_PLACEHOLDER = re.compile(r'\b\d+\.?\d*\b')
PATH_PLACEHOLDER = re.compile(r'[/\\]?[a-zA-Z0-9_\-\.]+\.(py|js|ts|jsx|tsx|vue|json|yaml|yml|md|sql|sh|go|rs|java|rb|toml)')

# ── 工具函数 ────────────────────────────────────────────────────────────────


def normalize_object(obj: str) -> str:
    """归一化 object 字符串：替换数字/路径为占位符，小写化"""
    obj = obj.lower().strip()
    obj = NUMERIC_PLACEHOLDER.sub('<NUM>', obj)
    obj = PATH_PLACEHOLDER.sub('<PATH>', obj)
    obj = re.sub(r'\s+', ' ', obj)
    return obj


def compute_fact_id(subject: str, predicate: str, obj: str) -> str:
    """确定性 fact_id：SHA1(subject + predicate + object) 的前12位十六进制"""
    raw = f"{subject}\x00{predicate}\x00{obj}"
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ── 主体提取 ────────────────────────────────────────────────────────────────


_FUNC_DEF_PATTERN = re.compile(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]+)', re.MULTILINE)
_FILE_EXT_PATTERN = re.compile(
    r'\b([a-zA-Z0-9_\-\.]+/)*[a-zA-Z0-9_\-\.]+\.(py|js|ts|jsx|tsx|vue|html|css|json|yaml|yml|toml|md|sql|sh|go|rs|java|rb|php|cpp|c|h)\b',
    re.IGNORECASE
)


def extract_subject_from_op(op: dict) -> str | None:
    """
    从 op 中提取最适格的主体（subject）：
    优先顺序：function def > file path > detail.path > bash command verb
    """
    summary = op.get("summary", "")
    detail = op.get("detail", {})
    combined = summary + " " + json.dumps(detail, ensure_ascii=False)

    # 1. def function_name → 取 function name
    def_match = _FUNC_DEF_PATTERN.search(combined)
    if def_match:
        return def_match.group(1)

    # 2. 文件路径（detail.path 最准确）
    file_path = detail.get("path", "")
    if file_path:
        name = Path(file_path).name
        if name:
            return name

    # 3. 文本中的文件路径
    file_match = _FILE_EXT_PATTERN.search(combined)
    if file_match:
        name = Path(file_match.group(0)).name
        if name:
            return name

    # 4. bash 命令第一个实词
    if op.get("type") == "bash_exec":
        cmd = detail.get("cmd", summary)
        words = cmd.strip().split()
        if len(words) >= 2:
            # e.g. "python clean_df.py" → "clean_df"
            second = words[1]
            if not second.startswith("-"):
                return Path(second).stem or second

    return None


# ── 核心提取逻辑 ───────────────────────────────────────────────────────────


def extract_facts_from_op(op: dict) -> list[dict]:
    """
    从单条操作记录中提取结构化事实三元组。

    返回格式：
    {
        "fact_id": "fct_<sha12hex>",
        "ts": "...",
        "session_id": "sess_xxx",
        "op_seq": 42,
        "subject": "clean_df",
        "predicate": "fills_nulls_with",
        "object": "empty string for text, 0 for numeric",
        "confidence": 0.7,
        "source_summary": "...",
        "source_type": "file_write|...",
        "tags": [...],
        "contradiction_count": 0,
        "last_accessed": "...",
        "access_count": 1,
        "status": "active",
        "expires_at": None
    }
    """
    facts = []
    summary = op.get("summary", "")
    detail = op.get("detail", {})
    op_type = op.get("type", "")
    ts = op.get("ts", "")
    seq = op.get("seq", 0)
    tags = op.get("tags", [])
    session = op.get("_session_id", "")

    combined_text = summary + " " + json.dumps(detail, ensure_ascii=False)

    # 从 op 中提取主体
    subject = extract_subject_from_op(op)
    if not subject:
        return []

    # 遍历谓词模式
    for pattern, predicate, type_filter in PREDICATE_PATTERNS:
        if type_filter and op_type != type_filter:
            continue

        for match in pattern.finditer(combined_text):
            obj = match.group("obj").strip()
            if not obj or len(obj) < 2:
                continue

            fact_id = compute_fact_id(subject, predicate, obj)

            # 基础置信度（模式匹配 = 0.7）
            base_confidence = 0.7

            # 如果 op_type 是 decision/user_instruction，置信度略高
            if op_type in ("decision", "user_instruction"):
                base_confidence = 0.8
            elif op_type == "milestone":
                base_confidence = 0.85

            fact = {
                "fact_id": f"fct_{fact_id}",
                "ts": ts,
                "session_id": session,
                "op_seq": seq,
                "subject": subject,
                "predicate": predicate,
                "object": obj,
                "confidence": base_confidence,
                "source_summary": summary[:100],
                "source_type": op_type,
                "tags": tags[:3] if tags else [],
                "contradiction_count": 0,
                "last_accessed": ts,
                "access_count": 1,
                "status": "active",
                "expires_at": None,
            }
            facts.append(fact)

    return facts


def _load_existing_facts() -> list[dict]:
    """加载所有已存在的 facts"""
    facts_file = ULTRA_MEMORY_HOME / "evolution" / "facts.jsonl"
    if not facts_file.exists():
        return []
    facts = []
    with open(facts_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                facts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return facts


def _cooccurrence_confidence(subject: str, predicate: str, existing_facts: list[dict]) -> float:
    """
    统计共现置信度：
    同一 (subject, predicate) 出现多次，object 越一致 → 置信度越高。
    """
    candidates = [
        f for f in existing_facts
        if f.get("subject") == subject
        and f.get("predicate") == predicate
    ]
    if len(candidates) < 2:
        return 0.7  # 初始值

    object_normalized = [normalize_object(f.get("object", "")) for f in candidates]
    counter = Counter(object_normalized)
    dominant_count = counter.most_common(1)[0][1]
    total = len(object_normalized)

    # 1 - (冲突数 / 总数)
    conflict_ratio = 1 - (dominant_count / total)
    return max(0.5, 1.0 - conflict_ratio)


# ── 存储 ────────────────────────────────────────────────────────────────────


def append_facts(facts: list[dict], session_id: str):
    """将提取的事实追加写入 evolution/facts.jsonl"""
    if not facts:
        return

    evolution_dir = ULTRA_MEMORY_HOME / "evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)
    facts_file = evolution_dir / "facts.jsonl"

    for fact in facts:
        if not fact.get("session_id"):
            fact["session_id"] = session_id

    with open(facts_file, "a", encoding="utf-8") as f:
        for fact in facts:
            f.write(json.dumps(fact, ensure_ascii=False) + "\n")


# ── 矛盾检测触发 ───────────────────────────────────────────────────────────


def trigger_contradiction_detection(session_id: str, fact_ids: list[str]):
    """
    以背景进程触发矛盾检测。
    检测完成后自动更新 fact_metadata.json。
    """
    try:
        scripts_dir = Path(__file__).parent
        python = sys.executable
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(
            [python, str(scripts_dir / "detect_contradictions.py"),
             "--session", session_id,
             "--new-fact-ids"] + fact_ids,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            startupinfo=startupinfo,
        )
    except Exception:
        pass  # 矛盾检测失败静默跳过


# ── 主入口 ─────────────────────────────────────────────────────────────────


def extract_and_store(session_id: str, op: dict) -> list[dict]:
    """
    对单条操作提取事实并写入 facts.jsonl。
    供 log_op.py 调用（同步模式，用于测试）。
    """
    op["_session_id"] = session_id
    facts = extract_facts_from_op(op)
    if facts:
        append_facts(facts, session_id)
        # 触发矛盾检测（背景）
        fact_ids = [f["fact_id"] for f in facts]
        trigger_contradiction_detection(session_id, fact_ids)
    return facts


def extract_batch(session_id: str, op_seq: int | None = None):
    """
    批量提取：读取 ops.jsonl 中指定 op_seq 或全部未处理记录。
    --batch 模式使用。
    """
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        print(f"[ultra-memory] ⚠️  ops.jsonl 不存在: {session_id}")
        return

    existing_facts = _load_existing_facts()

    # 找出已提取的 op_seq 集合
    existing_seqs = {
        f.get("op_seq") for f in existing_facts
        if f.get("session_id") == session_id
    }

    all_ops = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                op = json.loads(line)
                all_ops.append(op)
            except json.JSONDecodeError:
                continue

    # 过滤未处理的 ops
    if op_seq is not None:
        to_process = [op for op in all_ops if op.get("seq") == op_seq]
    else:
        to_process = [op for op in all_ops if op.get("seq") not in existing_seqs]

    if not to_process:
        print(f"[ultra-memory] ✅ 无新事实可提取 (session: {session_id})")
        return

    all_new_facts = []
    for op in to_process:
        op["_session_id"] = session_id
        facts = extract_facts_from_op(op)
        for fact in facts:
            # 使用共现置信度更新
            cooc_conf = _cooccurrence_confidence(
                fact["subject"], fact["predicate"], existing_facts + all_new_facts
            )
            fact["confidence"] = round(
                (fact["confidence"] * 0.5 + cooc_conf * 0.5), 2
            )
            all_new_facts.append(fact)

    if all_new_facts:
        append_facts(all_new_facts, session_id)
        fact_ids = [f["fact_id"] for f in all_new_facts]
        trigger_contradiction_detection(session_id, fact_ids)
        print(f"[ultra-memory] ✅ 事实提取完成 (session: {session_id})")
        print(f"  新增 {len(all_new_facts)} 条事实")
    else:
        print(f"[ultra-memory] ✅ 无新事实可提取 (session: {session_id})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="从操作日志提取结构化事实三元组 (subject, predicate, object)"
    )
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument(
        "--op-seq", type=int, default=None,
        help="只提取指定 seq 的操作（省略则批量提取未处理的）"
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="批量提取：扫描整个 ops.jsonl"
    )
    args = parser.parse_args()

    extract_batch(args.session, args.op_seq if not args.batch else None)

    if args.batch:
        # 全量扫描后触发矛盾检测
        evolution_dir = ULTRA_MEMORY_HOME / "evolution"
        evolution_dir.mkdir(parents=True, exist_ok=True)
        detect_script = Path(__file__).parent / "detect_contradictions.py"
        if detect_script.exists():
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.Popen(
                    [sys.executable, str(detect_script),
                     "--session", args.session, "--batch"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    startupinfo=startupinfo,
                )
            except Exception:
                pass
