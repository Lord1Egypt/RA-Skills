#!/usr/bin/env python3
"""
TinyScraper - 简单静态网站镜像爬虫
纯 Python3 标准库，无额外依赖
"""

import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
import html.parser
from collections import deque
from typing import Set, Dict, Optional, Tuple

# ============ 配置 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "conf")
CONF_FILE = os.path.join(CONF_DIR, ".tinyscraper.conf")

def load_config() -> Dict[str, str]:
    config = {
        "DELAY": "0.5",
        "MAX_DEPTH": "-1",
        "TIMEOUT": "30",
        "MIRRORS_DIR": "tmp/mirrors",
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    if os.path.exists(CONF_FILE):
        with open(CONF_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    val = val.strip().strip('"').strip("'")
                    config[key.strip()] = val
    return config

CONFIG = load_config()
DELAY = float(CONFIG["DELAY"])
MAX_DEPTH = int(CONFIG["MAX_DEPTH"])
TIMEOUT = int(CONFIG["TIMEOUT"])
WORKSPACE_DIR = os.environ.get(
    "OPENCLAW_WORKSPACE",
    os.path.expanduser("~/.openclaw/workspace")
)
MIRRORS_DIR = os.path.join(WORKSPACE_DIR, CONFIG["MIRRORS_DIR"])
USER_AGENT = CONFIG["USER_AGENT"]

# ============ 工具函数 ============

def log_info(msg: str):
    print(f"[INFO] {msg}")

def log_step(msg: str):
    print(f"[STEP] {msg}")

def log_warn(msg: str):
    print(f"[WARN] {msg}")

def log_error(msg: str):
    print(f"[ERROR] {msg}", file=sys.stderr)

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def url_to_filepath(base_dir: str, url: str) -> str:
    """
    将 URL 转换为本地文件路径
    e.g. /page?id=1 -> page/index.html
    """
    parsed = urllib.parse.urlparse(url)
    path = parsed.path if parsed.path else "/"

    # 去掉末尾斜杠
    path = path.rstrip("/")

    # 空路径或根路径转为 index
    if not path:
        path = "index.html"
    elif not os.path.splitext(path)[1]:
        # 无扩展名，加 /index.html
        path = path + "/index.html"
    # 清理路径中的 ..
    path = os.path.normpath(path)
    if path.startswith("/"):
        path = path[1:]

    return os.path.join(base_dir, path)

def make_relative_path(from_path: str, to_path: str) -> str:
    """从 from_path 到 to_path 的相对路径"""
    rel = os.path.relpath(to_path, os.path.dirname(from_path))
    # Windows 反斜杠转正斜杠
    return rel.replace("\\", "/")

# ============ HTML/CSS/JS 链接解析 ============

def _is_special_url(url: str) -> bool:
    """判断 URL 是否为特殊协议（应跳过处理）"""
    return url.startswith(("#", "javascript:", "mailto:", "tel:"))


class LinkExtractor(html.parser.HTMLParser):
    """从 HTML 中提取链接和资源"""

    def __init__(self):
        super().__init__()
        self.links: Set[str] = set()   # href 链接
        self.resources: Set[str] = set()  # src/link 等资源
        self.external_links: Set[str] = set()  # 外部链接

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        href = attrs_dict.get("href", "")
        src = attrs_dict.get("src", "")

        if href and not _is_special_url(href):
            if tag in ("a", "area"):
                self.links.add(href)
            else:
                self.resources.add(href)

        if src and not _is_special_url(src):
            self.resources.add(src)

    def handle_comment(self, data):
        # 从 HTML 注释中提取 src/href
        for match in re.finditer(r'(?:src|href)\s*=\s*["\x27]([^"\x27]+)["\x27]', data):
            url = match.group(1)
            if url and not url.startswith(("#", "javascript:", "mailto:", "tel:")):
                self.resources.add(url)

    def handle_style(self, data):
        # 提取 CSS 中的 url()
        urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', data)
        for u in urls:
            u = u.strip().strip('"\'')
            if u and not u.startswith("data:"):
                self.resources.add(u)

    def handle_startendtag(self, tag, attrs):
        # 处理自闭合标签如 <img ... />
        self.handle_starttag(tag, attrs)

class CSSParser:
    """解析 CSS 文件中的 url() 引用"""

    @staticmethod
    def extract_urls(css_content: str) -> Set[str]:
        urls = set()
        # url() 引用
        for match in re.finditer(r'url\(["\']?([^"\')]+)["\']?\)', css_content):
            url = match.group(1).strip().strip('"\'')
            if url and not url.startswith("data:"):
                urls.add(url)
        # @import
        for match in re.finditer(r'@import\s+["\']([^"\']+)["\']', css_content):
            urls.add(match.group(1))
        return urls

class JSParser:
    """解析 JS 中的 import/require/src 引用"""

    @staticmethod
    def extract_urls(js_content: str) -> Set[str]:
        urls = set()
        # import ... from '...'
        for match in re.finditer(r"import\s+.*?from\s+['\"]([^'\"]+)['\"]", js_content):
            urls.add(match.group(1))
        # import('...')
        for match in re.finditer(r"import\(['\"]([^'\"]+)['\"]\)", js_content):
            urls.add(match.group(1))
        # require('...')
        for match in re.finditer(r"require\(['\"]([^'\"]+)['\"]\)", js_content):
            urls.add(match.group(1))
        # src = '...'（仅限 JS 模块路径，不匹配 HTML 片段）
        # 限制只匹配被引号包裹的、以 .js 结尾或为相对路径的 src
        for match in re.finditer(r'src\s*=\s*["\']([^\"\']+)["\']', js_content):
            url = match.group(1)
            # 只接受相对路径或以 .js/.mjs 结尾的模块路径
            if url.endswith(('.js', '.mjs')) or (url.startswith('.') and '/' in url):
                urls.add(url)
        return urls

# ============ 链接重写 ============

def resolve_url(base_url: str, link: str) -> Optional[str]:
    """将相对链接转为绝对 URL"""
    if not link:
        return None
    try:
        abs_url = urllib.parse.urljoin(base_url, link)
        parsed = urllib.parse.urlparse(abs_url)
        # 只处理 http/https
        if parsed.scheme not in ("http", "https"):
            return None
        return abs_url
    except Exception:
        return None

def get_domain(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    # 去掉端口，只比较主机名
    return parsed.hostname or ""

def is_same_domain(base_url: str, target_url: str) -> bool:
    """判断是否同域名（忽略端口）"""
    return get_domain(base_url) == get_domain(target_url)

def normalize_url(url: str) -> str:
    """URL 去重规范化"""
    parsed = urllib.parse.urlparse(url)
    # 去掉 fragment
    return urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, parsed.path,
        parsed.params, parsed.query, ""
    ))

def guess_content_type(url: str, content: bytes) -> str:
    """根据 URL 或内容猜测 MIME 类型"""
    path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1].lower()

    mime_map = {
        ".html": "text/html",
        ".htm": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".xml": "application/xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".ttf": "font/ttf",
        ".eot": "application/vnd.ms-fontobject",
        ".pdf": "application/pdf",
        ".zip": "application/zip",
    }
    return mime_map.get(ext, "application/octet-stream")

