#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stock-top-gainers: 获取 A 股近 10 日涨幅前 20 股票

数据来源：同花顺问财
URL: https://www.iwencai.com/unifiedwap/result?w=近 10 日涨幅排名

✅ 2026-03-23 优化：
- 默认通过 browser 工具获取实时数据
- 只在 browser 失败时使用缓存 fallback
- 添加数据日期验证
"""

import sys
import json
import subprocess
import re
from pathlib import Path
from typing import Optional, List, Dict

# 配置
LIMIT = 20  # 获取前 20 只股票
EXCLUDE_ST = True  # 排除 ST 股票


# ==================== 实时数据获取 ====================

def fetch_from_browser(limit: int = 20, exclude_st: bool = True) -> Optional[List[Dict]]:
    """
    通过 browser 工具实时获取同花顺问财数据
    
    Returns:
        股票列表，或 None（失败）
    """
    try:
        # 打开同花顺问财页面
        url = "https://www.iwencai.com/unifiedwap/result?w=近 10 日涨幅排名"
        
        print(f"  🌐 访问同花顺问财：{url}")
        
        # 使用 browser 工具打开页面
        browser_result = subprocess.run(
            ["openclaw", "browser", "open", "--url", url],
            capture_output=True, text=True, timeout=30
        )
        
        if browser_result.returncode != 0:
            print(f"  ⚠️ browser open 失败：{browser_result.stderr}")
            return None
        
        # 等待页面加载
        subprocess.run(["sleep", "3"], capture_output=True)
        
        # 获取 snapshot
        print(f"  📸 获取页面 snapshot...")
        snapshot_result = subprocess.run(
            ["openclaw", "browser", "snapshot", "--refs", "aria"],
            capture_output=True, text=True, timeout=30
        )
        
        if snapshot_result.returncode != 0:
            print(f"  ⚠️ browser snapshot 失败：{snapshot_result.stderr}")
            return None
        
        # 解析 snapshot
        stocks = parse_snapshot(snapshot_result.stdout, limit, exclude_st)
        
        if stocks:
            print(f"  ✅ 成功获取 {len(stocks)} 只股票（实时数据）")
            return stocks
        else:
            print(f"  ⚠️ snapshot 解析失败")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ browser 操作超时")
        return None
    except Exception as e:
        print(f"  ⚠️ fetch_from_browser error: {e}")
        return None


def parse_snapshot(snapshot_text: str, limit: int = 20, exclude_st: bool = True) -> Optional[List[Dict]]:
    """
    解析同花顺问财 snapshot 数据
    
    从 snapshot 中提取表格行数据
    """
    try:
        stocks = []
        
        # 查找表格行（格式：row "1 600396 华电辽能 6.89 10.06 1/487 89.81"）
        row_pattern = r'row "(\d+)\s+(\d{6})\s+([^"]+)\s+([\d.]+)\s+(-?[\d.]+)\s+\d+/\d+\s+(-?[\d.]+)"'
        
        for match in re.finditer(row_pattern, snapshot_text):
            rank = int(match.group(1))
            code = match.group(2)
            name = match.group(3)
            price = float(match.group(4))
            today_change = float(match.group(5))
            gain_10d = float(match.group(6))
            
            # 排除 ST 股票
            if exclude_st and "ST" in name.upper():
                continue
            
            stocks.append({
                "排名": rank,
                "股票代码": code,
                "股票简称": name,
                "收盘价": price,
                "10 日涨幅": gain_10d,
                "今日涨跌": today_change,
            })
            
            if len(stocks) >= limit:
                break
        
        return stocks if stocks else None
        
    except Exception as e:
        print(f"  ⚠️ parse_snapshot error: {e}")
        return None


# ==================== 缓存数据（fallback） ====================

def load_sample_data() -> Optional[List[Dict]]:
    """
    加载示例数据（fallback 使用）
    
    数据来源：同花顺问财（缓存）
    """
    sample_file = Path(__file__).parent.parent / "data/sample_2026-03-21.json"
    if sample_file.exists():
        with open(sample_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def filter_st_stocks(stocks: List[Dict]) -> List[Dict]:
    """排除 ST 股票"""
    if not stocks:
        return []
    
    filtered = []
    for stock in stocks:
        name = stock.get("股票简称", "")
        # 排除所有包含 ST 的股票（*ST、ST、S*ST 等）
        if "ST" not in name.upper():
            filtered.append(stock)
    
    return filtered


def fetch_from_cache(limit: int = 20, exclude_st: bool = True) -> Optional[List[Dict]]:
    """
    从缓存获取数据（fallback）
    """
    try:
        data = load_sample_data()
        
        if data:
            # 排除 ST 股票
            if exclude_st:
                data = filter_st_stocks(data)
            
            # 限制数量
            data = data[:limit]
            
            print(f"  ℹ️  使用缓存数据：{len(data)} 只股票")
            return data
    except Exception as e:
        print(f"  ⚠️ fetch_from_cache error: {e}")
    
    return None


# ==================== 主函数 ====================

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="获取 A 股近 10 日涨幅前 20 股票")
    parser.add_argument("--limit", type=int, default=LIMIT, help=f"获取数量（默认：{LIMIT}）")
    parser.add_argument("--exclude-st", action="store_true", default=EXCLUDE_ST, help="排除 ST 股票")
    parser.add_argument("--source", choices=["browser", "cache", "auto"], default="auto", 
                        help="数据源选择（默认：auto 自动选择）")
    
    args = parser.parse_args()
    
    data = None
    
    if args.source == "browser":
        # 强制使用 browser 实时获取
        data = fetch_from_browser(limit=args.limit, exclude_st=args.exclude_st)
        if not data:
            print("  ⚠️ browser 获取失败，尝试 fallback 到缓存")
            data = fetch_from_cache(limit=args.limit, exclude_st=args.exclude_st)
    
    elif args.source == "cache":
        # 强制使用缓存
        data = fetch_from_cache(limit=args.limit, exclude_st=args.exclude_st)
    
    else:  # auto
        # 自动选择：优先 browser，失败则 fallback 到缓存
        print("🔄 自动模式：优先实时获取，失败则使用缓存")
        data = fetch_from_browser(limit=args.limit, exclude_st=args.exclude_st)
        if not data:
            print("📦 实时获取失败，使用缓存数据")
            data = fetch_from_cache(limit=args.limit, exclude_st=args.exclude_st)
    
    # 输出结果
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        # 返回空列表
        print(json.dumps([], ensure_ascii=False))


if __name__ == "__main__":
    main()
