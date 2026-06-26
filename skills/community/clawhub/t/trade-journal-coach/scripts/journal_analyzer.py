#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易复盘与心理诊断教练 - 主分析脚本 (v1.0)
分析交易记录，计算胜率/盈亏比，诊断心理问题，生成复盘报告
"""

import sys
import argparse
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Trade:
    """交易记录"""
    symbol: str  # 标的
    direction: str  # 买入/卖出
    plan_entry: float  # 计划入场价
    plan_exit: float  # 计划出场价/目标价
    plan_stop: float  # 计划止损价
    plan_position: float  # 计划仓位 (%)
    actual_entry: float  # 实际入场价
    actual_exit: float  # 实际出场价
    actual_position: float  # 实际仓位 (%)
    pnl: float  # 盈亏金额
    pnl_percent: float  # 盈亏比例 (%)
    emotion: str  # 交易时情绪
    reason: str  # 交易理由
    exit_reason: str  # 出场理由


@dataclass
class PerformanceMetrics:
    """绩效指标"""
    total_trades: int
    win_count: int
    lose_count: int
    win_rate: float  # 胜率
    avg_win: float  # 平均盈利
    avg_loss: float  # 平均亏损
    profit_loss_ratio: float  # 盈亏比
    total_pnl: float  # 总盈亏
    max_drawdown: float  # 最大回撤
    max_consecutive_wins: int
    max_consecutive_losses: int
    expectancy: float  # 期望值


@dataclass
class ExecutionGap:
    """执行差距"""
    trade: Trade
    gap_type: str  # 好亏损/坏盈利/致命失误/正常执行
    description: str
    severity: str  # 严重/中等/轻微


@dataclass
class PsychologyAssessment:
    """心理评估"""
    current_state: str  # 当前心理状态
    tilt_risk: str  # Tilt 风险（高/中/低）
    overconfidence_risk: str  # 过度自信风险
    key_issues: List[str]  # 主要问题
    intervention: str  # 干预建议


def calculate_metrics(trades: List[Trade]) -> PerformanceMetrics:
    """计算绩效指标"""
    if not trades:
        return PerformanceMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    wins = [t for t in trades if t.pnl > 0]
    losses = [t for t in trades if t.pnl <= 0]
    
    win_count = len(wins)
    lose_count = len(losses)
    total_trades = len(trades)
    
    win_rate = win_count / total_trades * 100 if total_trades > 0 else 0
    avg_win = sum(t.pnl for t in wins) / win_count if win_count > 0 else 0
    avg_loss = sum(t.pnl for t in losses) / lose_count if lose_count > 0 else 0
    profit_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    
    total_pnl = sum(t.pnl for t in trades)
    
    # 计算最大回撤（简化版）
    cumulative = 0
    peak = 0
    max_drawdown = 0
    for trade in trades:
        cumulative += trade.pnl
        if cumulative > peak:
            peak = cumulative
        drawdown = (peak - cumulative) / max(peak, 1) * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    # 计算连续盈利/亏损
    max_consecutive_wins = 0
    max_consecutive_losses = 0
    current_wins = 0
    current_losses = 0
    
    for trade in trades:
        if trade.pnl > 0:
            current_wins += 1
            current_losses = 0
            max_consecutive_wins = max(max_consecutive_wins, current_wins)
        else:
            current_losses += 1
            current_wins = 0
            max_consecutive_losses = max(max_consecutive_losses, current_losses)
    
    # 期望值
    expectancy = (win_rate / 100 * avg_win) - ((1 - win_rate / 100) * abs(avg_loss))
    
    return PerformanceMetrics(
        total_trades=total_trades,
        win_count=win_count,
        lose_count=lose_count,
        win_rate=win_rate,
        avg_win=avg_win,
        avg_loss=avg_loss,
        profit_loss_ratio=profit_loss_ratio,
        total_pnl=total_pnl,
        max_drawdown=max_drawdown,
        max_consecutive_wins=max_consecutive_wins,
        max_consecutive_losses=max_consecutive_losses,
        expectancy=expectancy
    )


def analyze_execution_gap(trades: List[Trade]) -> List[ExecutionGap]:
    """分析执行差距"""
    gaps = []
    
    for trade in trades:
        gap_type = "正常执行"
        description = "按计划执行"
        severity = "轻微"
        
        # 1. 检查是否计划外交易（FOMO）
        if not trade.reason or trade.reason in ["追高", "看到拉升", "临时起意", "FOMO"]:
            gap_type = "致命失误"
            description = f"计划外交易（FOMO）：{trade.reason}"
            severity = "严重"
        
        # 2. 检查是否擅改止损
        elif trade.actual_exit < trade.plan_stop and trade.pnl < 0:
            gap_type = "致命失误"
            description = f"擅改止损：计划{trade.plan_stop}，实际{trade.actual_exit}，死扛导致更大亏损"
            severity = "严重"
        
        # 3. 检查是否提前止盈
        elif trade.actual_exit > trade.plan_exit and trade.pnl > 0 and trade.plan_exit > trade.plan_entry:
            gap_type = "坏盈利"
            description = f"提前止盈：计划{trade.plan_exit}，实际{trade.actual_exit}，因恐惧利润回撤过早下车"
            severity = "中等"
        
        # 4. 检查是否逆势抗单
        elif trade.pnl < -10 and trade.pnl_percent < -10:
            gap_type = "致命失误"
            description = f"逆势抗单：亏损{trade.pnl_percent:.1f}%远超正常止损，缺乏断臂求生的勇气"
            severity = "严重"
        
        # 5. 检查是否仓位失控
        elif trade.actual_position > trade.plan_position * 1.5:
            gap_type = "致命失误"
            description = f"仓位失控：计划{trade.plan_position}%，实际{trade.actual_position}%"
            severity = "严重"
        
        # 6. 好亏损（按纪律止损）
        elif trade.pnl < 0 and abs(trade.pnl_percent) <= 5 and "止损" in trade.exit_reason:
            gap_type = "好亏损"
            description = "严格执行止损，这是好的亏损"
            severity = "轻微"
        
        # 7. 正常盈利
        elif trade.pnl > 0 and trade.actual_exit >= trade.plan_exit:
            gap_type = "正常执行"
            description = "按计划止盈，执行良好"
            severity = "轻微"
        
        gaps.append(ExecutionGap(
            trade=trade,
            gap_type=gap_type,
            description=description,
            severity=severity
        ))
    
    return gaps


def assess_psychology(trades: List[Trade], metrics: PerformanceMetrics, gaps: List[ExecutionGap]) -> PsychologyAssessment:
    """心理评估"""
    key_issues = []
    tilt_risk = "低"
    overconfidence_risk = "低"
    
    # 检查 Tilt 风险（连续亏损）
    if metrics.max_consecutive_losses >= 3:
        tilt_risk = "高"
        key_issues.append(f"连续{metrics.max_consecutive_losses}笔亏损，Tilt 风险高")
    elif metrics.max_consecutive_losses >= 2:
        tilt_risk = "中"
        key_issues.append(f"连续{metrics.max_consecutive_losses}笔亏损，注意情绪管理")
    
    # 检查过度自信风险（连续盈利）
    if metrics.max_consecutive_wins >= 5:
        overconfidence_risk = "高"
        key_issues.append(f"连续{metrics.max_consecutive_wins}笔盈利，警惕过度自信")
    elif metrics.max_consecutive_wins >= 3:
        overconfidence_risk = "中"
        key_issues.append(f"连续{metrics.max_consecutive_wins}笔盈利，保持谦逊")
    
    # 检查致命失误数量
    fatal_errors = [g for g in gaps if g.severity == "严重"]
    if len(fatal_errors) >= 3:
        key_issues.append(f"{len(fatal_errors)}笔严重违规操作，纪律执行堪忧")
    
    # 检查盈亏比
    if metrics.profit_loss_ratio < 1.5:
        key_issues.append(f"盈亏比{metrics.profit_loss_ratio:.2f}偏低，赚小钱亏大钱")
    
    # 确定当前心理状态
    if tilt_risk == "高":
        current_state = "🔴 Tilt 状态（心态爆炸）"
    elif overconfidence_risk == "高":
        current_state = "🟠 过度自信（觉得自己是股神）"
    elif len(fatal_errors) >= 3:
        current_state = "🟡 纪律松散（随意操作）"
    elif metrics.win_rate < 30:
        current_state = "🔵 挫败感强（连续亏损）"
    else:
        current_state = "🟢 状态正常"
    
    # 干预建议
    if tilt_risk == "高":
        intervention = "强制空仓 48 小时，远离盘面，运动/睡觉/转移注意力"
    elif overconfidence_risk == "高":
        intervention = "回顾历史亏损案例，提醒自己盈亏同源，保持原有纪律"
    elif len(fatal_errors) >= 3:
        intervention = "重新学习交易纪律，下周单笔仓位减半，找回执行盘感"
    else:
        intervention = "继续保持，定期复盘"
    
    return PsychologyAssessment(
        current_state=current_state,
        tilt_risk=tilt_risk,
        overconfidence_risk=overconfidence_risk,
        key_issues=key_issues,
        intervention=intervention
    )


def generate_report(trades: List[Trade], metrics: PerformanceMetrics, 
                   gaps: List[ExecutionGap], psych: PsychologyAssessment) -> str:
    """生成复盘报告"""
    
    # 系统健康度评价
    if metrics.win_rate >= 50 and metrics.profit_loss_ratio >= 2:
        health = "✅ 优秀（胜率盈亏比双高）"
    elif metrics.win_rate >= 40 and metrics.profit_loss_ratio >= 1.5:
        health = "🟢 良好（系统健康）"
    elif metrics.win_rate >= 40 and metrics.profit_loss_ratio < 1.5:
        health = "🟡 赚碎银子亏大钱（需提高盈亏比）"
    elif metrics.win_rate < 40 and metrics.profit_loss_ratio >= 2:
        health = "🟡 胜率低但盈亏比好（趋势交易特征）"
    else:
        health = "🔴 系统有问题（需全面复盘）"
    
    # 分类统计
    good_losses = [g for g in gaps if g.gap_type == "好亏损"]
    bad_wins = [g for g in gaps if g.gap_type == "坏盈利"]
    fatal_errors = [g for g in gaps if g.gap_type == "致命失误"]
    normal_exec = [g for g in gaps if g.gap_type == "正常执行"]
    
    # 工具联动建议
    if len(fatal_errors) > 0:
        tool_suggestion = """
 * 📡 **开仓前**：使用 `Market Sentiment Radar` 确认大盘环境是否安全
 * 📊 **选股时**：使用 `Select Super Stock` 筛选符合模型的标的，避免 FOMO
 * 🛡️ **持仓中**：使用 `Position Risk Manager` 锁死止损位，严格执行
