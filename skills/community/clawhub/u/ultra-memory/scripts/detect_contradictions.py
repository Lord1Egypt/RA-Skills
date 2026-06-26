#!/usr/bin/env python3
"""
ultra-memory: 矛盾检测引擎 (Evolution Engine Phase 2)
检测 facts.jsonl 中新事实与已有事实之间的矛盾，
写入 evolution/contradictions.jsonl，并自动处理低置信度矛盾的消解。

矛盾检测算法：
  1. 候选选取：同 (subject, predicate) 的事实对
  2. 相似度评分：Jaccard + 谓词结构匹配 + 主语精确匹配
  3. 否定检测：检测 "A" vs "not A" 类型的否定对
  4. 自动消解：双方置信度都 ≤ 0.85 的否定矛盾 → 自动降级旧事实

被 extract_facts.py 在每次提取后背景调用。
"""

import os
import sys
import re
import json
import argparse
import hashlib
import tempfile
import shutil
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# ── 否定词目录 ─────────────────────────────────────────────────────────────

NEGATION_WORDS = {
    # English
    "not", "no", "never", "none", "neither", "nobody",
    "nothing", "cannot", "won't", "don't", "doesn't",
    "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't",
    "hadn't", "shouldn't", "wouldn't", "couldn't",
    # Chinese
    "不对", "不是", "没有", "从不", "绝不", "无法",
    "禁止", "莫", "别", "休想", "永不",
}

# 占位符（与 extract_facts.py 保持一致）
NUMERIC_PLACEHOLDER = re.compile(r'\b\d+\.?\d*\b')
PATH_PLACEHOLDER = re.compile(
    r'[/\\]?[a-zA-Z0-9_\-\.]+\.(py|js|ts|jsx|tsx|vue|json|yaml|yml|md|sql|sh|go|rs|java|rb|toml)'
)

# 相似度阈值
SIMILARITY_THRESHOLD = 0.72

# ── 工具函数 ───────────────────────────────────────────────────────────────


def normalize_object(obj: str) -> str:
    """与 extract_facts.py 保持一致的归一化"""
    obj = obj.lower().strip()
    obj = NUMERIC_PLACEHOLDER.sub('<NUM>', obj)
    obj = PATH_PLACEHOLDER.sub('<PATH>', obj)
    obj = re.sub(r'\s+', ' ', obj)
    return obj


def tokenize(text: str) -> set[str]:
    """简单分词：按空白和常见标点分割"""
    tokens = re.split(r'[\s,;.()\[\]{}]+', text)
    return {t for t in tokens if t}


def fact_similarity(a: dict, b: dict) -> float:
    """
    组合相似度评分 ∈ [0, 1]。

    组成：
      - 归一化 object 的 Token Jaccard: 40% 权重
      - 谓词语义匹配（相同谓词=1.0）: 20% 权重
      - 主语精确匹配: 40% 权重
    """
    norm_a = normalize_object(a.get("object", ""))
    norm_b = normalize_object(b.get("object", ""))

    tokens_a = tokenize(norm_a)
    tokens_b = tokenize(norm_b)

    if not tokens_a or not tokens_b:
        jaccard = 0.0
    else:
        intersection = len(tokens_a & tokens_b)
        union = len(tokens_a | tokens_b)
        jaccard = intersection / union if union > 0 else 0.0

    # 谓词匹配
    pred_match = 1.0 if a.get("predicate") == b.get("predicate") else 0.0

    # 主语精确匹配
    subj_match = 1.0 if a.get("subject") == b.get("subject") else 0.0

    score = 0.4 * jaccard + 0.2 * pred_match + 0.4 * subj_match
    return min(1.0, max(0.0, score))


