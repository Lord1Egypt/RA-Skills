#!/usr/bin/env python3
"""
股票投资智投顾问 - 统一入口脚本
整合实时行情、分时量能、K线图采集、新闻搜索等功能

使用方法：
    uv run analyze.py 600519           # 分析贵州茅台
    uv run analyze.py 600519 --minute  # 包含分时量能分析
    uv run analyze.py 600519 --json    # JSON格式输出

注意：这是一个示例框架，实际使用时需要集成具体的行情采集脚本。
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 获取脚本目录
SCRIPT_DIR = Path(__file__).parent.absolute()
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"
DATA_DIR = WORKSPACE_DIR / "stock_data_output"

# 确保输出目录存在
DATA_DIR.mkdir(parents=True, exist_ok=True)


def normalize_code(code: str) -> str:
    """
    标准化股票代码格式
    
    Args:
        code: 原始代码（如 600519 或 600519.SS）
    
    Returns:
        标准化后的代码（如 600519.SS）
    """
    if "." in code:
        return code
    
    # 根据代码前缀判断市场
    if code.startswith("6"):
        return f"{code}.SS"  # 上交所
    elif code.startswith(("0", "3")):
        return f"{code}.SZ"  # 深交所
    elif code.startswith("8"):
        return f"{code}.BJ"  # 北交所
    else:
        return code


def analyze_stock(code: str, include_minute: bool = False) -> dict:
    """
    分析单只股票
    
    Args:
        code: 股票代码（6位数字或带后缀格式）
        include_minute: 是否包含分时量能分析
    
    Returns:
        dict: 分析结果
    """
    result = {
        "code": normalize_code(code),
        "timestamp": datetime.now().isoformat(),
        "data": {},
        "status": "success",
        "message": ""
    }
    
    try:
        # TODO: 在此处集成实际的行情采集脚本
        # 示例：调用 a-stock-analysis 的脚本
        # a_stock_script = SCRIPT_DIR / "a-stock" / "analyze.py"
        # if a_stock_script.exists():
        #     cmd = ["uv", "run", str(a_stock_script), result["code"]]
        #     if include_minute:
        #         cmd.append("--minute")
        #     output = subprocess.check_output(cmd, text=True)
        #     result["data"] = json.loads(output)
        
        result["message"] = f"股票 {result['code']} 分析完成"
        result["note"] = "这是一个示例框架，实际使用时需要集成具体的行情采集脚本"
        
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)
    
    return result


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="股票投资智投顾问 - 统一入口脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    uv run analyze.py 600519           # 分析贵州茅台
    uv run analyze.py 600519 --minute  # 包含分时量能分析
    uv run analyze.py 600519 --json    # JSON格式输出
    uv run analyze.py 0700.HK          # 分析港股腾讯控股
    uv run analyze.py AAPL             # 分析美股苹果
        """
    )
    parser.add_argument("code", help="股票代码")
    parser.add_argument("--minute", action="store_true", help="包含分时量能分析")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    result = analyze_stock(args.code, args.minute)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"股票代码: {result['code']}")
        print(f"分析时间: {result['timestamp']}")
        print(f"状态: {result['status']}")
        print(f"{'='*60}\n")
        if result.get("data"):
            print(json.dumps(result["data"], ensure_ascii=False, indent=2))
        else:
            print(result["message"])
            if result.get("note"):
                print(f"\n⚠️  {result['note']}")


if __name__ == "__main__":
    main()