"""
    else:
        tool_suggestion = """
 * 继续保持良好习惯，定期使用本工具复盘
 * 可根据市场环境调用 `Market Sentiment Radar` 调整仓位
"""
    
    report = f"""
### 🪞 交易灵魂拷问报告 (Trade Journal Review)

**报告生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

**1. 📊 客观数据真相 (Data Truth)**

| 指标 | 数值 | 健康参考 |
|------|------|----------|
| **样本量** | {metrics.total_trades} 笔 | >30 笔有统计意义 |
| **胜率** | {metrics.win_rate:.1f}% | 40-60% |
| **盈亏比** | {metrics.profit_loss_ratio:.2f} | >2.0 |
| **期望值** | {metrics.expectancy:.2f}元 | >0 |
| **总盈亏** | {metrics.total_pnl:+.2f}元 | - |
| **最大回撤** | {metrics.max_drawdown:.1f}% | <10% |
| **最长连盈** | {metrics.max_consecutive_wins}笔 | - |
| **最长连亏** | {metrics.max_consecutive_losses}笔 | - |

**系统健康度**：{health}

"""
    
    # 心理状态
    report += f"""**心理状态**：{psych.current_state}

"""
    
    # 纪律审判
    report += f"""---

**2. ⚖️ 纪律审判室 (Execution Gap)**

