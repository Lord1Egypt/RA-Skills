"""
tests/test_prompt_generator.py - P3 提示词生成器单元测试

测试目标：
1. generate_verification_prompt() 基本功能
2. 不同状态下的输出格式
3. 验证点列表格式化
4. 边界情况处理
"""

from pathlib import Path
import importlib.util

# 直接加载 prompt_generator 模块，避免触发 __init__.py 的其他导入
spec = importlib.util.spec_from_file_location(
    "prompt_generator", 
    Path(__file__).resolve().parent.parent / "prompt_generator.py"
)
pg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pg)

# 导入所需函数
generate_verification_prompt = pg.generate_verification_prompt
generate_verification_summary = pg.generate_verification_summary
format_point_as_json = pg.format_point_as_json
_format_header = pg._format_header
_format_points = pg._format_points
_format_footer = pg._format_footer
_describe_confidence = pg._describe_confidence


# ========== 测试数据构建助手 ==========

def make_packet(
    confidence: float = 0.7,
    status: str = "SUCCESS",
    verification_points: list = None,
    metadata: dict = None,
    original_birth: str = None,
    corrected_birth: str = None,
    shift_hours: float = 0.0,
    calibration_applied: bool = False
) -> dict:
    """
    构建 StandardDataPacket 测试数据
    
    参数：
    - confidence: 置信度 0-1
    - status: 状态字符串
    - verification_points: 验证点列表
    - metadata: 完整 metadata（可选，会与下参数合并）
    - original_birth: 原始出生时间字符串
    - corrected_birth: 校正后时间字符串
    - shift_hours: 偏移小时数
    - calibration_applied: 是否已校正
    """
    packet = {
        "trace_id": "test-123",
        "skill_name": "ziwei",
        "execution_time": 1.0,
        "timestamp": "2026-05-04T08:00:00+08:00",
        "status": status,
        "confidence": confidence,
        "data": {"test": True},
        "errors": [],
        "warnings": []
    }
    
    if verification_points is not None:
        packet["verification_points"] = verification_points
    
    # 构建 metadata
    meta = metadata or {}
    if original_birth:
        meta["original_birth"] = original_birth
    if corrected_birth:
        meta["corrected_birth"] = corrected_birth
    if shift_hours != 0.0:
        meta["shift_hours"] = shift_hours
    meta["calibration_applied"] = calibration_applied
    
    if meta:
        packet["metadata"] = meta
    
    return packet


def make_verification_point(
    field: str = "测试字段",
    category: str = "测试类别",
    description: str = "测试描述",
    impact: str = "medium",
    current_value: str = "测试值",
    suggestions: list = None,
    related_fields: list = None,
    age_range: list = None,
    confidence_weight: float = 0.5
) -> dict:
    """
    构建单个验证点字典
    """
    return {
        "field": field,
        "category": category,
        "description": description,
        "impact": impact,
        "current_value": current_value,
        "suggestions": suggestions or ["建议1", "建议2"],
        "related_fields": related_fields or ["关联字段1"],
        "age_range": age_range or [0, 0],
        "confidence_weight": confidence_weight
    }


# ========== 测试用例 ==========

def test_describe_confidence():
    """测试置信度描述函数"""
    print("\n[TEST] _describe_confidence")
    
    assert _describe_confidence(0.1) == "较低"
    assert _describe_confidence(0.4) == "中等"
    assert _describe_confidence(0.6) == "较好"
    assert _describe_confidence(0.8) == "较高"
    assert _describe_confidence(0.95) == "很高"
    print("  ✅ 置信度描述正确")


def test_format_header_success():
    """测试 SUCCESS 状态的标题"""
    print("\n[TEST] _format_header - SUCCESS")
    packet = make_packet(confidence=0.75, status="SUCCESS")
    header = _format_header(packet)
    
    assert "当前置信度：75.0%" in header
    assert "校准状态：✅ 已校正" not in header  # 没有校正
    assert "校准状态：✅ 校准完成/无需校正" in header
    print("  ✅ SUCCESS 状态标题正确")


def test_format_header_calibration_done():
    """测试 CALIBRATION_DONE 状态的标题（包含校正详情）"""
    print("\n[TEST] _format_header - CALIBRATION_DONE")
    packet = make_packet(
        confidence=0.82,
        status="CALIBRATION_DONE",
        original_birth="1993-04-01T14:00:00+08:00",
        corrected_birth="1993-04-01T15:00:00+08:00",
        shift_hours=1.0,
        calibration_applied=True
    )
    header = _format_header(packet)
    
    assert "当前置信度：82.0%" in header
    assert "校准状态：✅ 已校正（生时已调整）" in header
    assert "原始出生时间：1993-04-01 14:00" in header
    assert "校正后时间：1993-04-01 15:00" in header
    assert "时间偏移：推后1.0时辰" in header
    print("  ✅ CALIBRATION_DONE 状态标题及校正详情正确")


