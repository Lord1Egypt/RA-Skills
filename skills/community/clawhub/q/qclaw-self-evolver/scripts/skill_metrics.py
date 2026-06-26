#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能指标系统 - 轻量版
记录每个 skill 被选中和使用的频率，供 SEA 引擎评估技能健康度
"""

import os
import json
from datetime import datetime

def _resolve_workspace():
    return os.path.expanduser(os.environ.get("QW_WORKSPACE", "~/.qclaw/workspace"))

WORKSPACE    = _resolve_workspace()
METRICS_FILE = os.path.join(WORKSPACE, "skill_metrics.json")

def load_metrics():
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metrics(metrics):
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

def record(skill_id: str, applied: bool = False, completed: bool = False, effective: bool = False):
    """记录一次技能使用"""
    metrics = load_metrics()
    if skill_id not in metrics:
        metrics[skill_id] = {
            "total_selections": 0,
            "total_applied": 0,
            "total_completed": 0,
            "total_effective": 0,
            "first_seen": datetime.now().isoformat(),
            "last_used": None,
        }
    m = metrics[skill_id]
    m["total_selections"] += 1
    if applied:     m["total_applied"] += 1
    if completed:   m["total_completed"] += 1
    if effective:   m["total_effective"] += 1
    m["last_used"] = datetime.now().isoformat()
    save_metrics(metrics)
    return m

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--applied", action="store_true")
    parser.add_argument("--completed", action="store_true")
    parser.add_argument("--effective", action="store_true")
    args = parser.parse_args()
    m = record(args.skill, args.applied, args.completed, args.effective)
    print(f"已记录 → {args.skill}: selections={m['total_selections']}")
