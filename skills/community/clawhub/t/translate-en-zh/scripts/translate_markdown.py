#!/usr/bin/env python3
"""
Markdown文档翻译工具
保留原始格式，仅翻译文本内容
"""
import re
import sys
import argparse
from translate_batch import translate_text

def is_markdown_special(line: str) -> bool:
    """
    判断是否是Markdown特殊格式行，不需要翻译
    """
    # 代码块标记
    if line.strip().startswith('```'):
        return True
    # 标题
    if line.strip().startswith('#'):
        return False  # 标题需要翻译
    # 图片
    if re.match(r'!\[.*\]\(.*\)', line.strip()):
        return False  # 图片alt文本需要翻译
    # 链接
    if re.match(r'\[.*\]\(.*\)', line.strip()):
        return False  # 链接文本需要翻译
    # 列表项
    if line.strip().startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\. ', line.strip()):
        return False  # 列表内容需要翻译
    # 水平线
    if line.strip() in ('---', '***', '___'):
        return True
    # 引用块标记
    if line.strip().startswith('>'):
        return False  # 引用内容需要翻译
    # 表格分隔线
    if re.match(r'^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$', line.strip()):
        return True
    # HTML标签
    if re.match(r'<[^>]+>', line.strip()):
        return True
    # 注释
    if line.strip().startswith('<!--') and line.strip().endswith('-->'):
        return True
    # 代码行（缩进4个空格或tab）
    if line.startswith('    ') or line.startswith('\t'):
        return True
    return False

def translate_markdown_line(line: str, target_lang: str = None) -> str:
    """
    翻译单行Markdown内容，保留格式
    """
    original_line = line
    leading_spaces = len(line) - len(line.lstrip())
    line_stripped = line.lstrip()
    
    # 处理列表项
    list_match = re.match(r'^([-*+] |\d+\. )(.*)$', line_stripped)
    if list_match:
        prefix = list_match.group(1)
        content = list_match.group(2)
        translated = translate_text(content, target_lang)
        return ' ' * leading_spaces + prefix + translated
    
    # 处理引用块
    quote_match = re.match(r'^(>+) ?(.*)$', line_stripped)
    if quote_match:
        prefix = quote_match.group(1) + ' '
        content = quote_match.group(2)
        translated = translate_text(content, target_lang)
        return ' ' * leading_spaces + prefix + translated
    
    # 处理标题
    heading_match = re.match(r'^(#{1,6}) (.*)$', line_stripped)
    if heading_match:
        prefix = heading_match.group(1) + ' '
        content = heading_match.group(2)
        translated = translate_text(content, target_lang)
        return ' ' * leading_spaces + prefix + translated
    
    # 处理图片
    def replace_image(match):
        alt_text = match.group(1)
        url = match.group(2)
        translated_alt = translate_text(alt_text, target_lang)
        return f'![{translated_alt}]({url})'
    
    line_stripped = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_image, line_stripped)
    
    # 处理链接
    def replace_link(match):
        link_text = match.group(1)
        url = match.group(2)
        translated_text = translate_text(link_text, target_lang)
        return f'[{translated_text}]({url})'
    
    line_stripped = re.sub(r'\[(.*?)\]\((.*?)\)', replace_link, line_stripped)
    
    # 处理加粗
    def replace_bold(match):
        content = match.group(1)
        translated = translate_text(content, target_lang)
        return f'**{translated}**'
    
    line_stripped = re.sub(r'\*\*(.*?)\*\*', replace_bold, line_stripped)
    
    # 处理斜体
    def replace_italic(match):
        content = match.group(1)
        translated = translate_text(content, target_lang)
        return f'*{translated}*'
    
    line_stripped = re.sub(r'\*(.*?)\*', replace_italic, line_stripped)
    
    # 处理行内代码
    parts = re.split(r'(`[^`]+`)', line_stripped)
    translated_parts = []
    for part in parts:
        if part.startswith('`') and part.endswith('`'):
            translated_parts.append(part)  # 代码不翻译
        else:
            translated_parts.append(translate_text(part, target_lang))
    
    line_stripped = ''.join(translated_parts)
    
    return ' ' * leading_spaces + line_stripped

def translate_markdown_file(input_path: str, output_path: str = None, target_lang: str = None) -> None:
    """
    翻译Markdown文件
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        translated_lines = []
        in_code_block = False
        
        for line in lines:
            original_line = line.rstrip('\n')
            
            # 处理代码块
            if original_line.strip().startswith('```'):
                in_code_block = not in_code_block
                translated_lines.append(original_line)
                continue
            
            if in_code_block:
                translated_lines.append(original_line)
                continue
            
            # 空行直接保留
            if original_line.strip() == '':
                translated_lines.append('')
                continue
            
            # 特殊格式行
            if is_markdown_special(original_line):
                translated_lines.append(original_line)
                continue
            
            # 翻译普通行
            translated = translate_markdown_line(original_line, target_lang)
            translated_lines.append(translated)
        
        translated_content = '\n'.join(translated_lines) + '\n'
        
        if output_path is None:
            output_path = f"{input_path}.translated"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"Markdown翻译完成，结果已保存到: {output_path}")
        
    except Exception as e:
        print(f"翻译失败: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Markdown文档翻译工具')
    parser.add_argument('input', help='输入Markdown文件路径')
    parser.add_argument('--target', '-t', choices=['zh', 'en'], help='目标语言，zh=中文，en=英文，默认自动识别')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    translate_markdown_file(args.input, args.output, args.target)

if __name__ == '__main__':
    main()
