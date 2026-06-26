#!/usr/bin/env python3
"""
content-engine AI 配图提示词生成模块

为内容生成 AI 图片生成提示词，支持 Midjourney、DALL-E、Stable Diffusion 风格。
提供图片位置建议、SEO 友好的 alt text 生成、视觉内容规划等功能。
"""

import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

from utils import (
    load_input_data,
    output_error,
    output_success,
    parse_common_args,
)


# ============================================================
# 平台图片尺寸规格
# ============================================================

PLATFORM_IMAGE_SPECS = {
    "twitter": {
        "card": {"width": 1200, "height": 675, "ratio": "16:9", "label": "Twitter Card"},
        "profile": {"width": 400, "height": 400, "ratio": "1:1", "label": "头像"},
        "banner": {"width": 1500, "height": 500, "ratio": "3:1", "label": "横幅"},
        "in_stream": {"width": 1200, "height": 675, "ratio": "16:9", "label": "信息流图片"},
    },
    "linkedin": {
        "post": {"width": 1200, "height": 627, "ratio": "1.91:1", "label": "帖子配图"},
        "banner": {"width": 1128, "height": 191, "ratio": "5.9:1", "label": "公司横幅"},
        "article": {"width": 744, "height": 400, "ratio": "1.86:1", "label": "文章封面"},
    },
    "wechat": {
        "cover": {"width": 900, "height": 383, "ratio": "2.35:1", "label": "公众号封面"},
        "small_cover": {"width": 200, "height": 200, "ratio": "1:1", "label": "小图封面"},
        "article_image": {"width": 1080, "height": 720, "ratio": "3:2", "label": "文章配图"},
    },
    "blog": {
        "hero": {"width": 1200, "height": 630, "ratio": "1.91:1", "label": "Hero 大图"},
        "content": {"width": 800, "height": 450, "ratio": "16:9", "label": "正文配图"},
        "thumbnail": {"width": 400, "height": 300, "ratio": "4:3", "label": "缩略图"},
    },
    "medium": {
        "feature": {"width": 1400, "height": 788, "ratio": "16:9", "label": "特色图片"},
        "content": {"width": 700, "height": 394, "ratio": "16:9", "label": "正文配图"},
    },
}

# 图片风格模板
IMAGE_STYLE_TEMPLATES = {
    "professional": {
        "cn": "专业商务风格，简洁干净的背景，现代扁平设计",
        "en": "professional business style, clean minimal background, modern flat design",
    },
    "tech": {
        "cn": "科技感十足，蓝紫色调，数字化元素，未来感",
        "en": "tech-inspired, blue-purple color scheme, digital elements, futuristic",
    },
    "creative": {
        "cn": "创意艺术风格，大胆用色，抽象元素",
        "en": "creative artistic style, bold colors, abstract elements",
    },
    "minimal": {
        "cn": "极简风格，大量留白，少量元素，优雅排版",
        "en": "minimalist style, lots of white space, few elements, elegant typography",
    },
    "warm": {
        "cn": "温暖亲和风格，暖色调，自然光影，生活化场景",
        "en": "warm and friendly style, warm tones, natural lighting, lifestyle scene",
    },
    "illustration": {
        "cn": "手绘插画风格，线条流畅，色彩丰富",
        "en": "hand-drawn illustration style, smooth lines, rich colors",
    },
}


# ============================================================
# 辅助函数
# ============================================================

def _extract_key_concepts(text: str) -> List[str]:
    """从文本中提取关键概念词。

    通过简单的规则提取：
    - 粗体文本 **keyword**
    - 标题文本 # heading
    - 引号内文本 「keyword」
    - 频繁出现的名词短语

    Args:
        text: 内容正文。

    Returns:
        关键概念词列表。
    """
    concepts = []

    # 提取粗体文本
    bold = re.findall(r"\*\*(.+?)\*\*", text)
    concepts.extend(bold[:5])

    # 提取标题
    headings = re.findall(r"^#{1,3}\s+(.+)$", text, re.MULTILINE)
    concepts.extend(headings[:5])

    # 提取引号内容
    quoted_cn = re.findall(r"[「『](.+?)[」』]", text)
    quoted_en = re.findall(r'"(.+?)"', text)
    concepts.extend(quoted_cn[:3])
    concepts.extend(quoted_en[:3])

    # 去重保序
    seen = set()
    unique = []
    for c in concepts:
        c = c.strip()
        if c and c not in seen:
            seen.add(c)
            unique.append(c)

    return unique[:10]


