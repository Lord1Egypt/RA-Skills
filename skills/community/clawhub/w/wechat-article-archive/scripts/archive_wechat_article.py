#!/usr/bin/env python3
import argparse
import hashlib
import json
import mimetypes
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
EXTRACTOR = SCRIPT_DIR / "extract.js"


def fail(message, code=1):
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    raise SystemExit(code)


def run_extract(url: str, html_file=None):
    node = os.environ.get("NODE") or "node"
    js = f"""
const fs = require('fs');
const {{ extract }} = require({json.dumps(str(EXTRACTOR))});
(async () => {{
  const input = process.env.WECHAT_HTML_FILE
    ? fs.readFileSync(process.env.WECHAT_HTML_FILE, 'utf8')
    : {json.dumps(url)};
  const result = await extract(input, {{
    url: {json.dumps(url)},
    shouldReturnContent: true,
    shouldReturnRawMeta: false,
    shouldFollowTransferLink: true,
    shouldExtractMpLinks: true,
    shouldExtractTags: true,
    shouldExtractRepostMeta: true,
  }});
  process.stdout.write(JSON.stringify(result));
}})().catch(err => {{
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
}});
"""
    env = os.environ.copy()
    if html_file:
        env["WECHAT_HTML_FILE"] = str(html_file)
    res = subprocess.run(
        [node, "-e", js],
        capture_output=True,
        text=True,
        cwd=str(SKILL_DIR),
        env=env,
    )
    if res.returncode != 0:
        fail(res.stderr.strip() or "extract failed", 4)
    try:
        obj = json.loads(res.stdout)
    except Exception as exc:
        fail(f"invalid extractor output: {exc}", 5)
    if not obj.get("done"):
        fail(obj.get("msg") or f"extract failed code={obj.get('code')}", 6)
    return obj["data"]


def normalize_text(text: str):
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def text_of(node):
    return " ".join(node.stripped_strings).strip()


def inline_markdown(node):
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name == "br":
        return "\n"
    if name == "img":
        return ""
    if name == "a":
        href = node.get("href")
        title = normalize_text("".join(inline_markdown(c) for c in node.children))
        if href and title:
            return f"[{title}]({href})"
        return title
    return "".join(inline_markdown(c) for c in node.children)


def extract_code_block(node):
    if not isinstance(node, Tag):
        return ""
    classes = set(node.get("class") or [])
    if "code-snippet__fix" in classes or "code-snippet__js" in classes:
        clone = BeautifulSoup(str(node), "html.parser")
        for bad in clone.select("ul.code-snippet__line-index"):
            bad.decompose()
        inner = clone.find("pre", class_=lambda c: c and "code-snippet__js" in c)
        if inner:
            return inner.get_text("\n", strip=False).strip("\n")
    return node.get_text("\n", strip=False).strip("\n")


def append_code_block(lines, node):
    code = extract_code_block(node)
    if code:
        lines += ["```", code, "```", ""]


def append_table(lines, table):
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        if not cells:
            continue
        rows.append([normalize_text(text_of(cell)).replace("|", "\\|") for cell in cells])
    if not rows:
        txt = normalize_text(text_of(table))
        if txt:
            lines += [txt, ""]
        return
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    lines.append("| " + " | ".join(rows[0]) + " |")
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")


def image_src(node):
    return (
        node.get("data-src")
        or node.get("data-original")
        or node.get("data-croporisrc")
        or node.get("data-backsrc")
        or node.get("data-actualsrc")
        or node.get("data-lazy-src")
        or node.get("data-original-src")
        or node.get("src")
    )


def style_image_src(node):
    style = node.get("style") or ""
    if not style:
        return None
    match = re.search(r"""url\((['"]?)(.*?)\1\)""", style, re.I)
    if not match:
        return None
    return match.group(2)


def background_image_src(node):
    return (
        node.get("data-lazy-bgimg")
        or node.get("data-bgsrc")
        or node.get("data-background")
        or style_image_src(node)
    )


