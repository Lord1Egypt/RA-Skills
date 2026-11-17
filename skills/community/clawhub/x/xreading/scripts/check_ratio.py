#!/usr/bin/env python3
"""Check whether XReading cards roughly follow the 60/30/10 ratio."""

import re
import sys
from pathlib import Path


CONTENT = {
    "这本书在回答什么问题",
    "核心主张",
    "核心观点",
    "论证逻辑",
    "心法",
}
USE = {
    "可操作规则",
    "机会来了怎么用（可选的动手入口）",
    "一句话总结",
}
DOUBT = {
    "⚠️ 别用这些",
    "别用这些",
    "我不同意的地方",
    "作者的盲区",
}


def strip_frontmatter(text):
    if not text.startswith("---"):
        return text
    match = re.match(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", text, flags=re.S)
    return text[match.end():] if match else text


def classify(title):
    if title in CONTENT:
        return "content"
    if title in USE:
        return "use"
    if title in DOUBT:
        return "doubt"
    if any(keyword in title for keyword in ("对账", "讲透", "偷走", "为什么这本书", "读原著清单")):
        return "content"
    return "other"


def measure(path):
    text = strip_frontmatter(path.read_text(encoding="utf-8"))
    buckets = {"content": 0, "use": 0, "doubt": 0, "other": 0}
    others = []
    for section in re.split(r"^## ", text, flags=re.M)[1:]:
        title = section.split("\n", 1)[0].strip()
        size = len(re.sub(r"\s", "", section))
        kind = classify(title)
        buckets[kind] += size
        if kind == "other":
            others.append(title)
    total = sum(buckets.values()) or 1
    return {key: value / total * 100 for key, value in buckets.items()}, total, others


def resolve_cards(args):
    if not args:
        return sorted(Path.cwd().glob("*/卡片.md"))
    cards = []
    for raw in args:
        path = Path(raw)
        if path.is_dir():
            path = path / "卡片.md"
        cards.append(path)
    return cards


def main():
    cards = resolve_cards(sys.argv[1:])
    missing = [str(path) for path in cards if not path.is_file()]
    if missing or not cards:
        print("Card not found: " + ", ".join(missing or ["*/卡片.md"]), file=sys.stderr)
        return 1

    failed = False
    for card in cards:
        pct, total, others = measure(card)
        ok = pct["content"] >= 50 and pct["use"] >= 20 and pct["doubt"] <= 20
        failed = failed or not ok
        print(
            f"{card}: content={pct['content']:.0f}% use={pct['use']:.0f}% "
            f"doubt={pct['doubt']:.0f}% other={pct['other']:.0f}% "
            f"chars={total} {'OK' if ok else 'FAIL'}"
        )
        if others:
            print("  Unclassified sections: " + ", ".join(others))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
