"""
schemas.py - JSON Schema 定义
用于验证 StandardDataPacket 输入输出
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime

# StandardDataPacket JSON Schema (Draft 7)
STANDARD_DATA_PACKET_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "StandardDataPacket",
    "description": "紫微斗数技能通用数据包格式",
    "type": "object",
    "required": [
        "trace_id",
        "skill_name",
        "execution_time",
        "timestamp",
        "status",
        "confidence",
        "data"
    ],
    "properties": {
        "trace_id": {
            "type": "string",
            "format": "uuid",
            "description": "请求追踪ID"
        },
        "skill_name": {
            "type": "string",
            "enum": ["ziwei", "ziwei_verify", "ziwei_interpret"],
            "description": "技能名称"
        },
        "execution_time": {
            "type": "number",
            "minimum": 0,
            "description": "执行耗时（秒）"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 时间戳"
        },
        "status": {
            "type": "string",
            "enum": [
                "SUCCESS",
                "INVALID_INPUT",
                "LOW_CONFIDENCE",
                "NEED_VERIFICATION",
                "CALIBRATION_DONE",
                "CALIBRATION_FAILED"
            ],
            "description": "执行状态"
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "置信度（0-1）"
        },
        "data": {
            "type": "object",
            "description": "具体数据内容"
        },
        "errors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "错误信息列表"
        },
        "warnings": {
            "type": "array",
            "items": {"type": "string"},
            "description": "警告信息列表"
        },
        "verification_points": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["field", "description", "impact", "suggestions"],
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "字段名（如'命宫主星'）"
                    },
                    "description": {
                        "type": "string",
                        "description": "问题描述"
                    },
                    "impact": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                        "description": "影响级别"
                    },
                    "suggestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "建议的修复措施"
                    },
                    "related_fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "关联字段"
                    }
                }
            },
            "description": "命盘校验点列表"
        },
        "metadata": {
            "type": "object",
            "additionalProperties": True,
            "description": "元数据（自由结构）"
        }
    },
    "additionalProperties": True  # 允许扩展字段
}


def validate_input(packet: Dict[str, Any]) -> bool:
    """
    验证输入数据包是否符合 StandardDataPacket Schema
    
    注意：此为简化验证，生产环境应使用 jsonschema 库
    """
    required = ["trace_id", "skill_name", "execution_time", "timestamp", "status", "confidence", "data"]
    
    # 检查必需字段
    for field in required:
        if field not in packet:
            logger.warning(f"数据包缺少必需字段: {field}")
            return False
    
    # 检查字段类型
    if not isinstance(packet["trace_id"], str):
        return False
    if not isinstance(packet["skill_name"], str):
        return False
    if not isinstance(packet["execution_time"], (int, float)):
        return False
    if not isinstance(packet["timestamp"], str):
        return False
    if not isinstance(packet["status"], str):
        return False
    if not isinstance(packet["confidence"], (int, float)) or not (0 <= packet["confidence"] <= 1):
        return False
    if not isinstance(packet["data"], dict):
        return False
    
    # 可选字段类型检查
    if "errors" in packet and not isinstance(packet["errors"], list):
        return False
    if "warnings" in packet and not isinstance(packet["warnings"], list):
        return False
    if "verification_points" in packet and not isinstance(packet["verification_points"], list):
        return False
    if "metadata" in packet and not isinstance(packet["metadata"], dict):
        return False
    
    # 验证 verification_points 结构（如果存在）
    if "verification_points" in packet:
        for vp in packet["verification_points"]:
            if not isinstance(vp, dict):
                return False
            required_vp = ["field", "description", "impact", "suggestions"]
            for f in required_vp:
                if f not in vp:
                    return False
            if not isinstance(vp["suggestions"], list):
                return False
            if vp.get("impact") not in ["high", "medium", "low"]:
                return False
    
    return True


def validate_output(packet: Dict[str, Any]) -> bool:
    """验证输出数据包格式"""
    # 输出验证规则与输入基本相同，但 status 可能不同
    return validate_input(packet)


def get_schema_errors(packet: Dict[str, Any]) -> List[str]:
    """
    获取数据包验证失败的详细错误列表
    
    返回：错误消息列表
    """
    errors = []
    
    required = ["trace_id", "skill_name", "execution_time", "timestamp", "status", "confidence", "data"]
    for field in required:
        if field not in packet:
            errors.append(f"缺少必需字段: {field}")
    
    if "confidence" in packet:
        conf = packet["confidence"]
        if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
            errors.append(f"confidence 必须在 [0, 1] 范围内，当前: {conf}")
    
    if "verification_points" in packet:
        for idx, vp in enumerate(packet["verification_points"]):
            if not isinstance(vp, dict):
                errors.append(f"verification_points[{idx}] 不是对象")
                continue
            for f in ["field", "description", "impact", "suggestions"]:
                if f not in vp:
                    errors.append(f"verification_points[{idx}] 缺少字段: {f}")
            if "impact" in vp and vp["impact"] not in ["high", "medium", "low"]:
                errors.append(f"verification_points[{idx}].impact 必须是 high/medium/low")
    
    return errors


# 设置 logger（避免未定义）
import logging
logger = logging.getLogger(__name__)
