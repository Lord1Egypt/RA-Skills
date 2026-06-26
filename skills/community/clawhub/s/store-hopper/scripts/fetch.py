#!/usr/bin/env python3
"""
store-hopper: 网页内容抓取脚本
用法: python3 fetch.py <url> [--selector CSS选择器] [--max-length 5000]
输出: JSON 格式的网页提取内容

内容提取优先级(3级降级策略):
  1. Camoufox (最强反爬,可绕过知乎/小红书/Cloudflare等)
  2. 代理服务 (Jina/Markdown/Defuddle,通用性强)
  3. BeautifulSoup (基础抓取,快速)

依赖安装:
  pip install camoufox  # 推荐,最强反爬能力
  python3 -m camoufox fetch # 配合 camoufox 使用
  pip install requests beautifulsoup4 lxml  # 基础依赖
"""

import argparse
import json
import random
import re
import subprocess
import sys
import time
import requests


UA_POOL = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def summary(msg: str):
    """输出一行关键摘要到 stderr"""
    sys.stderr.write(f"[抓取] {msg}\n")
    sys.stderr.flush()


try:
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({"error": "请先安装 beautifulsoup4: pip install beautifulsoup4"}, ensure_ascii=False))
    sys.exit(1)


# 检查 camoufox 是否可用
CAMOUFOX_AVAILABLE = False
try:
    from camoufox.sync_api import Camoufox
    CAMOUFOX_AVAILABLE = True
except ImportError:
    pass


# 代理服务配置
PROXY_SERVICES = {
    "jina": {
        "url": "https://r.jina.ai/{url}",
        "desc": "Jina AI Reader - 最稳定，通用性强"
    },
    "markdown": {
        "url": "https://markdown.new/{url}",
        "desc": "Cloudflare Markdown - Cloudflare 保护网站专用"
    },
    "defuddle": {
        "url": "https://defuddle.md/{url}",
        "desc": "Defuddle - 备用方案"
    }
}


def get_random_headers() -> dict:
    """生成随机请求头"""
    return {
        "User-Agent": random.choice(UA_POOL),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }


def extract_with_camoufox(url: str, max_length: int = 8000) -> dict | None:
    """
    使用 Camoufox 反检测浏览器提取网页内容(最强反爬)
    可绕过知乎、小红书、Cloudflare等强反爬网站
    """
    if not CAMOUFOX_AVAILABLE:
        return None
    
    try:
        summary("使用 Camoufox 反检测浏览器...")
        
        with Camoufox(headless=True) as browser:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # 等待内容加载
            time.sleep(2)
            
            # 提取标题
            title = page.title()
            
            # 提取主内容(不移除元素,直接获取)
            content = page.evaluate("""
                () => {
                    const selectors = ['article', 'main', '.content', '.article', '.post'];
                    for (const sel of selectors) {
                        const elem = document.querySelector(sel);
                        if (elem && elem.innerText.length > 200) {
                            return elem.innerText;
                        }
                    }
                    return document.body.innerText;
                }
            """)
            
            if content and len(content.strip()) > 100:
                # 清理
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                clean_text = "\n".join(lines)
                
                if len(clean_text) > max_length:
                    clean_text = clean_text[:max_length] + "\n...[内容已截断]"
                
                return {
                    "url": url,
                    "title": title,
                    "content": clean_text,
                    "length": len(clean_text),
                    "extractor": "camoufox"
                }
    except Exception as e:
        import traceback
        summary(f"Camoufox错误: {str(e)}")
        traceback.print_exc()
    
    return None


