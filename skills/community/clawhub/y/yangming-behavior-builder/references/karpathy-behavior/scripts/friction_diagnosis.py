#!/usr/bin/env python3
"""
知行摩擦诊断脚本 v1.0
阳明造人术 · 行为操作系统核心模块

功能：诊断用户行为与目标人物行为模式之间的差距
输入：用户描述的具体行为场景（文本）
输出：知行摩擦报告（诊断点 + 改进建议）

使用方式：
python3 friction_diagnosis.py --user "你的行为描述" --target "人物名"
"""

import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ==================== 行为模式数据库 ====================
# 这是一个简化的行为模式库，实际使用时从skill的references加载

BEHAVIOR_PATTERNS = {
    "朱少醒": {
        "持仓换手率": {"value": "极低(约50%/年)", "meaning": "几乎不交易"},
        "危机行为": {"value": "不减仓，持有不动", "meaning": "信念型持仓"},
        "持仓集中度": {"value": "较高，前10占60%+", "meaning": "集中持仓"},
        "决策时机": {"value": "等跌到位才买", "meaning": "逆向决策"},
        "失败恢复": {"value": "快速，不纠缠", "meaning": "向前看"},
        "执行彻底性": {"value": "高，一旦决定不改变", "meaning": "信念驱动"}
    },
    "张坤": {
        "持仓换手率": {"value": "极低(<30%/年)", "meaning": "长期持有"},
        "危机行为": {"value": "不减持，扛住回撤", "meaning": "长期主义"},
        "持仓集中度": {"value": "高，茅台占20%+", "meaning": "集中重仓"},
        "决策时机": {"value": "好公司跌到位买", "meaning": "价值逆向"},
        "失败恢复": {"value": "等待，不操作", "meaning": "忍耐力强"},
        "执行彻底性": {"value": "极高，顶住压力不卖", "meaning": "信念坚定"}
    },
    "但斌": {
        "持仓换手率": {"value": "极低", "meaning": "超长期持有"},
        "危机行为": {"value": "危机时加仓", "meaning": "逆向加仓"},
        "持仓集中度": {"value": "集中，茅台为主", "meaning": "核心持仓"},
        "决策时机": {"value": "不择时", "meaning": "放弃择时"},
        "失败恢复": {"value": "长周期恢复", "meaning": "耐心等待"},
        "执行彻底性": {"value": "高，但暴露于极端风险", "meaning": "信念押注"}
    },
    "李蓓": {
        "持仓换手率": {"value": "灵活(0-100%)", "meaning": "动态调整"},
        "危机行为": {"value": "减仓躲避，回补获益", "meaning": "宏观择时"},
        "持仓集中度": {"value": "随时变化", "meaning": "灵活配置"},
        "决策时机": {"value": "宏观信号驱动", "meaning": "系统性择时"},
        "失败恢复": {"value": "快速承认，快速调整", "meaning": "纠错能力强"},
        "执行彻底性": {"value": "高，仓位执行一致", "meaning": "纪律性强"}
    },
    "邱国鹭": {
        "持仓换手率": {"value": "低", "meaning": "长期持有"},
        "危机行为": {"value": "人弃我取，加仓", "meaning": "逆向投资"},
        "持仓集中度": {"value": "低估+高壁垒", "meaning": "价值集中"},
        "决策时机": {"value": "等跌到位，好公司便宜时", "meaning": "价值择时"},
        "失败恢复": {"value": "不等反弹，换标的", "meaning": "灵活切换"},
        "执行彻底性": {"value": "高，价值投资不变", "meaning": "理念坚定"}
    }
}

