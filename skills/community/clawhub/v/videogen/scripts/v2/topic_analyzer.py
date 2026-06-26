#!/usr/bin/env python3
"""
videogen v2 — Topic Analyzer & Mode Selector
根据选题自动判断最适合的内容模式：
  Mode A: 纯干货型（知识讲解、数据驱动）
  Mode B: 剧情+科普型（情感开场 + 干货正文）
  Mode C: 漫剧型（全程角色驱动，适合强情感/故事主题）
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Literal

# ─── 内容模式定义 ───

MODES = Literal["A", "B", "C"]
"""
Mode A — 纯干货型
  特点：直接讲述，逻辑清晰，数据图表丰富
  适用：财经分析、技术教程、行业报告、数据解读
  结构：开场痛点 → 核心要点 × 3 → 金句收尾
  视觉：PPT/图表为主，AI点缀关键帧

Mode B — 剧情+科普型
  特点：有一个角色/人物困境开场引人，共情后进入干货
  适用：职业发展、认知升级、社会洞察、励志干货
  结构：角色剧情钩子 → 问题拆解 → 解决方案 → 升华
  视觉：剧情画面 + 干净科普画面混合

Mode C — 漫剧型
  特点：全程角色/故事驱动，强情感，强戏剧冲突
  适用：人生转折、励志逆袭、人情冷暖、情感故事
  结构：完整故事弧（起承转合）
  视觉：角色一致画面为主，剧情场景连贯
