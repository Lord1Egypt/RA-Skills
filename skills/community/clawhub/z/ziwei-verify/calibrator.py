"""
calibrator.py - 生时校正引擎
基于置信度最大化原则，搜索最优出生时间
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import uuid

logger = logging.getLogger(__name__)

# 一时辰 = 2 小时
HOURS_PER_SHIFT = 2


@dataclass
class CorrectionResult:
    """单个候选校正结果"""
    shift_hours: float              # 时间偏移（小时）
    corrected_dt: datetime          # 校正后时间
    packet: Dict                    # 校正后的 StandardDataPacket
    confidence: float               # 置信度
    verification_points_remaining: int  # 剩余高影响校验点数量
    key_changes: List[str]          # 关键变化摘要
    match_score: float              # 与原盘验证点的匹配度


def calibrate(
    original_packet: Dict[str, Any],
    birth_dt: datetime,
    max_shifts: int = 2,
    interactive: bool = False
) -> Dict[str, Any]:
    """
    执行生时校正
    
    步骤：
    1. 生成候选时间列表（±1、±2 时辰）
    2. 对每个候选时间调用 ziwei.arrange_with_packet() 生成新命盘
    3. 计算新命盘的 verification_points 和 confidence
    4. 计算匹配度（与原 verification_points 的匹配程度）
    5. 选择最优候选（confidence最高且高影响校验点最少）
    6. 返回校正结果
    
    返回：StandardDataPacket（status=CALIBRATION_DONE 或 LOW_CONFIDENCE 或 NEED_VERIFICATION）
    """
    results = []
    
    # 生成候选偏移列表（单位：时辰）
    shifts = generate_shift_list(max_shifts)
    logger.info(f"开始生时校正，候选偏移（时辰）: {shifts}")
    
    # 遍历所有候选
    for shift_hours in shifts:
        try:
            corrected_dt = birth_dt + timedelta(hours=shift_hours)
            
            # 调用 ziwei 生成新命盘
            # 注意：实际应通过 OpenClaw skill invoke 机制，此处为模拟实现
            new_packet = invoke_ziwei_skill(original_packet, corrected_dt)
            
            if not new_packet or new_packet.get("status") != "SUCCESS":
                logger.warning(f"候选偏移 {shift_hours}h 生成命盘失败")
                continue
            
            # 计算匹配度
            match_score = _calculate_match_score(
                original_packet.get("verification_points", []),
                new_packet.get("verification_points", [])
            )
            
            # 提取高影响校验点
            high_impact = count_high_impact_points(new_packet.get("verification_points", []))
            
            # 提取关键变化
            key_changes = extract_key_changes_summary(original_packet, new_packet)
            
            result = CorrectionResult(
                shift_hours=shift_hours,
                corrected_dt=corrected_dt,
                packet=new_packet,
                confidence=new_packet.get("confidence", 0.0),
                verification_points_remaining=high_impact,
                key_changes=key_changes,
                match_score=match_score
            )
            results.append(result)
            logger.debug(f"候选 {shift_hours:+}h: confidence={result.confidence:.3f}, high_impact={high_impact}")
            
        except Exception as e:
            logger.error(f"候选偏移 {shift_hours} 小时处理失败: {e}", exc_info=True)
            continue
    
    if not results:
        return {
            "status": "CALIBRATION_FAILED",
            "errors": ["所有候选时间均无法生成有效命盘"],
            "confidence": 0.0
        }
    
    # 排序：置信度降序，其次高影响校验点数量升序，再其次匹配度降序
    results.sort(
        key=lambda r: (r.confidence, -r.verification_points_remaining, r.match_score),
        reverse=True
    )
    
    best = results[0]
    logger.info(f"最优候选: {best.shift_hours:+}h, confidence={best.confidence:.3f}")
    
    # 判断是否达到自动校正标准
    auto_accept = (
        best.confidence >= 0.7 and
        best.verification_points_remaining == 0 and
        best.match_score >= 0.5
    )
    
    if interactive:
        # 交互模式：返回候选列表供用户选择
        return {
            "trace_id": original_packet.get("trace_id", str(uuid.uuid4())),
            "skill_name": "ziwei_verify",
            "execution_time": 0.0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "NEED_VERIFICATION",
            "confidence": 0.0,
            "data": {
                "original_birth_dt": birth_dt.isoformat(),
                "candidates": [asdict(r) for r in results[:3]],
                "best_candidate": asdict(best),
                "auto_accept_threshold": {"confidence": 0.7, "high_impact": 0, "match_score": 0.5},
                "interactive_required": True
            },
            "verification_points": original_packet.get("verification_points", []),
            "errors": [],
            "warnings": ["请从候选列表中选择校正方案"],
            "metadata": {
                "total_candidates": len(results),
                "max_shifts": max_shifts
            }
        }
    elif auto_accept:
        # 自动接受最优候选
        return {
            **best.packet,
            "trace_id": original_packet.get("trace_id", best.packet.get("trace_id")),
            "skill_name": "ziwei_verify",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "CALIBRATION_DONE",
            "data": {
                **best.packet.get("data", {}),
                "original_birth_dt": birth_dt.isoformat(),
                "corrected_birth_dt": best.corrected_dt.isoformat(),
                "shift_hours": best.shift_hours,
                "shift_description": format_shift_description(best.shift_hours),
                "calibration_metadata": {
                    "match_score": best.match_score,
                    "candidates_evaluated": len(results),
                    "auto_accepted": True
                }
            },
            "metadata": {
                **best.packet.get("metadata", {}),
                "original_packet_id": original_packet.get("trace_id"),
                "best_candidate_confidence": best.confidence,
                "calibration_strategy": "confidence_maximization"
            }
        }
    else:
        # 置信度不足，返回最佳候选但标记为 LOW_CONFIDENCE
        return {
            "trace_id": original_packet.get("trace_id", str(uuid.uuid4())),
            "skill_name": "ziwei_verify",
            "execution_time": 0.0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "LOW_CONFIDENCE",
            "confidence": best.confidence,
            "message": "自动校正置信度不足，建议人工复核",
            "data": {
                "best_candidate": asdict(best),
                "all_candidates": [asdict(r) for r in results[:3]],
                "auto_accept_requirements": {
                    "confidence": 0.7,
                    "high_impact_points": 0,
                    "match_score": 0.5
                },
                "reason": {
                    "confidence_too_low": best.confidence < 0.7,
                    "high_impact_remaining": best.verification_points_remaining > 0,
                    "match_score_too_low": best.match_score < 0.5
                }
            },
            "verification_points": best.packet.get("verification_points", []),
            "errors": [],
            "warnings": ["校正结果置信度低于阈值，请谨慎使用"],
            "metadata": {
                "total_candidates": len(results),
                "max_shifts": max_shifts
            }
        }


def generate_shift_list(max_shifts: int) -> List[int]:
    """
    生成候选时间偏移列表（单位：小时）
    
    策略：
    - max_shifts=1: [-2, +2]（±1 时辰）
    - max_shifts=2: [-4, -2, +2, +4]（±2 时辰，不含 0）
    """
    if max_shifts not in (1, 2):
        raise ValueError(f"max_shifts 必须为 1 或 2，当前: {max_shifts}")
    
    base_shifts = [(-max_shifts * HOURS_PER_SHIFT), -HOURS_PER_SHIFT,
                   HOURS_PER_SHIFT, max_shifts * HOURS_PER_SHIFT]
    return base_shifts


def generate_correction_candidates(
    packet: Dict[str, Any],
    birth_dt: datetime,
    max_shifts: int = 2
) -> List[Dict]:
    """
    生成候选列表（供 suggest action 使用）
    """
    shifts = generate_shift_list(max_shifts)
    candidates = []
    
    for shift_hours in shifts:
        corrected_dt = birth_dt + timedelta(hours=shift_hours)
        candidates.append({
            "shift_hours": shift_hours,
            "shift_description": format_shift_description(shift_hours),
            "corrected_dt": corrected_dt.isoformat(),
            "nongli_approx": "需重新计算"  # 占位
        })
    
    return candidates


def invoke_ziwei_skill(
    original_packet: Dict[str, Any],
    corrected_dt: datetime
) -> Optional[Dict[str, Any]]:
    """
    调用 ziwei 技能生成新命盘
    
    注意：此函数应通过 OpenClaw 的 skill invoke 机制实现。
    当前为模拟实现，返回一个假想的命盘数据包。
    
    实际实现方式：
    1. 使用 OpenClaw 插件系统：`invoke_skill("ziwei", ...)`
    2. 或通过 API 调用：`requests.post("/skills/ziwei/arrange", ...)`
    3. 或直接 import（会引入循环依赖，不推荐）
    """
    # TODO: 替换为实际的 ziwei 调用
    # 示例（伪代码）：
    # from openclaw.skills import invoke
    # new_packet = invoke("ziwei", action="arrange_with_packet", ...)
    
    # 临时：模拟生成一个命盘（仅用于结构验证）
    logger.warning("invoke_ziwei_skill() 为模拟实现，请替换为真实 ziwei 调用")
    
    # 提取原数据
    gender = original_packet.get("data", {}).get("birth_info", {}).get("gender", "M")
    
    # 模拟：置信度略有提升（实际应由 ziwei 计算）
    base_confidence = original_packet.get("confidence", 0.3)
    simulated_confidence = min(0.95, base_confidence + 0.15 + (abs(corrected_dt.hour - 14) * 0.01))
    
    # 模拟：生成新 verification_points（数量减少）
    original_vps = original_packet.get("verification_points", [])
    simulated_vps = simulate_verification_points(original_vps, simulated_confidence)
    
    return {
        "trace_id": str(uuid.uuid4()),
        "skill_name": "ziwei",
        "execution_time": 0.234,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "SUCCESS",
        "confidence": simulated_confidence,
        "data": {
            "birth_info": {
                "gender": gender,
                "birth_dt": corrected_dt.isoformat(),
                "location": original_packet.get("data", {}).get("birth_info", {}).get("location", "北京")
            },
            "chart_data": {"simulated": True}  # 占位
        },
        "verification_points": simulated_vps,
        "errors": [],
        "warnings": [],
        "metadata": {
            "cache_key": f"ziwei_sim:{corrected_dt.strftime('%Y%m%d%H')}:{gender}",
            "simulation_mode": True
        }
    }


def simulate_verification_points(
    original_vps: List[Dict],
    confidence: float
) -> List[Dict]:
    """
    模拟生成 verification_points（仅用于测试）
    
    规则：
    - confidence >= 0.7：无验证点（完全匹配）
    - confidence >= 0.5：仅保留低影响点
    - confidence < 0.5：保留所有点
    """
    import random
    random.seed(42)  # 可重复
    
    if not original_vps:
        return []
    
    # 高置信度：无验证点
    if confidence >= 0.7:
        return []
    
    simulated = []
    for vp in original_vps:
        # 中等置信度：只保留低影响点
        if confidence >= 0.5 and vp.get("impact") == "high":
            continue
        # 低置信度：保留所有点，但可能降级影响级别
        new_vp = vp.copy()
        if confidence > 0.6 and random.random() < 0.3:
            new_vp["impact"] = "medium"
        simulated.append(new_vp)
    
    return simulated


def _calculate_match_score(
    original_points: List[Dict],
    new_points: List[Dict]
) -> float:
    """
    计算新命盘验证点与原命盘验证点的匹配度
    
    匹配逻辑：
    1. 相同 event_type / field 的数量重叠度
    2. 高影响点完全匹配加权
    3. 描述语义相似度（简化：用关键词重叠）
    
    返回：匹配分数（0-1）
    """
    if not original_points:
        return 1.0  # 原盘无验证点，任何结果均可
    
    if not new_points:
        return 1.0  # 新盘无验证点（已全部解决），视为完全匹配
    
    # 提取字段集合
    orig_fields = {p.get("field", "") for p in original_points if p.get("field")}
    new_fields = {p.get("field", "") for p in new_points if p.get("field")}
    
    if not orig_fields:
        return 1.0
    
    # Jaccard 相似度
    intersection = orig_fields.intersection(new_fields)
    union = orig_fields.union(new_fields)
    jaccard = len(intersection) / len(union) if union else 1.0
    
    # 高影响点匹配加权
    orig_high = {p.get("field") for p in original_points if p.get("impact") == "high"}
    new_high = {p.get("field") for p in new_points if p.get("impact") == "high"}
    
    if orig_high:
        high_match = len(orig_high.intersection(new_high)) / len(orig_high)
    else:
        high_match = 1.0
    
    # 综合得分：Jaccard 70% + 高影响点匹配 30%
    final_score = 0.7 * jaccard + 0.3 * high_match
    return round(final_score, 4)


def count_high_impact_points(points: List[Dict]) -> int:
    """统计高影响校验点数量"""
    return sum(1 for p in points if p.get("impact") == "high")


def extract_key_changes_summary(
    original: Dict[str, Any],
    corrected: Dict[str, Any]
) -> List[str]:
    """
    提取关键变化摘要
    
    对比项：
    - confidence 变化
    - verification_points 数量变化
    - 高影响点是否消除
    """
    changes = []
    
    orig_conf = original.get("confidence", 0.0)
    new_conf = corrected.get("confidence", 0.0)
    delta_conf = new_conf - orig_conf
    changes.append(f"置信度 {orig_conf:.2f} → {new_conf:.2f} (Δ {delta_conf:+.2f})")
    
    orig_vps = original.get("verification_points", [])
    new_vps = corrected.get("verification_points", [])
    orig_high = count_high_impact_points(orig_vps)
    new_high = count_high_impact_points(new_vps)
    
    if orig_high > 0:
        changes.append(f"高影响校验点: {orig_high} → {new_high}")
    
    # 提取前几个关键字段变化（简化）
    if orig_vps and new_vps:
        orig_fields = {p.get("field") for p in orig_vps}
        new_fields = {p.get("field") for p in new_vps}
        resolved = orig_fields - new_fields
        if resolved:
            changes.append(f"已解决: {', '.join(list(resolved)[:2])}")
    
    return changes


def format_shift_description(shift_hours: float) -> str:
    """生成偏移描述文本"""
    if shift_hours < 0:
        return f"提前{abs(shift_hours) / 2:.1f}时辰"
    else:
        return f"推后{shift_hours / 2:.1f}时辰"
