#!/usr/bin/env python3
"""
WeChat Article Fetcher Lite - 轻量级版本
针对低内存环境优化，使用 requests + BeautifulSoup
"""

import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class WeChatFetcherLite:
    """轻量级微信文章抓取器"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
    
    def fetch_single(self, url: str, output_path: Optional[str] = None,
                     download_images: bool = False,
                     output_format: str = "markdown") -> Dict:
        """抓取单篇文章"""
        
        print(f"[INFO] 开始抓取: {url}")
        
        try:
            # 请求页面
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            # 解析 HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取元数据
            title = self._extract_title(soup)
            author = self._extract_author(soup)
            publish_time = self._extract_publish_time(soup)
            content_html = self._extract_content(soup)
            images = self._extract_images(soup, url)
            
            # 下载图片
            if download_images and output_path:
                images = self._download_images(images, output_path)
            
            # 生成结果
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
            
        except Exception as e:
            print(f"[ERROR] 抓取失败: {e}")
            raise
    
    def _extract_title(self, soup) -> str:
        """提取标题"""
        # 尝试多种方式
        selectors = [
            'h2.rich_media_title',
            '#activity_name',
            '.rich_media_title',
            'h1',
            'title'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text().strip()
                if text and text != "微信":
                    return text
        
        return "未知标题"
    
    def _extract_author(self, soup) -> str:
        """提取作者"""
        selectors = [
            '#js_name',
            '.profile_nickname',
            '#profileBt a',
            'a#js_name'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        
        return "未知作者"
    
    def _extract_publish_time(self, soup) -> str:
        """提取发布时间"""
        selectors = [
            '#publish_time',
            '.rich_media_meta_text',
            'em#publish_time'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        
        return "未知时间"
    
    def _extract_content(self, soup) -> str:
        """提取正文"""
        selectors = [
            '#js_content',
            '#js_article',
            '.rich_media_content'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return str(elem)
        
        return ""
    
    def _extract_images(self, soup, base_url: str) -> List[Dict]:
        """提取图片"""
        images = []
        content = soup.select_one('#js_content') or soup
        
        for i, img in enumerate(content.find_all('img')):
            data_src = img.get('data-src')
            src = img.get('src')
            
            image_url = data_src or src
            if image_url:
                # 处理相对 URL
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url
                
                images.append({
                    "index": i + 1,
                    "url": image_url,
                    "alt": img.get('alt', '')
                })
        
        return images
    
    def _download_images(self, images: List[Dict], output_path: str) -> List[Dict]:
        """下载图片"""
        if not images:
            return images
        
        output_dir = Path(output_path).parent
        images_dir = output_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        for img in images:
            try:
                url = img["url"]
                ext = Path(urlparse(url).path).suffix or ".jpg"
                if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    ext = '.jpg'
                
                filename = f"image_{img['index']:03d}{ext}"
                local_path = images_dir / filename
                
                response = self.session.get(url, timeout=30)
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
        """保存输出"""
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
        """转换为 Markdown"""
        from html import unescape
        
        title = result["title"]
        author = result["author"]
        publish_time = result["publish_time"]
        url = result["url"]
        content_html = result["content_html"]
        images = result.get("images", [])
        fetch_time = result["fetch_time"]
        
        # 使用 BeautifulSoup 清理 HTML
        soup = BeautifulSoup(content_html, 'html.parser')
        
        # 提取纯文本
        text = soup.get_text(separator='\n', strip=True)
        
        # 清理多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        md = f"""# {title}

**公众号:** {author}
**发布时间:** {publish_time}
**原文链接:** {url}

---

{text}

"""
        
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
        """转换为 HTML"""
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
        soup = BeautifulSoup(result["content_html"], 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        
        return f"""标题: {result['title']}
公众号: {result['author']}
发布时间: {result['publish_time']}
原文链接: {result['url']}

{'=' * 50}

{text}

{'=' * 50}

抓取时间: {result['fetch_time']}
"""


def main():
    parser = argparse.ArgumentParser(description="微信文章抓取工具 Lite 版")
    parser.add_argument("url", nargs="?", help="微信文章 URL")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--batch", help="批量抓取文件（每行一个URL）")
    parser.add_argument("--download-images", action="store_true", help="下载图片")
    parser.add_argument("--format", choices=["markdown", "html", "json", "txt"],
                       default="markdown", help="输出格式")
    parser.add_argument("--timeout", type=int, default=30, help="超时时间（秒）")
    parser.add_argument("--delay", type=int, default=2, help="请求间隔（秒）")
    
    args = parser.parse_args()
    
    fetcher = WeChatFetcherLite(timeout=args.timeout)
    
    if args.batch:
        # 批量模式
        urls = Path(args.batch).read_text().strip().split("\n")
        urls = [u.strip() for u in urls if u.strip()]
        output_dir = args.output or "./wechat_articles"
        
        print(f"[INFO] 开始批量抓取，共 {len(urls)} 篇文章")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        for i, url in enumerate(urls, 1):
            print(f"\n[PROGRESS] {i}/{len(urls)}")
            safe_name = f"article_{i:03d}"
            file_path = output_path / f"{safe_name}.{args.format if args.format != 'markdown' else 'md'}"
            
            try:
                result = fetcher.fetch_single(
                    url, str(file_path),
                    download_images=args.download_images,
                    output_format=args.format
                )
                results.append({"url": url, "status": "success", "title": result.get("title", "")})
            except Exception as e:
                print(f"[ERROR] 抓取失败: {e}")
                results.append({"url": url, "status": "failed", "error": str(e)})
            
            # 添加延迟
            if i < len(urls):
                print(f"[INFO] 等待 {args.delay} 秒...")
                time.sleep(args.delay)
        
        # 保存报告
        report_path = output_path / "batch_report.json"
        report = {
            "total": len(urls),
            "success": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results
        }
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
        
        print(f"\n[SUCCESS] 批量抓取完成: {report['success']}/{report['total']}")
        print(f"[INFO] 报告已保存: {report_path}")
        
    elif args.url:
        # 单篇模式
        fetcher.fetch_single(
            args.url, args.output,
            download_images=args.download_images,
            output_format=args.format
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
