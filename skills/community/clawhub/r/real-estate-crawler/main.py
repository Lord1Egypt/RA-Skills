#!/usr/bin/env python3
"""
房产中介网站综合爬虫主程序
整合了安居客和贝壳找房的爬虫功能
"""

import os
import sys
import json
import argparse
import time
import random
from datetime import datetime

def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(description='房产中介网站综合爬虫')
    parser.add_argument('-w', '--website', choices=['anjuke', 'ke', 'lianjia', 'soufun'], default='ke', help='目标网站')
    parser.add_argument('-c', '--city', default='北京', help='城市')
    parser.add_argument('-d', '--district', help='区域')
    parser.add_argument('-p', '--pages', type=int, default=1, help='爬取页数')
    parser.add_argument('-o', '--output', default='output/data.json', help='输出文件')
    parser.add_argument('-f', '--format', choices=['json', 'csv', 'html'], default='json', help='输出格式')
    parser.add_argument('-m', '--mode', choices=['python', 'agent-browser', 'batch'], default='agent-browser', help='爬取模式')
    parser.add_argument('--batch', help='批量处理配置文件')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    print(f"=== 房产中介网站综合爬虫 ===")
    print(f"网站: {args.website}")
    print(f"城市: {args.city}")
    print(f"模式: {args.mode}")
    print(f"页数: {args.pages}")
    print(f"输出格式: {args.format}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 选择爬取方式
    if args.mode == 'python':
        # Python爬取模式
        print("\n=== Python爬取模式 ===")
        python_crawl(args)
    elif args.mode == 'agent-browser':
        # agent-browser模式
        print("\n=== agent-browser模式 ===")
        agent_browser_crawl(args)
    elif args.mode == 'batch':
        # 批量模式
        print("\n=== 批量模式 ===")
        batch_crawl(args)
    
    print("\n=== 爬取完成 ===")
    print(f"数据保存在: {args.output}")

def python_crawl(args):
    """Python爬取模式"""
    
    if args.website == 'anjuke':
        print("执行安居客Python爬虫...")
        cmd = f"python3 scripts/anjuke_crawler.py -c {args.city} -p {args.pages} -o {args.output}"
        execute_command(cmd)
        
    elif args.website == 'ke':
        print("执行贝壳找房Python爬虫...")
        cmd = f"python3 scripts/ke_crawler.py -c {args.city} -p {args.pages} -o {args.output}"
        execute_command(cmd)
        
    else:
        print(f"警告: {args.website} 网站的Python爬虫脚本尚未实现")
        print("建议使用 agent-browser 模式")

def agent_browser_crawl(args):
    """agent-browser爬取模式"""
    
    if args.website == 'anjuke':
        print("执行安居客agent-browser爬虫...")
        cmd = f"bash scripts/bypass_anjuke.sh"
        execute_command(cmd)
        
    elif args.website == 'ke':
        print("执行贝壳找房agent-browser爬虫...")
        cmd = f"bash scripts/bypass_ke.sh"
        execute_command(cmd)
        
    elif args.website == 'lianjia':
        print("执行链家agent-browser爬虫...")
        cmd = f"bash scripts/bypass_lianjia.sh"
        execute_command(cmd)
        
    else:
        print(f"警告: {args.website} 网站的agent-browser爬虫脚本尚未实现")

def batch_crawl(args):
    """批量爬取模式"""
    
    if args.batch:
        print(f"加载批量配置文件: {args.batch}")
        cmd = f"python3 scripts/batch_crawler.py --config {args.batch}"
        execute_command(cmd)
    else:
        print("使用默认批量配置")
        cmd = "python3 scripts/batch_crawler.py"
        execute_command(cmd)

def execute_command(cmd):
    """执行命令"""
    
    print(f"执行命令: {cmd}")
    
    import subprocess
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"命令执行成功")
            print(f"输出: {result.stdout}")
        else:
            print(f"命令执行失败")
            print(f"错误: {result.stderr}")
            
    except Exception as e:
        print(f"执行命令出错: {e}")

def create_report(data_file, format):
    """创建报告"""
    
    print(f"创建{format}格式报告...")
    
    if format == 'json':
        # 已经保存为JSON
        print(f"JSON数据已保存在: {data_file}")
        
    elif format == 'csv':
        cmd = f"python3 scripts/convert_to_csv.py -i {data_file} -o {data_file.replace('.json', '.csv')}"
        execute_command(cmd)
        
    elif format == 'html':
        cmd = f"python3 scripts/create_html_report.py -i {data_file} -o {data_file.replace('.json', '.html')}"
        execute_command(cmd)

if __name__ == "__main__":
    main()