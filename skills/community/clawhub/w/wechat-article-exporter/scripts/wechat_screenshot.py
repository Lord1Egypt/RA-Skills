#!/usr/bin/env python3
"""
微信公众号长截图导出工具 - 反反爬优化版
"""
import argparse, re, sys, asyncio, os
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

DEFAULT_OUTPUT_DIR = Path.cwd() / "output"

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

def normalize_wechat_url(raw: str) -> str:
    s = str(raw or "").strip().strip("'\"><")
    import html
    s = html.unescape(s)
    s = re.sub(r"\\+([:/&amp;?=#%])", r"\1", s)
    if s.startswith("mp.weixin.qq.com/"):
        s = "https://" + s
    return s

def validate_wechat_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme == "https" and parsed.hostname == "mp.weixin.qq.com" and "/s/" in parsed.path
    except:
        return False

async def take_screenshot(url: str, output_dir: Path) -> dict:
    from playwright.async_api import async_playwright

    results = {"url": url, "title": "", "author": "", "screenshot_path": None, "error": None}

    try:
        async with async_playwright() as p:
            # 用 launch_persistent_context 更像真实浏览器
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
                    # 反自动化检测
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-bundled-ppapi-flash",
                    "--disable-infobars",
                    "--disable-ipc-flooding-protection",
                    "--disable-renderer-backgrounding",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-client-side-phishing-detection",
                    "--disable-crash-reporter",
                    "--disable-oopr-debug-crash-dump",
                    "--no-crash-upload",
                    "--disable-hang-monitor",
                    "--disable-popup-blocking",
                    "--disable-prompt-on-repost",
                    "--disable-sync",
                    "--enable-async-dns",
                    "--enable-simple-cache-backend",
                    "--metrics-recording-only",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--no/experiments/switches",
                    "--safebrowsing-disable-auto-update",
                    "--use-mock-keychain",
                    "--allow-pre-commit-input",
                    "--hide-scrollbars",
                    "--mute-audio",
                    "--disable-extensions",
                    "--disable-features=TranslateUI",
                    "--disable-logging",
                    "--logging-level=0",
                ],
                extra_http_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                },
            )

            page = context.pages[0] if context.pages else await context.new_page()

            # 深度反检测：覆盖更多自动化属性
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en_US', 'en'] });
                Object.defineProperty(document, 'hidden', { get: () => false });
                Object.defineProperty(document, 'visibilityState', { get: () => 'visible' });
                window.chrome = { runtime: {}, app: {}, loadTimes: function(){},_csi: function(){} };
                window.navigator.chrome = { runtime: {}, app: {}, loadTimes: function(){},_csi: function(){} };
                Object.defineProperty(navigator, 'chrome', { get: () => ({ runtime: {}, app: {}, loadTimes: function(){},_csi: function(){} }) });
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
                Object.defineProperty(navigator, 'touchEvent', { get: () => undefined });
                window.callPhantom = undefined;
                window._phantom = undefined;
                window.__nightmare = undefined;
                window.Buffer = undefined;
            """)

            print(f"🔄 正在处理: {url}")
            print("🌐 正在加载页面...")

            try:
                response = await page.goto(url, wait_until="networkidle", timeout=30000)
                if response:
                    print(f"   状态码: {response.status}")
            except Exception as e:
                print(f"   页面加载: {e}")

            await asyncio.sleep(8)  # 等 JS 完全加载

            # 检测验证码
            try:
                page_text = await page.evaluate("document.body.innerText")
                if "验证" in page_text or "异常" in page_text or "太过频繁" in page_text:
                    results["error"] = "⚠️ 微信检测到异常访问，请稍后再试"
                    await context.close()
                    return results
            except:
                pass

            # 获取标题
            for sel in ['h1.rich_media_title', '#activity-name', '.rich_media_title', 'h1']:
                try:
                    el = await page.query_selector(sel)
                    if el:
                        t = await el.text_content()
                        if t and len(t.strip()) > 5:
                            results["title"] = t.strip()
                            break
                except:
                    continue

            if not results["title"]:
                results["title"] = "微信文章"

            print(f"📄 标题: {results['title']}")

            # 智能滚动
            await smart_scroll(page)

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

            safe_title = re.sub(r'[/\\?%*:|"<>]', "_", results["title"])[:60]
            article_dir = output_dir / safe_title
            article_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            screenshot_path = article_dir / f"{safe_title}-{timestamp}.png"

            # 分段截图 + 精确拼接（消除重复）
            # 策略：每段带 OVERLAP 重叠区，拼接时裁掉重叠部分
            print("📐 正在测量页面总高度...")
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(1)
            total_height = await page.evaluate(
                "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight)"
            )
            viewport_h = await page.evaluate("window.innerHeight")
            dpr = await page.evaluate("window.devicePixelRatio")
            # 多次触底刷新高度
            for _ in range(3):
                await page.evaluate(f"window.scrollTo(0, {total_height})")
                await asyncio.sleep(1.5)
                h2 = await page.evaluate(
                    "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
                )
                if h2 > total_height:
                    total_height = h2
                    await page.evaluate(f"window.scrollTo(0, {total_height})")
                    await asyncio.sleep(1)
                else:
                    break
            print(f"   页面总高度: {total_height}px, DPR: {dpr}, viewport: {viewport_h}px")

            print("📷 正在分段截图...")
            OVERLAP = int(viewport_h * 0.15)  # 15% 重叠（约128px），用于消除拼接缝
            step = viewport_h - OVERLAP  # 每段实际前进 step 像素
            num_segments = max(1, int((total_height - viewport_h) / step) + 2)
            segment_paths = []
            for i in range(num_segments):
                scroll_y = i * step
                if scroll_y + viewport_h > total_height:
                    scroll_y = total_height - viewport_h
                await page.evaluate(f"window.scrollTo(0, {scroll_y})")
                await asyncio.sleep(0.8)  # 等待滚动稳定
                seg_path = article_dir / f"_seg_{i}.png"
                await page.screenshot(path=str(seg_path))
                segment_paths.append((scroll_y, str(seg_path)))
                print(f"   段 {i+1}/{num_segments}: y={scroll_y}px")

            # 精确拼接：每段按滚动位置计算实际像素坐标，裁掉重叠
            print("🖼️ 正在拼接...")
            from PIL import Image
            segment_imgs = [(y, Image.open(p)) for y, p in segment_paths]
            seg_width = segment_imgs[0][1].size[0]

            # 计算每段在最终图中的位置（CSS像素）
            combined_height_px = total_height * int(dpr)
            combined = Image.new('RGB', (seg_width, combined_height_px), (255, 255, 255))

            for i, (scroll_y, img) in enumerate(segment_imgs):
                # 计算这段在合并图中的 y 坐标（CSS像素转物理像素）
                css_y = scroll_y
                phys_y = css_y * int(dpr)
                combined.paste(img, (0, phys_y))
                img.close()

            combined.save(str(screenshot_path))
            results["screenshot_path"] = str(screenshot_path)
            print(f"✅ 完成: {screenshot_path} ({seg_width}x{combined_height_px})")

            # 清理临时分段文件
            for _, p in segment_paths:
                Path(p).unlink()

            # 转 PDF
            try:
                from PIL import Image
                pdf_path = article_dir / f"{safe_title}-{timestamp}.pdf"
                img = Image.open(screenshot_path)
                if img.mode in ('RGBA', 'P'):
                    bg = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'RGBA':
                        bg.paste(img, mask=img.split()[3])
                    else:
                        bg.paste(img)
                    img = bg
                img.save(pdf_path, 'PDF', resolution=100.0)
                results["pdf_path"] = str(pdf_path)
            except Exception as e:
                print(f"   ⚠️ PDF 转换: {e}")

            await context.close()

    except Exception as e:
        results["error"] = f"导出失败: {e}"

    return results

async def smart_scroll(page):
    import asyncio

    # 第一步：强制触发所有懒加载图片
    await page.evaluate("""
        () => {
            // 强制加载所有 data-src 图片
            document.querySelectorAll('img[data-src]').forEach(img => {
                if (!img.src.startsWith('http') || img.src === img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
            // 强制所有图片加载
            document.querySelectorAll('img').forEach(img => {
                if (img.dataset && img.dataset.src) {
                    img.src = img.dataset.src;
                }
                if (!img.src || img.src === window.location.href) {
                    const parent = img.closest('div[data-src], section[data-src]');
                    if (parent) img.src = parent.dataset.src;
                }
            });
        }
    """)

    # 第二步：滚动到顶部
    await page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(1)

    # 第三步：滚动到页面底部，触发所有懒加载
    total_height = await page.evaluate(
        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight)"
    )
    await page.evaluate(f"window.scrollTo(0, {total_height})")
    await asyncio.sleep(3)

    # 多次触底刷新高度（微信会动态扩展内容）
    for _ in range(5):
        new_height = await page.evaluate(
            "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
        )
        if new_height > total_height:
            total_height = new_height
            await page.evaluate(f"window.scrollTo(0, {total_height})")
            await asyncio.sleep(2)
        else:
            break

    # 第四步：逐步向上滚动，每步都等待图片加载
    new_height = await page.evaluate(
        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
    )
    if new_height > total_height:
        total_height = new_height

    viewport = await page.evaluate("window.innerHeight")
    step = max(viewport // 3, 200)
    pos = total_height

    while pos > 0:
        await page.evaluate(f"window.scrollTo(0, {pos})")
        await asyncio.sleep(0.4)
        # 触发可视区域图片加载
        await page.evaluate("""
            () => {
                const visibleTop = window.scrollY;
                const visibleBottom = visibleTop + window.innerHeight;
                document.querySelectorAll('img[data-src]').forEach(img => {
                    const rect = img.getBoundingClientRect();
                    if (rect.top >= visibleTop - 500 && rect.top <= visibleBottom + 500) {
                        if (!img.src.startsWith('http') || img.src === img.dataset.src) {
                            img.src = img.dataset.src;
                        }
                    }
                });
            }
        """)
        pos -= step

    # 第五步：直接留在底部（不去顶部，避免full_page截图范围异常）

    # 第六步：最终等待所有图片加载完成
    try:
        await page.wait_for_function("""
            () => {
                const imgs = [...document.querySelectorAll('img')];
                if (imgs.length === 0) return true;
                return imgs.every(img => {
                    return img.complete && img.naturalWidth > 0 && img.naturalHeight > 0;
                });
            }
        """, timeout=15000)
        print("   ✅ 所有图片加载完成")
    except Exception as e:
        print(f"   ⚠️ 部分图片加载超时: {e}")

    # 第七步：确保在底部，等待底部内容渲染完成
    total_height = await page.evaluate(
        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
    )
    # 滚到真正的底部
    await page.evaluate(f"window.scrollTo(0, {total_height})")
    await asyncio.sleep(3)
    # 检查最终内容
    final_height = await page.evaluate(
        "Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
    )
    if final_height > total_height:
        total_height = final_height
        await page.evaluate(f"window.scrollTo(0, {total_height})")
        await asyncio.sleep(2)
    print(f"   页面总高度: {total_height}px")

def main():
    parser = argparse.ArgumentParser(description="微信公众号长截图导出")
    parser.add_argument("url", help="微信文章 URL")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    url = normalize_wechat_url(args.url)
    if not validate_wechat_url(url):
        print("❌ 请输入有效的 mp.weixin.qq.com 文章链接")
        sys.exit(1)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = asyncio.run(take_screenshot(url, output_dir))
    if results.get("error"):
        print(f"❌ {results['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
