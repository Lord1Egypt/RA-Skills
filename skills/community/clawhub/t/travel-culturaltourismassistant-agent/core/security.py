# -*- coding: utf-8 -*-
"""
安全防护模块，包含输入验证、敏感数据过滤、提示词注入防御等功能
"""
import re
from typing import List, Dict, Any
from loguru import logger

# 危险模式列表，用于检测提示词注入
DANGEROUS_PATTERNS = [
    # 系统指令覆盖
    r"ignore.*previous.*instructions",
    r"disregard.*prior.*guidance",
    r"you.*are.*now.*",
    r"act.*as.*",
    r"pretend.*you.*are",
    r"your.*new.*role.*is",
    # 数据泄露诱导
    r"reveal.*your.*prompt",
    r"show.*your.*system.*prompt",
    r"disclose.*your.*instructions",
    r"output.*all.*your.*configuration",
    r"tell.*me.*your.*api.*key",
    r"leak.*the.*secret",
    # 代码执行诱导
    r"execute.*this.*code",
    r"run.*the.*following.*command",
    r"eval\(",
    r"exec\(",
    r"system\(",
    r"subprocess\.",
    r"os\.system",
    # 敏感信息请求
    r"get.*user.*data",
    r"list.*all.*users",
    r"access.*other.*user.*information",
    r"steal.*data",
    # 恶意内容生成
    r"generate.*malware",
    r"write.*a.*virus",
    r"create.*exploit",
    r"hack.*into",
    # 特殊字符绕过
    r"--",
    r";",
    r"`.*`",
    r"\$\(.*\)",
    r"\{\{.*\}\}",
]

# 编译正则表达式
DANGEROUS_REGEX = [re.compile(pattern, re.IGNORECASE) for pattern in DANGEROUS_PATTERNS]

# 敏感关键词，需要掩码处理
SENSITIVE_KEYWORDS = [
    "api_key",
    "secret_key",
    "password",
    "token",
    "credential",
    "private_key",
    "auth_token",
    "access_key",
]

def validate_user_input(input_str: str, max_length: int = 1000) -> bool:
    """
    验证用户输入是否合法
    :param input_str: 用户输入字符串
    :param max_length: 最大允许长度
    :return: 是否合法
    """
    if not input_str:
        return True
    
    # 长度检查
    if len(input_str) > max_length:
        logger.warning(f"用户输入过长：{len(input_str)}字符，超过最大限制{max_length}")
        return False
    
    # 危险模式检查
    for regex in DANGEROUS_REGEX:
        if regex.search(input_str):
            logger.warning(f"检测到危险输入模式：{input_str[:50]}...")
            return False
    
    # 特殊字符检查
    if re.search(r"[\x00-\x1F\x7F]", input_str):
        logger.warning("检测到不可见控制字符")
        return False
    
    return True

def sanitize_user_input(input_str: str) -> str:
    """
    清理用户输入，移除危险内容
    :param input_str: 原始输入
    :return: 清理后的输入
    """
    if not input_str:
        return ""
    
    # 移除危险模式匹配的内容
    for regex in DANGEROUS_REGEX:
        input_str = regex.sub("[REDACTED]", input_str)
    
    # 移除控制字符
    input_str = re.sub(r"[\x00-\x1F\x7F]", "", input_str)
    
    # 截断过长内容
    if len(input_str) > 2000:
        input_str = input_str[:2000] + "..."
    
    return input_str.strip()

def filter_sensitive_data(content: str) -> str:
    """
    过滤内容中的敏感数据
    :param content: 原始内容
    :return: 过滤后的内容
    """
    if not content:
        return ""
    
    # 掩码API Key模式（sk_开头的密钥）
    content = re.sub(r"\bsk_[A-Za-z0-9-]{32,}\b", lambda m: f"{m.group(0)[:4]}****{m.group(0)[-4:]}", content)
    
    # 掩码百度API Key
    content = re.sub(r"\b[A-Za-z0-9]{24,}\b", lambda m: f"{m.group(0)[:4]}****{m.group(0)[-4:]}" if len(m.group(0)) >= 16 else m.group(0), content)
    
    # 掩码敏感关键词对应的值
    for keyword in SENSITIVE_KEYWORDS:
        # 匹配 key: value 格式
        pattern = re.compile(rf"({keyword}[\"']?\s*[=:]\s*[\"']?)([A-Za-z0-9_\-./+]+)([\"']?)", re.IGNORECASE)
        content = pattern.sub(lambda m: f"{m.group(1)}{m.group(2)[:4]}****{m.group(2)[-4:]}{m.group(3)}", content)
    
    return content

def is_prompt_injection(input_str: str) -> bool:
    """
    检测是否为提示词注入攻击
    :param input_str: 用户输入
    :return: 是否为注入攻击
    """
    if not input_str:
        return False
    
    input_lower = input_str.lower()
    
    # 检查是否包含系统指令覆盖关键词
    injection_keywords = [
        "ignore previous",
        "disregard all",
        "forget everything",
        "you are now",
        "act as",
        "new instructions",
        "override system",
        "bypass security",
    ]
    
    for keyword in injection_keywords:
        if keyword in input_lower:
            logger.warning(f"检测到提示词注入关键词：{keyword}")
            return True
    
    # 正则匹配危险模式
    for regex in DANGEROUS_REGEX:
        if regex.search(input_str):
            logger.warning(f"检测到危险正则模式：{regex.pattern}")
            return True
    
    return False

def validate_city_name(city: str) -> bool:
    """
    验证城市名称是否合法
    :param city: 城市名称
    :return: 是否合法
    """
    if not city or len(city) > 50:
        return False
    
    # 城市名称只能包含中文、字母、空格、点、横线
    if not re.match(r"^[\u4e00-\u9fa5a-zA-Z\s\.-]+$", city):
        logger.warning(f"非法城市名称：{city}")
        return False
    
    return True

def validate_date(date_str: str) -> bool:
    """
    验证日期格式是否合法（YYYY-MM-DD）
    :param date_str: 日期字符串
    :return: 是否合法
    """
    if not date_str:
        return False
    
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        logger.warning(f"非法日期格式：{date_str}")
        return False
    
    try:
        from datetime import datetime
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        logger.warning(f"无效日期：{date_str}")
        return False

def validate_parameters(params: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    验证参数是否完整
    :param params: 参数字典
    :param required_fields: 必填字段列表
    :return: 是否完整
    """
    missing = [field for field in required_fields if field not in params or not params[field]]
    if missing:
        logger.warning(f"缺少必填参数：{', '.join(missing)}")
        return False
    return True