# ============ 内容重写 ============

def rewrite_html_content(html_content: str, page_url: str, local_dir: str) -> str:
    """重写 HTML 中的链接为相对路径（使用 HTML 解析器而非正则）"""
    parser = LinkExtractor()
    try:
        parser.feed(html_content)
    except Exception:
        return html_content

    # 建立绝对 URL -> 本地相对路径 映射
    url_to_local: Dict[str, str] = {}
    for url in parser.links | parser.resources:
        abs_url = resolve_url(page_url, url)
        if not abs_url:
            continue
        # 外部链接不重写
        if not is_same_domain(page_url, abs_url):
            continue
        normalized = normalize_url(abs_url)
        local_path = url_to_filepath(local_dir, normalized)
        rel_path = make_relative_path(os.path.join(local_dir, "_dummy.html"), local_path)
        url_to_local[normalized] = rel_path

    # 使用 HTML 解析器直接重写属性
    class AttributeRewriter(html.parser.HTMLParser):
        def __init__(self, url_map):
            super().__init__()
            self.url_map = url_map
            self.output = []

        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            new_attrs = []
            for key, val in attrs:
                if key in ("href", "src") and val:
                    abs_url = resolve_url(page_url, val)
                    if abs_url and is_same_domain(page_url, abs_url):
                        normalized = normalize_url(abs_url)
                        if normalized in self.url_map:
                            val = self.url_map[normalized]
                new_attrs.append((key, val))
            start = "<" + tag
            if new_attrs:
                start += " " + " ".join(f'{k}="{v}"' for k, v in new_attrs if v is not None)
            # 自闭合标签
            if tag in ("img", "br", "hr", "input", "meta", "link"):
                self.output.append(start + " />")
            else:
                self.output.append(start + ">")

        def handle_endtag(self, tag):
            self.output.append(f"</{tag}>")

        def handle_data(self, data):
            self.output.append(data)

        def handle_comment(self, data):
            self.output.append(f"<!--{data}-->")

        def handle_decl(self, decl):
            self.output.append(f"<!{decl}>")

        def get_result(self):
            return "".join(self.output)

    rewriter = AttributeRewriter(url_to_local)
    try:
        rewriter.feed(html_content)
        return rewriter.get_result()
    except Exception:
        return html_content

