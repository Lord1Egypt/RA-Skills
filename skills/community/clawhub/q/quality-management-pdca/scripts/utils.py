#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供通用工具函数、配置管理、日志功能等
"""
import os
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), '../quality_management.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('quality-management')
def load_config() -> Dict[str, Any]:
    """
    加载配置文件
    Returns:
        配置字典
    """
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        raise
def save_config(config: Dict[str, Any]) -> bool:
    """
    保存配置文件
    Args:
        config: 配置字典
    Returns:
        是否保存成功
    """
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    try:
        config['meta']['last_updated'] = datetime.now().isoformat()
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"保存配置文件失败: {e}")
        return False
def generate_id(prefix: str = 'qm') -> str:
    """
    生成唯一ID
    Args:
        prefix: ID前缀
    Returns:
        唯一ID字符串
    """
    return f"{prefix}_{uuid.uuid4().hex[:16]}"
def get_current_time() -> str:
    """
    获取当前时间字符串（ISO格式）
    Returns:
        当前时间字符串
    """
    return datetime.now().isoformat()
def get_current_timestamp() -> int:
    """
    获取当前时间戳
    Returns:
        时间戳（秒）
    """
    return int(datetime.now().timestamp())
def ensure_dir(path: str) -> bool:
    """
    确保目录存在，不存在则创建
    Args:
        path: 目录路径
    Returns:
        是否成功
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"创建目录失败 {path}: {e}")
        return False
def load_json_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
    加载JSON文件
    Args:
        file_path: 文件路径
    Returns:
        JSON数据，失败返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON文件失败 {file_path}: {e}")
        return None
def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """
    保存JSON文件
    Args:
        data: 要保存的数据
        file_path: 文件路径
    Returns:
        是否保存成功
    """
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"保存JSON文件失败 {file_path}: {e}")
        return False
def read_text_file(file_path: str) -> Optional[str]:
    """
    读取文本文件
    Args:
        file_path: 文件路径
    Returns:
        文件内容，失败返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取文本文件失败 {file_path}: {e}")
        return None
def write_text_file(content: str, file_path: str) -> bool:
    """
    写入文本文件
    Args:
        content: 文本内容
        file_path: 文件路径
    Returns:
        是否写入成功
    """
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"写入文本文件失败 {file_path}: {e}")
        return False
def calculate_score(items: List[Dict[str, Any]], weights: Dict[str, float]) -> float:
    """
    计算加权得分
    Args:
        items: 评分项列表，每个项包含name和score字段
        weights: 权重字典，key为项名称，value为权重值（0-100）
    Returns:
        加权得分（0-100）
    """
    total_score = 0.0
    total_weight = 0.0
    for item in items:
        name = item.get('name')
        score = item.get('score', 0)
        if name in weights:
            weight = weights[name]
            total_score += score * weight
            total_weight += weight
    if total_weight == 0:
        return 0.0
    return round(total_score / total_weight, 2)
def validate_smart_target(target: str) -> Dict[str, Any]:
    """
    验证SMART目标
    Args:
        target: 目标描述
    Returns:
        验证结果，包含passed、issues、score字段
    """
    issues = []
    score = 100
    # Specific: 具体的
    if len(target) < 10 or any(keyword in target.lower() for keyword in ['尽量', '大概', '可能', '差不多']):
        issues.append("目标不够具体，避免模糊表述（尽量、大概、可能等）")
        score -= 20
    # Measurable: 可衡量的
    if not any(char.isdigit() for char in target) and not any(keyword in target.lower() for keyword in ['完成', '实现', '达到', '通过']):
        issues.append("目标缺乏可衡量的指标，建议添加量化标准")
        score -= 20
    # Achievable: 可实现的
    if any(keyword in target.lower() for keyword in ['完美', '100%', '全部', '所有']) and '阶段' not in target.lower():
        issues.append("目标可能过高，建议拆分为阶段性目标")
        score -= 20
    # Relevant: 相关的
    # 这里需要上下文，暂时简化
    # Time-bound: 有时限的
    if not any(keyword in target for keyword in ['日前', '之前', '截止', '年', '月', '日', '天内', '周内', '月内']):
        issues.append("目标没有明确的时间限制")
        score -= 20
    return {
        'passed': score >= 60,
        'score': max(0, score),
        'issues': issues
    }
def calculate_risk_level(probability: int, impact: int, detectability: int = 5) -> str:
    """
    计算风险等级
    Args:
        probability: 发生概率（1-10）
        impact: 影响程度（1-10）
        detectability: 可检测性（1-10，越低越容易检测）
    Returns:
        风险等级：low/medium/high/critical
    """
    rpn = probability * impact * detectability
    if rpn >= 200:
        return 'critical'
    elif rpn >= 100:
        return 'high'
    elif rpn >= 50:
        return 'medium'
    else:
        return 'low'
def send_notification(message: str, level: str = 'info', channels: Optional[List[str]] = None) -> bool:
    """
    发送通知
    Args:
        message: 通知内容
        level: 通知级别：info/warning/error/critical
        channels: 通知渠道列表
    Returns:
        是否发送成功
    """
    config = load_config()
    if channels is None:
        channels = config['notification']['notification_channels']
    level_enabled = config['notification']['notification_levels'].get(level, False)
    if not level_enabled:
        return True
    # 记录日志
    log_method = getattr(logger, level, logger.info)
    log_method(f"通知 [{level}]: {message}")
    # TODO: 实现实际的通知发送（飞书、微信等）
    for channel in channels:
        try:
            if channel == 'webchat':
                # WebChat渠道通知
                print(f"[{level.upper()}] {message}")
            # 其他渠道实现
        except Exception as e:
            logger.error(f"发送通知到渠道 {channel} 失败: {e}")
    return True
def format_duration(seconds: int) -> str:
    """
    格式化时长
    Args:
        seconds: 秒数
    Returns:
        格式化的时长字符串
    """
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    parts = []
    if days > 0:
        parts.append(f"{days}天")
    if hours > 0:
        parts.append(f"{hours}小时")
    if minutes > 0:
        parts.append(f"{minutes}分钟")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}秒")
    return ''.join(parts)
