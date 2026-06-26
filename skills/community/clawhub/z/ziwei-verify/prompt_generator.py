"""
prompt_generator.py - 验证点提示词生成器

纯函数式模块：接收 StandardDataPacket，生成 ChatGPT 提示词
用于向用户解释命盘校准状态、引导理解验证点、列出待验证事项

设计原则：
- 纯函数：无副作用，不修改输入
- 易测试：每个函数独立可测
- 可配置：模板集中管理，便于后续优化
"""

from datetime import datetime
from typing import Dict, List, Optional
import json


# ========== 模板配置（可后续优化）==========

# 置信度描述
CONFIDENCE_LEVELS = {
    (0.0, 0.3): "较低",
    (0.3, 0.5): "中等",
    (0.5, 0.7): "较好",
    (0.7, 0.9): "较高",
    (0.9, 1.0): "很高"
}

# 影响级别描述
IMPACT_DESCRIPTIONS = {
    "high": "高影响（需重点关注）",
    "medium": "中等影响（建议关注）",
    "low": "低影响（参考信息）"
}

# 校准状态描述模板
CALIBRATION_STATUS_TEMPLATES = {
    "CALIBRATION_DONE": "✅ 已校正（生时已调整）",
    "NEED_VERIFICATION": "⚠️ 待校验（需要您确认）",
    "LOW_CONFIDENCE": "⚠️ 低置信度（结果仅供参考）",
    "SUCCESS": "✅ 校准完成/无需校正",
    "CALIBRATION_FAILED": "❌ 校正失败",
    "INVALID_INPUT": "❌ 输入无效"
}


def _describe_confidence(confidence: float) -> str:
    """根据分数返回置信度中文描述"""
    for (low, high), desc in CONFIDENCE_LEVELS.items():
        if low <= confidence < high:
            return desc
    return "很高" if confidence >= 1.0 else "较低"


def _format_calibration_details(packet: Dict) -> Optional[str]:
    """
    格式化校准详情（如果存在校正）
    
    返回：详情字符串 或 None
    """
    metadata = packet.get("metadata", {})
    
    if not metadata.get("calibration_applied", False):
        return None
    
    original_birth = metadata.get("original_birth")
    corrected_birth = metadata.get("corrected_birth")
    shift_hours = metadata.get("shift_hours", 0)
    
    if not original_birth or not corrected_birth:
        return None
    
    # 格式化时间显示
    def fmt(dt):
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except ValueError:
                return dt
        return dt.strftime("%Y-%m-%d %H:%M")
    
    direction = "提前" if shift_hours < 0 else "推后"
    abs_shift = abs(shift_hours)
    
    return (
        f"原始出生时间：{fmt(original_birth)}\n"
        f"校正后时间：{fmt(corrected_birth)}\n"
        f"时间偏移：{direction}{abs_shift:.1f}时辰"
    )


def _format_header(packet: Dict) -> str:
    """
    生成标题和状态摘要
    
    包含：
    - 报告标题
    - 当前置信度
    - 校准状态简述
    - 校准详情（如适用）
    """
    confidence = packet.get("confidence", 0.0)
    status = packet.get("status", "UNKNOWN")
    
    header_lines = [
        "【命盘校准状态报告】",
        f"当前置信度：{confidence:.1%}（{_describe_confidence(confidence)}）",
        f"校准状态：{CALIBRATION_STATUS_TEMPLATES.get(status, status)}"
    ]
    
    # 添加校准详情（如果适用）
    calibration_details = _format_calibration_details(packet)
    if calibration_details:
        header_lines.append(calibration_details)
    
    # 添加关键提示（根据状态）
    if status == "NEED_VERIFICATION":
        header_lines.append("💡 建议：请仔细阅读以下验证点，它们对命盘解读至关重要。")
    elif status == "LOW_CONFIDENCE":
        header_lines.append("💡 建议：当前命盘置信度较低，强烈建议进行生时校正。")
    elif status == "CALIBRATION_DONE":
        header_lines.append("💡 说明：系统已自动校正出生时间，请核对以下信息是否与您的人生经历相符。")
    
    return "\n".join(header_lines)


def _format_single_point(point: Dict, index: int) -> str:
    """
    格式化单个验证点
    
    字段参考：
    - field: 字段名（如"命宫主星"）
    - category: 类别（如"宫位星曜组合"）
    - description: 描述
    - impact: high/medium/low
    - current_value: 当前值描述
    - suggestions: 建议列表
    - age_range: [min_age, max_age] 或 [0,0] 表示不适用
    - confidence_weight: 权重 0-1
    """
    lines = []
    
    # 标题：序号 + 类别 + 影响级别
    impact_desc = IMPACT_DESCRIPTIONS.get(point.get("impact", ""), "未知影响")
    title = f"{index}. 【{point.get('category', '验证点')}】"
    if point.get("field"):
        title += f"（{point['field']}）"
    title += f" - {impact_desc}"
    lines.append(title)
    
    # 描述
    if point.get("description"):
        lines.append(f"   说明：{point['description']}")
    
    # 当前值
    if point.get("current_value"):
        lines.append(f"   当前状态：{point['current_value']}")
    
    # 权重（如非默认）
    weight = point.get("confidence_weight", 0.0)
    if weight > 0:
        lines.append(f"   权重：{weight:.2f}")
    
    # 年龄范围
    age_range = point.get("age_range", [0, 0])
    if age_range and age_range != [0, 0]:
        lines.append(f"   影响年龄：{age_range[0]}-{age_range[1]}岁")
    
    # 建议
    suggestions = point.get("suggestions", [])
    if suggestions:
        suggestion_lines = "\n".join([f"   • {s}" for s in suggestions])
        lines.append(f"   建议：\n{suggestion_lines}")
    
    # 关联字段
    related = point.get("related_fields", [])
    if related:
        lines.append(f"   关联：{', '.join(related)}")
    
    return "\n".join(lines)


