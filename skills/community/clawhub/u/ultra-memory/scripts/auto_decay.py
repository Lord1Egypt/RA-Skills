#!/usr/bin/env python3
"""
ultra-memory: 自动遗忘引擎 (Evolution Engine Phase 3)
基于时间衰减 + 访问频率 + 重要性评分计算每条事实的 decay_score。
decay_score < 0.05 的事实标记为遗忘（soft-delete，不删除原始记录）。

衰减公式：
  decay_score = importance_score × recency_weight × access_weight

  recency_weight  = 0.5 ^ (age_days / half_life_days)   # half_life=30天
  access_weight   = min(1.0, log2(access_count + 1) / log2(11))
                    # access_count=0 → ~0, access_count=10 → ~0.95

衰减等级：
  ≥ 0.6  → "none"      (健康)
  0.4–0.6 → "mild"     (轻度衰减)
  0.2–0.4 → "moderate" (中度衰减)
  0.05–0.2 → "severe"  (即将遗忘)
  < 0.05 → "forgotten" (触发遗忘)

被 cleanup.py --run-decay 调用，或每日定时触发。
"""

import os
import sys
import json
import argparse
import math
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# 默认衰减参数（可通过 config.json 覆盖）
DEFAULT_HALF_LIFE_DAYS = 30
DEFAULT_FORGET_THRESHOLD = 0.05

# ── 记忆类型 TTL 分层（参照 sdr-supermemory）─────────────────────────────
# permanent: 永不过期（用户画像、关键决策、里程碑）
# insight:   会话洞察、偏好（90天）
# signal:    临时信号、错误记录（30天）
# default:   其他事实（30天）

MEMORY_TYPE_TTL = {
    "permanent": None,   # 永不过期
    "insight":   90,     # 天
    "signal":    30,     # 天
    "default":   30,     # 天
}

# 实体类型 / 标签 → 记忆类型映射
ENTITY_TYPE_TO_MEMORY_TYPE = {
    "dependency": "permanent",   # 依赖包一般不变化
    "decision":   "permanent",   # 关键决策永久保留
    "class":      "permanent",   # 类定义稳定
    "function":   "insight",     # 函数实现可能演进
    "file":       "insight",     # 文件可能变化
    "error":      "signal",      # 错误记录临时
    "preference": "permanent",   # 用户偏好永久
    "person":     "permanent",   # 人物信息永久
    "project":    "permanent",   # 项目配置永久
}

# 衰减等级边界
DECAY_LEVELS = [
    (0.6, "none"),
    (0.4, "mild"),
    (0.2, "moderate"),
    (0.05, "severe"),
]


# ── 工具函数 ───────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_ts(ts_str: str) -> datetime:
    """解析 ISO 时间字符串"""
    if not ts_str:
        return datetime.now(timezone.utc)
    try:
        # 移除 Z 后缀
        ts_str = ts_str.replace("Z", "+00:00")
        return datetime.fromisoformat(ts_str)
    except ValueError:
        return datetime.now(timezone.utc)


