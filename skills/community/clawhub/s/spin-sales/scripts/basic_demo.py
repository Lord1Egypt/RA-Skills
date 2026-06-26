# ================================ =======================
# scripts/basic_demo.py - SPIN 销售法流程演示（Python 版）
# 目标：展示如何使用 scripts/ 中各模块完成完整 SPIN 流程
# ================================ =======================

import sys
import os

# 确保能导入同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from question_generator import generate_spin_questions
from demo_interview import SpinStateMachine


def run_spin_demo():
    """运行一次完整的 SPIN 销售流程演示"""
    
    print("=" * 70)
    print("  🎯 SPIN 销售法 — 完整流程演示（Python）")
    print("=" * 70)
    
    # ── 阶段 1：根据行业生成 S/P/I/N 问题序列 ──
    print("\n【第 1 步】生成 SPIN 四阶段问题序列")
    print("-" * 50)
    questions = generate_spin_questions("物流", "车队管理系统")
    
    for stage_key, q_list in questions["questions_by_stage"].items():
        stage_name = {
            "situation": "S - 背景问题",
            "problem": "P - 难题问题",
            "implication": "I - 影响问题",
            "need_payoff": "N - 需求效益"
        }.get(stage_key, stage_key)
        
        print(f"\n  📌 {stage_name}")
        for i, q in enumerate(q_list[:3], 1):  # 各阶段只展示前 3 个
            print(f"     {i}. {q}")
    
    # ── 阶段 2：使用状态机模拟对话流程 ──
    print("\n\n【第 2 步】状态机 — 模拟对话流程")
    print("-" * 50)
    
    sm = SpinStateMachine()
    industry = "物流"
    
    # S 阶段
    print("\n  📞 [S] 背景调研")
    s_qs = sm.get_situation_question(industry)
    print(f"     → {s_qs[0]}")
    
    # P 阶段
    print("\n  🔍 [P] 痛点挖掘")
    p_qs = sm.get_problem_question(industry)
    print(f"     → {p_qs[0]}")
    
    # I 阶段
    print("\n  💥 [I] 影响放大")
    i_qs = sm.get_implication_question(industry)
    print(f"     → {i_qs[0]}")
    
    # N 阶段
    print("\n  💰 [N] 价值确认")
    n_qs = sm.get_need_payoff_question(industry)
    print(f"     → {n_qs[0]}")
    
    # ── 阶段 3：80/20 监控 ──
    print("\n\n【第 3 步】80/20 法则监控")
    print("-" * 50)
    test_time = 75.0
    should_redirect = sm.check_and_redirect(test_time)
    status = "✅ 合格" if not should_redirect else "⚠️ 需要调整"
    print(f"     客户发言占比: {test_time}% → {status}")
    
    # ── 阶段 4：生成行动计划 ──
    action_plan = sm.generate_action_plan()
    print(f"\n📋 行动计划: {len(action_plan['milestones'])} 个里程碑")
    for m in action_plan["milestones"]:
        print(f"     🎯 {m['phase']}: {m['timeline']}")
    
    print("\n" + "=" * 70)
    print("  ✅ SPIN 流程演示完成！")
    print("=" * 70)


if __name__ == "__main__":
    run_spin_demo()
