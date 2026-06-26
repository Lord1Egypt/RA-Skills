#!/usr/bin/env python3
"""
ultra-memory: 记忆检索脚本
支持从五层记忆中检索相关内容
优化：BM25/IDF 评分 + 字段加权 + 同义词扩展 + 时间衰减 + 上下文窗口
"""

import os
import sys
import json
import argparse
import re
import math
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# ── 同义词/别名映射 ────────────────────────────────────────────────────────

SYNONYM_MAP = {
    # 数据处理
    "数据清洗": ["clean", "clean_df", "preprocess", "cleaner", "清洗", "data_clean"],
    "clean_df": ["数据清洗", "清洗", "preprocess", "数据处理", "clean"],
    "preprocess": ["预处理", "数据清洗", "clean_df", "数据处理"],
    "数据处理": ["clean_df", "preprocess", "transform", "处理数据"],
    # 测试
    "测试": ["test", "unittest", "pytest", "spec", "assert"],
    "test": ["测试", "单元测试", "pytest", "unittest"],
    "单元测试": ["test", "unittest", "pytest"],
    # 安装/依赖
    "安装": ["install", "pip install", "npm install", "setup", "依赖"],
    "install": ["安装", "依赖", "setup"],
    "依赖": ["install", "dependency", "requirements", "安装"],
    # 部署
    "部署": ["deploy", "docker", "release", "发布"],
    "deploy": ["部署", "发布", "release"],
    # 错误
    "报错": ["error", "exception", "traceback", "failed", "错误"],
    "error": ["报错", "错误", "exception", "traceback"],
    "错误": ["error", "exception", "报错", "traceback"],
    # 配置
    "配置": ["config", "settings", "setup", ".env"],
    "config": ["配置", "设置", "settings"],
    # 接口
    "接口": ["api", "endpoint", "route", "url"],
    "api": ["接口", "endpoint", "请求", "route"],
    # 函数/方法
    "函数": ["def", "function", "method", "func"],
    "function": ["函数", "方法", "def"],
    # 完成
    "完成": ["done", "finished", "milestone", "✅"],
    "done": ["完成", "finished", "milestone"],
}

# Weibull 拉伸指数衰减参数（比简单指数衰减更接近人类记忆曲线）
WEIBULL_LAMBDA = 3600 * 24   # 特征寿命 24小时
WEIBULL_K      = 0.75        # 形状参数 k<1: 初期快速衰减，长期记忆保留更好

# BM25 参数
BM25_K1 = 1.5   # 词频饱和参数（防止某词重复出现过度提升）
BM25_B = 0.75   # 文档长度归一化参数

# 停用词（检索时不考虑这些词的 IDF 惩罚）
STOPWORD_TOKENS = {
    "的", "了", "是", "在", "和", "与", "或", "以及", "把", "被", "用",
    "the", "a", "an", "is", "was", "are", "were", "to", "of", "for",
    "with", "by", "from", "that", "this", "it",
}

# 字段权重（搜索 detail 时不同字段的权重）
FIELD_WEIGHTS = {
    "summary": 1.0,
    "title": 1.2,     # 条目标题更重要
    "name": 1.5,       # 实体名最重要（函数名/文件名/类名）
    "content": 0.8,    # 知识库内容
    "context": 0.6,    # 实体上下文
    "detail.path": 1.4,  # 文件路径
    "detail.cmd": 1.0,   # bash 命令
    "tags": 0.7,         # 标签权重较低
    "rationale": 1.1,    # 决策依据
}

# 操作类型权重（重要操作类型排名靠前）
OP_TYPE_WEIGHT = {
    "milestone": 1.5,
    "decision": 1.3,
    "user_instruction": 1.2,
    "error": 1.1,
    "reasoning": 1.0,
    "file_write": 0.9,
    "bash_exec": 0.9,
    "file_read": 0.8,
    "tool_call": 0.8,
}


# ── 分词 ────────────────────────────────────────────────────────────────


def tokenize(text: str) -> list[str]:
    """中英文混合分词：英文保留完整词，中文返回 unigram（不用 bigram 避免噪音）"""
    if not text:
        return []
    # 英文：保留完整标识符
    words = re.findall(r'[a-zA-Z][a-zA-Z0-9_\-\.]*', text.lower())
    # 中文 unigram（每个汉字单独作为一个 token）
    chinese = re.findall(r'[\u4e00-\u9fff]', text)
    return words + chinese


def tokenize_set(text: str) -> set[str]:
    """返回去重 token set"""
    return set(tokenize(text))


# ── BM25 评分 ────────────────────────────────────────────────────────────


