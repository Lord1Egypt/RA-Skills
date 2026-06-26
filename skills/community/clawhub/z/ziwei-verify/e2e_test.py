#!/usr/bin/env python3
"""
ziwei_verify 端到端测试套件

测试范围：
1. 正常排盘（SUCCESS状态）→ 验证无提示词
2. 需要校正（NEED_VERIFICATION状态）→ 验证提示词生成
3. 低置信度（LOW_CONFIDENCE状态）→ 验证提示词内容
4. 完整流程：ziwei.arrange_with_packet() → ziwei_verify.calibrate() → interpret_with_packet()
"""

import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# 确保工作区在路径中
WORKSPACE = Path('/home/caojy/.openclaw/workspace')
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / 'skills'))
sys.path.insert(0, str(WORKSPACE / 'skills' / 'ziwei_interpret'))

from ziwei_verify.main import run as verify_run
from ziwei_verify.prompt_generator import generate_verification_prompt

# 尝试导入 ziwei 技能（如果可用）
try:
    from ziwei.skills import arrange_with_packet
    HAS_ZIWEI = True
except ImportError:
    HAS_ZIWEI = False
    print("⚠️  ziwei 技能不可用，将使用模拟数据")


def create_mock_packet(status="SUCCESS", confidence=0.8, has_verification=True):
    """创建模拟的 StandardDataPacket"""
    verification_points = []
    if has_verification:
        verification_points = [
            {
                "field": "命宫主星",
                "category": "宫位星曜组合",
                "description": "命宫主星需进一步确认",
                "impact": "high",
                "current_value": "紫微+贪狼",
                "suggestions": ["核对出生时间", "提供出生地点经纬度"],
                "related_fields": ["身宫", "迁移宫"],
                "age_range": [25, 45],
                "confidence_weight": 0.8
            },
            {
                "field": "迁移宫四化",
                "category": "四化星曜",
                "description": "迁移宫四化影响外出运势",
                "impact": "medium",
                "current_value": "武曲化忌",
                "suggestions": ["谨慎外出", "避开凶方"],
                "related_fields": ["事业宫", "财帛宫"],
                "age_range": [20, 50],
                "confidence_weight": 0.6
            }
        ]
    
    return {
        "trace_id": "test_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
        "skill_name": "ziwei",
        "execution_time": 0.5,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status,
        "confidence": confidence,
        "data": {
            "birth_info": {
                "gender": "M",
                "birth_dt": "1990-05-15T14:30:00+08:00",
                "location": "北京"
            },
            "chart_data": {}
        },
        "verification_points": verification_points,
        "errors": [],
        "warnings": [],
        "metadata": {}
    }


def test_case_1_success_no_prompt():
    """测试用例1：高置信度自动校正（CALIBRATION_DONE状态）→ 验证无提示词"""
    print("\n" + "="*60)
    print("测试用例1：高置信度自动校正（CALIBRATION_DONE状态）")
    print("="*60)
    
    packet = create_mock_packet(
        status="SUCCESS",
        confidence=0.85,  # 高置信度
        has_verification=True  # 有验证点，但会被自动校正解决
    )
    
    start = time.time()
    result = verify_run(
        action="calibrate",
        packet=packet,
        birth_dt="1990-05-15T14:30:00+08:00",
        max_shifts=2,
        interactive=False
    )
    elapsed = time.time() - start
    
    print(f"⏱️  耗时：{elapsed:.3f}秒")
    print(f"状态：{result.get('status')}")
    print(f"置信度：{result.get('confidence', 0):.1%}")
    
    # 验证：高置信度应自动校正为 CALIBRATION_DONE
    assert result["status"] in ("CALIBRATION_DONE", "SUCCESS"), f"期望 CALIBRATION_DONE/SUCCESS，实际 {result['status']}"
    # 已校正的状态不应生成提示词（或提示词为None）
    assert result.get("verification_prompt") is None, \
        f"CALIBRATION_DONE 状态不应生成提示词"
    
    print("✅ 测试通过：CALIBRATION_DONE 状态无提示词")
    return True


def test_case_2_need_verification():
    """测试用例2：需要校正（交互模式 NEED_VERIFICATION状态）→ 验证提示词生成"""
    print("\n" + "="*60)
    print("测试用例2：交互模式（NEED_VERIFICATION状态）")
    print("="*60)
    
    packet = create_mock_packet(
        status="NEED_VERIFICATION",
        confidence=0.45,
        has_verification=True
    )
    
    start = time.time()
    result = verify_run(
        action="calibrate",
        packet=packet,
        birth_dt="1990-05-15T14:30:00+08:00",
        max_shifts=2,
        interactive=True  # 交互模式才会返回 NEED_VERIFICATION
    )
    elapsed = time.time() - start
    
    print(f"⏱️  耗时：{elapsed:.3f}秒")
    print(f"状态：{result.get('status')}")
    print(f"置信度：{result.get('confidence', 0):.1%}")
    
    # 验证
    assert result["status"] == "NEED_VERIFICATION", \
        f"期望 NEED_VERIFICATION，实际 {result['status']}"
    assert "verification_prompt" in result, "应包含 verification_prompt 字段"
    assert result["verification_prompt"] is not None, "verification_prompt 不应为 None"
    assert isinstance(result["verification_prompt"], str), "verification_prompt 应为字符串"
    assert len(result["verification_prompt"]) > 0, "提示词不应为空"
    
    # 检查提示词内容
    prompt = result["verification_prompt"]
    print(f"\n📝 提示词预览（前200字）：\n{prompt[:200]}...")
    
    # 应包含关键部分
    assert "【命盘校准状态报告】" in prompt, "应包含标题"
    assert "验证点" in prompt, "应包含验证点说明"
    assert "置信度" in prompt, "应包含置信度信息"
    
    print("✅ 测试通过：NEED_VERIFICATION 状态生成了有效提示词")
    return True


