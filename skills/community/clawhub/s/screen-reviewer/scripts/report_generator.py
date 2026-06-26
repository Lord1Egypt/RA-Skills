#!/usr/bin/env python3
"""
复盘报告生成器
读取某一天的 JSONL 日志 → 聚合统计 → 调用 AI 生成 Markdown 报告
"""

import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, DATA_DIR

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
PROMPT_PATH = os.path.join(SKILL_DIR, "templates", "review_prompt.md")

# ── 日志读取与聚合 ────────────────────────────────────────


def load_day_logs(date_str: str) -> list:
    """读取指定日期的所有日志条目"""
    log_path = os.path.join(DATA_DIR, "logs", f"{date_str}.jsonl")
    if not os.path.exists(log_path):
        return []
    entries = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def aggregate_logs(entries: list, categories: dict) -> dict:
    """
    将原始日志聚合为 AI 可消费的摘要结构:
    - 按应用统计时间
    - 按时间段分组
    - 按价值类别统计
    """
    if not entries:
        return {}

    config = load_config()
    interval = config["capture"]["interval_seconds"]

    # 按应用统计
    app_stats = defaultdict(lambda: {"minutes": 0, "windows": set(), "texts": []})
    for e in entries:
        app = e.get("app", "Unknown")
        minutes = interval / 60.0
        app_stats[app]["minutes"] += minutes
        if e.get("window_title"):
            app_stats[app]["windows"].add(e["window_title"])
        if e.get("ocr_text"):
            app_stats[app]["texts"].append(e["ocr_text"][:100])

    app_summary = {}
    for app, data in app_stats.items():
        # 只保留前 5 条 OCR 文本作为代表性内容
        sample_texts = data["texts"][:5]
        app_summary[app] = {
            "minutes": round(data["minutes"], 1),
            "top_windows": list(data["windows"])[:10],
            "sample_content": sample_texts,
        }

    # 按时间段分组（上午/下午/晚上）
    timeline = {"morning": [], "afternoon": [], "evening": []}
    for e in entries:
        try:
            hour = datetime.fromisoformat(e["timestamp"]).hour
        except (ValueError, KeyError):
            continue
        period = "morning" if hour < 12 else ("afternoon" if hour < 18 else "evening")
        timeline[period].append({
            "time": e.get("timestamp", ""),
            "app": e.get("app", ""),
            "title": e.get("window_title", ""),
        })

    # 压缩 timeline：连续相同应用合并为一段
    compressed_timeline = {}
    for period, items in timeline.items():
        if not items:
            compressed_timeline[period] = []
            continue
        segments = []
        cur = {"app": items[0]["app"], "start": items[0]["time"], "end": items[0]["time"], "titles": set()}
        cur["titles"].add(items[0].get("title", ""))
        for item in items[1:]:
            if item["app"] == cur["app"]:
                cur["end"] = item["time"]
                cur["titles"].add(item.get("title", ""))
            else:
                cur["titles"] = list(cur["titles"])[:3]
                segments.append(cur)
                cur = {"app": item["app"], "start": item["time"], "end": item["time"], "titles": set()}
                cur["titles"].add(item.get("title", ""))
        cur["titles"] = list(cur["titles"])[:3]
        segments.append(cur)
        compressed_timeline[period] = segments

    # 按价值类别统计
    cat_minutes = {"high_value": 0, "medium_value": 0, "low_value": 0, "uncategorized": 0}
    high = [a.lower() for a in categories.get("high_value", [])]
    med = [a.lower() for a in categories.get("medium_value", [])]
    low = [a.lower() for a in categories.get("low_value", [])]

    for app, data in app_stats.items():
        app_lower = app.lower()
        if any(h in app_lower for h in high):
            cat_minutes["high_value"] += data["minutes"]
        elif any(m in app_lower for m in med):
            cat_minutes["medium_value"] += data["minutes"]
        elif any(l in app_lower for l in low):
            cat_minutes["low_value"] += data["minutes"]
        else:
            cat_minutes["uncategorized"] += data["minutes"]

    total_minutes = sum(data["minutes"] for data in app_stats.values())
    switch_count = sum(
        1 for i in range(1, len(entries))
        if entries[i].get("app") != entries[i - 1].get("app")
    )

    return {
        "date": entries[0].get("timestamp", "")[:10] if entries else "",
        "total_active_minutes": round(total_minutes, 1),
        "total_entries": len(entries),
        "app_switch_count": switch_count,
        "app_summary": app_summary,
        "timeline": compressed_timeline,
        "category_minutes": {k: round(v, 1) for k, v in cat_minutes.items()},
    }