def detect_negation(obj_a: str, obj_b: str) -> bool:
    """
    检测 obj_a 和 obj_b 是否构成否定关系。
    启发式：归一化后结构相同，但其中一个包含否定词而另一个不含。
    """
    norm_a = normalize_object(obj_a)
    norm_b = normalize_object(obj_b)

    if norm_a == norm_b:
        return False

    # 检查是否一边有否定词，另一边没有
    has_neg_a = any(nw in norm_a for nw in NEGATION_WORDS)
    has_neg_b = any(nw in norm_b for nw in NEGATION_WORDS)

    if has_neg_a != has_neg_b:
        return True

    # 检查互补集合模式："A or B" vs "not A"
    # 例："pandas or numpy" vs "not pandas"
    or_pattern = re.compile(r'(\w+)\s+or\s+(\w+)')

    match_a = or_pattern.search(norm_a)
    match_b = or_pattern.search(norm_b)

    if match_a and match_b:
        # 两者都是 OR 表达式，不认为矛盾
        return False

    # 检查互斥动词
    exclusive_pairs = [
        (("use", "uses"), ("avoid", "avoids", "not use", "doesn't use")),
        (("install", "installed"), ("remove", "removed", "not install", "uninstall")),
        (("enable", "enabled"), ("disable", "disabled", "not enable")),
        (("include", "includes"), ("exclude", "excludes", "not include")),
    ]

    for affirmative, negatives in exclusive_pairs:
        a_is_aff = any(ex in norm_a for ex in affirmative)
        b_is_neg = any(ex in norm_b for ex in negatives)
        b_is_aff = any(ex in norm_b for ex in affirmative)
        a_is_neg = any(ex in norm_a for ex in negatives)
        if (a_is_aff and b_is_neg) or (b_is_aff and a_is_neg):
            return True

    return False


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def compute_contradiction_id(fact_id_a: str, fact_id_b: str) -> str:
    """确定性矛盾 ID"""
    raw = f"{fact_id_a}\x00{fact_id_b}"
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


# ── 存储 ───────────────────────────────────────────────────────────────────


def _load_facts() -> list[dict]:
    """加载所有活跃 facts"""
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
    return [f for f in facts if f.get("status", "active") != "forgotten"]


def _load_fact_metadata() -> dict:
    """加载 fact_metadata.json"""
    meta_file = ULTRA_MEMORY_HOME / "evolution" / "fact_metadata.json"
    if not meta_file.exists():
        return {"version": 1, "updated_at": _now_iso(), "facts": {}}
    try:
        with open(meta_file, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"version": 1, "updated_at": _now_iso(), "facts": {}}


def _save_fact_metadata(meta: dict):
    """写入 fact_metadata.json（原子写入）"""
    evolution_dir = ULTRA_MEMORY_HOME / "evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)
    meta_file = evolution_dir / "fact_metadata.json"

    meta["updated_at"] = _now_iso()

    # 原子写入：先写临时文件再 rename
    tmp_file = meta_file.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    tmp_file.replace(meta_file)


def append_contradiction(contradiction: dict):
    """追加写入 contradictions.jsonl"""
    evolution_dir = ULTRA_MEMORY_HOME / "evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)
    ctd_file = evolution_dir / "contradictions.jsonl"

    with open(ctd_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(contradiction, ensure_ascii=False) + "\n")


# ── 自动消解 ───────────────────────────────────────────────────────────────


def auto_resolve(contradiction: dict, meta: dict) -> bool:
    """
    自动消解低置信度矛盾。
    条件：双方置信度都 ≤ 0.85，且是直接否定矛盾。
    策略：新事实胜出，旧事实置信度 ×0.35。
    返回：是否进行了自动消解。
    """
    if contradiction.get("resolution") != "auto_resolved":
        return False

    fact_ids = [contradiction.get("fact_id_new"), contradiction.get("fact_id_old")]
    new_conf_before = None
    old_conf_before = None

    for fid in fact_ids:
        if fid not in meta["facts"]:
            continue
        if fid == contradiction.get("fact_id_new"):
            new_conf_before = meta["facts"][fid].get("confidence", 1.0)
        else:
            old_conf_before = meta["facts"][fid].get("confidence", 1.0)

    if new_conf_before is None or old_conf_before is None:
        return False

    # 满足自动消解条件
    if new_conf_before <= 0.85 and old_conf_before <= 0.85:
        old_fact_id = contradiction.get("fact_id_old")
        if old_fact_id in meta["facts"]:
            old_entry = meta["facts"][old_fact_id]
            old_conf = old_entry.get("confidence", 0.5)
            new_conf = old_entry.get("confidence", 0.5)  # placeholder

            for fid in fact_ids:
                if fid == old_fact_id:
                    old_entry["confidence"] = round(old_conf * 0.35, 2)
                    if old_entry["confidence"] < 0.15:
                        old_entry["status"] = "superseded"
                elif fid == contradiction.get("fact_id_new"):
                    new_conf = meta["facts"][fid].get("confidence", 0.5)
                    meta["facts"][fid]["confidence"] = round(
                        (new_conf + 0.1), 2
                    )  # 微弱提升

            contradiction["resolution_detail"] = (
                f"Auto: new wins, old confidence {old_conf:.2f}→{old_conf*0.35:.2f}"
            )

            # 记录修正历史
            old_entry.setdefault("correction_history", []).append({
                "corrected_at": _now_iso(),
                "old_confidence": old_conf,
                "new_confidence": round(old_conf * 0.35, 2),
                "source": "auto",
                "contradiction_id": contradiction.get("contradiction_id"),
            })

            return True

    return False