def rewrite_css_content(css_content: str, page_url: str, css_path: str) -> str:
    """重写 CSS 中的 url() 为相对路径，css_path 是 CSS 文件的本地完整路径"""
    def replace_url(match):
        full = match.group(0)
        url = match.group(1).strip().strip('"\'')
        abs_url = resolve_url(page_url, url)
        if not abs_url or not is_same_domain(page_url, abs_url):
            return full
        normalized = normalize_url(abs_url)
        local_path = url_to_filepath(os.path.dirname(css_path), normalized)
        rel_path = make_relative_path(css_path, local_path)
        return f'url("{rel_path}")'

    # 重写 @import
    def replace_import(match):
        url = match.group(1).strip().strip('"\'')
        abs_url = resolve_url(page_url, url)
        if not abs_url or not is_same_domain(page_url, abs_url):
            return match.group(0)
        normalized = normalize_url(abs_url)
        local_path = url_to_filepath(os.path.dirname(css_path), normalized)
        rel_path = make_relative_path(css_path, local_path)
        return f'@import "{rel_path}"'

    result = re.sub(r'@import\s+["\']([^"\']+)["\']', replace_import, css_content)
    return re.sub(r'url\(["\']?([^)\'"]+)["\']?\)', replace_url, result)

# ============ 下载器 ============

