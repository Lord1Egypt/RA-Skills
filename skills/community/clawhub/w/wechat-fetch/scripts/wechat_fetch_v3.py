#!/usr/bin/env python3
"""
WeChat Article Fetcher v3.0
优化版本：添加免登录模式、批量抓取、图片下载、多格式输出
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse, unquote

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class WeChatFetcher:
    """微信公众号文章抓取器"""
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        self.headless = headless
        self.timeout = timeout
        self.user_data_dir = Path.home() / ".openclaw" / "browser" / "wechat-fetch-v3"
        
    def fetch_single(self, url: str, output_path: Optional[str] = None, 
                     no_login: bool = False, download_images: bool = False,
                     output_format: str = "markdown") -> Dict:
        """抓取单篇文章"""
        
        print(f"[INFO] 开始抓取: {url}")
        print(f"[INFO] 模式: {'免登录' if no_login else 'Cookie模式'}")
        
        with sync_playwright() as p:
            # 根据模式选择浏览器上下文
            if no_login:
                # 免登录模式：使用轻量级配置
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=[
                        '--disable-dev-shm-usage',
                        '--disable-setuid-sandbox',
                        '--no-sandbox',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features=IsolateOrigins,site-per-process',
                    ]
                )
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 720}
                )
            else:
                # Cookie模式：使用持久化上下文
                self.user_data_dir.mkdir(parents=True, exist_ok=True)
                context = p.chromium.launch_persistent_context(
                    str(self.user_data_dir),
                    headless=self.headless,
                    args=[
                        '--disable-dev-shm-usage',
                        '--disable-setuid-sandbox',
                        '--no-sandbox',
                    ]
                )
                browser = None
            
            page = context.new_page()
            
            try:
                # 访问页面（带重试）
                print(f"[INFO] 正在加载页面...")
                max_nav_retries = 2
                for nav_attempt in range(max_nav_retries):
                    try:
                        page.goto(url, wait_until="domcontentloaded", timeout=30000)
                        break
                    except Exception as nav_error:
                        if nav_attempt < max_nav_retries - 1:
                            print(f"[WARN] 页面加载失败，重试 {nav_attempt + 2}/{max_nav_retries}...")
                            time.sleep(2)
                        else:
                            raise nav_error
                
                # 简单等待，让页面渲染
                print(f"[INFO] 等待页面渲染...")
                page.wait_for_timeout(5000)
                
                # 尝试找到内容元素（不强制等待）
                content_selectors = ["#js_content", "#js_article", ".rich_media_content"]
                content_found = False
                for selector in content_selectors:
                    try:
                        if page.query_selector(selector):
                            content_found = True
                            print(f"[INFO] 找到内容元素: {selector}")
                            break
                    except:
                        continue
                
                if not content_found:
                    print(f"[WARN] 未找到标准内容元素，尝试继续...")
                
                # 等待一下确保 JS 渲染完成
                page.wait_for_timeout(3000)
                
                # 提取元数据
                title = self._extract_title(page)
                author = self._extract_author(page)
                publish_time = self._extract_publish_time(page)
                content_html = self._extract_content(page)
                images = self._extract_images(page)
                
                # 下载图片
                if download_images:
                    images = self._download_images(images, output_path)
                
                # 生成输出
                result = {
                    "title": title,
                    "author": author,
                    "publish_time": publish_time,
                    "url": url,
                    "content_html": content_html,
                    "images": images,
                    "fetch_time": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # 保存文件
                if output_path:
                    self._save_output(result, output_path, output_format, download_images)
                
                print(f"[SUCCESS] 抓取完成: {title}")
                return result
                
            except PlaywrightTimeout:
                print(f"[ERROR] 页面加载超时")
                raise
            except Exception as e:
                print(f"[ERROR] 抓取失败: {e}")
                raise
            finally:
                page.close()
                if browser:
                    browser.close()
                else:
                    context.close()
    
    def fetch_batch(self, urls: List[str], output_dir: str, 
                    no_login: bool = False, download_images: bool = False,
                    output_format: str = "markdown", max_retries: int = 3,
                    retry_delay: int = 5) -> List[Dict]:
        """批量抓取文章（带重试机制）"""
        
        print(f"[INFO] 开始批量抓取，共 {len(urls)} 篇文章")
        print(f"[INFO] 重试配置: 最多 {max_retries} 次，间隔 {retry_delay} 秒")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"\n[PROGRESS] {i}/{len(urls)}")
            
            # 生成输出文件名
            safe_title = f"article_{i:03d}"
            output_path = output_dir / f"{safe_title}.{self._get_extension(output_format)}"
            
            # 重试机制
            success = False
            last_error = None
            
            for attempt in range(1, max_retries + 1):
                if attempt > 1:
                    print(f"[RETRY] 第 {attempt}/{max_retries} 次尝试...")
                    time.sleep(retry_delay * (attempt - 1))  # 递增延迟
                
                try:
                    result = self.fetch_single(
                        url, str(output_path), no_login, download_images, output_format
                    )
                    results.append(result)
                    success = True
                    break
                    
                except Exception as e:
                    last_error = str(e)
                    print(f"[WARN] 尝试 {attempt} 失败: {e}")
                    
                    # 如果是最后尝试，记录失败
                    if attempt == max_retries:
                        print(f"[ERROR] 第 {i} 篇抓取失败（已重试 {max_retries} 次）")
                        results.append({
                            "url": url, 
                            "error": last_error,
                            "retries": max_retries,
                            "index": i
                        })
            
            # 添加延迟，避免触发反爬
            if i < len(urls) and success:
                delay = 2 + (i % 3)  # 2-4 秒随机延迟
                print(f"[INFO] 等待 {delay} 秒...")
                time.sleep(delay)
        
        # 生成批量抓取报告
        self._save_batch_report(results, output_dir)
        
        success_count = len([r for r in results if 'error' not in r])
        fail_count = len(urls) - success_count
        
        print(f"\n[SUCCESS] 批量抓取完成")
        print(f"  - 成功: {success_count}/{len(urls)}")
        print(f"  - 失败: {fail_count}/{len(urls)}")
        
        return results
    
    def _extract_title(self, page) -> str:
        """提取文章标题"""
        # 尝试多种选择器
        selectors = [
            "#activity_name",
            "h2.rich_media_title",
            ".rich_media_title",
            "#js_title",
            "title"
        ]
        
        for selector in selectors:
            try:
                elem = page.query_selector(selector)
                if elem:
                    text = elem.inner_text().strip()
                    if text and text != "未知标题":
                        return text
            except:
                continue
        
        # 从页面标题中提取
        try:
            page_title = page.title()
            if page_title and "-" in page_title:
                return page_title.split("-")[0].strip()
        except:
            pass
        
        return "未知标题"
    
    def _extract_author(self, page) -> str:
        """提取作者/公众号"""
        try:
            author_elem = page.query_selector("#js_name")
            if author_elem:
                return author_elem.inner_text().strip()
        except:
            pass
        
        try:
            author_elem = page.query_selector("a#js_name")
            if author_elem:
                return author_elem.inner_text().strip()
        except:
            pass
        
        return "未知作者"
    
    def _extract_publish_time(self, page) -> str:
        """提取发布时间"""
        try:
            time_elem = page.query_selector("#publish_time")
            if time_elem:
                return time_elem.inner_text().strip()
        except:
            pass
        
        return "未知时间"
    
    def _extract_content(self, page) -> str:
        """提取正文内容"""
        try:
            content_elem = page.query_selector("#js_content")
            if content_elem:
                return content_elem.inner_html()
        except:
            pass
        
        return ""
    
    def _extract_images(self, page) -> List[Dict]:
        """提取图片"""
        images = []
        
        try:
            img_elements = page.query_selector_all("#js_content img")
            for i, img in enumerate(img_elements):
                # 尝试获取真实图片URL
                data_src = img.get_attribute("data-src")
                src = img.get_attribute("src")
                
                image_url = data_src or src
                if image_url:
                    images.append({
                        "index": i + 1,
                        "url": image_url,
                        "alt": img.get_attribute("alt") or ""
                    })
        except Exception as e:
            print(f"[WARN] 图片提取失败: {e}")
        
        return images
    
    def _download_images(self, images: List[Dict], output_path: Optional[str]) -> List[Dict]:
        """下载图片到本地"""
        if not output_path:
            return images
        
        import requests
        
        output_dir = Path(output_path).parent
        images_dir = output_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        for img in images:
            try:
                url = img["url"]
                if url.startswith("//"):
                    url = "https:" + url
                
                ext = Path(urlparse(url).path).suffix or ".jpg"
                filename = f"image_{img['index']:03d}{ext}"
                local_path = images_dir / filename
                
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(local_path, "wb") as f:
                        f.write(response.content)
                    img["local_path"] = str(local_path.relative_to(output_dir))
                    print(f"[INFO] 图片下载成功: {filename}")
                else:
                    print(f"[WARN] 图片下载失败: {url}")
                    
            except Exception as e:
                print(f"[WARN] 图片下载异常: {e}")
        
        return images
    
    def _save_output(self, result: Dict, output_path: str, 
                     output_format: str, download_images: bool):
        """保存输出文件"""
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if output_format == "markdown":
            content = self._to_markdown(result, download_images)
            output_path.write_text(content, encoding="utf-8")
            
        elif output_format == "html":
            content = self._to_html(result)
            output_path.write_text(content, encoding="utf-8")
            
        elif output_format == "json":
            output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), 
                                   encoding="utf-8")
            
        elif output_format == "txt":
            content = self._to_txt(result)
            output_path.write_text(content, encoding="utf-8")
        
        print(f"[INFO] 文件已保存: {output_path}")
    
    def _to_markdown(self, result: Dict, download_images: bool) -> str:
        """转换为 Markdown - 增强版"""
        from html import unescape
        from html.parser import HTMLParser
        
        title = result["title"]
        author = result["author"]
        publish_time = result["publish_time"]
        url = result["url"]
        content_html = result["content_html"]
        images = result.get("images", [])
        fetch_time = result["fetch_time"]
        
        # 增强版 HTML 转 Markdown
        content = content_html
        
        # 移除微信特定的样式标签
        content = re.sub(r'<span[^>]*style="[^"]*visibility:\s*visible[^"]*"[^>]*>', '', content)
        content = re.sub(r'</span>', '', content)
        content = re.sub(r'<section[^>]*>', '', content)
        content = re.sub(r'</section>', '', content)
        
        # 转换标题
        content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', content, flags=re.DOTALL)
        content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', content, flags=re.DOTALL)
        content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', content, flags=re.DOTALL)
        content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n\n', content, flags=re.DOTALL)
        
        # 转换段落和换行
        content = re.sub(r'<br\s*/?>', '\n', content)
        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
        
        # 转换强调
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
        content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
        content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
        content = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', content, flags=re.DOTALL)
        
        # 转换列表
        content = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', content, flags=re.DOTALL)
        
        # 转换引用
        content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1\n\n', content, flags=re.DOTALL)
        
        # 转换代码
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL)
        content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```\n\n', content, flags=re.DOTALL)
        
        # 转换链接
        content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
        
        # 移除图片标签（单独处理）
        content = re.sub(r'<img[^>]*>', '', content)
        
        # 移除 figure 和 figcaption
        content = re.sub(r'<figure[^>]*>(.*?)</figure>', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'<figcaption[^>]*>(.*?)</figcaption>', r'*\1*\n', content, flags=re.DOTALL)
        
        # 移除剩余 HTML 标签
        content = re.sub(r'<[^>]+>', '', content)
        
        # HTML 实体解码
        content = unescape(content)
        
        # 清理多余空白
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()
        
        md = f"""# {title}

