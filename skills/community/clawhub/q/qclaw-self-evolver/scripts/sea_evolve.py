#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEA 自我进化引擎 v4.0
Sense → Assess → Evolve 循环
给新 Agent 开箱即用的完整版

使用方式:
    python sea_evolve.py              # 完整运行
    python sea_evolve.py --sense      # 仅感知
    python sea_evolve.py --assess    # 仅评估
    python sea_evolve.py --quiet      # 无打扰模式（供 cron 使用）
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# 路径配置（适配 QClaw 和小/小皮等 Agent 环境）
# ============================================================
def _resolve_workspace():
    # 优先用环境变量，否则用 ~/.qclaw/workspace
    return os.path.expanduser(os.environ.get("QW_WORKSPACE", "~/.qclaw/workspace"))

WORKSPACE     = _resolve_workspace()
LEARNINGS_DIR = os.path.join(WORKSPACE, ".learnings")
SKILLS_DIR    = os.path.join(WORKSPACE, "skills")
SCRIPTS_DIR   = os.path.join(WORKSPACE, "scripts")
METRICS_FILE  = os.path.join(WORKSPACE, "skill_metrics.json")

os.makedirs(LEARNINGS_DIR, exist_ok=True)
os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# ============================================================
# 第一阶段：Sense（感知）
# ============================================================
def sense():
    """从学习档案中感知需要处理的内容"""
    findings = {
        "pending_corrections": [],
        "errors": [],
        "feature_requests": [],
        "high_priority": [],
        "repeated_patterns": [],
        "last_scan_time": datetime.now().isoformat(),
    }

    # 读取 LEARNINGS.md
    learnings_path = os.path.join(LEARNINGS_DIR, "LEARNINGS.md")
    if os.path.exists(learnings_path):
        with open(learnings_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取未处理的记录
        pending = re.findall(r'\|\s*(\d{4}-\d{2}-\d{2}[^|]*?)\s*\|[^|]*?\|[^|]*?\|([^|]*?)\|', content)
        for p in pending:
            entry_text = '|'.join(p).strip()
            if '未处理' in entry_text or '处理中' in entry_text:
                findings["pending_corrections"].append(entry_text)
            if 'Priority=高' in entry_text:
                findings["high_priority"].append(entry_text)

        # 识别重复模式（出现 ≥3 次）
        pattern_counts = {}
        for line in content.split('\n'):
            if '|' in line and '---' not in line and '错误做法' not in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    key = parts[1].strip() + '|' + parts[2].strip()
                    pattern_counts[key] = pattern_counts.get(key, 0) + 1
        findings["repeated_patterns"] = [
            {"pattern": k, "count": v}
            for k, v in pattern_counts.items() if v >= 3
        ]

    # 读取 ERRORS.md
    errors_path = os.path.join(LEARNINGS_DIR, "ERRORS.md")
    if os.path.exists(errors_path):
        with open(errors_path, "r", encoding="utf-8") as f:
            content = f.read()
        for line in content.split('\n'):
            if '|' in line and '---' not in line and '时间' not in line:
                findings["errors"].append(line.strip())

    # 读取 FEATURE_REQUESTS.md
    features_path = os.path.join(LEARNINGS_DIR, "FEATURE_REQUESTS.md")
    if os.path.exists(features_path):
        with open(features_path, "r", encoding="utf-8") as f:
            content = f.read()
        for line in content.split('\n'):
            if '|' in line and '---' not in line and '时间' not in line:
                findings["feature_requests"].append(line.strip())

    return findings

# ============================================================
# 第二阶段：Assess（评估）
# ============================================================
def assess():
    """诊断技能健康度"""
    from skill_metrics import load_metrics

    metrics = load_metrics()
    assessment = {
        "total_skills": len(metrics),
        "healthy": [],
        "needs_work": [],
        "critical": [],
        "untouched": [],
    }

    FALLBACK_WARN   = 0.4   # 选了这个技能但没用的比例警告线
    COMPLETION_WARN = 0.35  # 完成率警戒线

    for skill_id, m in metrics.items():
        total = max(1, m["total_selections"])
        fallback    = (total - m["total_applied"]) / total
        completion  = m["total_completed"] / total if m["total_applied"] > 0 else 0

        if fallback > FALLBACK_WARN:
            assessment["critical"].append({
                "skill": skill_id,
                "fallback_rate": round(fallback, 2),
                "completion": round(completion, 2),
                "reason": f"有 {int(fallback*100)}% 的时间选了它但没用"
            })
        elif completion < COMPLETION_WARN:
            assessment["needs_work"].append({
                "skill": skill_id,
                "fallback_rate": round(fallback, 2),
                "completion": round(completion, 2),
                "reason": f"完成率仅 {int(completion*100)}%"
            })
        else:
            assessment["healthy"].append(skill_id)

    return assessment

# ============================================================
# 第三阶段：Evolve（进化）
# ============================================================
def evolve(sense_data, assess_data, quiet=False):
    """根据感知和评估结果执行进化"""
    actions = []
    improvements = []

    # 处理高优先级纠正
    if sense_data["high_priority"]:
        for entry in sense_data["high_priority"]:
            actions.append(f"⚡ 立即处理高优先级纠正: {entry[:60]}")
            improvements.append(entry)

    # 处理重复模式
    for rp in sense_data["repeated_patterns"]:
        pattern = rp["pattern"]
        count = rp["count"]
        if count >= 3:
            # 识别为可固化的模式，触发技能自进化
            actions.append(f"🔧 检测到重复模式 ×{count}: {pattern[:40]}")
            # 这里只记录，实际生成由 skill_evolution.py 处理
            improvements.append(f"触发技能生成: {pattern}")

    # 处理错误记录
    if sense_data["errors"]:
        actions.append(f"📋 {len(sense_data['errors'])} 条错误待处理")
        for err in sense_data["errors"][:3]:
            improvements.append(err)

    # 生成进化报告
    report = _build_report(sense_data, assess_data, actions, improvements)

    if not quiet:
        print(report)

    return report, actions, improvements

def _build_report(sense_data, assess_data, actions, improvements):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"## 🌱 SEA 进化报告 — {now}",
        "",
        "### Sense（感知）",
        f"- 待处理纠正：{len(sense_data['pending_corrections'])} 条",
        f"- 错误记录：{len(sense_data['errors'])} 条",
        f"- 重复模式：{len(sense_data['repeated_patterns'])} 条",
        f"- 高优先级：{len(sense_data['high_priority'])} 条",
        "",
        "### Assess（评估）",
        f"- 总技能数：{assess_data['total_skills']}",
        f"- 健康技能：{len(assess_data['healthy'])}",
        f"- 需改进：{len(assess_data['needs_work'])}",
        f"- 警戒：{len(assess_data['critical'])}",
        "",
        "### Evolve（进化）",
    ]
    for a in actions:
        lines.append(f"- {a}")

    if not actions:
        lines.append("- ✅ 无需进化，状态良好")

    lines.append("")
    lines.append("### 建议")
    if improvements:
        for imp in improvements[:3]:
            lines.append(f"- 考虑：{imp[:80]}")
    else:
        lines.append("- 继续保持当前工作状态")

    return '\n'.join(lines)

# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="SEA 自我进化引擎")
    parser.add_argument("--sense",  action="store_true", help="仅运行感知阶段")
    parser.add_argument("--assess", action="store_true", help="仅运行评估阶段")
    parser.add_argument("--evolve", action="store_true", help="仅运行进化阶段")
    parser.add_argument("--quiet",  action="store_true", help="静默模式（供 cron 使用）")
    parser.add_argument("--report", action="store_true", help="输出完整报告")
    args = parser.parse_args()

    if args.sense:
        data = sense()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if args.assess:
        data = assess()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    # 默认：完整 SEA 循环
    sense_data    = sense()
    assess_data   = assess()
    report, _, _  = evolve(sense_data, assess_data, quiet=args.quiet)

    if args.report or not args.quiet:
        print(report)

if __name__ == "__main__":
    main()
