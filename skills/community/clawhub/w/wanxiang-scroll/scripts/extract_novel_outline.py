#!/usr/bin/env python3
"""
从小说TXT文件中提取章节大纲和结构
- 识别章节标题、卷结构
- 提取关键情节点
- 输出结构化大纲JSON

用法:
  python3 scripts/extract_novel_outline.py --input INPUT_TXT --output OUTPUT_JSON
  python3 scripts/extract_novel_outline.py --dir INPUT_DIR --output-dir OUTPUT_DIR

参数:
  --input       单个TXT文件路径
  --output      单个文件输出JSON路径
  --dir         批量处理目录
  --output-dir  批量输出目录
  --max-chars   最大读取字符数 (默认: 500000, 约50万字)
"""

import argparse
import json
import os
import re
import sys
from collections import Counter


# 章节标题匹配模式（按优先级排序）
CHAPTER_PATTERNS = [
    # 第X卷/第X章 格式
    re.compile(r'^第[零一二三四五六七八九十百千万\d]+[卷章集部篇回]\s*.{0,50}$', re.MULTILINE),
    # 卷X/章X 格式
    re.compile(r'^[卷章集部篇回]\s*[零一二三四五六七八九十百千万\d]+\s*.{0,50}$', re.MULTILINE),
    # Chapter X 格式
    re.compile(r'^[Cc]hapter\s+\d+.*$', re.MULTILINE),
    # 第X话 格式
    re.compile(r'^第\d+话\s*.{0,50}$', re.MULTILINE),
    # 纯数字章节 如 "1" "001"
    re.compile(r'^\d{1,5}\s*$', re.MULTILINE),
    # 【标题】格式
    re.compile(r'^【[^】]{1,50}】$', re.MULTILINE),
    # 章节标记+标题 如 "第一章 标题"
    re.compile(r'^[第][\d零一二三四五六七八九十百千万]+[章节]\s*\S+', re.MULTILINE),
]


def detect_chapter_pattern(text, sample_size=50000):
    """自动检测最适合的章节匹配模式"""
    sample = text[:sample_size]
    best_pattern = None
    best_count = 0
    
    for pattern in CHAPTER_PATTERNS:
        matches = pattern.findall(sample)
        if len(matches) > best_count:
            best_count = len(matches)
            best_pattern = pattern
    
    return best_pattern, best_count


def extract_chapters(text, pattern=None):
    """从文本中提取章节结构"""
    if pattern is None:
        pattern, _ = detect_chapter_pattern(text)
    
    if pattern is None:
        return []
    
    matches = list(pattern.finditer(text))
    chapters = []
    
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = match.group().strip()
        content = text[start:end]
        
        # 提取章节首段文字（取前200字作为摘要）
        content_body = content[len(title):].strip()
        # 跳过空行
        lines = [l.strip() for l in content_body.split('\n') if l.strip()]
        preview = ' '.join(lines[:3])[:200] if lines else ""
        
        # 统计字数
        char_count = len(content_body)
        
        chapters.append({
            "title": title,
            "char_count": char_count,
            "preview": preview,
            "position": start
        })
    
    return chapters


def detect_volume_structure(chapters):
    """检测卷结构"""
    volumes = []
    current_volume = {"name": "默认卷", "chapters": []}
    
    for chapter in chapters:
        title = chapter["title"]
        # 检测卷标题
        if re.match(r'^第.+卷', title):
            if current_volume["chapters"]:
                volumes.append(current_volume)
            current_volume = {"name": title, "chapters": []}
        else:
            current_volume["chapters"].append(chapter)
    
    if current_volume["chapters"]:
        volumes.append(current_volume)
    
    return volumes


def extract_key_points(text, max_points=10):
    """提取关键情节点"""
    # 简单实现：提取包含关键词的句子
    keywords = ["发现", "决定", "遇到", "战斗", "死亡", "获得", "离开", "到达", "揭示", "背叛"]
    sentences = re.split(r'[。！？\n]', text)
    
    key_points = []
    for sentence in sentences:
        for kw in keywords:
            if kw in sentence and len(sentence) > 10:
                key_points.append(sentence.strip()[:100])
                break
        if len(key_points) >= max_points:
            break
    
    return key_points


def analyze_novel(filepath, max_chars=500000):
    """分析单个小说文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read(max_chars)
    except Exception as e:
        return {"error": str(e)}
    
    # 检测章节模式
    pattern, chapter_count = detect_chapter_pattern(text)
    
    # 提取章节
    chapters = extract_chapters(text, pattern)
    
    # 检测卷结构
    volumes = detect_volume_structure(chapters)
    
    # 提取关键情节点
    key_points = extract_key_points(text)
    
    # 统计信息
    total_chars = len(text)
    total_chapters = len(chapters)
    
    return {
        "filename": os.path.basename(filepath),
        "total_chars": total_chars,
        "total_chapters": total_chapters,
        "chapter_pattern": pattern.pattern if pattern else None,
        "volumes": volumes,
        "key_points": key_points
    }


def main():
    parser = argparse.ArgumentParser(description='提取小说大纲')
    parser.add_argument('--input', '-i', help='单个TXT文件路径')
    parser.add_argument('--output', '-o', help='输出JSON路径')
    parser.add_argument('--dir', '-d', help='批量处理目录')
    parser.add_argument('--output-dir', help='批量输出目录')
    parser.add_argument('--max-chars', type=int, default=500000, help='最大读取字符数')
    
    args = parser.parse_args()
    
    if args.input:
        # 单文件模式
        result = analyze_novel(args.input, args.max_chars)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"已保存到: {args.output}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.dir:
        # 批量模式
        input_dir = Path(args.dir)
        output_dir = Path(args.output_dir) if args.output_dir else input_dir / "outlines"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files = list(input_dir.glob("*.txt"))
        print(f"找到 {len(files)} 个文件")
        
        for i, filepath in enumerate(files):
            print(f"处理 [{i+1}/{len(files)}]: {filepath.name}")
            result = analyze_novel(str(filepath), args.max_chars)
            
            output_file = output_dir / f"{filepath.stem}_outline.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n完成! 输出目录: {output_dir}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
