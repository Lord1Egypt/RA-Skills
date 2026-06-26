#!/usr/bin/env python3
from __future__ import annotations

import argparse
from io import BytesIO
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from PIL import Image, ImageSequence

from common import DEFAULT_CONFIG_PATH, expand_path, load_config, load_yaml, now_iso, read_json, sanitize_filename, write_json


UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def text_from_html(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value or "", flags=re.I)
    value = re.sub(r"</p\s*>", "\n\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def unique(values: list[str]) -> list[str]:
    seen = set()
    out = []
    for value in values:
        value = html.unescape(str(value or "")).strip()
        if not value or value.startswith("data:") or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def load_rules(config: dict[str, Any]) -> list[dict[str, Any]]:
    path = expand_path(config["classification"]["rules_file"])
    data = load_yaml(path)
    return data.get("rules", []) if isinstance(data.get("rules"), list) else []


def haystack(item: dict[str, Any]) -> str:
    parts = [
        item.get("title"),
        item.get("desc"),
        item.get("plain"),
        item.get("excerpt"),
        item.get("html"),
    ]
    raw = item.get("raw")
    if isinstance(raw, dict):
        parts.extend([raw.get("desc"), raw.get("title")])
    card = item.get("list_card") or item.get("list_item")
    if isinstance(card, dict):
        parts.extend([card.get("title"), card.get("excerpt"), card.get("author")])
    return " ".join(str(p or "") for p in parts).lower()


def classify(config: dict[str, Any], item: dict[str, Any]) -> tuple[str, str]:
    h = haystack(item)
    for rule in load_rules(config):
        keywords = rule.get("keywords") or []
        if any(str(k).lower() in h for k in keywords):
            return str(rule.get("level1") or "其他"), str(rule.get("level2") or "待整理")
    c = config["classification"]
    return str(c.get("default_level1", "其他")), str(c.get("default_level2", "待整理"))


def item_id(platform: str, item: dict[str, Any], path: Path) -> str:
    if platform == "xhs":
        return str(item.get("note_id") or item.get("id") or path.stem)
    return str(item.get("id") or path.stem)


def item_title(item: dict[str, Any], fallback: str) -> str:
    raw = item.get("raw") if isinstance(item.get("raw"), dict) else {}
    card = item.get("list_card") or item.get("list_item") or {}
    for key in ("title", "displayTitle", "name"):
        for obj in (item, raw, card):
            if isinstance(obj, dict) and obj.get(key):
                return str(obj[key]).strip()
    return fallback


def item_url(platform: str, item: dict[str, Any], ident: str) -> str:
    if item.get("url"):
        return str(item["url"])
    if platform == "xhs":
        return f"https://www.xiaohongshu.com/explore/{ident}"
    if item.get("type") == "article":
        return f"https://zhuanlan.zhihu.com/p/{ident}"
    return str((item.get("list_item") or {}).get("url") or "")


def body(platform: str, item: dict[str, Any]) -> str:
    if platform == "xhs":
        raw = item.get("raw") if isinstance(item.get("raw"), dict) else {}
        return str(item.get("desc") or raw.get("desc") or "").strip()
    plain = str(item.get("plain") or "").strip()
    if plain:
        return plain
    return text_from_html(str(item.get("html") or ""))


def xhs_image_urls(item: dict[str, Any]) -> list[str]:
    urls = []
    raw = item.get("raw") if isinstance(item.get("raw"), dict) else {}
    for image in raw.get("imageList") or []:
        if not isinstance(image, dict):
            continue
        urls.append(str(image.get("urlDefault") or image.get("urlPre") or image.get("url") or ""))
        for info in image.get("infoList") or []:
            if isinstance(info, dict) and info.get("imageScene") == "WB_DFT":
                urls.append(str(info.get("url") or ""))
    card = item.get("list_card") if isinstance(item.get("list_card"), dict) else {}
    urls.append(str(card.get("cover") or ""))
    return unique(urls)


def zhihu_image_urls(item: dict[str, Any]) -> list[str]:
    html_text = str(item.get("html") or "")
    urls = []
    for tag in re.findall(r"<img\b[^>]*>", html_text, flags=re.I):
        for attr in ("data-original", "data-actualsrc", "src"):
            match = re.search(rf'{attr}\s*=\s*["\']([^"\']+)["\']', tag, flags=re.I)
            if match:
                urls.append(match.group(1))
    return unique(urls)


def image_urls(platform: str, item: dict[str, Any]) -> list[str]:
    if platform == "xhs":
        return xhs_image_urls(item)
    return zhihu_image_urls(item)


def extension_from_url(url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower().lstrip(".")
    return suffix if suffix in {"jpg", "jpeg", "png", "webp"} else "img"


def download_image(session: requests.Session, url: str, referer: str) -> bytes:
    headers = {"User-Agent": UA}
    if referer:
        headers["Referer"] = referer
    response = session.get(url, headers=headers, timeout=45)
    response.raise_for_status()
    return response.content


def save_webp(data: bytes, target: Path) -> None:
    with Image.open(BytesIO(data)) as image:
        frame = next(ImageSequence.Iterator(image))
        if frame.mode not in ("RGB", "L"):
            background = Image.new("RGB", frame.size, (255, 255, 255))
            if frame.mode in ("RGBA", "LA"):
                background.paste(frame, mask=frame.getchannel("A"))
                frame = background
            else:
                frame = frame.convert("RGB")
        elif frame.mode != "RGB":
            frame = frame.convert("RGB")
        target.parent.mkdir(parents=True, exist_ok=True)
        frame.save(target, "WEBP", quality=70, method=6)


def download_assets(
    platform: str,
    config: dict[str, Any],
    item: dict[str, Any],
    ident: str,
    source_url: str,
) -> tuple[list[str], list[dict[str, str]]]:
    vault = expand_path(config["obsidian"]["vault"])
    asset_dirname = str(config["obsidian"].get("asset_dirname") or "_assets").strip() or "_assets"
    platform_dir = "xhs" if platform == "xhs" else "zhihu"
    asset_dir = vault / asset_dirname / platform_dir / sanitize_filename(ident, ident)
    refs = []
    errors = []
    session = requests.Session()
    session.trust_env = False

    for index, url in enumerate(image_urls(platform, item), start=1):
        filename = f"{index:03d}-{extension_from_url(url)}.webp"
        target = asset_dir / filename
        wiki_path = f"{asset_dirname}/{platform_dir}/{sanitize_filename(ident, ident)}/{filename}"
        try:
            if not target.exists():
                save_webp(download_image(session, url, source_url), target)
            refs.append(f"![[{wiki_path}]]")
        except Exception as exc:
            errors.append({"url": url, "error": str(exc)[:500]})
    return refs, errors


def render(platform: str, config: dict[str, Any], item: dict[str, Any], src: Path) -> tuple[str, Path, list[dict[str, str]]]:
    ident = item_id(platform, item, src)
    title = item_title(item, ident)
    lv1, lv2 = classify(config, item)
    platform_name = "小红书" if platform == "xhs" else "知乎"
    filename = sanitize_filename(f"{title}-{ident}", ident) + ".md"
    target = expand_path(config["obsidian"]["vault"]) / config["obsidian"]["base_dir"] / platform_name / lv1 / lv2 / filename
    url = item_url(platform, item, ident)
    author = item.get("author") or ((item.get("raw") or {}).get("user") or {}).get("nickname") if isinstance(item.get("raw"), dict) else ""
    content = body(platform, item)
    image_refs, image_errors = download_assets(platform, config, item, ident, url)
    front = [
        "---",
        f'title: "{title.replace(chr(34), chr(92)+chr(34))}"',
        f'source: "{platform_name}"',
        f'source_id: "{ident}"',
        f'source_url: "{url}"',
        f'category_level1: "{lv1}"',
        f'category_level2: "{lv2}"',
        f'author: "{str(author or "").replace(chr(34), chr(92)+chr(34))}"',
        f'generated_at: "{now_iso()}"',
        "tags:",
        f'  - "{platform_name}"',
        f'  - "{platform_name}/{lv1}"',
        f'  - "{platform_name}/{lv1}/{lv2}"',
        "---",
        "",
        f"# {title}",
        "",
    ]
    if content:
        front.extend([content, ""])
    if image_refs:
        front.extend(["## 图片", "", *image_refs, ""])
    if url:
        front.extend(["---", f"[原文链接]({url})", ""])
    return "\n".join(front), target, image_errors


def export_platform(platform: str, config: dict[str, Any], incremental: bool) -> dict[str, int]:
    root = expand_path(config["data_dir"]) / platform
    raw = root / "raw"
    state_path = root / "export_state.json"
    state = read_json(state_path, {"exported": {}})
    exported = skipped = failed = images = image_failed = 0
    for src in sorted(raw.glob("*.json")):
        if incremental and src.name in state.get("exported", {}):
            skipped += 1
            continue
        try:
            item = read_json(src, {})
            text, target, image_errors = render(platform, config, item, src)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            image_count = text.count("![[")
            images += image_count
            image_failed += len(image_errors)
            state.setdefault("exported", {})[src.name] = {
                "at": now_iso(),
                "path": str(target),
                "images": image_count,
                "image_errors": image_errors,
            }
            exported += 1
        except Exception as exc:
            state.setdefault("failed", {})[src.name] = {"at": now_iso(), "error": str(exc)[:500]}
            failed += 1
    state["last_export"] = now_iso()
    write_json(state_path, state)
    return {"exported": exported, "skipped": skipped, "failed": failed, "images": images, "image_failed": image_failed}


def maybe_ob_sync(config: dict[str, Any]) -> None:
    if not config["obsidian"].get("run_ob_sync"):
        return
    vault = expand_path(config["obsidian"]["vault"])
    if not vault.exists():
        print(f"[skip] obsidian vault missing: {vault}")
        return
    ob = shutil.which("ob.cmd") or shutil.which("ob.exe") or shutil.which("ob") if sys.platform.startswith("win") else shutil.which("ob")
    if not ob:
        print("[skip] ob command not found")
        return
    try:
        subprocess.run([ob, "sync"], cwd=str(vault), check=False)
    except FileNotFoundError:
        print("[skip] ob command not found")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export synced raw favorites to categorized Obsidian Markdown")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--platform", choices=["xhs", "zhihu", "all"], default="all")
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--no-ob-sync", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    results = {}
    for platform in ("xhs", "zhihu"):
        if args.platform in (platform, "all"):
            results[platform] = export_platform(platform, config, args.incremental)
    if args.no_ob_sync:
        config["obsidian"]["run_ob_sync"] = False
    maybe_ob_sync(config)
    for platform, result in results.items():
        print(f"{platform}: " + ", ".join(f"{k}={v}" for k, v in result.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
