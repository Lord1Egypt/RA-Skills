"""
安全工具函数
"""

import re
import secrets
from typing import Optional


def validate_user_id(user_id: Optional[str]) -> bool:
    """
    验证 user_id 格式
    - 不允许为空
    - 3-64字符
    - 只允许字母、数字、下划线、横线
    """
    if not user_id or len(user_id) < 3 or len(user_id) > 64:
        return False
    return re.match(r'^[a-zA-Z0-9_-]+$', user_id) is not None


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    验证 API Key 格式
    - 不允许为空
    - 8-128字符
    - 只允许字母、数字、下划线、横线
    """
    if not api_key or len(api_key) < 8 or len(api_key) > 128:
        return False
    return re.match(r'^[a-zA-Z0-9_-]+$', api_key) is not None


def validate_tx_hash(tx_hash: Optional[str]) -> bool:
    """
    验证交易哈希格式
    - 必须以 0x 开头
    - 总共66字符（0x + 64位十六进制）
    """
    if not tx_hash or len(tx_hash) != 66:
        return False
    return bool(re.match(r'^0x[a-fA-F0-9]{64}$', tx_hash))


def validate_url(url: Optional[str]) -> bool:
    """
    验证 URL 格式
    - 必须以 http:// 或 https:// 开头
    """
    if not url:
        return False
    return url.startswith(("http://", "https://"))


def sanitize_user_id(user_id: str) -> str:
    """
    清理用户ID，移除危险字符
    """
    # 只保留允许的字符
    return re.sub(r'[^a-zA-Z0-9_-]', '', user_id)[:64]


def generate_api_key(prefix: str = "pg") -> str:
    """
    生成安全的 API Key
    """
    token = secrets.token_urlsafe(32)
    return f"{prefix}_{token}"


def generate_client_id() -> str:
    """
    生成客户端ID（用于免费试用）
    """
    return secrets.token_urlsafe(16)


def mask_sensitive_string(s: str, visible_chars: int = 4) -> str:
    """
    隐藏敏感字符串的中间部分
    
    Example:
        mask_sensitive_string("abcdef123456") -> "abcd********3456"
    """
    if len(s) <= visible_chars * 2:
        return "*" * len(s)
    return s[:visible_chars] + "*" * (len(s) - visible_chars * 2) + s[-visible_chars:]


def check_password_strength(password: str) -> dict:
    """
    检查密码强度
    
    Returns:
        {
            "is_strong": bool,
            "score": int (0-4),
            "feedback": [str]
        }
    """
    score = 0
    feedback = []
    
    # 长度检查
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password must be at least 8 characters")
    
    if len(password) >= 12:
        score += 1
    
    # 复杂性检查
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    if has_lower and has_upper:
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters")
    
    if has_digit:
        score += 1
    else:
        feedback.append("Include at least one number")
    
    if has_special:
        score += 1
    else:
        feedback.append("Include at least one special character")
    
    return {
        "is_strong": score >= 3,
        "score": min(score, 4),
        "feedback": feedback
    }