def test_format_header_need_verification():
    """测试 NEED_VERIFICATION 状态的标题"""
    print("\n[TEST] _format_header - NEED_VERIFICATION")
    packet = make_packet(confidence=0.45, status="NEED_VERIFICATION")
    header = _format_header(packet)
    
    assert "校准状态：⚠️ 待校验（需要您确认）" in header
    assert "请仔细阅读以下验证点" in header
    print("  ✅ NEED_VERIFICATION 状态标题正确")


def test_format_header_low_confidence():
    """测试 LOW_CONFIDENCE 状态的标题"""
    print("\n[TEST] _format_header - LOW_CONFIDENCE")
    packet = make_packet(confidence=0.25, status="LOW_CONFIDENCE")
    header = _format_header(packet)
    
    assert "校准状态：⚠️ 低置信度（结果仅供参考）" in header
    assert "当前命盘置信度较低" in header
    print("  ✅ LOW_CONFIDENCE 状态标题正确")


def test_format_points_empty():
    """测试空验证点列表"""
    print("\n[TEST] _format_points - empty")
    result = _format_points([])
    assert result == "未检测到需特别关注的验证点。"
    print("  ✅ 空列表处理正确")


def test_format_points_single():
    """测试单个验证点"""
    print("\n[TEST] _format_points - single")
    point = make_verification_point(
        field="命宫主星",
        category="宫位星曜",
        description="命宫为空宫",
        impact="high",
        current_value="无主星",
        suggestions=["校正出生时间", "验证出生地点"],
        related_fields=["命宫", "身宫"],
        age_range=[0, 0],
        confidence_weight=0.30
    )
    result = _format_points([point])
    
    assert "1. 【宫位星曜】" in result
    assert "（命宫主星）" in result
    assert "- 高影响（需重点关注）" in result
    assert "说明：命宫为空宫" in result
    assert "当前状态：无主星" in result
    assert "权重：0.30" in result
    assert "建议：" in result
    assert "• 校正出生时间" in result
    assert "关联：命宫, 身宫" in result
    print("  ✅ 单个验证点格式化正确")


def test_format_points_multiple():
    """测试多个验证点"""
    print("\n[TEST] _format_points - multiple")
    points = [
        make_verification_point(
            field="事业宫",
            category="官禄宫星曜组合",
            description="紫微+天府，事业起飞",
            impact="high",
            current_value="紫微:True, 天府:True",
            suggestions=["核对职业起点"],
            age_range=[28, 35],
            confidence_weight=0.80
        ),
        make_verification_point(
            field="财帛宫",
            category="财帛宫星曜组合",
            description="禄存+天马",
            impact="medium",
            current_value="禄存:True, 天马:True",
            suggestions=["验证财运年份"],
            age_range=[30, 40],
            confidence_weight=0.75
        )
    ]
    result = _format_points(points)
    
    # 检查两个点都出现
    assert "1. 【官禄宫星曜组合】" in result
    assert "2. 【财帛宫星曜组合】" in result
    assert "影响年龄：28-35岁" in result
    assert "影响年龄：30-40岁" in result
    print("  ✅ 多个验证点格式化正确")


def test_format_footer_success():
    """测试 SUCCESS 状态的页脚"""
    print("\n[TEST] _format_footer - SUCCESS")
    packet = make_packet(confidence=0.75, status="SUCCESS")
    footer = _format_footer(packet)
    
    assert "【说明】" in footer
    assert "以上验证点基于紫微斗数经典规则生成" in footer
    assert "【后续步骤】" in footer
    assert "如需详细解读，请咨询专业命理师" in footer
    print("  ✅ SUCCESS 页脚正确")


def test_format_footer_need_verification():
    """测试 NEED_VERIFICATION 状态的页脚"""
    print("\n[TEST] _format_footer - NEED_VERIFICATION")
    packet = make_packet(confidence=0.45, status="NEED_VERIFICATION")
    footer = _format_footer(packet)
    
    assert "以上验证点基于紫微斗数经典规则生成，需要您的确认或补充信息。" in footer
    assert "建议逐项核对" in footer
    assert "1. 逐项核对验证点的描述与您的人生经历是否相符" in footer
    print("  ✅ NEED_VERIFICATION 页脚正确")


def test_format_footer_low_confidence():
    """测试 LOW_CONFIDENCE 状态的页脚"""
    print("\n[TEST] _format_footer - LOW_CONFIDENCE")
    packet = make_packet(confidence=0.25, status="LOW_CONFIDENCE")
    footer = _format_footer(packet)
    
    assert "当前命盘置信度较低" in footer
    assert "出生时间不准确（建议校正）" in footer
    assert "建议进行生时校正以提升准确性" in footer
    print("  ✅ LOW_CONFIDENCE 页脚正确")


def test_format_footer_calibration_done():
    """测试 CALIBRATION_DONE 状态的页脚"""
    print("\n[TEST] _format_footer - CALIBRATION_DONE")
    packet = make_packet(confidence=0.82, status="CALIBRATION_DONE")
    footer = _format_footer(packet)
    
    assert "系统已自动调整出生时间" in footer
    assert "核对调整后的命盘是否与您的人生经历相符" in footer
    print("  ✅ CALIBRATION_DONE 页脚正确")


