#!/usr/bin/env python3
"""
从 wanxiang.json 提取 character_book 内容生成 markdown 文件
用法: python extract_character_book.py [--input INPUT] [--output OUTPUT]
"""

import json
import os
import re
import argparse
from pathlib import Path


def sanitize_filename(name):
    """清理文件名，移除非法字符"""
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, '_', name).strip()


def extract_character_book(input_path, output_dir):
    """
    从 JSON 文件提取 character_book 内容
    
    Args:
        input_path: wanxiang.json 文件路径
        output_dir: 输出目录
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # JSON 结构: data -> character_book -> entries
    data_section = data.get('data', {})
    character_book = data_section.get('character_book', {})
    entries = character_book.get('entries', [])
    
    if not entries:
        print("没有找到 data.character_book.entries")
        print(f"调试: data keys = {list(data.keys())}")
        if data_section:
            print(f"调试: data.data keys = {list(data_section.keys())}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建索引文件
    index_content = "# 万象原版\n\n"
    index_content += "> 从原始配置 JSON 提取的原始配置内容\n\n"
    index_content += "## 章节导航\n\n"
    index_content += "| 序号 | 名称 | 文件 |\n"
    index_content += "|------|------|------|\n"
    
    print(f"找到 {len(entries)} 个条目")
    
    for entry in entries:
        entry_id = entry.get('id', 0)
        name = entry.get('name', '未命名')
        content = entry.get('content', '')
        enabled = entry.get('enabled', True)
        comment = entry.get('comment', '')
        
        if not content:
            print(f"跳过空内容: {name}")
            continue
        
        safe_name = sanitize_filename(name)
        filename = f"{entry_id:02d}-{safe_name}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            if comment:
                f.write(f"> 注释: {comment}\n\n")
            f.write(f"> ID: {entry_id} | 启用: {'是' if enabled else '否'}\n\n")
            f.write("---\n\n")
            f.write(content)
        
        print(f"已创建: {filename}")
        
        index_content += f"| {entry_id} | {name} | [{filename}](./{filename}) |\n"
    
    # 保存索引文件
    index_path = os.path.join(output_dir, "index.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\n完成! 共提取 {len(entries)} 个条目")
    print(f"索引文件: {index_path}")


def main():
    parser = argparse.ArgumentParser(description='提取 character_book 内容')
    parser.add_argument('--input', '-i', 
                        default='wanxiang.json',
                        help='输入 JSON 文件路径')
    parser.add_argument('--output', '-o',
                        default='output',
                        help='输出目录')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_path.exists():
        print(f"错误: 输入文件不存在 - {input_path}")
        return
    
    extract_character_book(input_path, output_dir)


if __name__ == "__main__":
    main()
