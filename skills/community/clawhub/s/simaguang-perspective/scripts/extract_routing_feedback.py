#!/usr/bin/env python3
"""Extract unresolved user corrections from learning log as routing feedback candidates."""

import datetime
import sys
from pathlib import Path

import project_paths
from review_learning_log import parse_entries, parse_feedback

ROOT = Path(__file__).resolve().parents[1]
PROJECT = project_paths.find_project_dir()
FEEDBACK = ROOT / "references" / "技能路由反馈日志.md"

PROCESS_MARKERS = [
    "无额外指令",
    "自动化任务",
    "后台 OCR",
    "全文 OCR",
    "用户上传",
    "用户提供",
    "用户确认执行",
    "用户确认后台",
    "用户确认理解",
    "用户同意",
    "用户要求继续",
    "用户询问",
    "按项目默认流程",
]


def main():
    if PROJECT is None:
        print(project_paths.project_dir_help(), file=sys.stderr)
        print("反馈候选来自外部项目学习日志，未解析到项目根时无法提取。", file=sys.stderr)
        return 2
    log = PROJECT / "学习记录" / "学习日志.md"
    if not log.is_file():
        print(f"学习日志不存在：{log}", file=sys.stderr)
        return 2
    entries = parse_entries(log.read_text(encoding="utf-8", errors="ignore"))
    feedback_text = (
        FEEDBACK.read_text(encoding="utf-8", errors="ignore")
        if FEEDBACK.exists()
        else ""
    )
    candidates = []
    process_skipped = 0
    for entry in entries:
        correction = entry["fields"].get("用户追问/纠正", "无")
        if correction in ("无", "-"):
            continue
        if correction in feedback_text:
            continue
        if any(marker in correction for marker in PROCESS_MARKERS):
            process_skipped += 1
            continue
        candidates.append((entry["date"], entry["title"], correction))

    today = datetime.date.today().isoformat()
    lines = [
        f"# 技能路由反馈候选 - {today}",
        "",
        f"- 候选数：{len(candidates)}",
        f"- 已跳过流程/确认类：{process_skipped}",
        "",
        "说明：以下纠正来自学习日志，尚未进入 `references/技能路由反馈日志.md`。是否算路由反馈、应建议哪条 trigger/exclude，需要人工复核后再回写。",
        "",
    ]
    for date, title, correction in candidates:
        lines.append(f"## {date} {title}")
        lines.append(f"- 用户追问/纠正：{correction}")
        lines.append("")

    out = PROJECT / "学习记录" / f"技能路由反馈候选-{today}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"candidates={len(candidates)} process_skipped={process_skipped}")
    print(f"report={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