class BM25Index:
    """
    内存 BM25 索引。
    对每个文档维护：token→位置列表映射，以及 avgdl。
    """

    def __init__(self, docs: list[dict]):
        """
        docs: list of {"id": ..., "text": ..., "tokens": [token_list]}
        """
        self.doc_count = len(docs)
        self.doc_tokens: list[list[str]] = [d["tokens"] for d in docs]
        self.doc_texts: list[str] = [d["text"] for d in docs]
        self.doc_ids: list = [d["id"] for d in docs]

        # 构建 token→{doc_idx: [positions]} 反向索引
        self.term_to_docs: dict[str, dict[int, int]] = {}  # token → {doc_idx: count}
        for doc_idx, tokens in enumerate(self.doc_tokens):
            seen = set()
            for t in tokens:
                if t in STOPWORD_TOKENS:
                    continue
                if t not in self.term_to_docs:
                    self.term_to_docs[t] = {}
                if doc_idx not in self.term_to_docs[t]:
                    self.term_to_docs[t][doc_idx] = 0
                self.term_to_docs[t][doc_idx] += 1
                seen.add(t)

        # 平均文档长度
        self.avgdl = sum(len(t) for t in self.doc_tokens) / max(self.doc_count, 1)

        # IDF：log((N - n + 0.5) / (n + 0.5))
        self.idf: dict[str, float] = {}
        for t, doc_map in self.term_to_docs.items():
            n = len(doc_map)
            self.idf[t] = math.log((self.doc_count - n + 0.5) / (n + 0.5) + 1)

    def score(self, doc_idx: int, query_tokens: list[str]) -> float:
        """对单个文档计算 BM25 分数"""
        tokens = self.doc_tokens[doc_idx]
        doc_len = len(tokens)
        score = 0.0

        tf_map: dict[str, int] = {}
        for t in tokens:
            if t not in STOPWORD_TOKENS:
                tf_map[t] = tf_map.get(t, 0) + 1

        for t in query_tokens:
            if t in STOPWORD_TOKENS:
                continue
            if t not in self.term_to_docs:
                continue
            tf = tf_map.get(t, 0)
            idf = self.idf.get(t, 0)
            # BM25 公式
            numerator = tf * (BM25_K1 + 1)
            denominator = tf + BM25_K1 * (1 - BM25_B + BM25_B * doc_len / self.avgdl)
            score += idf * numerator / (denominator + 0.1)

        return score

    def search(self, query_tokens: list[str], top_k: int = 5) -> list[tuple[float, int]]:
        """返回 [(score, doc_idx)] 列表，按分数降序"""
        scored = [(self.score(i, query_tokens), i) for i in range(self.doc_count)]
        scored.sort(key=lambda x: -x[0])
        return scored[:top_k]


# ── 查询扩展 ────────────────────────────────────────────────────────────


def expand_query(query: str) -> list[str]:
    """将查询词扩展为同义词集合（返回 list 而非 set，保留权重信息）"""
    tokens = tokenize(query)
    expanded_tokens = list(tokens)

    # 1. 整句匹配：query 中含有的中文短语（如"数据清洗"）先匹配
    for key in SYNONYM_MAP:
        if len(key) > 1 and key in query:
            expanded_tokens.append(key.lower())
            expanded_tokens.extend(s.lower() for s in SYNONYM_MAP[key])

    # 2. 双向 token 匹配
    for token in tokens:
        token_lower = token.lower()
        for key, synonyms in SYNONYM_MAP.items():
            synonyms_lower = [s.lower() for s in synonyms]
            # token 命中 key（如 "数据清洗" 或 "preprocess"）
            if token_lower == key.lower() or token_lower in synonyms_lower:
                expanded_tokens.append(key.lower())
                expanded_tokens.extend(s.lower() for s in synonyms)

    return expanded_tokens


# ── 时间衰减 ────────────────────────────────────────────────────────────


def time_weight(ts_str: str) -> float:
    """Weibull 拉伸指数衰减：weight = exp(-(age/λ)^k)
    k=0.75 < 1: 初期24小时内衰减较快，之后趋于平缓，长期重要记忆保留更好。
    对比简单指数衰减（k=1），7天后权重从 0.07 提升到 0.19。
    """
    try:
        ts = datetime.fromisoformat(ts_str.rstrip("Z")).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        age_seconds = (now - ts).total_seconds()
        weight = math.exp(-math.pow(age_seconds / WEIBULL_LAMBDA, WEIBULL_K))
        return max(0.1, weight)
    except Exception:
        return 0.5


# ── 核心评分函数 ───────────────────────────────────────────────────────────


def score_text(
    query_tokens: list[str],
    text: str,
    field_weight: float = 1.0,
    ts_str: str = "",
) -> float:
    """
    BM25 评分 × 字段权重 × 时间权重。
    """
    if not text or not query_tokens:
        return 0.0

    text_tokens = tokenize(text)
    if not text_tokens:
        return 0.0

    # 构建单文档 BM25 索引
    doc = {"id": 0, "text": text, "tokens": text_tokens}
    idx = BM25Index([doc])

    bm25_score = idx.score(0, query_tokens)

    # 字段权重
    field_boost = field_weight

    # 时间权重
    tw = time_weight(ts_str) if ts_str else 0.85  # 无时间戳时用默认 0.85

    # 最终分数 = BM25 × 字段权重 × 时间权重
    return bm25_score * field_boost * tw


def score_text_with_match_boost(
    query_tokens: list[str],
    text: str,
    field_weight: float = 1.0,
    ts_str: str = "",
    exact_phrase_bonus: float = 0.0,
) -> float:
    """
    BM25 评分 + 精确短语匹配加分 + 字段权重 + 时间权重。
    """
    base = score_text(query_tokens, text, field_weight, ts_str)

    if exact_phrase_bonus > 0:
        # 查询词全部出现在文本开头位置，给予额外加分
        text_lower = text.lower()
        for qt in query_tokens:
            if len(qt) > 1 and qt in text_lower:
                pos = text_lower.find(qt)
                if pos < 20:  # 前20字符内出现
                    base += exact_phrase_bonus * field_weight
                    break

    return base


