"""
ziwei_verify 技能主入口
OpenClaw 调用格式：ziwei_verify action=calibrate packet=<StandardDataPacket>
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional

from .calibrator import calibrate
from .dialogue_handler import VerificationDialogueHandler
from .output_formatter import format_calibration_result
from .prompt_generator import generate_verification_prompt
from .schemas import validate_input

logger = logging.getLogger(__name__)

# 全局对话处理器实例（用于交互模式）
_dialogue_handler = VerificationDialogueHandler()


def run(
    action: str = "calibrate",
    packet: Optional[Dict[str, Any]] = None,
    birth_dt: Optional[str] = None,
    max_shifts: int = 2,
    interactive: bool = False
) -> Dict[str, Any]:
    """
    主入口函数
    
    参数：
    - action: "calibrate" | "suggest" | "validate"
    - packet: ziwei 返回的 StandardDataPacket（必须包含 verification_points）
    - birth_dt: 原始出生时间（ISO 8601），用于校正
    - max_shifts: 最大校正偏移（1 或 2 时辰）
    - interactive: 是否交互模式（需用户确认）
    
    返回：StandardDataPacket（status 为 CALIBRATION_DONE 或 LOW_CONFIDENCE）
    """
    # 参数验证
    if not packet or not isinstance(packet, dict):
        return {
            "status": "INVALID_INPUT",
            "errors": ["缺少有效命盘数据包（packet）"],
            "confidence": 0.0
        }
    
    if not validate_input(packet):
        return {
            "status": "INVALID_INPUT",
            "errors": ["数据包格式不符合 StandardDataPacket Schema"],
            "confidence": 0.0
        }
    
    # 检查 verification_points 字段是否存在（为空列表表示无需校正，不是错误）
    if 'verification_points' not in packet:
        return {
            "status": "INVALID_INPUT",
            "errors": ["命盘数据包缺少 verification_points 字段"],
            "confidence": 0.0
        }
    
    # 如果 verification_points 为空，说明无需校正，直接返回成功
    if not packet.get('verification_points'):
        return {
            "trace_id": packet.get("trace_id", ""),
            "skill_name": "ziwei_verify",
            "execution_time": 0.0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "SUCCESS",
            "confidence": packet.get("confidence", 1.0),
            "data": packet.get("data", {}),
            "verification_points": [],
            "errors": [],
            "warnings": ["命盘无验证点，无需校正"],
            "metadata": {"action": "calibrate", "no_verification_points": True}
        }
    
    # 解析 birth_dt
    birth_datetime = None
    if birth_dt:
        try:
            birth_datetime = datetime.fromisoformat(birth_dt.replace('Z', '+00:00'))
        except ValueError as e:
            return {
                "status": "INVALID_INPUT",
                "errors": [f"birth_dt 格式错误: {e}"],
                "confidence": 0.0
            }
    else:
        # 尝试从 packet 中提取
        birth_info = packet.get('data', {}).get('birth_info', {})
        birth_dt_str = birth_info.get('birth_dt')
        if birth_dt_str:
            try:
                birth_datetime = datetime.fromisoformat(birth_dt_str.replace('Z', '+00:00'))
            except ValueError:
                pass
    
    if not birth_datetime:
        return {
            "status": "INVALID_INPUT",
            "errors": ["未提供出生时间（birth_dt），无法进行生时校正"],
            "confidence": 0.0
        }
    
    # 路由到具体动作
    if action == "calibrate":
        result = calibrate(packet, birth_datetime, max_shifts, interactive)
        
        # 集成 prompt_generator：如果是 NEED_VERIFICATION 或 LOW_CONFIDENCE 状态，生成提示词
        if result.get("status") in ("NEED_VERIFICATION", "LOW_CONFIDENCE"):
            try:
                verification_prompt = generate_verification_prompt(result)
                result["verification_prompt"] = verification_prompt
            except Exception as e:
                logger.warning(f"生成验证提示词失败: {e}")
                result["verification_prompt"] = None
        
        return result
    elif action == "suggest":
        return suggest_correction(packet, birth_datetime, max_shifts)
    elif action == "validate":
        return validate_packet(packet)
    else:
        return {
            "status": "INVALID_INPUT",
            "errors": [f"未知动作: {action}，支持: calibrate | suggest | validate"],
            "confidence": 0.0
        }


def suggest_correction(
    packet: Dict[str, Any],
    birth_dt: datetime,
    max_shifts: int = 2
) -> Dict[str, Any]:
    """
    仅生成候选校正方案，不执行实际校正
    
    返回：包含候选列表的 StandardDataPacket（status=SUCCESS）
    """
    from .calibrator import generate_correction_candidates
    
    candidates = generate_correction_candidates(packet, birth_dt, max_shifts)
    
    return {
        "trace_id": packet.get("trace_id", ""),
        "skill_name": "ziwei_verify",
        "execution_time": 0.0,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "SUCCESS",
        "confidence": 0.0,
        "data": {
            "original_birth_dt": birth_dt.isoformat(),
            "candidates": candidates,
            "interactive_required": True
        },
        "verification_points": packet.get("verification_points", []),
        "errors": [],
        "warnings": ["此结果仅供建议，需用户确认后重新生成命盘"],
        "metadata": {
            "action": "suggest",
            "max_shifts": max_shifts
        }
    }


def validate_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证输入数据包是否符合 StandardDataPacket Schema
    
    返回：验证结果
    """
    from .schemas import validate_input
    
    is_valid = validate_input(packet)
    missing_fields = []
    
    required = ["trace_id", "skill_name", "status", "confidence", "data", "verification_points"]
    for field in required:
        if field not in packet:
            missing_fields.append(field)
    
    return {
        "trace_id": packet.get("trace_id", ""),
        "skill_name": "ziwei_verify",
        "execution_time": 0.0,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "SUCCESS" if is_valid else "INVALID_INPUT",
        "confidence": 1.0 if is_valid else 0.0,
        "data": {
            "is_valid": is_valid,
            "missing_fields": missing_fields,
            "has_verification_points": bool(packet.get("verification_points"))
        },
        "verification_points": [],
        "errors": [] if is_valid else ["数据包格式无效"],
        "warnings": [],
        "metadata": {
            "action": "validate"
        }
    }
