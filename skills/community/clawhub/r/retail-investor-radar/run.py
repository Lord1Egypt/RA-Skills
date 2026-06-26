#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py
A股体检报告 - 一键运行入口

用法：
    python run.py 600519        # 输入股票代码
    python run.py 贵州茅台       # 输入股票名称
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent


def setup_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(log_file), encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def load_config() -> dict:
    config_path = BASE_DIR / "config.yaml"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def check_env():
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("❌ 错误：未设置 DEEPSEEK_API_KEY 环境变量")
        print("请在 OpenClaw 中设置环境变量，或执行：")
        print("  export DEEPSEEK_API_KEY=你的密钥")
        sys.exit(1)


def main():
    setup_logging()
    check_env()

    # 获取股票输入
    if len(sys.argv) < 2:
        print("用法：python run.py <股票代码或名称>")
        print("示例：python run.py 600519")
        print("      python run.py 贵州茅台")
        sys.exit(1)

    raw_input = " ".join(sys.argv[1:]).strip()
    config = load_config()

    # 导入模块
    from fetch import fetch_all
    from report import generate_report

    # 抓取数据
    logging.info(f"🚀 开始为「{raw_input}」生成体检报告...")
    try:
        news_count = config.get("modules", {}) and config.get("news_count", 5)
        data = fetch_all(raw_input, news_count=news_count)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"数据抓取失败: {e}")
        print(f"❌ 数据抓取失败：{e}")
        sys.exit(1)

    # 生成报告
    try:
        report = generate_report(data, config)
    except Exception as e:
        logging.error(f"报告生成失败: {e}")
        print(f"❌ 报告生成失败：{e}")
        sys.exit(1)

    # 输出到控制台
    if config.get("output", {}).get("console", True):
        print("\n" + report)

    # 保存到文件
    output_cfg = config.get("output", {})
    if output_cfg.get("save_file", True):
        stock_name = data.get("basic", {}).get("name") or data.get("stock", {}).get("name", "stock")
        code = data.get("stock", {}).get("code", "")
        file_dir = BASE_DIR / output_cfg.get("file_dir", "reports")
        file_dir.mkdir(exist_ok=True)

        filename = f"{datetime.now().strftime('%Y%m%d_%H%M')}_{code}_{stock_name}.txt"
        filepath = file_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        logging.info(f"💾 报告已保存：{filepath}")
        print(f"💾 报告已保存：{filepath}")


if __name__ == "__main__":
    main()