def extract_with_proxy_services(url: str, max_length: int = 8000) -> dict | None:
    """
    使用代理服务获取网页内容(Jina/Markdown/Defuddle)
    这些服务可以绕过大部分反爬机制
    """
    errors = []
    
    for method in ["jina", "markdown", "defuddle"]:
        try:
            summary(f"尝试代理服务: {method}...")
            service_url = PROXY_SERVICES[method]["url"].format(url=url)
            
            result = subprocess.run(
                ["curl", "-s", "-L", service_url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout and len(result.stdout) > 100:
                content = result.stdout.strip()
                
                # 清理
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                clean_text = "\n".join(lines)
                
                if len(clean_text) > max_length:
                    clean_text = clean_text[:max_length] + "\n...[内容已截断]"
                
                # 尝试提取标题(第一行或前几行)
                title = ""
                for line in lines[:5]:
                    if len(line) > 5 and len(line) < 100:
                        title = line
                        break
                
                return {
                    "url": url,
                    "title": title,
                    "content": clean_text,
                    "length": len(clean_text),
                    "extractor": f"proxy:{method}"
                }
            else:
                errors.append(f"{method}: 内容为空或过短")
        except subprocess.TimeoutExpired:
            errors.append(f"{method}: 超时")
        except Exception as e:
            errors.append(f"{method}: {str(e)}")
    
    return None


def extract_with_beautifulsoup(url: str, selector: str = None, max_length: int = 8000) -> dict:
    """
    使用 BeautifulSoup 抓取网页(基础方案)
    带重试机制和随机UA
    """
    max_retries = 2
    last_error = None
    
    for attempt in range(max_retries):
        try:
            headers = get_random_headers()
            
            # 创建会话
            session = requests.Session()
            session.headers.update(headers)
            
            # 先访问建立cookies
            session.get(url, timeout=10, allow_redirects=True)
            time.sleep(0.5)
            
            # 正式请求
            resp = session.get(
                url,
                timeout=15,
                headers=headers,
                allow_redirects=True
            )
            resp.raise_for_status()
            
            soup = BeautifulSoup(resp.text, "lxml" if "lxml" in sys.modules else "html.parser")

            # 移除无用标签
            for tag in soup(["script", "style", "nav", "footer", "header", "iframe", "noscript"]):
                tag.decompose()

            # 提取标题
            title = soup.title.string.strip() if soup.title and soup.title.string else ""

            # 如果指定了 CSS 选择器
            if selector:
                elements = soup.select(selector)
                text = "\n".join(el.get_text(separator="\n", strip=True) for el in elements)
            else:
                # 尝试找主内容区域
                main = (soup.find("article") or soup.find("main") or
                       soup.find("div", class_=re.compile(r"(content|article|post|body|detail)", re.I)) or
                       soup.body or soup)
                text = main.get_text(separator="\n", strip=True)

            # 清理多余空行
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            clean_text = "\n".join(lines)

            # 截断
            if len(clean_text) > max_length:
                clean_text = clean_text[:max_length] + "\n...[内容已截断]"

            return {
                "url": url,
                "title": title,
                "content": clean_text,
                "length": len(clean_text),
                "extractor": "beautifulsoup"
            }
            
        except requests.RequestException as e:
            last_error = f"请求失败: {str(e)}"
            if attempt < max_retries - 1:
                time.sleep(1)
            continue
        except Exception as e:
            last_error = str(e)
            break
    
    return {"error": f"多次尝试失败: {last_error}", "url": url}


def fetch_and_parse(url: str, selector: str = None, max_length: int = 8000) -> dict:
    """
    抓取网页并提取主要文本内容
    3级降级策略:
    1. Camoufox (最强反爬)
    2. 代理服务 (Jina/Markdown/Defuddle)
    3. BeautifulSoup (基础抓取)
    """
    # 方式1: Camoufox (最强反爬)
    if not selector:
        result = extract_with_camoufox(url, max_length)
        if result:
            return result
    
    # 方式2: 代理服务
    result = extract_with_proxy_services(url, max_length)
    if result:
        return result
    
    # 方式3: BeautifulSoup
    summary("尝试直接抓取...")
    if selector:
        return extract_with_beautifulsoup(url, selector, max_length)
    else:
        return extract_with_beautifulsoup(url, None, max_length)


def main():
    parser = argparse.ArgumentParser(
        description="网页内容抓取 (3级降级策略: Camoufox > 代理服务 > BS4)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 fetch.py "https://example.com/article"
  python3 fetch.py "https://example.com/article" --max-length 5000
  python3 fetch.py "https://example.com/article" --selector ".content"

推荐安装:
  pip install camoufox  # 最强反爬(可选,但推荐!)
  python3 -m camoufox fetch # 配合 camoufox
  pip install requests beautifulsoup4 lxml  # 基础依赖
        """
    )
    parser.add_argument("url", help="目标网址")
    parser.add_argument("--selector", default=None, help="CSS 选择器(可选)")
    parser.add_argument("--max-length", type=int, default=8000, help="最大文本长度(默认8000)")
    args = parser.parse_args()

    # 检查依赖
    if not CAMOUFOX_AVAILABLE:
        sys.stderr.write("[提示] 未安装 camoufox,强反爬能力受限。安装: pip install camoufox\n")

    result = fetch_and_parse(args.url, args.selector, args.max_length)

    # 输出摘要到 stderr
    if result.get("error"):
        summary(f"失败 | {args.url[:60]}... | {result['error']}")
    else:
        title = result.get("title", "")[:40]
        length = result.get("length", 0)
        extractor = result.get("extractor", "?")
        summary(f"{title} | {length}字 | {extractor} | {args.url[:50]}...")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
