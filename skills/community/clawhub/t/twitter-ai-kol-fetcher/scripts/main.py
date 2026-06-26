#!/usr/bin/env python3
"""
Twitter KOL Fetcher - Main Runner
主流程脚本：抓取 → 过滤 → 生成报告
"""

import os
import sys
import json
from datetime import datetime

# 动态添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置
from scripts import 01_fetch_kols, 02_filter_and_score, 03_generate_report

def main():
    """主流程"""
    print("=" * 60)
    print("Twitter AI KOL 内参生成器")
    print("=" * 60)

    today = datetime.now().strftime('%Y%m%d')

    # Step 1: 抓取数据
    print("\n[Step 1] 抓取 KOL 推文...")
    tweets_file = f"/tmp/kol_tweets_{today}.json"

    # 检查是否已有缓存
    if os.path.exists(tweets_file):
        print(f"使用缓存: {tweets_file}")
    else:
        tweets_file = 01_fetch_kols.main()

    # Step 2: 过滤和评分
    print("\n[Step 2] 过滤和评分...")
    filtered_file = tweets_file.replace(".json", "_filtered.json")

    if os.path.exists(filtered_file):
        print(f"使用缓存: {filtered_file}")
    else:
        filtered_file = 02_filter_and_score.filter_and_score(tweets_file)

    # Step 3: 生成报告
    print("\n[Step 3] 生成内参...")

    # 配置 API Key
    03_generate_report.OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

    reports = 03_generate_report.generate_reports(filtered_file)

    # 输出报告
    print("\n" + "=" * 60)
    print("生成的报告")
    print("=" * 60)

    for i, report in enumerate(reports):
        print(f"\n--- 报告 {i+1} ---")
        print(report["content"])

    return reports

if __name__ == "__main__":
    # 设置 API Key（可以从环境变量读取）
    # os.environ["OPENROUTER_API_KEY"] = "your-api-key"

    reports = main()
