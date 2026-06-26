#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solution-architect v1.0 - 解决方案架构师

提供经过验证的商业解决方案框架：
- 增长营销（特斯拉方案）
- 内容升级（36 氪方案）
- 平台增长（小米 MiMo 方案）

作者：董国华（清醒建造者）
版本：v1.0
日期：2026-04-02
协议：CC BY-NC-SA 4.0
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


# 解决方案库定义
SOLUTIONS = {
    "growth-marketing": {
        "name": "增长营销",
        "source": "特斯拉台湾市场增长战略",
        "framework": "AI 赋能的内容飞轮 × 本地化社群裂变 × 跨界体验破圈",
        "tactics": ["视频内容矩阵", "AI 内容生产线", "社群裂变", "跨界项目"],
        "kpi": ["社交媒体声量提升 50%", "内容驱动线索转化率提升 30%", "社群达 10 万人"],
        "timeline": "12-18 个月",
        "keywords": ["增长", "营销", "内容", "视频", "社群", "AI", "品牌", "用户"]
    },
    "content-upgrade": {
        "name": "内容升级",
        "source": "36 氪二级市场内容体系升级",
        "framework": "一核两翼三驱动",
        "tactics": ["三级产品矩阵", "财报分析 SOP", "AI 生产管线", "专家网络", "社群运营"],
        "kpi": ["用户粘性提升 40%", "产出 3 个深度研究系列", "建立专家网络"],
        "timeline": "12 个月",
        "keywords": ["内容", "升级", "研究", "产品化", "AI", "媒体", "转型", "专家"]
    },
    "platform-growth": {
        "name": "平台增长",
        "source": "小米 MiMo 开放平台规模化增长战略",
        "framework": "三层驱动增长引擎（产品力/运营力/生态力）",
        "tactics": ["产品力引擎", "运营力引擎", "生态力引擎", "增长飞轮"],
        "kpi": ["MAD 增长 10 倍", "API 调用量季度 +20%", "应用商店 500+ 应用"],
        "timeline": "18 个月",
        "keywords": ["平台", "生态", "开发者", "API", "增长", "运营", "产品"]
    }
}


def list_solutions(args):
    """列出所有解决方案"""
    print("\n" + "="*70)
    print("                    解决方案架构师 v1.0")
    print("="*70)
    print(f"\n共 {len(SOLUTIONS)} 个解决方案：\n")
    
    for i, (key, sol) in enumerate(SOLUTIONS.items(), 1):
        print(f"{i}. {sol['name']} ({key})")
        print(f"   来源：{sol['source']}")
        print(f"   框架：{sol['framework']}")
        print(f"   周期：{sol['timeline']}")
        print(f"   核心 KPI：{', '.join(sol['kpi'][:2])}")
        print()
    
    print("使用提示:")
    print("  python3 script.py show <solution>     # 查看方案详情")
    print("  python3 script.py solve --problem '...' # 根据问题找方案")
    print("  python3 script.py plan --goal '...'     # 根据目标找路径")
    print("="*70 + "\n")
    
    return {"status": "success", "count": len(SOLUTIONS)}


def show_solution(args):
    """显示解决方案详情"""
    solution_key = args.solution
    
    if solution_key not in SOLUTIONS:
        print(f"❌ 错误：未找到解决方案 '{solution_key}'")
        print(f"可用方案：{', '.join(SOLUTIONS.keys())}")
        return {"status": "error", "message": "Solution not found"}
    
    sol = SOLUTIONS[solution_key]
    
    print("\n" + "="*70)
    print(f"  {sol['name']}")
    print("="*70)
    print(f"\n来源：{sol['source']}")
    print(f"实施周期：{sol['timeline']}")
    print(f"\n核心框架:")
    print(f"  {sol['framework']}")
    print(f"\n核心战术 ({len(sol['tactics'])}个):")
    for i, tactic in enumerate(sol['tactics'], 1):
        print(f"  {i}. {tactic}")
    print(f"\n核心 KPI:")
    for kpi in sol['kpi']:
        print(f"  ✅ {kpi}")
    
    # 显示框架文件路径
    framework_path = Path(__file__).parent / "solutions" / solution_key / "framework.md"
    if framework_path.exists():
        print(f"\n详细文档：{framework_path}")
    
    print("="*70 + "\n")
    
    return {"status": "success", "solution": solution_key}