def test_case_3_low_confidence():
    """测试用例3：低置信度（LOW_CONFIDENCE状态）→ 验证提示词生成"""
    print("\n" + "="*60)
    print("测试用例3：低置信度（LOW_CONFIDENCE状态）")
    print("="*60)
    
    packet = create_mock_packet(
        status="LOW_CONFIDENCE",
        confidence=0.35,
        has_verification=True
    )
    
    start = time.time()
    result = verify_run(
        action="calibrate",
        packet=packet,
        birth_dt="1990-05-15T14:30:00+08:00",
        max_shifts=2,
        interactive=False
    )
    elapsed = time.time() - start
    
    print(f"⏱️  耗时：{elapsed:.3f}秒")
    print(f"状态：{result.get('status')}")
    print(f"置信度：{result.get('confidence', 0):.1%}")
    
    # 验证：应该保持 LOW_CONFIDENCE
    assert result["status"] == "LOW_CONFIDENCE", \
        f"期望 LOW_CONFIDENCE，实际 {result['status']}"
    assert "verification_prompt" in result, "应包含 verification_prompt 字段"
    assert result["verification_prompt"] is not None, "verification_prompt 不应为 None"
    
    prompt = result["verification_prompt"]
    print(f"\n📝 提示词预览（前200字）：\n{prompt[:200]}...")
    
    # 低置信度应包含建议
    assert "建议" in prompt or "后续步骤" in prompt, "应包含建议或后续步骤"
    assert "校正" in prompt or "出生时间" in prompt, "应提及校正或出生时间"
    
    print("✅ 测试通过：LOW_CONFIDENCE 状态提示词内容正确")
    return True


def test_case_4_full_flow():
    """测试用例4：完整流程（如ziwei可用）"""
    print("\n" + "="*60)
    print("测试用例4：完整流程（ziwei → ziwei_verify → ziwei_interpret）")
    print("="*60)
    
    if not HAS_ZIWEI:
        print("⏭️  跳过：ziwei 技能不可用")
        return True
    
    try:
        from ziwei.skills import arrange_with_packet
        from ziwei_interpret import interpret_with_packet
        
        # 步骤1：排盘
        print("步骤1：调用 ziwei.arrange_with_packet()...")
        start = time.time()
        packet = arrange_with_packet(
            gender="M",
            birth_dt="1990-05-15T14:30:00+08:00",
            location="北京"
        )
        t1 = time.time() - start
        print(f"  耗时：{t1:.3f}秒")
        print(f"  状态：{packet.get('status')}，置信度：{packet.get('confidence', 0):.1%}")
        
        # 步骤2：校正
        print("\n步骤2：调用 ziwei_verify.calibrate()...")
        start = time.time()
        verified = verify_run(
            action="calibrate",
            packet=packet,
            birth_dt="1990-05-15T14:30:00+08:00",
            max_shifts=2,
            interactive=False
        )
        t2 = time.time() - start
        print(f"  耗时：{t2:.3f}秒")
        print(f"  状态：{verified.get('status')}，置信度：{verified.get('confidence', 0):.1%}")
        
        # 步骤3：解读
        print("\n步骤3：调用 ziwei_interpret.interpret_with_packet()...")
        start = time.time()
        report = interpret_with_packet(verified, format_output=True)
        t3 = time.time() - start
        print(f"  耗时：{t3:.3f}秒")
        print(f"  报告长度：{len(report)} 字符")
        
        total = t1 + t2 + t3
        print(f"\n📊 总耗时：{total:.3f}秒")
        
        # 验证
        assert verified.get("verification_prompt") is not None, "应生成提示词"
        assert len(report) > 0, "报告不应为空"
        assert "命盘" in report or "解读" in report, "报告应包含解读内容"
        
        if total > 3.0:
            print(f"⚠️  注意：总耗时 {total:.3f}秒 超过 3 秒阈值")
        else:
            print(f"✅ 性能达标：总耗时 {total:.3f}秒 < 3 秒")
        
        print("✅ 完整流程测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 完整流程测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试用例"""
    print("\n" + "="*60)
    print("🎯 紫微斗数 P4 端到端测试套件")
    print(f"启动时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = []
    tests = [
        ("SUCCESS 无提示词", test_case_1_success_no_prompt),
        ("NEED_VERIFICATION 提示词生成", test_case_2_need_verification),
        ("LOW_CONFIDENCE 提示词内容", test_case_3_low_confidence),
        ("完整流程", test_case_4_full_flow),
    ]
    
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed, None))
        except Exception as e:
            print(f"❌ 测试失败：{e}")
            import traceback
            traceback.print_exc()
            results.append((name, False, str(e)))
    
    # 汇总
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    passed_count = 0
    for name, passed, error in results:
        status = "✅ 通过" if passed else f"❌ 失败: {error}"
        print(f"  {name}: {status}")
        if passed:
            passed_count += 1
    
    print(f"\n总计：{passed_count}/{len(results)} 通过")
    
    if passed_count == len(results):
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  存在失败的测试，请检查")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
