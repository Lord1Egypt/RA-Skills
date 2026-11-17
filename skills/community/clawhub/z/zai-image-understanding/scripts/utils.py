"""
通用工具函数模块
"""

import os
import re
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse


def validate_image_url(url: str) -> tuple[bool, Optional[str]]:
    """
    验证图片 URL 格式
    
    Args:
        url: 待验证的 URL
        
    Returns:
        (is_valid, error_message)
    """
    if not url:
        return False, "URL 不能为空"
    
    if not url.startswith(('http://', 'https://')):
        return False, "URL 必须以 http:// 或 https:// 开头"
    
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return False, "URL 格式无效，缺少域名"
    except Exception as e:
        return False, f"URL 解析失败: {e}"
    
    return True, None


def validate_prompt(prompt: str) -> tuple[bool, Optional[str]]:
    """
    验证提示词
    
    Args:
        prompt: 待验证的提示词
        
    Returns:
        (is_valid, error_message)
    """
    if not prompt or not prompt.strip():
        return False, "提示词不能为空"
    
    if len(prompt.strip()) < 3:
        return False, "提示词过短，至少需要 3 个字符"
    
    if len(prompt) > 10000:
        return False, "提示词过长，最大 10000 字符"
    
    return True, None


def get_api_key() -> Optional[str]:
    """
    获取 API Key，优先级：环境变量 > .env 文件
    
    Returns:
        API Key 或 None
    """
    # 1. 环境变量
    api_key = os.environ.get("ZAI_API_KEY")
    if api_key:
        return api_key.strip()
    
    # 2. .env 文件
    env_paths = [
        Path.cwd() / ".env",
        Path.cwd() / "assets" / ".env",
        Path.home() / ".zai" / ".env",
    ]
    
    for env_path in env_paths:
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ZAI_API_KEY="):
                            return line.split("=", 1)[1].strip().strip('"\'')
            except Exception:
                continue
    
    return None


def load_env_file(env_path: Optional[str] = None) -> Dict[str, str]:
    """
    加载 .env 文件到环境变量
    
    Args:
        env_path: .env 文件路径，默认查找当前目录和项目根目录
        
    Returns:
        加载的环境变量字典
    """
    from pathlib import Path
    
    search_paths = []
    if env_path:
        search_paths.append(Path(env_path))
    else:
        search_paths.extend([
            Path.cwd() / ".env",
            Path.cwd() / "assets" / ".env.example",
            Path(__file__).parent.parent.parent / "assets" / ".env.example",
        ])
    
    env_vars = {}
    for path in search_paths:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key.strip()] = value.strip().strip('"\'')
            except Exception:
                continue
    
    return env_vars


def format_error_response(error: str, error_code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
    """格式化错误响应"""
    return {
        "success": False,
        "content": "",
        "raw_response": {},
        "usage": {},
        "error": error,
        "error_code": error_code
    }


def format_success_response(content: str, raw_response: Dict, usage: Dict) -> Dict[str, Any]:
    """格式化成功响应"""
    return {
        "success": True,
        "content": content,
        "raw_response": raw_response,
        "usage": usage,
        "error": None,
        "error_code": None
    }


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """从文本中提取 JSON 对象"""
    import json
    
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # 尝试提取代码块中的 JSON
    code_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(code_block_pattern, text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    # 尝试找第一个 { 到最后一个 }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
    
    return None


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除或替换非法字符
    illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
    sanitized = re.sub(illegal_chars, '_', filename)
    # 限制长度
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255 - len(ext)] + ext
    return sanitized


def get_file_extension_from_url(url: str) -> str:
    """从 URL 获取文件扩展名"""
    parsed = urlparse(url)
    path = parsed.path
    _, ext = os.path.splitext(path)
    return ext.lower() if ext else '.jpg'


# 延迟导入 Path
from pathlib import Path