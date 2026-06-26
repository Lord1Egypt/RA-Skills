# ================================ =======================
# scripts/demo_interview.py - State Machine v2.0
# 目标：实现完整的 SPIN 四阶段流程控制，监控对话进度并生成行动计划
# ================================ =======================

from enum import Enum
import json
import time

class InterviewStage(Enum):
    OPENING = "Opening（开场）"
    INVESTIGATING = "Investigating（调查）"
    DEMONSTRATING = "Demonstrating Capability（展示能力）"
    COMMITTING = "Obtaining Commitment（获得承诺）"

class SpinStateMachine:
    def __init__(self):
        self.stage = InterviewStage.OPENING
        self.keywords = {
            "S": ["目前", "怎么做的", "流程", "系统名称"],
            "P": ["不满足", "麻烦", "困难", "效率", "成本", "问题"],
            "I": ["怎么办", "更严重", "担心", "影响", "风险", "后果"],
            "N": ["如果", "能", "带来价值", "好处", "改进"]
        }
        self.situation_count = 0
        self.problem_count = 0
        self.implication_count = 0
        self.need_payoff_count = 0
    
    def get_situation_question(self, industry: str):
        """生成背景问题（Situation Questions）"""
        return [
            f"在{industry}行业，贵公司目前如何使用相关工具？",
            "现有的系统/流程是什么品牌或类型？使用多久了？",
            "团队规模和组织结构是怎样的？",
            "预算和时间表是怎样的？"
        ]
    
    def get_problem_question(self, industry: str):
        """生成难题问题（Problem Questions）"""
        return [
            f"在处理{industry}相关任务时，有哪些成本过高的问题？",
            "对于当前的流程，您是否满意？",
            "这些流程是否会失败或导致延误？"
        ]
    
    def get_implication_question(self, industry: str):
        """生成影响问题（Implication Questions）"""
        return [
            f"如果{industry}问题持续存在，对业务目标有什么影响？",
            "这个问题如何影响关键业务指标？",
            "如果不解决，会产生哪些连锁后果？"
        ]
    
    def get_need_payoff_question(self, industry: str):
        """生成需求效益问题（Need-Payoff Questions）"""
        return [
            f"如果实现了{industry}理想状态，对团队意味着什么？",
            "这能带来哪些改进？",
            "解决这个问题对您来说优先级如何？"
        ]
    
    def check_and_redirect(self, client_speaking_time: float):
        """80/20 法则检查"""
        if client_speaking_time < 70:
            print("\n⚠️ [监控]: 客户发言时间不足，将进入下一个阶段")
            return True  # 需要转换阶段
        return False
    
    def generate_action_plan(self) -> dict:
        """生成 SMART 原则行动计划"""
        return {
            "milestones": [
                {"phase": "试点项目", "timeline": "1-2 周"},
                {"phase": "全面实施", "timeline": "3-6 个月"}
            ],
            "success_criteria": "客户满意度 >4.5/5, NPS >70",
            "key_deliverables": [
                "需求分析报告",
                "实施方案文档",
                "培训材料"
            ]
        }

# 使用示例
if __name__ == "__main__":
    print("="*80)
    print("🎯 SPIN 销售法对话模拟")
    print("="*80)
    
    sm = SpinStateMachine()
    industry = "供应链管理"
    
    print(f"\n【阶段{sm.stage.value}】")
    print("-"*40)
    
    # 演示生成问题序列
    questions_s = sm.get_situation_question(industry)
    print("\n📋 Situation Questions:")
    for i, q in enumerate(questions_s, 1):
        print(f"   {i}. {q}")
    
    questions_p = sm.get_problem_question(industry)
    print("\n🔍 Problem Questions:")
    for i, q in enumerate(questions_p, 1):
        print(f"   {i}. {q}")
    
    # 模拟 80/20 检查
    print("\n💬 [对话监控]: 客户发言时间占比")
    test_time = client_speaking_time = 75.0
    should_redirect = sm.check_and_redirect(test_time)
    if not should_redirect:
        print(f"   ✅ 客户发言时间：{test_time:.1f}% - 符合 80/20 法则")
    
    # 生成行动计划
    action_plan = sm.generate_action_plan()
    print("\n📊 [行动计划] - SMART 原则:")
    print(json.dumps(action_plan, indent=2, ensure_ascii=False))
    
    print("\n" + "="*80)
    print("✅ State Machine demo completed successfully!")
    print("="*80)