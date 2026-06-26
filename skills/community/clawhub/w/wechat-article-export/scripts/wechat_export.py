#!/usr/bin/env python3
"""
微信公众号多功能导出工具
支持：长截图(PNG) / PDF / Markdown 三种格式

用法:
    python wechat_export.py "<URL>" -f <格式> [-o <输出目录>]
    python wechat_export.py "<URL>" -f all                    # 导出全部格式

格式:
    screenshot  - 长截图 PNG（移动端视图，3x DPR）
    pdf         - PDF 文档（基于截图转换）
    markdown    - 高质量 Markdown（保留代码块/图片/格式）
    all         - 全部格式

依赖:
    pip install playwright beautifulsoup4 markdownify requests Pillow
    playwright install chromium
"""

import argparse
import asyncio
import re
import sys
import os
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# ─────────────────────────────────────────────
# 路径配置（相对于脚本目录自动推导）
# ─────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
EXPORT_DIR = Path.cwd() / "output"

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

# ══════════════════════════════════════════════
# 工具函数
# ══════════════════════════════════════════════

def normalize_wechat_url(raw: str) -> str:
    import html
    s = str(raw or "").strip().strip("'\"><")
    s = html.unescape(s)
    s = re.sub(r"\\+([:/&amp;?=#%])", r"\1", s)
    if s.startswith("mp.weixin.qq.com/"):
        s = "https://" + s
    return s

def validate_wechat_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme == "https" and parsed.hostname == "mp.weixin.qq.com" and parsed.path.startswith("/s")
    except:
        return False

def sanitize_filename(name: str) -> str:
    import unicodedata
    name = unicodedata.normalize("NFKC", str(name))
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", name)
    name = re.sub(r"\s+", "_", name)
    name = name.strip("._")
    return name[:60] if len(name) > 60 else name or "wechat_article"

# ══════════════════════════════════════════════
# 截图核心（来自 wechat_screenshot.py）
# ══════════════════════════════════════════════

