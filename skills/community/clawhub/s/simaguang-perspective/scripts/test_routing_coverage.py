#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run a keyword routing hit test against test-prompts.

报告输出位置三级：`--out` 参数 → 外部项目根/学习记录/（若解析到）→ 技能包内 handoff/。
命中率只依赖包内 `references/技能路由配置.md` 与 `test-prompts.json`，
没有外部项目也能跑完整回归。
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

import project_paths

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "references" / "技能路由配置.md"
TEST = ROOT / "test-prompts.json"
META_IDS = (
    "first-meeting-",
    "identity-",
    "greeting-",
    "traceability-",
    "module-implicit-",
    "sima-foundation-",
)


def load_config():
    config = {}
    current = None
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line.strip())
        if m:
            current = m.group(2).strip()
            config[current] = {"trigger": [], "exclude": []}
        elif current:
            if line.startswith("- trigger:"):
                config[current]["trigger"] = [
                    item.strip()
                    for item in line.split(":", 1)[1].split("、")
                    if item.strip()
                ]
            elif line.startswith("- exclude:"):
                config[current]["exclude"] = [
                    item.strip()
                    for item in line.split(":", 1)[1].split("；")
                    if item.strip()
                ]
    return config


def hits(prompt, keywords):
    return [keyword for keyword in keywords if keyword and keyword in prompt]


def resolve_out(explicit: str | None) -> Path:
    """--out > 项目根/学习记录/ > 包内 handoff/。"""
    if explicit:
        return Path(explicit).expanduser()
    root = project_paths.find_project_dir()
    if root:
        return root / "学习记录" / "技能路由命中测试.md"
    return ROOT / "handoff" / "技能路由命中测试.md"