**公众号:** {author}
**发布时间:** {publish_time}
**原文链接:** {url}

---

{content}

"""
        
        # 添加图片
        if images:
            md += "## 图片列表\n\n"
            for img in images:
                if download_images and "local_path" in img:
                    md += f"![{img['alt']}]({img['local_path']})\n\n"
                else:
                    md += f"![{img['alt']}]({img['url']})\n\n"
        
        md += f"\n---\n\n*抓取时间: {fetch_time}*\n"
        
        return md
    
    def _to_html(self, result: Dict) -> str:
        """转换为完整 HTML"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{result['title']}</title>
</head>
<body>
    <h1>{result['title']}</h1>
    <p><strong>公众号:</strong> {result['author']}</p>
    <p><strong>发布时间:</strong> {result['publish_time']}</p>
    <p><strong>原文链接:</strong> <a href="{result['url']}">{result['url']}</a></p>
    <hr>
    {result['content_html']}
    <hr>
    <p><em>抓取时间: {result['fetch_time']}</em></p>
</body>
</html>"""
    
    def _to_txt(self, result: Dict) -> str:
        """转换为纯文本"""
        content = result["content_html"]
        content = re.sub(r'<[^>]+>', '', content)
        
        return f"""标题: {result['title']}
公众号: {result['author']}
发布时间: {result['publish_time']}
原文链接: {result['url']}

