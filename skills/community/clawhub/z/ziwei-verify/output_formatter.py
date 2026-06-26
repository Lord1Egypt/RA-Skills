"""
output_formatter.py - 结果格式化
"""

from typing import List, Dict, Any
from datetime import datetime
from .calibrator import CorrectionResult, format_shift_description


def format_calibration_result(result: CorrectionResult) -> str:
    """格式化单个校正结果（人类可读）"""
    lines = [
        "【生时校正结果】",
        f"• 时间偏移：{format_shift_description(result.shift_hours)}",
        f"• 校正时间：{result.corrected_dt.strftime('%Y-%m-%d %H:%M')}",
        f"• 置信度：{result.confidence:.3f}",
        f"• 剩余高影响校验点：{result.verification_points_remaining}",
    ]
    
    if result.key_changes:
        lines.append("• 关键变化：")
        for change in result.key_changes[:3]:  # 最多3条
            lines.append(f"  - {change}")
    
    if result.match_score is not None:
        lines.append(f"• 匹配度：{result.match_score:.1%}")
    
    return "\n".join(lines)


def format_comparison_table(results: List[CorrectionResult]) -> str:
    """
    格式化对比表（Markdown 风格，适合在消息中展示）
    
    返回：表格字符串
    """
    if not results:
        return "（无候选方案）"
    
    # 构建表头
    header = (
        f"{'方案':<4}  "
        f"{'偏移':<12}  "
        f"{'置信度':<8}  "
        f"{'高影响点':<6}  "
        f"{'关键变化'}"
    )
    separator = "-" * 80
    
    lines = [header, separator]
    
    for idx, r in enumerate(results[:3]):
        shift_desc = format_shift_description(r.shift_hours)
        conf_str = f"{r.confidence:.3f}"
        high_impact = str(r.verification_points_remaining)
        
        # 关键变化摘要
        changes = ""
        if r.key_changes:
            changes = "; ".join(r.key_changes[:2])
            if len(changes) > 30:
                changes = changes[:27] + "..."
        else:
            changes = "无"
        
        line = (
            f"{idx:<4}  "
            f"{shift_desc:<12}  "
            f"{conf_str:<8}  "
            f"{high_impact:<6}  "
            f"{changes}"
        )
        lines.append(line)
    
    return "\n".join(lines)


def format_full_calibration_report(
    original_packet: Dict[str, Any],
    results: List[CorrectionResult],
    best_index: int,
    interactive: bool = False
) -> str:
    """
    生成完整的校正报告
    
    返回：详细报告文本
    """
    lines = [
        "=" * 60,
        "生时校正完整报告",
        "=" * 60,
        f"原始时间：{original_packet.get('data', {}).get('birth_info', {}).get('birth_dt', '未知')}",
        f"评估候选数：{len(results)}",
        f"模式：{'交互式' if interactive else '自动'}",
        ""
    ]
    
    # 最优方案
    best = results[best_index]
    lines.append("【推荐方案】")
    lines.append(format_calibration_result(best))
    lines.append("")
    
    # 所有候选对比
    lines.append("【全部候选对比】")
    lines.append(format_comparison_table(results))
    lines.append("")
    
    # 结论
    if best.confidence >= 0.7 and best.verification_points_remaining == 0:
        conclusion = "✅ 校正成功：置信度高且无高影响校验点"
    elif best.confidence >= 0.6:
        conclusion = "⚠️ 校正中等：置信度一般，建议复核"
    else:
        conclusion = "❌ 校正失败：置信度过低，不建议采纳"
    
    lines.append(f"结论：{conclusion}")
    
    return "\n".join(lines)


def format_interactive_prompt(
    candidates: List[CorrectionResult],
    session_id: str
) -> str:
    """
    生成交互式选择提示
    
    返回：用户可读的提示消息
    """
    table = format_comparison_table(candidates)
    
    return (
        f"会话ID：{session_id}\n"
        f"请选择校正方案：\n\n"
        f"{table}\n\n"
        f"💬 回复数字（0-2）确认选择，或回复 `skip` 跳过"
    )


def format_validation_summary(validation_result: Dict[str, Any]) -> str:
    """格式化验证结果摘要"""
    is_valid = validation_result.get("data", {}).get("is_valid", False)
    missing = validation_result.get("data", {}).get("missing_fields", [])
    has_vps = validation_result.get("data", {}).get("has_verification_points", False)
    
    lines = ["【数据包验证结果】"]
    
    if is_valid and has_vps:
        lines.append("✅ 数据包格式正确，包含 verification_points")
    elif is_valid and not has_vps:
        lines.append("⚠️ 数据包格式正确，但缺少 verification_points")
    else:
        lines.append("❌ 数据包格式无效")
        if missing:
            lines.append(f"   缺失字段：{', '.join(missing)}")
    
    return "\n".join(lines)
