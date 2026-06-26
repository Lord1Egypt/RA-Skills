"""报告生产模块 — HTML 提取、Lint 修复、图片同步、页面生成、写入 dist

职责边界：
- 接收原始 HTML 文件，提取 body + style
- 调用 html_lint 管线做检查+自动修复（div 平衡、路径修正、chrome 移除等）
- 同步图片资源到 dist/images/，修正路径为绝对路径
- 用 page.py 模板生成完整页面 HTML
- 再次调用 html_lint 管线检查页面结构
- 写入 dist/category/ 目录并更新 index.json

不做的事：
- 不部署到 CF（交给 site 模块）
- 不验证线上结果（交给 verify 模块）
- 不定义 lint 规则（交给 html_lint 模块）
"""

import re, sys, json
from pathlib import Path
from datetime import date

from lib.config import (
    DIST_DIR, SITE_URL, SITE_NAME,
    load_index, save_index, strip_emoji, add_ids, check_config,
    CATEGORIES
)
from lib.page import generate_page_html


# ── 分类常量（统一在 config.py 管理） ──


def extract_body(html):
    """从原始 HTML 中提取纯净的 body 内容和 page style。

    处理步骤：
    1. 提取 <body> 或全文作为内容
    2. 剔除 emoji
    3. 提取 <style> 标签内容（page_style）
    4. 从 body 中移除已提取的 style 标签
    5. 清理框架嵌套（header/footer/h1/scroll-progress/toc 等）
    6. 解包多余的 wrapper div

    Returns:
        (body, page_style) — 纯净内容 HTML + 页面专属 CSS
    """
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL)
    if body_match:
        body = body_match.group(1).strip()
    else:
        body = html
    body = strip_emoji(body)

    # Extract style (handles <style>, <style type="text/css">, etc.)
    # Extract all style tags and concatenate their contents
    style_matches = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
    page_style = "\n".join(s.strip() for s in style_matches if s.strip()) if style_matches else ""

    # Remove extracted style from body (also matches <style type=...>)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL).strip()

    # Clean framework nesting
    body = re.sub(r'<header[^>]*>.*?</header>', '', body, flags=re.DOTALL)
    body = re.sub(r'<footer[^>]*>.*?</footer>', '', body, flags=re.DOTALL)
    body = re.sub(r'<h1[^>]*>.*?</h1>', '', body, flags=re.DOTALL)
    body = re.sub(r'<button[^>]*back-to-top[^>]*>.*?</button>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div[^>]*class="scroll-progress"[^>]*></div>', '', body)
    body = re.sub(r'<aside[^>]*class="toc-sidebar"[^>]*>.*?</aside>', '', body, flags=re.DOTALL)
    body = re.sub(r'<button[^>]*class="toc-toggle"[^>]*>.*?</button>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*main\.js[^>]*></script>', '', body)
    # Remove echarts/mermaid/chart.js init scripts (inline <script> blocks)
    body = re.sub(r'<script[^>]*src="[^"]*echarts[^"]*"[^>]*></script>', '', body)
    body = re.sub(r'<script[^>]*src="[^"]*mermaid[^"]*"[^>]*></script>', '', body)
    body = re.sub(r'<script[^>]*src="[^"]*chart\.js[^"]*"[^>]*></script>', '', body)
    # Remove inline echarts init script blocks (contain new ECharts or echarts.init)
    body = re.sub(r'<script>\s*(?:new\s+ECharts|var\s+chart\s*=|echarts\.init|\/\/\s*echarts).*?</script>', '', body, flags=re.DOTALL)
    # Remove inline mermaid init script blocks  
    body = re.sub(r'<script>\s*mermaid\.initialize.*?</script>', '', body, flags=re.DOTALL)

    # Unwrap redundant wrapper divs (report-wrap, page-body, wrap)
    # These are chrome from previous template generations.
    # Strategy: strip the opening and closing tags of these wrappers.
    # We do this iteratively since wrappers may be nested.
    changed = True
    while changed:
        changed = False
        for cls in ['report-wrap', 'page-body', 'wrap']:
            # Remove empty wrapper divs
            new_body = re.sub(rf'<div class="{cls}"[^>]*>\s*</div>', '', body)
            if new_body != body:
                body = new_body
                changed = True
                continue
            # Unwrap: strip opening <div class="cls"...> and its matching </div>
            # Use a simple balanced approach: find opening tag, then find matching close
            open_m = re.search(rf'<div class="{cls}"[^>]*>', body)
            if open_m:
                # Find the matching </div> by tracking nesting depth
                pos = open_m.end()
                depth = 1
                while pos < len(body) and depth > 0:
                    next_open = re.search(r'<div[\s>]', body[pos:])
                    next_close = re.search(r'</div>', body[pos:])
                    if not next_close:
                        break
                    if next_open and next_open.start() < next_close.start():
                        depth += 1
                        pos += next_open.end()
                    else:
                        depth -= 1
                        if depth == 0:
                            close_start = pos + next_close.start()
                            close_end = pos + next_close.end()
                            body = body[:open_m.start()] + body[open_m.end():close_start] + body[close_end:]
                            changed = True
                            break
                        pos += next_close.end()

    return body, page_style


