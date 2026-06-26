#!/usr/bin/env python3
"""
微信公众号文章格式化工具
将 Markdown 转换为公众号编辑器粘贴格式
"""

import re
import sys

def format_for_wechat(md_content):
    """转换为公众号友好格式"""
    lines = md_content.split('\n')
    result = []
    in_code = False
    
    for line in lines:
        line = line.rstrip()
        
        # 代码块处理
        if line.strip().startswith('```'):
            in_code = not in_code
            if in_code:
                result.append('【代码块】')
            else:
                result.append('【代码块结束】')
            continue
        
        if in_code:
            result.append('    ' + line)
            continue
        
        # 去除 markdown 标题符号
        if line.startswith('# '):
            result.append(line[2:])
            result.append('')
        elif line.startswith('## '):
            result.append('  ' + line[3:])
            result.append('')
        elif line.startswith('### '):
            result.append('    ' + line[4:])
            result.append('')
        # 空行
        elif not line.strip():
            result.append('')
        # 列表
        elif line.startswith('- '):
            result.append('• ' + line[2:])
        elif line.startswith('* '):
            result.append('• ' + line[2:])
        else:
            # 处理行内标记
            line = re.sub(r'\*\*(.*?)\*\*', r'【\1】', line)  # 加粗
            line = re.sub(r'\*(.*?)\*', r'\1', line)         # 斜体
            result.append(line)
    
    # 清理多余空行
    cleaned = []
    prev_empty = False
    for line in result:
        if not line.strip():
            if not prev_empty:
                cleaned.append(line)
                prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False
    
    return '\n'.join(cleaned)

def main():
    if len(sys.argv) < 2:
        print("用法: wechat-formatter <markdown文件>")
        print("   或: wechat-formatter --stdin")
        sys.exit(1)
    
    if sys.argv[1] == '--stdin':
        md_content = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            md_content = f.read()
    
    formatted = format_for_wechat(md_content)
    print(formatted)

if __name__ == "__main__":
    main()