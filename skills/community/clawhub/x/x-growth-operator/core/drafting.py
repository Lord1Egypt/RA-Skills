from __future__ import annotations

import html
import re

from scripts.common import normalize_text


def clean_text(value: str) -> str:
    return " ".join(html.unescape(value or "").split())


def strip_leading_mentions(text: str) -> str:
    cleaned = clean_text(text)
    return re.sub(r"^(?:@\w+\s+)+", "", cleaned).strip()


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def infer_theme(text: str) -> str:
    lowered = clean_text(text).lower()
    if any(token in lowered for token in ("memory", "markdown", "weights", "context", "knowledge")) or any(
        token in text for token in ("记忆", "上下文", "知识")
    ):
        return "memory"
    if any(token in lowered for token in ("marketplace", "persona", "workflow", "team", "playbook")) or any(
        token in text for token in ("工作流", "团队", "方法论", "场景")
    ):
        return "workflow-market"
    if any(token in lowered for token in ("security", "safeguard", "phishing", "destructive", "guardrail")) or any(
        token in text for token in ("安全", "风控", "护栏", "攻击")
    ):
        return "safety"
    if any(token in lowered for token in ("video", "slop vibe", "movie", "image")) or any(
        token in text for token in ("视频", "图片", "内容")
    ):
        return "media"
    if any(token in lowered for token in ("gpu", "profit", "cost", "bill", "margin")) or any(
        token in text for token in ("利润", "成本", "营收", "转化")
    ):
        return "economics"
    return "general"


def detect_stance(text: str) -> str:
    lowered = clean_text(text).lower()
    if "real money" in lowered or "profit" in lowered or "mrr" in lowered or "roi" in lowered or any(
        token in text for token in ("收入", "利润", "变现", "roi", "转化")
    ):
        return "monetization"
    if "memory" in lowered or "markdown" in lowered or "weights" in lowered or any(
        token in text for token in ("记忆", "上下文", "知识")
    ):
        return "memory"
    if "marketplace" in lowered or "workflow" in lowered or "persona" in lowered or any(
        token in text for token in ("工作流", "场景", "流程")
    ):
        return "workflow-market"
    if "security" in lowered or "safeguard" in lowered or "guardrail" in lowered or any(
        token in text for token in ("安全", "风控", "护栏")
    ):
        return "safety"
    if "video" in lowered or "movie" in lowered or "image" in lowered or any(
        token in text for token in ("视频", "图片", "内容")
    ):
        return "media"
    return "general"


def extract_hooks(text: str) -> list[str]:
    cleaned = strip_leading_mentions(text)
    parts = re.split(r"[.!?。！？]\s*", cleaned)
    hooks = [part.strip(" .") for part in parts if len(part.strip()) > 24]
    return hooks[:3]


def summarize_hook(hook: str) -> str:
    cleaned = strip_leading_mentions(hook)
    lowered = cleaned.lower()
    if "i use it" in lowered or "i use" in lowered:
        return "operators are describing repeatable real-world usage"
    if cleaned.startswith(("but ", "yes ", "no ", "and ")):
        return ""
    if cleaned.startswith(("但是", "是的", "不是", "而且")):
        return ""
    words = cleaned.split()
    if len(words) < 5:
        return cleaned[:28].rstrip(" ,.;:!?")
    return " ".join(words[:10]).rstrip(" ,.;:!?")


def concise_cta(cta: str) -> str:
    normalized = clean_text(cta)
    if not normalized:
        return ""
    return normalized[0].upper() + normalized[1:]


def mission_topic_label(mission: dict) -> str:
    for field in ("primary_topics", "watch_keywords"):
        values = mission.get(field, [])
        if isinstance(values, list):
            for value in values:
                cleaned = clean_text(str(value))
                if cleaned:
                    return cleaned
    goal = clean_text(mission.get("goal", ""))
    return goal or "this space"


def mission_audience_label(mission: dict) -> str:
    audience = mission.get("audience", [])
    if isinstance(audience, list) and audience:
        return clean_text(str(audience[0]))
    return "the right audience"


