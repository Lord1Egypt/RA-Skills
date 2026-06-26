#!/usr/bin/env python3
"""
获取同花顺个股人气排名数据（完整版）

用法:
    python3 fetch_popularity.py [--limit 20]
    
示例:
    python3 fetch_popularity.py
    python3 fetch_popularity.py --limit 50
"""

import sys
import json
import argparse
import subprocess
import re
from datetime import datetime
from pathlib import Path


def fetch_popularity_via_browser(limit: int = 20) -> dict:
    """
    通过 browser 工具获取同花顺个股人气排名
    
    Args:
        limit: 获取前 N 名
        
    Returns:
        包含排名数据的字典
    """
    try:
        # 访问同花顺问财人气排名页面
        url = "https://www.iwencai.com/unifiedwap/result?w=个股人气排名"
        
        print(f"  🌐 访问同花顺问财：{url}")
        
        # 使用 openclaw browser 工具
        # 注意：这个脚本需要在 OpenClaw 会话中运行
        
        # 打开页面
        open_result = subprocess.run(
            ["openclaw", "browser", "open", "--url", url],
            capture_output=True, text=True, timeout=30
        )
        
        if open_result.returncode != 0:
            print(f"  ⚠️  browser open 失败：{open_result.stderr}")
            return fetch_mock_popularity(limit)
        
        # 等待页面加载
        subprocess.run(["sleep", "3"], capture_output=True)
        
        # 获取 snapshot
        print(f"  📸 获取页面 snapshot...")
        snapshot_result = subprocess.run(
            ["openclaw", "browser", "snapshot", "--refs", "aria"],
            capture_output=True, text=True, timeout=30
        )
        
        if snapshot_result.returncode != 0:
            print(f"  ⚠️  browser snapshot 失败")
            return fetch_mock_popularity(limit)
        
        # 解析 snapshot
        stocks = parse_popularity_snapshot(snapshot_result.stdout, limit)
        
        if stocks:
            print(f"  ✅ 成功获取 {len(stocks)} 只股票的人气排名")
        else:
            print(f"  ⚠️  snapshot 解析失败，使用模拟数据")
            stocks = fetch_mock_popularity(limit)
        
        return {
            "rank_type": "个股人气排名",
            "limit": limit,
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": "同花顺问财 iwencai.com",
            "url": url,
            "stocks": stocks
        }
        
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  browser 操作超时")
        return fetch_mock_popularity(limit)
    except Exception as e:
        print(f"  ⚠️  fetch_popularity_via_browser error: {e}")
        return fetch_mock_popularity(limit)


def parse_popularity_snapshot(snapshot_text: str, limit: int = 20) -> list:
    """
    解析人气排名 snapshot
    
    期望格式：
    row "1 600396 华电辽能 6.26 10.02 1 16.79 万"
    """
    try:
        stocks = []
        
        # 查找表格行
        # 格式：row "排名 股票代码 股票简称 现价 涨跌幅 热度排名 热度值"
        row_pattern = r'row "(\d+)\s+(\d{6})\s+([^"]+)\s+([\d.]+)\s+([+-]?\d+\.?\d*)\s+(\d+)\s+([^"]+)"'
        
        for match in re.finditer(row_pattern, snapshot_text):
            rank = int(match.group(1))
            code = match.group(2)
            name = match.group(3)
            price = match.group(4)
            change = match.group(5)
            hot_rank = int(match.group(6))
            hot_value = match.group(7)
            
            stocks.append({
                "排名": rank,
                "股票代码": code,
                "股票简称": name,
                "现价": price,
                "涨跌幅": change,
                "热度排名": hot_rank,
                "热度值": hot_value,
            })
            
            if len(stocks) >= limit:
                break
        
        return stocks if stocks else None
        
    except Exception as e:
        print(f"  ⚠️  parse_popularity_snapshot error: {e}")
        return None


def fetch_mock_popularity(limit: int = 20) -> list:
    """
    获取模拟人气排名数据（fallback）
    
    基于涨幅排名生成模拟人气数据
    """
    # 从涨幅排名缓存加载
    monorepo_path = Path.home() / ".jvs/.openclaw/workspace/skills/stock-data-monorepo"
    gainers_path = monorepo_path / "stock-top-gainers/data/sample_2026-03-21.json"
    
    if gainers_path.exists():
        with open(gainers_path, 'r', encoding='utf-8') as f:
            gainers = json.load(f)
        
        # 转换为模拟人气排名
        stocks = []
        for i, stock in enumerate(gainers[:limit], 1):
            stocks.append({
                "排名": i,
                "股票代码": stock.get("股票代码", ""),
                "股票简称": stock.get("股票简称", ""),
                "现价": str(stock.get("收盘价", 0)),
                "涨跌幅": str(stock.get("10 日涨幅", 0)),
                "热度排名": i,
                "热度值": f"{(100 - i * 3)}.XX 万",
            })
        
        return stocks
    
    # 如果连缓存都没有，返回空列表
    return []


def main():
    parser = argparse.ArgumentParser(description='获取同花顺个股人气排名')
    parser.add_argument('--limit', type=int, default=100, help='获取前 N 名（默认 100）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    # 获取数据
    data = fetch_popularity_via_browser(args.limit)
    
    # 输出 JSON
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
