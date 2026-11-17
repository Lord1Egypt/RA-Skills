#!/usr/bin/env python3
"""
审稿检查点生成工具 — 在审稿开始时生成初始化 checklist.json

用法：
  python3 init_checklist.py <article-name> [draft-version] [reviewer]

输出：
  输出检查点 JSON 到 docs/reviews/<article-name>/checklist.json

使用流程：
  1. 审稿开始时，运行此脚本生成初始 checklist
  2. 每完成一个阶段，补充对应字段
  3. 审稿结束时，运行 validate_pipeline.py 验证完整性
"""

import json
import os
import sys
from datetime import datetime


def make_checklist(article_name, draft_version="v1", reviewer="笔探"):
    """生成审稿检查点 JSON"""
    checklist = {
        "schema": f"openclaw.review.checklist.v1",
        "meta": {
            "article": article_name,
            "draft_version": draft_version,
            "review_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "reviewer": reviewer,
        },
        "checks": {
            # 必检——未通过则不能发布
            "mandatory": {
                "source_material_verification": {
                    "passed": False,
                    "description": "素材对照（建立素材事实清单 → 逐句比对 → 输出对照表）",
                    "details": []
                },
                "fact_check_6_types": {
                    "passed": False,
                    "description": "6类风险审查（数字/概念/因果/绝对化/记忆/应然）",
                    "details": []
                },
                "concept_frequency": {
                    "passed": False,
                    "description": "概念频率检查（跨幕/跨段概念热力图）",
                    "details": []
                },
                "topic_consistency": {
                    "passed": False,
                    "description": "一句话定题（全文是不是一个核心）",
                    "details": []
                },
                "privacy_check": {
                    "passed": False,
                    "description": "隐私/收入敏感度检查",
                    "details": []
                },
                "hard_issues_tracked": {
                    "passed": False,
                    "description": "硬伤清单（🔴必须改的项有跟踪）",
                    "details": []
                },
            },
            # 建议检——能过最好，不过不影响发布
            "suggested": {
                "style_consistency": {
                    "passed": False,
                    "description": "风格一致性检查（voice漂移/解释段/升维/结尾拔高）",
                    "details": []
                },
                "reader_simulation": {
                    "passed": False,
                    "description": "逐句读者模拟",
                    "details": []
                },
                "structure_evaluation": {
                    "passed": False,
                    "description": "结构/洞察/传播力/反AI味评估",
                    "details": []
                },
                "audience_takeaway": {
                    "passed": False,
                    "description": "听众带走什么分析",
                    "details": []
                },
                "dialogue_rhythm": {
                    "passed": False,
                    "description": "对话节奏检查（适用于双人稿）",
                    "details": []
                },
                "ending_matches_core": {
                    "passed": False,
                    "description": "结尾是否回应前文最重矛盾",
                    "details": []
                },
            },
            # 可选——锦上添花
            "optional": {
                "gpt_second_opinion": {
                    "passed": False,
                    "description": "ChatGPT 次审",
                    "details": []
                },
                "cross_episode_consistency": {
                    "passed": False,
                    "description": "跨集一致性（系列内容用）",
                    "details": []
                },
                "fix_tracking": {
                    "passed": False,
                    "description": "修复跟踪（多轮迭代用）",
                    "details": []
                },
            }
        }
    }
    return checklist


def main():
    if len(sys.argv) < 2:
        print(f"用法: python3 {sys.argv[0]} <article-name> [draft-version] [reviewer]")
        print(f"示例: python3 init_checklist.py llm-wiki-todo v2")
        sys.exit(2)

    article = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else "v1"
    reviewer = sys.argv[3] if len(sys.argv) > 3 else "笔探"

    review_dir = os.path.join("docs", "reviews", article)
    os.makedirs(review_dir, exist_ok=True)

    checklist = make_checklist(article, version, reviewer)
    output_path = os.path.join(review_dir, "checklist.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(checklist, f, ensure_ascii=False, indent=2)

    items = {
        "mandatory": len(checklist["checks"]["mandatory"]),
        "suggested": len(checklist["checks"]["suggested"]),
        "optional": len(checklist["checks"]["optional"]),
    }
    print(f"✅ 检查点已初始化: {output_path}")
    print(f"   必检 {items['mandatory']} 项 + 建议检 {items['suggested']} 项 + 可选 {items['optional']} 项")
    print(f"   文章: {article}")
    print(f"   版本: {version}")
    print(f"   审稿: {reviewer}")
    print(f"   日期: {checklist['meta']['review_date']}")


if __name__ == "__main__":
    main()
