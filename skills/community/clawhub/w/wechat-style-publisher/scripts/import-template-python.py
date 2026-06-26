#!/usr/bin/env python3
"""Import intro/outro templates and layout styles from an existing WeChat article."""

import argparse
import json
import re
from datetime import datetime, UTC
from pathlib import Path

import httpx


def get_arg(namespace, *names):
    for name in names:
        value = getattr(namespace, name, None)
        if value not in [None, ""]:
            return value
    return None


def clean_html(html: str) -> str:
    return re.sub(r"<script\b[\s\S]*?</script>", "", html, flags=re.IGNORECASE)


def extract_style_blocks(html: str) -> str:
    matches = re.findall(r"<style\b[^>]*>([\s\S]*?)</style>", html, flags=re.IGNORECASE)
    return "\n".join(part.strip() for part in matches if part.strip())


def extract_article_html(html: str) -> str:
    patterns = [
        r'<div[^>]+id=["\']js_content["\'][^>]*>([\s\S]*?)</div>',
        r'<section[^>]+id=["\']js_content["\'][^>]*>([\s\S]*?)</section>',
        r'<div[^>]+class=["\'][^"\']*rich_media_content[^"\']*["\'][^>]*>([\s\S]*?)</div>',
        r"<article[^>]*>([\s\S]*?)</article>",
        r"<body[^>]*>([\s\S]*?)</body>",
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return html


def extract_blocks(html: str) -> list[str]:
    pattern = re.compile(
        r"<(p|section|blockquote|h1|h2|h3|h4|h5|h6|ul|ol|pre|table|figure|div)\b[^>]*>[\s\S]*?</\1>",
        flags=re.IGNORECASE,
    )
    blocks = []
    for match in pattern.finditer(html):
        block = match.group(0).strip()
        text_only = re.sub(r"<[^>]+>", " ", block)
        text_only = re.sub(r"\s+", " ", text_only).strip()
        if text_only:
            blocks.append(block)
    return blocks


def get_attribute_style(opening_tag: str) -> str:
    match = re.search(r'style=["\']([^"\']+)["\']', opening_tag, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def selector_rule(selector: str, style_text: str) -> str:
    return f"{selector} {{ {style_text} }}\n" if style_text else ""


def extract_style_profile(article_html: str, style_blocks: str) -> dict:
    title_tag = re.search(r"<h1\b[^>]*>", article_html, flags=re.IGNORECASE)
    h2_tag = re.search(r"<h2\b[^>]*>", article_html, flags=re.IGNORECASE)
    paragraph_tag = re.search(r"<p\b[^>]*>", article_html, flags=re.IGNORECASE)
    title_style = get_attribute_style(title_tag.group(0) if title_tag else "")
    heading_style = get_attribute_style(h2_tag.group(0) if h2_tag else "")
    paragraph_style = get_attribute_style(paragraph_tag.group(0) if paragraph_tag else "")
    extracted_css = "".join(
        [
            selector_rule(".wechat-content h1", title_style),
            selector_rule(".wechat-content h2", heading_style),
            selector_rule(".wechat-content p", paragraph_style),
        ]
    ).strip()
    custom_css = "\n".join(part for part in [extracted_css, style_blocks.strip()] if part).strip()
    return {
        "titleStyle": title_style,
        "headingStyle": heading_style,
        "paragraphStyle": paragraph_style,
        "customCss": custom_css,
    }


def find_edge_image(blocks: list[str], side: str) -> dict | None:
    window = blocks[:5] if side == "start" else blocks[-5:]
    for block in window:
        match = re.search(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', block, flags=re.IGNORECASE)
        if match:
            return {"src": match.group(1), "html": block}
    return None


def wrap_template(name: str, blocks: list[str]) -> str:
    klass = "wechat-intro" if name == "intro" else "wechat-outro"
    return f'<section class="{klass}">\n' + "\n".join(blocks) + "\n</section>\n"


def load_html(input_path: str, url: str) -> str:
    if input_path:
        return Path(input_path).read_text(encoding="utf-8")
    if url:
        response = httpx.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    raise ValueError("必须提供 --input 或 --url")


def load_registry(registry_path: str) -> dict:
    if not registry_path:
        return {"templates": {}}
    try:
        raw = Path(registry_path).read_text(encoding="utf-8")
        parsed = json.loads(raw)
        if "templates" in parsed:
            return parsed
    except Exception:
        pass
    return {"templates": {}}


def save_registry(registry_path: str, registry: dict) -> None:
    if registry_path:
        Path(registry_path).write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="从现有公众号文章导入模板变量")
    parser.add_argument("--input", default="", help="本地 HTML 文件")
    parser.add_argument("--html-file", default="", help="本地 HTML 文件，兼容别名")
    parser.add_argument("--file", default="", help="本地 HTML 文件，兼容别名")
    parser.add_argument("--url", default="", help="公众号文章 URL")
    parser.add_argument("--article-url", default="", help="公众号文章 URL，兼容别名")
    parser.add_argument("--link", default="", help="公众号文章 URL，兼容别名")
    parser.add_argument("--name", default="", help="模板变量名")
    parser.add_argument("--template-name", default="", help="模板变量名，兼容别名")
    parser.add_argument("--save-name", default="", help="模板变量名，兼容别名")
    parser.add_argument("--intro-count", type=int, default=3, help="头模板提取区块数")
    parser.add_argument("--header-blocks", type=int, default=0, help="头模板提取区块数，兼容别名")
    parser.add_argument("--outro-count", type=int, default=3, help="尾模板提取区块数")
    parser.add_argument("--footer-blocks", type=int, default=0, help="尾模板提取区块数，兼容别名")
    parser.add_argument("--intro-output", default="", help="头模板输出路径")
    parser.add_argument("--header-template-output", default="", help="头模板输出路径，兼容别名")
    parser.add_argument("--outro-output", default="", help="尾模板输出路径")
    parser.add_argument("--footer-template-output", default="", help="尾模板输出路径，兼容别名")
    parser.add_argument("--style-output", default="", help="样式输出路径")
    parser.add_argument("--css-output", default="", help="样式输出路径，兼容别名")
    parser.add_argument("--layout-style-output", default="", help="样式输出路径，兼容别名")
    parser.add_argument("--registry", default="", help="模板变量仓库 JSON")
    parser.add_argument("--template-registry", default="", help="模板变量仓库 JSON，兼容别名")
    parser.add_argument("--extract-mode", default="heuristic", help="heuristic 或 ai")
    parser.add_argument("--mode", default="", help="heuristic 或 ai，兼容别名")
    parser.add_argument("--analysis-output", default="", help="AI 辅助分析输出 JSON")
    parser.add_argument("--ai-analysis-output", default="", help="AI 辅助分析输出 JSON，兼容别名")
    args = parser.parse_args()

    input_path = get_arg(args, "input", "html_file", "file") or ""
    url = get_arg(args, "url", "article_url", "link") or ""
    template_name = get_arg(args, "name", "template_name", "save_name") or ""
    registry_path = get_arg(args, "registry", "template_registry") or ""
    intro_output = get_arg(args, "intro_output", "header_template_output") or ""
    outro_output = get_arg(args, "outro_output", "footer_template_output") or ""
    style_output = get_arg(args, "style_output", "css_output", "layout_style_output") or ""
    analysis_output = get_arg(args, "analysis_output", "ai_analysis_output") or ""
    mode = get_arg(args, "extract_mode", "mode") or "heuristic"
    intro_count = args.header_blocks or args.intro_count or (5 if mode == "ai" else 3)
    outro_count = args.footer_blocks or args.outro_count or (5 if mode == "ai" else 3)

    raw_html = load_html(input_path, url)
    cleaned_html = clean_html(raw_html)
    style_blocks = extract_style_blocks(cleaned_html)
    article_html = extract_article_html(cleaned_html)
    blocks = extract_blocks(article_html)
    if not blocks:
        raise ValueError("未找到可提取的文章区块")

    intro_html = wrap_template("intro", blocks[:intro_count])
    outro_html = wrap_template("outro", blocks[-outro_count:])
    style_profile = extract_style_profile(article_html, style_blocks)
    header_image = find_edge_image(blocks, "start")
    footer_image = find_edge_image(blocks, "end")
    analysis = {
        "mode": mode,
        "source": url or input_path,
        "introCandidateBlocks": blocks[: min(8, len(blocks))],
        "outroCandidateBlocks": blocks[max(0, len(blocks) - 8) :],
        "styleProfile": style_profile,
        "headerImage": header_image,
        "footerImage": footer_image,
    }

    if intro_output:
        Path(intro_output).write_text(intro_html, encoding="utf-8")
    else:
        print(intro_html)

    if outro_output:
        Path(outro_output).write_text(outro_html, encoding="utf-8")
    else:
        print(outro_html)

    if style_output:
        Path(style_output).write_text(style_profile["customCss"], encoding="utf-8")

    if analysis_output:
        Path(analysis_output).write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")

    if template_name:
        registry = load_registry(registry_path)
        registry["templates"][template_name] = {
            "name": template_name,
            "importedAt": datetime.now(UTC).isoformat(),
            "source": analysis["source"],
            "introHtml": intro_html,
            "outroHtml": outro_html,
            "customCss": style_profile["customCss"],
            "titleStyle": style_profile["titleStyle"],
            "headingStyle": style_profile["headingStyle"],
            "paragraphStyle": style_profile["paragraphStyle"],
            "headerImage": header_image,
            "footerImage": footer_image,
            "extractionMode": mode,
            "analysis": analysis,
        }
        save_registry(registry_path, registry)


if __name__ == "__main__":
    main()
