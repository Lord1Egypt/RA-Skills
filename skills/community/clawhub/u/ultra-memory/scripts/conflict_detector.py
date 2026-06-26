#!/usr/bin/env python3
"""
ultra-memory: 矛盾检测核心模块
检测 user_profile.json 和 knowledge_base.jsonl 中的时序矛盾，
将旧记录标记为 superseded: true，召回时跳过失效记录。

只使用 Python 标准库，无外部依赖。
"""

import os
import re
import json
from datetime import datetime, timezone
from pathlib import Path

# ── 停用词表 ────────────────────────────────────────────────────────────────

STOPWORDS = {
    "的", "了", "是", "在", "和", "与", "或", "以及",
    "a", "an", "the", "is", "was", "are", "were",
    "to", "of", "for", "with", "by", "from",
}

# ── 否定词表 ────────────────────────────────────────────────────────────────

NEGATION_WORDS = {
    "不", "没有", "无法", "不能", "不是", "别", "莫", "永不", "绝不",
    "not", "no", "never", "none", "cannot", "don't", "doesn't",
    "isn't", "aren't", "wasn't", "weren't", "won't", "wouldn't",
}

# ── 对立词对 ───────────────────────────────────────────────────────────────

CONTRADICTORY_PAIRS = [
    frozenset(["成功", "失败"]),
    frozenset(["可以", "不能"]),
    frozenset(["推荐", "不推荐"]),
    frozenset(["启用", "禁用"]),
    frozenset(["enable", "disable"]),
    frozenset(["success", "failure"]),
    frozenset(["yes", "no"]),
    frozenset(["true", "false"]),
]


# ── 工具函数 ───────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _stopword_filter(words: list[str]) -> list[str]:
    return [w for w in words if w.lower() not in STOPWORDS and len(w) > 1]


# ── 画像冲突检测 ───────────────────────────────────────────────────────────


def detect_profile_conflict(new_data: dict, home: Path) -> list[dict]:
    """
    检测 user_profile.json 中的字段冲突。
    返回冲突列表，每条格式：
      {"field": "...", "old_value": "...", "new_value": "...", "superseded_at": "..."}
    """
    profile_file = home / "semantic" / "user_profile.json"
    if not profile_file.exists():
        return []

    try:
        with open(profile_file, encoding="utf-8") as f:
            profile = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

    conflicts = []

    for field, new_value in new_data.items():
        # observed_patterns 只追加，不检测冲突
        if field == "observed_patterns":
            continue

        # 跳过 superseded 标记的字段
        if field.endswith("_superseded"):
            continue

        if field not in profile:
            continue

        old_value = profile[field]

        # 字符串类型：旧值与新值不同 → 冲突
        if isinstance(old_value, str) and isinstance(new_value, str):
            if old_value != new_value:
                conflicts.append({
                    "field": field,
                    "old_value": old_value,
                    "new_value": new_value,
                    "superseded_at": _now_iso(),
                })

        # 数组类型：完全替换（完全不同）→ 冲突；只新增元素 → 不冲突
        elif isinstance(old_value, list) and isinstance(new_value, list):
            # 新旧完全不同才算冲突；新值包含旧值的所有元素（新增元素）不算冲突
            old_set = set(str(v) for v in old_value)
            new_set = set(str(v) for v in new_value)
            if old_set and new_set and old_set != new_set:
                # 只有当旧值中的元素不在新值中，才算冲突
                removed = old_set - new_set
                if removed:  # 有元素被移除才算冲突
                    conflicts.append({
                        "field": field,
                        "old_value": old_value,
                        "new_value": new_value,
                        "superseded_at": _now_iso(),
                    })

        # dict 类型：递归检测每个 key
        elif isinstance(old_value, dict) and isinstance(new_value, dict):
            for sub_key, sub_old in old_value.items():
                if sub_key not in new_value:
                    continue
                sub_new = new_value[sub_key]
                if isinstance(sub_old, str) and isinstance(sub_new, str):
                    if sub_old != sub_new:
                        full_key = f"{field}.{sub_key}"
                        conflicts.append({
                            "field": full_key,
                            "old_value": sub_old,
                            "new_value": "（已更新）" if sub_new else sub_new,
                            "superseded_at": _now_iso(),
                        })

    return conflicts


