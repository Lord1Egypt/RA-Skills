# ================================ =======================
# scripts/question_generator.py - SPIN 问题序列生成器
# 目标：根据行业和产品自动生成 S/P/I/N 四阶段提问序列
# ================================ =======================

from typing import List, Dict


def generate_spin_questions(industry: str, product: str) -> Dict:
    """根据行业和产品生成 SPIN 提问序列
    
    Args:
        industry: 客户所在行业，如"物流"
        product:  销售的产品/服务，如"车队管理系统"
    
    Returns:
        包含各阶段问题列表的字典
    """
    spin_templates = {
        "situation": [
            f"在{industry}行业，贵公司目前如何使用{product}相关工具？",
            "现有的系统/流程是什么品牌或类型？使用多久了？",
            "团队规模和组织结构是怎样的？",
            "预算和时间表是怎样的？",
            "这个功能对贵组织的重要性程度如何？"
        ],
        "problem": [
            f"在处理{product}相关任务时，有哪些成本过高的问题？",
            f"对于当前的{product}流程，您是否满意？",
            "这些流程是否会失败或导致延误？",
            f"处理{product}相关任务的耗时程度如何？",
            "是否曾遇到过资源不足的情况？",
            f"关于当前{product}的做法，最让您感到挫败的是什么？"
        ],
        "implication": [
            f"如果{product}问题持续存在，对业务目标有什么影响？",
            "这个问题如何影响关键业务指标（如客户满意度、续约率）？",
            "如果不解决，会产生哪些连锁后果？",
            "谁会因此受到影响（团队其他成员、客户等）？",
            "是否可能引发合规或法律风险？",
            "如果持续发生，预计每年会增加多少额外成本？"
        ],
        "need_payoff": [
            f"如果实现了{product}理想状态，对团队意味着什么？",
            "拥有某功能如何改善当前的流程？",
            "这能为业务指标带来什么价值？",
            f"如果能解决当前问题，您会看到哪些改进？",
            "谁会从这个解决方案中受益最多？",
            "解决这个问题，对贵公司的优先级是怎样的？"
        ]
    }

    return {
        "industry": industry,
        "product": product,
        "questions_by_stage": spin_templates
    }


# 使用示例
if __name__ == "__main__":
    questions = generate_spin_questions("物流", "车队管理系统")
    print(f"行业: {questions['industry']}")
    print(f"产品: {questions['product']}")
    for stage, qs in questions["questions_by_stage"].items():
        print(f"\n[{stage.upper()}]")
        for i, q in enumerate(qs, 1):
            print(f"  {i}. {q}")