def _collect_images(body, src_file, dist_dir):
    """扫描 body 中的 <img> 标签，复制引用的图片到 dist/images/，并将路径改为绝对路径。

    Args:
        body: HTML body 内容
        src_file: 源 HTML 文件路径（用于定位相对路径图片）
        dist_dir: dist 目录路径

    Returns:
        body: 路径修正后的 HTML body
        copied: 复制的图片数量
    """
    src_path = Path(src_file).resolve()
    src_dir = src_path.parent

    # Find all <img> tags and extract src attributes
    img_tags = re.findall(r'<img[^>]*\ssrc="([^"]+)"[^>]*>', body)
    if not img_tags:
        # Also try single-quoted src
        img_tags = re.findall(r'<img[^>]*\ssrc=\'([^\']+)\'[^>]*>', body)

    if not img_tags:
        return body, 0

    images_dir = dist_dir / "images"
    copied = 0

    for img_src in img_tags:
        # Skip absolute URLs (http/https/data:)
        if img_src.startswith(('http://', 'https://', 'data:', '//')):
            continue

        # Absolute path starting with /images/ — look in dist/images/ directly
        if img_src.startswith('/images/'):
            img_name = img_src[len('/images/'):]
            img_file = images_dir / img_name
            if img_file.exists():
                # Already in dist, no need to copy or change path
                continue
            # Not in dist — can't resolve, report warning
            print(f"  ⚠️ 图片不在 dist/images/: {img_src}")
            continue

        # Resolve relative path against source file's directory
        img_file = (src_dir / img_src).resolve()

        if not img_file.exists():
            print(f"  ⚠️ 图片文件不存在: {img_src} → {img_file}")
            continue

        # Check it's a real image file (not HTML trick)
        img_ext = img_file.suffix.lower()
        if img_ext not in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico', '.bmp'):
            print(f"  ⚠️ 跳过非图片文件: {img_file.name}")
            continue

        # Copy to dist/images/ with sanitized filename
        # Use the basename (last part after any ../ or path segments)
        safe_name = img_file.name
        # Replace spaces with underscores for URL safety
        safe_name = safe_name.replace(' ', '_')

        dst_file = images_dir / safe_name
        images_dir.mkdir(parents=True, exist_ok=True)

        if not dst_file.exists() or dst_file.read_bytes() != img_file.read_bytes():
            import shutil
            shutil.copy2(img_file, dst_file)
            copied += 1

        # Replace the src in body: only inside <img> tags
        old_src = img_src
        new_src = f"/images/{safe_name}"
        body = re.sub(rf'<img([^>]*\s)src="{old_src}"', rf'<img\1src="{new_src}"', body)
        body = re.sub(rf'<img([^>]*\s)src=\'{old_src}\'', rf'<img\1src=\'{new_src}\'', body)

    if copied:
        print(f"  📷 复制了 {copied} 张图片到 dist/images/")

    return body, copied