def mark_profile_superseded(home: Path, conflicts: list[dict]):
    """
    将 user_profile.json 中冲突的旧字段标记为 superseded。
    在旧字段旁追加 "<field>_superseded" 记录旧值。
    """
    profile_file = home / "semantic" / "user_profile.json"
    if not profile_file.exists() or not conflicts:
        return

    try:
        with open(profile_file, encoding="utf-8") as f:
            profile = json.load(f)
    except (json.JSONDecodeError, IOError):
        return

    for conflict in conflicts:
        field = conflict["field"]
        # 记录旧值
        superseded_key = f"{field}_superseded"
        profile[superseded_key] = {
            "old_value": conflict["old_value"],
            "superseded_at": conflict["superseded_at"],
        }
        # 将新值写入主字段（已经在 profile_update 时更新了，这里只处理遗留情况）
        if "." in field:
            # 处理嵌套 dict key，如 work_style.confirm_before_implement
            parts = field.split(".")
            d = profile
            for p in parts[:-1]:
                d = d.setdefault(p, {})
            d[parts[-1]] = conflict["new_value"]
        else:
            profile[field] = conflict["new_value"]

    # 原子写入
    tmp_file = profile_file.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    tmp_file.replace(profile_file)


# ── 知识库冲突检测 ────────────────────────────────────────────────────────


def _extract_keywords(text: str) -> set[str]:
    """提取关键词（去除停用词）"""
    words = re.split(r'[\s,;.()\[\]{}]+', text.lower())
    return set(_stopword_filter(words))


def _title_similarity(title_a: str, title_b: str) -> float:
    """计算标题相似度：关键词重叠数 / max(len_a, len_b)"""
    keywords_a = _extract_keywords(title_a)
    keywords_b = _extract_keywords(title_b)
    if not keywords_a or not keywords_b:
        return 0.0
    overlap = len(keywords_a & keywords_b)
    max_len = max(len(keywords_a), len(keywords_b))
    return overlap / max_len


def _has_negation(text: str) -> bool:
    """检测文本中是否含否定词"""
    text_lower = text.lower()
    return any(nw in text_lower for nw in NEGATION_WORDS)


def _has_number_change(text_old: str, text_new: str) -> bool:
    """检测数值变化：两边都有数字但数字不同"""
    nums_old = set(re.findall(r'\d+\.?\d*', text_old))
    nums_new = set(re.findall(r'\d+\.?\d*', text_new))
    if nums_old and nums_new and nums_old != nums_new:
        return True
    return False


def _has_contradictory_pair(text_old: str, text_new: str) -> bool:
    """检测对立词对：一边含 A 另一边含 B"""
    text_lower_old = text_old.lower()
    text_lower_new = text_new.lower()
    for pair in CONTRADICTORY_PAIRS:
        words_old = set(pair & set(text_lower_old.split()))
        words_new = set(pair & set(text_lower_new.split()))
        if words_old and words_new and words_old != words_new:
            return True
    return False


def detect_knowledge_conflict(new_entry: dict, home: Path) -> list[dict]:
    """
    检测 knowledge_base.jsonl 中的内容矛盾。
    new_entry 格式：{"title": "...", "content": "...", ...}
    返回冲突列表： [{"seq": 行号, "title": "...", "reason": "规则1/2/3"}]
    """
    kb_file = home / "semantic" / "knowledge_base.jsonl"
    if not kb_file.exists():
        return []

    new_title = new_entry.get("title", "")
    new_content = new_entry.get("content", "")

    conflicts = []
    lines = []
    with open(kb_file, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            # 跳过已失效条目
            if entry.get("superseded"):
                continue
            lines.append((i + 1, entry))  # 行号从1开始

    for seq, old_entry in lines:
        old_title = old_entry.get("title", "")
        old_content = old_entry.get("content", "")

        # 标题相似度 >= 0.5 才进入内容矛盾检测
        sim = _title_similarity(new_title, old_title)
        if sim < 0.5:
            continue

        # 矛盾规则检测
        reason = None

        # 规则1 — 否定词检测
        has_neg_old = _has_negation(old_content)
        has_neg_new = _has_negation(new_content)
        if has_neg_old != has_neg_new:
            reason = "规则1"

        # 规则2 — 数值变化检测
        elif _has_number_change(old_content, new_content):
            reason = "规则2"

        # 规则3 — 对立词检测
        elif _has_contradictory_pair(old_content, new_content):
            reason = "规则3"

        if reason:
            conflicts.append({
                "seq": seq,
                "title": old_title,
                "reason": reason,
            })

    return conflicts


def mark_superseded(home: Path, jsonl_path: Path, seq_list: list[int]):
    """
    将 knowledge_base.jsonl 中指定行号的条目标记为 superseded。
    原子写入：先写 tmp 文件再 rename。
    """
    if not seq_list:
        return

    seq_set = set(seq_list)

    tmp_file = jsonl_path.with_suffix(".tmp")
    written_seq = set()

    with open(jsonl_path, encoding="utf-8") as f_in, \
         open(tmp_file, "w", encoding="utf-8") as f_out:
        for i, line in enumerate(f_in):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            line_num = i + 1  # 行号从1开始
            if line_num in seq_set and line_num not in written_seq:
                entry["superseded"] = True
                entry["superseded_at"] = _now_iso()
                written_seq.add(line_num)

            f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")

    tmp_file.replace(jsonl_path)
