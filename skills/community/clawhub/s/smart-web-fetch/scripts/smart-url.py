#!/usr/bin/env python3
"""
Smart Web Fetch - URL 预处理器
自动将 URL 转换为清洗服务地址，支持多级降级
"""

import sys
import urllib.parse
import urllib.request
import ssl

# 忽略 SSL 验证（某些服务需要）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def transform_url(original_url: str) -> str:
    """
    将原始 URL 转换为智能清洗 URL
    策略: Jina → markdown.new → defuddle.md
    """
    encoded_url = urllib.parse.quote(original_url, safe='')
    
    # 1. 首选: Jina Reader (免费，无需 API Key)
    jina_url = f"https://r.jina.ai/http://{original_url.replace('https://', '').replace('http://', '')}"
    if test_url(jina_url):
        return jina_url
    
    # 2. 降级: markdown.new
    markdown_new_url = f"https://markdown.new/{original_url}"
    if test_url(markdown_new_url):
        return markdown_new_url
    
    # 3. 最终降级: defuddle.md
    defuddle_url = f"https://defuddle.md/{original_url}"
    return defuddle_url


def test_url(url: str, timeout: int = 10) -> bool:
    """测试 URL 是否可用"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            },
            method='HEAD'
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.status == 200
    except Exception:
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: smart-url.py <url>", file=sys.stderr)
        sys.exit(1)
    
    original_url = sys.argv[1]
    transformed = transform_url(original_url)
    print(transformed)


if __name__ == "__main__":
    main()