def _format_points(points: List[Dict]) -> str:
    """
    格式化验证点列表
    
    返回：完整格式化字符串
    """
    if not points:
        return "未检测到需特别关注的验证点。"
    
    lines = ["\n检测到的关键验证点：\n"]
    
    for idx, point in enumerate(points, 1):
        formatted = _format_single_point(point, idx)
        lines.append(formatted)
        lines.append("")  # 空行分隔
    
    return "\n".join(lines).rstrip()


def _format_footer(packet: Dict) -> str:
    """
    生成建议和后续步骤
    
    根据状态给出不同建议
    """
    status = packet.get("status", "")
    confidence = packet.get("confidence", 0.0)
    lines = []
    
    lines.append("\n【说明】")
    
    if status == "NEED_VERIFICATION":
        lines.append("以上验证点基于紫微斗数经典规则生成，需要您的确认或补充信息。")
        lines.append("建议逐项核对，确保命盘解读准确。")
    elif status == "LOW_CONFIDENCE":
        lines.append("当前命盘置信度较低，可能原因：")
        lines.append("• 出生时间不准确（建议校正）")
        lines.append("• 出生地点经纬度未提供（影响真太阳时计算）")
        lines.append("• 命盘特殊格局（如命宫无主星）")
        lines.append("建议进行生时校正以提升准确性。")
    elif status == "CALIBRATION_DONE":
        lines.append("系统已自动调整出生时间，上述验证点用于核对调整后的命盘是否与您的人生经历相符。")
        lines.append("如有多项不匹配，请考虑提供更准确的出生地点或重新校准。")
    else:  # SUCCESS
        lines.append("以上验证点基于紫微斗数经典规则生成，供参考。")
    
    lines.append("\n【后续步骤】")
    if status in ["NEED_VERIFICATION", "LOW_CONFIDENCE"]:
        lines.append("1. 逐项核对验证点的描述与您的人生经历是否相符")
        lines.append("2. 如有不符，请提供更准确的出生时间或地点信息")
        lines.append("3. 或直接咨询专业命理师进行手动校准")
    else:
        lines.append("• 如需详细解读，请咨询专业命理师")
        lines.append("• 本报告仅供参考，不作为人生决策依据")
    
    lines.append("\n---")
    lines.append("生成时间：{}".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    return "\n".join(lines)


def generate_verification_prompt(packet: Dict) -> str:
    """
    主入口：生成完整的验证提示词
    
    参数：
        packet: StandardDataPacket 字典
        
    返回：
        ChatGPT 提示词字符串（Markdown 格式）
    """
    # 输入验证（基本检查）
    required_fields = ["confidence", "status"]
    for field in required_fields:
        if field not in packet:
            raise ValueError(f"StandardDataPacket 缺少必需字段: {field}")
    
    # 可选字段
    verification_points = packet.get("verification_points", [])
    
    # 分块生成
    parts = []
    
    # 1. 标题与状态
    parts.append(_format_header(packet))
    parts.append("")
    
    # 2. 验证点列表
    parts.append(_format_points(verification_points))
    parts.append("")
    
    # 3. 说明与后续步骤
    parts.append(_format_footer(packet))
    
    return "\n".join(parts)


# ========== 便捷函数（用于调试/单独使用）==========

def generate_verification_summary(packet: Dict) -> str:
    """
    生成验证点摘要（仅关键信息，不包含详细建议）
    
    用于快速预览
    """
    points = packet.get("verification_points", [])
    if not points:
        return "无验证点"
    
    high = sum(1 for p in points if p.get("impact") == "high")
    medium = sum(1 for p in points if p.get("impact") == "medium")
    low = sum(1 for p in points if p.get("impact") == "low")
    
    return f"共{len(points)}项（高影响{high}项，中影响{medium}项，低影响{low}项）"


def format_point_as_json(point: Dict) -> str:
    """
    将单个验证点格式化为 JSON 字符串（用于调试）
    """
    # 过滤掉可能的非序列化对象
    clean_point = {}
    for k, v in point.items():
        if isinstance(v, (str, int, float, bool, list, dict, type(None))):
            clean_point[k] = v
        else:
            clean_point[k] = str(v)
    return json.dumps(clean_point, ensure_ascii=False, indent=2)
