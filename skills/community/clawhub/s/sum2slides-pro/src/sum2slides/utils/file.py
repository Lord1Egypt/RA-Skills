"""
文件处理工具
"""

import os
import json
import yaml
from typing import Any, Dict, Optional


def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    """读取文件内容"""
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        raise IOError(f"无法读取文件 {file_path}: {str(e)}")


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
    """写入文件内容"""
    
    try:
        ensure_directory(os.path.dirname(file_path))
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"无法写入文件 {file_path}: {str(e)}")


def read_json(file_path: str, encoding: str = 'utf-8') -> Any:
    """读取JSON文件"""
    
    content = read_file(file_path, encoding)
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"无效的JSON格式 {file_path}: {str(e)}")


def write_json(file_path: str, data: Any, indent: int = 2, 
               encoding: str = 'utf-8') -> None:
    """写入JSON文件"""
    
    try:
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        write_file(file_path, content, encoding)
    except Exception as e:
        raise IOError(f"无法写入JSON文件 {file_path}: {str(e)}")


def read_yaml(file_path: str, encoding: str = 'utf-8') -> Any:
    """读取YAML文件"""
    
    content = read_file(file_path, encoding)
    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise ValueError(f"无效的YAML格式 {file_path}: {str(e)}")


def write_yaml(file_path: str, data: Any, encoding: str = 'utf-8') -> None:
    """写入YAML文件"""
    
    try:
        content = yaml.dump(data, allow_unicode=True, default_flow_style=False)
        write_file(file_path, content, encoding)
    except Exception as e:
        raise IOError(f"无法写入YAML文件 {file_path}: {str(e)}")


def ensure_directory(directory_path: str) -> None:
    """确保目录存在"""
    
    if directory_path and not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)


def get_file_extension(file_path: str) -> str:
    """获取文件扩展名"""
    
    _, ext = os.path.splitext(file_path)
    return ext.lower().lstrip('.')


def is_file_readable(file_path: str) -> bool:
    """检查文件是否可读"""
    
    return os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.R_OK)


def is_file_writable(file_path: str) -> bool:
    """检查文件是否可写"""
    
    # 如果文件存在，检查是否可写
    if os.path.exists(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.W_OK)
    
    # 如果文件不存在，检查目录是否可写
    directory = os.path.dirname(file_path) or '.'
    return os.path.isdir(directory) and os.access(directory, os.W_OK)


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    return os.path.getsize(file_path)


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """列出目录中的文件"""
    
    if not os.path.exists(directory):
        return []
    
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            if extension is None or get_file_extension(item_path) == extension:
                files.append(item_path)
    
    return files


def create_temp_file(content: str, extension: str = 'txt') -> str:
    """创建临时文件"""
    
    import tempfile
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{extension}', 
                                     delete=False, encoding='utf-8') as f:
        f.write(content)
        temp_path = f.name
    
    return temp_path