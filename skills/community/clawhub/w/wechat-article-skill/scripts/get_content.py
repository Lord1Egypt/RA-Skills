#!/usr/bin/env python3
"""
微信公众号文章正文提取脚本。

用途：根据 URL 抓取公众号页面 HTML，提取 #page-content 内的纯文本正文。
运行环境：本地 CLI，由 AI Agent 调用。
依赖：pip install -r requirements.txt（beautifulsoup4、certifi）

CLI 用法：python get_content.py --url <公众号文章链接>
输出：正文纯文本（stdout），供模型消费。
失败时：stderr 输出可操作建议，Agent 可据此决定是否改用 browser 工具。
"""
import argparse
import ssl
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import certifi
from bs4 import BeautifulSoup

# macOS 等环境默认证书链可能不完整，使用 certifi 的 CA 包
_SSL_CTX = ssl.create_default_context(cafile=certifi.where())

# 公众号服务器会校验 UA，必须使用真实浏览器 UA 否则 403
DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
)

MAX_RETRIES = 3
RETRY_DELAY = 1.5
TIMEOUT = 30


def extract_article_content(html: str) -> str | None:
    """
    从公众号页面 HTML 中提取正文。
    正文位于 #page-content 元素内。
    """
    if not html or not html.strip():
        return None
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.select_one("#page-content")
    if not content_div:
        return None
    return content_div.get_text(separator="\n", strip=True)


def fetch_html(url: str, user_agent: str = DEFAULT_UA) -> tuple[str, int | None]:
    """
    请求公众号链接，返回 (html, status_code)。
    status_code 为 None 表示非 HTTP 错误（如连接失败）。
    """
    req = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
        method="GET",
    )
    resp = urlopen(req, timeout=TIMEOUT, context=_SSL_CTX)
    html = resp.read().decode(resp.headers.get_content_charset() or "utf-8")
    return html, resp.status if hasattr(resp, "status") else 200


def main() -> int:
    parser = argparse.ArgumentParser(
        description="抓取微信公众号文章正文",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--url",
        required=True,
        help="公众号文章链接，如 https://mp.weixin.qq.com/s/xxx",
    )
    parser.add_argument(
        "--ua",
        default=DEFAULT_UA,
        help="User-Agent，默认使用 Chrome 138 桌面版",
    )
    args = parser.parse_args()

    for attempt in range(MAX_RETRIES):
        try:
            html, status = fetch_html(args.url, args.ua)
            if status == 403:
                print(
                    "请求被拒（403），公众号可能限制非浏览器请求。建议 Agent 改用 browser 工具。",
                    file=sys.stderr,
                )
                return 1
            content = extract_article_content(html)
            if content:
                print(content)
                return 0
            print(
                "未找到 #page-content 元素，可能页面结构变化或需登录。建议 Agent 改用 browser 工具。",
                file=sys.stderr,
            )
            return 1
        except HTTPError as e:
            if e.code == 403:
                print(
                    "请求被拒（403），公众号可能限制非浏览器请求。建议 Agent 改用 browser 工具。",
                    file=sys.stderr,
                )
                return 1
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            print(f"HTTP 错误 {e.code}: {e.reason}。可尝试 Agent 改用 browser 工具。", file=sys.stderr)
        except (URLError, OSError) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            print(f"请求失败（连接/超时）: {e}。可尝试 Agent 改用 browser 工具。", file=sys.stderr)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            print(f"未知错误: {e}。可尝试 Agent 改用 browser 工具。", file=sys.stderr)

    return 1


if __name__ == "__main__":
    sys.exit(main())
