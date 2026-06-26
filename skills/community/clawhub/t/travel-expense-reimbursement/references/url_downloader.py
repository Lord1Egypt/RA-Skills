"""
邮件发票下载器（url_downloader）

对应 SKILL.md 步骤：第四步「下载无附件情况的发票PDF」

适用场景：
  - himalaya 获取邮件后，发现邮件正文无 PDF/OFD 附件
  - 调用本模块，传入从正文提取的下载链接，模块自动判断用 curl 还是 Playwright 下载

核心逻辑（下载策略）：
  1. curl 直接下载（大多数 CDN/直链场景，成功率最高）
  2. curl 失败（超时/非PDF响应）→ Playwright 访问页面，自主判断下载方式
     - 若页面直接触发 PDF 下载 → 拦截下载事件
     - 若页面需要点击按钮 → 模拟点击后拦截下载
     - 若均失败 → 截图备用，返回截图路径

扩展方式：
  新增发票发件人只需添加新的 handler 即可，无需改动核心逻辑。
  handler 格式：handler(url) -> Optional[str]，返回已下载文件路径或 None

依赖：
    pip install playwright
"""

import os
import re
import time
import tempfile
import shutil
import uuid
import fcntl
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import subprocess

try:
    from playwright.sync_api import sync_playwright, Page, Download
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


# ─────────────────────────────────────────────
# 通用配置
# ─────────────────────────────────────────────

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "application/pdf,application/octet-stream,*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://pis.baiwang.com/",
}


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def get_unique_temp_path(save_dir: str, prefix: str = "tmp") -> tuple[str, str]:
    """
    生成唯一的临时文件路径和响应头路径，避免并发冲突。
    返回 (temp_file_path, headers_path)
    """
    unique_id = str(uuid.uuid4())[:8]
    temp_path = os.path.join(save_dir, f".{prefix}_{unique_id}.download")
    headers_path = os.path.join(save_dir, f".{prefix}_{unique_id}.headers")
    return temp_path, headers_path


class FileLock:
    """简单的文件锁，用于防止并发冲突"""

    def __init__(self, lock_path: str):
        self.lock_path = lock_path
        self.lock_file = None

    def __enter__(self):
        os.makedirs(os.path.dirname(self.lock_path), exist_ok=True)
        self.lock_file = open(self.lock_path, 'w')
        fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.lock_file:
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
            self.lock_file.close()
            try:
                os.remove(self.lock_path)
            except:
                pass


