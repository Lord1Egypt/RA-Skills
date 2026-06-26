#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理日志文件中的敏感信息
"""

import re
from pathlib import Path

def clean_log_file(file_path: Path):
    """清理单个日志文件"""
    if not file_path.exists():
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 替换 media_id（微信临时素材 ID）
    content = re.sub(
        r'media_id=Id2T[a-zA-Z0-9_-]{40,}',
        'media_id=***REDACTED***',
        content
    )
    
    # 替换草稿 ID
    content = re.sub(
        r'草稿 ID: Id2T[a-zA-Z0-9_-]{40,}',
        '草稿 ID: ***REDACTED***',
        content
    )
    
    # 替换草稿创建成功的 ID
    content = re.sub(
        r'草稿创建成功：Id2T[a-zA-Z0-9_-]{40,}',
        '草稿创建成功：***REDACTED***',
        content
    )
    
    # 替换完整的 access_token（保留格式但隐藏值）
    content = re.sub(
        r'Token: [a-zA-Z0-9_-]{20,}',
        'Token: ***REDACTED***',
        content
    )
    
    # 替换图片 URL（包含 mmbiz.qpic.cn 的）
    content = re.sub(
        r'http://mmbiz\.qpic\.cn/[a-zA-Z0-9/_-]{50,}',
        'http://mmbiz.qpic.cn/***REDACTED***',
        content
    )
    
    content = re.sub(
        r'https://mmbiz\.qpic\.cn/[a-zA-Z0-9/_-]{50,}',
        'https://mmbiz.qpic.cn/***REDACTED***',
        content
    )
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已清理：{file_path.name}")
        return True
    else:
        print(f"⚠️  无需清理：{file_path.name}")
        return False

def main():
    logs_dir = Path('/Users/brucesong/.openclaw/workspace/Bruce/wechat-mp-publish/logs')
    
    print("=" * 60)
    print("清理日志文件中的敏感信息")
    print("=" * 60)
    
    cleaned = 0
    for log_file in logs_dir.glob('*.log'):
        if clean_log_file(log_file):
            cleaned += 1
    
    print()
    print("=" * 60)
    print(f"清理完成，共清理 {cleaned} 个文件")
    print("=" * 60)

if __name__ == '__main__':
    main()