def _detect_content_theme(text: str, title: str = "") -> str:
    """检测内容主题以选择图片风格。

    Args:
        text: 内容正文。
        title: 内容标题。

    Returns:
        风格标识符（如 "tech", "professional" 等）。
    """
    combined = (title + " " + text).lower()

    # 主题关键词映射
    theme_keywords = {
        "tech": ["ai", "人工智能", "编程", "代码", "开发", "技术", "api",
                 "算法", "数据", "机器学习", "深度学习", "cloud", "云",
                 "python", "javascript", "react", "agent", "llm"],
        "professional": ["商业", "管理", "策略", "营销", "品牌", "企业",
                         "领导力", "团队", "business", "marketing", "strategy",
                         "leadership", "management"],
        "creative": ["设计", "创意", "艺术", "灵感", "design", "creative",
                     "art", "inspiration", "ui", "ux"],
        "warm": ["生活", "成长", "分享", "故事", "心得", "感悟",
                 "lifestyle", "growth", "story", "personal"],
        "minimal": ["效率", "极简", "工具", "方法", "productivity",
                    "minimal", "tools", "workflow"],
    }

    scores: Dict[str, int] = {}
    for theme, keywords in theme_keywords.items():
        score = sum(1 for kw in keywords if kw in combined)
        scores[theme] = score

    if scores:
        best = max(scores, key=lambda k: scores[k])
        if scores[best] > 0:
            return best

    return "professional"


def _build_image_prompt(
    description: str,
    style: str = "professional",
    aspect_ratio: str = "16:9",
    language: str = "both",
) -> Dict[str, str]:
    """构建 AI 图片生成提示词。

    Args:
        description: 图片内容描述。
        style: 风格标识符。
        aspect_ratio: 宽高比。
        language: 输出语言（"cn", "en", "both"）。

    Returns:
        包含中英文提示词的字典。
    """
    style_info = IMAGE_STYLE_TEMPLATES.get(style, IMAGE_STYLE_TEMPLATES["professional"])

    # 英文提示词（适配 Midjourney/DALL-E/SD）
    en_prompt = (
        f"{description}, {style_info['en']}, "
        f"high quality, detailed, {aspect_ratio} aspect ratio, "
        f"4k resolution, sharp focus"
    )

    # 中文提示词
    cn_prompt = (
        f"{description}，{style_info['cn']}，"
        f"高质量，细节丰富，{aspect_ratio} 比例"
    )

    result = {}
    if language in ("en", "both"):
        result["en"] = en_prompt
    if language in ("cn", "both"):
        result["cn"] = cn_prompt

    return result


# ============================================================
# 操作：生成图片提示词
# ============================================================

