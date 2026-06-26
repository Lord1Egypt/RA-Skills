#!/usr/bin/env python3
"""标题转安全文件名"""

import re
import sys

def safe_filename(title: str, max_len: int = 50) -> str:
    """
    将标题转换为安全的文件名
    
    处理：
    1. 英文特殊符号: / \ : * ? " < > |
    2. 中文标点: ：？＂《》【】
    3. 空格 → 下划线
    4. 按字符截断（不是字节，避免 UTF-8 问题）
    5. 去除首尾空格和点
    """
    # 替换英文不允许的字符
    filename = re.sub(r'[\/\\:*?"<>|]', '_', title)
    
    # 替换中文标点
    filename = re.sub(r'[：？！＂《》【】「」『』（）]', '_', filename)
    
    # 替换空格为下划线
    filename = filename.replace(' ', '_')
    
    # 替换连续下划线为单个
    filename = re.sub(r'_+', '_', filename)
    
    # 按字符截断（不是字节）
    filename = filename[:max_len]
    
    # 去除首尾的下划线和点
    filename = filename.strip('_.')
    
    # 如果为空，返回 default
    if not filename:
        filename = 'untitled'
    
    return filename

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: safe_filename.py <标题>")
        sys.exit(1)
    
    title = sys.argv[1]
    result = safe_filename(title)
    print(result)