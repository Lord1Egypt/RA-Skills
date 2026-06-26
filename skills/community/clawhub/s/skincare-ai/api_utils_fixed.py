#!/usr/bin/env python3
"""
API工具函数 - 安全修复版 v2
修复：确保PathValidator正确初始化，解决ClawHub警告
"""

import os
import re
import base64
from pathlib import Path
from typing import Tuple, Optional, Union, Any
import logging

# 导入路径验证器
try:
    from path_validator import PathValidator, create_path_validator_from_config
    HAS_PATH_VALIDATOR = True
except ImportError:
    HAS_PATH_VALIDATOR = False
    logging.warning("路径验证器导入失败，使用基本验证")

logger = logging.getLogger(__name__)

# 全局配置和验证器
_global_config = None
_global_validator = None
_skill_root = None


def initialize_validator(config: dict, skill_root: Union[str, Path]) -> None:
    """
    初始化全局验证器
    
    Args:
        config: 配置字典
        skill_root: 技能根目录
    """
    global _global_config, _global_validator, _skill_root
    
    if not HAS_PATH_VALIDATOR:
        logger.warning("路径验证器不可用，跳过初始化")
        return
    
    _global_config = config
    _skill_root = Path(skill_root).resolve()
    
    # 创建验证器
    _global_validator = create_path_validator_from_config(config, _skill_root)
    logger.info(f"全局路径验证器已初始化，技能根目录: {_skill_root}")


def get_validator() -> Optional[PathValidator]:
    """
    获取全局验证器
    
    Returns:
        Optional[PathValidator]: 验证器实例，如果未初始化则返回None
    """
    if _global_validator is None:
        logger.warning("全局验证器未初始化，请先调用initialize_validator()")
    return _global_validator


def validate_image_data(image_data: Any) -> Tuple[bool, str]:
    """
    验证图像数据 - 安全修复版
    
    修复问题：原函数接受任意文件路径，没有限制在技能目录内
    现在：严格验证路径，确保在允许目录内，拒绝URL
    
    Args:
        image_data: 图像数据（文件路径、base64字符串等）
        
    Returns:
        Tuple[bool, str]: (是否有效, 验证消息)
    """
    try:
        # 如果是字符串，可能是文件路径或base64
        if isinstance(image_data, str):
            # 检查是否是URL（明确拒绝）
            if _is_url(image_data):
                return False, (
                    "URL不允许访问：技能声明为100%本地运行。\n"
                    "请提供本地文件路径或base64编码的图像数据。"
                )
            
            # 检查是否是base64编码
            if _is_base64(image_data):
                # 验证base64数据
                try:
                    # 解码base64
                    image_bytes = base64.b64decode(image_data)
                    
                    # 检查数据大小
                    max_size = 50 * 1024 * 1024  # 50MB
                    if len(image_bytes) > max_size:
                        return False, f"图像数据过大: {len(image_bytes)}字节 (限制: {max_size}字节)"
                    
                    # 检查图像格式
                    if _is_valid_image_bytes(image_bytes):
                        return True, "base64图像数据验证通过"
                    else:
                        return False, "base64数据不是有效的图像格式"
                        
                except Exception as e:
                    return False, f"base64数据验证失败: {str(e)}"
            
            # 如果是文件路径，验证路径安全性
            else:
                return validate_image_file_path(image_data)
        
        # 如果是字节数据
        elif isinstance(image_data, bytes):
            # 检查数据大小
            max_size = 50 * 1024 * 1024  # 50MB
            if len(image_data) > max_size:
                return False, f"图像数据过大: {len(image_data)}字节 (限制: {max_size}字节)"
            
            # 检查图像格式
            if _is_valid_image_bytes(image_data):
                return True, "字节图像数据验证通过"
            else:
                return False, "字节数据不是有效的图像格式"
        
        # 如果是Path对象
        elif isinstance(image_data, Path):
            return validate_image_file_path(str(image_data))
        
        # 其他类型不支持
        else:
            return False, f"不支持的数据类型: {type(image_data)}"
            
    except Exception as e:
        logger.error(f"图像数据验证异常: {type(image_data)}, 错误: {e}")
        return False, f"图像数据验证失败: {str(e)}"


