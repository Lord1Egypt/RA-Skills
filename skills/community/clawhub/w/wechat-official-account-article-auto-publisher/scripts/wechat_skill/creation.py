from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from .utils import normalize_whitespace

CreationMode = Literal["title_to_article", "rewrite"]
AudienceTone = Literal["professional", "sharp", "warm"]


@dataclass(frozen=True)
class CreationSpec:
    mode: CreationMode
    target_words_min: int = 1200
    target_words_max: int = 1500
    target_headings_min: int = 3
    target_headings_max: int = 5
    include_lead: bool = True
    include_summary: bool = True
    tone: AudienceTone = "professional"
    forbidden_patterns: tuple[str, ...] = (
        "总之",
        "综上所述",
        "在这个快速发展的时代",
        "首先我们来看看",
        "让我们一起来看",
    )


@dataclass(frozen=True)
class WritingBrief:
    title: str
    mode: CreationMode
    audience: str
    angle: str
    key_points: tuple[str, ...] = ()
    source_summary: str = ""
    source_constraints: tuple[str, ...] = ()
    tone: AudienceTone = "professional"


@dataclass
class ArticleCheckResult:
    word_count: int
    heading_count: int
    passes: bool
    warnings: list[str] = field(default_factory=list)


def _tone_phrases(tone: AudienceTone) -> dict[str, str]:
    mapping = {
        "professional": {
            "lead": "很多人讨论这个主题时，容易停留在表面判断，但真正决定结果的往往是更底层的结构变化。",
            "transition": "真正值得展开的，不是一个孤立现象，而是它背后的逻辑链条。",
            "close": "如果把这层逻辑看清，后续判断和动作就不会只停留在情绪层面。",
        },
        "sharp": {
            "lead": "大多数人以为自己在讨论趋势，实际上只是在复述热词。",
            "transition": "问题不在于观点够不够响亮，而在于你有没有抓住真正的矛盾点。",
            "close": "看不清这一点，越忙越容易把自己困在低价值动作里。",
        },
        "warm": {
            "lead": "很多人的焦虑并不来自变化本身，而是来自不知道该怎么理解这种变化。",
            "transition": "把复杂问题拆开以后，往往就会发现事情没有想象中那么无从下手。",
            "close": "真正重要的不是立刻做对所有事，而是先把方向看准。",
        },
    }
    return mapping[tone]


def _build_section_heading(title: str, index: int) -> str:
    defaults = [
        "先看清问题到底变在哪里",
        "再拆开背后的关键原因",
        "接着判断这对现实意味着什么",
        "最后想清楚具体该怎么做",
        "把长期价值落到今天的动作上",
    ]
    if index < len(defaults):
        return defaults[index]
    return f"核心问题 {index + 1}"


def _paragraphs_for_point(point: str, tone: AudienceTone, audience: str) -> list[str]:
    phrases = _tone_phrases(tone)
    normalized_point = normalize_whitespace(point)
    return [
        f"{phrases['lead']} 对于{audience}来说，{normalized_point}不是一个适合轻描淡写带过的话题，而是会直接影响判断方式和行动顺序的核心问题。",
        f"{phrases['transition']} 如果只把它理解成一个单点变化，文章就会停留在结论层；但一旦把原因、场景和后果连起来看，就会发现它其实对应着一整套更深的结构调整。",
        f"更具体一点说，{normalized_point}至少意味着两件事：过去那些看起来理所当然的工作方式正在被重新定价，而更稀缺的价值会越来越集中到判断、取舍和组织能力上。{phrases['close']}",
    ]


def _paragraphs_for_generic_section(heading: str, brief: WritingBrief) -> list[str]:
    phrases = _tone_phrases(brief.tone)
    return [
        f"{phrases['lead']} 围绕“{heading}”这一节，关键不是把观点说得更大，而是把逻辑拆得更清楚。对{brief.audience}来说，只有当问题被拆到可判断、可行动的层面，文章才真正有用。",
        f"{phrases['transition']} 公众号写作不是简单罗列事实，而是帮助读者迅速建立判断框架，知道哪些信号值得重视，哪些动作值得优先做。{phrases['close']}",
    ]


