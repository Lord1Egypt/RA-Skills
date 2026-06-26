#!/usr/bin/env python3
"""
批量文本翻译工具
支持中英文互译，自动识别源语言
"""
import sys
import argparse
from typing import List

def translate_text(text: str, target_lang: str = None) -> str:
    """
    翻译文本
    :param text: 待翻译文本
    :param target_lang: 目标语言，'zh' 或 'en'，自动识别时为 None
    :return: 翻译结果
    """
    # 简单的语言检测（仅检测是否包含中文字符）
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)
    
    # 确定翻译方向
    if target_lang is None:
        target_lang = 'en' if has_chinese else 'zh'
    
    # 这里可以接入实际的翻译API，如百度翻译、谷歌翻译、DeepL等
    # 示例：简单的演示翻译
    if target_lang == 'zh':
        # 英译中示例
        translations = {
            'hello': '你好',
            'world': '世界',
            'hello world': '你好，世界',
            'welcome': '欢迎',
            'thank you': '谢谢',
            'goodbye': '再见'
        }
        return translations.get(text.lower(), f"[翻译] {text}")
    else:
        # 中译英示例
        translations = {
            '你好': 'Hello',
            '世界': 'World',
            '你好世界': 'Hello World',
            '欢迎': 'Welcome',
            '谢谢': 'Thank you',
            '再见': 'Goodbye'
        }
        return translations.get(text, f"[Translate] {text}")

def translate_file(input_path: str, output_path: str = None, target_lang: str = None) -> None:
    """
    翻译文件内容
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径，默认在原文件名后加 .translated
    :param target_lang: 目标语言
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        translated_lines = []
        
        for line in lines:
            if line.strip() == '':
                translated_lines.append('')
                continue
            translated = translate_text(line, target_lang)
            translated_lines.append(translated)
        
        translated_content = '\n'.join(translated_lines)
        
        if output_path is None:
            output_path = f"{input_path}.translated"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"翻译完成，结果已保存到: {output_path}")
        
    except Exception as e:
        print(f"翻译失败: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='中英文批量翻译工具')
    parser.add_argument('input', help='输入文本或文件路径')
    parser.add_argument('--target', '-t', choices=['zh', 'en'], help='目标语言，zh=中文，en=英文，默认自动识别')
    parser.add_argument('--file', '-f', action='store_true', help='输入是文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径（仅文件模式有效）')
    
    args = parser.parse_args()
    
    if args.file:
        translate_file(args.input, args.output, args.target)
    else:
        result = translate_text(args.input, args.target)
        print(result)

if __name__ == '__main__':
    main()