def append_image(lines, src, seen, image_refs):
    if not src:
        return
    src = src.strip().replace("&amp;", "&")
    if not src or src.startswith("data:"):
        return
    if src.startswith("//"):
        src = "https:" + src
    if src in seen:
        return
    seen.add(src)
    image_refs.append({"url": src, "local": None})
    lines += [f"![图片]({src})", ""]


def walk_blocks(node, lines, seen, stats, image_refs, inside_list=False):
    if isinstance(node, NavigableString) or not isinstance(node, Tag):
        return

    name = node.name.lower()
    classes = set(node.get("class") or [])

    if name in {"script", "style"}:
        return
    if name == "img":
        before = len(image_refs)
        append_image(lines, image_src(node), seen, image_refs)
        if len(image_refs) > before:
            stats["body_img_count"] += 1
        return
    bg_src = background_image_src(node)
    if bg_src:
        before = len(image_refs)
        append_image(lines, bg_src, seen, image_refs)
        if len(image_refs) > before:
            stats["body_img_count"] += 1
    if name == "hr":
        lines += ["---", ""]
        return
    if "code-snippet__fix" in classes or "code-snippet__js" in classes:
        append_code_block(lines, node)
        return
    if name == "pre":
        if node.find("section", class_=lambda c: c and "code-snippet__fix" in c):
            for child in node.children:
                walk_blocks(child, lines, seen, stats, image_refs, inside_list)
            return
        append_code_block(lines, node)
        return
    if name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        title = normalize_text(text_of(node))
        if title:
            level = min(max(int(name[1]), 1), 6)
            lines += ["#" * level + " " + title, ""]
        return
    if name in ["ul", "ol"]:
        idx = 1
        for li in node.find_all("li", recursive=False):
            prefix = f"{idx}. " if name == "ol" else "- "
            txt = normalize_text(inline_markdown(li))
            if txt:
                lines.append(prefix + txt)
            for img in li.find_all("img"):
                walk_blocks(img, lines, seen, stats, image_refs, True)
            idx += 1
        if idx > 1:
            lines.append("")
        return
    if name == "table":
        append_table(lines, node)
        return
    if name == "blockquote":
        txt = normalize_text(inline_markdown(node))
        if txt:
            for part in txt.splitlines():
                lines.append("> " + part)
            lines.append("")
        return

    is_container = name in ["section", "div", "article"]
    is_para = name == "p"
    if is_container:
        has_block_children = any(
            isinstance(child, Tag)
            and child.name
            and child.name.lower()
            in {
                "section",
                "div",
                "article",
                "p",
                "pre",
                "ul",
                "ol",
                "table",
                "img",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "blockquote",
                "hr",
            }
            for child in node.children
        )
        if has_block_children:
            for child in node.children:
                walk_blocks(child, lines, seen, stats, image_refs, inside_list)
            return

    if is_para or is_container or name == "li":
        txt = normalize_text(inline_markdown(node))
        if txt:
            lines += [txt, ""]
        for child in node.children:
            if isinstance(child, Tag) and child.name and child.name.lower() == "img":
                walk_blocks(child, lines, seen, stats, image_refs, inside_list)
        return

    for child in node.children:
        walk_blocks(child, lines, seen, stats, image_refs, inside_list)


def safe_filename(name: str, suffix: str = ""):
    raw = (name or "wechat_article").strip()
    raw = re.sub(r'[\\/:*?"<>|\r\n]+', "_", raw)
    raw = re.sub(r"\s+", " ", raw).strip().strip(".")
    if not raw:
        raw = "wechat_article"
    if suffix and not raw.lower().endswith(suffix.lower()):
        raw += suffix
    return raw


def guess_ext(url, content_type):
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"}:
        return ext
    guessed = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
    if guessed == ".jpe":
        return ".jpg"
    return guessed or ".jpg"


def download_image(url, assets_dir, index, timeout=30):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
        "Referer": "https://mp.weixin.qq.com/",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type", "")
    if not data:
        raise RuntimeError("empty image response")
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]
    ext = guess_ext(url, content_type)
    filename = f"image-{index:02d}-{digest}{ext}"
    path = assets_dir / filename
    path.write_bytes(data)
    return path