def solve_problem(args):
    """根据问题匹配解决方案"""
    problem = args.problem.lower()
    
    print(f"\n🔍 分析问题：'{args.problem}'\n")
    
    # 关键词匹配
    matches = []
    for key, sol in SOLUTIONS.items():
        score = 0
        matched_keywords = []
        
        for keyword in sol['keywords']:
            if keyword in problem:
                score += 1
                matched_keywords.append(keyword)
        
        if score > 0:
            matches.append((key, sol, score, matched_keywords))
    
    if not matches:
        print("⚠️  未找到完全匹配的解决方案")
        print("\n建议:")
        print("  1. 尝试使用更具体的关键词（增长/内容/平台/生态/AI 等）")
        print("  2. 使用 'python3 script.py list' 查看所有方案")
        print("  3. 详细描述你的业务场景和目标")
        return {"status": "no_match"}
    
    # 按匹配度排序
    matches.sort(key=lambda x: x[2], reverse=True)
    
    print("✅ 匹配结果:\n")
    for i, (key, sol, score, keywords) in enumerate(matches, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{medal} {i}. {sol['name']} (匹配度：{score})")
        print(f"   匹配关键词：{', '.join(keywords)}")
        print(f"   核心框架：{sol['framework']}")
        print(f"   推荐战术：{', '.join(sol['tactics'][:3])}")
        print()
    
    # 推荐最佳匹配
    best_match = matches[0]
    print(f"\n💡 建议:")
    print(f"   使用 'python3 script.py show {best_match[0]}' 查看详细方案")
    print(f"   使用 'python3 script.py plan --goal \"你的具体目标\"' 获取实施路径")
    
    print("="*70 + "\n")
    
    return {"status": "success", "matches": [m[0] for m in matches]}


def plan_goal(args):
    """根据目标规划实施路径"""
    goal = args.goal.lower()
    
    print(f"\n🎯 分析目标：'{args.goal}'\n")
    
    # 简单关键词匹配
    if any(kw in goal for kw in ["开发者", "API", "平台", "生态"]):
        recommended = "platform-growth"
        reason = "你的目标涉及开发者/平台/生态增长"
    elif any(kw in goal for kw in ["内容", "媒体", "研究", "专家"]):
        recommended = "content-upgrade"
        reason = "你的目标涉及内容升级/媒体转型"
    elif any(kw in goal for kw in ["营销", "品牌", "用户", "社群", "增长"]):
        recommended = "growth-marketing"
        reason = "你的目标涉及营销增长/用户运营"
    else:
        print("⚠️  无法确定最佳方案，请尝试使用更具体的关键词")
        return {"status": "unclear"}
    
    sol = SOLUTIONS[recommended]
    
    print(f"✅ 推荐方案：{sol['name']}")
    print(f"   理由：{reason}")
    print(f"   来源：{sol['source']}")
    print(f"\n核心框架:")
    print(f"   {sol['framework']}")
    print(f"\n实施周期：{sol['timeline']}")
    print(f"\n核心 KPI:")
    for kpi in sol['kpi']:
        print(f"   ✅ {kpi}")
    print(f"\n关键战术:")
    for i, tactic in enumerate(sol['tactics'][:4], 1):
        print(f"   {i}. {tactic}")
    
    print(f"\n💡 下一步:")
    print(f"   使用 'python3 script.py show {recommended}' 查看详细方案")
    print(f"   查看框架文档获取完整实施路线图")
    
    print("="*70 + "\n")
    
    return {"status": "success", "recommended": recommended}


def enhance_plan(args):
    """优化现有方案"""
    my_plan = args.my_plan
    reference = args.reference
    
    print(f"\n📊 方案对比分析\n")
    print(f"你的方案：{my_plan}")
    print(f"参考方案：{reference}")
    print()
    
    # 检查文件是否存在
    if not Path(my_plan).exists():
        print(f"❌ 错误：文件不存在 '{my_plan}'")
        return {"status": "error", "message": "File not found"}
    
    if reference not in SOLUTIONS:
        print(f"❌ 错误：未找到参考方案 '{reference}'")
        print(f"可用方案：{', '.join(SOLUTIONS.keys())}")
        return {"status": "error", "message": "Solution not found"}
    
    sol = SOLUTIONS[reference]
    
    print(f"✅ 参考方案核心要素:\n")
    print(f"框架：{sol['framework']}")
    print(f"\n核心战术 ({len(sol['tactics'])}个):")
    for tactic in sol['tactics']:
        print(f"  □ {tactic}")
    print(f"\n核心 KPI:")
    for kpi in sol['kpi']:
        print(f"  □ {kpi}")
    
    print(f"\n💡 对比建议:")
    print(f"   1. 阅读你的方案文件，识别缺失的核心战术")
    print(f"   2. 检查 KPI 体系是否完整")
    print(f"   3. 参考实施路线图优化时间规划")
    print(f"   4. 查看框架文档获取完整方法论")
    
    print("="*70 + "\n")
    
    return {"status": "success", "reference": reference}


def main():
    parser = argparse.ArgumentParser(
        description="solution-architect v1.0 - 解决方案架构师",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 script.py list
  python3 script.py show growth-marketing
  python3 script.py solve --problem "内容团队效率低，想引入 AI"
  python3 script.py plan --goal "6 个月内开发者从 1000 到 10 万"
  python3 script.py enhance --my-plan plan.md --reference growth-marketing
        """
    )
    
    parser.add_argument(
        "action",
        type=str,
        choices=["list", "show", "solve", "plan", "enhance"],
        help="执行动作"
    )
    
    parser.add_argument(
        "--solution", "-s",
        type=str,
        help="解决方案名称（用于 show 动作）"
    )
    
    parser.add_argument(
        "--problem", "-p",
        type=str,
        help="问题描述（用于 solve 动作）"
    )
    
    parser.add_argument(
        "--goal", "-g",
        type=str,
        help="目标描述（用于 plan 动作）"
    )
    
    parser.add_argument(
        "--my-plan",
        type=str,
        help="我的方案文件路径（用于 enhance 动作）"
    )
    
    parser.add_argument(
        "--reference", "-r",
        type=str,
        help="参考解决方案（用于 enhance 动作）"
    )
    
    args = parser.parse_args()
    
    # 执行对应动作
    actions = {
        "list": list_solutions,
        "show": show_solution,
        "solve": solve_problem,
        "plan": plan_goal,
        "enhance": enhance_plan
    }
    
    if args.action in actions:
        # 参数验证
        if args.action == "show" and not args.solution:
            print("❌ 错误：show 动作需要 --solution 参数")
            print("示例：python3 script.py show growth-marketing")
            sys.exit(1)
        
        if args.action == "solve" and not args.problem:
            print("❌ 错误：solve 动作需要 --problem 参数")
            print("示例：python3 script.py solve --problem '内容团队效率低'")
            sys.exit(1)
        
        if args.action == "plan" and not args.goal:
            print("❌ 错误：plan 动作需要 --goal 参数")
            print("示例：python3 script.py plan --goal '6 个月内开发者增长 10 倍'")
            sys.exit(1)
        
        if args.action == "enhance":
            if not args.my_plan:
                print("❌ 错误：enhance 动作需要 --my-plan 参数")
                sys.exit(1)
            if not args.reference:
                print("❌ 错误：enhance 动作需要 --reference 参数")
                sys.exit(1)
        
        result = actions[args.action](args)
        return result
    else:
        print(f"❌ 错误：未知的动作：{args.action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