def curl_download(url: str, save_dir: str, timeout: int = 30) -> Optional[str]:
    """
    用 curl 直接下载文件，自动从 Content-Disposition 获取原始文件名。
    返回下载文件的完整路径，失败返回 None。
    """
    # 使用唯一临时文件名，避免并发冲突
    temp_path, headers_path = get_unique_temp_path(save_dir, "curl")

    cmd = [
        "curl", "-s", "-L",
        "-o", temp_path,
        "-D", headers_path,
        "-w", "%{http_code}",
        "--max-time", str(timeout),
    ]
    for k, v in HEADERS.items():
        cmd += ["-H", f"{k}: {v}"]

    cmd.append(url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        http_code = result.stdout.strip() if result.stdout else ""

        if http_code != "200" or not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(headers_path):
                os.remove(headers_path)
            return None

        # 从响应头中提取原始文件名
        filename = None
        if os.path.exists(headers_path):
            with open(headers_path, "r", encoding="utf-8", errors="ignore") as f:
                headers_content = f.read()
                # 解析 Content-Disposition
                for line in headers_content.split("\n"):
                    if "Content-Disposition" in line:
                        # 提取 filename*= 或 filename=
                        import re
                        # 优先尝试 filename*= (RFC 5987)
                        match = re.search(r'filename\*=\s*UTF-8\'\'([^\s;]+)', line)
                        if match:
                            filename = match.group(1)
                        else:
                            # 尝试 filename=
                            match = re.search(r'filename=\s*"?([^"\s;]+)"?', line)
                            if match:
                                filename = match.group(1)
                        if filename:
                            break

            os.remove(headers_path)

        # 如果没有获取到文件名，从 URL 提取
        if not filename:
            parsed = urlparse(url)
            path_part = parsed.path.split("/")[-1]
            filename = path_part if path_part and "." in path_part else "invoice.pdf"

        # 重命名临时文件为最终文件名
        final_path = os.path.join(save_dir, filename)
        if final_path != temp_path:
            # 如果目标文件已存在，先删除
            if os.path.exists(final_path):
                os.remove(final_path)
            os.rename(temp_path, final_path)
        else:
            final_path = temp_path

        return final_path

    except Exception as e:
        print(f"[curl] 下载失败: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(headers_path):
            os.remove(headers_path)
        return None


def is_pdf_file(path: str) -> bool:
    """判断文件是否为有效 PDF"""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False
    with open(path, "rb") as f:
        return f.read(4) == b"%PDF"


def is_attachment_file(path: str) -> bool:
    """判断文件是否为附件（不是HTML页面）"""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return False

    # 读取文件开头部分判断是否为HTML
    try:
        with open(path, "rb") as f:
            # 读取前512字节足够判断
            header = f.read(512)

            # 检查是否为HTML文件（常见HTML开头标识）
            html_signatures = [
                b"<!DOCTYPE",
                b"<html",
                b"<HTML",
                b"<!doctype",
                b"<head",
                b"<HEAD",
                b"<body",
                b"<BODY",
            ]

            # 如果文件以HTML标签开头，说明是HTML页面而不是附件
            for sig in html_signatures:
                if sig in header:
                    return False

            return True
    except Exception:
        return False


# ─────────────────────────────────────────────
# Playwright 下载核心
# ─────────────────────────────────────────────

# 全局 Playwright 浏览器实例锁
PLAYWRIGHT_LOCK_PATH = "/tmp/.playwright_chrome.lock"

# Chrome 默认下载目录（当通过 CDP 连接时，Chrome 会下载到这里）
CHROME_DEFAULT_DOWNLOAD_DIR = "/tmp/chrome-data/Default/Downloads"


def playwright_download(url: str, save_dir: str, filename_hint: str = None) -> Optional[str]:
    """
    用 Playwright 访问页面，拦截/捕获 PDF 下载，返回已保存文件路径。

    策略：
      1. 设置浏览器下载目录为 save_dir
      2. 访问 URL，等待页面加载
      3. 拦截 download 事件（页面自动触发下载）
      4. 若未拦截到，查找并点击下载按钮，同时监控 save_dir 目录等待新 PDF 文件
      5. 验证文件

    注意：使用文件锁防止多个进程同时操作同一个 Chrome 实例
    """
    if not PLAYWRIGHT_AVAILABLE:
        print("[Playwright] 未安装，跳过")
        return None

    os.makedirs(save_dir, exist_ok=True)

    if not filename_hint:
        parsed = urlparse(url)
        path_part = parsed.path.split("/")[-1]
        filename_hint = path_part if path_part and "." in path_part else "invoice.pdf"

    save_path = os.path.join(save_dir, filename_hint)
    downloaded_path: Optional[str] = None

    before_files: set[str] = set(os.listdir(save_dir)) if os.path.exists(save_dir) else set()

    # 使用文件锁防止并发访问 Chrome CDP
    with FileLock(PLAYWRIGHT_LOCK_PATH):
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")

                context = browser.new_context(
                    accept_downloads=True,
                    extra_http_headers={k: v for k, v in HEADERS.items() if k != "Referer"},
                    viewport=None
                )
                page = context.new_page()

                try:
                    print(f"[Playwright] 访问: {url[:80]}")
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(3)

                    # 策略1: 检查页面是否自动触发了下载
                    if downloaded_path and is_attachment_file(downloaded_path):
                        browser.close()
                        return downloaded_path

                    # 策略2: 点击下载按钮并等待下载
                    # 百望发票特殊处理：使用 expect_download 等待下载事件
                    if page.url.startswith("https://pis.baiwang.com/"):
                        btn = page.query_selector("div.btn-web")
                        if btn:
                            print("[下载按钮] 找到百望 div.btn-web，点击并等待下载")
                            with page.expect_download(timeout=15000) as download_info:
                                btn.click()
                            download = download_info.value
                            suggested = download.suggested_filename or filename_hint
                            target = os.path.join(save_dir, suggested)
                            download.save_as(target)
                            downloaded_path = target
                            print(f"  [Playwright 拦截下载] -> {target}")
                    else:
                        # 通用下载按钮点击
                        if try_click_download_button(page):
                            deadline = time.time() + 15
                            while time.time() < deadline:
                                if downloaded_path and is_attachment_file(downloaded_path):
                                    break
                                current_files = set(os.listdir(save_dir)) if os.path.exists(save_dir) else set()
                                new_files = current_files - before_files
                                for f in new_files:
                                    fp = os.path.join(save_dir, f)
                                    if is_attachment_file(fp) and fp != save_path:
                                        downloaded_path = fp
                                        print(f"  [文件系统监控] 检测到新附件: {fp}")
                                        break
                                time.sleep(0.5)

                    # 策略3: 尝试拦截附件网络响应
                    if not (downloaded_path and is_attachment_file(downloaded_path)):
                        pdf_bytes = intercept_pdf_response(page, timeout=10)
                        if pdf_bytes:
                            with open(save_path, "wb") as f:
                                f.write(pdf_bytes)
                            if is_attachment_file(save_path):
                                downloaded_path = save_path
                                print(f"  [网络拦截] 保存附件: {save_path}")

                except Exception as e:
                    print(f"[Playwright] 页面访问失败: {e}")

                browser.close()

        except Exception as e:
            print(f"[Playwright] 浏览器连接失败: {e}")
            return None

    if downloaded_path and is_attachment_file(downloaded_path):
        return downloaded_path
    if os.path.exists(save_path) and is_attachment_file(save_path):
        return save_path
    return None


def intercept_pdf_response(page, timeout: float = 10.0) -> Optional[bytes]:
    """拦截页面中加载的 PDF 响应内容"""
    pdf_data: Optional[bytes] = None

    def handle_response(response):
        nonlocal pdf_data
        ct = response.headers.get("content-type", "")
        if "pdf" in ct.lower() or response.url.endswith(".pdf"):
            try:
                body = response.body()
                if body[:4] == b"%PDF":
                    pdf_data = body
                    print(f"  [网络拦截] 捕获 PDF: {response.url[:60]}")
            except Exception:
                pass

    page.on("response", handle_response)
    deadline = time.time() + timeout
    while time.time() < deadline and not pdf_data:
        time.sleep(0.3)

    page.remove_listener("response", handle_response)
    return pdf_data


def try_click_download_button(page: "Page", timeout: float = 15.0) -> bool:
    """
    通用下载按钮点击策略。
    按优先级尝试：
      1. 如果 URL 是 https://pis.baiwang.com/ 开头，点击 class="btn-web" 的 div（百望发票）
      2. text 包含"下载"/"下载发票"/"下载PDF"的 <a> 或 <button>
      3. 任意指向 .pdf 的 <a href>
    """
    # 获取当前页面 URL
    current_url = page.url

    # 百望发票专用按钮 - 仅当 URL 是百望域名时才尝试
    if current_url.startswith("https://pis.baiwang.com/"):
        try:
            btn = page.query_selector("div.btn-web")
            if btn:
                print("[下载按钮] 找到百望 div.btn-web，点击")
                btn.click()
                return True
        except Exception:
            pass

    # 通用下载链接/按钮
    selectors = [
        "a:has-text('下载')",
        "a:has-text('下载发票')",
        "a:has-text('下载PDF')",
        "button:has-text('下载')",
        "a[href$='.pdf']",
        "a[href*='download']",
    ]
    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if el:
                href = el.get_attribute("href") or ""
                text = el.inner_text() or ""
                print(f"[下载按钮] 点击: {sel} -> {text[:20]} | href={href[:50]}")
                el.click()
                time.sleep(2)
                return True
        except Exception:
            continue

    return False


def find_pdf_link(page: "Page") -> Optional[str]:
    """从页面中查找 PDF 链接"""
    try:
        links = page.query_selector_all("a[href], area[href]")
        for link in links:
            href = link.get_attribute("href") or ""
            if ".pdf" in href.lower() and href.startswith("http"):
                print(f"[PDF链接] 找到: {href}")
                return href
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────
# 统一入口
# ─────────────────────────────────────────────

def download_file(
    url: str,
    save_dir: str,
    filename_hint: str = None,
    try_curl_first: bool = True,
) -> Optional[str]:
    """
    统一的文件下载入口，自动识别 URL 类型并调用对应的 handler。

    流程:
      1. 根据 URL pattern 识别类型，调用对应的专用 handler
      2. 如果没有匹配的 handler，使用通用流程：
         - curl 直接下载（最快）
         - curl 失败 → playwright_download（处理点击按钮等场景）

    Args:
        url: 下载 URL
        save_dir: 保存目录
        filename_hint: 文件名提示（可选）
        try_curl_first: 是否先尝试 curl（默认 True，专用 handler 会忽略此参数）

    Returns:
        下载成功返回文件绝对路径，失败返回 None
    """
    os.makedirs(save_dir, exist_ok=True)

    # 根据 URL pattern 识别并调用对应的 handler
    handler = resolve_handler_by_url(url)
    if handler:
        print(f"[download_file] 检测到专用 URL pattern，使用对应 handler")
        return handler(url, save_dir)

    # 通用下载流程
    # 策略1: curl 直接下载（自动获取原始文件名）
    if try_curl_first:
        print(f"[curl] 尝试直接下载: {url[:80]}")
        result = curl_download(url, save_dir)
        if result and is_attachment_file(result):
            print(f"[curl] 下载成功: {result} ({os.path.getsize(result)} bytes)")
            return result
        else:
            print(f"[curl] 文件不是有效附件，重新下载")

    # 策略2: Playwright 兜底
    if not filename_hint:
        parsed = urlparse(url)
        path_part = parsed.path.split("/")[-1]
        filename_hint = path_part if path_part and "." in path_part else "invoice.pdf"

    print(f"[Playwright] curl 失败，启用浏览器方案: {url[:80]}")
    result = playwright_download(url, save_dir, filename_hint)
    if result and is_attachment_file(result):
        return result

    print(f"[download_file] URL 下载失败: {url[:60]}")
    return None


# ─────────────────────────────────────────────
# 扩展 handler：百望发票
# ─────────────────────────────────────────────

def download_baiwang_invoice(page_url: str, save_dir: str) -> Optional[str]:
    """
    百望发票下载 handler。

    邮件正文预览 URL 格式:
      https://pis.baiwang.com/smkp-vue/previewInvoiceAllEle?param=...

    策略:
      1. Playwright 访问百望预览页
      2. 等待页面完全加载和按钮可点击
      3. 使用 expect_download 等待下载事件
      4. 点击 .btn-web 按钮
      5. 保存下载文件
      6. 若失败，截图返回（供 OCR 备选）

    注意：使用文件锁防止多个进程同时操作同一个 Chrome 实例
    """
    os.makedirs(save_dir, exist_ok=True)
    screenshot_path = os.path.join(save_dir, f'baiwang_invoice_{uuid.uuid4().hex[:8]}.png')

    if not PLAYWRIGHT_AVAILABLE:
        print("[baiwang] Playwright 不可用，跳过")
        return None

    # 使用文件锁防止并发访问 Chrome CDP
    with FileLock(PLAYWRIGHT_LOCK_PATH):
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
                context = browser.new_context(
                    accept_downloads=True,
                    ignore_https_errors=True,
                    viewport=None
                )
                page = context.new_page()

                print(f"[baiwang] 访问预览页: {page_url}")
                try:
                    # 策略1: 等待页面完全加载（包括网络请求）
                    page.goto(page_url, wait_until='networkidle', timeout=30000)
                    print("[baiwang] 页面加载完成，等待按钮出现")

                    # 策略2: 等待按钮可见和可点击
                    btn = page.wait_for_selector('.btn-web', state='visible', timeout=10000)
                    if btn:
                        print("[baiwang] 找到 .btn-web 按钮，准备点击")

                        # 策略3: 等待一小段时间确保页面稳定
                        time.sleep(1)

                        # 先启动文件系统监控（监控多个可能的下载目录）
                        print("[baiwang] 启动文件系统监控...")
                        before_files_save = set(os.listdir(save_dir)) if os.path.exists(save_dir) else set()
                        before_files_chrome = set(os.listdir(CHROME_DEFAULT_DOWNLOAD_DIR)) if os.path.exists(CHROME_DEFAULT_DOWNLOAD_DIR) else set()

                        # 策略4: 尝试同时使用 download 事件和文件监控
                        download_result = None
                        try:
                            with page.expect_download(timeout=30000) as download_info:
                                btn.click()
                                print("[baiwang] 已点击按钮，等待下载...")

                            download = download_info.value
                            suggested = download.suggested_filename or 'baiwang_invoice.pdf'
                            target = os.path.join(save_dir, suggested)
                            download.save_as(target)
                            print(f"[baiwang] Download 事件捕获成功: {target}")
                            download_result = target
                        except Exception as download_err:
                            print(f"[baiwang] Download 事件失败: {download_err}")

                            # 策略5: 如果 download 事件失败，检查多个下载目录
                            print("[baiwang] 检查文件系统是否有新文件...")
                            deadline = time.time() + 20
                            while time.time() < deadline:
                                # 检查 save_dir
                                if os.path.exists(save_dir):
                                    current_files = set(os.listdir(save_dir))
                                    new_files = current_files - before_files_save
                                    for f in new_files:
                                        fp = os.path.join(save_dir, f)
                                        if (is_attachment_file(fp) and
                                            not f.startswith('.') and
                                            not f.startswith('baiwang_invoice_')):
                                            print(f"[baiwang] save_dir 检测到新文件: {fp}")
                                            download_result = fp
                                            break

                                # 检查 Chrome 默认下载目录
                                if not download_result and os.path.exists(CHROME_DEFAULT_DOWNLOAD_DIR):
                                    current_files = set(os.listdir(CHROME_DEFAULT_DOWNLOAD_DIR))
                                    new_files = current_files - before_files_chrome
                                    for f in new_files:
                                        fp = os.path.join(CHROME_DEFAULT_DOWNLOAD_DIR, f)
                                        if is_attachment_file(fp):
                                            print(f"[baiwang] Chrome 默认目录检测到新文件: {fp}")
                                            # 将文件移动到 save_dir
                                            target = os.path.join(save_dir, f)
                                            shutil.move(fp, target)
                                            print(f"[baiwang] 已移动到: {target}")
                                            download_result = target
                                            break

                                if download_result:
                                    break
                                time.sleep(0.5)

                        if download_result and is_attachment_file(download_result):
                            print(f"[baiwang] 下载成功: {download_result}")
                            return download_result
                        else:
                            print("[baiwang] 未找到有效下载文件")
                    else:
                        print("[baiwang] 未找到 .btn-web 按钮")

                    # 下载失败，截图备用
                    try:
                        page.screenshot(path=screenshot_path, full_page=False, timeout=8000)
                        print(f"[baiwang] 截图已保存: {screenshot_path}")
                    except Exception as ss_err:
                        print(f"[baiwang] 截图失败: {ss_err}")

                    return screenshot_path if os.path.exists(screenshot_path) else None

                except Exception as e:
                    print(f"[baiwang] 页面访问失败: {e}")
                    return None
                finally:
                    browser.close()

        except Exception as e:
            print(f"[baiwang] 浏览器连接失败: {e}")
            return None


# ─────────────────────────────────────────────
# URL pattern 映射表（可扩展）
# ─────────────────────────────────────────────

URL_PATTERN_HANDLERS = [
    # (pattern, handler_function)
    # 添加新类型只需要在这里加一行映射，例如：
    # ("https://aa.com/", download_AA_invoice),
    ("https://pis.baiwang.com/", download_baiwang_invoice),
    ("https://greenpaper.baiwang.com/", download_baiwang_invoice),
]


def resolve_handler_by_url(url: str) -> Optional[callable]:
    """
    根据 URL pattern 返回对应的 handler 函数。
    """
    for pattern, handler_func in URL_PATTERN_HANDLERS:
        if url.startswith(pattern):
            return handler_func
    return None


# ─────────────────────────────────────────────
# 测试
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    save_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp/openclaw/uploads"
    os.makedirs(save_dir, exist_ok=True)

    # 测试通用 curl 下载
    test_url = "https://pis.baiwang.com/smkp-vue/previewInvoiceAllEle?param=B1F11C8790E4D6933F04A28D76E3969FE2E156CA378337A2A7D2957ECDF2B2804638C3709E991D2E4C5FCDDC54AAA3C17B6E91E6A04D467B29525F31C2403F80"
    # test_url = "https://jxtax.juneyaoair.com/gxhfw/download/invFile?invid=36249124609610000071&invDate=20260526&code=Gxj9t3c%3D&type=pdf"
    result = download_file(test_url, save_dir, "test.pdf")
    print(f"\n测试结果: {result}")