def generate_prompt(data: Dict[str, Any]) -> None:
    """根据内容文本生成 AI 图片生成提示词。

    必填字段: text（内容文本或描述）
    可选字段: style（风格）, platform（目标平台）, type（图片类型）, title

    Args:
        data: 包含内容文本和选项的字典。
    """
    text = data.get("text", "")
    if not text:
        output_error("内容文本（text）为必填字段", code="VALIDATION_ERROR")
        return

    title = data.get("title", "")
    style = data.get("style", "")
    platform = data.get("platform", "").lower()
    img_type = data.get("type", "content")

    # 自动检测风格
    if not style:
        style = _detect_content_theme(text, title)

    # 提取关键概念
    concepts = _extract_key_concepts(text)

    # 获取平台图片规格
    specs = {}
    if platform and platform in PLATFORM_IMAGE_SPECS:
        platform_specs = PLATFORM_IMAGE_SPECS[platform]
        if img_type in platform_specs:
            specs = platform_specs[img_type]
        else:
            # 使用第一个可用规格
            first_key = list(platform_specs.keys())[0]
            specs = platform_specs[first_key]

    aspect_ratio = specs.get("ratio", "16:9")

    # 构建描述
    description = title if title else text[:100]
    if concepts:
        concept_str = ", ".join(concepts[:3])
        description = f"{description} — featuring: {concept_str}"

    prompt = _build_image_prompt(description, style, aspect_ratio)

    result = {
        "message": "已生成图片提示词",
        "prompts": prompt,
        "style": style,
        "style_description": IMAGE_STYLE_TEMPLATES.get(style, {}),
        "key_concepts": concepts,
    }

    if specs:
        result["recommended_size"] = specs
        result["platform"] = platform

    output_success(result)


# ============================================================
# 操作：建议图片位置
# ============================================================

def suggest_images(data: Dict[str, Any]) -> None:
    """分析内容文本，建议在哪些位置放置图片以及图片内容。

    必填字段: text（完整内容文本）
    可选字段: title, style, max_suggestions（最大建议数，默认 5）

    Args:
        data: 包含内容文本的字典。
    """
    text = data.get("text", "")
    if not text:
        output_error("内容文本（text）为必填字段", code="VALIDATION_ERROR")
        return

    title = data.get("title", "")
    style = data.get("style", "") or _detect_content_theme(text, title)
    max_suggestions = data.get("max_suggestions", 5)

    suggestions = []

    # 1. 文章开头 — Hero 图片
    suggestions.append({
        "position": "文章开头",
        "position_type": "hero",
        "reason": "吸引读者注意力，建立文章视觉基调",
        "description": f"文章主题「{title or text[:30]}」的概念图",
        "prompts": _build_image_prompt(
            f"Hero image for article about {title or text[:50]}",
            style, "16:9",
        ),
    })

    # 2. 按段落/标题分析内容，在关键段落后建议配图
    sections = re.split(r"(?=^#{1,3}\s+)", text, flags=re.MULTILINE)
    section_index = 0

    for section in sections:
        if len(suggestions) >= max_suggestions:
            break

        section = section.strip()
        if not section:
            continue

        # 提取段落标题
        heading_match = re.match(r"^#{1,3}\s+(.+)$", section, re.MULTILINE)
        if heading_match:
            heading = heading_match.group(1).strip()
            section_body = section[heading_match.end():].strip()

            # 检查段落是否足够长（值得配图）
            if len(section_body) > 100:
                section_concepts = _extract_key_concepts(section_body)
                desc = f"Illustration for section: {heading}"
                if section_concepts:
                    desc += f" — {', '.join(section_concepts[:2])}"

                suggestions.append({
                    "position": f"「{heading}」章节后",
                    "position_type": "section",
                    "reason": f"为「{heading}」章节提供视觉解释",
                    "description": desc,
                    "prompts": _build_image_prompt(desc, style, "16:9"),
                })

            section_index += 1

    # 3. 检查是否有列表/步骤（适合信息图）
    list_items = re.findall(r"^\d+\.\s+(.+)$", text, re.MULTILINE)
    if len(list_items) >= 3 and len(suggestions) < max_suggestions:
        items_str = ", ".join(list_items[:5])
        suggestions.append({
            "position": "步骤/列表区域",
            "position_type": "infographic",
            "reason": "将步骤或列表可视化为信息图",
            "description": f"Infographic showing steps: {items_str}",
            "prompts": _build_image_prompt(
                f"Clean infographic with numbered steps: {items_str}",
                "minimal", "4:3",
            ),
        })

    # 4. 代码块区域建议截图/示意图
    code_blocks = re.findall(r"```(\w*)\n[\s\S]*?```", text)
    if code_blocks and len(suggestions) < max_suggestions:
        lang = code_blocks[0] if code_blocks[0] else "code"
        suggestions.append({
            "position": "代码块附近",
            "position_type": "code_illustration",
            "reason": "为代码段提供视觉说明或运行效果展示",
            "description": f"Technical illustration related to {lang} code",
            "prompts": _build_image_prompt(
                f"Clean technical diagram or screenshot showing {lang} code output",
                "tech", "16:9",
            ),
        })

    # 5. 文章结尾 — CTA 图片
    if len(suggestions) < max_suggestions:
        suggestions.append({
            "position": "文章结尾",
            "position_type": "cta",
            "reason": "在文章结尾添加行动号召配图",
            "description": f"Call-to-action image for {title or 'the article'}",
            "prompts": _build_image_prompt(
                f"Engaging call-to-action image, inviting and motivational",
                "warm", "16:9",
            ),
        })

    output_success({
        "message": f"为文章建议了 {len(suggestions)} 处配图位置",
        "style": style,
        "suggestions": suggestions[:max_suggestions],
    })


