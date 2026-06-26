#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
ACTION_LABEL = {
    "open-now": "立即点开",
    "read-later": "稍后看",
    "skip": "可跳过",
}


def load_items(path: Path):
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "items" in data:
        data = data["items"]
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list or an object with an 'items' array")
    return data


def normalize(item):
    return {
        "circle_name": item.get("circle_name", "未分类星球"),
        "title_or_hook": item.get("title_or_hook") or item.get("title") or "（无标题）",
        "why_it_matters": item.get("why_it_matters", "待补充"),
        "suggested_action": item.get("suggested_action", "read-later"),
        "priority": item.get("priority", "medium"),
        "url": item.get("url", ""),
        "content_preview": item.get("content_preview", ""),
    }


def render(items, window_text="今天", circles_text="全部已采集星球"):
    norm = [normalize(x) for x in items]
    norm.sort(key=lambda x: (PRIORITY_ORDER.get(x["priority"], 9), x["circle_name"], x["title_or_hook"]))

    high = [x for x in norm if x["priority"] == "high"]
    grouped = defaultdict(list)
    for item in norm:
        grouped[item["circle_name"]].append(item)

    out = []
    out.append("# 知识星球日报")
    out.append(f"- 时间范围：{window_text}")
    out.append(f"- 覆盖星球：{circles_text}")
    out.append(f"- 更新概览：共 {len(norm)} 条，其中高优先级 {len(high)} 条")
    out.append("")
    out.append("## 今日最值得点开的 3 条")
    for idx, item in enumerate(high[:3], start=1):
        line = f"{idx}. [{item['circle_name']}] {item['title_or_hook']}"
        if item["url"]:
            line += f" ({item['url']})"
        out.append(line)
        out.append(f"   - 值得看原因：{item['why_it_matters']}")
        out.append(f"   - 建议动作：{ACTION_LABEL.get(item['suggested_action'], item['suggested_action'])}")
    if not high:
        out.append("1. 暂无高优先级条目，可按分星球摘要浏览。")
    out.append("")

    out.append("## 分星球更新")
    for circle in sorted(grouped):
        out.append(f"### {circle}")
        for item in grouped[circle]:
            title = item['title_or_hook']
            if item["url"]:
                title += f" ({item['url']})"
            out.append(f"- [{item['priority']}] {title}")
            out.append(f"  - 摘要：{item['content_preview'] or '（无预览）'}")
            out.append(f"  - 建议：{ACTION_LABEL.get(item['suggested_action'], item['suggested_action'])}；{item['why_it_matters']}")
        out.append("")

    out.append("## 建议阅读顺序")
    ranked = [x for x in norm if x["suggested_action"] != "skip"][:5]
    if ranked:
        for idx, item in enumerate(ranked, start=1):
            out.append(f"{idx}. [{item['circle_name']}] {item['title_or_hook']}")
    else:
        out.append("1. 今日暂无强烈建议点开的内容。")
    out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description="Render a markdown digest from normalized ZSXQ update JSON")
    parser.add_argument("input", help="Path to JSON input")
    parser.add_argument("--window", default="今天")
    parser.add_argument("--circles", default="全部已采集星球")
    args = parser.parse_args()

    items = load_items(Path(args.input))
    print(render(items, window_text=args.window, circles_text=args.circles))


if __name__ == "__main__":
    main()
