#!/usr/bin/env python3
"""
云旅LinkedIn优化器 - Yunlv LinkedIn Optimizer
开发信效果评分、跟进序列设计、行业钩子库匹配

命令:
  score-message   - 开发信效果评分
  sequence-design - 跟进序列设计
  hook-match     - 行业钩子库匹配
"""

import sys
import json
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# ============ 数据模型 ============

@dataclass
class MessageScore:
    """开发信评分结果"""
    total_score: float
    dimensions: Dict
    overall_feedback: str
    suggestions: List[str]

@dataclass
class FollowUpSequence:
    """跟进序列"""
    rounds: int
    days: List[int]
    sequence: List[Dict]

# ============ 核心评分函数 ============

def score_message(
    subject: str = None,
    opening_hook: str = None,
    value_proposition: str = None,
    cta: str = None,
    industry: str = None,
    full_message: str = None
) -> Dict:
    """开发信效果评分 - 4维度评估"""
    
    dimensions = {}
    total_score = 0
    
    # 1. 主题行评分
    if subject:
        subject_score = _score_subject(subject)
        dimensions["subject"] = {
            "value": subject,
            "score": subject_score,
            "analysis": _get_subject_analysis(subject_score)
        }
        total_score += subject_score * 0.25
    
    # 2. 开头钩子评分
    if opening_hook:
        hook_score = _score_hook(opening_hook)
        dimensions["opening_hook"] = {
            "value": opening_hook,
            "score": hook_score,
            "analysis": _get_hook_analysis(hook_score)
        }
        total_score += hook_score * 0.25
    
    # 3. 价值主张评分
    if value_proposition:
        vp_score = _score_value_proposition(value_proposition)
        dimensions["value_proposition"] = {
            "value": value_proposition,
            "score": vp_score,
            "analysis": _get_vp_analysis(vp_score)
        }
        total_score += vp_score * 0.30
    
    # 4. CTA评分
    if cta:
        cta_score = _score_cta(cta)
        dimensions["cta"] = {
            "value": cta,
            "score": cta_score,
            "analysis": _get_cta_analysis(cta_score)
        }
        total_score += cta_score * 0.20
    
    # 如果提供完整消息，分析整体
    if full_message:
        dimensions["full_message_analysis"] = _analyze_full_message(full_message, industry)
    
    # 生成反馈和建议
    overall_feedback = _get_overall_feedback(total_score, dimensions)
    suggestions = _get_improvement_suggestions(dimensions)
    
    return {
        "input": {
            "subject": subject,
            "opening_hook": opening_hook,
            "value_proposition": value_proposition,
            "cta": cta,
            "industry": industry,
            "full_message": full_message
        },
        "total_score": round(total_score, 1) if total_score > 0 else None,
        "rating": _get_rating(total_score),
        "dimensions": dimensions,
        "overall_feedback": overall_feedback,
        "suggestions": suggestions
    }

def _score_subject(subject: str) -> float:
    """主题行评分"""
    score = 50  # 基础分
    
    # 长度检查
    if len(subject) <= 40:
        score += 10
    elif len(subject) <= 60:
        score += 5
    elif len(subject) > 80:
        score -= 10
    
    # 个性化检测
    if any(kw in subject.lower() for kw in ["您好", "hi", "hello", "dear"]):
        score += 5
    
    # 价值词检测
    value_keywords = ["免费", "赠送", "折扣", "方案", "策略", "建议", "insight", "tip", "guide", "free"]
    for kw in value_keywords:
        if kw in subject.lower():
            score += 5
            break
    
    # 疑问句检测
    if any(subject.endswith(p) for p in ["?", "？"]):
        score += 8
    
    # 数字检测
    import re
    if re.search(r'\d+', subject):
        score += 5
    
    return min(100, max(0, score))

def _score_hook(hook: str) -> float:
    """开头钩子评分"""
    score = 40  # 基础分
    
    if not hook:
        return 30
    
    # 长度适中
    if 30 <= len(hook) <= 100:
        score += 15
    elif len(hook) < 20:
        score -= 5
    elif len(hook) > 150:
        score -= 10
    
    # 钩子类型识别
    hook_types = {
        "问题式": ["发现", "是否", "有没有", "是否", "?"],
        "数据式": ["%", "增长", "减少", "研究", "显示", "data"],
        "引用式": ["据", "显示", "报告", "研究发现"],
        "痛点式": ["困难", "挑战", "问题", "困扰", "pain"],
        "利益式": ["帮助", "解决", "提升", "增加", "benefit"]
    }
    
    for htype, keywords in hook_types.items():
        for kw in keywords:
            if kw in hook.lower():
                score += 8
                break
    
    return min(100, max(0, score))