# ============================================================
# 操作：生成 alt text
# ============================================================

def format_alt_text(data: Dict[str, Any]) -> None:
    """为图片生成 SEO 友好的 alt text。

    必填字段: description（图片描述）或 images（图片描述列表）
    可选字段: context（文章上下文）, keywords（SEO 关键词）

    Args:
        data: 包含图片描述的字典。
    """
    description = data.get("description", "")
    images = data.get("images", [])
    context = data.get("context", "")
    keywords = data.get("keywords", [])

    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    if not description and not images:
        output_error("图片描述（description）或图片列表（images）为必填字段", code="VALIDATION_ERROR")
        return

    results = []

    # 处理单个描述
    if description and not images:
        images = [{"description": description}]

    # 处理图片列表
    for img in images:
        if isinstance(img, str):
            img = {"description": img}
        desc = img.get("description", "")
        if not desc:
            continue

        # 生成 alt text
        alt_text_cn = _generate_alt_text(desc, keywords, "cn", context)
        alt_text_en = _generate_alt_text(desc, keywords, "en", context)

        results.append({
            "original_description": desc,
            "alt_text_cn": alt_text_cn,
            "alt_text_en": alt_text_en,
            "seo_keywords_included": [k for k in keywords if k.lower() in alt_text_en.lower() or k in alt_text_cn],
        })

    output_success({
        "message": f"已为 {len(results)} 张图片生成 alt text",
        "alt_texts": results,
    })


def _generate_alt_text(description: str, keywords: List[str], lang: str, context: str = "") -> str:
    """生成单张图片的 alt text。

    规则:
    - 长度控制在 60-120 字符
    - 包含关键信息和 SEO 关键词
    - 描述性且准确

    Args:
        description: 图片描述。
        keywords: SEO 关键词列表。
        lang: 语言（"cn" 或 "en"）。
        context: 文章上下文。

    Returns:
        alt text 字符串。
    """
    # 清理描述
    desc = description.strip()
    desc = re.sub(r"\s+", " ", desc)

    # 截断到合理长度
    if len(desc) > 100:
        desc = desc[:97] + "..."

    # 尝试包含关键词
    if keywords:
        kw_str = "、".join(keywords[:2]) if lang == "cn" else ", ".join(keywords[:2])
        if lang == "cn":
            alt = f"{desc} — {kw_str}"
        else:
            alt = f"{desc} — {kw_str}"
    else:
        alt = desc

    # 确保长度合理
    if len(alt) > 125:
        alt = alt[:122] + "..."

    return alt


# ============================================================
# 操作：视觉内容规划
# ============================================================

