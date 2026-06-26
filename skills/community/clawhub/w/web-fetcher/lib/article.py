"""Article fetching with three-tier strategy and image localization."""
import os
import re
import subprocess
import tempfile
import urllib.request
from urllib.parse import urlparse, urljoin

from lib.router import check_dependency
from lib.utils import slugify, extract_title


def fetch_article(url, output_dir, route_config, no_images=False):
    """Fetch article, convert to markdown, download images. Returns output path."""
    os.makedirs(output_dir, exist_ok=True)
    method = route_config.get("method", "scrapling")
    selector = route_config.get("selector")
    post_hook = route_config.get("post", "default_images")

    result = None

    # Tier 1: scrapling GET (pure HTTP)
    if method in ("scrapling",):
        result = _fetch_with_scrapling_get(url, selector)

    # Tier 2: scrapling fetch (headless browser)
    if result is None and method in ("scrapling",):
        print("[*] Tier 1 failed, trying headless browser...")
        result = _fetch_with_scrapling_fetch(url, selector)

    # Tier 3: camoufox (anti-detection)
    if result is None:
        print("[*] Trying camoufox (anti-detection browser)...")
        result = _fetch_with_camoufox(url, selector)

    if result is None:
        print("[!] All fetch methods failed.")
        return None

    md_text, html_text = result

    # Extract title from first heading or first line
    title = extract_title(md_text)
    slug = slugify(title) if title else "article"

    # Save markdown
    md_path = os.path.join(output_dir, f"{slug}.md")
    img_dir = os.path.join(output_dir, "images", slug)

    # Download images
    if not no_images and html_text:
        if post_hook == "wx_images":
            md_text = _wx_image_hook(md_text, html_text, img_dir)
        elif post_hook == "toutiao_images":
            md_text = _toutiao_image_hook(md_text, html_text, img_dir)
        else:
            md_text = _default_image_hook(md_text, html_text, img_dir)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    print(f"[+] Saved: {md_path}")
    return md_path


def _fetch_with_scrapling_get(url, selector):
    """Tier 1: Pure HTTP via scrapling CLI. Returns (md_text, html_text) or None."""
    if not check_dependency("scrapling"):
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = os.path.join(tmpdir, "out.md")
        html_file = os.path.join(tmpdir, "out.html")

        cmd_md = ["scrapling", "extract", "get", url, md_file]
        cmd_html = ["scrapling", "extract", "get", url, html_file]
        if selector:
            cmd_md += ["-s", selector]
            cmd_html += ["-s", selector]

        print(f"[*] Scrapling GET: {url}")
        r1 = subprocess.run(cmd_md, capture_output=True, text=True, timeout=60)
        r2 = subprocess.run(cmd_html, capture_output=True, text=True, timeout=60)

        md_text = _read_if_exists(md_file)
        html_text = _read_if_exists(html_file)

        if md_text and len(md_text.strip()) > 100:
            return md_text, html_text or ""
        return None


def _fetch_with_scrapling_fetch(url, selector):
    """Tier 2: Headless browser via scrapling fetch. Returns (md_text, html_text) or None."""
    if not check_dependency("scrapling"):
        return None

    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = os.path.join(tmpdir, "out.md")
        html_file = os.path.join(tmpdir, "out.html")

        cmd_md = ["scrapling", "extract", "fetch", url, md_file, "--network-idle"]
        cmd_html = ["scrapling", "extract", "fetch", url, html_file, "--network-idle"]
        if selector:
            cmd_md += ["-s", selector]
            cmd_html += ["-s", selector]

        print(f"[*] Scrapling fetch (browser): {url}")
        r1 = subprocess.run(cmd_md, capture_output=True, text=True, timeout=120)
        r2 = subprocess.run(cmd_html, capture_output=True, text=True, timeout=120)

        md_text = _read_if_exists(md_file)
        html_text = _read_if_exists(html_file)

        if md_text and len(md_text.strip()) > 100:
            return md_text, html_text or ""
        return None


def _fetch_with_camoufox(url, selector):
    """Tier 3: Anti-detection browser via camoufox. Returns (md_text, html_text) or None."""
    if not check_dependency("camoufox"):
        return None
    if not check_dependency("html2text"):
        return None

    try:
        from camoufox.sync_api import Camoufox
        import html2text

        with Camoufox(headless=True) as browser:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)

            if selector:
                elements = page.query_selector_all(selector)
                html_text = "\n".join(el.inner_html() for el in elements) if elements else page.content()
            else:
                html_text = page.content()

            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            md_text = h.handle(html_text)

            # Readability.js fallback: if extracted content is too thin, inject
            # Mozilla Readability to pull the main article content from the page.
            if len(md_text.strip()) < 200:
                readability_result = _readability_extract(page)
                if readability_result:
                    rd_html, rd_title = readability_result
                    rd_md = h.handle(rd_html)
                    if len(rd_md.strip()) > len(md_text.strip()):
                        print("[*] Readability.js extracted better content")
                        html_text = rd_html
                        md_text = rd_md

            return md_text, html_text
    except Exception as e:
        print(f"[!] Camoufox error: {e}")
        return None


