#!/usr/bin/env python3
"""
命令行工具调用器

让 Agent 可以通过 bash 命令调用 55 个工具
用法: python3 run_tool.py tool_name param1=value1 param2=value2
"""

import sys
import json
import asyncio
import argparse
from pathlib import Path

# 添加 tools 目录到路径
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

from __init__ import load_all_tools, get_registry


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="OpenClaw Tool Executor")
    parser.add_argument("tool", help="工具名称")
    parser.add_argument("params", nargs="*", help="参数列表 (key=value 格式)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    return parser.parse_args()


def parse_params(params_list):
    """解析参数列表为字典"""
    params = {}
    for p in params_list:
        if "=" in p:
            key, value = p.split("=", 1)
            # 尝试解析为 Python 对象
            try:
                # 尝试 JSON 解析
                params[key] = json.loads(value)
            except json.JSONDecodeError:
                # 如果是纯数字
                if value.isdigit():
                    params[key] = int(value)
                elif value.replace(".", "", 1).isdigit():
                    params[key] = float(value)
                elif value.lower() == "true":
                    params[key] = True
                elif value.lower() == "false":
                    params[key] = False
                else:
                    # 去除引号
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        params[key] = value[1:-1]
                    else:
                        params[key] = value
    return params


async def execute_tool(tool_name: str, params: dict):
    """执行工具并返回结果"""
    # 加载工具（只加载一次）
    total = load_all_tools()
    
    # 只在第一次加载时打印摘要
    if total > 0:
        print(f"已加载 {total} 个工具", file=sys.stderr)
    
    registry = get_registry()
    
    # 执行工具
    result = await registry.execute(tool_name, **params)
    
    return result


def main():
    args = parse_args()
    
    # 解析参数
    params = parse_params(args.params)
    
    # 只在调试模式显示加载信息
    import os
    debug = os.environ.get("DEBUG", "")
    
    # 执行工具
    try:
        # 临时抑制加载日志
        if not debug:
            # 重定向 stderr
            import io
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
        
        result = asyncio.run(execute_tool(args.tool, params))
        
        if not debug:
            sys.stderr = old_stderr
        
        # 输出结果
        if args.json:
            output = {
                "success": result.success,
                "data": result.data,
                "error": result.error
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            if result.success:
                if isinstance(result.data, dict):
                    # 格式化输出
                    for key, value in result.data.items():
                        print(f"{key}: {value}")
                else:
                    print(result.data)
            else:
                print(f"错误: {result.error}", file=sys.stderr)
                sys.exit(1)
                
    except Exception as e:
        if not debug:
            sys.stderr = old_stderr
        print(f"执行失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()