def mission_goal_style(mission: dict) -> str:
    raw_goal = clean_text(mission.get("goal", ""))
    goal = raw_goal.lower()
    if contains_cjk(raw_goal):
        if any(token in raw_goal for token in ("线索", "报名", "转化", "销售", "营收")):
            return "把注意力连接到可验证的结果和明确下一步"
        if any(token in raw_goal for token in ("信任", "权威", "认知", "口碑")):
            return "用证据和细节建立可信度"
        if any(token in raw_goal for token in ("社区", "互动", "讨论")):
            return "制造有价值讨论并持续在场"
        if any(token in raw_goal for token in ("曝光", "可见度", "认知", "触达")):
            return "用清晰观点抓住时机并持续跟进"
        return "把注意力沉淀成可复用的增长结果"
    if any(token in goal for token in ("lead", "signup", "pipeline", "sale", "revenue", "demo")):
        return "connect attention to proof and a concrete next step"
    if any(token in goal for token in ("trust", "credibility", "authority", "position")):
        return "show evidence, specificity, and follow-through"
    if any(token in goal for token in ("community", "engagement", "discussion", "conversation")):
        return "create useful discussion and stay present in the thread"
    if any(token in goal for token in ("awareness", "visibility", "reach", "discover")):
        return "earn attention with a clear point of view and timely follow-up"
    return "turn attention into repeatable outcomes"


def topic_specific_angle(theme: str, stance: str) -> str:
    if theme == "general" and stance == "general":
        return "make the viewpoint specific enough to be actionable"
    if stance == "monetization":
        return "tie the conversation to measurable outcomes instead of vague interest"
    if theme == "memory":
        return "show how the idea changes actual decision-making, not just storage"
    if theme == "workflow-market":
        return "make the workflow repeatable instead of leaving it as a one-off insight"
    if theme == "safety":
        return "pair capability with clear controls and recovery paths"
    if theme == "economics":
        return "translate the shift into pricing, margin, or operating leverage"
    if theme == "media":
        return "connect the creative angle to why people will keep paying attention"
    return "turn the point of view into something specific, useful, and repeatable"


def topic_specific_angle_zh(theme: str, stance: str) -> str:
    if stance == "monetization":
        return "把讨论落到可衡量结果，而不是停留在抽象观点"
    if theme == "memory":
        return "说明它如何改变真实决策，而不只是多存一点信息"
    if theme == "workflow-market":
        return "把方法沉淀成可复用流程，而不是一次性灵感"
    if theme == "safety":
        return "把能力和边界、恢复机制一起讲清楚"
    if theme == "economics":
        return "把变化翻译成成本、利润或效率提升"
    if theme == "media":
        return "把内容亮点和持续关注理由连接起来"
    return "把观点讲到可执行、可验证"


def build_reply(mission: dict, theme: str, stance: str, hooks: list[str], source: str, include_question: bool, cta: str) -> tuple[str, str]:
    topic_label = mission_topic_label(mission)
    audience_label = mission_audience_label(mission)
    goal_style = mission_goal_style(mission)
    anchor = summarize_hook(hooks[0]) if hooks else "that point"
    if contains_cjk(mission.get("goal", "")) or contains_cjk(topic_label):
        draft = f"关键点在于：{anchor}。在{topic_label}这个方向，真正能打动{audience_label}的是持续做到“{goal_style}”。"
        draft += f" 更好的动作是：{topic_specific_angle_zh(theme, stance)}。"
        if include_question:
            draft += " 你觉得这里最该优先优化的信号是什么？"
        if cta:
            draft += f" {cta}"
        rationale = f"建议回复：{source} 当前讨论有动能，且 mission 偏向及时参与。"
    else:
        draft = (
            f"The key part is {anchor}. In {topic_label}, the accounts that win with {audience_label} are the ones that {goal_style}."
        )
        draft += f" The stronger move is to {topic_specific_angle(theme, stance)}."
        if include_question:
            draft += " What signal do you think matters most here?"
        if cta:
            draft += f" {cta}"
        rationale = f"Reply is favored because {source} already has momentum and the mission prefers timely participation."
    return draft, rationale


def build_quote(mission: dict, theme: str, stance: str, hooks: list[str], cta: str) -> tuple[str, str]:
    topic_label = mission_topic_label(mission)
    goal_style = mission_goal_style(mission)
    anchor = summarize_hook(hooks[0]) if hooks else "the core claim"
    if contains_cjk(mission.get("goal", "")) or contains_cjk(topic_label):
        draft = f"这条说对了核心：{anchor}。在{topic_label}里，更强的打法是“{goal_style}”。"
        draft += f" 这通常意味着你要先做到：{topic_specific_angle_zh(theme, stance)}。"
        if cta:
            draft += f" {cta}"
        rationale = "建议引用转发：机会强，且适合补一个更清晰的观点。"
    else:
        draft = f"What this gets right: {anchor}. In {topic_label}, the stronger move is to {goal_style}."
        draft += f" That usually means you need to {topic_specific_angle(theme, stance)}."
        if cta:
            draft += f" {cta}"
        rationale = "Quote post is favored because the opportunity is strong but benefits from adding a distinct point of view."
    return draft, rationale


