#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票数据下载主入口程序
支持从OpenClaw接收自然语言指令，提供纯后台下载和网页监控两种模式

使用示例：
1. 命令行参数模式：
   python main.py --period=1d --days=500 --batch_size=50 --mode=web

2. 自然语言指令模式：
   python main.py "下载日线数据，最近500天，每批50个，使用网页模式"

3. 从stdin读取：
   echo "后台下载30分钟线数据，最近100天，每批20个" | python main.py

参数说明：
- period: 数据周期 (1d=日线, 30m=30分钟线, 5m=5分钟线, 1m=1分钟线)
- days: 回溯天数 (1-9999)
- batch_size: 每批处理数量 (1-1000)
- mode: 下载模式 (web=网页监控模式, background=纯后台模式)
"""

import sys
import re
import subprocess
import threading
import os
from typing import Dict, Optional, Tuple

def parse_natural_language(instruction: str) -> Dict[str, str]:
    """
    解析自然语言指令，提取下载参数
    
    支持的指令格式：
    - "下载日线数据，最近500天，每批50个，使用网页模式"
    - "后台下载30分钟线数据，最近100天，每批20个"
    - "下载5分钟线，200天，每批30，网页"
    - "下载数据 日线 500天 50个 后台"
    
    返回参数字典，包含：period, days, batch_size, mode
    """
    params = {
        'period': '1d',
        'days': '500',
        'batch_size': '50',
        'mode': 'web'  # 默认网页模式
    }
    
    # 转换为小写方便处理
    text = instruction.lower()
    
    # 1. 解析下载模式
    if '后台' in text or 'background' in text or '纯后台' in text:
        params['mode'] = 'background'
    elif '网页' in text or 'web' in text or '监控' in text:
        params['mode'] = 'web'
    
    # 2. 解析数据周期
    period_patterns = {
        r'日线|1d|日k|daily': '1d',
        r'30分钟线|30m|30分钟|30分钟k': '30m',
        r'5分钟线|5m|5分钟|5分钟k': '5m',
        r'1分钟线|1m|1分钟|1分钟k': '1m',
    }
    
    for pattern, period in period_patterns.items():
        if re.search(pattern, text):
            params['period'] = period
            break
    
    # 3. 解析天数
    days_match = re.search(r'(\d+)\s*天', text)
    if days_match:
        params['days'] = days_match.group(1)
    else:
        # 尝试其他格式
        days_match = re.search(r'最近\s*(\d+)\s*天', text)
        if days_match:
            params['days'] = days_match.group(1)
        else:
            days_match = re.search(r'days?\s*[:：=]?\s*(\d+)', text)
            if days_match:
                params['days'] = days_match.group(1)
    
    # 4. 解析批次大小
    batch_patterns = [
        r'每批\s*(\d+)\s*个',
        r'批次\s*(\d+)\s*个',
        r'batch\s*[:：=]?\s*(\d+)',
        r'batch_size\s*[:：=]?\s*(\d+)',
        r'每批\s*(\d+)\s*',
    ]
    
    for pattern in batch_patterns:
        batch_match = re.search(pattern, text)
        if batch_match:
            params['batch_size'] = batch_match.group(1)
            break
    
    # 5. 如果没有匹配到批次大小，尝试最后出现的数字（但不在天数中）
    if params['batch_size'] == '50':  # 如果是默认值
        # 查找所有数字
        all_numbers = re.findall(r'\b(\d+)\b', text)
        if len(all_numbers) >= 2:
            # 假设最后一个数字是批次大小（如果天数已经匹配）
            params['batch_size'] = all_numbers[-1]
        elif len(all_numbers) == 1:
            # 只有一个数字，可能是天数或批次大小
            # 检查是否已经匹配到天数
            if 'days_match' not in locals() or not days_match:
                # 这个数字可能是天数
                params['days'] = all_numbers[0]
    
    return params

def validate_params(params: Dict[str, str]) -> Tuple[bool, str]:
    """
    验证参数有效性
    
    返回: (是否有效, 错误信息)
    """
    try:
        days = int(params['days'])
        if days < 1 or days > 9999:
            return False, f"天数必须在1-9999之间: {days}"
    except ValueError:
        return False, f"天数必须是整数: {params['days']}"
    
    try:
        batch_size = int(params['batch_size'])
        if batch_size < 1 or batch_size > 1000:
            return False, f"批次大小必须在1-1000之间: {batch_size}"
    except ValueError:
        return False, f"批次大小必须是整数: {params['batch_size']}"
    
    valid_periods = ['1d', '30m', '5m', '1m']
    if params['period'] not in valid_periods:
        return False, f"周期参数无效: {params['period']}，必须是 {valid_periods}"
    
    valid_modes = ['web', 'background']
    if params['mode'] not in valid_modes:
        return False, f"模式参数无效: {params['mode']}，必须是 {valid_modes}"
    
    return True, ""

def run_background_download(period: str, days: int, batch_size: int):
    """
    运行纯后台下载模式
    """
    print(f"[启动] 启动纯后台下载模式")
    print(f"[参数] 参数: 周期={period}, 天数={days}, 批次大小={batch_size}")
    print("=" * 50)
    
    try:
        # 导入agent模块并直接调用下载函数
        import agent
        agent.download_all_data(period=period, days=days, batch_size=batch_size)
        print("[成功] 后台下载任务完成")
    except Exception as e:
        print(f"[错误] 后台下载失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def run_web_mode(period: str, days: int, batch_size: int):
    """
    运行网页监控模式
    """
    # 自动选择可用端口（从5018开始尝试）
    import socket
    
    def is_port_available(port):
        """检查端口是否可用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.bind(('127.0.0.1', port))
                return True
        except (socket.error, OSError):
            return False
    
    # 寻找可用端口
    start_port = 5018
    max_attempts = 20
    selected_port = None
    
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            selected_port = port
            break
    
    if selected_port is None:
        print(f"[错误] 无法找到可用端口（尝试端口 {start_port}-{start_port+max_attempts-1}）")
        sys.exit(1)
    
    print(f"[网页] 启动网页监控模式")
    print(f"[参数] 参数: 周期={period}, 天数={days}, 批次大小={batch_size}")
    print(f"[提示] 提示: 请访问 http://127.0.0.1:{selected_port} 进行控制")
    print("=" * 50)
    
    try:
        # 启动monitor.py作为子进程，传递下载参数和端口
        cmd = [
            sys.executable,  # 当前Python解释器
            "monitor.py",
            "--mode=frontend",
            f"--period={period}",
            f"--days={days}",
            f"--batch_size={batch_size}",
            f"--port={selected_port}",
            f"--host=127.0.0.1"
        ]
        
        print(f"启动命令: {' '.join(cmd)}")
        print("正在启动Web服务器...")
        print(f"[重要] 服务器将运行在端口 {selected_port}，请访问 http://127.0.0.1:{selected_port}")
        
        # 运行monitor.py
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"[错误] 网页监控模式启动失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[停止] 用户中断，停止Web服务器")
        sys.exit(0)

