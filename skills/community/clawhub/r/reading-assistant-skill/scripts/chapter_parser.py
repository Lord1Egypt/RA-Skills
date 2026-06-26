#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节识别脚本
从文本中识别章节信息，支持多种章节格式
"""

import sys
import json
import re
from typing import Dict, Optional, List


def parse_chapter(text: str) -> Dict[str, any]:
    """
    从文本中识别章节信息
    
    参数:
        text: 待识别的文本内容
    
    返回:
        {
            "success": True/False,
            "chapter": "识别到的章节信息",
            "chapter_type": "章节类型",
            "confidence": 0.0-1.0,
            "error": "错误信息（如果失败）"
        }
    """
    try:
        if not text or not text.strip():
            return {
                "success": False,
                "error": "文本内容为空"
            }
        
        # 章节识别规则（按优先级排序）
        rules = [
            # 规则1：中文章节格式
            {
                "pattern": r'(第[一二三四五六七八九十百千万零\d]+[章节回部篇卷集])',
                "type": "chinese_chapter",
                "priority": 1
            },
            # 规则2：带括号的章节
            {
                "pattern": r'[（\(]第[一二三四五六七八九十百千万零\d]+[章节回部篇卷集][）\)]',
                "type": "bracketed_chapter",
                "priority": 2
            },
            # 规则3：英文章节格式
            {
                "pattern": r'(Chapter\s+\d+)',
                "type": "english_chapter",
                "priority": 3,
                "flags": re.IGNORECASE
            },
            # 规则4：数字编号格式
            {
                "pattern": r'^(\d+[\.\、\s])',
                "type": "numeric",
                "priority": 4
            },
            # 规则5：页码格式（P123、第123页）
            {
                "pattern": r'[Pp](\d+)|第(\d+)页',
                "type": "page_number",
                "priority": 5
            },
            # 规则6：标题格式（# 标题）
            {
                "pattern": r'^#+\s*(.+)$',
                "type": "markdown_header",
                "priority": 6
            }
        ]
        
        # 按优先级尝试匹配
        matched_results = []
        
        for rule in rules:
            flags = rule.get("flags", 0)
            pattern = rule["pattern"]
            
            # 多行匹配
            matches = re.finditer(pattern, text, flags | re.MULTILINE)
            
            for match in matches:
                matched_results.append({
                    "chapter": match.group(0).strip(),
                    "type": rule["type"],
                    "priority": rule["priority"],
                    "position": match.start()
                })
        
        # 如果有匹配结果，选择优先级最高且位置最靠前的
        if matched_results:
            # 按优先级和位置排序
            matched_results.sort(key=lambda x: (x["priority"], x["position"]))
            best_match = matched_results[0]
            
            return {
                "success": True,
                "chapter": best_match["chapter"],
                "chapter_type": best_match["type"],
                "confidence": 0.9 if best_match["priority"] <= 2 else 0.7,
                "all_matches": [
                    {
                        "chapter": r["chapter"],
                        "type": r["type"]
                    } for r in matched_results[:3]  # 最多返回3个匹配结果
                ]
            }
        
        # 如果没有明确匹配，尝试模糊识别
        # 检查文本开头是否包含可能的章节标识
        first_line = text.split('\n')[0].strip()
        
        if len(first_line) < 50:  # 短行可能是章节标题
            # 检查是否包含关键词
            keywords = ['章', '节', '回', '篇', 'PART', 'CHAPTER', 'SECTION']
            for keyword in keywords:
                if keyword in first_line.upper():
                    return {
                        "success": True,
                        "chapter": first_line,
                        "chapter_type": "inferred",
                        "confidence": 0.5,
                        "note": "基于关键词推断"
                    }
        
        return {
            "success": False,
            "error": "未能识别章节信息",
            "suggestion": "请手动指定章节信息"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"章节识别失败: {str(e)}"
        }


def infer_from_context(text: str, previous_chapter: Optional[str] = None) -> Dict[str, any]:
    """
    基于上下文推断章节信息
    
    参数:
        text: 当前文本
        previous_chapter: 前一条摘录的章节信息
    
    返回:
        同 parse_chapter
    """
    result = parse_chapter(text)
    
    # 如果识别成功，直接返回
    if result["success"]:
        return result
    
    # 如果识别失败，但有上一条章节信息，使用上一条的章节
    if previous_chapter:
        return {
            "success": True,
            "chapter": previous_chapter,
            "chapter_type": "inherited",
            "confidence": 0.6,
            "note": "继承上一条摘录的章节信息"
        }
    
    return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "缺少参数。用法: python chapter_parser.py <text>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    text = sys.argv[1]
    previous_chapter = sys.argv[2] if len(sys.argv) > 2 else None
    
    if previous_chapter:
        result = infer_from_context(text, previous_chapter)
    else:
        result = parse_chapter(text)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
