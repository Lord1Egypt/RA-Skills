"""公共工具模块"""
import os
import sys


def get_script_dir() -> str:
    """获取脚本所在目录"""
    return os.path.dirname(os.path.abspath(__file__))


def ensure_dir(path: str) -> None:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def get_tesseract_path() -> str:
    """获取 Tesseract 路径"""
    # 检查环境变量
    tesseract_cmd = os.environ.get("TESSERACT_CMD")
    if tesseract_cmd and os.path.exists(tesseract_cmd):
        return tesseract_cmd
    
    # 常见路径
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return "tesseract"  # 假设在 PATH 中