def image_plan(data: Dict[str, Any]) -> None:
    """为文章创建完整的视觉内容规划。

    必填字段: text（文章正文）
    可选字段: title, platforms（目标平台列表）, style

    为每个目标平台生成：
    - Hero 大图提示词
    - 章节配图提示词
    - 社交媒体分享缩略图提示词

    Args:
        data: 包含文章内容的字典。
    """
    text = data.get("text", "")
    if not text:
        output_error("文章正文（text）为必填字段", code="VALIDATION_ERROR")
        return

    title = data.get("title", "")
    platforms = data.get("platforms", ["blog"])
    style = data.get("style", "") or _detect_content_theme(text, title)

    if isinstance(platforms, str):
        platforms = [p.strip() for p in platforms.split(",") if p.strip()]

    concepts = _extract_key_concepts(text)

    plan = {
        "title": title or "未命名文章",
        "style": style,
        "key_concepts": concepts,
        "images": [],
    }

    # 1. Hero 图片（各平台尺寸）
    hero_desc = f"Hero image: {title or text[:50]}"
    if concepts:
        hero_desc += f", featuring {', '.join(concepts[:2])}"

    hero_item = {
        "name": "Hero 大图",
        "type": "hero",
        "description": hero_desc,
        "prompts": _build_image_prompt(hero_desc, style, "16:9"),
        "platform_sizes": {},
    }
    for p in platforms:
        p_lower = p.lower()
        if p_lower in PLATFORM_IMAGE_SPECS:
            specs = PLATFORM_IMAGE_SPECS[p_lower]
            # 选择最适合 hero 的规格
            for key in ["hero", "feature", "cover", "card", "post"]:
                if key in specs:
                    hero_item["platform_sizes"][p_lower] = specs[key]
                    break
    plan["images"].append(hero_item)

    # 2. 章节配图
    headings = re.findall(r"^#{1,3}\s+(.+)$", text, re.MULTILINE)
    for i, heading in enumerate(headings[:4]):  # 最多 4 个章节配图
        section_desc = f"Section illustration: {heading}"
        section_item = {
            "name": f"章节配图 — {heading}",
            "type": "section",
            "description": section_desc,
            "prompts": _build_image_prompt(section_desc, style, "16:9"),
            "platform_sizes": {},
        }
        for p in platforms:
            p_lower = p.lower()
            if p_lower in PLATFORM_IMAGE_SPECS:
                specs = PLATFORM_IMAGE_SPECS[p_lower]
                for key in ["content", "article_image", "in_stream"]:
                    if key in specs:
                        section_item["platform_sizes"][p_lower] = specs[key]
                        break
        plan["images"].append(section_item)

    # 3. 社交媒体分享缩略图
    share_desc = f"Social media thumbnail: {title or text[:30]}"
    share_item = {
        "name": "社交媒体分享缩略图",
        "type": "thumbnail",
        "description": share_desc,
        "prompts": _build_image_prompt(
            f"Eye-catching social media thumbnail, {title or text[:30]}, "
            f"clear text space, bold visual",
            style, "1.91:1",
        ),
        "platform_sizes": {},
    }
    for p in platforms:
        p_lower = p.lower()
        if p_lower in PLATFORM_IMAGE_SPECS:
            specs = PLATFORM_IMAGE_SPECS[p_lower]
            for key in ["card", "thumbnail", "small_cover", "post"]:
                if key in specs:
                    share_item["platform_sizes"][p_lower] = specs[key]
                    break
    plan["images"].append(share_item)

    # 4. 汇总平台规格参考
    all_specs = {}
    for p in platforms:
        p_lower = p.lower()
        if p_lower in PLATFORM_IMAGE_SPECS:
            all_specs[p_lower] = PLATFORM_IMAGE_SPECS[p_lower]

    plan["platform_specs_reference"] = all_specs
    plan["total_images"] = len(plan["images"])

    output_success({
        "message": f"已生成视觉内容规划（共 {plan['total_images']} 张图片）",
        "plan": plan,
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("content-engine AI 配图助手")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "generate-prompt": lambda: generate_prompt(data or {}),
        "suggest-images": lambda: suggest_images(data or {}),
        "format-alt-text": lambda: format_alt_text(data or {}),
        "image-plan": lambda: image_plan(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
