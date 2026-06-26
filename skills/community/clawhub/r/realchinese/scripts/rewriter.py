"""
RealChinese — 8-platform style rewriter.
Reference implementation v1.1.2 | MIT License

Usage:
    from rewriter import rewrite
    result = rewrite("AI写的文字", platform="小红书")
    print(result)
"""

import re
import random
from typing import Optional


# ── Platform Style Definitions ─────────────────────────────

PLATFORM_STYLES = {
    "公众号": {
        "name": "微信公众号",
        "tone": "专业不端着",
        "rules": [
            "标题含钩子（数字/反问/冲突）",
            "首段不超过3行，快速进入话题",
            "段落间留白（空行分隔）",
            "文末加CTA（引导关注/评论/转发）",
            "每300字一个金句（加粗标注）",
        ],
        "hooks": [
            "99%的人不知道的{n}个{topic}真相",
            "我用{n}年才明白的{topic}道理",
            "为什么你的{topic}总是失败？",
        ],
        "cta": [
            "如果觉得有用，点个「在看」👇",
            "转发给需要的朋友 🔄",
            "关注我，每周分享干货 🎯",
        ],
    },
    "小红书": {
        "name": "小红书",
        "tone": "姐妹聊天感",
        "rules": [
            "emoji密度高（每2-3句一个）",
            "语气词丰富（真的、超、巨、贼、老）",
            "用'姐妹们'/'宝子们'开篇",
            "结尾加3-5个标签SEO",
            "分段用emoji代替标点",
            "每段不超过2行",
        ],
        "hooks": [
            "姐妹们！这个{topic}太绝了😭",
            "救命🆘 {topic}居然可以这样做",
            "任何人没看过这个{topic}我都会伤心的OK？",
        ],
        "tags": [
            "#{topic}", "#干货分享", "#打工人必备",
            "#提升自己", "#效率工具", "#小红书助手",
        ],
    },
    "知乎": {
        "name": "知乎",
        "tone": "有理有据",
        "rules": [
            "开篇亮观点（一句话说清立场）",
            "引用数据/研究/案例支撑",
            "逻辑分点：第一...第二...第三...",
            "避免情绪化用词，保持理性",
            "结尾留讨论空间（你怎么看？）",
        ],
        "hooks": [
            "先说结论：{opinion}",
            "{topic}这个问题，我研究了{n}个案例后发现...",
            "大多数人搞错了{topic}的真正原因",
        ],
    },
    "抖音": {
        "name": "抖音",
        "tone": "快节奏钩子",
        "rules": [
            "前3秒必须出钩子（黄金3秒）",
            "短句为主（每句≤15字）",
            "节奏快：每2-3句留悬念",
            "多用反问、惊叹、对比制造冲突",
            "结尾引导互动（评论区见/你怎么看）",
        ],
        "hooks": [
            "你还在{action}？停下来！",
            "3秒学会{topic}🔥",
            "90%的人都搞错了{topic}",
        ],
    },
    "微博": {
        "name": "微博",
        "tone": "吃瓜闲聊",
        "rules": [
            "140字内尽量说清（适合快读）",
            "带话题标签 #topic#",
            "可以用网络流行语和梗",
            "结尾加「你怎么看」引导评论",
            "允许主观情绪和吐槽",
        ],
        "hooks": [
            "#{topic}# 这事我必须说两句...",
            "笑死，#{topic}# 评论区更精彩",
        ],
    },
    "豆瓣": {
        "name": "豆瓣",
        "tone": "文青细腻",
        "rules": [
            "用细腻的感官描写",
            "允许较长的句子和段落",
            "情感真实，不刻意正能量",
            "可以引用电影/书籍/音乐",
            "避免营销感（豆瓣用户极度敏感）",
        ],
    },
    "即刻": {
        "name": "即刻",
        "tone": "极客产品感",
        "rules": [
            "短平快（即刻是碎片化社区）",
            "产品经理视角叙事",
            "可加入技术细节和对比",
            "多用反问和'为什么'引导思考",
            "用'即友'称呼读者",
        ],
    },
    "B站": {
        "name": "B站",
        "tone": "Z世代up主",
        "rules": [
            "用二次元/游戏/鬼畜梗（适度）",
            "语气轻松幽默，自嘲加分",
            "弹幕友好的短句节奏",
            "结尾求三连（点赞+投币+收藏）",
            "加入'前方高能'/'划重点'等B站黑话",
        ],
        "hooks": [
            "各位观众老爷们好！今天聊聊{topic}",
            "{topic}到底怎么回事？我来扒一扒",
        ],
    },
}


