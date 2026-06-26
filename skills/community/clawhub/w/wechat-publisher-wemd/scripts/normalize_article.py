#!/usr/bin/env python3
"""正文归一化：WeMD 渲染 + 图片上传替换"""
import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from wechat_client import WeChatSkillError, upload_article_image

DEFAULT_THEME = "Default"

_BUILTIN_THEMES: dict[str, str] = {
    "默认": "Default", "学术论文": "Academic-Paper", "极光玻璃": "Aurora-Glass",
    "包豪斯": "Bauhaus", "赛博朋克": "Cyberpunk-Neon", "知识库": "Knowledge-Base",
    "黑金奢华": "Luxury-Gold", "莫兰迪森林": "Morandi-Forest", "新粗野主义": "Neo-Brutalism",
    "购物小票": "Receipt", "落日胶片": "Sunset-Film", "主题模板": "Template",
}

CUSTOM_THEMES_JSON = Path(__file__).resolve().parent.parent / "vendor" / "wemd" / "custom_themes.json"
WEMD_RENDER_JS = Path(__file__).resolve().parent.parent / "vendor" / "wemd" / "render.js"

HTML_IMAGE_RE = re.compile(r'(<img\b[^>]*\bsrc=")([^"]+)(".*?>)', re.IGNORECASE)
REMOTE_SRC_RE = re.compile(r"^(?:https?:)?//|^data:|^mailto:", re.IGNORECASE)


def _load_theme_map() -> dict[str, str]:
    result = dict(_BUILTIN_THEMES)
    if CUSTOM_THEMES_JSON.is_file():
        try:
            result.update(json.loads(CUSTOM_THEMES_JSON.read_text(encoding="utf-8")))
        except Exception:
            pass
    return result


def resolve_theme(name: str | None) -> str:
    if not name:
        return DEFAULT_THEME
    theme_map = _load_theme_map()
    en_to_cn = {v: k for k, v in theme_map.items()}
    if name in en_to_cn:
        return name
    if name in theme_map:
        return theme_map[name]
    raise WeChatSkillError(
        f"未知主题「{name}」。可用主题：\n"
        + "\n".join(f"  {cn}（{en}）" for cn, en in theme_map.items())
    )


def wemd_convert(markdown_text: str, theme: str) -> str:
    if not WEMD_RENDER_JS.is_file():
        raise WeChatSkillError("WeMD renderer not found")
    from setup import ensure_installed
    ensure_installed()
    payload_str = json.dumps({"markdown": markdown_text, "theme": theme}, ensure_ascii=False)
    r = subprocess.run(
        ["node", str(WEMD_RENDER_JS), "--json"],
        input=payload_str, capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        raise WeChatSkillError(f"WeMD render failed: {(r.stderr or r.stdout).strip()[:300]}")
    stdout = r.stdout
    idx = stdout.find("{")
    if idx > 0:
        stdout = stdout[idx:]
    result = json.loads(stdout)
    if not result.get("ok"):
        raise WeChatSkillError(f"WeMD render error: {result.get('error', 'unknown')}")
    return result["html"]


def _resolve_base_dir(payload: dict) -> Path:
    if payload.get("content_base_dir"):
        return Path(payload["content_base_dir"]).expanduser().resolve()
    if payload.get("content_markdown_path"):
        return Path(payload["content_markdown_path"]).expanduser().resolve().parent
    return Path.cwd()


def replace_inline_images(html_content: str, payload: dict) -> tuple[str, dict]:
    base_dir = _resolve_base_dir(payload)
    uploaded: list[dict] = []

    def repl(m: re.Match) -> str:
        prefix, src, suffix = m.groups()
        if REMOTE_SRC_RE.match(src):
            return m.group(0)
        candidate = Path(src).expanduser()
        if not candidate.is_absolute():
            candidate = base_dir / candidate
        candidate = candidate.resolve()
        if not candidate.is_file():
            raise WeChatSkillError(f"Inline image not found: {src}")
        result = upload_article_image(str(candidate))
        url = result.get("url")
        if not url:
            raise WeChatSkillError(f"Image upload got no url: {src}")
        uploaded.append({"source": src, "resolved_path": str(candidate), "url": url})
        return f'{prefix}{html.escape(url, quote=True)}{suffix}'

    updated = HTML_IMAGE_RE.sub(repl, html_content)
    return updated, {"inline_image_upload_count": len(uploaded), "inline_images": uploaded}


def _resolve_source(payload: dict) -> tuple[str, str]:
    if payload.get("content_markdown"):
        return payload["content_markdown"], "markdown"
    if payload.get("content_markdown_path"):
        p = Path(payload["content_markdown_path"]).expanduser().resolve()
        if not p.is_file():
            raise WeChatSkillError(f"Markdown file not found: {payload['content_markdown_path']}")
        return p.read_text(encoding="utf-8"), "markdown"
    if payload.get("content_text"):
        return payload["content_text"], "text"
    if payload.get("content"):
        return payload["content"], str(payload.get("content_format", "html")).lower()
    raise WeChatSkillError("Missing article body")


def normalize_article_payload(payload: dict) -> tuple[dict, dict]:
    normalized = dict(payload)
    source_content, source_format = _resolve_source(payload)
    theme = resolve_theme(payload.get("theme"))

    if source_format in ("markdown", "text"):
        normalized["content"] = wemd_convert(source_content, theme)
    elif source_format == "html":
        normalized["content"] = source_content
    else:
        raise WeChatSkillError(f"Unsupported format: {source_format}")

    normalized["content"], inline_meta = replace_inline_images(normalized["content"], payload)
    normalized["content_format"] = "html"
    return normalized, {"source_format": source_format, "engine": "wemd", "theme": theme, "normalized": source_format != "html", **inline_meta}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--theme", default=None)
    parser.add_argument("--list-themes", action="store_true")
    args = parser.parse_args()

    if args.list_themes:
        theme_map = _load_theme_map()
        custom = {}
        if CUSTOM_THEMES_JSON.is_file():
            try:
                custom = json.loads(CUSTOM_THEMES_JSON.read_text(encoding="utf-8"))
            except Exception:
                pass
        print(json.dumps({
            "default": DEFAULT_THEME,
            "themes": [{"cn": cn, "en": en, "custom": cn in custom} for cn, en in theme_map.items()],
        }, ensure_ascii=False, indent=2))
        return 0

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)
        if args.theme:
            payload["theme"] = args.theme
        normalized, metadata = normalize_article_payload(payload)
        json.dump({"ok": True, "step": "normalize_article", "metadata": metadata, "payload": normalized}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    except Exception as e:
        json.dump({"ok": False, "step": "normalize_article", "message": str(e)}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
