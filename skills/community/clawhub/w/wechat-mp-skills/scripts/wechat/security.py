# -*- coding: utf-8 -*-
"""
安全工具模块
提供路径验证、URL验证、输入清理等安全功能
"""

import os
import re
import ipaddress
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, List


class SecurityValidator:
    """安全验证器"""
    
    # 允许的图片扩展名
    ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'}
    
    # 允许的 URL 协议
    ALLOWED_PROTOCOLS = {'http', 'https'}
    
    # 禁止访问的域名
    BLOCKED_DOMAINS = {
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '169.254.169.254',  # AWS 元数据服务
        'metadata.google.internal',  # GCP 元数据服务
    }
    
    # 禁止访问的路径前缀
    BLOCKED_PATH_PREFIXES = {
        '/etc',
        '/root',
        '/home',
        '/var/log',
        'C:\\Windows',
        'C:\\Users',
        '/proc',
        '/sys',
    }
    
    @staticmethod
    def validate_file_path(
        file_path: str,
        base_dir: Optional[str] = None,
        allowed_extensions: Optional[set] = None
    ) -> tuple[bool, str]:
        """
        验证文件路径是否安全
        
        Args:
            file_path: 要验证的文件路径
            base_dir: 基础目录，文件必须在此目录下
            allowed_extensions: 允许的文件扩展名
        
        Returns:
            (是否安全, 错误信息)
        """
        try:
            # 转换为绝对路径
            abs_path = os.path.abspath(file_path)
            
            # 检查路径是否存在
            if not os.path.exists(abs_path):
                return False, f"文件不存在: {os.path.basename(file_path)}"
            
            # 检查是否是文件
            if not os.path.isfile(abs_path):
                return False, "路径不是文件"
            
            # 检查路径遍历
            if '..' in file_path:
                return False, "路径包含非法字符"
            
            # 检查是否在禁止的路径前缀中
            for prefix in SecurityValidator.BLOCKED_PATH_PREFIXES:
                if abs_path.startswith(prefix):
                    return False, "访问被禁止的路径"
            
            # 如果指定了基础目录，确保文件在该目录下
            if base_dir:
                base_path = os.path.abspath(base_dir)
                if not abs_path.startswith(base_path):
                    return False, "文件不在允许的目录下"
            
            # 检查文件扩展名
            if allowed_extensions is None:
                allowed_extensions = SecurityValidator.ALLOWED_IMAGE_EXTENSIONS
            
            file_ext = os.path.splitext(abs_path)[1].lower()
            if file_ext not in allowed_extensions:
                return False, f"不支持的文件类型: {file_ext}"
            
            # 检查文件大小（限制为 10MB）
            file_size = os.path.getsize(abs_path)
            if file_size > 10 * 1024 * 1024:
                return False, "文件大小超过限制（10MB）"
            
            return True, "验证通过"
            
        except Exception as e:
            return False, f"路径验证失败: {str(e)}"
    
    @staticmethod
    def validate_url(url: str, allow_private: bool = False) -> tuple[bool, str]:
        """
        验证 URL 是否安全
        
        Args:
            url: 要验证的 URL
            allow_private: 是否允许访问内网地址
        
        Returns:
            (是否安全, 错误信息)
        """
        try:
            # 解析 URL
            parsed = urlparse(url)
            
            # 检查协议
            if parsed.scheme not in SecurityValidator.ALLOWED_PROTOCOLS:
                return False, f"不支持的协议: {parsed.scheme}"
            
            # 检查主机名
            hostname = parsed.hostname
            if not hostname:
                return False, "URL 缺少主机名"
            
            # 检查是否在黑名单中
            if hostname.lower() in SecurityValidator.BLOCKED_DOMAINS:
                return False, "访问被禁止的域名"
            
            # 检查是否是内网地址
            if not allow_private:
                try:
                    ip = ipaddress.ip_address(hostname)
                    if ip.is_private or ip.is_loopback or ip.is_link_local:
                        return False, "不允许访问内网地址"
                except ValueError:
                    # 不是 IP 地址，是域名，允许
                    pass
            
            # 检查端口（禁止非标准端口）
            if parsed.port and parsed.port not in [80, 443]:
                return False, f"不允许的端口: {parsed.port}"
            
            return True, "验证通过"
            
        except Exception as e:
            return False, f"URL 验证失败: {str(e)}"
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        清理文件名，移除危险字符
        
        Args:
            filename: 原始文件名
        
        Returns:
            清理后的安全文件名
        """
        # 只保留文件名，移除路径
        filename = os.path.basename(filename)
        
        # 移除危险字符
        dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\0']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # 移除控制字符
        filename = ''.join(char for char in filename if ord(char) >= 32)
        
        # 限制文件名长度
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:255-len(ext)] + ext
        
        return filename
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """
        清理 HTML 文本，防止 XSS
        
        Args:
            text: 原始文本
        
        Returns:
            清理后的安全文本
        """
        # 转义 HTML 特殊字符
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&#39;",
            ">": "&gt;",
            "<": "&lt;",
        }
        
        return "".join(html_escape_table.get(c, c) for c in text)
    
    @staticmethod
    def validate_image_content(file_path: str) -> tuple[bool, str]:
        """
        验证图片文件内容
        
        Args:
            file_path: 图片文件路径
        
        Returns:
            (是否有效, 错误信息)
        """
        try:
            # 读取文件头
            with open(file_path, 'rb') as f:
                header = f.read(16)
            
            # 检查文件魔数
            image_signatures = {
                b'\x89PNG\r\n\x1a\n': 'PNG',
                b'\xff\xd8\xff': 'JPEG',
                b'GIF87a': 'GIF',
                b'GIF89a': 'GIF',
                b'RIFF': 'WEBP',
                b'BM': 'BMP',
            }
            
            for signature, image_type in image_signatures.items():
                if header.startswith(signature):
                    return True, f"有效的 {image_type} 图片"
            
            return False, "不是有效的图片文件"
            
        except Exception as e:
            return False, f"图片验证失败: {str(e)}"


class InputSanitizer:
    """输入清理器"""
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """
        清理字符串输入
        
        Args:
            text: 原始字符串
            max_length: 最大长度
        
        Returns:
            清理后的字符串
        """
        # 移除控制字符
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        # 限制长度
        if len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    @staticmethod
    def sanitize_topic(topic: str) -> str:
        """
        清理主题输入
        
        Args:
            topic: 原始主题
        
        Returns:
            清理后的主题
        """
        # 只保留中文、英文、数字、空格和常见标点
        pattern = re.compile(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\-_，。！？、]')
        topic = pattern.sub('', topic)
        
        return topic.strip()[:100]  # 限制长度


# 便捷函数
def validate_file_path(file_path: str, base_dir: str = None) -> tuple[bool, str]:
    """验证文件路径"""
    return SecurityValidator.validate_file_path(file_path, base_dir)


def validate_url(url: str) -> tuple[bool, str]:
    """验证 URL"""
    return SecurityValidator.validate_url(url)


def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    return SecurityValidator.sanitize_filename(filename)


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """清理字符串"""
    return InputSanitizer.sanitize_string(text, max_length)