def build_markdown(data):
    title = data.get("msg_title") or "未命名文章"
    html = data.get("msg_content") or ""
    soup = BeautifulSoup(html, "html.parser")
    lines = [
        f"# {title}",
        "",
        f"> **作者**: {data.get('msg_author') or '未知'}  ",
        f"> **公众号**: {data.get('account_name') or '未知'}  ",
        f"> **发布时间**: {data.get('msg_publish_time_str') or '未知'}  ",
        f"> **原文链接**: {data.get('msg_link') or ''}",
        "",
        "---",
        "",
    ]
    seen = set()
    image_refs = []
    stats = {"body_img_count": 0}
    for node in soup.children:
        walk_blocks(node, lines, seen, stats, image_refs)

    cover_used = False
    cover = data.get("msg_cover")
    if stats["body_img_count"] == 0 and cover:
        cover_used = True
        image_refs.insert(0, {"url": cover, "local": None})
        lines = lines[:9] + [f"![封面]({cover})", ""] + lines[9:]

    cleaned = []
    blank = False
    for line in lines:
        if line == "":
            if not blank:
                cleaned.append(line)
            blank = True
        else:
            cleaned.append(line)
            blank = False
    return "\n".join(cleaned).strip() + "\n", image_refs, stats["body_img_count"], cover_used


def rewrite_image_links(markdown, image_refs, md_dir):
    for ref in image_refs:
        if not ref.get("local"):
            continue
        rel = ref["local"].relative_to(md_dir).as_posix()
        markdown = markdown.replace(f"]({ref['url']})", f"]({rel})")
    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Archive a WeChat Official Account article as Markdown plus local assets."
    )
    parser.add_argument("url", help="mp.weixin.qq.com article URL")
    parser.add_argument("output_dir", help="target directory for article.md and assets/")
    parser.add_argument("--filename", help="optional Markdown filename")
    parser.add_argument("--skip-images", action="store_true", help="do not download images")
    parser.add_argument(
        "--html-file",
        help="optional saved WeChat page source; use it instead of fetching the URL",
    )
    parser.add_argument(
        "--image-timeout",
        type=float,
        default=30,
        help="timeout in seconds for each image download (default: 30)",
    )
    args = parser.parse_args()

    if not EXTRACTOR.exists():
        fail(f"extractor not found: {EXTRACTOR}", 3)

    html_file = Path(args.html_file).expanduser().resolve() if args.html_file else None
    if html_file and not html_file.is_file():
        fail(f"HTML file not found: {html_file}", 2)
    if args.image_timeout <= 0:
        fail("image timeout must be greater than 0", 2)

    output_dir = Path(args.output_dir).expanduser().resolve()
    assets_dir = output_dir / "assets"
    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    data = run_extract(args.url, html_file)
    markdown, image_refs, body_img_count, cover_used = build_markdown(data)

    failures = []
    if not args.skip_images:
        for index, ref in enumerate(image_refs, start=1):
            try:
                ref["local"] = download_image(
                    ref["url"], assets_dir, index, timeout=args.image_timeout
                )
            except Exception as exc:
                failures.append({"url": ref["url"], "error": str(exc)})

    filename = safe_filename(args.filename or data.get("msg_title") or data.get("msg_sn"), ".md")
    md_path = output_dir / filename
    markdown = rewrite_image_links(markdown, image_refs, output_dir)
    md_path.write_text(markdown, encoding="utf-8")
    body_text = normalize_text(
        BeautifulSoup(data.get("msg_content") or "", "html.parser").get_text("\n")
    )

    result = {
        "ok": True,
        "title": data.get("msg_title"),
        "account": data.get("account_name"),
        "author": data.get("msg_author"),
        "publish_time": data.get("msg_publish_time_str"),
        "markdown_path": str(md_path),
        "assets_dir": str(assets_dir),
        "body_img_count": body_img_count,
        "body_text_length": len(body_text),
        "cover_used": cover_used,
        "image_count": len(image_refs),
        "downloaded_image_count": sum(1 for ref in image_refs if ref.get("local")),
        "image_failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
