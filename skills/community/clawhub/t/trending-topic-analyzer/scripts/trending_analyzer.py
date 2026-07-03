#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点深度分析器
输入话题 → 输出全网热度趋势+关键观点+情感分析+竞品对比+行动建议
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import random

# ============ 平台配置 ============

PLATFORMS = {
    "weibo": {
        "name": "微博",
        "data_type": "阅读量",
        "unit": "亿",
        "peak_times": ["09:00", "12:00", "21:00"],
    },
    "douyin": {
        "name": "抖音",
        "data_type": "播放量",
        "unit": "亿",
        "peak_times": ["12:00", "18:00", "21:00"],
    },
    "xhs": {
        "name": "小红书",
        "data_type": "笔记数",
        "unit": "万篇",
        "peak_times": ["08:00", "12:00", "20:00"],
    },
    "bilibili": {
        "name": "B站",
        "data_type": "视频数",
        "unit": "条",
        "peak_times": ["18:00", "22:00"],
    },
}

# ============ 模拟数据生成（实际应调用API） ============

def fetch_topic_data(topic, platforms):
    """
    获取话题数据（这里用模拟数据，实际需调用各平台API）
    """
    data = {}
    for p in platforms:
        cfg = PLATFORMS[p]
        # 模拟数据
        base_value = random.uniform(1.0, 20.0)
        data[p] = {
            "platform": cfg["name"],
            "metric": cfg["data_type"],
            "value": round(base_value, 1),
            "unit": cfg["unit"],
            "growth_rate": f"+{random.randint(20, 80)}%",
            "peak_time": random.choice(cfg["peak_times"]),
        }
    return data


def extract_key_viewpoints(topic):
    """
    提取关键观点（模拟）
    """
    viewpoints = [
        ("工具推荐", random.randint(25, 40)),
        ("使用教程", random.randint(20, 35)),
        ("效果对比", random.randint(15, 30)),
        ("变现案例", random.randint(10, 20)),
    ]
    return sorted(viewpoints, key=lambda x: x[1], reverse=True)


def analyze_sentiment(topic):
    """
    情感分析（模拟）
    """
    positive = random.randint(50, 70)
    neutral = random.randint(15, 30)
    negative = 100 - positive - neutral
    
    return {
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "positive_reasons": ["效率提升", "创意辅助", "降低门槛"],
        "negative_reasons": ["版权担忧", "质量质疑", "伦理争议"],
    }


def compare_competitors(topic, competitors):
    """
    竞品声量对比（模拟）
    """
    comparison = {topic: {}}
    for p in PLATFORMS:
        comparison[topic][p] = random.randint(100, 1000)
    
    for comp in competitors:
        comparison[comp] = {}
        for p in PLATFORMS:
            comparison[comp][p] = random.randint(50, 500)
    
    return comparison


def predict_spread_path(topic):
    """
    传播路径预测（模拟）
    """
    return [
        {
            "wave": "第一波",
            "target": "技术圈（知乎/B站）",
            "channel": "知识付费圈",
            "estimated_time": "1-2天",
        },
        {
            "wave": "第二波",
            "target": "大众群体",
            "channel": "社交媒体热搜",
            "estimated_time": "3-5天",
        },
        {
            "wave": "第三波",
            "target": "垂直领域",
            "channel": "自媒体变现",
            "estimated_time": "5-7天",
        },
    ]


def generate_action_recommendations(topic, data, viewpoints, sentiment):
    """
    生成行动建议
    """
    # 找出最热的观点方向
    top_viewpoint = viewpoints[0][0]
    
    # 找出最佳平台
    best_platform = max(data.items(), key=lambda x: x[1]["value"])[0]
    
    recommendations = [
        f"✅ 选题方向：{topic} - {top_viewpoint}（热度高+内容稀缺）",
        f"✅ 发布平台：{PLATFORMS[best_platform]['name']}（声量最大）",
        f"✅ 发布时间：{data[best_platform]['peak_time']}（流量高峰）",
        f"✅ 内容形式：教程类视频（互动率最高）",
    ]
    
    if sentiment["negative"] > 20:
        recommendations.append(f"⚠️ 风险提示：负面占比{sentiment['negative']}%，需平衡正负面观点")
    
    return recommendations


# ============ 报告生成 ============

def generate_report(topic, platforms, competitors=None, output_path=None):
    """
    生成完整分析报告
    """
    print(f"\n🔍 正在分析【{topic}】的热度数据...")
    
    # 获取数据
    data = fetch_topic_data(topic, platforms)
    viewpoints = extract_key_viewpoints(topic)
    sentiment = analyze_sentiment(topic)
    spread_path = predict_spread_path(topic)
    
    if competitors:
        competitor_data = compare_competitors(topic, competitors.split(","))
    else:
        competitor_data = None
    
    recommendations = generate_action_recommendations(topic, data, viewpoints, sentiment)
    
    # 生成Markdown报告
    report = f"""# 热点深度分析报告 - {topic}

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 热度概览

| 平台 | 指标 | 数值 | 增长率 |
|------|------|------|--------|
"""

    for p, d in data.items():
        report += f"| {d['platform']} | {d['metric']} | {d['value']}{d['unit']} | {d['growth_rate']} |\n"

    report += f"""

## 热度趋势

- 峰值时间：{data[list(data.keys())[0]]['peak_time']}
- 7天增长率：{data[list(data.keys())[0]]['growth_rate']}
- 预测：未来3天持续上升

## 关键观点提取

| 观点方向 | 占比 |
|----------|------|
"""

    for vp, pct in viewpoints:
        report += f"| {vp} | {pct}% |\n"

    report += f"""

## 情感分析

- 正面：{sentiment['positive']}%（{', '.join(sentiment['positive_reasons'][:2])}）
- 中性：{sentiment['neutral']}%
- 负面：{sentiment['negative']}%（{', '.join(sentiment['negative_reasons'][:2])}）

## 传播路径预测

"""

    for wave in spread_path:
        report += f"**{wave['wave']}**：{wave['target']} → {wave['channel']}（预计{wave['estimated_time']}）\n\n"

    if competitor_data:
        report += f"""## 竞品声量对比

| 关键词 | {' | '.join([PLATFORMS[p]['name'] for p in platforms])} |
|--------|{'|'.join(['------' for _ in platforms])}|
"""
        for keyword, values in competitor_data.items():
            row = f"| {keyword} |"
            for p in platforms:
                row += f" {values[p]} |"
            report += row + "\n"

    report += f"""
## 行动建议

"""
    for rec in recommendations:
        report += f"{rec}\n\n"

    report += f"""
---

*数据来源：{', '.join([PLATFORMS[p]['name'] for p in platforms])}*
*注：实际数据需调用各平台API，当前为模拟数据*
"""

    # 保存报告
    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")
        print(f"\n✅ 报告已保存: {output_path}\n")
    else:
        print(report)
    
    return report


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(description="热点深度分析器")
    parser.add_argument("--topic", "-t", type=str, required=True, help="分析话题")
    parser.add_argument("--platforms", "-p", type=str, default="weibo,douyin,xhs,bilibili",
                        help="分析平台（逗号分隔）")
    parser.add_argument("--competitors", "-c", type=str, help="竞品关键词（逗号分隔）")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    args = parser.parse_args()
    
    platforms = [p.strip() for p in args.platforms.split(",")]
    generate_report(args.topic, platforms, args.competitors, args.output)


if __name__ == "__main__":
    main()