# ── 核心检测 ───────────────────────────────────────────────────────────────


def detect_for_facts(new_fact_ids: list[str], session_id: str) -> list[dict]:
    """
    检测与新事实产生矛盾的所有已有事实。
    """
    all_facts = _load_facts()

    # 建立 fact_id → fact 映射
    fact_map = {f.get("fact_id"): f for f in all_facts}

    # 筛选目标新事实
    target_new = [f for f in all_facts if f.get("fact_id") in set(new_fact_ids)]

    contradictions_found = []

    for new_fact in target_new:
        # 找候选：同 subject + 同 predicate
        candidates = [
            f for f in all_facts
            if f.get("subject") == new_fact.get("subject")
            and f.get("predicate") == new_fact.get("predicate")
            and f.get("fact_id") != new_fact.get("fact_id")
            and f.get("status") not in ("forgotten", "superseded")
        ]

        for old_fact in candidates:
            score = fact_similarity(new_fact, old_fact)
            if score < SIMILARITY_THRESHOLD:
                continue

            negation = detect_negation(
                new_fact.get("object", ""),
                old_fact.get("object", "")
            )

            ctd = {
                "contradiction_id": f"ctd_{compute_contradiction_id(new_fact['fact_id'], old_fact['fact_id'])}",
                "detected_at": _now_iso(),
                "session_id": session_id,
                "fact_id_new": new_fact.get("fact_id"),
                "fact_id_old": old_fact.get("fact_id"),
                "fact_new": {
                    "subject": new_fact.get("subject"),
                    "predicate": new_fact.get("predicate"),
                    "object": new_fact.get("object"),
                },
                "fact_old": {
                    "subject": old_fact.get("subject"),
                    "predicate": old_fact.get("predicate"),
                    "object": old_fact.get("object"),
                },
                "similarity_score": round(score, 3),
                "negation_detected": negation,
                "resolution": "pending",
                "resolution_detail": None,
                "confidence_new_before": new_fact.get("confidence"),
                "confidence_old_before": old_fact.get("confidence"),
                "confidence_new_after": new_fact.get("confidence"),
                "confidence_old_after": old_fact.get("confidence"),
            }

            contradictions_found.append(ctd)

    return contradictions_found


def update_contradiction_count(fact_ids: list[str], meta: dict, delta: int):
    """更新事实的矛盾计数"""
    for fid in fact_ids:
        if fid in meta["facts"]:
            meta["facts"][fid]["contradiction_count"] = (
                meta["facts"][fid].get("contradiction_count", 0) + delta
            )


def run_detection(new_fact_ids: list[str], session_id: str):
    """执行检测：找矛盾 → 写文件 → 自动消解 → 更新 metadata"""
    contradictions = detect_for_facts(new_fact_ids, session_id)

    if not contradictions:
        return

    meta = _load_fact_metadata()

    # 确保所有涉及的 fact_id 都在 metadata 中
    all_involved_ids = set()
    for ctd in contradictions:
        all_involved_ids.add(ctd["fact_id_new"])
        all_involved_ids.add(ctd["fact_id_old"])

    for fid in all_involved_ids:
        if fid not in meta["facts"]:
            meta["facts"][fid] = {
                "confidence": 0.7,
                "access_count": 0,
                "last_accessed": _now_iso(),
                "last_updated": _now_iso(),
                "importance_score": 0.5,
                "decay_level": "none",
                "ttl_days": 30,
                "expires_at": None,
                "status": "active",
                "contradiction_count": 0,
                "correction_history": [],
            }

    for ctd in contradictions:
        # 自动消解尝试
        auto_resolved = auto_resolve(ctd, meta)

        if not auto_resolved:
            ctd["resolution"] = "pending"

        # 写入矛盾记录
        append_contradiction(ctd)

        # 更新矛盾计数
        update_contradiction_count(
            [ctd["fact_id_new"], ctd["fact_id_old"]],
            meta, 1
        )

    _save_fact_metadata(meta)

    pending = sum(1 for c in contradictions if c["resolution"] == "pending")
    auto_resolved = len(contradictions) - pending
    print(f"[ultra-memory] ✅ 矛盾检测完成: {len(contradictions)} 个矛盾 "
          f"({auto_resolved} 个自动消解, {pending} 个待确认)")")


