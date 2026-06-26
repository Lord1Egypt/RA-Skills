#!/usr/bin/env python3
"""口才陪练龙虾 — 用户进步追踪系统

提供 15 步训练进度管理、多维评分、里程碑检测和周报生成。
供 SKILL.md 通过 exec 调用。

Author: openclaw-user
Version: 1.0.0
License: MIT
"""

import os
import io
import json
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace"
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding="utf-8", errors="replace"
    )


WORKSPACE = Path(os.environ.get(
    "SPEECH_COACH_DIR",
    os.path.expanduser("~/.openclaw/workspace/speech-coach")
))

PROGRESS_FILE = WORKSPACE / "progress.json"
SESSIONS_FILE = WORKSPACE / "sessions.json"
PROFILE_FILE = WORKSPACE / "user_profile.json"

STEPS = {
    1:  {"name": "体态训练",           "module": 1, "phase": "基础", "pass_score": 6},
    2:  {"name": "目光训练",           "module": 1, "phase": "基础", "pass_score": 6},
    3:  {"name": "手势训练",           "module": 1, "phase": "基础", "pass_score": 6},
    4:  {"name": "声音训练",           "module": 1, "phase": "基础", "pass_score": 6},
    5:  {"name": "表情训练",           "module": 1, "phase": "基础", "pass_score": 6},
    6:  {"name": "综合实战·自我介绍",  "module": 1, "phase": "基础", "pass_score": 6},
    7:  {"name": "金字塔讲话思路",     "module": 2, "phase": "基础", "pass_score": 6},
    8:  {"name": "黄金三点结构",       "module": 2, "phase": "基础", "pass_score": 6},
    9:  {"name": "鞋挂法讲故事",       "module": 2, "phase": "基础", "pass_score": 6},
    10: {"name": "综合实战·主题演讲",  "module": 2, "phase": "基础", "pass_score": 7},
    11: {"name": "降落伞思路",         "module": 3, "phase": "应用", "pass_score": 7},
    12: {"name": "楼梯切入法",         "module": 3, "phase": "应用", "pass_score": 7},
    13: {"name": "口吐莲花法",         "module": 3, "phase": "应用", "pass_score": 7},
    14: {"name": "千斤法诤言思路",     "module": 3, "phase": "应用", "pass_score": 7},
    15: {"name": "毕业实战·综合演讲",  "module": 4, "phase": "应用", "pass_score": 8},
}

SCORE_DIMENSIONS = [
    "annotation", "structure", "logic",
    "storytelling", "improvisation", "persuasion",
    "knowledge",
]

DIMENSION_LABELS = {
    "annotation": "标注设计", "structure": "结构",
    "logic": "逻辑", "storytelling": "叙事",
    "improvisation": "即兴", "persuasion": "说服力",
    "knowledge": "方法理解",
}

MILESTONES = [
    {"id": "first_session",      "label": "🎉 首次训练完成",        "condition": "sessions >= 1"},
    {"id": "overcome_tension",   "label": "💪 克服紧张 (Module 1)",  "condition": "step >= 7"},
    {"id": "clear_expression",   "label": "🧠 清晰表达 (Module 2)",  "condition": "step >= 11"},
    {"id": "improv_ready",       "label": "⚡ 即兴达人 (Module 3)",   "condition": "step >= 15"},
    {"id": "graduated",          "label": "🎓 毕业！全部通关",       "condition": "step > 15"},
    {"id": "ten_sessions",       "label": "🔥 坚持 10 次训练",       "condition": "sessions >= 10"},
    {"id": "twenty_sessions",    "label": "🏆 坚持 20 次训练",       "condition": "sessions >= 20"},
    {"id": "perfect_score",      "label": "⭐ 获得单项满分",         "condition": "any_score_10"},
    {"id": "all_above_7",        "label": "🌟 七维度均 7 分以上",     "condition": "all_dims >= 7"},
]