# ── Deep Rewrite Engine (for complex texts) ────────────────

def _deep_restructure(text: str) -> str:
    """Deep structural rewrite: reorder paragraphs, vary sentence patterns."""
    paras = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 20]
    if len(paras) < 3:
        return text
    
    # Strategy 1: Move the "most interesting" paragraph to position 2
    # (breaks the "intro → body → conclusion" AI pattern)
    if len(paras) >= 4:
        # Find the paragraph with most concrete details (numbers, examples)
        scored = [(i, len(re.findall(r'\d+|[例如比如]|“|"', p)), p) for i, p in enumerate(paras)]
        scored.sort(key=lambda x: -x[1])
        if scored[0][0] > 1:  # Move an interesting para earlier
            para_list = list(paras)
            moved = para_list.pop(scored[0][0])
            para_list.insert(2, moved)
            paras = para_list
    
    # Strategy 2: Varied paragraph lengths
    for i, p in enumerate(paras):
        if i % 3 == 1 and len(p) > 80:  # Every 3rd para: break long ones
            sent_list = re.split(r'([。！？])', p)
            if len(sent_list) > 5:
                mid = len(sent_list) // 2
                if mid % 2 == 0:
                    mid += 1
                paras[i] = "".join(sent_list[:mid]) + "\n" + "".join(sent_list[mid:])
    
    # Strategy 3: Add rhetorical questions in long texts (>500 chars)
    if len(text) > 500:
        questions = [
            "你可能会问，这真的有用吗？",
            "说实话，你是不是也遇到过类似的情况？",
            "但你有没有想过，问题的根源在哪里？",
        ]
        if "？" not in paras[-1] and "?" not in paras[-1]:
            paras.append(random.choice(questions))
    
    return "\n\n".join(paras)


def _vary_sentence_starts(text: str) -> str:
    """Vary sentence starters to break AI uniformity."""
    sentences = re.split(r'([。！？\n])', text)
    if len(sentences) < 9:
        return text
    
    starters = [
        "另外", "同时", "因此", "不过", "而且", "所以", "但是", "然而",
        "例如", "比如", "具体", "首先", "其次", "最后", "总之",
    ]
    replacements = {
        "另外": ["还有，", "对了，", "补充一下，"],
        "同时": ["另一方面，", "还有就是，", "顺带一提，"],
        "因此": ["所以，", "这意味着，", "说白了，"],
        "而且": ["更关键的是，", "更要命的是，", "更棒的是，"],
        "首先": ["先说第一点：", "第一，", "一来呢，"],
        "最后": ["最后想说的是：", "说了这么多，核心就一点：", "总结一下呗："],
    }
    
    for i in range(0, len(sentences)-4, 2):
        stripped = sentences[i].lstrip()
        for prefix in starters:
            if stripped.startswith(prefix):
                if prefix in replacements:
                    leading_ws = sentences[i][:len(sentences[i]) - len(stripped)]
                    after_prefix = stripped[len(prefix):].lstrip("，,。")
                    sentences[i] = leading_ws + random.choice(replacements[prefix]) + after_prefix
                break
    
    return "".join(sentences)


def deep_rewrite(text: str, platform: str = "小红书", topic: str = "") -> str:
    """Deep rewrite mode: structural transformation + surface polish.
    For complex texts where basic rewrite() is insufficient.
    """
    if platform not in PLATFORM_STYLES:
        return f"❌ 不支持的平台: {platform}。支持: {', '.join(PLATFORM_STYLES.keys())}"
    result = text
    
    # Phase 1: Structural transformation
    result = _deep_restructure(result)
    result = _vary_sentence_starts(result)
    
    # Phase 2: Surface polish (same as basic rewrite but with enhanced params)
    result = _remove_template_sentences(result)
    result = _shorten_sentences(result, platform)
    result = _add_human_markers(result, platform)
    result = _add_era_slang(result)
    
    # Inject stronger personality
    personality_markers = [
        "说句实话，", "我个人的体会是，", "踩过坑才敢这么说：",
        "这件事值得好好说说。", "不吹不黑，",
    ]
    if len(result) > 200:
        idx = result.find("\n\n")
        if idx > 0:
            result = result[:idx] + "\n\n" + random.choice(personality_markers) + result[idx+2:]
    
    result = _add_platform_hook(result, platform, topic)
    result = _add_emoji(result, platform)
    
    if platform == "B站":
        result = _add_bilibili_blackwords(result)
    
    result = result.replace("。\n，", "。\n").replace("。\n。", "。\n")
    result = _add_platform_cta(result, platform)
    
    if platform in ("小红书", "微博"):
        result = _add_tags(result, platform, topic)
    
    return result.strip()


