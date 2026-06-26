"""
文件工具模块
"""

import os
import shutil
import tempfile
import hashlib
from typing import Optional, List, Tuple, Dict, Any
from pathlib import Path
import mimetypes
from datetime import datetime
from .logger import get_logger
from .error_handler import FileError, safe_execute


logger = get_logger("file_utils")


def validate_file(file_path: str, 
                 required_extensions: Optional[List[str]] = None,
                 max_size_mb: Optional[float] = None,
                 check_exists: bool = True) -> Tuple[bool, str]:
    """
    验证文件
    
    Args:
        file_path: 文件路径
        required_extensions: 要求的文件扩展名
        max_size_mb: 最大文件大小（MB）
        check_exists: 是否检查文件存在
        
    Returns:
        (是否有效, 错误消息)
    """
    # 检查文件是否存在
    if check_exists and not os.path.exists(file_path):
        return False, f"文件不存在: {file_path}"
    
    # 检查是否是文件
    if check_exists and not os.path.isfile(file_path):
        return False, f"路径不是文件: {file_path}"
    
    # 检查文件扩展名
    if required_extensions:
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in required_extensions:
            return False, f"文件扩展名不支持: {file_ext}，支持: {required_extensions}"
    
    # 检查文件大小
    if max_size_mb is not None:
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > max_size_mb:
                return False, f"文件太大: {file_size_mb:.2f}MB > {max_size_mb}MB"
        except OSError as e:
            return False, f"无法获取文件大小: {e}"
    
    return True, "文件验证通过"


def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    获取文件信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件信息字典
    """
    try:
        stat_info = os.stat(file_path)
        
        # 获取文件扩展名和MIME类型
        file_ext = os.path.splitext(file_path)[1].lower()
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # 计算文件哈希（用于唯一标识）
        file_hash = calculate_file_hash(file_path)
        
        return {
            "path": file_path,
            "name": os.path.basename(file_path),
            "size_bytes": stat_info.st_size,
            "size_mb": stat_info.st_size / (1024 * 1024),
            "created": datetime.fromtimestamp(stat_info.st_ctime),
            "modified": datetime.fromtimestamp(stat_info.st_mtime),
            "extension": file_ext,
            "mime_type": mime_type or "application/octet-stream",
            "hash": file_hash,
            "is_readable": os.access(file_path, os.R_OK),
            "is_writable": os.access(file_path, os.W_OK)
        }
        
    except Exception as e:
        raise FileError(f"无法获取文件信息: {file_path}", original_error=e)


def calculate_file_hash(file_path: str, algorithm: str = "md5") -> str:
    """
    计算文件哈希值
    
    Args:
        file_path: 文件路径
        algorithm: 哈希算法
        
    Returns:
        文件哈希值
    """
    hash_func = getattr(hashlib, algorithm, hashlib.md5)()
    
    try:
        with open(file_path, 'rb') as f:
            # 分块读取大文件
            for chunk in iter(lambda: f.read(8192), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
        
    except Exception as e:
        raise FileError(f"无法计算文件哈希: {file_path}", original_error=e)


def create_temp_file(content: Optional[bytes] = None, 
                    suffix: str = ".tmp",
                    prefix: str = "ppt_maker_",
                    directory: Optional[str] = None) -> str:
    """
    创建临时文件
    
    Args:
        content: 文件内容（字节）
        suffix: 文件后缀
        prefix: 文件前缀
        directory: 临时目录
        
    Returns:
        临时文件路径
    """
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(
            mode='wb' if content else 'w',
            suffix=suffix,
            prefix=prefix,
            dir=directory,
            delete=False
        ) as temp_file:
            temp_path = temp_file.name
            
            # 写入内容
            if content is not None:
                temp_file.write(content)
            
            logger.debug(f"创建临时文件: {temp_path}")
            return temp_path
            
    except Exception as e:
        raise FileError("无法创建临时文件", original_error=e)


def create_temp_directory(prefix: str = "ppt_maker_",
                         suffix: str = "",
                         directory: Optional[str] = None) -> str:
    """
    创建临时目录
    
    Args:
        prefix: 目录前缀
        suffix: 目录后缀
        directory: 父目录
        
    Returns:
        临时目录路径
    """
    try:
        temp_dir = tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=directory)
        logger.debug(f"创建临时目录: {temp_dir}")
        return temp_dir
        
    except Exception as e:
        raise FileError("无法创建临时目录", original_error=e)


def cleanup_temp_files(file_paths: List[str]) -> None:
    """
    清理临时文件
    
    Args:
        file_paths: 文件路径列表
    """
    for file_path in file_paths:
        safe_execute(os.remove, file_path, default_return=None)
        logger.debug(f"清理临时文件: {file_path}")


def cleanup_temp_directory(dir_path: str) -> None:
    """
    清理临时目录
    
    Args:
        dir_path: 目录路径
    """
    safe_execute(shutil.rmtree, dir_path, default_return=None)
    logger.debug(f"清理临时目录: {dir_path}")


def ensure_directory(directory_path: str) -> str:
    """
    确保目录存在
    
    Args:
        directory_path: 目录路径
        
    Returns:
        确保存在的目录路径
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.debug(f"确保目录存在: {directory_path}")
        return directory_path
        
    except Exception as e:
        raise FileError(f"无法创建目录: {directory_path}", original_error=e)