def _score_value_proposition(vp: str) -> float:
    """价值主张评分"""
    score = 45  # 基础分
    
    if not vp:
        return 30
    
    # 长度适中
    if 100 <= len(vp) <= 300:
        score += 15
    elif len(vp) < 50:
        score -= 10
    elif len(vp) > 500:
        score -= 10
    
    # 价值关键词
    value_keywords = ["帮助", "解决", "提升", "节省", "增加", "降低成本", "提高效率", 
                      "help", "solve", "improve", "save", "increase", "reduce"]
    for kw in value_keywords:
        if kw in vp.lower():
            score += 5
    
    # 具体性检测（数字、案例）
    import re
    if re.search(r'\d+%|\d+x|\d+倍|\d+天|\d+周|\d+年', vp):
        score += 10
    
    # 差异化检测
    diff_keywords = ["不同于", "相比", "独特", "唯一", "区别于", "unlike", "different", "unique"]
    for kw in diff_keywords:
        if kw in vp.lower():
            score += 8
            break
    
    return min(100, max(0, score))

def _score_cta(cta: str) -> float:
    """CTA评分"""
    score = 45  # 基础分
    
    if not cta:
        return 25
    
    # CTA关键词检测
    good_cta_keywords = ["安排", "预约", "获取", "下载", "schedule", "book", "get", "download",
                         "点击", "回复", "确认", "click", "reply", "confirm"]
    for kw in good_cta_keywords:
        if kw in cta.lower():
            score += 10
            break
    
    # 单一行动
    if cta.count('\n') <= 2:
        score += 5
    
    # 紧迫感
    urgency_keywords = ["限时", "今天", "本周", "尽快", "asap", "today", "this week"]
    for kw in urgency_keywords:
        if kw in cta.lower():
            score += 5
            break
    
    # 简洁性
    if len(cta) <= 50:
        score += 5
    
    return min(100, max(0, score))

def _analyze_full_message(message: str, industry: str) -> Dict:
    """完整消息分析"""
    analysis = {
        "length": len(message),
        "word_count": len(message.split()),
        "paragraphs": message.count('\n\n') + 1,
        "has_bullet_points": '•' in message or '-' in message or '*' in message,
        "has_numbers": bool(__import__('re').search(r'\d+', message)),
        "has_emoji": any(ord(c) > 127000 for c in message),
        "readability": _assess_readability(message)
    }
    return analysis

def _assess_readability(message: str) -> str:
    """评估可读性"""
    words = message.split()
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
    
    if avg_word_len < 4 and len(words) < 100:
        return "优秀 - 简洁易读"
    elif avg_word_len < 5 and len(words) < 150:
        return "良好 - 可读性较好"
    else:
        return "建议优化 - 适当精简内容"

def _get_subject_analysis(score: float) -> str:
    if score >= 80:
        return "主题行吸引力强，有个性化元素和价值承诺"
    elif score >= 60:
        return "主题行较好，建议优化长度和个性化"
    else:
        return "主题行吸引力不足，建议添加数字或个性化"

def _get_hook_analysis(score: float) -> str:
    if score >= 80:
        return "开头钩子有力，能快速抓住注意力"
    elif score >= 60:
        return "开头钩子尚可，建议更具针对性"
    else:
        return "开头钩子平淡，建议使用问题或数据开场"

def _get_vp_analysis(score: float) -> str:
    if score >= 80:
        return "价值主张清晰具体，有差异化优势"
    elif score >= 60:
        return "价值主张较清晰，建议补充数据支撑"
    else:
        return "价值主张不够突出，建议强化独特卖点"

def _get_cta_analysis(score: float) -> str:
    if score >= 80:
        return "CTA明确有力，引导行动清晰"
    elif score >= 60:
        return "CTA还行，建议增强紧迫感"
    else:
        return "CTA不够明确，建议简化并增强行动指引"

def _get_overall_feedback(score: float, dimensions: Dict) -> str:
    if score >= 80:
        return "整体表现优秀，是一封高效果的开发信"
    elif score >= 65:
        return "整体表现良好，部分维度可优化"
    elif score >= 50:
        return "整体表现中等，需要针对性优化"
    else:
        return "整体表现需要提升，建议根据反馈全面优化"

def _get_rating(score: float) -> str:
    if score >= 85:
        return "A+ (优秀)"
    elif score >= 75:
        return "A (良好)"
    elif score >= 60:
        return "B (中等)"
    elif score >= 45:
        return "C (及格)"
    else:
        return "D (需改进)"

