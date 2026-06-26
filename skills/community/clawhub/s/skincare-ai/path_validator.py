#!/usr/bin/env python3
"""
路径安全验证器 - AISkinX安全修复组件 (修复版)
确保所有文件访问限制在允许的目录内，解决ClawHub警告问题
修复：1) base_dir不使用parent.parent 2) 移除create_test_file 3) 不动态修改allowed_dirs
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Union
import logging

logger = logging.getLogger(__name__)


class PathValidator:
    """路径安全验证器 - 核心安全组件 (修复版)"""
    
    def __init__(self, base_dir: Union[str, Path], 
                 allowed_dirs: Optional[List[Union[str, Path]]] = None):
        """
        初始化路径验证器
        
        Args:
            base_dir: 基础目录（必须是技能根目录，由调用者明确指定）
            allowed_dirs: 允许访问的目录列表（从config.yaml读取，不动态修改）
        """
        # 设置基础目录（必须由调用者明确指定）
        self.base_dir = Path(base_dir).resolve()
        
        if not self.base_dir.exists():
            raise ValueError(f"基础目录不存在: {base_dir}")
        
        # 初始化允许目录列表（不动态修改）
        self.allowed_dirs = []
        
        # 添加基础目录
        self.allowed_dirs.append(self.base_dir)
        
        # 添加config.yaml中配置的允许目录
        if allowed_dirs:
            for directory in allowed_dirs:
                dir_path = Path(directory)
                # 如果是相对路径，转换为基于base_dir的绝对路径
                if not dir_path.is_absolute():
                    dir_path = self.base_dir / dir_path
                
                dir_path = dir_path.resolve()
                
                # 安全检查：只允许base_dir下的目录
                try:
                    dir_path.relative_to(self.base_dir)
                    if dir_path.exists():
                        self.allowed_dirs.append(dir_path)
                        logger.debug(f"添加允许目录: {dir_path}")
                    else:
                        logger.warning(f"允许目录不存在，已跳过: {directory}")
                except ValueError:
                    logger.warning(f"目录不在基础目录下，已跳过: {directory}")
        
        # 记录初始化信息
        logger.info(f"路径验证器初始化完成，基础目录: {self.base_dir}")
        logger.info(f"允许访问的目录: {[str(d) for d in self.allowed_dirs]}")
    
    def is_safe_path(self, file_path: Union[str, Path]) -> bool:
        """
        检查文件路径是否安全（在允许目录内）
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否安全
        """
        try:
            # 转换为Path对象并解析
            path = Path(file_path).resolve()
            
            # 检查路径遍历攻击
            path_str = str(path)
            if '..' in path_str or '~' in path_str:
                logger.warning(f"路径包含遍历字符: {file_path}")
                return False
            
            # 检查是否在允许目录内
            for allowed_dir in self.allowed_dirs:
                try:
                    path.relative_to(allowed_dir)
                    logger.debug(f"路径安全: {file_path} (在 {allowed_dir} 内)")
                    return True
                except ValueError:
                    continue
            
            logger.warning(f"路径不在允许目录内: {file_path}")
            return False
            
        except Exception as e:
            logger.error(f"检查路径安全时出错: {file_path}, 错误: {e}")
            return False
    
    def get_safe_path(self, file_path: Union[str, Path]) -> Optional[Path]:
        """
        获取安全路径（如果在允许目录内）
        
        Args:
            file_path: 文件路径
            
        Returns:
            Optional[Path]: 安全路径，如果不安全则返回None
        """
        if self.is_safe_path(file_path):
            return Path(file_path).resolve()
        return None
    
    def validate_image_path(self, image_path: Union[str, Path]) -> tuple[bool, str]:
        """
        验证图像文件路径
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            tuple[bool, str]: (是否有效, 消息)
        """
        # 检查路径安全
        if not self.is_safe_path(image_path):
            return False, f"文件路径不在允许的目录内: {image_path}"
        
        # 检查文件是否存在
        path = Path(image_path)
        if not path.exists():
            return False, f"文件不存在: {image_path}"
        
        # 检查是否为文件
        if not path.is_file():
            return False, f"不是文件: {image_path}"
        
        # 检查文件大小（最大50MB）
        max_size = 50 * 1024 * 1024  # 50MB
        if path.stat().st_size > max_size:
            return False, f"文件太大（最大50MB）: {image_path}"
        
        # 检查文件扩展名
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        if path.suffix.lower() not in allowed_extensions:
            return False, f"不支持的文件类型: {path.suffix}，支持的类型: {', '.join(allowed_extensions)}"
        
        return True, "文件路径有效"
    
    def validate_model_path(self, model_path: Union[str, Path]) -> tuple[bool, str]:
        """
        验证模型文件路径
        
        Args:
            model_path: 模型文件路径
            
        Returns:
            tuple[bool, str]: (是否有效, 消息)
        """
        # 检查路径安全
        if not self.is_safe_path(model_path):
            return False, f"模型路径不在允许的目录内: {model_path}"
        
        # 检查文件是否存在
        path = Path(model_path)
        if not path.exists():
            return False, f"模型文件不存在: {model_path}"
        
        # 检查是否为文件
        if not path.is_file():
            return False, f"不是文件: {model_path}"
        
        # 检查文件扩展名
        allowed_extensions = {'.pth', '.pt', '.h5', '.keras', '.joblib', '.pkl'}
        if path.suffix.lower() not in allowed_extensions:
            return False, f"不支持的模型文件类型: {path.suffix}"
        
        return True, "模型路径有效"
    
    def get_allowed_dirs(self) -> List[Path]:
        """
        获取允许目录列表（只读）
        
        Returns:
            List[Path]: 允许目录列表
        """
        return self.allowed_dirs.copy()  # 返回副本，防止外部修改
    
    def is_within_base_dir(self, path: Union[str, Path]) -> bool:
        """
        检查路径是否在基础目录内
        
        Args:
            path: 路径
            
        Returns:
            bool: 是否在基础目录内
        """
        try:
            Path(path).resolve().relative_to(self.base_dir)
            return True
        except ValueError:
            return False
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"PathValidator(base_dir={self.base_dir}, allowed_dirs={len(self.allowed_dirs)})"


# 工具函数
def create_path_validator_from_config(config: dict, skill_root: Union[str, Path]) -> PathValidator:
    """
    从配置创建路径验证器
    
    Args:
        config: 配置字典（包含security.path_restriction）
        skill_root: 技能根目录
        
    Returns:
        PathValidator: 路径验证器实例
    """
    skill_root_path = Path(skill_root).resolve()
    
    # 从配置获取允许目录
    allowed_dirs = []
    if 'security' in config and 'path_restriction' in config['security']:
        path_config = config['security']['path_restriction']
        if 'allowed_dirs' in path_config:
            allowed_dirs = path_config['allowed_dirs']
    
    # 创建验证器
    return PathValidator(base_dir=skill_root_path, allowed_dirs=allowed_dirs)


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
    
    # 创建验证器
    validator = create_path_validator_from_config(test_config, '.')
    
    # 测试安全路径
    test_paths = [
        './data/test.jpg',
        '../outside.txt',
        '/etc/passwd',
        'C:\\Windows\\system32'
    ]
    
    print("🔍 路径安全测试:")
    for path in test_paths:
        is_safe = validator.is_safe_path(path)
        status = "✅ 安全" if is_safe else "❌ 不安全"
        print(f"  {status}: {path}")
    
    print(f"\n📁 允许目录: {[str(d) for d in validator.get_allowed_dirs()]}")
# 全局验证器实例（单例模式）
_global_validator = None

def get_global_validator(config: dict = None, skill_root: Union[str, Path] = None) -> PathValidator:
    """
    获取全局路径验证器实例（单例模式）
    
    Args:
        config: 配置字典（可选）
        skill_root: 技能根目录（可选）
        
    Returns:
        PathValidator: 全局验证器实例
    """
    global _global_validator
    
    if _global_validator is None:
        if config is None or skill_root is None:
            raise ValueError("首次调用需要提供config和skill_root参数")
        
        _global_validator = create_path_validator_from_config(config, skill_root)
        logger.info("全局路径验证器已初始化")
    
    return _global_validator


def set_global_validator(validator: PathValidator) -> None:
    """
    设置全局路径验证器（主要用于测试）
    
    Args:
        validator: 路径验证器实例
    """
    global _global_validator
    _global_validator = validator
    logger.info("全局路径验证器已设置")


def clear_global_validator() -> None:
    """清除全局路径验证器（主要用于测试）"""
    global _global_validator
    _global_validator = None
    logger.info("全局路径验证器已清除")