"""

@dataclass
class AnalysisResult:
    mode: MODES
    confidence: float  # 0.0–1.0
    reasoning: str
    suggested_hooks: list[str]  # 推荐的开场钩子类型
    mode_description: str


# ─── 关键词/模式识别 ───

# 强剧情/情感驱动 → Mode C
DRAMA_KEYWORDS = [
    # 人生状态
    r"失业", r"裁员", r"失业后", r"找工作", r"面试失败", r"被辞退",
    r"创业失败", r"破产", r"负债", r"还债",
    # 情感关系
    r"分手", r"离婚", r"离婚后", r"复合", r"暗恋", r"表白", r"异地恋",
    r"父母", r"原生家庭", r"亲子", r"婆媳",
    # 励志逆袭
    r"逆袭", r"翻身", r"从零到", r"从一无所有", r"从负债", r"草根",
    r"普通人如何", r"月薪.*万", r"存款.*万", r"第.*年",
    # 强烈情绪
    r"崩溃", r"大哭", r"绝望", r"绝望中", r"最难的.*时候",
    r"人生.*低谷", r"至暗", r"最黑暗",
    # 具体故事场景
    r"讲述.*经历", r".*的自述", r".*的故事", r"我.*岁时",
    r"那年.*我", r"那一年",
]

# 剧情+干货混合 → Mode B
HYBRID_KEYWORDS = [
    # 职业发展
    r"职场", r"升职", r"加薪", r"辞职", r"转行", r"副业",
    r"自由职业", r"远程办公", r"打工.*还是", r"打工.*创业",
    # 认知升级
    r"认知", r"思维", r"格局", r"眼界", r"人间清醒",
    r"通透", r"活明白", r"看透", r"本质",
    # 社会洞察
    r"社会", r"人性", r"人情世故", r"潜规则", r"真相",
    r"为什么.*总是", r"越.*越", r"扎心",
    # 财经/商业洞察
    r"赚钱", r"财富", r"投资", r"理财", r"财务自由",
    r"商业", r"创业", r"生意", r"机会",
    # 关系/成长
    r"成长", r"提升", r"改变", r"进步", r"突破",
    r"人际关系", r"沟通", r"情商",
]

# 强干货型 → Mode A
KNOWLEDGE_KEYWORDS = [
    # 数据/事实类
    r"\d+[%％]", r"数据显示", r"研究表明", r"根据.*报告",
    r"数据分析", r"统计", r"排名", r"榜单",
    # 技术教程
    r"教程", r"如何.*步骤", r".*方法", r"技巧", r"攻略",
    r"入门", r"基础.*教学", r"使用.*方法", r"设置.*教程",
    # 知识讲解
    r"是什么", r"科普", r"原理", r"解释", r"概念",
    r"解读", r"分析", r"盘点", r"对比",
    # 行业报告类
    r"行业", r"趋势", r"报告", r"市场", r"赛道",
    r"202[0-9]", r"未来.*年",
]


def score_keyword_matches(text: str, patterns: list[str]) -> float:
    """返回匹配得分 (0.0–1.0)，考虑命中密度"""
    text_lower = text.lower()
    hits = 0
    for p in patterns:
        if re.search(p, text_lower):
            hits += 1
    if hits == 0:
        return 0.0
    # 归一化：3+命中趋向饱和
    return min(1.0, hits / 3.0)


def extract_topic_summary(text: str) -> str:
    """提取选题核心（去除语气词和冗余）"""
    text = re.sub(r"[吗呢吧呀啊呃嗯哦的呀咧哇嗨哼]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:100]


def analyze(url_or_text: str) -> AnalysisResult:
    """
    入口函数：分析 URL 或纯文本，判断最优内容模式。
    
    Returns AnalysisResult(mode, confidence, reasoning, suggested_hooks)
    """
    # 如果是 URL，尝试抓取页面文字
    raw_text = url_or_text
    if url_or_text.startswith("http"):
        try:
            import requests
            resp = requests.get(url_or_text, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            # 简单提取正文（去除 HTML 标签）
            import re as re2
            raw_text = re2.sub(r"<[^>]+>", " ", resp.text)
            raw_text = re2.sub(r"\s+", " ", raw_text)[:5000]
        except Exception:
            raw_text = url_or_text  # 降级

    text = raw_text.lower()

    # ─── 评分 ───
    score_drama  = score_keyword_matches(text, DRAMA_KEYWORDS)
    score_hybrid = score_keyword_matches(text, HYBRID_KEYWORDS)
    score_knowledge = score_keyword_matches(text, KNOWLEDGE_KEYWORDS)

    # 额外启发规则
    extra_drama = 0.0
    extra_hybrid = 0.0
    extra_knowledge = 0.0

    # 有第一人称叙事感 → C
    if re.search(r"我.*了|我的.*是|那年|那时候|当时|经历", text):
        extra_drama += 0.2
    # 有数据/百分比 → A
    if re.search(r"\d+[%％]", text):
        extra_knowledge += 0.15
    # 问句形式（如何、为什么）→ A 或 B
    if re.search(r"如何|怎么|为什么|是什么|教程", text):
        extra_hybrid += 0.1
        extra_knowledge += 0.1
    # 有对比反差（普通→厉害、之前→之后）→ C
    if re.search(r"之前.*之后|从.*到|原来.*现在", text):
        extra_drama += 0.25

    final_drama     = min(1.0, score_drama     + extra_drama)
    final_hybrid    = min(1.0, score_hybrid    + extra_hybrid)
    final_knowledge = min(1.0, score_knowledge + extra_knowledge)

    scores = {"A": final_knowledge, "B": final_hybrid, "C": final_drama}
    mode = max(scores, key=scores.get)
    confidence = scores[mode]

    # ─── 生成推荐钩子 ───
    hooks = generate_hooks(mode, text)

    # ─── 模式描述 ───
    descriptions = {
        "A": "纯干货型 — 直接讲述，数据/逻辑驱动，适合财经分析、技术教程、行业报告",
        "B": "剧情+科普型 — 角色共情开场 + 核心干货展开，兼顾情感与信息量",
        "C": "漫剧/剧情型 — 强角色、强情感、强冲突，适合励志逆袭、情感故事",
    }

    reasoning = (
        f"选题分析：剧情驱动={final_drama:.2f} | 混合型={final_hybrid:.2f} | 干货型={final_knowledge:.2f}。"
        f" 选中 Mode {mode}（置信度 {confidence:.2f}）"
    )

    return AnalysisResult(
        mode=mode,
        confidence=confidence,
        reasoning=reasoning,
        suggested_hooks=hooks,
        mode_description=descriptions[mode],
    )


def generate_hooks(mode: MODES, text: str) -> list[str]:
    """根据模式推荐开场钩子类型"""
    hooks_map = {
        "A": [
            "颠覆认知的数据",
            "一个反常识的结论",
            "行业内部数据曝光",
            "一个让人意外的真实案例",
        ],
        "B": [
            "一个普通人的故事",
            "一个职场/生活的典型困境",
            "一个认知反差场景",
            "一个让人思考的选择难题",
        ],
        "C": [
            "最低谷的那一刻",
            "一个戏剧化的转折点",
            "一段真实的内心独白",
            "命运的反转瞬间",
        ],
    }
    return hooks_map.get(mode, [])


def main():
    if len(sys.argv) < 2:
        print("用法: python topic_analyzer.py <选题文本或URL>")
        sys.exit(1)

    text = sys.argv[1]
    result = analyze(text)

    print(f"=== 选题模式分析结果 ===")
    print(f"推荐模式: Mode {result.mode}")
    print(f"置信度: {result.confidence:.2f}")
    print(f"推理: {result.reasoning}")
    print(f"推荐钩子类型: {result.suggested_hooks}")
    print(f"模式说明: {result.mode_description}")


if __name__ == "__main__":
    main()