def _readability_extract(page):
    """Inject Readability.js into the page and extract article content.

    Returns (html_content, title) or None on failure.
    """
    try:
        js_path = os.path.join(os.path.dirname(__file__), "readability.js")
        with open(js_path, "r", encoding="utf-8") as f:
            readability_js = f.read()

        # Inject Readability constructor, then parse the current document
        result = page.evaluate("""
            (readabilityCode) => {
                eval(readabilityCode);
                try {
                    const cloned = document.cloneNode(true);
                    const article = new Readability(cloned).parse();
                    if (article && article.content) {
                        return {content: article.content, title: article.title || ''};
                    }
                } catch(e) {}
                return null;
            }
        """, readability_js)

        if result and result.get("content"):
            return result["content"], result.get("title", "")
    except Exception as e:
        print(f"[!] Readability.js injection failed: {e}")
    return None


def _wx_image_hook(md_text, html_text, img_dir):
    """WeChat-specific: extract data-src, replace SVG placeholders, download."""
    # Extract real image URLs from data-src
    data_src_urls = re.findall(r'data-src="(https://mmbiz\.qpic\.cn[^"]+)"', html_text)
    if not data_src_urls:
        return _default_image_hook(md_text, html_text, img_dir)

    os.makedirs(img_dir, exist_ok=True)

    for i, img_url in enumerate(data_src_urls):
        ext = _guess_ext(img_url, "jpg")
        local_name = f"img_{i:02d}.{ext}"
        local_path = os.path.join(img_dir, local_name)

        if _download_image(img_url, local_path, referer="https://mp.weixin.qq.com/"):
            # Replace SVG placeholder or original URL in markdown
            md_text = md_text.replace(img_url, os.path.join("images", os.path.basename(img_dir), local_name))

    # Replace remaining data:image/svg+xml placeholders
    md_text = re.sub(r'!\[([^\]]*)\]\(data:image/svg\+xml[^)]*\)', '', md_text)

    return md_text


def _toutiao_image_hook(md_text, html_text, img_dir):
    """Toutiao-specific: extract real URLs from data-src containing toutiaoimg.com."""
    data_src_urls = re.findall(r'data-src="(https?://[^"]*toutiaoimg\.com[^"]+)"', html_text)
    if not data_src_urls:
        # Also try src with toutiaoimg
        data_src_urls = re.findall(r'src="(https?://[^"]*toutiaoimg\.com[^"]+)"', html_text)
    if not data_src_urls:
        return _default_image_hook(md_text, html_text, img_dir)

    os.makedirs(img_dir, exist_ok=True)

    for i, img_url in enumerate(data_src_urls):
        ext = _guess_ext(img_url, "jpg")
        local_name = f"img_{i:02d}.{ext}"
        local_path = os.path.join(img_dir, local_name)

        if _download_image(img_url, local_path, referer="https://www.toutiao.com/"):
            md_text = md_text.replace(img_url, os.path.join("images", os.path.basename(img_dir), local_name))

    # Remove base64 placeholders
    md_text = re.sub(r'!\[([^\]]*)\]\(data:image/[^)]*\)', '', md_text)

    return md_text


def _default_image_hook(md_text, html_text, img_dir):
    """Generic: find all image URLs in markdown, download, replace."""
    img_urls = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', md_text)
    if not img_urls:
        return md_text

    # Filter out data: URLs
    real_images = [(alt, url) for alt, url in img_urls if not url.startswith("data:")]
    if not real_images:
        return md_text

    os.makedirs(img_dir, exist_ok=True)

    for i, (alt, img_url) in enumerate(real_images):
        ext = _guess_ext(img_url, "jpg")
        local_name = f"img_{i:02d}.{ext}"
        local_path = os.path.join(img_dir, local_name)

        if _download_image(img_url, local_path):
            local_ref = os.path.join("images", os.path.basename(img_dir), local_name)
            md_text = md_text.replace(img_url, local_ref)

    return md_text


def _download_image(url, local_path, referer=None):
    """Download image with appropriate headers. Returns True on success."""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        if referer:
            req.add_header("Referer", referer)

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if len(data) < 100:  # Too small, likely an error
                return False
            with open(local_path, "wb") as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"[!] Image download failed: {url} - {e}")
        return False



def _guess_ext(url, default="jpg"):
    """Guess image extension from URL."""
    path = urlparse(url).path.lower()
    for ext in ("png", "jpg", "jpeg", "gif", "webp", "svg", "bmp"):
        if f".{ext}" in path:
            return ext
    if "wx_fmt=png" in url:
        return "png"
    if "wx_fmt=gif" in url:
        return "gif"
    return default


def _read_if_exists(path):
    """Read file content if it exists, else return None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return None