def generate_article_markdown(brief: WritingBrief, spec: CreationSpec | None = None, heading_count: int = 4) -> str:
    spec = spec or CreationSpec(mode=brief.mode, tone=brief.tone)
    heading_count = max(spec.target_headings_min, min(spec.target_headings_max, heading_count))
    phrases = _tone_phrases(brief.tone)

    lines: list[str] = [f"# {brief.title}", ""]
    lead = (
        f"导语：{phrases['lead']} 这篇文章想讲清楚的，是{brief.angle}。"
        f"如果你正好是{brief.audience}，那这不是一个只适合旁观的话题，而是值得尽快形成自己判断的现实问题。"
    )
    lines.extend([lead, ""])

    points = list(brief.key_points)
    while len(points) < heading_count:
        points.append(_build_section_heading(brief.title, len(points)))

    for index in range(heading_count):
        heading = points[index] if points[index] else _build_section_heading(brief.title, index)
        lines.append(f"## {heading}")
        lines.append("")

        if index < len(brief.key_points):
            paragraphs = _paragraphs_for_point(heading, brief.tone, brief.audience)
        else:
            paragraphs = _paragraphs_for_generic_section(heading, brief)

        for paragraph in paragraphs:
            lines.append(paragraph)
            lines.append("")

    conclusion = (
        f"## 结尾\n\n{phrases['lead']} 回到标题本身，真正关键的从来不是把话题说得更热闹，"
        f"而是让读者清楚知道：{brief.angle}。对{brief.audience}来说，越早把这个判断变成行动，越有机会在变化真正完成重排之前，先站到更有价值的位置上。"
    )
    lines.append(conclusion)
    return "\n".join(lines).strip() + "\n"


def infer_mode_from_request(request_text: str) -> CreationMode:
    text = request_text or ""
    rewrite_signals = ("改写", "重写", "参考", "基于这篇", "洗成", "仿照", "rewrite")
    if any(signal in text for signal in rewrite_signals):
        return "rewrite"
    return "title_to_article"


def infer_audience_from_request(request_text: str) -> str:
    text = request_text or ""
    audience_rules = [
        (("产品经理", "pm"), "产品经理和业务负责人"),
        (("创业", "创始人", "老板"), "创业者和中小团队管理者"),
        (("运营", "新媒体"), "运营和内容从业者"),
        (("职场", "打工人"), "普通职场人"),
        (("程序员", "开发", "技术"), "技术从业者和技术管理者"),
        (("ai", "人工智能"), "关注 AI 趋势与应用的公众号读者"),
    ]
    lowered = text.lower()
    for keywords, audience in audience_rules:
        if any(keyword in text or keyword in lowered for keyword in keywords):
            return audience
    return "关注行业趋势的微信公众号读者"


def infer_angle_from_request(request_text: str, mode: CreationMode) -> str:
    text = normalize_whitespace(request_text)
    if not text:
        return "找到一个清晰、有传播性的切口来展开"
    if "为什么" in text:
        return "围绕“为什么会这样”来拆解原因和后果"
    if "怎么" in text or "如何" in text:
        return "围绕“具体怎么做”来提供方法和动作建议"
    if "趋势" in text or "变化" in text:
        return "围绕趋势变化背后的结构性原因来展开"
    if mode == "rewrite":
        return "从一个更适合公众号传播的角度重写主题"
    return "找到一个清晰、有传播性的切口来展开"


def infer_key_points_from_request(request_text: str) -> tuple[str, ...]:
    text = request_text or ""
    segments = re.split(r"[，。；;、\n]", text)
    candidates: list[str] = []
    for segment in segments:
        cleaned = normalize_whitespace(segment)
        if not cleaned or len(cleaned) < 6:
            continue
        if any(trigger in cleaned for trigger in ("重点", "包括", "要讲", "讲清", "分析", "拆解", "原因", "建议", "案例", "写给", "适合")):
            candidates.append(cleaned)
            continue
        if any(trigger in cleaned for trigger in ("为什么", "怎么", "如何")):
            candidates.append(cleaned)
    unique: list[str] = []
    for item in candidates:
        if item not in unique:
            unique.append(item)
    return tuple(unique[:5])


def infer_brief_from_request(title: str, request_text: str, tone: AudienceTone = "professional") -> WritingBrief:
    mode = infer_mode_from_request(request_text)
    return WritingBrief(
        title=title,
        mode=mode,
        audience=infer_audience_from_request(request_text),
        angle=infer_angle_from_request(request_text, mode),
        key_points=infer_key_points_from_request(request_text),
        tone=tone,
    )