def _remove_template_sentences(text: str) -> str:
    """Remove AI template patterns."""
    patterns = [
        r'值得注意[的的]是[，,].*?[。.]',
        r'需要强调[的的]是[，,].*?[。.]',
        r'不可忽视[的的]是[，,].*?[。.]',
        r'总而言之[,，].*?[。.]',
        r'综上所述[,，].*?[。.]',
        r'从某种角度[来来说看][,，].*?[。.]',
        r'在此基础[之上][,，].*?[。.]',
    ]
    for p in patterns:
        text = re.sub(p, '', text)
    # Remove "首先...其次...最后..." structure
    text = re.sub(r'首先[,，]', '', text)
    text = re.sub(r'其次[,，]', '另外，', text)
    text = re.sub(r'最后[,，]', '', text)
    return text.strip()


def _add_human_markers(text: str, platform: str) -> str:
    """Inject human speech markers appropriate for the platform."""
    markers_general = ["其实", "讲真", "说真的", "真的", "就是说", "说白了"]
    markers_xhs = ["真的", "超", "巨", "绝了", "救命", "天啊"]
    markers_weibo = ["笑死", "笑不活了", "我服了", "好吧"]
    markers_douyin = ["注意看", "划重点", "说白了", "记住"]

    marker_map = {
        "小红书": markers_xhs,
        "微博": markers_weibo,
        "抖音": markers_douyin,
    }

    markers = marker_map.get(platform, markers_general)
    # Insert 2-3 markers at random positions
    sentences = re.split(r'([。！？!?\n])', text)
    positions = [i for i in range(0, len(sentences), 2) if i < len(sentences) and len(sentences[i].strip()) > 10]
    if len(positions) > 3:
        positions = random.sample(positions, min(3, len(positions)))
    
    for pos in positions:
        marker = random.choice(markers)
        sentences[pos] = marker + "，" + sentences[pos].lstrip("，,。")
    
    return "".join(sentences)


def _add_era_slang(text: str) -> str:
    """Sprinkle era-appropriate slang."""
    slang = ["绝绝子", "YYDS", "显眼包", "真的很6", "太卷了", "狠狠get了"]
    # Replace one or two formal words with slang
    replacements = {
        "非常有效": "YYDS",
        "很好": "绝绝子",
        "很实用": "真的6",
    }
    for formal, s in replacements.items():
        if formal in text:
            text = text.replace(formal, s, 1)
            break
    return text


def _add_emoji(text: str, platform: str, density: str = "medium") -> str:
    """Add platform-appropriate emoji density."""
    emoji_map = {
        "小红书": ["😭", "🔥", "✨", "💡", "🆘", "🤯", "😱", "👍", "❤️", "👀"],
        "微博": ["🤔", "😂", "😅", "🙄", "💪", "👍"],
        "抖音": ["🔥", "⚡", "💯", "🎯", "😱", "👉"],
        "B站": ["🤣", "🙏", "🎉", "💪", "🤔", "👍"],
    }
    emojis = emoji_map.get(platform, ["✨", "💡", "👍"])
    
    # Insert emoji after every 2-3 sentences
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        result.append(line)
        if platform == "小红书" and i % 2 == 0 and line.strip():
            result[-1] = result[-1].rstrip() + " " + random.choice(emojis)
        elif i % 3 == 0 and platform != "小红书" and line.strip():
            result[-1] = result[-1].rstrip() + " " + random.choice(emojis)
    return "\n".join(result)