"""
    
    if good_losses:
        report += f"""**✅ 值得表扬的执行（{len(good_losses)}笔）**：
"""
        for g in good_losses:
            report += f""" * [{g.trade.symbol}]：{g.description}
"""
        report += "\n"
    
    if normal_exec:
        report += f"""**🟢 正常执行（{len(normal_exec)}笔）**：
"""
        for g in normal_exec[:3]:  # 只显示前 3 笔
            report += f""" * [{g.trade.symbol}]：{g.description}
"""
        report += "\n"
    
    if bad_wins:
        report += f"""**⚠️ 坏盈利（{len(bad_wins)}笔）**：
"""
        for g in bad_wins:
            report += f""" * [{g.trade.symbol}]：{g.description}
"""
        report += "\n"
    
    if fatal_errors:
        report += f"""**❌ 致命失误（{len(fatal_errors)}笔）**：
"""
        for g in fatal_errors:
            report += f""" * [{g.trade.symbol}]：{g.description}
"""
        report += "\n"
    
    # 心理诊断
    report += f"""---

**3. 🧠 心理诊断与干预 (Psychological Coaching)**

**当前心理状态分析**：{psych.current_state}

"""
    
    if psych.key_issues:
        report += """**关键问题**：
"""
        for issue in psych.key_issues:
            report += f"- {issue}\n"
        report += "\n"
    
    # AI 的客观视角
    if psych.tilt_risk == "高":
        ai_perspective = """
