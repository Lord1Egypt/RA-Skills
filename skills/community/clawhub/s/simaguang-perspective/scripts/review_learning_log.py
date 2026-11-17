#!/usr/bin/env python3
"""Review 学习记录/学习日志.md and produce a learning-cycle report."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import datetime
import re
from collections import Counter
from pathlib import Path

TOPIC_PATTERNS = {
    "劳动法/职场权益": ["劳动法", "劳动争议", "竞业", "劳动合同", "N+3", "裁员", "工资", "社保", "劳动权益"],
    "AI/技术治理": ["AI", "算法", "监管", "平台治理", "技术治理", "CFIUS"],
    "实时数据/事实核验": ["实时", "数据", "核验", "预测", "统计", "概率"],
    "法律/证据/程序": ["法律", "证据", "程序", "非法证据", "证明标准", "司法"],
    "家庭照护/资源": ["照护", "家庭", "护工", "康复", "养老", "医疗", "健康"],
    "心理/关系/陪伴": ["心理", "关系", "陪伴", "情绪", "亲密"],
    "历史/档案/制度信息": ["历史", "档案", "史料", "制度", "明代", "失踪", "信息控制"],
    "投资/金融/市场": ["投资", "金融", "市场", "股票", "财务", "现金流"],
    "侦查/推理/技术证据": ["侦查", "推理", "数字取证", "物证", "法医", "证据链"],
}

ROOT = Path(__file__).resolve().parents[1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument(
        "--routing",
        default=str(ROOT / "references" / "技能路由反馈日志.md"),
    )
    return parser.parse_args()


def parse_entries(text):
    entries = []
    current = None
    for line in text.splitlines():
        m = re.match(r"^## (\d{4}-\d{2}-\d{2}) (.+)$", line)
        if m:
            if current:
                entries.append(current)
            current = {"date": m.group(1), "title": m.group(2).strip(), "body": []}
        elif current is not None:
            current["body"].append(line)
    if current:
        entries.append(current)

    for entry in entries:
        fields = {}
        for line in entry["body"]:
            fm = re.match(r"^- (.+?)[:：](.*)$", line)
            if fm:
                fields[fm.group(1).strip()] = fm.group(2).strip()
        entry["fields"] = fields
    return entries


def count_topics(entries):
    counter = Counter()
    for entry in entries:
        fields = entry["fields"]
        text = " ".join(
            [
                fields.get("不确定部分", ""),
                fields.get("知识缺口", ""),
                fields.get("建议补充", ""),
            ]
        )
        for topic, keys in TOPIC_PATTERNS.items():
            if any(key in text for key in keys):
                counter[topic] += 1
    return counter


def parse_feedback(text):
    entries = []
    current = None
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("## "):
            if current:
                entries.append(current)
            current = {"date": line[3:].strip(), "fields": {}}
        elif current is not None:
            m = re.match(r"^- (.+?)[:：](.*)$", line)
            if m:
                current["fields"][m.group(1).strip()] = m.group(2).strip()
    if current:
        entries.append(current)
    return entries


def main():
    args = parse_args()
    text = Path(args.log).read_text(encoding="utf-8", errors="ignore")
    entries = parse_entries(text)
    confidence = Counter()
    uncertain = []
    corrections = []
    sources = Counter()

    routing_path = Path(args.routing)
    feedback_entries = []
    if routing_path.exists():
        feedback_entries = parse_feedback(
            routing_path.read_text(encoding="utf-8", errors="ignore")
        )

    for entry in entries:
        fields = entry["fields"]
        level = fields.get("置信度", "")
        if "高" in level:
            confidence["高"] += 1
        elif "中" in level:
            confidence["中"] += 1
        else:
            confidence["低/未标"] += 1

        if fields.get("不确定部分", "无") not in ("无", "-"):
            uncertain.append((entry["date"], entry["title"], fields.get("不确定部分", "")))
        correction = fields.get("用户追问/纠正", "无")
        if correction not in ("无", "-"):
            corrections.append((entry["date"], entry["title"], correction))
        source_text = fields.get("使用的来源", "")
        for part in re.split(r"[、,，;；/]", source_text):
            part = part.strip().strip("《》")
            if len(part) >= 2:
                sources[part] += 1

    topics = count_topics(entries)
    today = datetime.date.today().isoformat()
    lines = [
        f"# 学习循环复盘 - {today}",
        "",
        "## 概况",
        "",
        f"- 分析记录数：{len(entries)}",
        f"- 高置信：{confidence.get('高', 0)}",
        f"- 中置信：{confidence.get('中', 0)}",
        f"- 低/未标：{confidence.get('低/未标', 0)}",
        f"- 有不确定记录：{len(uncertain)}",
        f"- 有用户追问/纠正：{len(corrections)}",
        "",
        "## 高频缺口/建议领域",
        "",
        "| 领域 | 出现次数 |",
        "|---|---|",
    ]
    for topic, count in topics.most_common():
        lines.append(f"| {topic} | {count} |")
    if not topics:
        lines.append("| 暂无 | 0 |")

    lines += ["", "## 待追踪条目", ""]
    for date, title, detail in uncertain:
        lines.append(f"- {date} {title}：{detail}")
    lines += ["", "## 用户追问/纠正", ""]
    for date, title, detail in corrections:
        lines.append(f"- {date} {title}：{detail}")

    lines += ["", "## 调用来源频次", ""]
    lines.append("| 来源 | 次数 |")
    lines.append("|---|---|")
    for source, count in sources.most_common(15):
        lines.append(f"| {source} | {count} |")
    if not sources:
        lines.append("| 暂无 | 0 |")

    low = [source for source, count in sources.items() if count == 1]
    lines += ["", "## 低频来源（仅出现 1 次）", ""]
    if low:
        lines.append("、".join(low[:30]))
    else:
        lines.append("暂无")

    lines += ["", "## 技能路由反馈", ""]
    lines.append(f"- 反馈记录数：{len(feedback_entries)}")
    if feedback_entries:
        lines.append(f"- 最近记录：{feedback_entries[-1]['date']}")
        suggestions = Counter()
        useful_packs = Counter()
        for entry in feedback_entries:
            suggestion = entry["fields"].get("建议调整", "")
            useful = entry["fields"].get("更有效的技能包", "")
            if suggestion:
                suggestions[suggestion] += 1
            if useful:
                useful_packs[useful] += 1
        if useful_packs:
            lines.append("- 高频有效技能包：" + "、".join(f"{k}({v})" for k, v in useful_packs.most_common(8)))
        if suggestions:
            lines.append("- 高频调整建议：" + "、".join(f"{k}({v})" for k, v in suggestions.most_common(8)))
        lines += ["", "### 最近反馈明细", ""]
        for entry in feedback_entries[-10:]:
            lines.append(
                f"- {entry['date']}：原问题 `{entry['fields'].get('原问题', '')}`；原簇 `{entry['fields'].get('我选的簇', '')}`；有效技能包 `{entry['fields'].get('更有效的技能包', '')}`"
            )
    else:
        lines.append("- 暂无")

    report = "\n".join(lines) + "\n"
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