def run_batch_detection(session_id: str):
    """全量扫描模式：检测所有活跃事实对"""
    all_facts = _load_facts()

    # 按 (subject, predicate) 分组
    from collections import defaultdict
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for f in all_facts:
        if f.get("status") in ("forgotten", "superseded"):
            continue
        key = (f.get("subject"), f.get("predicate"))
        groups[key].append(f)

    # 对每组内的 fact 两两检测
    contradictions = []
    for key, group in groups.items():
        for i, fact_a in enumerate(group):
            for fact_b in group[i+1:]:
                score = fact_similarity(fact_a, fact_b)
                if score < SIMILARITY_THRESHOLD:
                    continue

                negation = detect_negation(
                    fact_a.get("object", ""),
                    fact_b.get("object", "")
                )

                if not negation and score < 0.9:
                    continue

                ctd_id = compute_contradiction_id(fact_a["fact_id"], fact_b["fact_id"])
                contradictions.append({
                    "contradiction_id": f"ctd_{ctd_id}",
                    "detected_at": _now_iso(),
                    "session_id": session_id,
                    "fact_id_new": fact_a["fact_id"],
                    "fact_id_old": fact_b["fact_id"],
                    "fact_new": {
                        "subject": fact_a.get("subject"),
                        "predicate": fact_a.get("predicate"),
                        "object": fact_a.get("object"),
                    },
                    "fact_old": {
                        "subject": fact_b.get("subject"),
                        "predicate": fact_b.get("predicate"),
                        "object": fact_b.get("object"),
                    },
                    "similarity_score": round(score, 3),
                    "negation_detected": negation,
                    "resolution": "pending",
                    "resolution_detail": None,
                    "confidence_new_before": fact_a.get("confidence"),
                    "confidence_old_before": fact_b.get("confidence"),
                    "confidence_new_after": fact_a.get("confidence"),
                    "confidence_old_after": fact_b.get("confidence"),
                })

    if not contradictions:
        print("[ultra-memory] ✅ 全量矛盾检测完成：无矛盾")
        return

    meta = _load_fact_metadata()

    # 初始化所有涉及 fact 的 metadata
    all_involved_ids = set()
    for ctd in contradictions:
        all_involved_ids.update([ctd["fact_id_new"], ctd["fact_id_old"]])

    for fid in all_involved_ids:
        if fid not in meta["facts"]:
            meta["facts"][fid] = {
                "confidence": 0.7, "access_count": 0,
                "last_accessed": _now_iso(), "last_updated": _now_iso(),
                "importance_score": 0.5, "decay_level": "none",
                "ttl_days": 30, "expires_at": None,
                "status": "active", "contradiction_count": 0,
                "correction_history": [],
            }

    for ctd in contradictions:
        auto_resolved = auto_resolve(ctd, meta)
        if not auto_resolved:
            ctd["resolution"] = "pending"
        append_contradiction(ctd)
        update_contradiction_count(
            [ctd["fact_id_new"], ctd["fact_id_old"]], meta, 1
        )

    _save_fact_metadata(meta)

    pending = sum(1 for c in contradictions if c["resolution"] == "pending")
    auto_resolved = len(contradictions) - pending
    print(f"[ultra-memory] ✅ 全量矛盾检测完成: {len(contradictions)} 个矛盾 "
          f"({auto_resolved} 个自动消解, {pending} 个待确认)")


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检测事实间的矛盾")
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument(
        "--new-fact-ids", nargs="+", default=None,
        help="新事实 ID 列表（检测与已有事实的矛盾）"
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="全量扫描模式（扫描所有活跃事实对）"
    )
    args = parser.parse_args()

    if args.batch:
        run_batch_detection(args.session)
    elif args.new_fact_ids:
        run_detection(args.new_fact_ids, args.session)
    else:
        print("[ultra-memory] ⚠️  请指定 --new-fact-ids 或 --batch")
        sys.exit(1)