def _add_platform_hook(text: str, platform: str, topic: str = "") -> str:
    """Add platform-specific opening hook."""
    style = PLATFORM_STYLES.get(platform, {})
    hooks = style.get("hooks", [])
    if not hooks or not topic:
        return text
    
    hook = random.choice(hooks).format(topic=topic, n=random.choice([3, 5, 7, 10]), 
                                        action=random.choice(["手动操作", "手写", "复制粘贴"]),
                                        opinion=random.choice(["这个方向不对", "关键在细节", "多数人忽略了"]))
    return hook + "\n\n" + text


def _add_platform_cta(text: str, platform: str) -> str:
    """Add platform-specific call-to-action at the end."""
    style = PLATFORM_STYLES.get(platform, {})
    cta_list = style.get("cta", [])
    if cta_list:
        return text + "\n\n" + random.choice(cta_list)
    return text


def _add_tags(text: str, platform: str, topic: str = "") -> str:
    """Add SEO tags for platform."""
    style = PLATFORM_STYLES.get(platform, {})
    tags = style.get("tags", [])
    if not tags:
        return text
    tag_text = " ".join(t.format(topic=topic) for t in tags[:4])
    return text + "\n\n" + tag_text


def _shorten_sentences(text: str, platform: str) -> str:
    """Shorten sentences for fast-paced platforms."""
    if platform not in ("抖音", "即刻"):
        return text
    # Split long sentences at commas
    sentences = re.split(r'([。！？!?\n])', text)
    result = []
    for part in sentences:
        if len(part) > 25 and "，" in part:
            part = re.sub(r'，', '。\n', part)
        result.append(part)
    return "".join(result)


def _add_bilibili_blackwords(text: str) -> str:
    """Add B-station specific phrases."""
    phrases = ["前方高能！", "划重点：", "干货来了：", "记笔记！"]
    if "B站" in text or random.random() < 0.3:
        idx = text.find("\n\n")
        if idx > 0:
            return text[:idx] + "\n\n" + random.choice(phrases) + "\n" + text[idx+2:]
    return text


# ── Public API ─────────────────────────────────────────────

def rewrite(text: str, platform: str = "小红书", topic: str = "") -> str:
    """Rewrite AI-generated text for a specific Chinese platform.

    Args:
        text: The original AI-generated text
        platform: One of '公众号', '小红书', '知乎', '抖音', '微博', '豆瓣', '即刻', 'B站'
        topic: Optional topic keyword for hooks and tags

    Returns:
        Rewritten text in platform-native style
    """
    if platform not in PLATFORM_STYLES:
        return f"❌ 不支持的平台: {platform}。支持: {', '.join(PLATFORM_STYLES.keys())}"

    result = text

    # Step 1: Remove AI template patterns
    result = _remove_template_sentences(result)

    # Step 2: Shorten for fast-pace platforms
    result = _shorten_sentences(result, platform)

    # Step 3: Add human speech markers
    result = _add_human_markers(result, platform)

    # Step 4: Add era slang
    result = _add_era_slang(result)

    # Step 5: Add platform hook at the start
    result = _add_platform_hook(result, platform, topic)

    # Step 6: Add emoji
    result = _add_emoji(result, platform)

    # Step 7: Platform-specific tweaks
    if platform == "B站":
        result = _add_bilibili_blackwords(result)

    # Step 8: Clean up any grammar issues from sentence splitting
    result = result.replace("。\n，", "。\n").replace("。\n。", "。\n")
    
    # Step 9: Add CTA
    result = _add_platform_cta(result, platform)

    # Step 9: Add tags (for SEO platforms)
    if platform in ("小红书", "微博"):
        result = _add_tags(result, platform, topic)

    return result.strip()


def list_platforms() -> list:
    """Return available platform names."""
    return list(PLATFORM_STYLES.keys())


def platform_info(platform: str) -> dict:
    """Return platform style info."""
    return PLATFORM_STYLES.get(platform, {})


# ── CLI ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python rewriter.py <text> <platform> [topic]")
        print("       python rewriter.py --deep <text> <platform> [topic]")
        sys.exit(0)
    if sys.argv[1] == "--deep":
        text, plat = sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "小红书"
        topic = sys.argv[4] if len(sys.argv) > 4 else ""
        print(deep_rewrite(text, plat, topic))
    else:
        text, plat = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "小红书"
        topic = sys.argv[3] if len(sys.argv) > 3 else ""
        print(rewrite(text, plat, topic))
