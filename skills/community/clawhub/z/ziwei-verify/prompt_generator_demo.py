#!/usr/bin/env python3
"""
prompt_generator_demo.py - P3 提示词生成器演示

展示 generate_verification_prompt() 在不同场景下的输出效果
"""

import importlib.util
from pathlib import Path

# 直接加载 prompt_generator 模块（避免触发 __init__ 的循环导入）
spec = importlib.util.spec_from_file_location(
    "prompt_generator", 
    Path(__file__).resolve().parent / "prompt_generator.py"
)
pg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pg)

generate_verification_prompt = pg.generate_verification_prompt


def demo_success():
    """场景1：高置信度，无需校正"""
    print("\n" + "=" * 70)
    print("场景1：高置信度，无需校正 (SUCCESS, confidence=0.75)")
    print("=" * 70)
    
    packet = {
        "trace_id": "demo-001",
        "skill_name": "ziwei",
        "execution_time": 1.1,
        "timestamp": "2026-05-04T08:00:00+08:00",
        "status": "SUCCESS",
        "confidence": 0.75,
        "data": {"chart": "data"},
        "verification_points": [
            {
                "field": "fude_gong.stars",
                "category": "福德宫星曜",
                "description": "福德宫天同+天梁，家庭关系温和稳定",
                "impact": "medium",
                "current_value": "天同:True, 天梁:True",
                "suggestions": ["核对婚恋时间", "验证家庭重大决策年份"],
                "related_fields": ["fude_gong", "fuqi_gong"],
                "age_range": [25, 32],
                "confidence_weight": 0.65
            },
            {
                "field": "shengong.location",
                "category": "身宫位置",
                "description": "身宫在迁移宫，人生重心在外",
                "impact": "low",
                "current_value": "身宫在迁移宫",
                "suggestions": ["验证迁移相关经历"],
                "related_fields": ["shengong", "qianyi_gong"],
                "age_range": [0, 0],
                "confidence_weight": 0.05
            }
        ],
        "metadata": {}
    }
    
    print(generate_verification_prompt(packet))


def demo_calibration_done():
    """场景2：已自动校正，需要用户核对"""
    print("\n" + "=" * 70)
    print("场景2：已自动校正 (CALIBRATION_DONE, confidence=0.82)")
    print("=" * 70)
    
    packet = {
        "trace_id": "demo-002",
        "skill_name": "ziwei",
        "execution_time": 1.5,
        "timestamp": "2026-05-04T08:00:00+08:00",
        "status": "CALIBRATION_DONE",
        "confidence": 0.82,
        "data": {"chart": "data"},
        "verification_points": [
            {
                "field": "guanlu_gong.stars",
                "category": "官禄宫星曜组合",
                "description": "官禄宫紫微+天府，事业起飞明显（28-35岁）",
                "impact": "high",
                "current_value": "紫微:True, 天府:True",
                "suggestions": ["核对职业起点时间", "验证职位晋升记录"],
                "related_fields": ["guanlu_gong", "daxian_2"],
                "age_range": [28, 35],
                "confidence_weight": 0.80
            }
        ],
        "metadata": {
            "calibration_applied": True,
            "original_birth": "1993-04-01T14:00:00+08:00",
            "corrected_birth": "1993-04-01T15:00:00+08:00",
            "shift_hours": 1.0
        }
    }
    
    print(generate_verification_prompt(packet))


def demo_need_verification():
    """场景3：需要人工校验（交互模式）"""
    print("\n" + "=" * 70)
    print("场景3：需要人工校验 (NEED_VERIFICATION, confidence=0.45)")
    print("=" * 70)
    
    packet = {
        "trace_id": "demo-003",
        "skill_name": "ziwei",
        "execution_time": 1.2,
        "timestamp": "2026-05-04T08:00:00+08:00",
        "status": "NEED_VERIFICATION",
        "confidence": 0.45,
        "data": {"chart": "data"},
        "verification_points": [
            {
                "field": "minggong.main_stars",
                "category": "命宫主星",
                "description": "命宫无主星（空宫），命盘稳定性低，需校准时辰或地点",
                "impact": "high",
                "current_value": "无主星",
                "suggestions": ["重点校验出生时间", "验证出生地点经纬度", "考虑真太阳时调整"],
                "related_fields": ["minggong", "birth_time", "birth_location"],
                "age_range": [0, 0],
                "confidence_weight": 0.30
            },
            {
                "field": "jie_gong.hua+stars",
                "category": "疾厄宫四化+煞星",
                "description": "疾厄宫化忌+火星，注意健康隐患",
                "impact": "high",
                "current_value": "化忌:True, 火星:True",
                "suggestions": ["核对疾病发生时间", "验证体检异常记录"],
                "related_fields": ["jie_gong", "hua_map", "daxian_all"],
                "age_range": [0, 0],
                "confidence_weight": 0.70
            },
            {
                "field": "caibo_gong.stars",
                "category": "财帛宫星曜组合",
                "description": "财帛宫禄存+天马（禄马交驰），财富积累快",
                "impact": "high",
                "current_value": "禄存:True, 天马:True",
                "suggestions": ["核对资产积累关键年份", "验证投资/外快收入时间"],
                "related_fields": ["caibo_gong", "minggong", "daxian_3"],
                "age_range": [30, 40],
                "confidence_weight": 0.75
            }
        ],
        "metadata": {}
    }
    
    print(generate_verification_prompt(packet))


def demo_low_confidence():
    """场景4：低置信度，建议校正"""
    print("\n" + "=" * 70)
    print("场景4：低置信度 (LOW_CONFIDENCE, confidence=0.25)")
    print("=" * 70)
    
    packet = {
        "trace_id": "demo-004",
        "skill_name": "ziwei",
        "execution_time": 0.8,
        "timestamp": "2026-05-04T08:00:00+08:00",
        "status": "LOW_CONFIDENCE",
        "confidence": 0.25,
        "data": {"chart": "data"},
        "verification_points": [
            {
                "field": "birth_time",
                "category": "时辰交界",
                "description": "出生在子时（真太阳时敏感时段），需验证真太阳时校正",
                "impact": "high",
                "current_value": "23:30",
                "suggestions": ["计算出生地真太阳时", "验证太阳时调整后的命盘"],
                "related_fields": ["birth_time", "timezone", "longitude"],
                "age_range": [0, 0],
                "confidence_weight": 0.20
            }
        ],
        "metadata": {}
    }
    
    print(generate_verification_prompt(packet))


def demo_no_points():
    """场景5：无验证点（完美命盘）"""
    print("\n" + "=" * 70)
    print("场景5：无验证点 (SUCCESS, confidence=0.88)")
    print("=" * 70)
    
    packet = {
        "trace_id": "demo-005",
        "skill_name": "ziwei",
        "execution_time": 1.0,
        "timestamp": "2026-05-04T08:00:00+08:00",
        "status": "SUCCESS",
        "confidence": 0.88,
        "data": {"chart": "data"},
        "verification_points": [],
        "metadata": {}
    }
    
    print(generate_verification_prompt(packet))


if __name__ == "__main__":
    print("\n" + "🔮 紫微斗数提示词生成器 - 演示输出" + "\n")
    
    demo_success()
    demo_calibration_done()
    demo_need_verification()
    demo_low_confidence()
    demo_no_points()
    
    print("\n" + "=" * 70)
    print("演示结束")
    print("=" * 70)
