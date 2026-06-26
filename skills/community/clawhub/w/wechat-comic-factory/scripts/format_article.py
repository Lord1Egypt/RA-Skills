from __future__ import annotations

import argparse
import json
import sys
from html import escape
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    SkillError,
    ensure_directory,
    get_wechat_access_token,
    load_config,
    normalize_display_text,
    read_json_file,
    read_text_file,
    setup_logger,
    update_json_file,
    wechat_upload_file,
)


def build_uploaded_mapping(assets_payload: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in assets_payload.get("article_image_uploads", []):
        if not isinstance(item, dict):
            continue
        remote_url = str(item.get("remote_url", "")).strip()
        if not remote_url:
            continue
        for key in ("local_path", "source_path"):
            path_value = str(item.get(key, "")).strip()
            if path_value:
                mapping[path_value] = remote_url
    return mapping


def upload_article_image(access_token: str, image_path: Path, logger) -> str:
    result = wechat_upload_file(
        access_token,
        "/media/uploadimg",
        image_path,
        logger=logger,
    )
    image_url = result.get("url")
    if not image_url:
        raise SkillError(
            "format_article",
            "微信正文图片上传成功，但接口未返回 url",
            details=result,
        )
    return image_url


def extract_markdown_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return normalize_display_text(stripped[2:])
    return ""


def extract_markdown_paragraphs(markdown_text: str) -> list[str]:
    paragraphs: list[str] = []
    buffer: list[str] = []
    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if not line:
            if buffer:
                paragraphs.append(normalize_display_text(" ".join(buffer)))
                buffer = []
            continue
        if line.startswith("# ") or line.startswith("!["):
            if buffer:
                paragraphs.append(normalize_display_text(" ".join(buffer)))
                buffer = []
            continue
        buffer.append(line)
    if buffer:
        paragraphs.append(normalize_display_text(" ".join(buffer)))
    return [item for item in paragraphs if item]


def prepare_article_payload(markdown_text: str, assets_payload: dict[str, Any]) -> dict[str, Any]:
    fallback_paragraphs = extract_markdown_paragraphs(markdown_text)
    title = normalize_display_text(assets_payload.get("title")) or extract_markdown_title(markdown_text)
    intro = normalize_display_text(assets_payload.get("intro"))
    ending = normalize_display_text(assets_payload.get("ending"))
    if not intro and fallback_paragraphs:
        intro = fallback_paragraphs[0]
    if not ending and len(fallback_paragraphs) > 1:
        ending = fallback_paragraphs[-1]

    images: list[dict[str, Any]] = []
    for image in assets_payload.get("images", []):
        if not isinstance(image, dict):
            continue
        images.append(
            {
                "index": int(image.get("index", len(images) + 1)),
                "caption": normalize_display_text(image.get("caption")),
                "source_path": str(image.get("source_path", "")).strip(),
                "wechat_path": str(image.get("wechat_path", "")).strip(),
            }
        )

    return {
        "title": title,
        "topic": normalize_display_text(assets_payload.get("topic")),
        "comic_type": normalize_display_text(assets_payload.get("comic_type")),
        "intro": intro,
        "ending": ending,
        "images": images,
    }


def resolve_branding(config: dict[str, Any] | None) -> dict[str, str]:
    defaults = (config or {}).get("defaults", {})
    brand_name = normalize_display_text(defaults.get("publisher_name")) or "心枢ai研习社"
    brand_tagline = (
        normalize_display_text(defaults.get("publisher_tagline"))
        or "AI 内容生产、漫画创作与公众号排版"
    )
    return {
        "publisher_name": brand_name,
        "publisher_tagline": brand_tagline,
    }


def render_paragraphs(text: str, style: str) -> str:
    paragraphs = [segment.strip() for segment in normalize_display_text(text).split("\n") if segment.strip()]
    return "".join(f'<p style="{style}">{escape(paragraph)}</p>' for paragraph in paragraphs)


def build_banner_section(title: str, subtitle: str) -> str:
    subtitle_html = (
        f'<section style="font-size:13px;color:#3d637e;letter-spacing:2px;line-height:1.8;'
        f'margin:0 0 10px 0;">{escape(subtitle)}</section>'
        if subtitle
        else ""
    )
    return f"""
<section style="padding-top:32px;">
  <section style="font-size:0;line-height:0;">
    <section style="display:inline-block;vertical-align:top;width:50%;background:#214c6e;height:30px;"></section>
    <section style="display:inline-block;vertical-align:top;width:20%;background:#fbf2d4;height:30px;"></section>
  </section>
  <section style="background:#ffffff;box-shadow:-5px 7px 20px rgba(0,0,0,0.12);margin:-12px auto 0 auto;width:84%;box-sizing:border-box;border-radius:14px;padding:28px 24px;text-align:center;">
    {subtitle_html}
    <h1 style="margin:0;color:#09385e;font-size:30px;line-height:1.55;font-weight:700;">{escape(title)}</h1>
  </section>
  <section style="font-size:0;line-height:0;text-align:right;">
    <section style="display:inline-block;vertical-align:top;width:20%;background:#fbf2d4;height:30px;"></section>
    <section style="display:inline-block;vertical-align:top;width:50%;background:#214c6e;height:30px;"></section>
  </section>
</section>
"""


def build_intro_section(intro: str) -> str:
    if not intro:
        return ""
    paragraph_style = (
        "margin:0 0 14px 0;color:#566975;letter-spacing:1px;line-height:1.9;font-size:15px;"
        "text-align:left;word-break:break-word;"
    )
    content_html = render_paragraphs(intro, paragraph_style)
    return f"""
<section style="width:88%;margin:34px auto 0 auto;">
  <section style="display:inline-block;background:rgba(178,187,193,0.5);color:#3d637e;font-weight:400;padding:8px 14px;font-size:15px;">开篇</section>
  <section style="border-top:1px solid #3d637e;margin-top:8px;padding-top:16px;">
    {content_html}
  </section>
</section>
"""


def build_part_section(index: int, image_src: str, caption: str, part_title: str) -> str:
    paragraph_style = (
        "margin:0;color:#1e2234;line-height:1.9;font-size:15px;letter-spacing:1px;"
        "word-break:break-word;text-align:left;"
    )
    caption_html = render_paragraphs(caption, paragraph_style)
    return f"""
<section style="width:88%;margin:42px auto 0 auto;">
  <section style="display:inline-block;background:#ffffff;border-radius:10px;box-shadow:-3px 1px 16px rgba(0,0,0,0.12);padding:10px 16px;">
    <span style="color:#fbd646;font-weight:700;font-style:italic;font-size:14px;">Part.{index:02d}</span>
    <span style="color:#3d637e;font-weight:700;font-size:15px;padding-left:8px;">{escape(part_title)}</span>
  </section>
  <section style="text-align:right;font-size:0;line-height:0;height:0;">
    <section style="display:inline-block;background:#fbd84f;width:44px;height:34px;position:relative;top:18px;right:10px;"></section>
  </section>
  <section style="background:#ffffff;box-shadow:-3px 1px 16px rgba(0,0,0,0.12);border-radius:12px;padding:20px 18px 28px 18px;position:relative;z-index:1;">
    <img src="{escape(image_src)}" alt="{escape(caption or part_title)}" style="width:100%;border-radius:10px;margin:0 auto 18px auto;display:block;"/>
    <section style="width:92%;margin:0 auto;">
      {caption_html}
    </section>
  </section>
  <section style="background:#3d637e;width:56px;height:74px;margin-top:-36px;margin-left:12px;position:relative;z-index:0;"></section>
</section>
"""


def build_ending_section(ending: str) -> str:
    if not ending:
        return ""
    paragraph_style = (
        "margin:0;color:#09385e;line-height:1.95;font-size:15px;font-weight:700;"
        "letter-spacing:1px;text-align:center;word-break:break-word;"
    )
    return f"""
<section style="width:88%;margin:42px auto 0 auto;">
  <section style="background:rgba(251,218,79,0.15);padding:18px;border-radius:10px;">
    {render_paragraphs(ending, paragraph_style)}
  </section>
  <section style="text-align:center;color:#566975;line-height:1.8;font-size:18px;margin-top:18px;">【完】</section>
</section>
"""


def build_footer_section(topic: str, publisher_name: str, publisher_tagline: str) -> str:
    tag = topic or "公众号文章"
    return f"""
<section style="padding:22px 16px 24px 16px;background:#d8dcdf;margin-top:46px;text-align:center;">
  <section style="display:inline-block;background:#214c6e;color:#e0e4e7;font-weight:700;font-size:20px;padding:8px 22px;margin-top:-38px;">{escape(publisher_name)}</section>
  <section style="color:#628298;font-size:13px;line-height:1.8;letter-spacing:1px;margin-top:16px;">{escape(publisher_tagline)}</section>
  <section style="display:inline-block;background:#fbd84f;color:#214c6e;font-weight:700;font-size:16px;padding:6px 16px;margin-top:14px;">· {escape(tag)} ·</section>
  <section style="color:#5e707d;font-size:12px;line-height:1.8;letter-spacing:1px;margin-top:14px;">建议在浏览器中打开本 HTML 后全选复制，再粘贴到公众号编辑器。</section>
</section>
"""


def build_html_document(title: str, article_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{escape(title)}</title>
  </head>
  <body style="margin:0;padding:24px 0;background:#efefef;">
    <section id="article-root">
      <section style="background:#f7f7f7;width:600px;margin:0 auto;">
        {article_html}
      </section>
    </section>
  </body>
</html>
"""


def format_article(
    markdown_path: str | Path,
    assets_path: str | Path,
    output_dir: str | Path,
    *,
    upload_to_wechat: bool = True,
) -> dict[str, Any]:
    output_dir = ensure_directory(output_dir)
    logger = setup_logger("wechat_comic_factory", output_dir)
    markdown_text = read_text_file(markdown_path)
    assets_payload = read_json_file(assets_path)
    article_payload = prepare_article_payload(markdown_text, assets_payload)
    config = load_config()
    branding = resolve_branding(config)

    title = article_payload["title"]
    if not title:
        raise SkillError("format_article", "publish_assets.json 与 article.md 都缺少可用标题")
    if not article_payload["images"]:
        raise SkillError("format_article", "publish_assets.json 缺少正文图片，无法生成公众号 HTML")

    subtitle_parts = [item for item in [branding["publisher_name"], article_payload["topic"]] if item]
    subtitle = " · ".join(subtitle_parts)

    uploaded_mapping = build_uploaded_mapping(assets_payload)
    upload_results: list[dict[str, Any]] = []
    access_token: str | None = None
    if upload_to_wechat:
        publish_config = load_config(required_paths=["wechat.appid", "wechat.appsecret"])
        access_token = get_wechat_access_token(publish_config, logger)

    part_sections: list[str] = []
    for item in article_payload["images"]:
        source_path = item["source_path"]
        publish_path = item["wechat_path"] or source_path
        best_relative_path = publish_path or source_path
        if not best_relative_path:
            raise SkillError("format_article", "正文图片缺少可用路径", details=item)
        local_path = Path(output_dir) / best_relative_path
        if not local_path.exists():
            raise SkillError(
                "format_article",
                f"文章图片不存在: {local_path}",
                details={"source_path": source_path, "publish_path": publish_path},
            )

        if upload_to_wechat and access_token:
            remote_url = upload_article_image(access_token, local_path, logger)
            image_src = remote_url
            upload_results.append(
                {
                    "source_path": source_path,
                    "local_path": best_relative_path,
                    "remote_url": remote_url,
                }
            )
        else:
            image_src = (
                uploaded_mapping.get(best_relative_path)
                or uploaded_mapping.get(source_path)
                or best_relative_path.replace("\\", "/")
            )

        part_sections.append(
            build_part_section(
                index=item["index"],
                image_src=image_src,
                caption=item["caption"],
                part_title="漫画分镜",
            )
        )

    article_image_uploads = upload_results or assets_payload.get("article_image_uploads", [])
    article_images_uploaded = all(
        isinstance(item, dict) and str(item.get("remote_url", "")).startswith("http")
        for item in article_image_uploads
    )

    article_html = "".join(
        [
            build_banner_section(title, subtitle),
            build_intro_section(article_payload["intro"]),
            "".join(part_sections),
            build_ending_section(article_payload["ending"]),
            build_footer_section(
                article_payload["topic"],
                branding["publisher_name"],
                branding["publisher_tagline"],
            ),
        ]
    )
    final_html = build_html_document(title, article_html)
    final_html_path = Path(output_dir) / "final.html"
    final_html_path.write_text(final_html, encoding="utf-8")

    updated_assets = {
        "final_html_path": str(final_html_path),
        "article_image_uploads": article_image_uploads,
        "article_images_uploaded": article_images_uploaded,
    }
    update_json_file(assets_path, updated_assets)
    logger.info("文章 HTML 已生成，final_html_path=%s", final_html_path)
    return {
        "success": True,
        "stage": "format_article",
        "title": title,
        "html_path": str(final_html_path),
        "output_dir": str(output_dir),
        "article_images_uploaded": article_images_uploaded,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将 Markdown 转为微信公众号兼容 HTML")
    parser.add_argument("--markdown_path", required=True, help="article.md 路径")
    parser.add_argument("--assets_path", required=True, help="publish_assets.json 路径")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    parser.add_argument("--skip_upload", action="store_true", help="调试时跳过正文图片上传")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = format_article(
            args.markdown_path,
            args.assets_path,
            args.output_dir,
            upload_to_wechat=not args.skip_upload,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
