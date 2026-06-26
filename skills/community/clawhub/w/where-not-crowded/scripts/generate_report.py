#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


HOLIDAY_LABELS = {
    "五一": "2026 年五一劳动节（5/1 周五 - 5/5 周二）",
    "国庆": "2026 年国庆节（10/1 周四 - 10/7 周三）",
    "端午": "2026 年端午节（6/19 周五 - 6/21 周日）",
    "中秋": "2026 年中秋节（9/25 周五 - 9/27 周日）",
    "清明": "2026 年清明节（4/4 周六 - 4/6 周一）",
    "春节": "2026 年春节（2/15 周日 - 2/23 周一）",
    "元旦": "2026 年元旦（1/1 周四 - 1/3 周六）"
}

HOLIDAY_ORDER = ["元旦", "春节", "清明", "五一", "端午", "中秋", "国庆"]

ORIGIN_SLUG = {
    "上海": "shanghai",
    "杭州": "hangzhou",
    "北京": "beijing",
    "广州": "guangzhou",
    "深圳": "shenzhen",
    "苏州": "suzhou",
    "南京": "nanjing",
    "一线城市": "tier1-origin"
}

HOLIDAY_SLUG = {
    "五一": "wuyi",
    "国庆": "national-day",
    "端午": "dragon-boat",
    "中秋": "mid-autumn",
    "清明": "qingming",
    "春节": "spring-festival",
    "元旦": "new-year"
}

