"""
完整功能测试
测试所有模块的核心功能
"""

import asyncio
import sys
import base64
from pathlib import Path
import pandas as pd
from io import BytesIO

sys.path.insert(0, str(Path(__file__).parent))

from main import execute


async def test_document_module():
    """测试文档处理模块"""
    print("\n" + "="*60)
    print("测试文档处理模块")
    print("="*60)
    
    tests_passed = 0
    tests_total = 3
    
    # 测试1: 公文生成
    print("\n1. 公文生成测试")
    result = await execute({
        "action": "生成通知公文",
        "action_type": "generate_document",
        "doc_type": "notice",
        "title": "关于开展年度工作总结的通知",
        "subject": "请各部门于12月31日前提交年度工作总结报告",
        "keywords": ["年度总结", "工作汇报"],
        "recipient": "各部门",
        "sender": "办公室",
        "date": "2026年3月16日"
    })
    
    if result["success"] and "file_data" in result:
        print("  ✓ 公文生成成功")
        doc_bytes = base64.b64decode(result["file_data"])
        print(f"  ✓ 文件大小: {len(doc_bytes)} bytes")
        tests_passed += 1
    else:
        print(f"  ✗ 公文生成失败: {result.get('message', 'Unknown error')}")
    
    # 测试2: 文档润色
    print("\n2. 文档润色测试")
    result = await execute({
        "action": "润色文档",
        "action_type": "polish_document",
        "content": "这个项目做得挺好的，大家都很努力。",
        "style": "formal"
    })
    
    if result["success"] and "polished_content" in result.get("data", {}):
        print("  ✓ 文档润色成功")
        print(f"  ✓ 润色后内容: {result['data']['polished_content'][:50]}...")
        tests_passed += 1
    else:
        print(f"  ✗ 文档润色失败")
    
    # 测试3: 合同审查
    print("\n3. 合同审查测试")
    result = await execute({
        "action": "审查合同",
        "action_type": "review_contract",
        "content": "本合同违约金为合同总额的50%，且不可撤销。双方独家合作，自动续约。"
    })
    
    if result["success"] and "risk_score" in result.get("data", {}):
        print("  ✓ 合同审查成功")
        print(f"  ✓ 风险评分: {result['data']['risk_score']}/100")
        print(f"  ✓ 风险条款数: {len(result['data']['risk_items'])}")
        tests_passed += 1
    else:
        print(f"  ✗ 合同审查失败")
    
    print(f"\n文档模块测试结果: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


async def test_spreadsheet_module():
    """测试表格处理模块"""
    print("\n" + "="*60)
    print("测试表格处理模块")
    print("="*60)
    
    tests_passed = 0
    tests_total = 3
    
    # 创建测试数据
    df = pd.DataFrame({
        '地区': ['华东', '华北', '华东', '华南', '华北'],
        '销售额': [100000, 80000, 120000, 90000, 85000],
        '成本': [60000, 50000, 70000, 55000, 52000]
    })
    
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = base64.b64encode(excel_buffer.getvalue()).decode('utf-8')
    
    # 测试1: 数据清洗
    print("\n1. 数据清洗测试")
    result = await execute({
        "action": "清洗数据",
        "action_type": "clean_data",
        "data": excel_data,
        "remove_duplicates": True,
        "handle_missing": "mean"
    })
    
    if result["success"]:
        print("  ✓ 数据清洗成功")
        print(f"  ✓ 原始行数: {result['data']['original_rows']}")
        print(f"  ✓ 清洗后行数: {result['data']['cleaned_rows']}")
        tests_passed += 1
    else:
        print(f"  ✗ 数据清洗失败")
    
    # 测试2: 数据分析
    print("\n2. 数据分析测试")
    result = await execute({
        "action": "分析表格",
        "action_type": "analyze_data",
        "analysis_type": "sum",
        "data": excel_data,
        "columns": ["销售额", "成本"],
        "group_by": "地区"
    })
    
    if result["success"] and "data" in result:
        print("  ✓ 数据分析成功")
        print(f"  ✓ 分析类型: {result['data']['analysis_type']}")
        tests_passed += 1
    else:
        print(f"  ✗ 数据分析失败")
    
    # 测试3: 图表生成
    print("\n3. 图表生成测试")
    result = await execute({
        "action": "生成图表",
        "action_type": "generate_chart",
        "chart_type": "bar",
        "data": excel_data,
        "x_column": "地区",
        "y_columns": ["销售额"],
        "title": "销售分析"
    })
    
    if result["success"] and "file_data" in result:
        print("  ✓ 图表生成成功")
        chart_bytes = base64.b64decode(result["file_data"])
        print(f"  ✓ 图表文件大小: {len(chart_bytes)} bytes")
        tests_passed += 1
    else:
        print(f"  ✗ 图表生成失败")
    
    print(f"\n表格模块测试结果: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


async def test_presentation_module():
    """测试演示处理模块"""
    print("\n" + "="*60)
    print("测试演示处理模块")
    print("="*60)
    
    tests_passed = 0
    tests_total = 2
    
    # 测试1: PPT大纲生成
    print("\n1. PPT大纲生成测试")
    result = await execute({
        "action": "生成PPT大纲",
        "action_type": "generate_ppt_outline",
        "topic": "2026年度工作计划",
        "slide_count": 8,
        "key_points": ["市场拓展", "产品研发", "团队建设"]
    })
    
    if result["success"] and "slides" in result.get("data", {}):
        print("  ✓ PPT大纲生成成功")
        print(f"  ✓ 幻灯片数量: {len(result['data']['slides'])}")
        tests_passed += 1
    else:
        print(f"  ✗ PPT大纲生成失败")
    
    # 测试2: 创建演示文稿
    print("\n2. 创建演示文稿测试")
    result = await execute({
        "action": "创建PPT",
        "action_type": "create_presentation",
        "outline": {
            "title": "测试演示",
            "slides": [
                {"title": "标题页", "content": ["测试内容"], "layout_type": "title"},
                {"title": "内容页", "content": ["要点1", "要点2"], "layout_type": "title_content"}
            ]
        },
        "style": "business"
    })
    
    if result["success"] and "file_data" in result:
        print("  ✓ 演示文稿创建成功")
        ppt_bytes = base64.b64decode(result["file_data"])
        print(f"  ✓ 文件大小: {len(ppt_bytes)} bytes")
        tests_passed += 1
    else:
        print(f"  ✗ 演示文稿创建失败")
    
    print(f"\n演示模块测试结果: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


async def test_intent_parsing():
    """测试意图解析"""
    print("\n" + "="*60)
    print("测试意图解析")
    print("="*60)
    
    from main import IntentParser, ActionType
    
    tests_passed = 0
    tests_total = 10
    
    test_cases = [
        ("生成一份通知公文", ActionType.GENERATE_DOCUMENT),
        ("润色文档内容", ActionType.POLISH_DOCUMENT),
        ("审查这份合同", ActionType.REVIEW_CONTRACT),
        ("清洗数据", ActionType.CLEAN_DATA),
        ("分析表格数据", ActionType.ANALYZE_DATA),
        ("生成图表", ActionType.GENERATE_CHART),
        ("生成PPT大纲", ActionType.GENERATE_PPT_OUTLINE),
        ("PDF转Word", ActionType.CONVERT_PDF),
        ("提取PDF内容", ActionType.EXTRACT_PDF),
        ("合并PDF文件", ActionType.MERGE_PDF),
    ]
    
    for instruction, expected_action in test_cases:
        result = IntentParser.parse(instruction)
        if result == expected_action:
            print(f"  [OK] '{instruction}' -> {result.value}")
            tests_passed += 1
        else:
            print(f"  [FAIL] '{instruction}' 解析失败")
    
    print(f"\n意图解析测试结果: {tests_passed}/{tests_total} 通过")
    return tests_passed, tests_total


async def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("WPS Office Automation Skill - 完整功能测试")
    print("="*60)
    
    total_passed = 0
    total_tests = 0
    
    # 测试意图解析
    passed, total = await test_intent_parsing()
    total_passed += passed
    total_tests += total
    
    # 测试文档模块
    passed, total = await test_document_module()
    total_passed += passed
    total_tests += total
    
    # 测试表格模块
    passed, total = await test_spreadsheet_module()
    total_passed += passed
    total_tests += total
    
    # 测试演示模块
    passed, total = await test_presentation_module()
    total_passed += passed
    total_tests += total
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    print(f"总测试数: {total_tests}")
    print(f"通过数: {total_passed}")
    print(f"失败数: {total_tests - total_passed}")
    print(f"通过率: {total_passed/total_tests*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n✓ 所有测试通过！")
    else:
        print(f"\n! 有 {total_tests - total_passed} 个测试失败")


if __name__ == "__main__":
    asyncio.run(main())