def ensure_workspace():
    WORKSPACE.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(path: Path, data: dict):
    ensure_workspace()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def init_progress() -> dict:
    progress = {
        "current_step": 1,
        "training_steps": {},
        "milestones_achieved": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    for step_num, info in STEPS.items():
        key = f"step_{step_num:02d}"
        progress["training_steps"][key] = {
            "name": info["name"],
            "module": info["module"],
            "phase": info["phase"],
            "status": "in_progress" if step_num == 1 else "locked",
            "best_score": None,
            "latest_score": None,
            "session_count": 0,
            "scores_history": [],
        }
    return progress


def get_progress() -> dict:
    data = load_json(PROGRESS_FILE)
    if not data:
        data = init_progress()
        save_json(PROGRESS_FILE, data)
    return data


def get_sessions() -> list:
    data = load_json(SESSIONS_FILE)
    return data.get("sessions", [])


def save_sessions(sessions: list):
    save_json(SESSIONS_FILE, {"sessions": sessions})


def total_sessions() -> int:
    return len(get_sessions())


def record_score(step: int, scores: Dict[str, int], note: str = "") -> dict:
    """记录一次训练评分。"""
    progress = get_progress()
    key = f"step_{step:02d}"

    if key not in progress["training_steps"]:
        return {"error": f"无效的步骤编号: {step}"}

    step_data = progress["training_steps"][key]

    valid_scores = {k: v for k, v in scores.items() if k in SCORE_DIMENSIONS}
    avg = round(sum(valid_scores.values()) / len(valid_scores), 1) if valid_scores else 0

    session_record = {
        "timestamp": datetime.now().isoformat(),
        "scores": valid_scores,
        "average": avg,
        "note": note,
    }

    step_data["scores_history"].append(session_record)
    step_data["latest_score"] = avg
    step_data["session_count"] += 1
    step_data["status"] = "in_progress"

    if step_data["best_score"] is None or avg > step_data["best_score"]:
        step_data["best_score"] = avg

    pass_score = STEPS[step]["pass_score"]
    if avg >= pass_score:
        step_data["status"] = "completed"

    progress["training_steps"][key] = step_data
    progress["updated_at"] = datetime.now().isoformat()

    sessions = get_sessions()
    sessions.append(session_record | {"step": step, "step_name": STEPS[step]["name"]})
    save_sessions(sessions)

    check_milestones(progress)
    save_json(PROGRESS_FILE, progress)

    result = {
        "step": step,
        "step_name": STEPS[step]["name"],
        "scores": valid_scores,
        "average": avg,
        "pass_score": pass_score,
        "passed": avg >= pass_score,
        "best_score": step_data["best_score"],
        "session_count": step_data["session_count"],
    }

    if avg >= pass_score:
        result["message"] = f"恭喜通过 Step {step:02d}！"
        if step < 15:
            result["next_step"] = step + 1
            result["next_step_name"] = STEPS[step + 1]["name"]
    else:
        gap = round(pass_score - avg, 1)
        result["message"] = f"距离通过还差 {gap} 分，继续加油！"
        weakest = min(valid_scores, key=valid_scores.get) if valid_scores else None
        if weakest:
            result["focus_area"] = DIMENSION_LABELS.get(weakest, weakest)

    return result


def unlock_step(step: int) -> dict:
    """解锁指定步骤。"""
    progress = get_progress()
    key = f"step_{step:02d}"

    if key not in progress["training_steps"]:
        return {"error": f"无效的步骤编号: {step}"}

    step_data = progress["training_steps"][key]
    if step_data["status"] == "locked":
        step_data["status"] = "in_progress"
    progress["training_steps"][key] = step_data

    if step > progress.get("current_step", 1):
        progress["current_step"] = step

    progress["updated_at"] = datetime.now().isoformat()
    save_json(PROGRESS_FILE, progress)

    return {"unlocked": step, "name": STEPS[step]["name"], "status": "in_progress"}


def check_milestones(progress: dict):
    """检查并触发里程碑。"""
    achieved = set(progress.get("milestones_achieved", []))
    current = progress.get("current_step", 1)
    sessions_count = total_sessions()

    completed_steps = [
        k for k, v in progress["training_steps"].items()
        if v["status"] == "completed"
    ]
    farthest_completed = max(
        (int(k.split("_")[1]) for k in completed_steps), default=0
    )
    effective_step = farthest_completed + 1

    all_latest = {}
    any_10 = False
    for step_key, step_data in progress["training_steps"].items():
        if step_data["scores_history"]:
            last = step_data["scores_history"][-1]["scores"]
            all_latest.update(last)
            if any(v >= 10 for v in last.values()):
                any_10 = True

    for m in MILESTONES:
        if m["id"] in achieved:
            continue
        cond = m["condition"]
        triggered = False
        if cond.startswith("sessions >="):
            threshold = int(cond.split(">=")[1].strip())
            triggered = sessions_count >= threshold
        elif cond.startswith("step >="):
            threshold = int(cond.split(">=")[1].strip())
            triggered = effective_step >= threshold
        elif cond.startswith("step >"):
            threshold = int(cond.split(">")[1].strip())
            triggered = effective_step > threshold
        elif cond == "any_score_10":
            triggered = any_10
        elif cond.startswith("all_dims >="):
            threshold = int(cond.split(">=")[1].strip())
            if all_latest:
                triggered = all(v >= threshold for v in all_latest.values())

        if triggered:
            achieved.add(m["id"])

    progress["milestones_achieved"] = list(achieved)


def get_status() -> dict:
    """获取当前训练状态总览。"""
    progress = get_progress()
    sessions_count = total_sessions()

    steps_summary = []
    for step_num in sorted(STEPS.keys()):
        key = f"step_{step_num:02d}"
        sd = progress["training_steps"].get(key, {})
        status_icon = {
            "completed": "✅", "in_progress": "🔵", "locked": "🔒"
        }.get(sd.get("status", "locked"), "❓")

        steps_summary.append({
            "step": step_num,
            "name": STEPS[step_num]["name"],
            "status": sd.get("status", "locked"),
            "icon": status_icon,
            "best_score": sd.get("best_score"),
            "sessions": sd.get("session_count", 0),
        })

    completed_count = sum(1 for s in steps_summary if s["status"] == "completed")
    overall_pct = round(completed_count / len(STEPS) * 100)

    achieved_milestones = progress.get("milestones_achieved", [])
    milestones_display = []
    for m in MILESTONES:
        milestones_display.append({
            "label": m["label"],
            "achieved": m["id"] in achieved_milestones,
        })

    return {
        "current_step": progress.get("current_step", 1),
        "completed_steps": completed_count,
        "total_steps": len(STEPS),
        "progress_pct": overall_pct,
        "total_sessions": sessions_count,
        "steps": steps_summary,
        "milestones": milestones_display,
    }


def get_step_detail(step: int) -> dict:
    """获取指定步骤的详细信息。"""
    if step not in STEPS:
        return {"error": f"无效的步骤编号: {step}"}

    progress = get_progress()
    key = f"step_{step:02d}"
    sd = progress["training_steps"].get(key, {})

    info = STEPS[step].copy()
    info["step"] = step
    info["status"] = sd.get("status", "locked")
    info["best_score"] = sd.get("best_score")
    info["latest_score"] = sd.get("latest_score")
    info["session_count"] = sd.get("session_count", 0)

    history = sd.get("scores_history", [])
    if history:
        latest = history[-1]
        info["latest_detail"] = latest
        if len(history) >= 2:
            prev_avg = history[-2]["average"]
            curr_avg = latest["average"]
            info["trend"] = round(curr_avg - prev_avg, 1)
            info["trend_label"] = "📈 进步" if info["trend"] > 0 else (
                "📉 退步" if info["trend"] < 0 else "➡️ 持平"
            )

        all_dims_latest = latest.get("scores", {})
        if all_dims_latest:
            strongest = max(all_dims_latest, key=all_dims_latest.get)
            weakest = min(all_dims_latest, key=all_dims_latest.get)
            info["strongest"] = DIMENSION_LABELS.get(strongest, strongest)
            info["weakest"] = DIMENSION_LABELS.get(weakest, weakest)

    return info


def generate_report() -> str:
    """生成训练周报。"""
    progress = get_progress()
    sessions = get_sessions()
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    week_sessions = [
        s for s in sessions
        if datetime.fromisoformat(s["timestamp"]) >= week_ago
    ]

    status = get_status()

    lines = [
        "# 🦞 口才陪练龙虾 · 训练周报",
        f"生成时间：{now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 📊 总体进度",
        f"- 当前步骤：Step {status['current_step']:02d} — {STEPS.get(status['current_step'], {}).get('name', '已毕业')}",
        f"- 完成进度：{status['completed_steps']}/{status['total_steps']}（{status['progress_pct']}%）",
        f"- 累计训练：{status['total_sessions']} 次",
        f"- 本周训练：{len(week_sessions)} 次",
        "",
    ]

    progress_bar_len = 15
    filled = round(status["progress_pct"] / 100 * progress_bar_len)
    bar = "█" * filled + "░" * (progress_bar_len - filled)
    lines.append(f"进度条：[{bar}] {status['progress_pct']}%")
    lines.append("")

    if week_sessions:
        lines.append("## 📈 本周训练记录")
        lines.append("")
        lines.append("| 日期 | 步骤 | 平均分 | 备注 |")
        lines.append("|------|------|--------|------|")
        for s in week_sessions:
            ts = datetime.fromisoformat(s["timestamp"]).strftime("%m-%d %H:%M")
            step_name = s.get("step_name", f"Step {s.get('step', '?')}")
            avg = s.get("average", "-")
            note = s.get("note", "")[:20]
            lines.append(f"| {ts} | {step_name} | {avg} | {note} |")
        lines.append("")

        week_scores: Dict[str, List[int]] = {}
        for s in week_sessions:
            for dim, val in s.get("scores", {}).items():
                week_scores.setdefault(dim, []).append(val)

        if week_scores:
            lines.append("## 🎯 本周各维度平均分")
            lines.append("")
            for dim in SCORE_DIMENSIONS:
                if dim in week_scores:
                    vals = week_scores[dim]
                    avg = round(sum(vals) / len(vals), 1)
                    label = DIMENSION_LABELS.get(dim, dim)
                    bar_filled = round(avg)
                    dim_bar = "■" * bar_filled + "□" * (10 - bar_filled)
                    lines.append(f"- {label}：{dim_bar} {avg}/10")
            lines.append("")
    else:
        lines.append("## 📈 本周训练记录")
        lines.append("")
        lines.append("本周暂无训练记录，记得保持练习节奏！")
        lines.append("")

    lines.append("## 🏅 里程碑")
    lines.append("")
    for m in status["milestones"]:
        icon = "✅" if m["achieved"] else "⬜"
        lines.append(f"- {icon} {m['label']}")
    lines.append("")

    all_scores_by_dim: Dict[str, List[int]] = {}
    for s in sessions:
        for dim, val in s.get("scores", {}).items():
            all_scores_by_dim.setdefault(dim, []).append(val)

    if all_scores_by_dim:
        strongest_dim = max(
            all_scores_by_dim,
            key=lambda d: sum(all_scores_by_dim[d]) / len(all_scores_by_dim[d])
        )
        weakest_dim = min(
            all_scores_by_dim,
            key=lambda d: sum(all_scores_by_dim[d]) / len(all_scores_by_dim[d])
        )
        lines.append("## 💡 教练建议")
        lines.append("")
        lines.append(f"- **最强维度**：{DIMENSION_LABELS.get(strongest_dim, strongest_dim)} — 继续保持！")
        lines.append(f"- **待提升维度**：{DIMENSION_LABELS.get(weakest_dim, weakest_dim)} — 建议在日常中多刻意练习")

        if len(sessions) >= 5 and not week_sessions:
            lines.append("- ⚠️ 本周没有训练记录，坚持练习才能巩固进步！")
        elif len(week_sessions) >= 3:
            lines.append("- 🔥 本周训练频率很棒！保持这个节奏！")
        lines.append("")

    lines.extend([
        "---",
        "*口才不是天赋，是技能。每一次练习，都在离更好的自己更近一步。* 🦞",
    ])

    return "\n".join(lines)


def format_status_text(status: dict) -> str:
    """将状态数据格式化为可读文本。"""
    lines = [
        "🦞 口才陪练龙虾 · 训练状态",
        f"当前步骤：Step {status['current_step']:02d}",
        f"完成进度：{status['completed_steps']}/{status['total_steps']}（{status['progress_pct']}%）",
        f"累计训练：{status['total_sessions']} 次",
        "",
        "训练步骤：",
    ]
    for s in status["steps"]:
        score_str = f"  最高 {s['best_score']}" if s["best_score"] else ""
        sessions_str = f"  ({s['sessions']}次)" if s["sessions"] else ""
        lines.append(f"  {s['icon']} Step {s['step']:02d} {s['name']}{score_str}{sessions_str}")

    lines.append("")
    lines.append("里程碑：")
    for m in status["milestones"]:
        icon = "✅" if m["achieved"] else "⬜"
        lines.append(f"  {icon} {m['label']}")

    return "\n".join(lines)


def format_step_detail_text(detail: dict) -> str:
    """将步骤详情格式化为可读文本。"""
    if "error" in detail:
        return f"错误：{detail['error']}"

    lines = [
        f"📋 Step {detail['step']:02d} — {detail['name']}",
        f"阶段：{detail['phase']}（Module {detail['module']}）",
        f"状态：{detail['status']}",
        f"通过分数：{detail['pass_score']}",
        f"最高分：{detail.get('best_score', '暂无')}",
        f"最近分：{detail.get('latest_score', '暂无')}",
        f"训练次数：{detail.get('session_count', 0)}",
    ]

    if "trend_label" in detail:
        lines.append(f"趋势：{detail['trend_label']}（{'+' if detail['trend'] > 0 else ''}{detail['trend']}）")
    if "strongest" in detail:
        lines.append(f"最强维度：{detail['strongest']}")
    if "weakest" in detail:
        lines.append(f"待提升：{detail['weakest']}")

    if "latest_detail" in detail:
        lines.append("")
        lines.append("最近一次评分：")
        for dim, val in detail["latest_detail"].get("scores", {}).items():
            label = DIMENSION_LABELS.get(dim, dim)
            lines.append(f"  {label}：{val}/10")
        if detail["latest_detail"].get("note"):
            lines.append(f"  备注：{detail['latest_detail']['note']}")

    return "\n".join(lines)


def format_score_result_text(result: dict) -> str:
    """将评分结果格式化为可读文本。"""
    if "error" in result:
        return f"错误：{result['error']}"

    lines = [
        f"📝 评分记录 — Step {result['step']:02d} {result['step_name']}",
        "",
    ]

    for dim, val in result["scores"].items():
        label = DIMENSION_LABELS.get(dim, dim)
        bar = "■" * val + "□" * (10 - val)
        lines.append(f"  {label}：{bar} {val}/10")

    lines.append("")
    lines.append(f"  平均分：{result['average']}  |  通过线：{result['pass_score']}  |  历史最高：{result['best_score']}")
    lines.append(f"  本步训练次数：{result['session_count']}")
    lines.append("")
    lines.append(f"  {'✅' if result['passed'] else '🔵'} {result['message']}")

    if "next_step_name" in result:
        lines.append(f"  ➡️ 下一步：Step {result['next_step']:02d} {result['next_step_name']}")
    if "focus_area" in result:
        lines.append(f"  🎯 重点关注：{result['focus_area']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="口才陪练龙虾 · 进步追踪系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python progress_tracker.py status\n"
               "  python progress_tracker.py score --step 1 --posture 7 --eye-contact 6 --gesture 5 --voice 7 --expression 6 --rhythm 6 --structure 5 --logic 6 --improvisation 5 --persuasion 5\n"
               "  python progress_tracker.py unlock --step 2\n"
               "  python progress_tracker.py report\n"
               "  python progress_tracker.py milestones\n"
               "  python progress_tracker.py step-detail --step 3\n"
    )

    sub = parser.add_subparsers(dest="command", help="可用命令")

    sub.add_parser("status", help="查看训练状态总览")

    score_p = sub.add_parser("score", help="记录训练评分")
    score_p.add_argument("--step", type=int, required=True, help="步骤编号 (1-15)")
    score_p.add_argument("--annotation", type=int, default=0, help="标注设计 (1-10)")
    score_p.add_argument("--structure", type=int, default=0, help="结构 (1-10)")
    score_p.add_argument("--logic", type=int, default=0, help="逻辑 (1-10)")
    score_p.add_argument("--storytelling", type=int, default=0, help="叙事 (1-10)")
    score_p.add_argument("--improvisation", type=int, default=0, help="即兴 (1-10)")
    score_p.add_argument("--persuasion", type=int, default=0, help="说服力 (1-10)")
    score_p.add_argument("--knowledge", type=int, default=0, help="方法理解 (1-10)")
    score_p.add_argument("--note", type=str, default="", help="训练备注")

    unlock_p = sub.add_parser("unlock", help="解锁指定步骤")
    unlock_p.add_argument("--step", type=int, required=True, help="步骤编号")

    sub.add_parser("report", help="生成训练周报")
    sub.add_parser("milestones", help="查看里程碑")

    detail_p = sub.add_parser("step-detail", help="查看步骤详情")
    detail_p.add_argument("--step", type=int, required=True, help="步骤编号")

    sub.add_parser("reset", help="重置所有训练数据（需确认）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    ensure_workspace()

    if args.command == "status":
        status = get_status()
        print(format_status_text(status))

    elif args.command == "score":
        scores = {}
        if args.annotation:    scores["annotation"] = max(1, min(10, args.annotation))
        if args.structure:     scores["structure"] = max(1, min(10, args.structure))
        if args.logic:         scores["logic"] = max(1, min(10, args.logic))
        if args.storytelling:  scores["storytelling"] = max(1, min(10, args.storytelling))
        if args.improvisation: scores["improvisation"] = max(1, min(10, args.improvisation))
        if args.persuasion:    scores["persuasion"] = max(1, min(10, args.persuasion))
        if args.knowledge:     scores["knowledge"] = max(1, min(10, args.knowledge))

        if not scores:
            print("错误：至少需要提供一项评分")
            sys.exit(1)

        result = record_score(args.step, scores, args.note)
        print(format_score_result_text(result))

    elif args.command == "unlock":
        result = unlock_step(args.step)
        if "error" in result:
            print(f"错误：{result['error']}")
        else:
            print(f"✅ 已解锁 Step {result['unlocked']:02d} — {result['name']}")

    elif args.command == "report":
        print(generate_report())

    elif args.command == "milestones":
        status = get_status()
        print("🏅 里程碑")
        for m in status["milestones"]:
            icon = "✅" if m["achieved"] else "⬜"
            print(f"  {icon} {m['label']}")

    elif args.command == "step-detail":
        detail = get_step_detail(args.step)
        print(format_step_detail_text(detail))

    elif args.command == "reset":
        confirm = input("⚠️ 确定要重置所有训练数据吗？输入 YES 确认：")
        if confirm.strip() == "YES":
            progress = init_progress()
            save_json(PROGRESS_FILE, progress)
            save_sessions([])
            print("✅ 训练数据已重置")
        else:
            print("❌ 取消重置")


if __name__ == "__main__":
    main()
