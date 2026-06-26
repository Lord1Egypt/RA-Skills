#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word文档读取工具 - OpenClaw Skill
支持 .docx 和 .doc 格式，完美支持中文

作者: 叶文洁
版本: 1.0.0
"""

import os
import sys
import argparse
from pathlib import Path

def read_docx(filepath):
    """
    读取 .docx 文件
    
    Args:
        filepath: 文件路径 (str 或 Path)
    
    Returns:
        list: 段落文本列表
    """
    try:
        from docx import Document
    except ImportError:
        print("[错误] 缺少 python-docx 库")
        print("请运行: pip install python-docx")
        sys.exit(1)
    
    doc = Document(str(filepath))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return paragraphs

def read_doc_ole(filepath):
    """
    使用OLE读取旧版 .doc 文件
    
    注意：这是简化解析，复杂格式可能无法完美提取
    
    Args:
        filepath: 文件路径
    
    Returns:
        list: 段落文本列表
    """
    try:
        import olefile
    except ImportError:
        print("[错误] 缺少 olefile 库")
        print("请运行: pip install olefile")
        sys.exit(1)
    
    ole = olefile.OleFileIO(str(filepath))
    
    if not ole.exists('WordDocument'):
        ole.close()
        raise ValueError("无法找到WordDocument流，可能不是有效的.doc文件")
    
    data = ole.openstream('WordDocument').read()
    ole.close()
    
    # 提取可打印字符
    text = ''
    for i in range(0, len(data) - 1, 2):
        char = data[i]
        if 32 <= char <= 126 or char in [10, 13]:
            text += chr(char)
    
    return [line for line in text.split('\n') if line.strip()]

def read_word_document(filepath):
    """
    读取Word文档，自动判断格式
    
    Args:
        filepath: Word文档路径 (str 或 Path)
    
    Returns:
        list: 段落文本列表
    
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的文件格式
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"[错误] 文件不存在: {filepath}")
    
    suffix = filepath.suffix.lower()
    
    if suffix == '.docx':
        return read_docx(filepath)
    elif suffix == '.doc':
        return read_doc_ole(filepath)
    else:
        raise ValueError(f"[错误] 不支持的文件格式: {suffix}，仅支持 .doc 和 .docx")

def search_in_document(filepath, keywords):
    """
    在Word文档中搜索关键词
    
    Args:
        filepath: Word文档路径
        keywords: 关键词列表 (list)
    
    Returns:
        list: 包含关键词的段落列表，格式为 "[第N段] 内容"
    """
    paragraphs = read_word_document(filepath)
    results = []
    
    for i, para in enumerate(paragraphs):
        for kw in keywords:
            if kw in para:
                results.append(f"[第{i+1}段] {para}")
                break
    
    return results

def save_as_text(paragraphs, output_path):
    """
    保存段落列表为UTF-8文本文件
    
    Args:
        paragraphs: 段落列表
        output_path: 输出文件路径
    """
    output_path = Path(output_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(paragraphs))
    print(f"✅ 已保存: {output_path}")

def analyze_document(filepath):
    """
    分析文档基本信息
    
    Args:
        filepath: Word文档路径
    
    Returns:
        dict: 包含文件大小、段落数等信息
    """
    filepath = Path(filepath)
    paragraphs = read_word_document(filepath)
    
    total_chars = sum(len(p) for p in paragraphs)
    
    return {
        'filename': filepath.name,
        'size': filepath.stat().st_size,
        'paragraphs': len(paragraphs),
        'total_chars': total_chars
    }

def main():
    parser = argparse.ArgumentParser(
        description='Word文档读取工具 - 支持.docx和.doc格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "文档.docx"                          # 基本读取
  %(prog)s "文档.docx" -l 50                    # 显示前50段
  %(prog)s "文档.docx" -s "关键词1,关键词2"      # 搜索关键词
  %(prog)s "文档.docx" -o "输出.txt"            # 保存为文本
        """
    )
    parser.add_argument('filepath', help='Word文档路径')
    parser.add_argument('--output', '-o', help='输出文本文件路径')
    parser.add_argument('--search', '-s', help='搜索关键词（多个用逗号分隔）')
    parser.add_argument('--limit', '-l', type=int, default=100, 
                       help='显示前N段（默认100）')
    parser.add_argument('--info', '-i', action='store_true',
                       help='只显示文档信息')
    
    args = parser.parse_args()
    
    try:
        # 读取文档
        print(f"[信息] 正在读取: {args.filepath}")
        paragraphs = read_word_document(args.filepath)
        
        # 仅显示信息模式
        if args.info:
            info = analyze_document(args.filepath)
            print(f"\n[信息] 文档信息:")
            print(f"  文件名: {info['filename']}")
            print(f"  文件大小: {info['size']:,} 字节")
            print(f"  段落数: {info['paragraphs']}")
            print(f"  总字符: {info['total_chars']:,}")
            return
        
        print(f"[成功] 读取完成，共 {len(paragraphs)} 段\n")
        
        # 搜索模式
        if args.search:
            keywords = [k.strip() for k in args.search.split(',')]
            print(f"[搜索] 搜索关键词: {', '.join(keywords)}")
            results = search_in_document(args.filepath, keywords)
            print(f"\n[结果] 找到 {len(results)} 条结果:\n")
            for r in results[:100]:  # 最多显示100条
                print(r)
                print()
            if len(results) > 100:
                print(f"... 还有 {len(results) - 100} 条结果未显示")
        
        # 输出模式
        elif args.output:
            save_as_text(paragraphs, args.output)
        
        # 显示模式
        else:
            print("=" * 60)
            print("[内容] 内容预览")
            print("=" * 60)
            for i, para in enumerate(paragraphs[:args.limit]):
                print(f"\n[{i+1}] {para}")
            
            if len(paragraphs) > args.limit:
                print(f"\n... 还有 {len(paragraphs) - args.limit} 段 (使用 -l 参数查看更多)")
                
    except FileNotFoundError as e:
        print(f"[错误] {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"[错误] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[错误] 读取失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