async def _smart_scroll(page):
    import asyncio as _asyncio

    await page.evaluate("""
        () => {
            document.querySelectorAll('img[data-src]').forEach(img => {
                if (!img.src.startsWith('http') || img.src === img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
            document.querySelectorAll('img').forEach(img => {
                if (img.dataset && img.dataset.src) img.src = img.dataset.src;
                if (!img.src || img.src === window.location.href) {
                    const parent = img.closest('div[data-src], section[data-src]');
                    if (parent) img.src = parent.dataset.src;
                }
            });
        }
    """)

    await page.evaluate("window.scrollTo(0, 0)")
    await _asyncio.sleep(1)

    # 关闭并隐藏临时链接横幅（固定在顶部，截图时会出现在每段）
    await page.evaluate("""
        () => {
            // 点击关闭按钮
            const closeBtn = document.querySelector('#js_close_temp');
            if (closeBtn) closeBtn.click();
            // 强制隐藏横幅容器
            const banner = document.querySelector('#preview_bar.rich_media_global_msg');
            if (banner) banner.style.display = 'none';
            const inner = document.querySelector('.rich_media_global_msg_inner');
            if (inner) inner.style.display = 'none';
        }
    """)
    await _asyncio.sleep(0.5)

    total_height = await page.evaluate(
        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight)"
    )
    await page.evaluate(f"window.scrollTo(0, {total_height})")
    await _asyncio.sleep(3)

    for _ in range(5):
        new_h = await page.evaluate(
            "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
        )
        if new_h > total_height:
            total_height = new_h
            await page.evaluate(f"window.scrollTo(0, {total_height})")
            await _asyncio.sleep(2)
        else:
            break

    viewport = await page.evaluate("window.innerHeight")
    step = max(viewport // 3, 200)
    pos = total_height
    while pos > 0:
        await page.evaluate(f"window.scrollTo(0, {pos})")
        await _asyncio.sleep(0.4)
        await page.evaluate("""
            () => {
                const visTop = window.scrollY, visBot = visTop + window.innerHeight;
                document.querySelectorAll('img[data-src]').forEach(img => {
                    const r = img.getBoundingClientRect();
                    if (r.top >= visTop - 500 && r.top <= visBot + 500) {
                        if (!img.src.startsWith('http') || img.src === img.dataset.src)
                            img.src = img.dataset.src;
                    }
                });
            }
        """)
        pos -= step

    try:
        await page.wait_for_function("""
            () => {
                const imgs = [...document.querySelectorAll('img')];
                if (imgs.length === 0) return true;
                return imgs.every(img => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0);
            }
        """, timeout=15000)
        print("      ✅ 所有图片加载完成")
    except Exception as e:
        print(f"      ⚠️ 部分图片加载超时: {e}")

    total_height = await page.evaluate(
        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
    )
    await page.evaluate(f"window.scrollTo(0, {total_height})")
    await _asyncio.sleep(3)

async def _take_screenshot(url: str, output_dir: Path, formats=None) -> dict:
    from playwright.async_api import async_playwright as _pw
    from PIL import Image

    result = {"url": url, "title": "", "screenshot_path": None, "pdf_path": None, "html": None, "error": None}

    try:
        async with _pw() as p:
            context = await p.chromium.launch_persistent_context(
                "",
                headless=True,
                viewport={"width": 393, "height": 852},
                device_scale_factor=3,
                user_agent=MOBILE_UA,
                locale="zh-CN",
                timezone_id="Asia/Shanghai",
                is_mobile=True,
                has_touch=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox", "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage", "--disable-gpu",
                    "--disable-bundled-ppapi-flash",
                    "--disable-infobars", "--disable-ipc-flooding-protection",
                    "--disable-renderer-backgrounding",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-client-side-phishing-detection",
                    "--disable-crash-reporter", "--disable-hang-monitor",
                    "--disable-popup-blocking", "--disable-prompt-on-repost",
                    "--disable-sync", "--enable-async-dns",
                    "--enable-simple-cache-backend",
                    "--metrics-recording-only",
                    "--no-first-run", "--no-default-browser-check",
                    "--safebrowsing-disable-auto-update",
                    "--use-mock-keychain",
                    "--hide-scrollbars", "--mute-audio",
                    "--disable-extensions",
                    "--disable-features=TranslateUI",
                    "--disable-logging", "--logging-level=0",
                ],
                extra_http_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1",
                },
            )

            page = context.pages[0] if context.pages else await context.new_page()

            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en_US', 'en'] });
                Object.defineProperty(document, 'hidden', { get: () => false });
                Object.defineProperty(document, 'visibilityState', { get: () => 'visible' });
                window.chrome = { runtime: {}, app: {}, loadTimes: function(){}, _csi: function(){} };
                window.navigator.chrome = { runtime: {}, app: {}, loadTimes: function(){}, _csi: function(){} };
                Object.defineProperty(navigator, 'chrome', { get: () => ({ runtime: {}, app: {}, loadTimes: function(){}, _csi: function(){} }) });
                if (!navigator.permissions) navigator.permissions = {};
                Object.defineProperty(navigator.permissions, 'query', {
                    value: async (params) => {
                        if (params.name === 'notifications') return { state: Notification.permission === 'granted' ? 'granted' : 'default' };
                        return { state: 'prompt' };
                    }
                });
                Object.defineProperty(screen, 'colorDepth', { get: () => 24 });
                Object.defineProperty(screen, 'pixelDepth', { get: () => 24 });
                Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5 });
                window.callPhantom = undefined; window._phantom = undefined;
                window.__nightmare = undefined; window.Buffer = undefined;
            """)

            print(f"  🔄 正在加载页面...")
            try:
                resp = await page.goto(url, wait_until="networkidle", timeout=30000)
                if resp:
                    print(f"     状态码: {resp.status}")
            except Exception as e:
                print(f"     页面加载: {e}")

            await asyncio.sleep(8)

            # 验证码检测
            try:
                txt = await page.evaluate("document.body.innerText")
                if any(k in txt for k in ("验证", "异常", "太过频繁")):
                    result["error"] = "⚠️ 微信检测到异常访问，请稍后再试"
                    await context.close()
                    return result
            except:
                pass

            # 捕獲完整 HTML（供 Markdown 共用）
            html = await page.content()

            # 获取标题
            for sel in ['h1.rich_media_title', '#activity-name', '.rich_media_title', 'h1']:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        t = await el.text_content()
                        if t and len(t.strip()) > 5:
                            result["title"] = t.strip()
                            break
                except:
                    continue

            if not result["title"]:
                result["title"] = "微信文章"

            print(f"  📄 标题: {result['title']}")

            await _smart_scroll(page)

            # 隐藏底部工具栏
            await page.evaluate("""
                () => {
                    const bars = ['.bottom_bar_wrp', '.bottom_bar_interaction_wrp', '.bottom_bar_interaction',
                                  '#bottom_bar', '.wx_expand_article_bottom_area', '.unlogin_bottom_bar'];
                    bars.forEach(s => document.querySelectorAll(s).forEach(el => {
                        el.style.display='none'; el.style.visibility='hidden';
                    }));
                    document.querySelectorAll('*').forEach(el => {
                        const r = el.getBoundingClientRect();
                        if (getComputedStyle(el).position === 'fixed' && r.top > window.innerHeight - 100)
                            el.style.display = 'none';
                    });
                }
            """)

            safe_title = sanitize_filename(result["title"])
            article_dir = output_dir / safe_title
            article_dir.mkdir(parents=True, exist_ok=True)

            ts = datetime.now().strftime("%Y%m%d%H%M%S")

            # 测量页面高度
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(1)
            total_height = await page.evaluate(
                "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight)"
            )
            viewport_h = await page.evaluate("window.innerHeight")
            dpr = await page.evaluate("window.devicePixelRatio")

            for _ in range(3):
                await page.evaluate(f"window.scrollTo(0, {total_height})")
                await asyncio.sleep(1.5)
                h2 = await page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
                if h2 > total_height:
                    total_height = h2
                    await page.evaluate(f"window.scrollTo(0, {total_height})")
                    await asyncio.sleep(1)
                else:
                    break

            print(f"  📐 页面总高度: {total_height}px, DPR: {dpr}")

            # 分段截图
            OVERLAP = int(viewport_h * 0.15)
            step = viewport_h - OVERLAP
            num_segments = max(1, int((total_height - viewport_h) / step) + 2)
            segment_paths = []

            for i in range(num_segments):
                scroll_y = i * step
                if scroll_y + viewport_h > total_height:
                    scroll_y = total_height - viewport_h
                await page.evaluate(f"window.scrollTo(0, {scroll_y})")
                await asyncio.sleep(0.8)
                seg_path = article_dir / f"_seg_{i}.png"
                await page.screenshot(path=str(seg_path))
                segment_paths.append((scroll_y, str(seg_path)))

            # 拼接
            print("  🖼️  正在拼接...")
            segment_imgs = [(y, Image.open(p)) for y, p in segment_paths]
            seg_width = segment_imgs[0][1].size[0]
            combined_h_px = total_height * int(dpr)
            combined = Image.new('RGB', (seg_width, combined_h_px), (255, 255, 255))

            for i, (scroll_y, img) in enumerate(segment_imgs):
                phys_y = scroll_y * int(dpr)
                combined.paste(img, (0, phys_y))
                img.close()

            for _, p in segment_paths:
                Path(p).unlink()

            # ── 截圖：僅當明確請求時保存 PNG ──
            screenshot_path = None
            want_ss = not formats or "screenshot" in formats
            want_pdf = not formats or "pdf" in formats

            if want_ss:
                screenshot_path = article_dir / f"{safe_title}-{ts}.png"
                combined.save(str(screenshot_path))
                result["screenshot_path"] = str(screenshot_path)
                print(f"  ✅ 截图完成: {screenshot_path} ({seg_width}x{combined_h_px})")
            else:
                print("  ⏭️  跳过截图（未请求）")

            # ── PDF：需要拼接圖作為來源，無論是否請求截圖都即時生成 ──
            pdf_path = None
            if want_pdf:
                # 若未保存截圖，則用拼接圖直接轉 PDF（不留下 PNG）
                pdf_img = combined
                if not want_ss:
                    # 保存到臨時路徑，轉 PDF 後即刪除
                    import tempfile
                    tmp_png = Path(tempfile.gettempdir()) / f"_wechat_pdf_src_{ts}.png"
                    combined.save(str(tmp_png))
                    pdf_img = Image.open(str(tmp_png))
                try:
                    if pdf_img.mode in ('RGBA', 'P'):
                        bg = Image.new('RGB', pdf_img.size, (255, 255, 255))
                        if pdf_img.mode == 'RGBA':
                            bg.paste(pdf_img, mask=pdf_img.split()[3])
                        else:
                            bg.paste(pdf_img)
                        pdf_img = bg
                    pdf_path = article_dir / f"{safe_title}-{ts}.pdf"
                    pdf_img.save(str(pdf_path), 'PDF', resolution=100.0)
                    result["pdf_path"] = str(pdf_path)
                    print(f"  ✅ PDF 完成: {pdf_path}")
                    if not want_ss and tmp_png.exists():
                        tmp_png.unlink()   # 清理臨時 PNG
                except Exception as e:
                    print(f"  ⚠️ PDF 转换: {e}")
            else:
                print("  ⏭️  跳过 PDF（未请求）")

            await context.close()
            result["html"] = html

    except Exception as e:
        result["error"] = f"截图导出失败: {e}"

    return result

# ══════════════════════════════════════════════
# Markdown 核心（来自 wechat_to_md.py）
# ══════════════════════════════════════════════

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

def _html_unescape(text):
    return (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&#39;", "'").replace("&#x27;", "'"))

def _normalize_url(raw):
    raw = raw.strip()
    raw = _html_unescape(raw)
    if raw.startswith("//"):
        raw = "https:" + raw
    if not raw.startswith("http"):
        raw = "https://" + raw
    return raw

def _fetch_html_playwright(url, timeout=30000):
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                user_agent=DEFAULT_UA,
                locale="zh-CN",
                viewport={"width": 1280, "height": 900},
                extra_http_headers={"Accept-Language": "zh-CN,zh;q=0.9"},
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            for sel in ["#js_content", ".rich_media_content", "#page-content"]:
                try:
                    page.wait_for_selector(sel, timeout=5000)
                    break
                except PWTimeout:
                    continue
            if "验证" in page.title() or "verify" in page.url.lower():
                raise RuntimeError("页面被验证码拦截")
            return page.content()
        finally:
            browser.close()

def _fetch_html(url):
    try:
        return _fetch_html_playwright(url)
    except Exception as e:
        import requests as _req
        print(f"     [降级] Playwright 不可用，使用 requests: {e}")
        resp = _req.get(url, timeout=20,
                        headers={"User-Agent": DEFAULT_UA,
                                 "Accept-Language": "zh-CN,zh;q=0.9",
                                 "Referer": "https://mp.weixin.qq.com/"},
                        allow_redirects=True)
        resp.raise_for_status()
        # 智能編碼檢測：Content-Type header > apparent_encoding > gb18030
        content_type = resp.headers.get("Content-Type", "").lower()
        if "charset=" in content_type:
            enc = content_type.split("charset=")[-1].strip(" '").split(";")[0].strip()
            if enc in ("utf-8", "utf8", "gbk", "gb2312", "gb18030"):
                resp.encoding = enc
            else:
                resp.encoding = resp.apparent_encoding or "utf-8"
        else:
            # 微信文章主要用 UTF-8 或 gb 系列，優先試 UTF-8
            resp.encoding = resp.apparent_encoding or "utf-8"
        return resp.text

NOISE_SELECTORS = [
    "script", "style", "noscript",
    ".mp_profile_iframe", "#js_pc_close", ".qr_code_pc",
    ".ad_container", "#ad_content", ".mp-ad",
    ".reward_area", "#reward_area", ".rewards_area",
    ".reward_qrcode_area", ".reward_display",
    "#comment_container", ".discuss_container", "#js_cmt_area",
    ".rich_media_tool", "#js_tags_wrap",
    "#relation_article", ".relation_article",
    "#recommend_article", ".recommend",
    "#page_bottom",
    ".rich_media_meta_nickname_extra",
    "#js_read_area3", "#js_like_area",
    ".rich_media_footer", "#js_bottom_ad_area",
    "mpvoice", ".mp_voice_inner", "mpvideo", ".mp_video_inner",
    ".scene_scene_card_qrcode", ".qr_code_pc_area",
    "#copyright_area", ".copyright_area",
    ".rich_media_extra", "#js_ip_wording_wrp",
    ".js_poi_popover", ".global_avatar_msg_card",
    ".rich_media_global_comment_confirm",
    ".rich_media_global_msg", ".rich_media_global_msg_inner", "#preview_bar",
    "[id*='audio']", "[class*='audio-player']",
    "[class*='follow_tip']", "[class*='guide']",
    "[class*='promotion']", "[class*='advertise']",
]

def _remove_noise(soup):
    for sel in NOISE_SELECTORS:
        for el in soup.select(sel):
            el.decompose()

def _remove_hidden(soup):
    for el in list(soup.find_all(True)):
        try:
            style = el.get("style", "") or ""
            sc = style.replace(" ", "").lower()
            if "display:none" in sc or "visibility:hidden" in sc:
                el.decompose()
        except:
            continue

def _fix_images(soup):
    urls = []
    seen = set()
    for img in soup.find_all("img"):
        ds = img.get("data-src", "")
        if ds and ("mmbiz" in ds or ds.startswith("http")):
            img["src"] = ds
            if ds not in seen:
                seen.add(ds)
                urls.append(ds)
        src = img.get("src", "")
        if src and src not in seen and ("mmbiz" in src or src.startswith("http")):
            seen.add(src)
            urls.append(src)
        for attr in list(img.attrs):
            if attr.startswith("data-") and attr != "data-src":
                del img[attr]
    return urls

LANG_HINTS = {
    "python": ["def ", "import ", "from ", "class ", "self.", "print(", "if __name__"],
    "javascript": ["const ", "let ", "var ", "function", "=>", "console.log"],
    "typescript": ["interface ", "type ", "enum ", ": string", ": number"],
    "java": ["public class", "public static", "System.out", "private "],
    "go": ["func ", "package ", "import (", "fmt.Print", ":="],
    "rust": ["fn ", "let mut", "impl ", "pub fn", "use std::"],
    "c": ["#include", "printf(", "malloc(", "int main", "void "],
    "cpp": ["cout", "cin", "std::", "namespace", "vector<"],
    "shell": ["#!/bin/bash", "#!/bin/sh", "echo $", "apt-get"],
    "sql": ["SELECT ", "INSERT ", "UPDATE ", "CREATE TABLE"],
    "html": ["<!DOCTYPE", "<html", "<div", "<head"],
    "css": ["margin:", "padding:", "display:", "background:"],
    "json": ['"key":', '"name":', '"type":'],
    "yaml": ["---", "key:", "apiVersion:", "spec:"],
    "dockerfile": ["FROM ", "RUN ", "COPY ", "WORKDIR", "EXPOSE "],
}

def _detect_lang(code_text, hint=""):
    if hint and hint.strip().lower() not in ("text", "plain", "none", ""):
        return hint.strip().lower()
    first = code_text.strip().split("\n")[0] if code_text.strip() else ""
    if first.startswith("#!"):
        for kw in ["python", "bash", "node", "ruby"]:
            if kw in first:
                return kw
        return "bash"
    scores = {}
    sample = code_text[:3000]
    for lang, hints in LANG_HINTS.items():
        scores[lang] = sum(1 for h in hints if h in sample)
    if scores:
        return max(scores, key=scores.get)
    return ""

def _process_code_blocks(soup):
    code_blocks = []
    processed = set()
    for sel in ["pre.code-snippet", ".code-snippet__fix", "pre[data-lang]", "pre"]:
        for el in soup.select(sel):
            eid = id(el)
            if eid in processed:
                continue
            processed.add(eid)
            lang = el.get("data-lang", "")
            for cls in el.get("class", []):
                cls_s = str(cls)
                if cls_s.startswith("language-") or cls_s.startswith("lang-"):
                    lang = cls_s.split("-", 1)[1]
                    break
            for lb in el.select(".code-snippet__line-index, [class*='line-number'], .hljs-ln-n"):
                lb.decompose()
            code_tag = el.find("code")
            raw = code_tag.get_text(separator="\n") if code_tag else el.get_text(separator="\n")
            lines = []
            for line in raw.split("\n"):
                s = line.strip()
                if not re.match(r"^[ce]?ounter\(line", s):
                    lines.append(line)
            code_text = "\n".join(lines).strip()
            if not code_text:
                continue
            idx = len(code_blocks)
            placeholder = f"__CODEBLOCK_{idx}__"
            code_blocks.append({"lang": _detect_lang(code_text, lang), "code": code_text})
            p = soup.new_tag("p")
            p.string = placeholder
            el.replace_with(p)
    return code_blocks

def _optimize_rich_text(soup):
    for section in list(soup.find_all("section")):
        try:
            style = section.get("style", "") or ""
            sc = style.replace(" ", "").lower()
            cls = " ".join(str(c) for c in section.get("class", []))
            if "border-left" in sc or "blockquote" in cls:
                section.name = "blockquote"
                continue
            if "font-size" in sc:
                m = re.search(r"font-size:\s*(\d+)px", style)
                if m:
                    sz = int(m.group(1))
                    section.name = {22: "h2", 19: "h3", 17: "h4"}.get(sz, section.name)
        except:
            continue
    for b in list(soup.find_all("b")):
        try:
            b.name = "strong"
        except:
            pass
    for i in list(soup.find_all("i")):
        try:
            if not i.find_parent("em"):
                i.name = "em"
        except:
            pass
    for p in list(soup.find_all("p")):
        try:
            if not p.get_text(strip=True) and not p.find("img"):
                p.decompose()
        except:
            pass

def _html_to_md(content_html, code_blocks):
    try:
        import markdownify
    except ImportError:
        sys.exit("缺少 markdownify: pip install markdownify")
    md = markdownify.markdownify(
        content_html,
        heading_style="ATX",
        bullets="-",
        newline_style="backslash",
        convert=["p","h1","h2","h3","h4","h5","h6","strong","b","em","i",
                 "a","img","ul","ol","li","blockquote","br","hr",
                 "table","thead","tbody","tr","th","td","pre","code","sup","sub"],
    )
    for i, block in enumerate(code_blocks):
        ph = f"__CODEBLOCK_{i}__"
        lang = block.get("lang", "")
        code = block.get("code", "")
        fenced = f"\n\n```{lang}\n{code}\n```\n\n"
        md = md.replace(ph, fenced)
        md = md.replace(f"`{ph}`", fenced)
    return md

def _postprocess_md(md, meta, no_frontmatter=False):
    md = (md.replace("\u00a0", " ").replace("\u200b", "").replace("\u200c", "")
           .replace("\u200d", "").replace("\u3000", "  "))
    md = _html_unescape(md)
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    md = re.sub(r"[ \t]+$", "", md, flags=re.MULTILINE)
    md = re.sub(r"\n{3,}(```)", r"\n\n```", md)
    md = re.sub(r"(```)\n{3,}", r"```\n\n", md)
    if no_frontmatter:
        return md.strip() + "\n"
    def ey(s):
        return s.replace("\\","\\\\").replace('"', '\\"').replace("\n"," ").strip()
    fm = ["---",
          f'title: "{ey(meta.get("title",""))}"',
          f'author: "{ey(meta.get("author",""))}"',
          f'date: "{ey(meta.get("publish_date",""))}"',
          f'source: "{ey(meta.get("url",""))}"']
    if meta.get("description"):
        fm.append(f'description: "{ey(meta["description"])}"')
    fm.append("---")
    return "\n".join(fm) + "\n\n" + md.strip() + "\n"

def _extract_metadata(soup, url):
    title = ""
    for sel in ["#activity-name","#js_activity_name","h1.rich_media_title","h1#activity-name",
                ".rich_media_title","#js_title"]:
        el = soup.select_one(sel)
        if el:
            title = el.get_text(strip=True)
            if title:
                break
    if not title:
        title = soup.title.string if soup.title else "未知标题"
    title = _html_unescape(title).strip()

    author = ""
    for sel in ["#js_name",".profile_nickname","strong.rich_media_meta_text",
                "#js_author_name","a.rich_media_meta_link",".account_nickname_inner"]:
        el = soup.select_one(sel)
        if el:
            author = el.get_text(strip=True)
            if author:
                break
    author = _html_unescape(author).strip() if author else "未知公众号"

    date = ""
    for sel in ["#publish_time","em#publish_time"]:
        el = soup.select_one(sel)
        if el:
            date = el.get_text(strip=True)
            if date:
                break
    if not date:
        mt = soup.find("meta", attrs={"property": "article:published_time"})
        if mt:
            date = mt.get("content", "")

    desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md:
        desc = md.get("content", "")

    return {"title": title, "author": author, "publish_date": date,
            "description": desc, "url": url}

def _download_images(img_urls, output_dir, concurrency=5, timeout=30, retries=2):
    import requests as _req
    import concurrent.futures
    from time import sleep

    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    url_to_local = {}

    def _dl(url, idx):
        from urllib.parse import urlparse as _up
        ext = ".jpg"
        try:
            p = _up(url).path.lower()
            for e in [".png",".jpg",".jpeg",".gif",".webp",".bmp",".svg"]:
                if p.endswith(e):
                    ext = e
                    break
        except:
            pass
        path = images_dir / f"img_{idx:03d}{ext}"
        for attempt in range(retries + 1):
            try:
                resp = _req.get(url, timeout=timeout, stream=True, allow_redirects=True)
                resp.raise_for_status()
                ct = resp.headers.get("Content-Type", "").lower()
                if "png" in ct: ext = ".png"
                elif "gif" in ct: ext = ".gif"
                elif "webp" in ct: ext = ".webp"
                elif "jpeg" in ct or "jpg" in ct: ext = ".jpg"
                path = images_dir / f"img_{idx:03d}{ext}"
                if path.exists() and path.stat().st_size > 100:
                    return url, str(path)
                with open(path, "wb") as f:
                    for chunk in resp.iter_content(8192):
                        if chunk: f.write(chunk)
                if path.stat().st_size < 100:
                    path.unlink()
                    raise ValueError("file too small")
                return url, str(path)
            except:
                if attempt < retries: sleep(0.5 * (attempt+1))
                continue
        return url, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as exe:
        futures = {exe.submit(_dl, u, i): u for i, u in enumerate(img_urls)}
        for fut in concurrent.futures.as_completed(futures):
            u, local = fut.result()
            if local:
                url_to_local[u] = local

    return url_to_local

def _replace_img_urls(md, url_to_local):
    if not url_to_local:
        return md
    for orig, local in url_to_local.items():
        md = md.replace(orig, "images/" + Path(local).name)
    # 处理 URL 变体
    for orig, local in url_to_local.items():
        base = orig.split('?')[0]
        if base != orig:
            md = re.sub(re.escape(base) + r'(?:\?[^)"\]\s]*)?',
                        lambda m: "images/" + Path(local).name, md)
    return re.sub(r'images/images/', 'images/', md)

async def _export_markdown(url: str, output_dir: Path, download_imgs=True,
                           no_frontmatter=False,
                           pre_fetched_html: str = None,
                           pre_fetched_title: str = None) -> dict:
    from bs4 import BeautifulSoup

    result = {"url": url, "title": pre_fetched_title or "", "markdown_path": None, "error": None}
    url = _normalize_url(url)

    try:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        if pre_fetched_html:
            html = pre_fetched_html
            print("  🔄 使用預取 HTML（節省一次瀏覽器啟動）...")
        else:
            print("  🔄 正在抓取 HTML...")
            html = _fetch_html(url)
            print(f"     OK ({len(html)} 字节)")

        soup = BeautifulSoup(html, "html.parser")
        meta = _extract_metadata(soup, url)
        result["title"] = meta["title"]
        print(f"     📄 {meta['title']} | {meta['author']}")

        content = None
        for sel in ["#js_content", ".rich_media_content", "#page-content", "article"]:
            content = soup.select_one(sel)
            if content and content.get_text(strip=True):
                break

        if not content or not content.get_text(strip=True):
            result["error"] = "无法找到文章正文"
            return result

        _remove_noise(content)
        _remove_hidden(content)
        img_urls = _fix_images(content)
        code_blocks = _process_code_blocks(content)
        _optimize_rich_text(content)

        md = _html_to_md(str(content), code_blocks)
        md = _postprocess_md(md, meta, no_frontmatter=no_frontmatter)

        safe_title = sanitize_filename(meta["title"])
        article_dir = output_dir / safe_title
        article_dir.mkdir(parents=True, exist_ok=True)

        if download_imgs and img_urls:
            print(f"  📥 下载 {len(img_urls)} 张图片...")
            url_map = _download_images(img_urls, article_dir)
            if url_map:
                md = _replace_img_urls(md, url_map)
            print(f"     ✅ {len(url_map)}/{len(img_urls)} 张完成")

        md_path = article_dir / f"{safe_title}-{ts}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)

        result["markdown_path"] = str(md_path)
        print(f"  ✅ Markdown 完成: {md_path}")

    except Exception as e:
        result["error"] = f"Markdown 导出失败: {e}"

    return result

# ══════════════════════════════════════════════
# 统一导出入口
# ══════════════════════════════════════════════

async def export_wechat_article(url: str, formats=None, output_dir=None,
                                download_imgs=True, no_frontmatter=False) -> dict:
    """
    统一导出入口。

    Args:
        url: 微信文章 URL
        formats: list[str] 要导出的格式，支持 "screenshot" / "pdf" / "markdown"
                 默认为 ["screenshot", "pdf", "markdown"] 全部
        output_dir: Path 输出根目录，默认 ./output
        download_imgs: bool 是否下载 Markdown 图片（默认 True）
        no_frontmatter: bool Markdown 是否省略 YAML frontmatter（默认 False）

    Returns:
        dict: {
            "title": str,
            "url": str,
            "screenshot_path": str or None,
            "pdf_path": str or None,
            "markdown_path": str or None,
            "error": str or None,
        }
    """
    if formats is None:
        formats = ["screenshot", "pdf", "markdown"]

    url = normalize_wechat_url(url)
    if not validate_wechat_url(url):
        return {"error": "❌ 无效的 mp.weixin.qq.com 链接", "title": "", "url": url,
                "screenshot_path": None, "pdf_path": None, "markdown_path": None}

    if output_dir is None:
        output_dir = EXPORT_DIR
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    combined = {
        "title": "", "url": url,
        "screenshot_path": None, "pdf_path": None, "markdown_path": None,
        "error": None,
    }

    # 第一步：截圖 + PDF（同時順便捕獲 HTML）
    shared_html = None
    shared_title = None
    if "screenshot" in formats or "pdf" in formats or "markdown" in formats:
        ss_result = await _take_screenshot(url, output_dir, formats)
        shared_html = ss_result.get("html")
        shared_title = ss_result.get("title", combined["title"])
        combined["title"] = shared_title or combined["title"]
        combined["screenshot_path"] = ss_result.get("screenshot_path")
        combined["pdf_path"] = ss_result.get("pdf_path")
        if ss_result.get("error") and not combined["error"]:
            combined["error"] = ss_result.get("error")

    # 第二步：Markdown（重用已捕獲的 HTML，不重啟瀏覽器）
    if "markdown" in formats:
        md_result = await _export_markdown(
            url, output_dir, download_imgs, no_frontmatter,
            pre_fetched_html=shared_html,
            pre_fetched_title=combined["title"]
        )
        if md_result.get("title"):
            combined["title"] = md_result["title"]
        combined["markdown_path"] = md_result.get("markdown_path")
        if md_result.get("error") and not combined["error"]:
            combined["error"] = md_result.get("error")

    return combined

# ══════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="微信公众号多功能导出工具（截图 / PDF / Markdown）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python wechat_export.py "<URL>" -f all          # 全部格式
  python wechat_export.py "<URL>" -f screenshot  # 仅截图
  python wechat_export.py "<URL>" -f markdown    # 仅 Markdown
  python wechat_export.py "<URL>" -f screenshot,markdown  # 截图+Markdown
  python wechat_export.py "<URL>" -f screenshot,pdf,markdown -o /tmp/out
        """
    )
    parser.add_argument("url", help="微信文章 URL")
    parser.add_argument("-f", "--formats", default="all",
                        help="导出格式，逗号分隔: screenshot / pdf / markdown / all (默认: all)")
    parser.add_argument("-o", "--output", type=Path, default=EXPORT_DIR,
                        help=f"输出目录 (默认: {EXPORT_DIR})")
    parser.add_argument("--no-images", action="store_true",
                        help="Markdown 不下载图片（保留远程 URL）")
    parser.add_argument("--no-frontmatter", action="store_true",
                        help="Markdown 不生成 YAML frontmatter")

    args = parser.parse_args()

    url = normalize_wechat_url(args.url)
    if not validate_wechat_url(url):
        print("❌ 请输入有效的 mp.weixin.qq.com 文章链接")
        sys.exit(1)

    raw_fmt = args.formats.lower()
    if raw_fmt == "all":
        formats = ["screenshot", "pdf", "markdown"]
    else:
        formats = [f.strip() for f in raw_fmt.split(",")]
        for f in formats:
            if f not in ("screenshot", "pdf", "markdown"):
                print(f"❌ 不支持的格式: {f}，支持: screenshot / pdf / markdown / all")
                sys.exit(1)

    print(f"\n📄 {url}")
    print(f"📦 导出格式: {', '.join(formats)}")
    print(f"📁 输出目录: {args.output}\n")

    result = asyncio.run(
        export_wechat_article(
            url,
            formats=formats,
            output_dir=args.output,
            download_imgs=not args.no_images,
            no_frontmatter=args.no_frontmatter,
        )
    )

    print("\n" + "="*50)
    print(f"📄 标题: {result.get('title', 'N/A')}")
    if result.get("screenshot_path"):
        print(f"🖼️  截图: {result['screenshot_path']}")
    if result.get("pdf_path"):
        print(f"📄 PDF:  {result['pdf_path']}")
    if result.get("markdown_path"):
        print(f"📝 MD:   {result['markdown_path']}")
    if result.get("error"):
        print(f"⚠️  错误: {result['error']}")

    if result.get("error") and not any(result.get(k) for k in ("screenshot_path","pdf_path","markdown_path")):
        sys.exit(1)

if __name__ == "__main__":
    main()
