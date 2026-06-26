#!/usr/bin/env python3
"""
微信公众号发布前检查脚本
检查 Markdown 文章是否符合发布标准
"""

import sys
import os
import re
import yaml


def print_error(msg):
    print(f"- ERROR: {msg}")


def print_warn(msg):
    print(f"- WARN: {msg}")


def print_passed():
    print("CHECK PASSED")


def print_failed():
    print("CHECK FAILED")


def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    if not content.startswith('---'):
        return None
    
    end_idx = content.find('---', 3)
    if end_idx == -1:
        return None
    
    frontmatter_text = content[3:end_idx].strip()
    try:
        return yaml.safe_load(frontmatter_text)
    except Exception:
        return None


def check_markdown(filepath):
    """执行所有检查项"""
    errors = []
    warnings = []
    
    # 1. 检查文件是否存在
    if not os.path.exists(filepath):
        print_error(f"文件不存在: {filepath}")
        return False
    
    # 读取文件内容
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print_error(f"无法读取文件: {e}")
        return False
    
    # 2. 检查 frontmatter
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        errors.append("缺少 frontmatter")
    else:
        # 3. 检查 title
        if 'title' not in frontmatter:
            errors.append("frontmatter 中缺少 title")
        
        # 4. 检查 cover
        if 'cover' not in frontmatter:
            errors.append("frontmatter 中缺少 cover")
        else:
            cover = frontmatter.get('cover', '')
            if cover.startswith('http://') or cover.startswith('https://'):
                # URL 类型，认为有效
                pass
            elif cover.startswith('file://'):
                # 本地文件
                local_path = cover.replace('file://', '')
                if not os.path.exists(local_path):
                    errors.append(f"cover 文件不存在: {local_path}")
            elif cover:
                # 尝试作为相对路径
                base_dir = os.path.dirname(os.path.abspath(filepath))
                local_path = os.path.join(base_dir, cover)
                if not os.path.exists(local_path):
                    errors.append(f"cover 文件不存在: {local_path}")
    
    # 5. 检查 Markdown 中的图片路径
    img_pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
    for match in re.finditer(img_pattern, content):
        img_path = match.group(2)
        # 跳过外部 URL
        if img_path.startswith('http://') or img_path.startswith('https://'):
            continue
        # 检查本地文件
        base_dir = os.path.dirname(os.path.abspath(filepath))
        full_path = os.path.join(base_dir, img_path)
        if not os.path.exists(full_path):
            errors.append(f"图片文件不存在: {img_path}")
    
    # 6. 检查 Obsidian wiki 链接
    wiki_pattern = r'!\[\[([^\]]+)\]\]'
    if re.search(wiki_pattern, content):
        warnings.append("发现 Obsidian wiki 图片链接 ![[...]]，微信不支持")
    
    # 7. 检查未标注语言的 code block
    code_block_pattern = r'```(\w*)\s*\n'
    for match in re.finditer(r'```', content):
        start = match.start()
        # 找到对应的结束 ``` 
        end = content.find('```', start + 3)
        if end != -1:
            block_content = content[start:end]
            # 检查是否没有语言标注（开头只有 ``` 后直接是换行或空格）
            if re.match(r'```\s*\n', block_content):
                # 无语言标注
                warnings.append("发现未标注语言的 fenced code block")
                break
    
    # 输出结果
    for err in errors:
        print_error(err)
    
    for warn in warnings:
        print_warn(warn)
    
    if errors:
        print_failed()
        return False
    
    if warnings:
        print_passed()
        return True
    
    print_passed()
    return True


def main():
    if len(sys.argv) != 2:
        print_error("用法: python3 scripts/check.py <markdown_file>")
        sys.exit(2)
    
    filepath = sys.argv[1]
    success = check_markdown(filepath)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