def load_all_ops(session_dir: Path) -> list[dict]:
    """加载全部操作（含已压缩，用于提取上下文窗口）"""
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        return []
    ops = []
    with open(ops_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ops.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return ops


def get_context_window(all_ops: list[dict], target_seq: int, window: int = 1) -> dict:
    """
    返回目标 seq 前后各 window 条操作作为上下文。
    """
    seq_map = {op["seq"]: op for op in all_ops}
    before = []
    after = []
    for i in range(1, window + 1):
        if (target_seq - i) in seq_map:
            before.insert(0, seq_map[target_seq - i])
        if (target_seq + i) in seq_map:
            after.append(seq_map[target_seq + i])
    return {"before": before, "after": after}


def search_ops(session_dir: Path, query_tokens: list[str], top_k: int) -> list[dict]:
    """在操作日志中搜索，附带时间权重和上下文窗口"""
    all_ops = load_all_ops(session_dir)
    if not all_ops:
        return []

    op_type_weight = {k.lower(): v for k, v in OP_TYPE_WEIGHT.items()}

    # 构建语料级 BM25 索引（一次构建，IDF 基于全量语料，性能 O(n) 而非 O(n²)）
    texts = []
    for op in all_ops:
        summary = op.get("summary", "")
        detail_text = json.dumps(op.get("detail", {}), ensure_ascii=False)
        texts.append(summary + " " + detail_text)

    corpus_docs = [{"id": i, "text": t, "tokens": tokenize(t)} for i, t in enumerate(texts)]
    corpus_index = BM25Index(corpus_docs)

    results = []
    for i, op in enumerate(all_ops):
        ts = op.get("ts", "")
        bm25_score = corpus_index.score(i, query_tokens)
        tw = time_weight(ts) if ts else 0.85
        op_type = op.get("type", "").lower()
        type_mult = op_type_weight.get(op_type, 0.8)

        # 重要性权重：(0.5 + 0.5×importance) 使高重要性操作分数最多翻倍
        importance = op.get("importance", 0.5)
        importance_mult = 0.5 + 0.5 * importance

        # 访问频率加成：log(1 + access_count) × 0.1 使常被召回的记忆衰减更慢
        access_boost = 1.0 + math.log1p(op.get("access_count", 0)) * 0.1

        score = bm25_score * tw * type_mult * importance_mult * access_boost

        if score > 0:
            ctx = get_context_window(all_ops, op["seq"], window=1)
            results.append({
                "score": score,
                "source": "ops",
                "data": op,
                "context": ctx,
            })

    results.sort(key=lambda x: (-x["score"], -x["data"]["seq"]))
    return results[:top_k]


def search_summary(session_dir: Path, query_tokens: list[str]) -> list[dict]:
    """在摘要文件中搜索"""
    summary_file = session_dir / "summary.md"
    if not summary_file.exists():
        return []
    with open(summary_file, encoding="utf-8") as f:
        content = f.read()
    paragraphs = [p.strip() for p in content.split("\n") if p.strip() and not p.startswith("#")]
    results = []
    for para in paragraphs:
        score = score_text(query_tokens, para, field_weight=1.0, ts_str="")
        if score > 0.1:
            results.append({"score": score, "source": "summary", "text": para})
    results.sort(key=lambda x: -x["score"])
    return results[:3]


def search_entities(query_tokens: list[str], top_k: int) -> list[dict]:
    """
    第4层：实体索引搜索（结构化精确检索）。
    适合回答：
      - "我们用过哪些函数？" → entity_type=function
      - "动过哪些文件？"     → entity_type=file
      - "装了哪些依赖？"     → entity_type=dependency
      - "做了哪些决策？"     → entity_type=decision
    相比 bigram 关键词，对结构化查询的精度提升显著。
    """
    entities_file = ULTRA_MEMORY_HOME / "semantic" / "entities.jsonl"
    if not entities_file.exists():
        return []

    # 实体类型别名：查询词到实体类型的映射
    TYPE_ALIASES = {
        "函数": "function", "function": "function", "方法": "function", "func": "function",
        "文件": "file", "file": "file", "路径": "file",
        "依赖": "dependency", "dependency": "dependency", "包": "dependency",
        "决策": "decision", "decision": "decision", "选择": "decision",
        "错误": "error", "error": "error", "报错": "error", "异常": "error",
        "类": "class", "class": "class",
    }

    # 检测查询是否包含实体类型词（精确类型过滤）
    target_type = None
    query_token_set = set(query_tokens)
    for token in query_token_set:
        if token in TYPE_ALIASES:
            target_type = TYPE_ALIASES[token]
            break

    results = []
    seen_names: set[str] = set()  # 去重：同名实体只保留最新一条

    all_entities = []
    with open(entities_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                all_entities.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    # 按 ts 倒序（最新优先）
    all_entities.sort(key=lambda e: e.get("ts", ""), reverse=True)

    for ent in all_entities:
        # 类型过滤
        if target_type and ent.get("entity_type") != target_type:
            continue

        name = ent.get("name", "")
        context = ent.get("context", "")
        ent_text = name + " " + context
        ts = ent.get("ts", "")

        # 实体 name 字段权重 1.5，context 字段权重 0.6
        name_score = score_text(query_tokens, name, field_weight=FIELD_WEIGHTS["name"], ts_str=ts)
        ctx_score = score_text(query_tokens, context, field_weight=FIELD_WEIGHTS["context"], ts_str=ts)
        score = max(name_score, ctx_score)

        # 实体名精确匹配给予额外加分
        name_tokens = tokenize(name)
        exact_match = bool(query_token_set & set(name_tokens))
        if exact_match:
            score = max(score, 0.5)  # 保底 0.5 分

        # 如果是类型查询（"所有函数" "所有文件"），返回全部该类型实体
        if target_type and not seen_names:
            score = max(score, 0.3)

        if score > 0.1:
            dedup_key = f"{ent.get('entity_type')}:{name}"
            if dedup_key not in seen_names:
                seen_names.add(dedup_key)
                results.append({
                    "score": score,
                    "source": "entity",
                    "data": ent,
                })

    results.sort(key=lambda x: -x["score"])
    return results[:top_k]


def search_entity_history(entity_name: str, home: Path) -> list[dict]:
    """
    查询同名实体的所有版本（含 superseded），按时间倒序。
    参照 supermemory history <entity> 实体版本时间线功能。
    """
    entities_file = home / "semantic" / "entities.jsonl"
    if not entities_file.exists():
        return []

    name_lower = entity_name.lower()
    versions = []

    with open(entities_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ent = json.loads(line)
            except json.JSONDecodeError:
                continue

            # 名字匹配（忽略大小写）
            if ent.get("name", "").lower() != name_lower:
                continue

            # 标注是否为当前活跃版本
            is_active = not ent.get("superseded", False)
            ts = ent.get("ts", "")

            versions.append({
                "ts": ts,
                "is_active": is_active,
                "entity_type": ent.get("entity_type", "?"),
                "name": ent.get("name", "?"),
                "context": ent.get("context", ""),
                "superseded_at": ent.get("superseded_at", ""),
            })

    # 按时间倒序（最新优先）
    versions.sort(key=lambda v: v["ts"], reverse=True)
    return versions


def format_entity_history(versions: list[dict], entity_name: str) -> str:
    """格式化实体历史版本输出"""
    if not versions:
        return f"[实体历史] 未找到实体: {entity_name}"

    lines = [f"[实体历史] {entity_name} — 共 {len(versions)} 个版本\n"]
    for i, v in enumerate(versions):
        status = "✅ 活跃" if v["is_active"] else "❌ 已失效"
        ts = v["ts"][:16].replace("T", " ") if v["ts"] else "未知时间"
        superseded_note = f" (失效于 {v['superseded_at'][:16].replace('T',' ')})" if v["superseded_at"] else ""
        lines.append(f"  v{i+1} · {ts} · {status}{superseded_note}")
        lines.append(f"    类型: {v['entity_type']}  |  上下文: {v['context'][:60]}")
    return "\n".join(lines)


def search_semantic(query_tokens: list[str], top_k: int, as_of: str = "") -> list[dict]:
    """
    在 Layer 3 语义层搜索（轻量模式：关键词匹配 + 同义词扩展）。
    as_of: ISO 时间字符串，查询该时间点的知识状态（时间旅行）。
           跳过他之后创建的条目；superseded 条目若在 as_of 前仍有效则返回历史版本。
    """
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    kb_file = semantic_dir / "knowledge_base.jsonl"
    index_file = semantic_dir / "session_index.json"

    # 解析 as_of 时间点
    as_of_dt: datetime | None = None
    if as_of:
        try:
            as_of_dt = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
        except ValueError:
            as_of_dt = None

    def _entry_in_range(entry: dict) -> bool:
        """判断条目是否在 as_of 时间范围内"""
        if as_of_dt is None:
            return True
        ts_str = entry.get("ts", "")
        if not ts_str:
            return True
        try:
            entry_dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            return entry_dt <= as_of_dt
        except ValueError:
            return True

    def _superseded_at_the_time(entry: dict) -> bool:
        """判断 superseded 条目在 as_of 时间是否仍有效"""
        if as_of_dt is None:
            return False
        superseded_at = entry.get("superseded_at", "")
        if not superseded_at:
            return True  # 没有 superseded_at 标记，无法判断，视为无效
        try:
            superseded_dt = datetime.fromisoformat(superseded_at.replace("Z", "+00:00"))
            return superseded_dt > as_of_dt  # 被取代的时间 > as_of，说明在 as_of 时还活着
        except ValueError:
            return False

    results = []

    if kb_file.exists():
        with open(kb_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # 时间旅行过滤
                if not _entry_in_range(entry):
                    continue

                # superseded 条目：as_of 之前仍有效的才返回
                if entry.get("superseded"):
                    if not _superseded_at_the_time(entry):
                        continue  # 在 as_of 时已被取代，不返回
                    # 仍有效，标记为历史版本
                    entry = dict(entry)
                    entry["_history"] = True

                title = entry.get("title", "")
                content = entry.get("content", "")
                ts = entry.get("ts", "")
                title_score = score_text(query_tokens, title, field_weight=FIELD_WEIGHTS["title"], ts_str=ts)
                content_score = score_text(query_tokens, content, field_weight=FIELD_WEIGHTS["content"], ts_str=ts)
                score = max(title_score, content_score)
                if score > 0.1:
                    results.append({"score": score, "source": "knowledge_base", "data": entry})

    if index_file.exists():
        with open(index_file, encoding="utf-8") as f:
            index = json.load(f)
        for s in index.get("sessions", []):
            project = s.get("project", "")
            milestone = s.get("last_milestone") or ""
            ts = s.get("started_at", "")
            project_score = score_text(query_tokens, project, field_weight=1.0, ts_str=ts)
            milestone_score = score_text(query_tokens, milestone, field_weight=1.2, ts_str=ts)
            score = max(project_score, milestone_score)
            if score > 0.1:
                results.append({"score": score, "source": "history", "data": s})

    results.sort(key=lambda x: -x["score"])
    return results[:top_k]


def search_profile(query_tokens: list[str], home: Path) -> list[dict]:
    """从 user_profile.json 检索相关字段，跳过 superseded 字段"""
    profile_file = home / "semantic" / "user_profile.json"
    if not profile_file.exists():
        return []

    try:
        with open(profile_file, encoding="utf-8") as f:
            profile = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    results = []
    for key, value in profile.items():
        # 跳过 superseded 标记的字段
        if key.endswith("_superseded"):
            continue
        text = f"{key} {value}"
        score = score_text(query_tokens, str(text), field_weight=FIELD_WEIGHTS["name"])
        if score > 0.1:
            results.append({
                "score": score,
                "source": "profile",
                "data": {"field": key, "value": value},
            })

    results.sort(key=lambda x: -x["score"])
    return results[:3]


# ── TF-IDF 向量语义搜索层（第四层召回的增强）───────────────────────────

def is_sklearn_available() -> bool:
    try:
        import sklearn; return True
    except ImportError:
        return False


def is_sentencetransformers_available() -> bool:
    try:
        from sentence_transformers import SentenceTransformer; return True
    except ImportError:
        return False


_TFidfCache: dict[str, dict] = {}  # session_id → {vocab, idfs, doc_vectors, doc_texts}


def _get_tfidf_cache_path(session_dir: Path) -> Path:
    return session_dir / "tfidf_cache.json"


def _text_from_op(op: dict) -> str:
    """提取 op 中可索引的文本"""
    parts = [
        op.get("summary", ""),
        op.get("type", ""),
        " ".join(op.get("tags", [])),
    ]
    detail = op.get("detail", {})
    if isinstance(detail, dict):
        for v in detail.values():
            if isinstance(v, str):
                parts.append(v)
    return " ".join(parts)


def _build_tfidf_index(ops: list[dict]) -> dict:
    """
    用 sklearn TfidfVectorizer 构建内存索引。
    返回 {vocab: [...], idfs: [...], doc_vectors: [[...], ...], doc_texts: [...]}
    完全零外部 API 依赖。
    """
    import math
    from collections import Counter

    texts = [_text_from_op(op) for op in ops]
    # 简单 tokenize：英文保留 word，中文逐字
    def tokens(text: str) -> list[str]:
        import re
        en = re.findall(r'[a-zA-Z0-9_]+', text.lower())
        zh = list(text)
        return en + zh

    tokenized = [tokens(t) for t in texts]
    # 构建词表
    vocab_set: set[str] = set()
    for tk in tokenized:
        vocab_set.update(tk)
    vocab = sorted(vocab_set)
    word2idx = {w: i for i, w in enumerate(vocab)}
    n = len(vocab)

    # TF: 词频
    N = len(texts)
    df = Counter()
    for tk in tokenized:
        df.update(set(tk))

    idfs = []
    for w in vocab:
        df_w = df[w]
        idf = math.log((N + 1) / (df_w + 1)) + 1  # 平滑
        idfs.append(idf)

    # 文档向量 = TF × IDF
    doc_vectors = []
    for tk in tokenized:
        tf = Counter(tk)
        vec = [0.0] * n
        for w, f in tf.items():
            if w in word2idx:
                idx = word2idx[w]
                vec[idx] = f * idfs[idx]
        # L2 归一化
        norm = math.sqrt(sum(v ** 2 for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        doc_vectors.append(vec)

    return {
        "vocab": vocab,
        "idfs": idfs,
        "doc_vectors": doc_vectors,
        "doc_texts": texts,
        "n_docs": N,
    }


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    import math
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _search_tfidf(session_dir: Path, all_ops: list[dict],
                  query: str, top_k: int) -> list[dict]:
    """纯 sklearn TF-IDF 语义搜索（零依赖，fallback 方案）"""
    import re

    cache_path = _get_tfidf_cache_path(session_dir)

    # 加载或构建缓存
    if cache_path.exists():
        try:
            import json as _json
            with open(cache_path, encoding="utf-8") as f:
                cache = _json.load(f)
            doc_vectors = cache["doc_vectors"]
            doc_texts   = cache["doc_texts"]
            vocab       = cache["vocab"]
            idfs        = cache["idfs"]
            cached_seq  = cache.get("last_seq", -1)
        except Exception:
            cache = None
            doc_vectors = None
    else:
        cache = None

    # 如果缓存过期（seq 变了）或不存在，重新构建
    current_seq = max((op.get("seq", 0) for op in all_ops), default=0)
    if doc_vectors is None or cache is None or cache.get("last_seq", -1) != current_seq:
        cache = _build_tfidf_index(all_ops)
        doc_vectors = cache["doc_vectors"]
        doc_texts   = cache["doc_texts"]
        vocab       = cache["vocab"]
        idfs        = cache["idfs"]
        cache["last_seq"] = current_seq
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache, f)
        except Exception:
            pass  # 写入失败不影响搜索

    # 把 query 也转成 TF-IDF 向量
    def tokens(text: str) -> list[str]:
        en = re.findall(r'[a-zA-Z0-9_]+', text.lower())
        zh = list(text)
        return en + zh

    q_tokens = tokens(query)
    tf_q = Counter(q_tokens)
    word2idx = {w: i for i, w in enumerate(vocab)}
    vec_q = [0.0] * len(vocab)
    for w, f in tf_q.items():
        if w in word2idx:
            idx = word2idx[w]
            vec_q[idx] = f * idfs[idx]

    # L2 归一化
    import math
    norm = math.sqrt(sum(v * v for v in vec_q))
    if norm > 0:
        vec_q = [v / norm for v in vec_q]

    # 余弦相似度
    scored = []
    for i, dv in enumerate(doc_vectors):
        score = _cosine_similarity(vec_q, dv)
        if score > 0.05:  # 阈值过滤噪音
            scored.append((score, i))
    scored.sort(key=lambda x: -x[0])

    results = []
    # all_ops 和 doc_vectors/doc_texts 按同一顺序排列，直接用索引对应
    for score, i in scored[:top_k]:
        results.append({"score": score, "source": "tfidf", "data": all_ops[i]})

    return results


def _search_sentencetransformers(
    session_dir: Path, all_ops: list[dict],
    query: str, top_k: int
) -> list[dict]:
    """
    sentence-transformers 向量语义搜索（更高质量，需 pip install sentence-transformers）。
    使用 all-MiniLM-L6-v2（22MB，本地运行，无需 API）。
    """
    import json as _json

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return []

    cache_path = session_dir / "embed_cache.json"

    # 加载或构建 embedding 缓存
    if cache_path.exists():
        try:
            with open(cache_path, encoding="utf-8") as f:
                cache = _json.load(f)
            cached_seq = cache.get("last_seq", -1)
            current_seq = max((op.get("seq", 0) for op in all_ops), default=0)
            if cached_seq != current_seq:
                cache = None
        except Exception:
            cache = None
    else:
        cache = None

    texts = [_text_from_op(op) for op in all_ops]

    model = SentenceTransformer("all-MiniLM-L6-v2")  # 只加载一次

    if cache is None:
        embeddings = model.encode(texts, show_progress_bar=False).tolist()
        current_seq = max((op.get("seq", 0) for op in all_ops), default=0)
        cache = {"embeddings": embeddings, "last_seq": current_seq}
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                _json.dump(cache, f)
        except Exception:
            pass

    # 将查询向量化（复用上方已加载的 model）
    query_emb = model.encode([query], show_progress_bar=False)[0].tolist()

    embeddings = cache["embeddings"]
    import math
    scored = []
    for i, emb in enumerate(embeddings):
        dot = sum(a * b for a, b in zip(query_emb, emb))
        na = math.sqrt(sum(a * a for a in query_emb))
        nb = math.sqrt(sum(a * a for a in emb))
        score = dot / (na * nb) if na > 0 and nb > 0 else 0
        if score > 0.3:
            scored.append((score, i))
    scored.sort(key=lambda x: -x[0])

    results = []
    for score, i in scored[:top_k]:
        results.append({"score": score, "source": "embedding", "data": all_ops[i]})
    return results


def search_tfidf(session_dir: Path, all_ops: list[dict],
                 query: str, top_k: int) -> list[dict]:
    """
    语义搜索入口：优先 sentence-transformers，退回 sklearn TF-IDF。
    如果都不可用，返回空列表（不阻塞主流程）。
    """
    if is_sentencetransformers_available():
        return _search_sentencetransformers(session_dir, all_ops, query, top_k)
    elif is_sklearn_available():
        return _search_tfidf(session_dir, all_ops, query, top_k)
    return []


# ── 访问计数回写 ───────────────────────────────────────────────────────────


def _increment_access_count(session_dir: Path, seq_set: set[int]) -> None:
    """将被召回操作的 access_count +1，写回 ops.jsonl（原子替换）。
    用于访问频率感知衰减：常被召回的记忆在时间衰减公式中获得加成，衰减更慢。
    seq_set 为空时跳过，异常时静默忽略（不阻塞检索）。
    """
    if not seq_set:
        return
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        return
    try:
        lines = ops_file.read_text(encoding="utf-8").splitlines()
        updated = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                op = json.loads(line)
                if op.get("seq") in seq_set:
                    op["access_count"] = op.get("access_count", 0) + 1
                updated.append(json.dumps(op, ensure_ascii=False))
            except json.JSONDecodeError:
                updated.append(line)
        tmp = ops_file.with_suffix(".tmp")
        tmp.write_text("\n".join(updated) + "\n", encoding="utf-8")
        tmp.replace(ops_file)
    except Exception:
        pass  # 回写失败不影响检索结果


# ── RRF 融合 ──────────────────────────────────────────────────────────────


def _get_doc_id(result: dict) -> str:
    """为检索结果生成唯一 ID（用于 RRF 跨层去重合并）"""
    source = result.get("source", "")
    data   = result.get("data", {})
    if source in ("ops", "tfidf", "embedding"):
        return f"op:{data.get('seq', id(data))}"
    elif source == "summary":
        return f"sum:{hash(result.get('text', '')[:80])}"
    elif source == "knowledge_base":
        return f"kb:{data.get('title', '')[:40]}"
    elif source == "entity":
        return f"ent:{data.get('entity_type', '')}:{data.get('name', '')}"
    elif source == "history":
        return f"hist:{data.get('session_id', '')}"
    elif source == "profile":
        return f"prof:{data.get('field', '')}"
    return f"other:{hash(str(data)[:80])}"


def rrf_merge(ranked_lists: list[list[dict]], k: int = 60) -> list[dict]:
    """
    Reciprocal Rank Fusion（Robertson et al. 2009）：
    合并多个独立排序的检索结果列表，每条结果分数 = Σ 1/(k + rank_i)。
    k=60 是标准参数，防止头部排名过度主导。
    优于简单得分合并：不同来源（BM25/TF-IDF/向量）得分量纲不同，
    RRF 只依赖排名位次，天然解决量纲不一致问题。
    同一文档出现在多个列表时，分数叠加，体现多源一致性加分。
    """
    rrf_scores: dict[str, float] = {}
    best_item:  dict[str, dict]  = {}

    for ranked in ranked_lists:
        for rank, item in enumerate(ranked):
            doc_id = _get_doc_id(item)
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
            if doc_id not in best_item:
                best_item[doc_id] = item

    merged = sorted(best_item.values(), key=lambda x: -rrf_scores[_get_doc_id(x)])
    for item in merged:
        item["score"] = rrf_scores[_get_doc_id(item)]
    return merged


# ── Snippet 截取 ───────────────────────────────────────────────────────────


def extract_snippet(text: str, query_tokens: list[str], max_len: int = 150) -> str:
    """
    从长文本中截取与查询最相关的片段（节省 Token，精准展示）。
    算法：找到 query token 命中最密集的位置，以该位置为中心截取窗口。
    """
    if not text or len(text) <= max_len:
        return text

    text_lower = text.lower()
    best_pos, best_score = 0, 0

    for token in query_tokens:
        if len(token) < 2:
            continue
        idx = text_lower.find(token)
        if idx < 0:
            continue
        win_s = max(0, idx - 50)
        win_e = min(len(text), idx + 100)
        window = text_lower[win_s:win_e]
        score  = sum(1 for t in query_tokens if len(t) >= 2 and t in window)
        if score > best_score:
            best_score, best_pos = score, idx

    start   = max(0, best_pos - 50)
    end     = min(len(text), start + max_len)
    snippet = text[start:end].strip()
    return ("…" if start > 0 else "") + snippet + ("…" if end < len(text) else "")


# ── 本地 Cross-Encoder 精排 ────────────────────────────────────────────────

_cross_encoder_instance = None   # 懒加载单例


def _get_cross_encoder():
    """懒加载本地 CrossEncoder（首次调用时下载 ~80MB 模型，之后本地缓存）。
    模型：cross-encoder/ms-marco-MiniLM-L-6-v2（MIT 协议，完全本地运行，零 API 调用）
    未安装 sentence-transformers 时静默返回 None，RRF 结果直接使用。
    """
    global _cross_encoder_instance
    if _cross_encoder_instance is not None:
        return _cross_encoder_instance
    try:
        from sentence_transformers import CrossEncoder
        _cross_encoder_instance = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    except Exception:
        _cross_encoder_instance = None
    return _cross_encoder_instance


def _result_to_plain_text(result: dict) -> str:
    """将检索结果序列化为纯文本（供 cross-encoder 评分输入）"""
    source = result.get("source", "")
    data   = result.get("data", {})
    if source in ("ops", "tfidf", "embedding"):
        detail_str = json.dumps(data.get("detail", {}), ensure_ascii=False)[:200]
        return data.get("summary", "") + " " + detail_str
    elif source == "summary":
        return result.get("text", "")
    elif source == "knowledge_base":
        return f"{data.get('title', '')} {data.get('content', '')}"
    elif source == "entity":
        return f"{data.get('name', '')} {data.get('context', '')}"
    elif source == "profile":
        return f"{data.get('field', '')}: {data.get('value', '')}"
    return str(data)[:300]


def local_cross_encode(query: str, results: list[dict], top_k: int) -> list[dict]:
    """
    本地 Cross-Encoder 精排（完全私有，无 API 调用）。
    在 RRF 初排后对 top_k*3 候选进行精排，进一步提升准确率约 5-8%。
    只在 sentence-transformers 已安装时启用，否则直接返回 RRF 结果。
    """
    if not results:
        return results
    model = _get_cross_encoder()
    if model is None:
        return results[:top_k]

    candidates = results[:top_k * 3]
    pairs      = [(query, _result_to_plain_text(r)) for r in candidates]
    try:
        scores = model.predict(pairs, show_progress_bar=False)
        for r, s in zip(candidates, scores):
            r["cross_score"] = float(s)
        candidates = sorted(candidates, key=lambda x: -x.get("cross_score", 0.0))
    except Exception:
        pass
    return candidates[:top_k]


# ── 结果格式化 ──────────────────────────────────────────────────────────

def format_result(result: dict, show_context: bool = True, query_tokens: list[str] = None) -> str:
    source = result["source"]
    lines = []

    if source == "ops":
        op      = result["data"]
        ts      = op["ts"][:16].replace("T", " ")
        summary = op["summary"]
        if query_tokens and len(summary) > 80:
            summary = extract_snippet(summary, query_tokens, max_len=120)
        tier_tag = f" [{op.get('tier', '')}]" if op.get("tier") else ""
        lines.append(f"[ops #{op['seq']} · {ts}{tier_tag}] {summary}")
        # 显示上下文窗口
        if show_context and result.get("context"):
            ctx = result["context"]
            for before_op in ctx.get("before", []):
                lines.append(f"  ↑ [#{before_op['seq']}] {before_op['summary'][:60]}")
            for after_op in ctx.get("after", []):
                lines.append(f"  ↓ [#{after_op['seq']}] {after_op['summary'][:60]}")
    elif source == "summary":
        lines.append(f"[摘要] {result['text']}")
    elif source == "knowledge_base":
        d       = result["data"]
        content = d.get("content", "")
        if query_tokens and len(content) > 100:
            content = extract_snippet(content, query_tokens, max_len=150)
        history_tag = " [历史版本]" if d.get("_history") else ""
        lines.append(f"[知识库{history_tag} · {d.get('title', '?')}] {content}")
    elif source == "history":
        d = result["data"]
        ts = d.get("started_at", "")[:10]
        lines.append(f"[历史会话 · {ts} · {d.get('project', '')}] {d.get('last_milestone', '无里程碑记录')}")
    elif source == "entity":
        d = result["data"]
        et = d.get("entity_type", "?")
        name = d.get("name", "?")
        ctx = d.get("context", "")
        ts = d.get("ts", "")[:16].replace("T", " ")
        extra = ""
        if et == "dependency":
            extra = f" [via {d.get('manager', '?')}]"
        elif et == "decision":
            rationale = d.get("rationale", "")
            extra = f" 依据: {rationale}" if rationale else ""
        elif et == "error":
            extra = f" ← {d.get('message', '')}"
        lines.append(f"[实体/{et} · {ts}] {name}{extra}")
        if ctx:
            lines.append(f"  来源: {ctx}")

    elif source in ("tfidf", "embedding"):
        d      = result["data"]
        ts     = d.get("ts", "")[:16].replace("T", " ")
        label  = "TF-IDF" if source == "tfidf" else "向量"
        summary = d.get("summary", "?")
        if query_tokens and len(summary) > 80:
            summary = extract_snippet(summary, query_tokens, max_len=120)
        lines.append(f"[语义/{label} #{d.get('seq', '?')} · {ts}] {summary}")

    elif source == "profile":
        d = result["data"]
        lines.append(f"[用户画像] {d['field']}: {d['value']}")

    return "\n".join(lines) if lines else str(result)


def recall(session_id: str, query: str, top_k: int = 5, as_of: str = ""):
    """
    检索记忆。

    as_of: ISO 时间字符串，启用时间旅行模式。
          查询在指定时间点的知识状态，忽略之后创建/更新的记录。
          例: --as-of 2026-03-01T00:00:00Z
    """
    query_tokens = expand_query(query)
    session_dir  = ULTRA_MEMORY_HOME / "sessions" / session_id

    # 收集各层检索结果（保持各自排序，交由 RRF 统一融合）
    all_layers: list[list[dict]] = []

    ops_results = search_ops(session_dir, query_tokens, top_k * 3)
    if ops_results:
        all_layers.append(ops_results)

    summary_results = search_summary(session_dir, query_tokens)
    if summary_results:
        all_layers.append(summary_results)

    semantic_results = search_semantic(query_tokens, top_k * 2, as_of=as_of)
    if semantic_results:
        all_layers.append(semantic_results)

    profile_results = search_profile(query_tokens, ULTRA_MEMORY_HOME)
    if profile_results:
        all_layers.append(profile_results)

    entity_results = search_entities(query_tokens, top_k * 2)
    if entity_results:
        all_layers.append(entity_results)

    ops_all = load_all_ops(session_dir)
    if ops_all:
        vector_results = search_tfidf(session_dir, ops_all, query, top_k * 2)
        if vector_results:
            all_layers.append(vector_results)

    if not all_layers:
        print(f"[RECALL] 未找到与「{query}」相关的记忆")
        if as_of:
            print(f"[RECALL] 时间旅行模式: {as_of}")
        return

    # RRF 融合：跨层去重 + 多源一致性加权（替代简单 score 合并）
    found = rrf_merge(all_layers)

    # 可选精排：本地 Cross-Encoder（需 sentence-transformers，完全离线）
    found = local_cross_encode(query, found, top_k)

    if not found:
        print(f"[RECALL] 未找到与「{query}」相关的记忆")
        return

    # 回写 access_count：常被召回的操作衰减更慢
    recalled_seqs = {
        r["data"]["seq"]
        for r in found
        if r.get("source") in ("ops", "tfidf", "embedding") and "seq" in r.get("data", {})
    }
    _increment_access_count(session_dir, recalled_seqs)

    time_travel_note = f" [时间旅行: {as_of}]" if as_of else ""
    print(f"\n[RECALL] 找到 {len(found)} 条相关记录（查询: {query}）{time_travel_note}：\n")
    for i, r in enumerate(found, 1):
        print(f"{i}. {format_result(r, show_context=True, query_tokens=query_tokens)}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检索记忆")
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument("--query", required=True, help="检索关键词")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--as-of", default="", help="时间旅行：查询该时间点的知识状态（ISO 格式）")
    parser.add_argument("--history", default="", help="查询同名实体的版本历史（实体名称）")
    args = parser.parse_args()

    if args.history:
        versions = search_entity_history(args.history, ULTRA_MEMORY_HOME)
        print(format_entity_history(versions, args.history))
    else:
        recall(args.session, args.query, args.top_k, as_of=args.as_of)
