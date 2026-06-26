#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取个股题材脚本 - 调用 ths-stock-themes skill 获取股票的题材/概念列表
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List
import os
import subprocess
import time


def get_stock_themes_from_skill(stock_code: str) -> Dict:
    """
    调用 ths-stock-themes skill 获取股票题材
    
    Args:
        stock_code: 股票代码（6 位数字）
    
    Returns:
        题材信息字典
    """
    try:
        # 使用 sessions_spawn 调用 ths-stock-themes skill
        # 这里通过 subprocess 调用 OpenClaw CLI（简化方案）
        # 实际应用中应该通过 API 或 skill 调用机制
        
        cmd = [
            "openclaw",
            "sessions",
            "spawn",
            "--task",
            f"查询股票代码 {stock_code} 的题材和概念信息，使用 ths-stock-themes skill",
            "--runtime",
            "subagent",
            "--mode",
            "run"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # 解析返回结果（需要从输出中提取 JSON）
            # 这里简化处理，实际需要根据返回格式解析
            return parse_themes_result(result.stdout, stock_code)
        else:
            print(f"调用 ths-stock-themes skill 失败：{result.stderr}")
            return None
    
    except subprocess.TimeoutExpired:
        print(f"查询 {stock_code} 超时")
        return None
    except Exception as e:
        print(f"查询 {stock_code} 失败：{e}")
        return None


def parse_themes_result(output: str, stock_code: str) -> Dict:
    """
    解析 skill 返回结果
    
    实际格式取决于 ths-stock-themes skill 的返回
    这里假设返回 JSON 格式
    """
    try:
        # 尝试从输出中提取 JSON
        import re
        json_match = re.search(r'\{[^{}]*"股票代码"[^{}]*\}', output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    
    # 如果解析失败，返回空结构
    return {
        "股票代码": stock_code,
        "股票简称": "",
        "涉及概念": [],
        "所属地域": "",
        "主营业务": "",
        "人气排名": None
    }


def get_themes_batch(stock_codes: List[str], output_path: str, 
                     cache_path: str = None) -> Dict[str, List[str]]:
    """
    批量获取股票题材
    
    Args:
        stock_codes: 股票代码列表
        output_path: 输出 JSON 文件路径
        cache_path: 缓存文件路径（可选）
    
    Returns:
        {股票代码：[题材列表]}
    """
    # 加载缓存（如果有）
    stock_themes = {}
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            stock_themes = json.load(f)
        print(f"加载缓存：{len(stock_themes)} 只股票")
    
    # 获取未查询的股票
    remaining = [code for code in stock_codes if code not in stock_themes]
    
    if remaining:
        print(f"需要查询 {len(remaining)} 只股票...")
        
        for i, code in enumerate(remaining, 1):
            print(f"[{i}/{len(remaining)}] 查询：{code}")
            
            result = get_stock_themes_from_skill(code)
            
            if result:
                # 提取题材列表
                themes = result.get("涉及概念", [])
                stock_themes[code] = themes
                
                # 保存到缓存
                if cache_path:
                    os.makedirs(os.path.dirname(cache_path) or '.', exist_ok=True)
                    with open(cache_path, 'w', encoding='utf-8') as f:
                        json.dump(stock_themes, f, ensure_ascii=False, indent=2)
            
            # 避免请求过快
            time.sleep(1)
    
    # 保存结果
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stock_themes, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到：{output_path}")
    return stock_themes


def main():
    parser = argparse.ArgumentParser(description='获取个股题材脚本')
    parser.add_argument('--stocks', help='股票代码列表（逗号分隔）')
    parser.add_argument('--stocks-file', help='股票代码文件（每行一个）')
    parser.add_argument('--output', required=True, help='输出 JSON 文件路径')
    parser.add_argument('--cache', help='缓存文件路径')
    parser.add_argument('--top', type=int, default=30, help='近 10 日涨幅前 N 只股票')
    
    args = parser.parse_args()
    
    # 获取股票代码列表
    stock_codes = []
    
    if args.stocks:
        stock_codes = [s.strip() for s in args.stocks.split(',')]
    elif args.stocks_file:
        with open(args.stocks_file, 'r', encoding='utf-8') as f:
            stock_codes = [line.strip() for line in f if line.strip()]
    else:
        print("错误：需要指定 --stocks 或 --stocks-file")
        parser.print_help()
        return
    
    print(f"将获取 {len(stock_codes)} 只股票的题材信息...")
    
    # 批量获取
    get_themes_batch(stock_codes, args.output, args.cache)


if __name__ == '__main__':
    main()