TAG_KEYWORDS = {
    "海边": ["海边", "看海", "海岛", "沙滩", "海风"],
    "城市": ["城市", "citywalk", "逛街", "都市", "看展", "文艺"],
    "美食": ["美食", "吃", "好吃", "小吃", "逛吃"],
    "短途": ["周边", "短途", "高铁", "周末感", "人少"],
    "轻松": ["轻松", "放松", "舒服", "不折腾", "慢节奏"]
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_holiday(text: str) -> str:
    if "十一" in text:
        return "国庆"
    for holiday in HOLIDAY_ORDER:
        if holiday in text:
            return holiday
    return "五一"


def parse_origin(text: str) -> str:
    known_origins = [city for city in ORIGIN_SLUG.keys() if city != "一线城市"]
    for city in known_origins:
        if city in text:
            return city
    patterns = [
        r"我从([\u4e00-\u9fff]{2,6})",
        r"我在([\u4e00-\u9fff]{2,6})",
        r"从([\u4e00-\u9fff]{2,6})出发",
        r"([\u4e00-\u9fff]{2,6})出发"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return "一线城市"


def parse_budget(text: str):
    for pattern in [r"预算\s*(\d{3,5})", r"(\d{3,5})\s*块"]:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def infer_tags(text: str):
    tags = set()
    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            tags.add(tag)
    return tags


def pick_frame(frames, intent: str, origin: str):
    lowered = intent.lower()
    inferred_tags = infer_tags(intent)
    scored = []

    for frame in frames:
        score = 0
        for alias in frame.get("aliases", []):
            if alias.lower() in lowered:
                score += 15
        if origin in frame.get("preferred_origins", []):
            score += 12
        frame_tags = set(frame.get("tags", []))
        score += len(inferred_tags & frame_tags) * 6
        if frame["default_choice"] in intent or frame["main_choice"] in intent:
            score += 12
        scored.append((score, frame))

    scored.sort(key=lambda item: item[0], reverse=True)
    if scored and scored[0][0] > 0:
        return scored[0][1]

    for frame in frames:
        if origin in frame.get("preferred_origins", []):
            return frame

    if "海边" in inferred_tags:
        return next(frame for frame in frames if frame["id"] == "sanya-okinawa")
    if origin in {"上海", "苏州", "南京"}:
        return next(frame for frame in frames if frame["id"] == "shanghai-east-china-escape")
    if origin == "杭州":
        return next(frame for frame in frames if frame["id"] == "hangzhou-linhai")
    if origin == "北京":
        return next(frame for frame in frames if frame["id"] == "beijing-seoul")
    return frames[0]


def score_label(score: int) -> str:
    if score >= 8:
        return "高"
    if score >= 5:
        return "中"
    return "低"


def build_report(frame, holiday: str, origin: str, budget):
    report = {
        "title": "节假日出行判断报告",
        "holiday_label": f"{HOLIDAY_LABELS[holiday]} | {origin}出发",
        "verdict": frame["verdict"],
        "default_path": {
            "name": frame["default_choice"],
            "summary": frame["default_summary"],
            "why_default": frame["why_default"],
            "why_not_optimal": frame["why_not_optimal"]
        },
        "crowd_reasons": frame["crowd_reasons"],
        "risk_cards": [
            {
                "bucket": "高拥挤风险",
                "place": frame["default_choice"],
                "reason": frame["crowd_reasons"]["structure"],
                "level_class": "level-high"
            },
            {
                "bucket": "中等拥挤风险",
                "place": frame["near_choice"],
                "reason": "同类替代里仍有热度，但体感比默认路径轻。",
                "level_class": "level-mid"
            },
            {
                "bucket": "更优低拥挤选择",
                "place": frame["main_choice"],
                "reason": "结构更分散，节假日体验更稳定。",
                "level_class": "level-low"
            }
        ],
        "risk_matrix": [],
        "recommendations": {
            "main": {**frame["recommendations"]["main"], "role": "主推荐"},
            "near": {**frame["recommendations"]["near"], "role": "近程替代"},
            "far": {**frame["recommendations"]["far"], "role": "远程替代"}
        },
        "cost_comparison": frame["cost_comparison"],
        "travel_window": frame["travel_window"],
        "if_ignore": frame["if_ignore"],
        "final_recommendation": frame["final_recommendation"]
    }

    for item in frame["risk_matrix"]:
        report["risk_matrix"].append({
            "dimension": item["dimension"],
            "default_label": score_label(item["default_score"]),
            "alternative_label": score_label(item["alternative_score"]),
            "label": item["label"]
        })

    if budget:
        report["verdict"] = (
            f"预算约 {budget} 元时，不要先默认热门路径更稳。"
            f"{frame['main_choice']} 这种替代方案更容易把预算花在体验上，而不是花在节假日溢价上。"
        )
    return report


def build_markdown(report: dict) -> str:
    lines = [
        "# 节假日出行判断报告",
        "",
        f"节假日：{report['holiday_label']}",
        "",
        "## 一句话结论",
        "",
        report["verdict"],
        "",
        "## 默认路径判断",
        "",
        f"默认路径：**{report['default_path']['name']}**",
        "",
        report["default_path"]["summary"],
        "",
        "为什么大家会默认这么选："
    ]
    lines.extend([f"- {item}" for item in report["default_path"]["why_default"]])
    lines.extend(["", "为什么它这次未必最优："])
    lines.extend([f"- {item}" for item in report["default_path"]["why_not_optimal"]])
    lines.extend(["", "## 为什么不推荐", "", "### 人流趋势"])
    lines.append(f"- 历年规律：{report['crowd_reasons']['history']}")
    lines.append(f"- 结构影响：{report['crowd_reasons']['structure']}")
    lines.append("- 热点影响：")
    lines.extend([f"  - {item}" for item in report["crowd_reasons"]["hotspots"]])
    lines.extend(["", "## 多维判断", "", "| 维度 | 默认路径 | 更优替代 | 判断 |", "|------|----------|----------|------|"])
    for row in report["risk_matrix"]:
        lines.append(f"| {row['dimension']} | {row['default_label']} | {row['alternative_label']} | {row['label']} |")
    lines.extend(["", "## 推荐去哪", ""])
    for key in ["main", "near", "far"]:
        item = report["recommendations"][key]
        lines.append(f"### {item['role']}：{item['name']}")
        lines.append(f"- 类型：{item['type']}")
        lines.append(f"- 为什么更值：{item['why_better']}")
        lines.append(f"- 更适合谁：{item['fit_for']}")
        lines.append("")
    lines.extend(["## 国内外成本对比", "", "| 方案 | 机票 | 酒店 | 总预算 | 判断 |", "|------|------|------|--------|------|"])
    for row in report["cost_comparison"]:
        lines.append(f"| {row['option']} | {row['flight']} | {row['hotel']} | {row['total']} | {row['verdict']} |")
    window = report["travel_window"]
    lines.extend([
        "",
        "## 最佳出行窗口建议",
        "",
        f"- 建议请假日期：{window['leave_date']}",
        f"- 建议出发日期：{window['depart_date']}",
        f"- 建议返程日期：{window['return_date']}",
        f"- 推荐玩几天：{window['duration']}",
        f"- 机票价格参考：{window['flight_tip']}",
        f"- 酒店价格参考：{window['hotel_tip']}",
        f"- 为什么这是更优窗口：{window['reason']}",
        "",
        "## 如果你不这么走，会发生什么",
        ""
    ])
    lines.extend([f"- {item}" for item in report["if_ignore"]])
    lines.extend(["", "## 最终建议", "", report["final_recommendation"], ""])
    return "\n".join(lines)


def render_html(template_path: Path, output_path: Path, report: dict):
    template = template_path.read_text(encoding="utf-8")
    html = template.replace(
        "/* __REPORT_DATA_PLACEHOLDER__ */",
        f"window.__WIDGET_DATA__ = {json.dumps(report, ensure_ascii=False, indent=2)};"
    )
    output_path.write_text(html, encoding="utf-8")


def slugify(text: str) -> str:
    return re.sub(r"[^\w\u4e00-\u9fff-]+", "_", text).strip("_") or "where-not-crowded-report"


def main():
    parser = argparse.ArgumentParser(description="Generate where-not-crowded report")
    parser.add_argument("--intent", required=True)
    parser.add_argument("--output-dir", default=".")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    data = load_json(skill_dir / "assets" / "destination_frames.json")
    holiday = parse_holiday(args.intent)
    origin = parse_origin(args.intent)
    budget = parse_budget(args.intent)
    frame = pick_frame(data["frames"], args.intent, origin)
    report = build_report(frame, holiday, origin, budget)
    markdown = build_markdown(report)

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cn_stem = slugify(f"{holiday}去哪不挤报告_{origin}")
    en_stem = f"{HOLIDAY_SLUG.get(holiday, 'holiday')}-{ORIGIN_SLUG.get(origin, 'origin')}-where-not-crowded-report"
    paths = {
        "markdown": output_dir / f"{cn_stem}.md",
        "html": output_dir / f"{cn_stem}.html",
        "ascii_markdown": output_dir / f"{en_stem}.md",
        "ascii_html": output_dir / f"{en_stem}.html",
        "latest_markdown": output_dir / "where-not-crowded-report-latest.md",
        "latest_html": output_dir / "where-not-crowded-report-latest.html"
    }

    for key in ["markdown", "ascii_markdown", "latest_markdown"]:
        paths[key].write_text(markdown, encoding="utf-8")
    for key in ["html", "ascii_html", "latest_html"]:
        render_html(skill_dir / "assets" / "report_widget.html", paths[key], report)

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {
        "intent": args.intent,
        "holiday": holiday,
        "origin": origin,
        "markdown": str(paths["markdown"]),
        "html": str(paths["html"]),
        "ascii_markdown": str(paths["ascii_markdown"]),
        "ascii_html": str(paths["ascii_html"]),
        "latest_markdown": str(paths["latest_markdown"]),
        "latest_html": str(paths["latest_html"]),
        "conversation_markdown": markdown
    }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