# 知行摩擦维度定义
FRICTION_DIMENSIONS = {
    "决策时机": {
        "描述": "在决策时机的选择上",
        "value_range": ["极度逆向(等跌到位)", "适度逆向", "中性", "适度顺势", "极度顺势(追涨)"],
        "positive": "逆向",
        "negative": "顺势"
    },
    "压力反应": {
        "描述": "在压力/危机情况下的反应",
        "value_range": ["心完全不动", "心动但延迟行动", "心动但有限反应", "立即反应", "过度反应"],
        "positive": "延迟/不动",
        "negative": "立即反应"
    },
    "失败恢复": {
        "描述": "在失败/错误发生后的恢复速度",
        "value_range": ["立即重启(<24h)", "快速恢复(1-3天)", "正常恢复(1-2周)", "较长恢复(1个月+)", "长期纠缠"],
        "positive": "快速",
        "negative": "纠缠"
    },
    "执行彻底性": {
        "描述": "在执行过程中的彻底程度",
        "value_range": ["极度彻底(不改变)", "高彻底性", "适度", "容易调整", "经常改变"],
        "positive": "彻底",
        "negative": "易变"
    },
    "持仓风格": {
        "描述": "在持仓集中度上",
        "value_range": ["极度集中(<5只)", "适度集中(5-10只)", "中等分散(10-20只)", "高度分散(20-50只)", "极度分散(50+只)"],
        "positive": "集中",
        "negative": "分散"
    },
    "时间视野": {
        "描述": "在投资/决策的时间视野上",
        "value_range": ["5年以上", "3-5年", "1-3年", "6-12个月", "短线(<6个月)"],
        "positive": "长期",
        "negative": "短期"
    }
}


# ==================== 核心诊断函数 ====================

def parse_user_behavior(user_input: str) -> Dict[str, str]:
    """
    解析用户输入的行为描述
    提取关键行为维度
    """
    user_input_lower = user_input.lower()
    
    parsed = {}
    
    # 持仓换手率识别
    if any(kw in user_input_lower for kw in ["换手", "交易", "买卖", "操作", "卖", "买", "频繁", "经常换"]):
        if any(kw in user_input_lower for kw in ["每天", "每周", "经常", "频繁", "很高"]):
            parsed["持仓换手率"] = "极高(>300%)"
        elif any(kw in user_input_lower for kw in ["每月", "有时", "偶尔"]):
            parsed["持仓换手率"] = "中等(100-200%)"
        elif any(kw in user_input_lower for kw in ["很少", "几乎不", "基本不"]):
            parsed["持仓换手率"] = "极低(<50%)"
        else:
            parsed["持仓换手率"] = "待确认"
    
    # 危机行为识别
    if any(kw in user_input_lower for kw in ["股灾", "大跌", "回撤", "亏损", "暴跌", "危机", "压力"]):
        if any(kw in user_input_lower for kw in ["不减仓", "持有", "不动", "等待", "不卖"]):
            parsed["危机行为"] = "不减仓，持有"
        elif any(kw in user_input_lower for kw in ["减仓", "卖出", "躲避", "清仓"]):
            parsed["危机行为"] = "减仓躲避"
        elif any(kw in user_input_lower for kw in ["加仓", "买入", "抄底"]):
            parsed["危机行为"] = "加仓"
        else:
            parsed["危机行为"] = "待确认"
    
    # 持仓集中度识别
    if any(kw in user_input_lower for kw in ["集中", "重仓", "主要", "仓位高", "占比"]):
        if any(kw in user_input_lower for kw in ["3", "5", "少数", "主要几只"]):
            parsed["持仓集中度"] = "集中(<10只)"
        elif any(kw in user_input_lower for kw in ["分散", "很多", "50", "20", "东一只西一只"]):
            parsed["持仓集中度"] = "分散(>20只)"
        else:
            parsed["持仓集中度"] = "待确认"
    
    # 失败恢复识别
    if any(kw in user_input_lower for kw in ["失败", "错误", "亏", "错", "后悔"]):
        if any(kw in user_input_lower for kw in ["很快", "继续", "下一个", "不等", "立刻"]):
            parsed["失败恢复"] = "快速恢复"
        elif any(kw in user_input_lower for kw in ["很久", "需要时间", "纠结", "走不出来", "一直"]):
            parsed["失败恢复"] = "较长恢复"
        else:
            parsed["失败恢复"] = "待确认"
    
    return parsed