def produce(category, html_file, title=None, desc=None):
    """报告生产的主入口。

    流程：提取 → 校验 → 图片同步 → 生成 → 写入 dist → 更新索引

    Args:
        category: 分类 key（research/analysis/summary 等）
        html_file: 源 HTML 文件路径
        title: 报告标题（不填则从 <title> 提取）
        desc: 报告描述

    Returns:
        (filename, category) — 生成文件的文件名和分类
    """
    if category not in CATEGORIES:
        raise ValueError(f"未知分类: {category}（可选: {', '.join(CATEGORIES.keys())}）")

    # Validate category is a safe path component (no path traversal)
    if '/' in category or '\\' in category or category.startswith('.'):
        raise ValueError(f"分类名称不合法: {category}")

    src = Path(html_file).resolve()
    if not src.exists():
        raise FileNotFoundError(f"文件不存在: {html_file}")

    # Validate the source file is a regular file (not a symlink to sensitive paths)
    if not src.is_file():
        raise ValueError(f"不是普通文件: {html_file}")

    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    # ── 1. 提取 ──
    body, page_style = extract_body(html)

    # ── 2. Body lint + fix ──
    from lib.html_lint import lint_body
    body, body_failed = lint_body(body, label=src.stem, dist_dir=DIST_DIR)
    for r in body_failed:
        if r.rule.severity == "error":
            raise ValueError(f"Lint 检查未通过: {r.details}")

    # ── 3. 图片资源同步 ──
    body, img_copied = _collect_images(body, src, DIST_DIR)

    # ── 4. 生成 ──
    if not title:
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1) if title_match else src.stem

    today = date.today().isoformat()
    # Generate filename: use source file stem, not title (URL-safe filenames)
    stem = src.stem
    # Avoid double date prefix: if stem already starts with YYYY-MM-DD-, strip it
    if re.match(r'\d{4}-\d{2}-\d{2}-', stem):
        stem = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
    # Strip _adapted_ prefix from adapter temp files
    stem = re.sub(r'^_adapted_', '', stem)
    # Sanitize for URL: replace spaces and non-ASCII with safe chars
    stem = stem.replace(' ', '_')
    # Remove CJK characters from filename (they cause URL encoding issues)
    stem = re.sub(r'[^\w.-]', '', stem)
    if not stem:
        stem = 'report'
    filename = f"{today}-{stem}.html"

    page_info = {
        "title": title,
        "desc": desc or "",
        "date": today,
        "category": category,
        "body": body,
        "style": page_style,
    }
    page_html = generate_page_html(page_info, SITE_URL)

    # ── Page lint + fix ──
    from lib.html_lint import lint_page
    page_html, page_failed = lint_page(page_html, label=src.stem, dist_dir=DIST_DIR)
    for r in page_failed:
        if r.rule.severity == "error":
            raise ValueError(f"Page lint 检查未通过: {r.details}")

    # ── 4. 写入 dist ──
    cat_dir = DIST_DIR / category
    cat_dir.mkdir(parents=True, exist_ok=True)
    with open(cat_dir / filename, "w", encoding="utf-8") as f:
        f.write(page_html)

    # ── 5. 更新索引（同标题覆盖） ──
    data = load_index()
    page_url = f"/{category}/{filename}"
    new_entry = {
        "filename": filename,
        "title": title,
        "desc": desc or "",
        "date": today,
        "category": category,
        "url": page_url,
    }
    replaced = False
    for i, p in enumerate(data["pages"]):
        if p.get("title") == title:
            # Preserve external flag if it existed
            if p.get("external"):
                new_entry["external"] = p["external"]
            data["pages"][i] = new_entry
            replaced = True
            break
    if not replaced:
        data["pages"].append(new_entry)
    save_index(data)

    # ── 6. 备份索引 ──
    from lib.site import _backup_index
    _backup_index(data)

    print(f"✅ 报告生成成功")
    print(f"   分类: {CATEGORIES.get(category, category)} ({category})")
    print(f"   标题: {title}")
    print(f"   文件: dist/{category}/{filename}")

    return filename, category