def _get_improvement_suggestions(dimensions: Dict) -> List[str]:
    suggestions = []
    
    for key, dim in dimensions.items():
        if key == "full_message_analysis":
            continue
        if isinstance(dim, dict) and "score" in dim:
            if dim["score"] < 60:
                suggestions.append(f"建议优化{dim.get('name', key)}: {dim.get('analysis', '')}")
    
    if not suggestions:
        suggestions.append("消息整体质量良好，建议保持当前风格")
    
    return suggestions[:5]

def design_followup_sequence(
    industry: str = None,
    rounds: int = 5
) -> Dict:
    """跟进序列设计"""
    
    if rounds not in [3, 5, 7]:
        rounds = 5  # 默认5轮
    
    # 基础时间线
    timelines = {
        3: [1, 3, 7],      # 第1/3/7天
        5: [1, 3, 7, 14, 21],  # 更长跟进
        7: [1, 2, 4, 7, 14, 21, 30]  # 深度跟进
    }
    
    days = timelines.get(rounds, timelines[5])
    
    # 序列模板
    sequence_templates = [
        {
            "round": 1,
            "day": 0,
            "channel": "邮件",
            "purpose": "初次触达",
            "content_type": "个性化开发信",
            "key_elements": ["主题行个性化", "价值主张明确", "单一CTA"],
            "template_hint": "开头问候+发现客户需求+自身优势+行动邀请"
        },
        {
            "round": 2,
            "day": 3,
            "channel": "邮件",
            "purpose": "价值补充",
            "content_type": "案例分享/资源赠送",
            "key_elements": ["分享相关案例", "提供免费资源", "非销售导向"],
            "template_hint": "提及上次邮件+分享相关案例/报告+自然衔接"
        },
        {
            "round": 3,
            "day": 7,
            "channel": "LinkedIn",
            "purpose": "社交触达",
            "content_type": "连接邀请+简短留言",
            "key_elements": ["添加个性化备注", "说明连接价值", "简短有力"],
            "template_hint": "提及公司/共同点+连接价值+期待合作"
        },
        {
            "round": 4,
            "day": 14,
            "channel": "邮件",
            "purpose": "痛点提醒",
            "content_type": "问题引导型",
            "key_elements": ["提出行业痛点", "引导思考", "提供解决方案线索"],
            "template_hint": "行业挑战+可能的影响+引导回应"
        },
        {
            "round": 5,
            "day": 21,
            "channel": "邮件",
            "purpose": "最后通牒",
            "content_type": "温和收尾",
            "key_elements": ["表达理解", "保持友好", "留下后续联系方式"],
            "template_hint": "感谢+理解忙碌+保持联系+期待未来合作"
        },
        {
            "round": 6,
            "day": 30,
            "channel": "LinkedIn",
            "purpose": "内容互动",
            "content_type": "评论动态/分享内容",
            "key_elements": ["点赞/评论对方动态", "展现专业性", "自然互动"],
            "template_hint": "真诚互动+展示专业+自然提及"
        },
        {
            "round": 7,
            "day": 45,
            "channel": "邮件",
            "purpose": "长期维护",
            "content_type": "节日问候/市场资讯",
            "key_elements": ["节日祝福", "市场最新资讯", "不推销"],
            "template_hint": "节日问候+分享有价值资讯+保持联系"
        }
    ]
    
    sequence = []
    for i in range(rounds):
        if i < len(sequence_templates):
            template = sequence_templates[i].copy()
            template["day"] = days[i] if i < len(days) else days[-1] + (i - len(days) + 1) * 7
            sequence.append(template)
    
    return {
        "industry": industry or "通用",
        "total_rounds": rounds,
        "duration_days": days[-1] if days else 21,
        "sequence": sequence,
        "tips": [
            "每次跟进间隔不宜过短，避免骚扰感",
            "根据对方反应动态调整序列",
            "LinkedIn和邮件结合使用效果更好",
            "始终保持专业和尊重的态度"
        ]
    }

