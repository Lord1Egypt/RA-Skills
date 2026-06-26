#!/usr/bin/env python3
"""
批量发布工具
- 批量发布目录中的所有文章
- 支持草稿箱一键发布
- 支持定时发布（待实现）
"""
import os
import sys
import time
from datetime import datetime
from publish_post import publish_from_file, load_env

def batch_publish(directory='articles', publish_now=True, delay=2):
    """
    批量发布目录中的所有 Markdown 文件
    
    Args:
        directory: 文章目录
        publish_now: True=立即发布，False=保存草稿
        delay: 每篇文章之间的延迟（秒）
    """
    if not os.path.exists(directory):
        print(f"❌ 目录不存在：{directory}")
        return
    
    # 查找所有 Markdown 文件
    md_files = [f for f in os.listdir(directory) if f.endswith('.md')]
    
    if not md_files:
        print(f"📭 目录中没有 Markdown 文件")
        return
    
    print(f"📦 找到 {len(md_files)} 篇文章：")
    for f in md_files:
        print(f"  - {f}")
    
    print(f"\n{'✅ 立即发布' if publish_now else '💾 保存草稿'}，间隔 {delay}秒")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for i, filename in enumerate(md_files, 1):
        filepath = os.path.join(directory, filename)
        print(f"\n[{i}/{len(md_files)}] 处理：{filename}")
        
        # 发布
        result = publish_from_file(filepath, publish_now=publish_now)
        
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        # 延迟（避免请求过快）
        if i < len(md_files):
            print(f"⏳ 等待 {delay}秒...")
            time.sleep(delay)
    
    print("\n" + "=" * 60)
    print("📊 批量发布完成：")
    print(f"  成功：{success_count} 篇")
    print(f"  失败：{fail_count} 篇")
    print(f"  总计：{len(md_files)} 篇")

def publish_drafts():
    """将草稿箱的文章全部发布"""
    print("🚀 功能待实现：需要先从博客获取草稿列表")
    print("   当前建议：在博客后台手动发布草稿")

def print_help():
    print("""
📦 批量发布工具

用法:
  python3 batch_publish.py [目录] [--draft] [--delay=秒数]

示例:
  python3 batch_publish.py articles           # 发布 articles 目录
  python3 batch_publish.py articles --draft   # 保存为草稿
  python3 batch_publish.py articles --delay=5 # 每篇间隔 5 秒
  python3 batch_publish.py --help             # 显示帮助
""")

if __name__ == "__main__":
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    
    # 解析参数
    directory = 'articles'
    publish_now = True
    delay = 2
    
    for arg in sys.argv[1:]:
        if arg == '--draft':
            publish_now = False
        elif arg.startswith('--delay='):
            try:
                delay = int(arg.split('=')[1])
            except:
                pass
        elif not arg.startswith('--'):
            directory = arg
    
    batch_publish(directory, publish_now, delay)
