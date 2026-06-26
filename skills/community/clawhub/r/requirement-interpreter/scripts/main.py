#!/usr/bin/env python3
"""
需求解读技能入口文件
提供命令行界面和API接口
"""

import sys
import json
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from optimized_interpreter import OptimizedRequirementInterpreter
from optimized_classifier import RequirementClassifier
from delivery_standards import DeliveryStandards


def print_delivery_checklist(checklist: dict):
    """打印交付物清单"""
    print("\n" + "=" * 60)
    print("📦 标准化交付物清单")
    print("=" * 60)
    
    print(f"\n📋 交付标准: {checklist['standard_name']}")
    
    print("\n【必需交付物】")
    for item in checklist['required_items']:
        formats = ", ".join(item['formats'])
        print(f"  ✓ {item['name']}")
        print(f"    描述: {item['description']}")
        print(f"    格式: {formats}")
        if item['notes']:
            print(f"    备注: {item['notes']}")
    
    print("\n【可选交付物】")
    for item in checklist['optional_items']:
        formats = ", ".join(item['formats'])
        print(f"  ○ {item['name']} ({formats})")
    
    print("\n【验收检查清单】")
    for i, check in enumerate(checklist['validation_checklist'], 1):
        print(f"  □ {check}")
    
    print(f"\n📖 使用指南: {checklist['usage_guide']}")


def main():
    """主入口函数"""
    if len(sys.argv) < 2:
        print("用法: python main.py <需求描述>")
        print("示例: python main.py \"请帮我设计一个蛋糕促销海报\"")
        sys.exit(1)
    
    requirement_text = sys.argv[1]
    
    # 初始化解读器
    case_library_path = script_dir / "case_library.json"
    interpreter = OptimizedRequirementInterpreter(str(case_library_path))
    
    # 解读需求
    result = interpreter.interpret_requirement(requirement_text)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("📋 需求解读结果")
    print("=" * 60)
    
    print(f"\n🎯 需求类型: {result['classification'].primary_type.value}")
    print(f"📂 二级分类: {result['classification'].secondary_type}")
    print(f"📊 置信度: {result['classification'].confidence:.2%}")
    print(f"🏢 行业背景: {result['classification'].context.industry}")
    print(f"⚡ 紧急程度: {result['classification'].context.urgency.value}")
    print(f"📈 复杂度: {result['classification'].context.complexity.value}")
    
    print(f"\n🧭 推荐思考维度 ({len(result['dimensions'])}):")
    for dim in result['dimensions'][:6]:
        print(f"  - {dim}")
    
    print(f"\n📚 相似案例 ({len(result['similar_cases'])}):")
    for case in result['similar_cases'][:3]:
        print(f"  - {case.title}")
    
    print(f"\n❓ 建议访谈问题 ({len(result['interview_plan']['questions'])}):")
    for q in result['interview_plan']['questions'][:3]:
        print(f"  - {q}")
    
    # 生成交付物清单
    requirement_type = result['classification'].primary_type.value
    secondary_type = result['classification'].secondary_type
    delivery_checklist = DeliveryStandards.generate_delivery_checklist(
        requirement_type, 
        secondary_type,
        requirement_text
    )
    print_delivery_checklist(delivery_checklist)
    
    print()


if __name__ == "__main__":
    main()
