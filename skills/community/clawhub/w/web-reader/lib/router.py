"""URL routing with platform detection."""
import shutil
from urllib.parse import urlparse

ROUTE_TABLE = {
    # WeChat
    "mp.weixin.qq.com": {"type": "article", "method": "scrapling", "selector": "#js_content", "post": "wx_images"},
    # Toutiao
    "www.toutiao.com": {"type": "article", "method": "scrapling", "selector": ".article-content", "post": "toutiao_images"},
    # Zhihu
    "zhuanlan.zhihu.com": {"type": "article", "method": "scrapling", "selector": ".Post-RichText", "post": "default_images"},
    "www.zhihu.com": {"type": "article", "method": "scrapling", "selector": ".RichContent", "post": "default_images"},
    # Xiaohongshu
    "www.xiaohongshu.com": {"type": "article", "method": "camoufox", "selector": ".note-content", "post": "default_images"},
    # Weibo
    "www.weibo.com": {"type": "article", "method": "camoufox", "selector": ".WB_text", "post": "default_images"},
    # Feishu (wildcard handled in route())
    "feishu.cn": {"type": "article", "method": "feishu", "selector": "[data-content-editable-root]", "post": "default_images"},
    # Video platforms
    "www.bilibili.com": {"type": "video", "method": "ytdlp"},
    "bilibili.com": {"type": "video", "method": "ytdlp"},
    "b23.tv": {"type": "video", "method": "ytdlp"},
    "www.youtube.com": {"type": "video", "method": "ytdlp"},
    "youtube.com": {"type": "video", "method": "ytdlp"},
    "youtu.be": {"type": "video", "method": "ytdlp"},
    "www.douyin.com": {"type": "video", "method": "ytdlp"},
    "douyin.com": {"type": "video", "method": "ytdlp"},
}

# Default for unknown URLs
_DEFAULT = {"type": "article", "method": "scrapling", "selector": None, "post": "default_images"}


def route(url):
    """Parse URL and return routing config dict."""
    parsed = urlparse(url)
    domain = parsed.hostname or ""

    # Exact match
    if domain in ROUTE_TABLE:
        return dict(ROUTE_TABLE[domain])

    # Subdomain matching (e.g., *.feishu.cn)
    for key, config in ROUTE_TABLE.items():
        if domain.endswith("." + key):
            return dict(config)

    return dict(_DEFAULT)


def check_dependency(name):
    """Check if a dependency is available, print install hint if not. Returns bool."""
    hints = {
        "scrapling": "pip install scrapling",
        "yt-dlp": "pip install yt-dlp",
        "camoufox": "pip install camoufox && python3 -m camoufox fetch",
        "html2text": "pip install html2text",
    }

    if name == "yt-dlp":
        if shutil.which("yt-dlp"):
            return True
        print(f"[!] yt-dlp not found. Install: {hints[name]}")
        return False

    try:
        __import__(name)
        return True
    except ImportError:
        hint = hints.get(name, f"pip install {name}")
        print(f"[!] {name} not found. Install: {hint}")
        return False