def estimate_chinese_word_count(text: str) -> int:
    cleaned = re.sub(r"\s+", "", text or "")
    return len(cleaned)


def count_markdown_headings(markdown_text: str) -> int:
    return len(re.findall(r"^##\s+", markdown_text or "", flags=re.M))


def extract_plain_markdown_text(markdown_text: str) -> str:
    text = re.sub(r"```.*?```", "", markdown_text or "", flags=re.S)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", "", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*]\s+", "", text, flags=re.M)
    return normalize_whitespace(text)


def build_creation_prompt(brief: WritingBrief, spec: CreationSpec | None = None) -> str:
    spec = spec or CreationSpec(mode=brief.mode, tone=brief.tone)
    lines = [
        "你正在为微信公众号写一篇可直接发布的中文文章。",
        f"任务模式：{'基于标题直接创作' if brief.mode == 'title_to_article' else '基于参考内容改写'}。",
        f"标题：{brief.title}",
        f"目标读者：{brief.audience}",
        f"文章切入角度：{brief.angle}",
        f"正文目标字数：{spec.target_words_min}-{spec.target_words_max} 字。",
        f"小标题数量：{spec.target_headings_min}-{spec.target_headings_max} 个二级标题。",
        "输出必须是 Markdown。",
        "结构必须包含：标题、导语、若干个二级小标题、结尾总结。",
        "文风要求：信息密度高、口语化但不油腻、适合公众号传播。",
        "避免空泛套话，不要堆砌正确但无信息量的句子。",
        "每个二级标题下都要有明确观点、解释和至少一个具体例子或场景。",
        "不要输出提示语、解释过程或额外说明，只输出最终文章。",
    ]

    if brief.key_points:
        lines.append("必须覆盖的关键点：")
        lines.extend([f"- {item}" for item in brief.key_points])

    if brief.source_summary:
        lines.append("参考内容摘要：")
        lines.append(brief.source_summary)

    if brief.source_constraints:
        lines.append("改写时必须保留的信息边界：")
        lines.extend([f"- {item}" for item in brief.source_constraints])

    if spec.forbidden_patterns:
        lines.append("尽量避免这些陈词滥调：")
        lines.extend([f"- {item}" for item in spec.forbidden_patterns])

    return "\n".join(lines)


def build_outline_template(title: str, heading_count: int = 4) -> str:
    heading_count = max(3, min(5, heading_count))
    outline = [f"# {title}", "", "导语：用 2-3 句话交代问题、冲突或价值。", ""]
    for index in range(1, heading_count + 1):
        outline.append(f"## 小标题 {index}")
        outline.append("这一节先抛观点，再解释原因，最后给例子或行动建议。")
        outline.append("")
    outline.append("## 结尾")
    outline.append("收束全文，回扣标题，并给出一个明确的判断或建议。")
    return "\n".join(outline).strip()


def validate_article(markdown_text: str, spec: CreationSpec | None = None) -> ArticleCheckResult:
    spec = spec or CreationSpec(mode="title_to_article")
    plain_text = extract_plain_markdown_text(markdown_text)
    word_count = estimate_chinese_word_count(plain_text)
    heading_count = count_markdown_headings(markdown_text)
    warnings: list[str] = []

    if word_count < spec.target_words_min:
        warnings.append(f"正文偏短，当前约 {word_count} 字，低于 {spec.target_words_min}。")
    if word_count > spec.target_words_max:
        warnings.append(f"正文偏长，当前约 {word_count} 字，高于 {spec.target_words_max}。")
    if heading_count < spec.target_headings_min:
        warnings.append(f"二级标题偏少，当前 {heading_count} 个，低于 {spec.target_headings_min}。")
    if heading_count > spec.target_headings_max:
        warnings.append(f"二级标题偏多，当前 {heading_count} 个，高于 {spec.target_headings_max}。")
    if spec.include_summary and "## 结尾" not in markdown_text and "## 总结" not in markdown_text:
        warnings.append("缺少明确的结尾总结小节。")
    if spec.include_lead and "导语" not in markdown_text[:120]:
        warnings.append("开头没有明显导语提示，建议增强开篇引导。")

    for pattern in spec.forbidden_patterns:
        if pattern and pattern in markdown_text:
            warnings.append(f"检测到套话表达：{pattern}")

    return ArticleCheckResult(
        word_count=word_count,
        heading_count=heading_count,
        passes=not warnings,
        warnings=warnings,
    )
