# -*- coding: utf-8 -*-
"""
🛤️ Path Helper - 路径辅助工具
提供跨平台路径处理、文件查找、目录操作等实用函数
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Union


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).parent.absolute()


def ensure_dir(path: Union[str, Path]) -> Path:
    """确保目录存在，不存在则创建"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(filename: str, replacement: str = "_") -> str:
    """将文件名转换为安全的格式（去除非法字符）"""
    import re
    # Windows 非法字符: < > : " / \ | ? *
    illegal_chars = r'[<>:"/\\|?*]'
    safe = re.sub(illegal_chars, replacement, filename)
    # 去除首尾空格和点
    safe = safe.strip(" .")
    # 限制长度
    if len(safe) > 200:
        safe = safe[:200]
    return safe or "untitled"


def find_files(
    pattern: str,
    root: Optional[Union[str, Path]] = None,
    recursive: bool = True
) -> List[Path]:
    """
    查找匹配的文件

    Args:
        pattern: glob 模式，如 "*.md"、"**/*.txt"
        root: 搜索根目录，默认为项目根目录
        recursive: 是否递归搜索

    Returns:
        匹配的文件路径列表
    """
    root = Path(root) if root else get_project_root()
    if recursive and not pattern.startswith("**"):
        pattern = f"**/{pattern}"
    return list(root.glob(pattern))


def get_relative_path(path: Union[str, Path], base: Optional[Union[str, Path]] = None) -> str:
    """获取相对于 base 的相对路径"""
    path = Path(path).absolute()
    base = Path(base) if base else get_project_root()
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def get_file_info(path: Union[str, Path]) -> dict:
    """获取文件信息"""
    path = Path(path)
    if not path.exists():
        return {"exists": False}

    stat = path.stat()
    return {
        "exists": True,
        "path": str(path.absolute()),
        "name": path.name,
        "stem": path.stem,
        "suffix": path.suffix,
        "size": stat.st_size,
        "size_human": _human_readable_size(stat.st_size),
        "modified": stat.st_mtime,
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }


def _human_readable_size(size_bytes: int) -> str:
    """将字节大小转换为人类可读格式"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def get_data_dir(subdir: Optional[str] = None) -> Path:
    """
    获取数据存储目录
    优先使用环境变量 ZOT_DATA_DIR，否则使用项目目录下的 data/
    """
    data_dir = os.environ.get("ZOT_DATA_DIR")
    if data_dir:
        path = Path(data_dir)
    else:
        path = get_project_root() / "data"

    if subdir:
        path = path / subdir

    return ensure_dir(path)


def get_temp_dir() -> Path:
    """获取临时目录"""
    import tempfile
    temp = Path(tempfile.gettempdir()) / "zero-one-two-three"
    return ensure_dir(temp)


if __name__ == "__main__":
    print("🛤️ Path Helper 测试")
    print(f"项目根目录: {get_project_root()}")
    print(f"数据目录: {get_data_dir()}")
    print(f"临时目录: {get_temp_dir()}")

    # 查找所有 Python 文件
    py_files = find_files("*.py", recursive=False)
    print(f"\n📁 项目根目录下的 Python 文件 ({len(py_files)} 个):")
    for f in py_files[:10]:
        info = get_file_info(f)
        print(f"  - {f.name} ({info['size_human']})")