def calculate_friction(target_name: str, user_behavior: Dict[str, str]) -> List[Dict]:
    """
    计算知行摩擦点
    返回摩擦点列表
    """
    if target_name not in BEHAVIOR_PATTERNS:
        return [{"error": f"目标人物 {target_name} 不在数据库中"}]
    
    target_patterns = BEHAVIOR_PATTERNS[target_name]
    friction_points = []
    
    # 定义摩擦维度
    dimension_mapping = {
        "持仓换手率": "持仓换手率",
        "危机行为": "压力反应",
        "持仓集中度": "持仓风格",
        "失败恢复": "失败恢复"
    }
    
    for user_dim, user_val in user_behavior.items():
        if user_dim == "error":
            continue
            
        if user_dim in dimension_mapping:
            target_dim = dimension_mapping[user_dim]
        else:
            target_dim = user_dim
        
        if target_dim not in target_patterns:
            continue
        
        target_info = target_patterns[target_dim]
        
        # 计算摩擦
        friction = {
            "dimension": target_dim,
            "target_behavior": target_info["value"],
            "target_meaning": target_info["meaning"],
            "user_behavior": user_val,
            "friction_type": "待分析"
        }
        
        # 简单摩擦判断逻辑
        # 这是一个简化版本，实际使用时需要更复杂的匹配
        if "待确认" not in user_val:
            if target_dim == "持仓换手率":
                if "极低" in target_info["value"] and ("高" in user_val or "频繁" in user_val):
                    friction["friction_type"] = "过度交易 vs 信念持有"
                    friction["suggestion"] = "从'持有一只股票一年不卖'开始练习"
                elif "高" in target_info["value"] and "低" in user_val:
                    friction["friction_type"] = "低换手 vs 活跃交易"
                    friction["suggestion"] = "减少交易频率，每笔交易前问'是否需要操作'"
            elif target_dim == "压力反应":
                if "不减仓" in target_info["value"] and "减" in user_val:
                    friction["friction_type"] = "压力下减仓 vs 信念持有"
                    friction["suggestion"] = "下次大跌时，先等48小时再决定是否减仓"
                elif "减仓" in target_info["value"] and "不减" in user_val:
                    friction["friction_type"] = "不止损 vs 风险控制"
                    friction["suggestion"] = "建立下跌20%必须审视的规则"
            elif target_dim == "持仓风格":
                if "集中" in target_info["value"] and ("分散" in user_val or "50" in user_val):
                    friction["friction_type"] = "过度分散 vs 集中优势"
                    friction["suggestion"] = "选择你最看好的3只，减少到10只以内"
            elif target_dim == "失败恢复":
                if "快速" in target_info["value"] and ("很久" in user_val or "纠结" in user_val):
                    friction["friction_type"] = "失败后纠缠 vs 快速重启"
                    friction["suggestion"] = "建立'失败后48小时行动'仪式"
        
        friction_points.append(friction)
    
    return friction_points


def calculate_friction_index(friction_points: List[Dict]) -> Tuple[int, str]:
    """
    计算知行摩擦指数（0-10）
    分数越高=差距越大
    """
    if not friction_points or any(p.get("error") for p in friction_points):
        return 0, "无法评估"
    
    # 简化评分逻辑
    score = 0
    for fp in friction_points:
        if fp.get("friction_type") and "待分析" not in fp.get("friction_type", ""):
            score += 2  # 每个确定的摩擦点+2分
    
    score = min(10, max(0, score))
    
    if score >= 8:
        level = "严重摩擦（需重大改变）"
    elif score >= 5:
        level = "中等摩擦（需针对性改进）"
    elif score >= 3:
        level = "轻度摩擦（已有基础匹配）"
    else:
        level = "低摩擦（接近目标行为）"
    
    return score, level


def generate_report(target_name: str, user_behavior: Dict, friction_points: List[Dict], 
                   friction_index: int, level: str) -> str:
    """
    生成知行摩擦诊断报告
    """
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║           知行摩擦诊断报告                                   ║
║           用户 vs {target_name}                               ║
╠══════════════════════════════════════════════════════════════╣"""

    # 目标人物行为特征
    if target_name in BEHAVIOR_PATTERNS:
        report += f"""
║  【目标人物行为特征】                                        ║"""
        for dim, info in BEHAVIOR_PATTERNS[target_name].items():
            report += f"""
║  {dim}：{info['value']}                                    ║
║       含义：{info['meaning']}                             ║"""

    # 摩擦点
    report += """
╠══════════════════════════════════════════════════════════════╣
║  【知行摩擦点】                                              ║"""
    
    if friction_points:
        for i, fp in enumerate(friction_points, 1):
            if fp.get("friction_type") and "待分析" not in fp.get("friction_type", ""):
                report += f"""
║  摩擦点{i}：{fp['dimension']}                             ║
║  {target_name}做法：{fp['target_behavior']}              ║
║  你的做法：{fp['user_behavior']}                          ║
║  差距：{fp['friction_type']}                              ║
║  建议：{fp.get('suggestion', '待分析')}                      ║"""
    else:
        report += """
