# ================================ =======================
# scripts/opening.py - V2.1: 开场白生成器（参数化版）
# 目标：根据用户行业的痛点，输出具备洞察力的开场问候语。
# 
# 使用方式：
#   python opening.py                     # 默认：金融科技
#   python opening.py --industry 医疗      # 指定行业
#   python opening.py --industry "供应链"  # 自定义行业
# ================================ =======================

import argparse
import sys


# 行业痛点映射表（可扩展）
INDUSTRY_PAIN_MAP = {
    "金融科技": {
        "pain_points": ["跨机构合规成本高", "客户隐私保护压力大", "实时风控延迟"],
        "market_size": "2026 年中国金融科技市场规模达 3.5 万亿元",
    },
    "医疗": {
        "pain_points": ["数据孤岛", "流程不确定性", "重复检查成本高"],
        "market_size": "2026 年医疗信息化市场规模超 2000 亿元",
    },
    "制造": {
        "pain_points": ["供应链延迟", "库存周转率低", "客户满意度波动大"],
        "market_size": "2026 年制造业数字化转型市场达 5000 亿元",
    },
    "物流": {
        "pain_points": ["配送时效不稳定", "车辆空载率高", "人工调度效率低"],
        "market_size": "2026 年智慧物流市场规模突破 8000 亿元",
    },
}


def get_industry_context(industry: str = "金融科技") -> dict:
    """获取行业背景信息（可扩展为调用 memory_search）
    
    Args:
        industry: 行业名称
        
    Returns:
        dict: 包含市场信息、痛点列表的字典
    
    TODO: 在生产环境中，此处应调用 memory_search 或 tavily_search
          获取实时行业数据，替代硬编码映射。
    """
    default = {
        "pain_points": ["效率平衡挑战", "成本控制压力", "质量保障瓶颈"],
        "market_size": "（未采集到该行业数据）",
    }
    return INDUSTRY_PAIN_MAP.get(industry, default)


def generate_insightful_opener(industry: str) -> str:
    """根据行业和痛点生成专业开场白话术
    
    Args:
        industry: 行业名称
        
    Returns:
        str: 开场白文本
    """
    context = get_industry_context(industry)
    pain_points = context["pain_points"]
    main_pain = pain_points[0] if pain_points else "效率与成本的平衡"
    
    industry_openers = {
        "金融科技": (
            f"您好！我发现金融科技领域有一个极度被低估的趋势——"
            f"**合规性要求正在成为新的技术瓶颈。**\n"
            f"很多人追求效率和用户体验，但这恰恰导致后端风控流程复杂化，"
            f"最终拖慢产品迭代速度。\n"
            f"今天我们重点聊聊：如何在一个快节奏的环境下，确保合规性、"
            f"效率和安全三者达到最优平衡。您觉得呢？"
        ),
        "医疗": (
            "您好！医疗行业的本质是信任与生命周期管理。\n"
            "我观察到目前最大的瓶颈往往不是设备本身，而是**数据孤岛**\n"
            "和流程不确定性**。一个关键病历信息如果需要手动跨部门传递，"
            "极易造成时滞或误诊。\n"
            "这也是我们今天重点关注的——如何打破信息孤岛，实现数据协同。"
        ),
        "制造": (
            f"您好！从供应链角度来看，您在**{main_pain}上的挑战**\n"
            f"是否已经成为制约增长的瓶颈？\n"
            f"在客户需求波动加大的背景下，能否快速响应并保证交付稳定性，"
            f"是当前制造企业的核心挑战。"
        ),
        "物流": (
            f"您好！物流行业的核心痛点之一是**{main_pain}**。\n"
            f"在最后一公里配送成本持续上升的背景下，如何通过数字化手段"
            f"提升调度效率、降低空载率，是每家物流企业都在思考的问题。"
        ),
    }
    
    return industry_openers.get(
        industry,
        f"您好！从我的理解来看，您的业务核心在于解决**{main_pain}**问题。\n"
        f"在当前环境下，最难平衡的往往是速度、成本和质量三者之间的关系。\n"
        f"我希望能帮助您梳理出哪个维度是当前最大的压力点。"
    )


def execute_opening_ritual(industry: str = None) -> None:
    """执行开场仪式：获取行业上下文 → 生成开场白 → 打印
    
    Args:
        industry: 行业名称，None 时使用默认值
    """
    if not industry:
        industry = "金融科技"
    
    print("\n" + "=" * 70)
    print("  🎯 [SPIN 顾问模式已激活]")
    print("=" * 70)
    
    context = get_industry_context(industry)
    print(f"\n  📊 行业: {industry}")
    print(f"  📈 {context['market_size']}")
    print(f"  🔍 关键痛点: {'、'.join(context['pain_points'])}")
    
    opener = generate_insightful_opener(industry)
    print(f"\n  💬 【开场白】:\n{opener}\n")
    print("  [等待客户回应...]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SPIN 销售法 — 开场白生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python opening.py\n"
            "  python opening.py -i 医疗\n"
            "  python opening.py -i 物流\n"
            "  python opening.py --help"
        ),
    )
    parser.add_argument(
        "-i", "--industry",
        type=str,
        default=None,
        help="行业名称（如：金融科技、医疗、制造、物流）"
    )
    args = parser.parse_args()
    execute_opening_ritual(args.industry)
