# -*- coding: utf-8 -*-
"""
文件操作工具
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Optional


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，不存在则创建
    
    @param path: 目录路径
    @return: Path对象
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
    
    
def get_file_hash(file_path: str, algorithm: str = 'sha256', chunk_size: int = 8192) -> str:
    """
    计算文件的哈希值
    
    @param file_path: 文件路径
    @param algorithm: 哈希算法 (md5/sha1/sha256/sha512)
    @param chunk_size: 每次读取的块大小
    @return: 哈希值（十六进制）
    """
    hash_func = getattr(hashlib, algorithm)()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hash_func.update(chunk)
            
    return hash_func.hexdigest()
    
    
def get_file_size(file_path: str) -> int:
    """
    获取文件大小（字节）
    
    @param file_path: 文件路径
    @return: 文件大小
    """
    return os.path.getsize(file_path)
    
    
def format_file_size(size: int) -> str:
    """
    格式化文件大小
    
    @param size: 字节大小
    @return: 格式化后的字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"
    
    
def copy_file(src: str, dst: str, overwrite: bool = False) -> bool:
    """
    复制文件
    
    @param src: 源文件路径
    @param dst: 目标文件路径
    @param overwrite: 是否覆盖已存在的文件
    @return: 是否成功
    """
    dst_path = Path(dst)
    
    if dst_path.exists() and not overwrite:
        return False
        
    # 确保目标目录存在
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(src, dst)
    return True
    
    
def move_file(src: str, dst: str, overwrite: bool = False) -> bool:
    """
    移动文件
    
    @param src: 源文件路径
    @param dst: 目标文件路径
    @param overwrite: 是否覆盖已存在的文件
    @return: 是否成功
    """
    dst_path = Path(dst)
    
    if dst_path.exists() and not overwrite:
        return False
        
    # 确保目标目录存在
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.move(src, dst)
    return True
    
    
def delete_file(file_path: str) -> bool:
    """
    删除文件
    
    @param file_path: 文件路径
    @return: 是否成功
    """
    try:
        Path(file_path).unlink()
        return True
    except FileNotFoundError:
        return False
        
    
def cleanup_temp_files(temp_dir: str, extensions: List[str] = None):
    """
    清理临时文件
    
    @param temp_dir: 临时目录路径
    @param extensions: 要清理的文件扩展名（如 ['.tmp', '.verify']）
    """
    if extensions is None:
        extensions = ['.tmp', '.verify.tmp', '.temp']
        
    temp_path = Path(temp_dir)
    
    if not temp_path.exists():
        return
        
    for ext in extensions:
        for f in temp_path.glob(f'*{ext}'):
            try:
                f.unlink()
            except Exception:
                pass
                
                
def list_files(directory: str, extensions: List[str] = None, 
               recursive: bool = False) -> List[str]:
    """
    列出目录中的文件
    
    @param directory: 目录路径
    @param extensions: 过滤的文件扩展名
    @param recursive: 是否递归子目录
    @return: 文件路径列表
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return []
        
    files = []
    
    if recursive:
        for f in dir_path.rglob('*'):
            if f.is_file():
                if extensions is None or f.suffix.lower() in extensions:
                    files.append(str(f))
    else:
        for f in dir_path.iterdir():
            if f.is_file():
                if extensions is None or f.suffix.lower() in extensions:
                    files.append(str(f))
                    
    return files


def scan_directory(dir_path: str, extensions: List[str] = None, 
                   recursive: bool = False) -> List[str]:
    """
    扫描目录获取支持的文件列表
    
    @param dir_path: 目录路径
    @param extensions: 文件扩展名列表，如 ['docx', 'pdf', 'txt']
    @param recursive: 是否递归子目录
    @return: 文件路径列表
    """
    if extensions is None:
        extensions = ['.docx', '.doc', '.pdf', '.txt', '.md']
    
    # 统一添加点前缀
    ext_set = set(ext if ext.startswith('.') else f'.{ext}' for ext in extensions)
    
    files = []
    dir_path = Path(dir_path)
    
    if not dir_path.exists() or not dir_path.is_dir():
        return files
    
    # 扫描文件
    try:
        if recursive:
            for ext in ext_set:
                for f in dir_path.rglob(f'*{ext}'):
                    if f.is_file():
                        files.append(str(f))
        else:
            for ext in ext_set:
                for f in dir_path.glob(f'*{ext}'):
                    if f.is_file():
                        files.append(str(f))
    except PermissionError:
        print(f"[!] 无权限访问: {dir_path}")
    except Exception as e:
        print(f"[!] 扫描目录出错: {e}")
    
    # 去重并排序
    return sorted(list(set(files)))