def print_usage():
    """打印使用说明"""
    print(__doc__)
    print("\n示例指令:")
    print("  1. '下载日线数据，最近500天，每批50个，使用网页模式'")
    print("  2. '后台下载30分钟线数据，最近100天，每批20个'")
    print("  3. '下载5分钟线，200天，每批30，网页'")
    print("  4. '下载数据 日线 500天 50个 后台'")
    print("\n命令行参数:")
    print("  --period=1d      数据周期 (1d, 30m, 5m, 1m)")
    print("  --days=500       回溯天数")
    print("  --batch_size=50  每批处理数量")
    print("  --mode=web       下载模式 (web, background)")
    print("  --help           显示帮助信息")

def parse_command_line_args():
    """
    解析命令行参数
    
    支持两种格式：
    1. 标准命令行参数: --period=1d --days=500 --mode=web
    2. 自然语言指令: "下载日线数据，最近500天"
    
    返回: (params, is_natural_language)
    """
    if len(sys.argv) <= 1:
        return None, False
    
    # 检查是否是帮助请求
    if sys.argv[1] in ['--help', '-h', '/?']:
        print_usage()
        sys.exit(0)
    
    # 检查是否是自然语言指令（第一个参数不以--开头）
    if not sys.argv[1].startswith('--'):
        # 可能是自然语言指令
        if len(sys.argv) == 2:
            # 单个字符串参数，很可能是自然语言指令
            return parse_natural_language(sys.argv[1]), True
        else:
            # 多个参数但不是以--开头，合并为自然语言指令
            instruction = ' '.join(sys.argv[1:])
            return parse_natural_language(instruction), True
    
    # 标准命令行参数解析
    params = {
        'period': '1d',
        'days': '500',
        'batch_size': '50',
        'mode': 'web'
    }
    
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            # 移除--前缀
            arg = arg[2:]
            if '=' in arg:
                key, value = arg.split('=', 1)
                if key in params:
                    params[key] = value
            else:
                # 布尔标志，如--web或--background
                if arg in ['web', 'background']:
                    params['mode'] = arg
    
    return params, False

def read_from_stdin():
    """从stdin读取指令"""
    if not sys.stdin.isatty():
        # 有管道输入
        instruction = sys.stdin.read().strip()
        if instruction:
            return instruction
    return None

def main():
    """主函数"""
    print("股票数据下载系统")
    print("=" * 50)
    
    # 1. 尝试从stdin读取指令
    stdin_instruction = read_from_stdin()
    if stdin_instruction:
        print(f"[收到] 收到标准输入指令: {stdin_instruction}")
        params = parse_natural_language(stdin_instruction)
        is_natural_language = True
    else:
        # 2. 解析命令行参数
        result = parse_command_line_args()
        if result[0] is None:
            # 没有参数，使用默认参数并提示
            print("[提示] 没有指定参数，使用默认设置:")
            params = {
                'period': '1d',
                'days': '500',
                'batch_size': '50',
                'mode': 'web'
            }
            is_natural_language = False
            print(f"  周期: {params['period']}, 天数: {params['days']}, 批次: {params['batch_size']}, 模式: {params['mode']}")
            print("  使用 --help 查看完整帮助")
        else:
            params, is_natural_language = result
    
    # 3. 验证参数
    is_valid, error_msg = validate_params(params)
    if not is_valid:
        print(f"[错误] 参数错误: {error_msg}")
        print_usage()
        sys.exit(1)
    
    # 4. 显示解析结果
    print(f"[成功] 参数解析完成:")
    print(f"  下载周期: {params['period']}")
    print(f"  回溯天数: {params['days']}")
    print(f"  批次大小: {params['batch_size']}")
    print(f"  下载模式: {'网页监控' if params['mode'] == 'web' else '纯后台'}")
    if is_natural_language:
        print(f"  解析方式: 自然语言指令")
    print("=" * 50)
    
    # 5. 执行相应模式
    days_int = int(params['days'])
    batch_size_int = int(params['batch_size'])
    
    if params['mode'] == 'background':
        run_background_download(params['period'], days_int, batch_size_int)
    else:  # web mode
        run_web_mode(params['period'], days_int, batch_size_int)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[停止] 用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"[错误] 程序运行异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)