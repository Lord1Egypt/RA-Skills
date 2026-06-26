#!/usr/bin/env python3
"""
网页截图工具 - 使用 agent-browser 截图网页
"""

import argparse
import subprocess
import sys
import time
import os


def run_command(cmd, timeout=120):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"


def screenshot_webpage(url, output, wait=3, full_page=False, timeout=60000):
    """
    截图网页
    
    Args:
        url: 网页 URL
        output: 输出图片路径
        wait: 等待页面加载时间（秒）
        full_page: 是否截图整页
        timeout: 超时时间（毫秒）
    """
    print(f"Opening webpage: {url}")
    
    # 打开网页
    cmd = f'agent-browser open "{url}" --timeout {timeout}'
    success, stdout, stderr = run_command(cmd, timeout=timeout//1000 + 10)
    
    if not success:
        print(f"Error opening webpage: {stderr}")
        return False
    
    print(f"Waiting {wait} seconds for page to load...")
    time.sleep(wait)
    
    # 截图
    print(f"Taking screenshot...")
    full_arg = "--full" if full_page else ""
    cmd = f'agent-browser screenshot "{output}" {full_arg}'
    success, stdout, stderr = run_command(cmd, timeout=60)
    
    if not success:
        print(f"Error taking screenshot: {stderr}")
        return False
    
    print(f"Screenshot saved: {output}")
    
    # 关闭浏览器
    run_command("agent-browser close", timeout=10)
    
    return True


def main():
    parser = argparse.ArgumentParser(description='网页截图工具')
    parser.add_argument('--url', required=True, help='网页 URL')
    parser.add_argument('--output', required=True, help='输出图片路径')
    parser.add_argument('--wait', type=int, default=3, help='等待页面加载时间（秒）')
    parser.add_argument('--full-page', action='store_true', help='截图整页')
    parser.add_argument('--timeout', type=int, default=60000, help='超时时间（毫秒）')
    
    args = parser.parse_args()
    
    success = screenshot_webpage(
        url=args.url,
        output=args.output,
        wait=args.wait,
        full_page=args.full_page,
        timeout=args.timeout
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