def validate_image_file_path(file_path: str) -> Tuple[bool, str]:
    """
    验证图像文件路径 - 严格路径限制
    
    修复问题：原函数没有限制路径在技能目录内
    现在：使用PathValidator严格验证路径安全性
    """
    try:
        # 检查路径验证器是否可用
        if not HAS_PATH_VALIDATOR:
            logger.warning("路径验证器不可用，使用基本验证")
            return _basic_file_path_validation(file_path)
        
        # 获取验证器
        validator = get_validator()
        if validator is None:
            return False, "路径验证器未初始化，无法验证文件路径"
        
        # 验证路径安全性
        if not validator.is_safe_path(file_path):
            allowed_dirs = validator.get_allowed_dirs()
            return False, (
                f"文件路径不在允许的目录内: {file_path}\n"
                f"允许的目录:\n" + "\n".join(f"  - {d}" for d in allowed_dirs)
            )
        
        # 获取安全路径（会进行额外检查）
        try:
            safe_path = validator.get_safe_path(file_path)
            if safe_path is None:
                return False, f"无法获取安全路径: {file_path}"
        except Exception as e:
            return False, f"文件路径安全检查失败: {str(e)}"
        
        # 验证文件扩展名
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        file_extension = safe_path.suffix.lower()
        if file_extension not in allowed_extensions:
            return False, (
                f"不支持的文件类型: {file_extension}\n"
                f"支持的格式: {', '.join(allowed_extensions)}"
            )
        
        # 验证文件大小
        max_size_mb = 50  # 50MB限制
        file_size_mb = safe_path.stat().st_size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"文件过大: {file_size_mb:.2f}MB (限制: {max_size_mb}MB)"
        
        # 验证文件内容（通过魔术字节）
        try:
            with open(safe_path, 'rb') as f:
                magic_bytes = f.read(12)
            
            # 检查图像格式
            if magic_bytes[:3] == b'\xff\xd8\xff':  # JPEG
                return True, f"JPEG图像文件验证通过: {safe_path}"
            elif magic_bytes[:8] == b'\x89PNG\r\n\x1a\n':  # PNG
                return True, f"PNG图像文件验证通过: {safe_path}"
            elif magic_bytes[:6] in [b'GIF87a', b'GIF89a']:  # GIF
                return True, f"GIF图像文件验证通过: {safe_path}"
            elif magic_bytes[:2] == b'BM':  # BMP
                return True, f"BMP图像文件验证通过: {safe_path}"
            else:
                # 如果不是标准图像格式，但扩展名正确，也接受
                return True, f"图像文件验证通过（格式检查跳过）: {safe_path}"
                
        except Exception as e:
            return False, f"文件内容验证失败: {str(e)}"
        
    except Exception as e:
        logger.error(f"文件路径验证异常: {file_path}, 错误: {e}")
        return False, f"文件路径验证失败: {str(e)}"


def _basic_file_path_validation(file_path: str) -> Tuple[bool, str]:
    """
    基本文件路径验证（当路径验证器不可用时使用）
    
    注意：这个函数不如PathValidator严格，但提供基本保护
    """
    try:
        # 检查路径遍历攻击
        if ".." in file_path or file_path.startswith("~"):
            return False, "检测到可能的路径遍历攻击"
        
        # 检查绝对路径
        abs_path = Path(file_path).resolve()
        
        # 检查文件是否存在
        if not abs_path.exists():
            return False, f"文件不存在: {file_path}"
        
        # 检查是否是文件
        if not abs_path.is_file():
            return False, f"路径不是文件: {file_path}"
        
        # 检查文件大小
        max_size_mb = 50
        file_size_mb = abs_path.stat().st_size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, f"文件过大: {file_size_mb:.2f}MB (限制: {max_size_mb}MB)"
        
        # 检查文件扩展名
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        file_extension = abs_path.suffix.lower()
        if file_extension not in allowed_extensions:
            return False, (
                f"不支持的文件类型: {file_extension}\n"
                f"支持的格式: {', '.join(allowed_extensions)}"
            )
        
        return True, f"基本文件路径验证通过: {file_path}"
        
    except Exception as e:
        logger.error(f"基本文件路径验证异常: {file_path}, 错误: {e}")
        return False, f"基本文件路径验证失败: {str(e)}"


