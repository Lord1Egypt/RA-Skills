# -*- coding: utf-8 -*-
"""
编码检测工具

用于自动检测 CSV 文件的编码格式
"""

import codecs
import chardet
from typing import List, Optional, Tuple


def detect_encoding(file_path: str, 
                    encoding_list: Optional[List[str]] = None) -> str:
    """
    检测文件编码
    
    Args:
        file_path: 文件路径
        encoding_list: 尝试的编码列表，默认为常用编码列表
    
    Returns:
        检测到的编码格式
    """
    if encoding_list is None:
        encoding_list = [
            'utf-8-sig',  # 带BOM的UTF-8
            'utf-8',      # 标准UTF-8
            'gbk',        # 中文GBK
            'gb2312',     # 中文GB2312
            'gb18030',    # 中文GB18030
            'latin-1'     # 通用拉丁字符集（兼容性最好）
        ]
    
    # 方法1: 使用 chardet 自动检测
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 读取前10KB用于检测
            result = chardet.detect(raw_data)
            if result['confidence'] > 0.7:
                detected_encoding = result['encoding']
                if detected_encoding.lower().startswith('utf'):
                    detected_encoding = detected_encoding.lower()
                # 验证检测的编码是否可用
                try:
                    with open(file_path, 'r', encoding=detected_encoding) as f:
                        f.read(1000)
                    return detected_encoding
                except:
                    pass
    except Exception as e:
        print(f"chardet 检测失败: {e}")
    
    # 方法2: 依次尝试编码列表
    for encoding in encoding_list:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # 尝试读取前几行
                f.read(1000)
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # 如果都失败了，返回 latin-1 作为最后的尝试
    return 'latin-1'


def try_read_file(file_path: str, encoding_list: List[str]) -> Tuple[Optional[str], str]:
    """
    尝试读取文件并返回内容
    
    Args:
        file_path: 文件路径
        encoding_list: 编码列表
    
    Returns:
        (文件内容, 使用的编码) 的元组，如果失败则返回 (None, '')
    """
    for encoding in encoding_list:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    return None, ''


def is_bom_encoding(encoding: str) -> bool:
    """
    检查编码是否包含BOM
    
    Args:
        encoding: 编码名称
    
    Returns:
        是否包含BOM
    """
    return encoding.lower().endswith('-sig') or encoding.lower() == 'utf-8-sig'
