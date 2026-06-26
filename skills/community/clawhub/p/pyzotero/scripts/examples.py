#!/usr/bin/env python3
"""
PyZotero 使用示例脚本

演示如何使用 pyzotero.py 脚本的各种功能
"""

import subprocess
import os
import json

# 设置环境变量 (根据需要修改)
# os.environ['ZOTERO_LOCAL'] = 'true'  # 本地模式
# os.environ['ZOTERO_LOCAL'] = 'false'  # 在线模式
# os.environ['ZOTERO_USER_ID'] = 'your_user_id'
# os.environ['ZOTERO_API_KEY'] = 'your_api_key'

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'pyzotero.py')


def run_command(args):
    """运行 pyzotero.py 命令"""
    cmd = ['python3', SCRIPT_PATH] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def example_basic_search():
    """示例 1: 基本搜索"""
    print("=" * 60)
    print("示例 1: 基本搜索")
    print("=" * 60)
    
    stdout, stderr, code = run_command(['search', '-q', 'machine learning', '-l', '5'])
    print(stdout)
    if stderr:
        print(f"[STDERR] {stderr}")


def example_fulltext_search():
    """示例 2: 全文搜索"""
    print("\n" + "=" * 60)
    print("示例 2: 全文搜索 (包括 PDF)")
    print("=" * 60)
    
    stdout, stderr, code = run_command(['search', '-q', 'neural networks', '--fulltext', '-l', '5'])
    print(stdout)
    if stderr:
        print(f"[STDERR] {stderr}")


def example_filtered_search():
    """示例 3: 按类型过滤搜索"""
    print("\n" + "=" * 60)
    print("示例 3: 按项目类型过滤")
    print("=" * 60)
    
    stdout, stderr, code = run_command(['search', '-q', 'python', '--itemtype', 'journalArticle', '-l', '5'])
    print(stdout)
    if stderr:
        print(f"[STDERR] {stderr}")


def example_json_output():
    """示例 4: JSON 输出"""
    print("\n" + "=" * 60)
    print("示例 4: JSON 输出")
    print("=" * 60)
    
    stdout, stderr, code = run_command(['search', '-q', 'deep learning', '--json', '-l', '3'])
    
    if code == 0:
        data = json.loads(stdout)
        print(f"找到 {len(data)} 个项目")
        if data:
            print(f"\n第一个项目标题：{data[0]['data'].get('title', 'N/A')}")
    if stderr:
        print(f"[STDERR] {stderr}")


def example_list_collections():
    """示例 5: 列出所有集合"""
    print("\n" + "=" * 60)
    print("示例 5: 列出所有集合")
    print("=" * 60)
    
    stdout, stderr, code = run_command(['listcollections'])
    print(stdout)
    if stderr:
        print(f"[STDERR] {stderr}")


def example_item_types():
    """示例 6: 列出项目类型"""
    print("\n" + "=" * 60)
    print("示例 6: 列出项目类型")
    print("=" * 60)
    
    stdout, stderr, code = run_command(['itemtypes'])
    print(stdout)
    if stderr:
        print(f"[STDERR] {stderr}")


def example_daily_review():
    """示例 7: 每日文献回顾工作流"""
    print("\n" + "=" * 60)
    print("示例 7: 每日文献回顾工作流")
    print("=" * 60)
    
    # 搜索最近添加的论文 (假设标签包含 "2024" 或 "new")
    topics = ['machine learning', 'deep learning', 'artificial intelligence']
    
    for topic in topics:
        print(f"\n📚 搜索主题：{topic}")
        stdout, stderr, code = run_command(['search', '-q', topic, '-l', '3'])
        if code == 0 and stdout.strip():
            # 只显示前几行
            lines = stdout.split('\n')[:10]
            print('\n'.join(lines))
            print("...")


def main():
    print("PyZotero 使用示例")
    print("请确保已正确配置环境变量并启动 Zotero (本地模式) 或设置 API 密钥 (在线模式)\n")
    
    # 运行所有示例
    example_basic_search()
    example_fulltext_search()
    example_filtered_search()
    example_json_output()
    example_list_collections()
    example_item_types()
    example_daily_review()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