def main():
    parser = argparse.ArgumentParser(description="跑关键词路由命中回归，输出统计报告。")
    parser.add_argument("--out", help="报告输出路径（默认：项目根/学习记录/ 或 包内 handoff/）")
    parser.add_argument("--quiet", action="store_true", help="只打印一行统计，不写报告文件")
    args = parser.parse_args()

    config = load_config()
    data = json.loads(TEST.read_text(encoding="utf-8"))
    cases = data["test_cases"]

    rows = []
    for case in cases:
        prompt = case["prompt"]
        candidates = []
        for name, meta in config.items():
            trigger_hits = hits(prompt, meta["trigger"])
            exclude_hits = hits(prompt, meta["exclude"])
            if trigger_hits:
                candidates.append(
                    {
                        "cluster": name,
                        "trigger": trigger_hits,
                        "exclude": exclude_hits,
                    }
                )
        rows.append({"case": case, "candidates": candidates})

    no_route = [row for row in rows if not row["candidates"]]
    content_no_route = [
        row for row in no_route if not any(row["case"]["id"].startswith(prefix) for prefix in META_IDS)
    ]
    single = [row for row in rows if len(row["candidates"]) == 1]
    multi = [row for row in rows if len(row["candidates"]) > 1]
    conflicts = [
        row
        for row in rows
        if any(candidate["exclude"] for candidate in row["candidates"])
    ]

    expected_rows = [
        row for row in rows if row["case"].get("expected_clusters")
    ]
    required_hit = []
    exact = []
    partial = []
    missed = []
    expected_no_hit = []
    precisions = []
    recalls = []
    for row in expected_rows:
        candidates = {candidate["cluster"] for candidate in row["candidates"]}
        expected = set(row["case"]["expected_clusters"])
        if not candidates:
            expected_no_hit.append(row)
            continue
        overlap = candidates & expected
        precisions.append(len(overlap) / len(candidates))
        recalls.append(len(overlap) / len(expected))
        if expected <= candidates:
            required_hit.append(row)
            if candidates == expected:
                exact.append(row)
        elif overlap:
            partial.append(row)
        else:
            missed.append(row)

    cluster_counts = {}
    for row in rows:
        for candidate in row["candidates"]:
            cluster_counts[candidate["cluster"]] = (
                cluster_counts.get(candidate["cluster"], 0) + 1
            )
    top_clusters = sorted(cluster_counts.items(), key=lambda item: item[1], reverse=True)

    lines = [
        f"# 技能路由命中测试（{datetime.date.today().isoformat()}）",
        "",
        "## 统计",
        "",
        f"- 测试提示词：{len(cases)}",
        f"- 无路由命中：{len(no_route)}",
        f"- 无路由且非元协议：{len(content_no_route)}",
        f"- 单簇命中：{len(single)}",
        f"- 多簇命中：{len(multi)}",
        f"- 触发与排除冲突：{len(conflicts)}",
        "",
        "## 准确率结果",
        "",
        f"- 带预期簇：{len(expected_rows)}",
        f"- 预期簇全部命中：{len(required_hit)}",
        f"- 完全命中：{len(exact)}",
        f"- 部分命中：{len(partial)}",
        f"- 零命中：{len(missed)}",
        f"- 预期簇但无路由：{len(expected_no_hit)}",
        f"- 平均精确率：{sum(precisions) / len(precisions) * 100:.1f}%" if precisions else "- 平均精确率：无",
        f"- 平均召回率：{sum(recalls) / len(recalls) * 100:.1f}%" if recalls else "- 平均召回率：无",
        "",
        "## 簇命中排行",
        "",
        "| 簇 | 命中提示词数 |",
        "| --- | --- |",
    ]
    for name, count in top_clusters:
        lines.append(f"| {name} | {count} |")

    lines += ["", "## 无路由命中", ""]
    for row in no_route[:30]:
        lines.append(f"- {row['case']['id']}：{row['case']['prompt']}")
    if not no_route:
        lines.append("- 无")

    lines += ["", "## 多簇命中示例（超过 6 簇）", ""]
    many = [row for row in multi if len(row["candidates"]) > 6]
    for row in many[:30]:
        clusters = "、".join(c["cluster"] for c in row["candidates"])
        lines.append(f"- {row['case']['id']}：{clusters}；{row['case']['prompt']}")
    if not many:
        lines.append("- 无")

    lines += ["", "## 触发与排除冲突", ""]
    for row in conflicts[:30]:
        detail = "、".join(
            f"{c['cluster']}(排除命中:{','.join(c['exclude'])})"
            for c in row["candidates"]
            if c["exclude"]
        )
        lines.append(f"- {row['case']['id']}：{detail}；{row['case']['prompt']}")
    if not conflicts:
        lines.append("- 无")

    lines += ["", "## 预期簇但零命中", ""]
    for row in missed[:30]:
        expected = "、".join(row["case"]["expected_clusters"])
        actual = "、".join(c["cluster"] for c in row["candidates"]) or "无"
        lines.append(f"- {row['case']['id']}：预期 {expected}；实际 {actual}；{row['case']['prompt']}")
    if not missed:
        lines.append("- 无")

    lines += ["", "## 预期簇但无路由", ""]
    for row in expected_no_hit[:30]:
        expected = "、".join(row["case"]["expected_clusters"])
        lines.append(f"- {row['case']['id']}：预期 {expected}；实际无路由；{row['case']['prompt']}")
    if not expected_no_hit:
        lines.append("- 无")

    if not args.quiet:
        out = resolve_out(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    status = "OK" if not (content_no_route or missed or expected_no_hit) else "FAIL"
    print(
        f"prompts={len(cases)} no_route={len(no_route)} required_hit={len(required_hit)} exact={len(exact)} partial={len(partial)} missed={len(missed)} expected_no_hit={len(expected_no_hit)}"
    )
    if recalls:
        print(f"avg_precision={sum(precisions) / len(precisions) * 100:.1f}% avg_recall={sum(recalls) / len(recalls) * 100:.1f}%")
    if not args.quiet:
        print(f"report={out}")
    print(f"routing_accuracy_status={status}")
    return 0 if status == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