║  暂未发现明显摩擦点（需要更多具体行为描述）                    ║"""

    # 综合评估
    report += f"""
╠══════════════════════════════════════════════════════════════╣
║  【综合评估】                                                ║
║  知行摩擦指数：{friction_index}/10                              ║
║  摩擦等级：{level}                                  ║
╠══════════════════════════════════════════════════════════════╣
║  【核心发现】                                                ║"""

    # 核心发现
    if friction_points:
        main_friction = [fp for fp in friction_points if fp.get("friction_type") and "待分析" not in fp.get("friction_type", "")]
        if main_friction:
            report += f"""
║  主要矛盾：{main_friction[0]['friction_type']}                ║
║  影响最大的维度：{main_friction[0]['dimension']}              ║"""
    
    report += """
╠══════════════════════════════════════════════════════════════╣
║  【行动建议】                                                ║
║  1. 从最小行为改变开始（不要试图一次性改变所有）               ║
║  2. 记录每次决策时的行为，对比目标人物的做法                   ║
║  3. 定期回顾知行摩擦的变化（建议每2周一次）                    ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    return report


# ==================== 主程序 ====================

def main():
    """
    主程序入口
    使用方式：python3 friction_diagnosis.py --user "行为描述" --target "人物名"
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="知行摩擦诊断")
    parser.add_argument("--user", "-u", type=str, help="用户行为描述")
    parser.add_argument("--target", "-t", type=str, help="目标人物名")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.interactive or (not args.user and not args.target):
        # 交互模式
        print("=" * 60)
        print("阳明造人术 · 知行摩擦诊断")
        print("=" * 60)
        
        # 选择目标人物
        print("\n可选目标人物：")
        for i, name in enumerate(BEHAVIOR_PATTERNS.keys(), 1):
            print(f"  {i}. {name}")
        print(f"  {len(BEHAVIOR_PATTERNS)+1}. 自定义")
        
        choice = input("\n请选择目标人物（输入序号）：").strip()
        try:
            idx = int(choice) - 1
            if idx < len(BEHAVIOR_PATTERNS):
                target_name = list(BEHAVIOR_PATTERNS.keys())[idx]
            elif idx == len(BEHAVIOR_PATTERNS):
                target_name = input("请输入自定义人物名：").strip()
            else:
                print("无效选择")
                return
        except:
            target_name = choice if choice else "朱少醒"
        
        print(f"\n目标人物：{target_name}")
        print("\n请描述你的行为（尽量具体，例如：")
        print("  '我持仓50只股票，股灾时回撤15%就减仓，失败了会郁闷好几天'")
        print("  '我一看到持有的股票涨了就忍不住想卖'")
        print("  '我做错决定后要很久才能走出来'")
        print("）")
        user_input = input("\n你的行为描述：").strip()
    else:
        target_name = args.target or "朱少醒"
        user_input = args.user or ""
    
    if not user_input:
        print("错误：请提供行为描述")
        return
    
    # 解析用户行为
    user_behavior = parse_user_behavior(user_input)
    
    print(f"\n解析到你的行为特征：")
    for dim, val in user_behavior.items():
        print(f"  - {dim}: {val}")
    
    # 计算摩擦
    friction_points = calculate_friction(target_name, user_behavior)
    friction_index, level = calculate_friction_index(friction_points)
    
    # 生成报告
    report = generate_report(target_name, user_behavior, friction_points, 
                           friction_index, level)
    print(report)
    
    # 保存到日志
    log_path = f"logs/friction_log_{datetime.now().strftime('%Y%m%d')}.md"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n## 诊断记录 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**目标人物**：{target_name}\n")
            f.write(f"**用户行为**：{user_input}\n")
            f.write(f"**解析结果**：{user_behavior}\n")
            f.write(f"**摩擦指数**：{friction_index}/10 ({level})\n")
            if friction_points:
                f.write(f"**摩擦点**：\n")
                for fp in friction_points:
                    if fp.get("friction_type") and "待分析" not in fp.get("friction_type", ""):
                        f.write(f"  - {fp['dimension']}: {fp['friction_type']}\n")
    except Exception as e:
        print(f"\n注意：日志保存失败 ({e})")


if __name__ == "__main__":
    main()