def build_post(mission: dict, theme: str, stance: str, hooks: list[str], cta: str) -> tuple[str, str]:
    topic_label = mission_topic_label(mission)
    audience_label = mission_audience_label(mission)
    goal_style = mission_goal_style(mission)
    if contains_cjk(mission.get("goal", "")) or contains_cjk(topic_label):
        draft = f"一个判断：在{topic_label}里，真正会复利的增长来自“{goal_style}”。"
        draft += f" 最可能跑出来的团队，往往是那些能持续做到“{topic_specific_angle_zh(theme, stance)}”的人。"
        if hooks:
            draft += f" 当前市场信号是：{summarize_hook(hooks[0])}。"
        if cta:
            draft += f" {cta}"
        rationale = "建议发原创：话题匹配，但不需要强绑定单条源帖。"
    else:
        draft = f"Hot take: in {topic_label}, growth compounds when teams {goal_style}."
        draft += f" The winners with {audience_label} will be the ones that {topic_specific_angle(theme, stance)}."
        if hooks:
            draft += f" The market signal here is {summarize_hook(hooks[0])}."
        if cta:
            draft += f" {cta}"
        rationale = "Standalone post is favored because the topic is aligned but not urgent enough to attach to a single source post."
    return draft, rationale


def build_post_from_signal(mission: dict, theme: str, stance: str, hooks: list[str], cta: str) -> tuple[str, str]:
    topic_label = mission_topic_label(mission)
    audience_label = mission_audience_label(mission)
    goal_style = mission_goal_style(mission)
    anchor = summarize_hook(hooks[0]) if hooks else ""
    anchor_text = anchor or "operators are starting to describe concrete, repeatable usage"
    if contains_cjk(mission.get("goal", "")) or contains_cjk(topic_label):
        draft = f"最近越来越明显：在{topic_label}里，{anchor_text}。"
        draft += f" 能持续赢得{audience_label}的团队，本质上都在做“{goal_style}”。"
        draft += f" 可执行的优势在于：{topic_specific_angle_zh(theme, stance)}。"
        if cta:
            draft += f" {cta}"
        rationale = "建议改为原创：源信号有价值，但互动条件受限，不适合直接回复或引用。"
    else:
        draft = f"Seeing more evidence that in {topic_label}, {anchor_text}."
        draft += f" The teams that win with {audience_label} will be the ones that {goal_style}."
        draft += f" The practical edge is to {topic_specific_angle(theme, stance)}."
        if cta:
            draft += f" {cta}"
        rationale = "Standalone post is favored because the source signal is useful, but interaction readiness is too constrained for a direct reply or quote."
    return draft, rationale


def build_draft(mission: dict, opportunity: dict) -> tuple[str, str]:
    voice = mission.get("voice", "direct, clear, credible")
    cta = concise_cta(mission.get("cta", ""))
    source = opportunity.get("source_account", "the source")
    text = clean_text(opportunity.get("text", ""))
    action = opportunity.get("recommended_action", "observe")
    hints = opportunity.get("algorithm_hints", {})
    reply_window_open = bool(hints.get("reply_window_open"))
    interaction_readiness = hints.get("interaction_readiness", "open")
    theme = infer_theme(text)
    stance = detect_stance(text)
    hooks = extract_hooks(text)

    if action == "reply":
        draft, rationale = build_reply(mission, theme, stance, hooks, source, reply_window_open, cta)
    elif action == "quote_post":
        draft, rationale = build_quote(mission, theme, stance, hooks, cta)
    elif action == "post":
        if interaction_readiness in {"restricted", "thread_reply"}:
            draft, rationale = build_post_from_signal(mission, theme, stance, hooks, cta)
        else:
            draft, rationale = build_post(mission, theme, stance, hooks, cta)
    else:
        draft = ""
        rationale = "Observe is favored because the risk is too high or the fit is too weak."
        if contains_cjk(mission.get("goal", "")):
            rationale = "建议先观察：当前风险偏高或匹配度偏弱。"

    if hints.get("avoid_link_in_main_post"):
        rationale += " Keep any external link in a follow-up reply, not in the main post."
        if contains_cjk(mission.get("goal", "")):
            rationale += " 外链建议放在后续回复，不要放主帖。"

    notes = (
        f"Voice: {voice}. Theme: {theme}. Stance: {stance}. Source account: {source}. "
        f"Mission topic: {normalize_text(mission_topic_label(mission))}. Interaction readiness: {interaction_readiness}. "
        f"Source text summary: {text[:180]}"
    )
    return draft, f"{rationale} {notes}"
