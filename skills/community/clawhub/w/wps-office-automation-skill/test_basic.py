"""
基础测试文件
验证Skill核心功能
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from main import execute


async def test_document_generation():
    """测试文档生成"""
    print("测试1: 文档生成")
    result = await execute({
        "action": "生成通知公文",
        "action_type": "generate_document",
        "doc_type": "notice",
        "title": "测试通知",
        "subject": "这是一个测试通知",
    })
    
    assert result["success"] == True
    assert "file_data" in result
    print("[OK] 文档生成测试通过")


async def test_document_polish():
    """测试文档润色"""
    print("\n测试2: 文档润色")
    result = await execute({
        "action": "润色文档",
        "action_type": "polish_document",
        "content": "这个项目做得挺好的",
        "style": "formal"
    })
    
    assert result["success"] == True
    assert "polished_content" in result["data"]
    print("[OK] 文档润色测试通过")


async def test_contract_review():
    """测试合同审查"""
    print("\n测试3: 合同审查")
    result = await execute({
        "action": "审查合同",
        "action_type": "review_contract",
        "content": "本合同违约金为合同总额的50%，且不可撤销。"
    })
    
    assert result["success"] == True
    assert "risk_score" in result["data"]
    print("[OK] 合同审查测试通过")


async def test_ppt_outline():
    """测试PPT大纲生成"""
    print("\n测试4: PPT大纲生成")
    result = await execute({
        "action": "生成PPT大纲",
        "action_type": "generate_ppt_outline",
        "topic": "测试演示",
        "slide_count": 5
    })
    
    assert result["success"] == True
    assert "slides" in result["data"]
    print("[OK] PPT大纲生成测试通过")


async def test_intent_parsing():
    """测试意图解析"""
    print("\n测试5: 意图解析")
    
    from main import IntentParser, ActionType
    
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
        assert result == expected_action, f"意图解析失败: {instruction}"
        
    print("[OK] 意图解析测试通过")


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("开始运行基础测试")
    print("=" * 60)
    
    try:
        await test_intent_parsing()
        await test_document_generation()
        await test_document_polish()
        await test_contract_review()
        await test_ppt_outline()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] 所有测试通过")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n[FAIL] 测试失败: {str(e)}")
    except Exception as e:
        print(f"\n[ERROR] 测试异常: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
