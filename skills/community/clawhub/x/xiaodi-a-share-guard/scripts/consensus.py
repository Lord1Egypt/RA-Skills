#!/usr/bin/env python3
"""
A股避雷针 - 第三层：决策判官（Decision）

任务：
1. 对比前两层的输出
2. 如果研报全是利好，但量化指标极差 → 触发避雷预警
3. 三层必须达成共识才输出结论

共识规则：
- 三层一致（全部安全）→ 输出"安全"
- 三层一致（全部预警）→ 输出"高危"
- 不一致（研报利好+量化预警）→ 输出"避雷预警"（特殊标记）
- 不一致（研报利空+量化安全）→ 输出"观察"（谨慎）

输出：
- 综合风险评级：安全 / 观察 / 预警 / 高危
- 避雷建议：持有 / 观察 / 减仓 / 回避
- 关键雷点清单
"""

import argparse
import datetime as dt
import json


# ========== 风险评级阈值 ==========
RATING_THRESHOLDS = {
    "安全": {"max_score": 29},
    "观察": {"min_score": 30, "max_score": 49},
    "预警": {"min_score": 50, "max_score": 69},
    "高危": {"min_score": 70},
}

# ========== 避雷建议映射 ==========
RATING_TO_ACTION = {
    "安全": "持有",
    "观察": "观察",
    "预警": "减仓",
    "高危": "回避",
}


# ========== 共聚判官核心逻辑 ==========
def make_consensus_decision(
    sentiment_score,  # 第一层：语义评分（0-100）
    quant_score,      # 第二层：量化评分（0-100）
    sentiment_detail=None,
    quant_detail=None
):
    """
    三层共识决策
    
    规则：
    1. 研报评分低（<30，利好为主）+ 量化评分高（>50）→ 避雷预警
    2. 研报评分高（>50，利空为主）+ 量化评分低（<30）→ 观察
    3. 三层一致 → 正常评级
    """
    
    # 判断单层状态
    def get_level(score):
        if score < 30:
            return "安全"
        elif score < 50:
            return "观察"
        elif score < 70:
            return "预警"
        else:
            return "高危"
    
    sentiment_level = get_level(sentiment_score)
    quant_level = get_level(quant_score)
    
    # 共聚判断
    consensus_type = "一致"
    
    # 特殊情况：研报利好 + 量化高危 → 避雷预警
    if sentiment_score < 30 and quant_score >= 50:
        final_level = "预警"
        consensus_type = "背离预警"
        special_note = "研报乐观但量化高危 → 隐藏雷点"
    
    # 特殊情况：研报利空 + 量化安全 → 观察
    elif sentiment_score >= 50 and quant_score < 30:
        final_level = "观察"
        consensus_type = "谨慎观察"
        special_note = "研报悲观但量化健康 → 可能过度反应"
    
    # 三层一致
    else:
        # 取两层最高分作为最终评分
        final_score = max(sentiment_score, quant_score)
        final_level = get_level(final_score)
        special_note = None
    
    # 综合评分（加权平均）
    weighted_score = (
        sentiment_score * 0.3 +  # 语义权重 30%
        quant_score * 0.7        # 量化权重 70%
    )
    
    return {
        "sentiment_level": sentiment_level,
        "sentiment_score": sentiment_score,
        "quant_level": quant_level,
        "quant_score": quant_score,
        "consensus_type": consensus_type,
        "final_level": final_level,
        "weighted_score": round(weighted_score, 1),
        "action": RATING_TO_ACTION[final_level],
        "special_note": special_note,
    }


# ========== 雷点提取 ==========
def extract_red_flags(sentiment_detail, quant_detail):
    """
    从前两层提取关键雷点
    
    输出：雷点清单（最多5条）
    """
    red_flags = []
    
    # 从量化层提取
    if quant_detail:
        reasons = quant_detail.get("reasons", [])
        for r in reasons[:3]:  # 最多取3条
            red_flags.append({
                "source": "量化审计",
                "content": r,
                "severity": "high" if "高危" in r or "连续" in r else "medium",
            })
    
    # 从语义层提取
    if sentiment_detail:
        negative_counts = sentiment_detail.get("negative_counts", {})
        for kw, data in list(negative_counts.items())[:2]:
            red_flags.append({
                "source": "研报语义",
                "content": f"{kw}（出现{data['count']}次）",
                "severity": "medium",
            })
    
    return red_flags