> 💬 **AI 的客观视角**：
> 
> 作为一个没有情感的系统，我看到的事实是：你的策略没有失效，是你的【执行】在情绪的干扰下崩溃了。
> 
> 连续亏损是交易系统的正常损耗，就像开店的房租成本。你现在的痛苦来自于"急于翻本"，这会让你做出更糟糕的决策。
> 
> 不要用概率的随机性来惩罚自己的情绪。
"""
    elif psych.overconfidence_risk == "高":
        ai_perspective = """
> 💬 **AI 的客观视角**：
> 
> 作为一个没有情感的系统，我看到的事实是：你的盈利可能来自于"大盘主升浪"而非个人能力。
> 
> 历史上有太多人在主升浪赚到的钱，在退潮期全部还回去。你现在觉得自已是股神，这正是最危险的时候。
> 
> 盈亏同源，保持敬畏。
"""
    else:
        ai_perspective = """
> 💬 **AI 的客观视角**：
> 
> 作为一个没有情感的系统，我看到的事实是：你的交易记录反映了你的执行力和心态。
> 
> 好的交易不是每笔都赚，而是长期保持正期望值。继续执行你的系统，让概率为你工作。
"""
    
    report += ai_perspective
    
    # 下一步强制约束
    report += f"""
---

**4. 🔒 下一步强制约束 (Next Steps & Hard Rules)**

**心理处方**：{psych.intervention}

**强制性纪律约束**：
"""
    
    if psych.tilt_risk == "高":
        report += """
1. **强制空仓 48 小时**：关闭交易软件，删除自选股
2. **转移注意力**：去运动、看电影、陪家人，做任何与交易无关的事
3. **写反思日记**：写下这几次亏损的真实原因（不是借口）
4. **回归模拟盘**：48 小时后先用模拟盘找回盘感
"""
    elif psych.overconfidence_risk == "高":
        report += """
1. **回顾历史**：翻看自己以前的亏损记录，提醒自己也会亏钱
2. **保持仓位**：不要因为连续盈利就加大仓位
3. **严格止损**：继续执行原有止损纪律，不要放松
4. **定期出金**：把盈利的一部分取出，让利润变得真实
"""
    elif len(fatal_errors) >= 3:
        report += """
1. **重新学习**：复习交易纪律和系统规则
2. **减半仓位**：下周单笔仓位上限缩减至平时的 50%
3. **写计划**：每笔交易前写下计划（入场/止损/目标/仓位）
4. **对账**：每日收盘后对比计划与执行
"""
    else:
        report += """
1. **继续保持**：当前状态良好，继续执行系统
2. **定期复盘**：每周/每月使用本工具复盘
3. **记录情绪**：在交易日记中记录每笔交易时的情绪
"""
    
    report += f"""
**工具联动建议**：{tool_suggestion}

---

**5. 📝 总结**

"""
    
    # 总结
    if psych.tilt_risk == "高":
        summary = """
> 🔴 **当前最紧急的是调整心态，而不是赚钱。**
> 
> 市场永远在那里，机会永远有。但如果你心态崩溃，本金亏光，就真的出局了。
> 
> 听我一句劝：关掉软件，出去走走。48 小时后再说。
"""
    elif psych.overconfidence_risk == "高":
        summary = """
> 🟠 **记住：市场会教训每一个骄傲的人。**
> 
> 你现在的盈利可能是市场给你的礼物，不是你的能力。
> 
> 保持谦逊，继续执行纪律，把盈利变成真正的利润（出金）。
"""
    elif len(fatal_errors) >= 3:
        summary = """
