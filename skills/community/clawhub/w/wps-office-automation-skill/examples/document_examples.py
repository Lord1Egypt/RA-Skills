"""
使用示例：文档处理
"""

import asyncio
import base64
from main import execute


async def example_generate_notice():
    """示例：生成通知公文"""
    params = {
        "action": "生成通知公文",
        "action_type": "generate_document",
        "doc_type": "notice",
        "title": "关于开展2026年度工作总结的通知",
        "subject": "为全面总结2026年度工作成果，请各部门于12月31日前提交年度工作总结报告",
        "keywords": ["年度总结", "工作汇报", "绩效考核"],
        "recipient": "各部门",
        "sender": "公司办公室",
        "date": "2026年3月16日"
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        
        file_data = base64.b64decode(result["file_data"])
        with open("通知.docx", "wb") as f:
            f.write(file_data)
        print(f"✓ 文件已保存: {result['file_name']}")
    else:
        print(f"✗ 失败: {result['message']}")


async def example_generate_report():
    """示例：生成报告"""
    params = {
        "action": "生成工作报告",
        "action_type": "generate_document",
        "doc_type": "report",
        "title": "2026年第一季度市场拓展工作报告",
        "subject": "本报告总结了第一季度市场拓展工作的主要成果、存在问题及下一步计划",
        "keywords": ["市场拓展", "客户开发", "销售业绩"],
    }
    
    result = await execute(params)
    
    if result["success"]:
        file_data = base64.b64decode(result["file_data"])
        with open("工作报告.docx", "wb") as f:
            f.write(file_data)
        print(f"✓ 报告生成成功")


async def example_polish_document():
    """示例：文档润色"""
    params = {
        "action": "润色文档",
        "action_type": "polish_document",
        "content": """
        这个项目我们做得挺好的，团队里的每个人都很努力。
        虽然中间遇到了一些问题，但是最后都解决了。
        客户对我们的工作也比较满意。
        """,
        "style": "formal",
        "preserve_structure": True
    }
    
    result = await execute(params)
    
    if result["success"]:
        print("润色前:")
        print(params["content"])
        print("\n润色后:")
        print(result["data"]["polished_content"])


async def example_review_contract():
    """示例：合同审查"""
    contract_content = """
    甲方：XX科技有限公司
    乙方：YY咨询公司
    
    第一条：乙方应在合同签订后5个工作日内完成全部服务。
    
    第二条：甲方应支付乙方服务费用100万元，违约金为合同总额的50%。
    
    第三条：本合同为独家合作协议，甲方在合同期内不得委托第三方提供类似服务。
    
    第四条：本合同自动续约，除非一方提前30天书面通知不续约。
    
    第五条：本合同不可撤销，双方应严格履行合同义务。
    """
    
    params = {
        "action": "审查合同",
        "action_type": "review_contract",
        "content": contract_content
    }
    
    result = await execute(params)
    
    if result["success"]:
        print(f"审查摘要: {result['data']['summary']}")
        print(f"风险评分: {result['data']['risk_score']}/100")
        print("\n风险条款:")
        for item in result['data']['risk_items']:
            print(f"  - {item['keyword']}: {item['suggestion']}")
        print("\n修改建议:")
        for suggestion in result['data']['suggestions']:
            print(f"  • {suggestion}")


async def main():
    """运行所有示例"""
    print("=" * 60)
    print("示例1: 生成通知公文")
    print("=" * 60)
    await example_generate_notice()
    
    print("\n" + "=" * 60)
    print("示例2: 生成工作报告")
    print("=" * 60)
    await example_generate_report()
    
    print("\n" + "=" * 60)
    print("示例3: 文档润色")
    print("=" * 60)
    await example_polish_document()
    
    print("\n" + "=" * 60)
    print("示例4: 合同审查")
    print("=" * 60)
    await example_review_contract()


if __name__ == "__main__":
    asyncio.run(main())
