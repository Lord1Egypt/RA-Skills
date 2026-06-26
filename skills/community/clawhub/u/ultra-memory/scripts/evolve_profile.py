#!/usr/bin/env python3
"""
ultra-memory: 用户画像进化引擎 (Evolution Engine Phase 4)
基于贝叶斯置信度更新实现 user_profile.json 的动态演化。

贝叶斯更新公式（Beta 分布）：
  alpha_post = max(0.5, old_conf × old_count) + new_evidence_conf
  beta_post  = max(0.5, (1-old_conf) × old_count) + (1 - new_evidence_conf)
  new_conf   = alpha_post / (alpha_post + beta_post)

当新事实与画像矛盾时：
  1. 追加 correction_history
  2. 新值胜出，旧值降权记录
  3. 如果旧置信度 > 0.85 → 标记为 pending manual resolution

被 extract_facts.py 或 SKILL.md Step 7B 触发。
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

# ── 贝叶斯更新 ─────────────────────────────────────────────────────────────


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_ts(ts_str: str) -> datetime:
    if not ts_str:
        return datetime.now(timezone.utc)
    try:
        ts_str = ts_str.replace("Z", "+00:00")
        return datetime.fromisoformat(ts_str)
    except ValueError:
        return datetime.now(timezone.utc)


def bayesian_update(
    existing_confidence: float,
    new_evidence_confidence: float,
    existing_count: int,
) -> tuple[float, int]:
    """
    Beta 分布贝叶斯更新。

    Jeffreys prior: Beta(0.5, 0.5)
    posterior alpha' = prior_alpha + new_weight
    posterior beta'  = prior_beta  + (1 - new_weight)
    new_confidence    = alpha' / (alpha' + beta')

    Returns: (new_confidence, new_count)
    """
    # Jeffreys prior 保护
    alpha_prior = max(0.5, existing_confidence * existing_count)
    beta_prior = max(0.5, (1 - existing_confidence) * existing_count)

    alpha_post = alpha_prior + new_evidence_confidence
    beta_post = beta_prior + (1 - new_evidence_confidence)

    new_confidence = alpha_post / (alpha_post + beta_post)
    new_count = existing_count + 1

    return round(new_confidence, 3), new_count


# ── 画像加载/保存 ─────────────────────────────────────────────────────────


def _load_profile() -> dict:
    """加载 user_profile.json，兼容 v1 和 v2 格式"""
    profile_file = ULTRA_MEMORY_HOME / "semantic" / "user_profile.json"
    if not profile_file.exists():
        return {"version": 2, "fields": {}, "last_reflection": None, "last_distillation": None}

    try:
        with open(profile_file, encoding="utf-8") as f:
            profile = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"version": 2, "fields": {}, "last_reflection": None, "last_distillation": None}

    # v1 → v2 迁移
    if profile.get("version") != 2:
        migrated = {"version": 2, "fields": {}, "last_reflection": None, "last_distillation": None}

        # 迁移 tech_stack
        if "tech_stack" in profile:
            migrated["fields"]["tech_stack"] = {
                "value": profile["tech_stack"] if isinstance(profile["tech_stack"], list) else [profile["tech_stack"]],
                "confidence": 0.6,
                "evidence_count": 1,
                "last_updated": profile.get("last_updated", _now_iso()),
                "sources": [],
                "corrected_at": None,
            }

        # 迁移 language
        if "language" in profile:
            migrated["fields"]["language"] = {
                "value": profile["language"],
                "confidence": 0.7,
                "evidence_count": 1,
                "last_updated": profile.get("last_updated", _now_iso()),
                "sources": [],
                "corrected_at": None,
            }

        # 迁移 work_style
        if "work_style" in profile:
            for k, v in profile["work_style"].items():
                migrated["fields"][f"work_style.{k}"] = {
                    "value": v,
                    "confidence": 0.5,
                    "evidence_count": 1,
                    "last_updated": profile.get("last_updated", _now_iso()),
                    "sources": [],
                    "corrected_at": None,
                }

        # 迁移 observed_patterns
        if "observed_patterns" in profile:
            migrated["fields"]["observed_patterns"] = {
                "value": profile["observed_patterns"],
                "confidence": 0.5,
                "evidence_count": 1,
                "last_updated": profile.get("last_updated", _now_iso()),
                "sources": [],
                "corrected_at": None,
            }

        migrated["last_reflection"] = profile.get("last_reflection")
        migrated["last_distillation"] = profile.get("last_distillation")

        return migrated

    return profile


def _save_profile(profile: dict):
    """原子写入 user_profile.json"""
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    semantic_dir.mkdir(parents=True, exist_ok=True)
    profile_file = semantic_dir / "user_profile.json"
    profile["version"] = 2

    tmp_file = profile_file.with_suffix(".tmp")
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    tmp_file.replace(profile_file)


# ── 字段更新 ───────────────────────────────────────────────────────────────


# 偏好类谓词 → 画像字段映射
PREFERENCE_MAPPINGS = {
    "user_prefers": "preferences",
    "user_avoids": "preferences",
    "adopted": "preferences",
    "chose": "preferences",
}


def update_profile_from_fact(fact: dict, session_id: str):
    """
    基于提取到的事实更新用户画像。
    判断事实是否涉及用户偏好/行为，并更新对应字段。
    """
    predicate = fact.get("predicate", "")
    subject = fact.get("subject", "")
    obj = fact.get("object", "")
    confidence = fact.get("confidence", 0.7)

    profile = _load_profile()
    fields = profile.setdefault("fields", {})

    changed = False

    # 1. 处理用户偏好类谓词
    if predicate in PREFERENCE_MAPPINGS:
        pref_key = f"preferences.{subject}"

        existing = fields.get(pref_key)
        if existing:
            new_conf, new_count = bayesian_update(
                existing.get("confidence", 0.5),
                confidence,
                existing.get("evidence_count", 0),
            )
            existing["confidence"] = new_conf
            existing["evidence_count"] = new_count
            existing["last_updated"] = _now_iso()
            existing["sources"] = existing.get("sources", []) + [session_id]
            existing["sources"] = existing["sources"][-10:]  # 最多保留10个来源

            # 如果新值与旧值不同 → 追加修正历史
            if existing.get("value") != obj:
                existing.setdefault("correction_history", []).append({
                    "corrected_at": _now_iso(),
                    "old_value": existing.get("value"),
                    "new_value": obj,
                    "confidence_delta": round(new_conf - existing.get("confidence", 0.5), 3),
                    "source": "auto",
                })
                existing["value"] = obj
        else:
            fields[pref_key] = {
                "value": obj,
                "confidence": confidence,
                "evidence_count": 1,
                "last_updated": _now_iso(),
                "sources": [session_id],
                "corrected_at": None,
                "correction_history": [],
            }
        changed = True

    # 2. 处理技术栈推断（从 depends_on / requires / uses 谓词推断）
    elif predicate in ("depends_on", "requires", "uses", "installed_as"):
        tech_key = "tech_stack"
        existing = fields.get(tech_key)

        if existing:
            new_conf, new_count = bayesian_update(
                existing.get("confidence", 0.5),
                confidence,
                existing.get("evidence_count", 0),
            )
            existing["confidence"] = new_conf
            existing["evidence_count"] = new_count
            existing["last_updated"] = _now_iso()

            # 如果技术不在列表中，追加
            if isinstance(existing["value"], list) and obj not in existing["value"]:
                existing["value"] = existing["value"] + [obj]
        else:
            fields[tech_key] = {
                "value": [obj],
                "confidence": confidence,
                "evidence_count": 1,
                "last_updated": _now_iso(),
                "sources": [session_id],
                "corrected_at": None,
                "correction_history": [],
            }
        changed = True

    # 3. 处理行为模式（从 skip / fail_on / blocks 谓词推断）
    elif predicate in ("skips", "fails_on", "blocks"):
        pattern_key = f"work_style.behavior.{subject}"
        existing = fields.get(pattern_key)

        if existing:
            new_conf, new_count = bayesian_update(
                existing.get("confidence", 0.5),
                confidence,
                existing.get("evidence_count", 0),
            )
            existing["confidence"] = new_conf
            existing["evidence_count"] = new_count
            existing["last_updated"] = _now_iso()
            if existing.get("value") != obj:
                existing.setdefault("correction_history", []).append({
                    "corrected_at": _now_iso(),
                    "old_value": existing.get("value"),
                    "new_value": obj,
                    "confidence_delta": round(new_conf - existing.get("confidence", 0.5), 3),
                    "source": "auto",
                })
                existing["value"] = obj
        else:
            fields[pattern_key] = {
                "value": obj,
                "confidence": confidence,
                "evidence_count": 1,
                "last_updated": _now_iso(),
                "sources": [session_id],
                "corrected_at": None,
                "correction_history": [],
            }
        changed = True

    if changed:
        _save_profile(profile)
        print(f"[ultra-memory] ✅ 画像更新: {predicate} / {subject} = {obj}")


# ── 手动修正（SKILL.md Step 7B）────────────────────────────────────────────


def correct_profile_field(
    field_path: str,
    new_value,
    evidence_confidence: float = 1.0,
    session_id: str | None = None,
):
    """
    手动修正画像字段（Step 7B：错误修正）。
    强制覆盖旧值，追加 correction_history。
    """
    profile = _load_profile()
    fields = profile.setdefault("fields", {})

    old_value = None
    old_confidence = 0.5
    old_count = 0

    if field_path in fields:
        old_value = fields[field_path].get("value")
        old_confidence = fields[field_path].get("confidence", 0.5)
        old_count = fields[field_path].get("evidence_count", 0)

    # 强制更新
    fields[field_path] = {
        "value": new_value,
        "confidence": min(1.0, evidence_confidence),
        "evidence_count": old_count + 1,
        "last_updated": _now_iso(),
        "sources": [session_id] if session_id else [],
        "corrected_at": _now_iso(),
        "correction_history": fields.get(field_path, {}).get("correction_history", []) + [
            {
                "corrected_at": _now_iso(),
                "old_value": old_value,
                "new_value": new_value,
                "old_confidence": old_confidence,
                "new_confidence": evidence_confidence,
                "source": "manual",
            }
        ],
    }

    _save_profile(profile)
    print(f"[ultra-memory] ✅ 画像修正: {field_path}")
    print(f"  旧值: {old_value} (conf={old_confidence:.2f})")
    print(f"  新值: {new_value} (conf={evidence_confidence:.2f})")


# ── 时间戳更新 ─────────────────────────────────────────────────────────────


def update_reflection_timestamp():
    """Step 7A/7C 完成后更新 last_reflection 时间戳"""
    profile = _load_profile()
    profile["last_reflection"] = _now_iso()
    _save_profile(profile)


def update_distillation_timestamp():
    """Step 7C 完成后更新 last_distillation 时间戳"""
    profile = _load_profile()
    profile["last_distillation"] = _now_iso()
    _save_profile(profile)


# ── CLI ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="更新用户画像")
    parser.add_argument("--field", help="字段路径（dot-notation，如 tech_stack）")
    parser.add_argument("--value", help="新值")
    parser.add_argument("--evidence", type=float, default=0.8,
                        help="证据置信度 (0.0-1.0)")
    parser.add_argument("--source-session", default=None,
                        help="来源 session ID")
    parser.add_argument(
        "--correct", action="store_true",
        help="手动修正模式（强制覆盖旧值）"
    )
    parser.add_argument(
        "--update-reflection", action="store_true",
        help="仅更新时间戳"
    )
    args = parser.parse_args()

    if args.update_reflection:
        update_reflection_timestamp()
        print("[ultra-memory] ✅ last_reflection 已更新")
    elif args.correct and args.field and args.value is not None:
        correct_profile_field(
            args.field, args.value, args.evidence, args.source_session
        )
    elif args.field and args.value is not None:
        # 模拟 fact 结构
        fact = {
            "predicate": args.field,
            "subject": "",
            "object": args.value,
            "confidence": args.evidence,
        }
        update_profile_from_fact(fact, args.source_session or "cli")
    else:
        profile = _load_profile()
        print(f"[ultra-memory] 当前画像版本: {profile.get('version', '?')}")
        print(f"字段数: {len(profile.get('fields', {}))}")
        print(f"last_reflection: {profile.get('last_reflection')}")
        print(f"last_distillation: {profile.get('last_distillation')}")
        for path, data in profile.get("fields", {}).items():
            print(f"  {path}: {data.get('value')} "
                  f"(conf={data.get('confidence', 0):.2f}, "
                  f"n={data.get('evidence_count', 0)})")
