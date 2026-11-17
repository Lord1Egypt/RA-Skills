#!/usr/bin/env python3
"""Run mechanical pre-delivery checks on a high-productivity output file."""

import argparse
import re
import sys
from pathlib import Path


CHECKS = {
    "ppt": [
        ("价值主张", r"价值|一句话|痛点"),
        ("行动入口", r"下一步|行动|联系|融资|合作"),
        ("数据来源", r"来源|数据|待核验"),
    ],
    "project-plan": [
        ("定位与目标", r"定位|目标|价值"),
        ("主备路径", r"备选|路径|方案"),
        ("风险", r"风险"),
        ("复查指标", r"复查|指标|失效|节点"),
    ],
    "bid": [
        ("响应评分", r"评分|响应|要求|标准"),
        ("资质合规", r"资质|合规|证明|盖章"),
        ("方案", r"方案|实施|计划"),
    ],
    "thesis-defense": [
        ("研究问题", r"问题|研究|目标"),
        ("方法", r"方法|数据|分析"),
        ("局限", r"局限|不足|下一步"),
    ],
    "debate": [
        ("立场", r"立场|观点|主张"),
        ("判准", r"判准|定义|标准"),
        ("反方", r"反方|反对|质疑"),
    ],
    "business-plan": [
        ("痛点", r"痛点|问题|需求"),
        ("方案", r"方案|产品|服务"),
        ("商业模式", r"付费|收入|模式|成本"),
        ("风险", r"风险|退出|失效"),
    ],
    "report": [
        ("结论", r"结论|建议"),
        ("证据", r"依据|数据|来源|证据"),
        ("行动", r"行动|下一步|负责人"),
    ],
    "meeting-minutes": [
        ("决策", r"决策|结论|议定"),
        ("行动项", r"负责人|时间|行动|完成"),
        ("待定", r"待补充|待定|待确认"),
    ],
    "risk-plan": [
        ("风险清单", r"风险"),
        ("触发信号", r"信号|触发|条件"),
        ("责任人", r"负责人|责任|路径|降级"),
    ],
    "novel": [
        ("高概念", r"概念|高概念|世界|主题"),
        ("人物", r"人物|角色|欲望|恐惧"),
        ("冲突", r"冲突|阻力|转折"),
        ("结局", r"结局|终点|收束"),
        ("写作手法", r"视角|节奏|对白|比喻|悬念|钩子"),
    ],
    "screenplay": [
        ("场景任务", r"场景|任务|目的"),
        ("动作视觉", r"动作|视觉|镜头|景别|光线"),
        ("对白", r"对白|台词|对话"),
        ("悬念", r"悬念|钩子|期待"),
    ],
    "ai-video": [
        ("主体", r"主体|角色|人物|道具"),
        ("动作时间线", r"动作|秒|时间|起点|终点"),
        ("镜头", r"镜头|景别|运镜|机位"),
        ("光线风格", r"光线|风格|色彩|灯光"),
        ("声音", r"声音|音效|音乐|静音"),
        ("限制", r"保持|限制|不变量|负向"),
    ],
    "nonfiction": [
        ("事实边界", r"事实|来源|信源|待核验"),
        ("采访素材", r"采访|访谈|引语|素材"),
        ("编辑审稿", r"编辑|审稿|修改|终审"),
    ],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="output file to inspect")
    parser.add_argument(
        "--output-type",
        required=True,
        choices=sorted(CHECKS),
        help="deliverable type",
    )
    parser.add_argument("--output", help="optional markdown report path")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR file not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8", errors="ignore")
    rows = []
    for label, patterns in CHECKS[args.output_type]:
        found = any(re.search(pattern, text) for pattern in patterns)
        rows.append((label, found))

    passed = sum(1 for _, ok in rows if ok)
    total = len(rows)
    lines = [
        "# 高生产力输出机械自检",
        "",
        f"- file: {path}",
        f"- output_type: {args.output_type}",
        f"- result: {passed}/{total} checks found",
        "",
        "| 检查项 | 是否命中 |",
        "|---|---|",
    ]
    for label, ok in rows:
        lines.append(f"| {label} | {'PASS' if ok else 'MISSING'} |")
    lines += [
        "",
        "注：这是机械关键词检查，不能替代人工核验事实、专业边界、平台合规和真实反馈。",
        "",
    ]
    report = "\n".join(lines)
    print(report)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"output: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