# ========== 主决策函数 ==========
def make_final_decision(
    code6,
    sentiment_data=None,
    quant_data=None
):
    """
    生成最终避雷决策
    
    输入：
    - code6: 股票代码
    - sentiment_data: 第一层输出
    - quant_data: 第二层输出
    
    输出：
    - 综合避雷报告
    """
    
    result = {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "code": code6,
    }
    
    # 提取评分
    sentiment_score = sentiment_data.get("sentiment", {}).get("score", 0) if sentiment_data else 0
    quant_score = quant_data.get("risk", {}).get("score", 0) if quant_data else 0
    
    # 共聚决策
    decision = make_consensus_decision(
        sentiment_score,
        quant_score,
        sentiment_data.get("sentiment") if sentiment_data else None,
        quant_data.get("risk") if quant_data else None,
    )
    
    result["decision"] = decision
    
    # 提取雷点
    red_flags = extract_red_flags(
        sentiment_data.get("sentiment") if sentiment_data else None,
        quant_data.get("risk") if quant_data else None,
    )
    result["red_flags"] = red_flags
    
    # 输出格式化报告
    result["report"] = format_report(code6, decision, red_flags)
    
    return result


def format_report(code6, decision, red_flags):
    """
    格式化输出报告（30秒可读完）
    """
    lines = []
    lines.append(f"⚡ [{code6}] 避雷扫描报告")
    lines.append("")
    lines.append(f"## 🎯 综合评级：{get_emoji(decision['final_level'])} {decision['final_level']}")
    
    if decision.get("special_note"):
        lines.append(f"**判官结论**：{decision['special_note']}")
    
    lines.append("")
    lines.append("### 🔍 第一层：语义对齐")
    lines.append(f"- 研报情绪：{decision['sentiment_level']}（评分 {decision['sentiment_score']}）")
    
    lines.append("")
    lines.append("### 📊 第二层：数智校验")
    lines.append(f"- 量化风险：{decision['quant_level']}（评分 {decision['quant_score']}）")
    
    lines.append("")
    lines.append(f"### ⚠️ 第三层：决策判官")
    lines.append(f"- 共聚类型：{decision['consensus_type']}")
    lines.append(f"- 综合评分：{decision['weighted_score']}分")
    
    lines.append("")
    lines.append("## 📋 避雷建议")
    lines.append(f"- **{decision['action']}**")
    
    if red_flags:
        lines.append("- **关键雷点**：")
        for flag in red_flags[:3]:
            lines.append(f"  - [{flag['source']}] {flag['content']}")
    
    return "\n".join(lines)


def get_emoji(level):
    """评级对应 emoji"""
    emoji_map = {
        "安全": "✅",
        "观察": "⚠️",
        "预警": "❌",
        "高危": "🔥",
    }
    return emoji_map.get(level, "❓")


def main():
    parser = argparse.ArgumentParser(description="A股避雷针 - 共聚判官")
    parser.add_argument("--code", required=True, help="股票代码")
    parser.add_argument("--sentiment-score", type=int, default=0, help="语义评分")
    parser.add_argument("--quant-score", type=int, default=0, help="量化评分")
    parser.add_argument("--pretty", action="store_true", help="美化输出")
    args = parser.parse_args()
    
    # 模拟数据（实际应从前两层获取）
    sentiment_data = {
        "sentiment": {
            "score": args.sentiment_score,
            "negative_counts": {},
        }
    }
    quant_data = {
        "risk": {
            "score": args.quant_score,
            "reasons": [],
        }
    }
    
    result = make_final_decision(args.code, sentiment_data, quant_data)
    
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())