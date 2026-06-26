"""
resume-rocket · 主入口
用法见 SKILL.md
"""
from __future__ import annotations
import argparse
import io
import json
import os
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from typing import Literal

from lib.parser import parse_resume
from lib.jd_fetcher import fetch_jd
from lib.matcher import score_match
from lib.rewriter import rewrite_resume
from lib.interview import generate_interview_cards
from lib.license import check_tier
from lib.exporter import export_docx, export_markdown


def cmd_rewrite(args: argparse.Namespace) -> int:
    tier: Literal["free", "single", "monthly", "pro"] = check_tier(args.tier)
    print(f"[Resume Rocket] 服务档位: {tier}")

    resume = parse_resume(Path(args.resume))
    print(f"[Resume Rocket] 简历解析完成: {len(resume.experiences)} 段工作经历, {len(resume.skills)} 项技能")

    jd = fetch_jd(args.jd)
    print(f"[Resume Rocket] JD 已加载: {jd.title} @ {jd.company}")

    score = score_match(resume, jd)
    print(f"[Resume Rocket] 匹配度: {score.total}/100")

    rewritten = rewrite_resume(resume, jd, score)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    export_docx(rewritten, out_dir / "resume-optimized.docx")
    export_markdown(score.report(), out_dir / "match-report.md")

    if tier in ("single", "monthly", "pro"):
        cards = generate_interview_cards(resume, jd, n=10)
        export_markdown(cards, out_dir / "interview-cards.md")
        print(f"[Resume Rocket] 面试卡 10 张已生成")
    else:
        print("[Resume Rocket] 免费版不含面试卡，升级 ¥29 单次 / ¥99 月卡解锁")

    print(f"[Resume Rocket] ✅ 输出目录: {out_dir.resolve()}")
    return 0


def cmd_match_score(args: argparse.Namespace) -> int:
    resume = parse_resume(Path(args.resume))
    jd = fetch_jd(args.jd)
    score = score_match(resume, jd)
    print(score.report())
    return 0


def cmd_auto_apply(args: argparse.Namespace) -> int:
    tier = check_tier("pro")
    if tier != "pro":
        print("[Resume Rocket] ❌ auto-apply 仅 Pro 版支持（¥299/月）")
        return 2
    from lib.auto_apply import run_batch
    run_batch(
        jd_list=Path(args.jd_list),
        resume_base=Path(args.resume_base),
        daily_limit=args.daily_limit,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="resume-rocket")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_rewrite = sub.add_parser("rewrite", help="改写简历")
    p_rewrite.add_argument("--resume", required=True)
    p_rewrite.add_argument("--jd", required=True)
    p_rewrite.add_argument("--output", default="./output")
    p_rewrite.add_argument("--tier", default="free")
    p_rewrite.set_defaults(func=cmd_rewrite)

    p_score = sub.add_parser("match-score", help="只算匹配度")
    p_score.add_argument("--resume", required=True)
    p_score.add_argument("--jd", required=True)
    p_score.set_defaults(func=cmd_match_score)

    p_apply = sub.add_parser("auto-apply", help="[Pro] 批量投递")
    p_apply.add_argument("--jd-list", required=True)
    p_apply.add_argument("--resume-base", required=True)
    p_apply.add_argument("--daily-limit", type=int, default=50)
    p_apply.set_defaults(func=cmd_auto_apply)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