def test_generate_verification_prompt_full():
    """测试完整提示词生成"""
    print("\n[TEST] generate_verification_prompt - full")
    packet = make_packet(
        confidence=0.72,
        status="NEED_VERIFICATION",
        verification_points=[
            make_verification_point(
                field="guanlu_gong.stars",
                category="官禄宫星曜组合",
                description="官禄宫紫微+天府，事业起飞明显（28-35岁）",
                impact="high",
                current_value="紫微:True, 天府:True",
                suggestions=["核对职业起点时间", "验证职位晋升记录"],
                related_fields=["guanlu_gong", "daxian_2"],
                age_range=[28, 35],
                confidence_weight=0.80
            ),
            make_verification_point(
                field="minggong.main_stars",
                category="命宫主星",
                description="命宫无主星（空宫），命盘稳定性低",
                impact="high",
                current_value="无主星",
                suggestions=["重点校验出生时间", "验证出生地点"],
                related_fields=["minggong", "birth_time"],
                age_range=[0, 0],
                confidence_weight=0.30
            )
        ],
        original_birth="1993-04-01T14:00:00+08:00",
        corrected_birth="1993-04-01T15:00:00+08:00",
        shift_hours=1.0,
        calibration_applied=True
    )
    
    prompt = generate_verification_prompt(packet)
    
    # 检查关键部分
    assert "【命盘校准状态报告】" in prompt
    assert "当前置信度：72.0%" in prompt
    assert "校准状态：⚠️ 待校验（需要您确认）" in prompt
    assert "原始出生时间：1993-04-01 14:00" in prompt
    assert "校正后时间：1993-04-01 15:00" in prompt
    assert "时间偏移：推后1.0时辰" in prompt
    assert "检测到的关键验证点：" in prompt
    assert "1. 【官禄宫星曜组合】" in prompt
    assert "2. 【命宫主星】" in prompt
    assert "影响年龄：28-35岁" in prompt
    assert "权重：0.80" in prompt
    assert "建议：" in prompt
    assert "• 核对职业起点时间" in prompt
    assert "【说明】" in prompt
    assert "【后续步骤】" in prompt
    assert "生成时间：" in prompt
    print("  ✅ 完整提示词生成正确")


def test_generate_verification_summary():
    """测试验证点摘要"""
    print("\n[TEST] generate_verification_summary")
    packet = make_packet(verification_points=[
        make_verification_point(impact="high"),
        make_verification_point(impact="high"),
        make_verification_point(impact="medium"),
        make_verification_point(impact="low")
    ])
    summary = generate_verification_summary(packet)
    
    assert "共4项" in summary
    assert "高影响2项" in summary
    assert "中影响1项" in summary
    assert "低影响1项" in summary
    print("  ✅ 摘要统计正确")


def test_generate_prompt_no_verification_points():
    """测试无验证点的情况"""
    print("\n[TEST] generate_verification_prompt - no points")
    packet = make_packet(confidence=0.8, status="SUCCESS", verification_points=[])
    prompt = generate_verification_prompt(packet)
    
    assert "未检测到需特别关注的验证点" in prompt
    assert "【说明】" in prompt
    print("  ✅ 无验证点处理正确")


def test_format_point_as_json():
    """测试 JSON 格式化输出"""
    print("\n[TEST] format_point_as_json")
    point = make_verification_point(
        field="test_field",
        description="test_desc",
        impact="high",
        confidence_weight=0.9
    )
    json_str = format_point_as_json(point)
    
    assert '"field": "test_field"' in json_str
    assert '"impact": "high"' in json_str
    assert "0.9" in json_str
    print("  ✅ JSON 格式化正确")


def test_invalid_packet_missing_field():
    """测试无效数据包（缺少必需字段）"""
    print("\n[TEST] generate_verification_prompt - invalid packet")
    try:
        generate_verification_prompt({"confidence": 0.5})  # 缺少 status
        assert False, "应抛出 ValueError"
    except ValueError as e:
        assert "缺少必需字段" in str(e)
        print("  ✅ 缺失字段检查正确")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("P3 提示词生成器单元测试")
    print("=" * 60)
    
    tests = [
        test_describe_confidence,
        test_format_header_success,
        test_format_header_calibration_done,
        test_format_header_need_verification,
        test_format_header_low_confidence,
        test_format_points_empty,
        test_format_points_single,
        test_format_points_multiple,
        test_format_footer_success,
        test_format_footer_need_verification,
        test_format_footer_low_confidence,
        test_format_footer_calibration_done,
        test_generate_verification_prompt_full,
        test_generate_verification_summary,
        test_generate_prompt_no_verification_points,
        test_format_point_as_json,
        test_invalid_packet_missing_field
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    return failed == 0


import sys

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
