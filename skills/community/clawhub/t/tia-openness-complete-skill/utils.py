"""辅助工具函数"""

import os
import winreg
import tempfile
from typing import Optional

def get_openness_dll_path(tia_version: str = "V18") -> tuple:
    """
    从注册表获取Openness DLL路径
    返回 (engineering_dll_path, hmi_dll_path)
    """
    try:
        key_path = f"SOFTWARE\\Siemens\\Automation\\Openness\\{tia_version}\\PublicAPI\\{tia_version}.0.0"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ) as key:
            eng_dll, _ = winreg.QueryValueEx(key, "Siemens.Engineering")
            hmi_dll, _ = winreg.QueryValueEx(key, "Siemens.Engineering.Hmi")
        return eng_dll, hmi_dll
    except Exception as e:
        raise RuntimeError(f"无法从注册表获取Openness DLL路径: {e}")

def ensure_directory(path: str) -> bool:
    """确保目录存在，如果不存在则创建"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False

def create_temp_file(content: str, suffix: str = ".tmp") -> str:
    """创建临时文件并写入内容"""
    fd, path = tempfile.mkstemp(suffix=suffix, text=True)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def parse_bool(value) -> bool:
    """将各种输入转换为布尔值"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    return bool(value)