# ── AI 调用 ───────────────────────────────────────────────


def _load_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _call_openai(prompt: str, data_json: str, model: str, api_key: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"以下是今日活动数据，请生成复盘报告：\n\n```json\n{data_json}\n```"},
        ],
        temperature=0.7,
        max_tokens=4000,
    )
    return resp.choices[0].message.content


def _call_claude(prompt: str, data_json: str, model: str, api_key: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=4000,
        system=prompt,
        messages=[
            {"role": "user", "content": f"以下是今日活动数据，请生成复盘报告：\n\n```json\n{data_json}\n```"},
        ],
    )
    return resp.content[0].text


def _call_ollama(prompt: str, data_json: str, model: str, url: str) -> str:
    import urllib.request
    payload = json.dumps({
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"以下是今日活动数据，请生成复盘报告：\n\n```json\n{data_json}\n```"},
        ],
    }).encode()
    req = urllib.request.Request(
        f"{url}/api/chat", data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    return result["message"]["content"]


def generate_report(date_str: str = None) -> str:
    """
    为指定日期生成复盘报告，返回 Markdown 文本。
    date_str 默认为昨天。
    """
    if date_str is None:
        date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    config = load_config()
    entries = load_day_logs(date_str)
    if not entries:
        return f"# {date_str} 没有活动记录\n\n当天没有截图日志，无法生成报告。"

    summary = aggregate_logs(entries, config["categories"])
    prompt = _load_prompt()
    data_json = json.dumps(summary, ensure_ascii=False, indent=2)

    provider = config["report"]["ai_provider"]
    model = config["report"]["ai_model"]

    if provider == "openai":
        api_key = os.environ.get(config["report"]["api_key_env"], "")
        if not api_key:
            return _fallback_report(summary, date_str)
        report = _call_openai(prompt, data_json, model, api_key)

    elif provider == "claude":
        api_key = os.environ.get(config["report"]["api_key_env"], "")
        if not api_key:
            return _fallback_report(summary, date_str)
        report = _call_claude(prompt, data_json, model, api_key)

    elif provider == "ollama":
        url = config["report"]["ollama_url"]
        report = _call_ollama(prompt, data_json, model, url)

    else:
        return _fallback_report(summary, date_str)

    # 保存报告
    report_dir = os.path.join(DATA_DIR, "reports")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{date_str}-review.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[screen-reviewer] 报告已生成: {report_path}")
    return report


def _fallback_report(summary: dict, date_str: str) -> str:
    """无 AI 时的纯统计报告"""
    total = summary.get("total_active_minutes", 0)
    cats = summary.get("category_minutes", {})
    apps = summary.get("app_summary", {})

    lines = [
        f"# 每日复盘报告 — {date_str}（纯统计版）",
        "",
        "## 一、今日概览",
        f"- 总活跃时间: {total:.0f} 分钟 ({total/60:.1f} 小时)",
        f"- 有效记录数: {summary.get('total_entries', 0)}",
        f"- 应用切换次数: {summary.get('app_switch_count', 0)}",
        "",
        "## 二、时间分配",
        "",
        "| 应用 | 时长(分钟) | 占比 |",
        "|------|-----------|------|",
    ]
    sorted_apps = sorted(apps.items(), key=lambda x: x[1]["minutes"], reverse=True)
    for app, data in sorted_apps[:15]:
        pct = (data["minutes"] / total * 100) if total > 0 else 0
        lines.append(f"| {app} | {data['minutes']:.0f} | {pct:.1f}% |")

    lines += [
        "",
        "## 三、价值分类",
        f"- 高价值: {cats.get('high_value', 0):.0f} 分钟",
        f"- 中价值: {cats.get('medium_value', 0):.0f} 分钟",
        f"- 低价值: {cats.get('low_value', 0):.0f} 分钟",
        f"- 未分类: {cats.get('uncategorized', 0):.0f} 分钟",
        "",
        "> 提示: 配置 AI API Key 后可生成含 ROI 分析和行动建议的完整报告。",
    ]

    report_text = "\n".join(lines)
    report_dir = os.path.join(DATA_DIR, "reports")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"{date_str}-review.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"[screen-reviewer] 纯统计报告已生成: {report_path}")
    return report_text


# ── CLI ───────────────────────────────────────────────────

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    print(generate_report(target))