> 🟡 **你的问题不是技术，是纪律。**
> 
> 再好的系统，不执行也是零。
> 
> 从下一笔交易开始，重新学习什么叫"知行合一"。
"""
    else:
        summary = """
> 🟢 **你走在正确的道路上。**
> 
> 交易是一场马拉松，不是百米冲刺。
> 
> 保持耐心，保持纪律，让时间和复利为你工作。
"""
    
    report += summary
    
    report += f"""
---

⚠️ **风险提示**：本报告仅供参考，不构成投资建议。交易有风险，投资需谨慎。

*记住：交易的终极对手不是市场，是自己。*
"""
    
    return report


def parse_trades_from_json(json_str: str) -> List[Trade]:
    """从 JSON 字符串解析交易记录"""
    try:
        data = json.loads(json_str)
        trades = []
        for item in data:
            trades.append(Trade(**item))
        return trades
    except Exception as e:
        print(f"解析交易记录失败：{e}")
        return []


def get_sample_trades() -> List[Trade]:
    """返回示例交易记录"""
    return [
        Trade(
            symbol="中国海油",
            direction="买入",
            plan_entry=30.0,
            plan_exit=36.0,
            plan_stop=28.5,
            plan_position=20,
            actual_entry=30.0,
            actual_exit=38.0,
            actual_position=20,
            pnl=8000,
            pnl_percent=26.7,
            emotion="平静",
            reason="符合模型 A，长线稳步上涨",
            exit_reason="移动止盈触发"
        ),
        Trade(
            symbol="璞泰来",
            direction="买入",
            plan_entry=35.0,
            plan_exit=40.0,
            plan_stop=33.0,
            plan_position=15,
            actual_entry=35.0,
            actual_exit=32.0,
            actual_position=15,
            pnl=-4500,
            pnl_percent=-8.6,
            emotion="恐惧",
            reason="符合模型 B，历史低位反弹",
            exit_reason="严格止损"
        ),
        Trade(
            symbol="某妖股",
            direction="买入",
            plan_entry=0,
            plan_exit=0,
            plan_stop=0,
            plan_position=0,
            actual_entry=25.0,
            actual_exit=22.0,
            actual_position=30,
            pnl=-9000,
            pnl_percent=-12.0,
            emotion="贪婪",
            reason="看到拉升，临时追高",
            exit_reason="扛不住亏损卖出"
        ),
        Trade(
            symbol="洛阳钼业",
            direction="买入",
            plan_entry=23.0,
            plan_exit=26.0,
            plan_stop=21.5,
            plan_position=20,
            actual_entry=23.0,
            actual_exit=19.0,
            actual_position=25,
            pnl=-10000,
            pnl_percent=-17.4,
            emotion="侥幸",
            reason="觉得是低位，可以抄底",
            exit_reason="死扛到深套"
        ),
        Trade(
            symbol="AI 龙头",
            direction="买入",
            plan_entry=50.0,
            plan_exit=60.0,
            plan_stop=47.0,
            plan_position=20,
            actual_entry=50.0,
            actual_exit=52.0,
            actual_position=20,
            pnl=2000,
            pnl_percent=4.0,
            emotion="恐惧",
            reason="主线板块龙头",
            exit_reason="害怕利润回撤，提前卖出"
        ),
    ]


def main():
    parser = argparse.ArgumentParser(description='交易复盘与心理诊断教练')
    parser.add_argument('--trades', type=str, help='交易记录 JSON 字符串')
    parser.add_argument('--sample', action='store_true', help='使用示例数据')
    
    args = parser.parse_args()
    
    # 获取交易记录
    if args.trades:
        trades = parse_trades_from_json(args.trades)
    elif args.sample:
        print("⚠️ 使用示例交易记录\n")
        trades = get_sample_trades()
    else:
        print("⚠️ 未提供交易记录，使用示例数据\n")
        trades = get_sample_trades()
    
    if not trades:
        print("❌ 没有交易记录可分析")
        return
    
    # 分析
    metrics = calculate_metrics(trades)
    gaps = analyze_execution_gap(trades)
    psych = assess_psychology(trades, metrics, gaps)
    
    # 生成报告
    report = generate_report(trades, metrics, gaps, psych)
    print(report)


if __name__ == '__main__':
    main()