def _load_config() -> dict:
    """加载配置（如果有 decay 相关配置）"""
    config_file = ULTRA_MEMORY_HOME / "config.json"
    if config_file.exists():
        try:
            with open(config_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


# ── 衰减计算 ───────────────────────────────────────────────────────────────


def compute_decay_score(
    fact_metadata: dict,
    now: datetime,
) -> float:
    """
    计算单条事实的衰减评分。

    decay_score = importance_score × recency_weight × access_weight
    """
    age_days = (now - _parse_ts(fact_metadata.get("last_updated", ""))).days
    half_life_days = fact_metadata.get("ttl_days", DEFAULT_HALF_LIFE_DAYS)

    # 时间衰减权重
    recency_weight = math.pow(0.5, age_days / half_life_days) if half_life_days > 0 else 0.0

    # 访问频率权重
    access_count = fact_metadata.get("access_count", 0)
    access_weight = min(1.0, math.log2(access_count + 1) / math.log2(11))

    # 重要性评分
    importance_score = fact_metadata.get("importance_score", 0.5)

    score = importance_score * recency_weight * access_weight

    # 从未访问且较老的事实额外惩罚
    if access_count == 0 and age_days > half_life_days:
        score *= 0.5

    return max(0.0, min(1.0, score))


def detect_memory_type(fact: dict) -> str:
    """
    根据事实的实体类型、标签或来源判断记忆类型。
    返回 "permanent" | "insight" | "signal" | "default"。
    """
    # 1. 实体类型优先
    entity_type = fact.get("entity_type", "")
    if entity_type and entity_type in ENTITY_TYPE_TO_MEMORY_TYPE:
        return ENTITY_TYPE_TO_MEMORY_TYPE[entity_type]

    # 2. 标签判断
    tags = set(fact.get("tags", []))
    if tags & {"preference", "person", "project", "milestone"}:
        return "permanent"
    if tags & {"error", "debug", "signal"}:
        return "signal"

    # 3. 来源类型判断
    source_type = fact.get("source_type", "")
    if source_type in ("milestone", "decision"):
        return "permanent"
    if source_type in ("error",):
        return "signal"

    # 4. fact 内容关键词（针对 facts.jsonl 中无 entity_type 的情况）
    content = (fact.get("subject", "") + " " + fact.get("predicate", "") + " " + fact.get("object", "")).lower()
    permanent_kw = ["用户", "偏好", "决策", "项目", "配置", "住在", "工作", "职"]
    signal_kw = ["错误", "报错", "失败", "异常", "bug"]
    for kw in permanent_kw:
        if kw in content:
            return "permanent"
    for kw in signal_kw:
        if kw in content:
            return "signal"

    return "default"



    """根据衰减评分确定衰减等级"""
    for threshold, level in DECAY_LEVELS:
        if score >= threshold:
            return level
    return "forgotten"


def compute_importance_score(fact: dict, meta: dict) -> float:
    """
    计算事实的重要性评分 (0.0–1.0)。
    来源类型 × 矛盾抵抗 × 用户确认度 的加权组合。
    """
    base = 0.5

    # 来源类型权重
    source_weights = {
        "milestone": 0.9,
        "decision": 0.85,
        "user_instruction": 0.8,
        "file_write": 0.7,
        "tool_call": 0.6,
        "reasoning": 0.6,
        "bash_exec": 0.55,
        "error": 0.5,
        "file_read": 0.4,
    }
    source_type = fact.get("source_type", "")
    base = source_weights.get(source_type, 0.6)

    # 矛盾抵抗：矛盾越少越稳定
    contradiction_count = meta.get("contradiction_count", 0)
    contradiction_penalty = min(0.3, contradiction_count * 0.1)
    base = max(0.1, base - contradiction_penalty)

    # 用户显式确认权重（如果 correction_history 有 manual 条目）
    manual_corrections = [
        c for c in meta.get("correction_history", [])
        if c.get("source") == "manual"
    ]
    if manual_corrections:
        base = min(1.0, base + 0.15)

    return max(0.1, min(1.0, base))


# ── 遗忘处理 ───────────────────────────────────────────────────────────────


def _load_facts() -> list[dict]:
    """加载所有 facts"""
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


def _load_metadata() -> dict:
    """加载 fact_metadata.json"""
    meta_file = ULTRA_MEMORY_HOME / "evolution" / "fact_metadata.json"
    if not meta_file.exists():
        return {"version": 1, "updated_at": _now_iso(), "facts": {}}
    try:
        with open(meta_file, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"version": 1, "updated_at": _now_iso(), "facts": {}}


def _save_metadata(meta: dict):
    """原子写入 metadata"""
    evolution_dir = ULTRA_MEMORY_HOME / "evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)
    meta_file = evolution_dir / "fact_metadata.json"
    meta["updated_at"] = _now_iso()

    tmp_file = meta_file.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    tmp_file.replace(meta_file)


def append_decay_log(entry: dict):
    """追加写入 decay_log.jsonl"""
    evolution_dir = ULTRA_MEMORY_HOME / "evolution"
    evolution_dir.mkdir(parents=True, exist_ok=True)
    log_file = evolution_dir / "decay_log.jsonl"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── 全量衰减扫描 ───────────────────────────────────────────────────────────


def run_decay_pass(session_id: str | None = None):
    """
    执行全量衰减扫描。
    session_id 不为 None 时只扫描指定 session 的事实。
    """
    now = datetime.now(timezone.utc)
    facts = _load_facts()
    meta = _load_metadata()

    config = _load_config()
    forget_threshold = (
        config.get("decay", {}).get("forget_threshold", DEFAULT_FORGET_THRESHOLD)
    )

    # 初始化所有 fact 的 metadata（如果不存在）
    for fact in facts:
        fid = fact.get("fact_id")
        if not fid:
            continue
        if fid not in meta["facts"]:
            mem_type = detect_memory_type(fact)
            ttl_days = MEMORY_TYPE_TTL[mem_type]

            meta["facts"][fid] = {
                "confidence": fact.get("confidence", 0.7),
                "access_count": fact.get("access_count", 1),
                "last_accessed": fact.get("last_accessed", _now_iso()),
                "last_updated": fact.get("ts", _now_iso()),
                "importance_score": compute_importance_score(fact, {}),
                "decay_level": "none",
                "ttl_days": ttl_days,
                "memory_type": mem_type,
                "expires_at": None,
                "status": "active",
                "contradiction_count": fact.get("contradiction_count", 0),
                "correction_history": [],
            }

    # 计算每条事实的衰减
    forgotten_ids = []
    severe_ids = []
    updated_ids = []

    for fid, fact_meta in meta["facts"].items():
        if fact_meta.get("status") in ("forgotten", "superseded"):
            continue

        # session_id 过滤
        if session_id:
            # 找到对应 fact
            matching_fact = next(
                (f for f in facts if f.get("fact_id") == fid), None
            )
            if not matching_fact:
                continue
            if matching_fact.get("session_id") != session_id:
                continue

        # TTL 过期检测
        if fact_meta.get("expires_at"):
            expires_at = _parse_ts(fact_meta["expires_at"])
            if now >= expires_at:
                fact_meta["decay_level"] = "forgotten"

        # 重新计算重要性评分（基于最新事实数据）
        matching_fact = next(
            (f for f in facts if f.get("fact_id") == fid), None
        )
        if matching_fact:
            fact_meta["importance_score"] = compute_importance_score(
                matching_fact, fact_meta
            )

        # 计算衰减评分
        decay_score = compute_decay_score(fact_meta, now)
        old_level = fact_meta.get("decay_level", "none")
        new_level = compute_decay_level(decay_score)
        fact_meta["decay_level"] = new_level

        # 更新 ttl_days 配置（仅 non-permanent 类型）
        ttl_days = fact_meta.get("ttl_days", DEFAULT_HALF_LIFE_DAYS)
        # permanent 类型永不过期
        if ttl_days is None:
            fact_meta["decay_level"] = "none"
            continue

        # 触发遗忘
        if new_level == "forgotten" and old_level != "forgotten":
            fact_meta["status"] = "forgotten"
            fact_meta["forgotten_at"] = _now_iso()
            forgotten_ids.append(fid)

            append_decay_log({
                "ts": _now_iso(),
                "fact_id": fid,
                "reason": "ttl_expired" if fact_meta.get("expires_at") else "importance_decay",
                "decay_level_before": old_level,
                "action": "marked_forgotten",
                "decay_score": round(decay_score, 3),
                "session_id": session_id or "system",
            })
        elif new_level == "severe" and old_level in ("none", "mild", "moderate"):
            severe_ids.append(fid)

        if new_level != old_level:
            updated_ids.append(fid)

    _save_metadata(meta)

    print(f"[ultra-memory] ✅ 衰减扫描完成 (session: {session_id or 'all'})")
    print(f"  遗忘: {len(forgotten_ids)} 条")
    print(f"  严重衰减: {len(severe_ids)} 条")
    print(f"  等级变化: {len(updated_ids)} 条")

    return {
        "forgotten": forgotten_ids,
        "severe": severe_ids,
        "updated": updated_ids,
    }


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="执行事实衰减扫描")
    parser.add_argument(
        "--session", default=None,
        help="会话 ID（省略则扫描所有事实）"
    )
    parser.add_argument(
        "--run", action="store_true",
        help="执行衰减扫描（配合 cleanup.py 使用）"
    )
    args = parser.parse_args()

    result = run_decay_pass(args.session)
    sys.exit(0)
