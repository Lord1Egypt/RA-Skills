#!/usr/bin/env python3
"""
特朗普日报趋势分析脚本
分析历史报告中的市场数据变化，生成趋势摘要

用法:
    # 默认使用环境变量 TRUMP_DAILY_MEMORY_PATH
    python analyze_trends.py

    # 或通过命令行指定路径
    python analyze_trends.py /path/to/memory/trump-daily
"""

import re
import os
import sys
from datetime import datetime
from pathlib import Path


def get_memory_dir() -> Path:
    """从环境变量或命令行参数获取记忆目录路径"""
    # 优先使用环境变量
    memory_path = os.environ.get("TRUMP_DAILY_MEMORY_PATH")
    if memory_path:
        return Path(memory_path)

    # 其次使用命令行参数
    if len(sys.argv) > 1:
        return Path(sys.argv[1])

    # 默认使用相对路径（相对于脚本所在目录）
    # 脚本位于 skills/trump-daily-report/scripts/
    # 默认向上两级目录的 memory/trump-daily
    script_dir = Path(__file__).parent.resolve()
    default_memory = (script_dir.parent.parent / "memory" / "trump-daily").resolve()
    return default_memory


def parse_report_date(filename: str) -> str:
    """从文件名提取日期"""
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return match.group(1) if match else None


def extract_metrics_from_report(content: str) -> dict:
    """从报告内容提取关键指标"""
    metrics = {}

    # 标普500
    sp500 = re.search(r"标普500.*?([+-]?\d+\.?\d*)%", content)
    if sp500:
        metrics["sp500"] = float(sp500.group(1))

    # 纳斯达克
    nasdaq = re.search(r"纳斯达克.*?([+-]?\d+\.?\d*)%", content)
    if nasdaq:
        metrics["nasdaq"] = float(nasdaq.group(1))

    # 布伦特原油
    oil = re.search(r"布伦特原油.*?\$?([\d.]+)", content)
    if oil:
        metrics["oil"] = float(oil.group(1))

    # 黄金
    gold = re.search(r"黄金.*?\$?([\d,]+)", content)
    if gold:
        metrics["gold"] = float(gold.group(1).replace(",", ""))

    # 美元指数
    dollar = re.search(r"美元指数.*?([+-]?\d+\.?\d*)%", content)
    if dollar:
        metrics["dollar"] = float(dollar.group(1))

    return metrics


def get_market_sentiment(content: str) -> str:
    """识别市场情绪"""
    if "避险" in content and "冒险" in content:
        if "→" in content:
            return "🔄 情绪切换"
        return "混合"
    elif "避险" in content:
        return "🔴 避险"
    elif "冒险" in content or "风险偏好" in content:
        return "🟢 冒险"
    return "⚪ 中性"


def get_core_topic(content: str) -> str:
    """提取核心议题"""
    topics = []
    if "伊朗" in content or "停火" in content:
        topics.append("伊朗/停火")
    if "关税" in content:
        topics.append("关税")
    if "中国" in content:
        topics.append("中国")
    if "美联储" in content or "Fed" in content:
        topics.append("美联储")
    return topics[0] if topics else "其他"


def generate_trend_summary(reports_dir: Path, n_recent: int = 5) -> str:
    """生成趋势摘要"""
    reports = []

    if not reports_dir.exists():
        return f"报告目录不存在: {reports_dir}\n请设置 TRUMP_DAILY_MEMORY_PATH 环境变量"

    for f in sorted(reports_dir.glob("2026-*.md"), reverse=True)[:n_recent]:
        date = parse_report_date(f.name)
        if date:
            content = f.read_text(encoding="utf-8")
            reports.append({
                "date": date,
                "content": content,
                "metrics": extract_metrics_from_report(content),
                "sentiment": get_market_sentiment(content),
                "topic": get_core_topic(content)
            })

    if not reports:
        return f"目录 {reports_dir} 中暂无历史报告数据"

    # 生成摘要
    summary = ["## 趋势分析摘要\n"]
    summary.append(f"分析期：{reports[-1]['date']} ~ {reports[0]['date']}")
    summary.append(f"报告数量：{len(reports)} 份\n")

    # 议题变化
    topics = [r["topic"] for r in reports]
    if len(set(topics)) > 1:
        summary.append("### 议题演变")
        for r in reports:
            summary.append(f"- {r['date']}: {r['topic']}")
        summary.append("")

    # 情绪变化
    sentiments = [r["sentiment"] for r in reports]
    if len(set(sentiments)) > 1:
        summary.append("### 情绪变化")
        for r in reports:
            summary.append(f"- {r['date']}: {r['sentiment']}")
        summary.append("")

    # 价格变化
    if len(reports) >= 2:
        latest = reports[0]["metrics"]
        oldest = reports[-1]["metrics"]

        summary.append("### 价格趋势（最新 vs 最早）")
        for key in ["sp500", "nasdaq", "oil", "gold", "dollar"]:
            if key in latest and key in oldest:
                change = latest[key] - oldest[key]
                arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
                summary.append(f"- {key.upper()}: {oldest[key]} → {latest[key]} ({arrow}{abs(change):.1f})")
        summary.append("")

    return "\n".join(summary)


if __name__ == "__main__":
    memory_dir = get_memory_dir()
    result = generate_trend_summary(memory_dir)
    print(result)