class TinyCrawler:
    def __init__(self, start_url: str, dry_run: bool = False):
        self.start_url = normalize_url(start_url)
        self.domain = get_domain(self.start_url)
        self.base_dir = os.path.join(MIRRORS_DIR, self.domain)
        self.dry_run = dry_run

        self.visited: Set[str] = set()
        self.downloaded: Set[str] = set()
        self.pending: deque = deque()
        self.failed: list = []

        self.stats = {
            "pages": 0,
            "resources": 0,
            "failed": 0
        }

        ensure_dir(self.base_dir)

    def is_same_domain(self, url: str) -> bool:
        return is_same_domain(self.start_url, url)

    def should_follow(self, url: str) -> bool:
        normalized = normalize_url(url)
        if normalized in self.visited:
            return False
        if not self.is_same_domain(url):
            return False
        return True

    def enqueue(self, url: str, depth: int = 0):
        """加入待爬队列（页面）"""
        normalized = normalize_url(url)
        if not self.should_follow(normalized):
            return
        self.pending.append((normalized, depth, "page"))

    def enqueue_resource(self, url: str, depth: int = 0):
        """将资源加入待爬队列（统一走 crawl 循环）"""
        normalized = normalize_url(url)
        if normalized in self.downloaded:
            return
        self.pending.append((normalized, depth, "resource"))

    def download_url(self, url: str, timeout: int = TIMEOUT) -> tuple[Optional[bytes], Optional[str]]:
        """下载 URL，返回 (content_bytes, content_type) 或 (None, None)"""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                # 优先从响应头获取 Content-Type
                content_type = resp.headers.get("Content-Type", "")
                # 去掉 ";charset=..." 部分
                if ";" in content_type:
                    content_type = content_type.split(";")[0].strip()
                return body, content_type
        except Exception as e:
            log_warn(f"下载失败: {url} -> {e}")
            self.failed.append(url)
            self.stats["failed"] += 1
            return None, None

    def save_file(self, filepath: str, content: bytes, content_type: str = ""):
        """保存文件到本地"""
        ensure_dir(os.path.dirname(filepath))
        with open(filepath, "wb") as f:
            f.write(content)

    def handle_page(self, url: str, content: bytes, depth: int):
        """处理 HTML 页面"""
        self.stats["pages"] += 1

        # 解析并提取链接（dry-run 也需要解析来发现更多 URL）
        try:
            html_content = content.decode("utf-8", errors="replace")
        except UnicodeDecodeError:
            html_content = content.decode("latin-1", errors="replace")

        if self.dry_run:
            log_info(f"[DRY] PAGE: {url} (depth={depth})")
        else:
            # 重写 HTML 中的链接
            page_dir = url_to_filepath(self.base_dir, url)
            # 确保有 .html 扩展名
            if not page_dir.endswith(".html"):
                page_dir += ".html"
            rewritten = rewrite_html_content(html_content, url, os.path.dirname(page_dir))
            self.save_file(page_dir, rewritten.encode("utf-8"))
            log_info(f"保存页面: {url} -> {page_dir}")

        # 提取链接入队
        parser = LinkExtractor()
        try:
            parser.feed(html_content)
        except Exception:
            pass

        for link in parser.links:
            abs_url = resolve_url(url, link)
            if abs_url and self.is_same_domain(abs_url):
                if MAX_DEPTH == -1 or depth < MAX_DEPTH:
                    self.enqueue(abs_url, depth + 1)
                    if self.dry_run:
                        log_info(f"  [DRY] LINK: {abs_url}")

        for resource in parser.resources:
            abs_url = resolve_url(url, resource)
            if abs_url and self.is_same_domain(abs_url):
                self.enqueue_resource(abs_url, depth=depth+1)
                if self.dry_run:
                    log_info(f"  [DRY] RES: {abs_url}")

    def download_resource(self, url: str, referrer: str = "",
                          content: Optional[bytes] = None,
                          content_type: Optional[str] = None,
                          depth: int = 0):
        """下载单个资源文件，可选传入已下载的内容和类型"""
        normalized = normalize_url(url)

        # 跳过已处理过的资源（防止 enqueue 后重复下载）
        # 但 dry_run 模式下每次都需要处理（不入 downloaded）
        if not self.dry_run and normalized in self.downloaded:
            return

        # 如果没有传入 content，则重新下载
        if content is None:
            content, http_ct = self.download_url(url)
            if content is None:
                return
            if http_ct:
                content_type = http_ct

        if self.dry_run:
            log_info(f"[DRY] RES: {url}")

        self.stats["resources"] += 1

        # 确定 MIME 类型
        if not content_type:
            content_type = guess_content_type(url, content)
        local_path = url_to_filepath(self.base_dir, url)

        # CSS 需要重写
        if content_type == "text/css":
            css_dir = os.path.dirname(local_path)
            css_text = content.decode("utf-8", errors="replace")
            rewritten = rewrite_css_content(css_text, url, local_path)
            if not self.dry_run:
                self.save_file(local_path, rewritten.encode("utf-8"), content_type)
            else:
                log_info(f"  [DRY] (CSS 规则已重写但未保存)")
            # 提取 CSS 里的资源并下载
            for css_url in CSSParser.extract_urls(css_text):
                abs_url = resolve_url(url, css_url)
                if abs_url and self.is_same_domain(abs_url):
                    if self.dry_run:
                        self.enqueue_resource(abs_url)
                        log_info(f"  [DRY] CSS RES: {abs_url}")
                    else:
                        self.download_resource(abs_url, referrer=url, depth=depth+1)
        else:
            if not self.dry_run:
                self.save_file(local_path, content, content_type)

        if not self.dry_run:
            log_info(f"保存资源: {url} -> {local_path}")
            self.downloaded.add(normalized)  # 保存后标记，防止重复下载

        # 如果是 HTML 或 JS，递归解析其中的链接
        # (CSS 已在上方处理，下载其引用的资源)
        if content_type in ("text/html", "application/javascript"):
            try:
                text = content.decode("utf-8", errors="replace")
            except (UnicodeDecodeError, AttributeError, TypeError):
                try:
                    text = content.decode("latin-1", errors="replace")
                except Exception:
                    return

            if content_type == "text/html":
                parser = LinkExtractor()
                parser.feed(text)
                for link in parser.links:
                    abs_url = resolve_url(url, link)
                    if abs_url and self.is_same_domain(abs_url):
                        if MAX_DEPTH == -1 or depth < MAX_DEPTH:
                            self.enqueue(abs_url, depth + 1)
            else:
                # JS
                for imp_url in JSParser.extract_urls(text):
                    abs_url = resolve_url(url, imp_url)
                    if abs_url and self.is_same_domain(abs_url):
                        self.download_resource(abs_url, url, depth=depth+1)

    def crawl(self):
        """主循环 - 广度优先"""
        log_step(f"🌐 开始镜像: {self.start_url}")
        log_step(f"📁 保存目录: {self.base_dir}")
        if self.dry_run:
            log_warn("🔍 DRY RUN 模式 - 不实际下载")

        self.enqueue(self.start_url, 0)

        while self.pending:
            item = self.pending.popleft()
            if len(item) == 2:
                url, depth = item
                kind = "page"
            else:
                url, depth, kind = item

            if url in self.visited:
                continue
            self.visited.add(url)

            if MAX_DEPTH != -1 and depth > MAX_DEPTH:
                log_info(f"跳过（超过深度限制）: {url}")
                continue

            log_step(f"爬取 ({depth}): {url}")

            content, http_ct = self.download_url(url)
            if content is None:
                continue

            # 优先用 HTTP 响应头的 Content-Type，其次用 URL 扩展名猜测
            if http_ct and http_ct.startswith("text/html"):
                content_type = "text/html"
            elif http_ct and http_ct.startswith("text/"):
                content_type = http_ct
            else:
                content_type = guess_content_type(url, content)

            if kind == "resource" or content_type != "text/html":
                self.download_resource(url, content=content, content_type=content_type, depth=depth)
            else:
                self.handle_page(url, content, depth)

            # 请求延迟
            if not self.dry_run:
                time.sleep(DELAY)

            # 进度报告
            log_info(f"进度: 已爬 {self.stats['pages']} 页面, {self.stats['resources']} 资源, {len(self.pending)} 待爬")

        log_info("=" * 50)
        log_info("镜像完成!")
        log_info(f"  页面: {self.stats['pages']}")
        log_info(f"  资源: {self.stats['resources']}")
        log_info(f"  失败: {self.stats['failed']}")
        log_info(f"  目录: {self.base_dir}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TinyScraper - 静态网站镜像工具")
    parser.add_argument("url", nargs="?", help="目标 URL")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不下载")
    parser.add_argument("-d", "--disconnect", action="store_true", help="清理镜像")
    parser.add_argument("--domain", help="指定域名（与 -d 配合）")
    args = parser.parse_args()

    if args.disconnect:
        domain = args.domain or input("输入要清理的域名: ").strip()
        target = os.path.join(MIRRORS_DIR, domain)
        if os.path.exists(target):
            import shutil
            shutil.rmtree(target)
            log_info(f"已清理: {target}")
        else:
            log_warn(f"目录不存在: {target}")
    elif args.url:
        crawler = TinyCrawler(args.url, dry_run=args.dry_run)
        crawler.crawl()
    else:
        parser.print_help()