{'=' * 50}

{content}

{'=' * 50}

抓取时间: {result['fetch_time']}
"""
    
    def _get_extension(self, output_format: str) -> str:
        """获取文件扩展名"""
        extensions = {
            "markdown": "md",
            "html": "html",
            "json": "json",
            "txt": "txt"
        }
        return extensions.get(output_format, "md")
    
    def _save_batch_report(self, results: List[Dict], output_dir: Path):
        """保存批量抓取报告"""
        report_path = output_dir / "batch_report.json"
        
        summary = {
            "total": len(results),
            "success": len([r for r in results if "error" not in r]),
            "failed": len([r for r in results if "error" in r]),
            "results": results
        }
        
        report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        print(f"[INFO] 批量报告已保存: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="微信文章抓取工具 v3.0")
    parser.add_argument("url", nargs="?", help="微信文章 URL")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--batch", help="批量抓取文件（每行一个URL）")
    parser.add_argument("--no-login", action="store_true", 
                       help="免登录模式（可能不稳定）")
    parser.add_argument("--download-images", action="store_true",
                       help="下载图片到本地")
    parser.add_argument("--format", choices=["markdown", "html", "json", "txt"],
                       default="markdown", help="输出格式")
    parser.add_argument("--headless", action="store_true", default=True,
                       help="无头模式")
    parser.add_argument("--timeout", type=int, default=30,
                       help="超时时间（秒）")
    parser.add_argument("--max-retries", type=int, default=3,
                       help="最大重试次数（批量模式）")
    parser.add_argument("--retry-delay", type=int, default=5,
                       help="重试间隔（秒）")
    
    args = parser.parse_args()
    
    fetcher = WeChatFetcher(headless=args.headless, timeout=args.timeout)
    
    if args.batch:
        # 批量模式
        urls = Path(args.batch).read_text().strip().split("\n")
        urls = [u.strip() for u in urls if u.strip()]
        output_dir = args.output or "./wechat_articles"
        
        fetcher.fetch_batch(
            urls, output_dir, 
            no_login=args.no_login,
            download_images=args.download_images,
            output_format=args.format,
            max_retries=args.max_retries,
            retry_delay=args.retry_delay
        )
        
    elif args.url:
        # 单篇模式
        fetcher.fetch_single(
            args.url, args.output,
            no_login=args.no_login,
            download_images=args.download_images,
            output_format=args.format
        )
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