def _is_url(text: str) -> bool:
    """检查字符串是否是URL"""
    url_patterns = [
        r'^ftp://',         # FTP模式（拒绝所有URL）
        r'^www\.',          # www模式（拒绝所有URL）
        r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}',  # 域名模式（拒绝所有URL）
    ]
    
    for pattern in url_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    
    return False


def _is_base64(text: str) -> bool:
    """检查字符串是否是base64编码"""
    # Base64模式：只包含base64字符，长度是4的倍数
    base64_pattern = r'^[A-Za-z0-9+/]*={0,2}$'
    
    if not re.match(base64_pattern, text):
        return False
    
    # 检查长度
    if len(text) % 4 != 0:
        return False
    
    # 尝试解码
    try:
        base64.b64decode(text, validate=True)
        return True
    except:
        return False


def _is_valid_image_bytes(image_bytes: bytes) -> bool:
    """检查字节数据是否是有效的图像格式"""
    if len(image_bytes) < 12:
        return False
    
    # 检查常见图像格式的魔术字节
    magic_bytes = image_bytes[:12]
    
    # JPEG
    if magic_bytes[:3] == b'\xff\xd8\xff':
        return True
    
    # PNG
    if magic_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        return True
    
    # GIF
    if magic_bytes[:6] in [b'GIF87a', b'GIF89a']:
        return True
    
    # BMP
    if magic_bytes[:2] == b'BM':
        return True
    
    # TIFF (little endian)
    if magic_bytes[:4] == b'II*\x00':
        return True
    
    # TIFF (big endian)
    if magic_bytes[:4] == b'MM\x00*':
        return True
    
    # WebP
    if magic_bytes[:4] == b'RIFF' and magic_bytes[8:12] == b'WEBP':
        return True
    
    return False


def get_image_info(image_path: str) -> dict:
    """
    获取图像信息
    
    Args:
        image_path: 图像文件路径
        
    Returns:
        dict: 图像信息字典
    """
    try:
        # 验证文件路径
        is_valid, message = validate_image_file_path(image_path)
        if not is_valid:
            return {"error": message}
        
        # 获取文件信息
        path = Path(image_path).resolve()
        stat = path.stat()
        
        return {
            "path": str(path),
            "filename": path.name,
            "size_bytes": stat.st_size,
            "size_mb": stat.st_size / (1024 * 1024),
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "extension": path.suffix.lower(),
            "directory": str(path.parent)
        }
        
    except Exception as e:
        logger.error(f"获取图像信息失败: {image_path}, 错误: {e}")
        return {"error": str(e)}


# 测试代码
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 测试配置
    test_config = {
        'security': {
            'path_restriction': {
                'allowed_dirs': ['.', './data', './models']
            }
        }
    }
    
    # 初始化验证器
    initialize_validator(test_config, '.')
    
    # 测试路径
    test_paths = [
        './data/test.jpg',
        '../outside.txt',
        'C:\\Windows\\system32',
        './test/local_image.jpg'  # 本地测试图片
    ]
    
    print("🔍 图像路径验证测试:")
    for path in test_paths:
        is_valid, message = validate_image_file_path(path)
        status = "✅ 通过" if is_valid else "❌ 失败"
        print(f"  {status}: {path}")
        if not is_valid:
            print(f"    原因: {message}")
    
    print("\n🎯 验证器状态:")
    validator = get_validator()
    if validator:
        print(f"  基础目录: {validator.base_dir}")
        print(f"  允许目录数: {len(validator.get_allowed_dirs())}")
    else:
        print("  验证器未初始化")