def copy_file(source_path: str, 
             target_path: str,
             overwrite: bool = False) -> str:
    """
    复制文件
    
    Args:
        source_path: 源文件路径
        target_path: 目标文件路径
        overwrite: 是否覆盖已存在的文件
        
    Returns:
        目标文件路径
    """
    # 检查源文件
    is_valid, error_msg = validate_file(source_path)
    if not is_valid:
        raise FileError(f"源文件无效: {error_msg}")
    
    # 检查目标文件是否已存在
    if os.path.exists(target_path) and not overwrite:
        raise FileError(f"目标文件已存在: {target_path}")
    
    try:
        # 确保目标目录存在
        target_dir = os.path.dirname(target_path)
        if target_dir:
            ensure_directory(target_dir)
        
        # 复制文件
        shutil.copy2(source_path, target_path)
        logger.info(f"复制文件: {source_path} -> {target_path}")
        
        return target_path
        
    except Exception as e:
        raise FileError(f"无法复制文件: {source_path} -> {target_path}", original_error=e)


def move_file(source_path: str, 
             target_path: str,
             overwrite: bool = False) -> str:
    """
    移动文件
    
    Args:
        source_path: 源文件路径
        target_path: 目标文件路径
        overwrite: 是否覆盖已存在的文件
        
    Returns:
        目标文件路径
    """
    # 检查源文件
    is_valid, error_msg = validate_file(source_path)
    if not is_valid:
        raise FileError(f"源文件无效: {error_msg}")
    
    # 检查目标文件是否已存在
    if os.path.exists(target_path) and not overwrite:
        raise FileError(f"目标文件已存在: {target_path}")
    
    try:
        # 确保目标目录存在
        target_dir = os.path.dirname(target_path)
        if target_dir:
            ensure_directory(target_dir)
        
        # 移动文件
        shutil.move(source_path, target_path)
        logger.info(f"移动文件: {source_path} -> {target_path}")
        
        return target_path
        
    except Exception as e:
        raise FileError(f"无法移动文件: {source_path} -> {target_path}", original_error=e)


def get_unique_filename(base_path: str, 
                       max_attempts: int = 100) -> str:
    """
    获取唯一的文件名（避免冲突）
    
    Args:
        base_path: 基础文件路径
        max_attempts: 最大尝试次数
        
    Returns:
        唯一的文件路径
    """
    if not os.path.exists(base_path):
        return base_path
    
    # 分离文件名和扩展名
    directory = os.path.dirname(base_path)
    filename, extension = os.path.splitext(os.path.basename(base_path))
    
    for i in range(1, max_attempts + 1):
        # 尝试添加序号
        new_filename = f"{filename}_{i}{extension}"
        new_path = os.path.join(directory, new_filename)
        
        if not os.path.exists(new_path):
            return new_path
    
    # 如果所有尝试都失败，使用时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{filename}_{timestamp}{extension}"
    return os.path.join(directory, new_filename)


def get_file_size_readable(file_path: str) -> str:
    """
    获取可读的文件大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        可读的大小字符串
    """
    try:
        size_bytes = os.path.getsize(file_path)
        
        # 转换为合适的单位
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} TB"
        
    except Exception as e:
        return "未知大小"


# 测试代码
if __name__ == "__main__":
    print("🔧 文件工具模块测试")
    print("=" * 50)
    
    # 测试临时文件
    temp_file = create_temp_file(content=b"test content", suffix=".txt")
    print(f"✅ 创建临时文件: {temp_file}")
    
    # 测试文件信息
    file_info = get_file_info(temp_file)
    print(f"✅ 文件信息: {file_info['name']}, {file_info['size_bytes']}字节")
    
    # 测试文件哈希
    file_hash = calculate_file_hash(temp_file)
    print(f"✅ 文件哈希: {file_hash}")
    
    # 测试文件验证
    is_valid, message = validate_file(temp_file, required_extensions=['.txt', '.md'])
    print(f"✅ 文件验证: {is_valid}, {message}")
    
    # 测试唯一文件名
    unique_name = get_unique_filename(temp_file)
    print(f"✅ 唯一文件名: {unique_name}")
    
    # 测试可读文件大小
    readable_size = get_file_size_readable(temp_file)
    print(f"✅ 可读文件大小: {readable_size}")
    
    # 测试临时目录
    temp_dir = create_temp_directory()
    print(f"✅ 创建临时目录: {temp_dir}")
    
    # 清理测试文件
    cleanup_temp_files([temp_file])
    cleanup_temp_directory(temp_dir)
    
    print("\n✅ 文件工具模块测试完成")