def match_industry_hooks(
    industry: str = None,
    product_type: str = None
) -> Dict:
    """行业钩子库匹配"""
    
    # 行业钩子库
    industry_hooks = {
        "制造业": [
            {"type": "数据式", "content": "制造业利润率平均提升15%的关键在于..."},
            {"type": "痛点式", "content": "还在为库存积压和交期延误头疼吗？"},
            {"type": "问题式", "content": "您的供应商是否经常出现质量问题？"},
            {"type": "案例式", "content": "某500强企业通过优化采购流程节省了30%成本"}
        ],
        "电商零售": [
            {"type": "数据式", "content": "旺季备货提前多少天能降低断货风险？"},
            {"type": "痛点式", "content": "同类产品竞争激烈，如何突出重围？"},
            {"type": "利益式", "content": "帮您找到提升店铺转化率的关键因素"},
            {"type": "引用式", "content": "根据最新电商报告，80%买家关注..."}
        ],
        "科技": [
            {"type": "趋势式", "content": "AI正在重塑供应链，您准备好了吗？"},
            {"type": "问题式", "content": "您的技术架构能否支撑业务高速增长？"},
            {"type": "数据式", "content": "数字化转型成功的客户平均ROI提升200%"},
            {"type": "对比式", "content": "传统方案vs智能方案，差距在哪里？"}
        ],
        "消费品": [
            {"type": "场景式", "content": "当消费者在货架前犹豫时，您的产品如何脱颖而出？"},
            {"type": "趋势式", "content": "Z世代消费偏好正在发生哪些变化？"},
            {"type": "数据式", "content": "2024年热门品类增长最快的三大趋势"},
            {"type": "痛点式", "content": "产品同质化严重，差异化从何做起？"}
        ],
        "通用": [
            {"type": "问题式", "content": "您是否正在寻找更可靠的合作伙伴？"},
            {"type": "价值式", "content": "我们能帮助您解决最关键的挑战"},
            {"type": "数据式", "content": "与同行相比，您的成本结构是否优化？"},
            {"type": "利益式", "content": "只需15分钟，可能为您节省大量时间和成本"}
        ]
    }
    
    # 选择匹配的行业钩子
    hooks_to_use = []
    
    if industry and industry in industry_hooks:
        hooks_to_use = industry_hooks[industry]
    elif product_type:
        # 模糊匹配
        for ind, hooks in industry_hooks.items():
            if any(kw in product_type for kw in ["电子", "科技", "数码"]):
                hooks_to_use = industry_hooks.get("科技", [])
                break
            elif any(kw in product_type for kw in ["服装", "家居", "礼品"]):
                hooks_to_use = industry_hooks.get("消费品", [])
                break
            elif any(kw in product_type for kw in ["机械", "设备", "工具"]):
                hooks_to_use = industry_hooks.get("制造业", [])
                break
    
    if not hooks_to_use:
        hooks_to_use = industry_hooks["通用"]
    
    return {
        "industry": industry or "通用",
        "product_type": product_type,
        "matched_hooks": hooks_to_use,
        "usage_tips": [
            "选择与目标客户痛点最相关的钩子",
            "钩子应与后续内容逻辑连贯",
            "避免过度使用数据式钩子，保持新鲜感",
            "可根据实际情况组合多种钩子类型"
        ],
        "hook_categories": ["问题式", "数据式", "痛点式", "利益式", "案例式", "趋势式", "引用式", "场景式", "对比式"]
    }

# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(
        description="云旅LinkedIn优化器 - B2B开发信优化工具"
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # score-message命令
    p_msg = subparsers.add_parser('score-message', help='开发信效果评分')
    p_msg.add_argument('--subject', help='主题行')
    p_msg.add_argument('--hook', help='开头钩子')
    p_msg.add_argument('--vp', help='价值主张')
    p_msg.add_argument('--cta', help='CTA行动号召')
    p_msg.add_argument('--industry', help='行业')
    p_msg.add_argument('--message', help='完整消息')
    
    # sequence-design命令
    p_seq = subparsers.add_parser('sequence-design', help='跟进序列设计')
    p_seq.add_argument('--industry', help='行业')
    p_seq.add_argument('--rounds', type=int, default=5, help='跟进轮数(3/5/7)')
    
    # hook-match命令
    p_hook = subparsers.add_parser('hook-match', help='行业钩子库匹配')
    p_hook.add_argument('--industry', help='行业')
    p_hook.add_argument('--product', help='产品类型')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'score-message':
        result = score_message(
            subject=args.subject,
            opening_hook=args.hook,
            value_proposition=args.vp,
            cta=args.cta,
            industry=args.industry,
            full_message=args.message
        )
    elif args.command == 'sequence-design':
        result = design_followup_sequence(
            industry=args.industry,
            rounds=args.rounds
        )
    elif args.command == 'hook-match':
        result = match_industry_hooks(
            industry=args.industry,
            product_type=args.product
        )
    else:
        print(f"未知命令: {args.command}")
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
