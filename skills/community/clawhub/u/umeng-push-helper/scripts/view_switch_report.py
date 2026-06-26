#!/usr/bin/env python3
"""
友盟推送助手 - 打开最新的开关统计图表报告
"""

import os
import sys
import subprocess
from pathlib import Path

REPORTS_DIR = Path.home() / ".qoderwork/skills/umeng-push-helper/reports"

def find_latest_report():
    """查找最新的报告文件"""
    if not REPORTS_DIR.exists():
        return None
    
    html_files = list(REPORTS_DIR.glob("switch_report_*.html"))
    if not html_files:
        return None
    
    # 按修改时间排序，返回最新的
    latest = max(html_files, key=lambda f: f.stat().st_mtime)
    return latest

def main():
    latest_report = find_latest_report()
    
    if not latest_report:
        print("❌ 未找到任何开关统计报告")
        print("\n💡 提示：先运行以下命令生成报告：")
        print("   python scripts/query_switch_statistics.py <appkey>")
        sys.exit(1)
    
    print(f"📊 打开最新开关统计报告：{latest_report.name}")
    print(f"📁 文件位置：{latest_report}")
    
    # 根据操作系统打开文件
    if sys.platform == 'darwin':
        subprocess.run(['open', str(latest_report)])
    elif sys.platform == 'linux':
        subprocess.run(['xdg-open', str(latest_report)])
    elif sys.platform == 'win32':
        os.startfile(str(latest_report))
    else:
        print(f"\n请在浏览器中手动打开：file://{latest_report}")

if __name__ == "__main__":
    main()
