#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章转 Markdown 工具
将微信文章抓取并转换为 Obsidian 兼容的 Markdown 格式
"""

import argparse
import os
import re
import sys
import hashlib
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 第三方库（需要安装）
try:
    import requests
    from readability import Document
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"错误：缺少依赖库 {e}")
    print("请运行：pip install requests readability-lxml beautifulsoup4")
    sys.exit(1)


class WeChatSaver:
    """微信文章保存器"""

    def __init__(self, output_dir="~/Documents/Obsidian Vault/00-Inbox"):
        self.output_dir = os.path.expanduser(output_dir)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "Version/17.0 Safari/605.1.15"
        })
        self.images_dir = None

    def fetch_article(self, url):
        """抓取文章 HTML"""
        print(f"📥 正在抓取：{url}")
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.text

    def extract_title(self, html):
        """提取文章标题（针对微信文章优化）"""
        soup = BeautifulSoup(html, 'lxml')
        title = None

        # 方法 1: #activity-name (微信文章专用)
        title_elem = soup.find(id='activity-name')
        if title_elem:
            title = title_elem.get_text(strip=True)

        # 方法 2: meta[property="og:title"]
        if not title:
            og_title = soup.find('meta', property='og:title')
            if og_title:
                title = og_title.get('content', '')

        # 方法 3: h1/h2 标签
        if not title:
            h1 = soup.find('h1') or soup.find('h2')
            if h1:
                title = h1.get_text(strip=True)

        # 方法 4: title 标签
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)

        # 方法 5: readability 兜底
        if not title or title == '[no-title]':
            try:
                doc = Document(html)
                title = doc.title()
            except:
                pass

        return title or '[no-title]'

    def extract_content(self, html):
        """提取文章正文（针对微信文章优化）"""
        title = self.extract_title(html)
        soup = BeautifulSoup(html, 'lxml')

        # 方法 1: 微信文章专用容器 id="js_content"
        content_container = soup.find(id='js_content')

        # 方法 2: class="rich_media_content"
        if not content_container:
            content_container = soup.find(class_='rich_media_content')

        # 方法 3: readability 兜底
        if not content_container:
            try:
                doc = Document(html)
                content_container = BeautifulSoup(doc.summary(), 'lxml')
            except:
                content_container = soup

        # 按顺序提取元素（段落、图片、标题等）
        elements = []  # 列表元素为 ('text', 文本) 或 ('img', src) 或 ('heading', 文本)

        def process_element(elem):
            """递归处理元素"""
            if not hasattr(elem, 'name') or elem.name is None:
                return

            # 段落
            if elem.name == 'p':
                text = elem.get_text(strip=True)
                # 检查段落内是否有图片
                img = elem.find('img')
                if img:
                    src = img.get('data-src') or img.get('data-original') or img.get('src')
                    if src and not src.startswith('data:'):
                        elements.append(('img', src))
                if text:
                    elements.append(('text', text))

            # 图片（独立）
            elif elem.name == 'img':
                src = elem.get('data-src') or elem.get('data-original') or elem.get('src')
                if src and not src.startswith('data:'):
                    elements.append(('img', src))

            # 标题（h1-h6）
            elif elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = elem.get_text(strip=True)
                if text:
                    level = min(int(elem.name[1]), 3)
                    elements.append(('heading', text, level))

            # 递归处理子元素
            else:
                for child in elem.children:
                    process_element(child)

        # 从内容容器开始处理
        process_element(content_container)

        # 如果没有找到元素，尝试直接提取文本
        if not elements:
            text = content_container.get_text(separator='\n', strip=True)
            if text:
                elements.append(('text', text))

        return title, elements

    def process_images(self, content_html, article_dir):
        """处理图片：下载并转换为本地引用"""
        images_dir = os.path.join(article_dir, "images")
        os.makedirs(images_dir, exist_ok=True)

        soup = BeautifulSoup(content_html, 'lxml')
        img_tags = soup.find_all('img')

        for i, img in enumerate(img_tags):
            src = img.get('data-src') or img.get('src')
            if not src or src.startswith('data:'):
                continue

            try:
                # 下载图片
                print(f"  🖼️  下载图片 {i+1}/{len(img_tags)}")
                img_resp = self.session.get(src, timeout=10)
                if img_resp.status_code == 200:
                    # 生成文件名
                    ext = self._get_image_ext(src)
                    filename = f"image_{i+1:03d}.{ext}"
                    filepath = os.path.join(images_dir, filename)

                    # 保存图片
                    with open(filepath, 'wb') as f:
                        f.write(img_resp.content)

                    # 替换为本地路径（Obsidian 相对路径）
                    relative_path = os.path.join("images", filename)
                    img['src'] = relative_path
                    img['data-src'] = None
                else:
                    print(f"  ⚠️  图片下载失败：{src}")
            except Exception as e:
                print(f"  ⚠️  图片处理错误：{e}")

        return str(soup)

    def _get_image_ext(self, url):
        """从 URL 推断图片扩展名"""
        ext_map = {
            'jpeg': 'jpg', 'jpg': 'jpg', 'png': 'png',
            'gif': 'gif', 'webp': 'webp', 'bmp': 'bmp'
        }
        parsed = urlparse(url)
        path = parsed.path.lower()

        for ext in ext_map:
            if ext in path:
                return ext_map[ext]

        # 默认返回 jpg
        return 'jpg'

    def html_to_markdown(self, content_html):
        """HTML 转 Markdown"""
        soup = BeautifulSoup(content_html, 'lxml')
        md_lines = []

        def process_element(elem):
            """递归处理元素"""
            if not hasattr(elem, 'name') or elem.name is None:
                return

            # 段落/文本块
            if elem.name in ['p', 'div']:
                text = elem.get_text(strip=True)
                if text:
                    md_lines.append(text + '\n')

            # 标题
            elif elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = min(int(elem.name[1]), 3)
                text = elem.get_text(strip=True)
                if text:
                    md_lines.append('#' * level + ' ' + text + '\n')

            # 图片
            elif elem.name == 'img':
                src = elem.get('src') or elem.get('data-src')
                alt = elem.get('alt', 'image')
                if src:
                    md_lines.append(f'![{alt}]({src})\n')

            # 引用
            elif elem.name == 'blockquote':
                text = elem.get_text(strip=True)
                if text:
                    md_lines.append('> ' + text + '\n')

            # 列表
            elif elem.name in ['ul', 'ol']:
                for li in elem.find_all('li', recursive=False):
                    text = li.get_text(strip=True)
                    if text:
                        md_lines.append(f'- {text}\n')

            # 代码块
            elif elem.name == 'pre':
                code = elem.get_text()
                md_lines.append('```\n' + code + '\n```\n')

            # 链接
            elif elem.name == 'a':
                text = elem.get_text(strip=True)
                href = elem.get('href', '')
                if text and href:
                    md_lines.append(f'[{text}]({href})\n')

            # 递归处理子元素
            elif elem.name in ['section', 'article', 'figure', 'figcaption', 'span', 'strong', 'em', 'b', 'i']:
                for child in elem.children:
                    if hasattr(child, 'name'):
                        process_element(child)
                    elif child.strip():
                        md_lines.append(child.strip() + ' ')

            # 默认：处理所有子元素
            else:
                for child in elem.children:
                    if hasattr(child, 'name'):
                        process_element(child)
                    elif hasattr(child, 'strip') and child.strip():
                        md_lines.append(child.strip() + ' ')

        # 从 body 开始处理（如果有）
        body = soup.find('body')
        if body:
            for child in body.children:
                process_element(child)
        else:
            for child in soup.children:
                process_element(child)

        return '\n'.join(md_lines)

    def save_article(self, title, content_md, output_path):
        """保存文章到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content_md)
        print(f"✅ 已保存：{output_path}")

    def generate_frontmatter(self, title, url, tags=None):
        """生成 YAML Frontmatter"""
        frontmatter = [
            "---",
            f"title: {title}",
            f"source: {url}",
            f"created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ]

        if tags:
            frontmatter.append(f"tags: [{', '.join(tags)}]")
        else:
            frontmatter.append("tags: [wechat, article]")

        frontmatter.append("---")
        return '\n'.join(frontmatter)

    def convert_to_markdown(self, elements, image_map):
        """将有序元素列表转换为 Markdown"""
        md_lines = []
        prev_type = None

        for item in elements:
            etype = item[0]

            # 跳过空文本
            if etype == 'text' and not item[1].strip():
                prev_type = etype
                continue

            # 处理文本（检测特殊格式）
            if etype == 'text':
                text = self._format_text(item[1])
                md_lines.append(text + '\n')

            # 处理图片（图片前后加空行）
            elif etype == 'img':
                src = item[1]
                local_path = image_map.get(src)
                if local_path:
                    # 如果前一个不是图片，前面加空行
                    if prev_type not in [None, 'img']:
                        md_lines.append('\n')
                    md_lines.append(f'![image]({local_path})\n')
                    md_lines.append('\n')

            # 处理标题
            elif etype == 'heading':
                text, level = item[1], item[2]
                md_lines.append('#' * level + ' ' + text + '\n')

            prev_type = etype

        # 清理过多空行（超过 2 个连续空行改为 1 个）
        result = '\n'.join(md_lines)
        result = re.sub(r'\n{3,}', '\n\n', result)

        return result

    def _format_text(self, text):
        """格式化文本，检测代码、列表、引用等"""
        # 1. 检测代码块（命令行、代码）
        code_patterns = [
            (r'^(\s*)(# macOS|/Applications|C:\\Program Files|google-chrome)', r'```bash\n\\g<0>\n```'),
            (r'^(\s*)(curl\s+http)', r'```bash\n\\g<0>\n```'),
            (r'^(\s*)(pip\s+|npm\s+|node\s+)', r'```bash\n\\g<0>\n```'),
            (r'^(\s*)(chrome://)', r'```bash\n\\g<0>\n```'),
        ]
        for pattern, replacement in code_patterns:
            if re.search(pattern, text):
                if not text.startswith('```'):
                    return f'```bash\n{text}\n```'

        # 2. 检测列表（第一，、第二，、第三，或 1. 2. 3. 或 X 层：）
        # 第一，第二，第三（中文序号）
        if text.startswith('第一') or text.startswith('第二') or text.startswith('第三'):
            return f'- {text}'
        # X 层：格式（基础层：、核心层：、效率层：等）
        if re.match(r'^.+层：', text):
            return f'- {text}'
        # 数字列表 1. 2. 3.
        list_match = re.match(r'^(\d+)\.\s*', text)
        if list_match:
            return f'- {text}'
        # 特殊符号列表
        if re.match(r'^[•●○■□▪▫]\s*', text):
            return re.sub(r'^[•●○■□▪▫]\s*', '- ', text)

        # 3. 检测引用（打个比方、例如、比如）
        quote_patterns = ['打个比方', '例如', '比如', '注意：', '提示：']
        for qp in quote_patterns:
            if text.startswith(qp):
                return '> ' + text

        # 4. 检测 URL 并转为链接
        url_pattern = r'(https?://[^\s，。；]+)'
        if re.search(url_pattern, text) and len(text) < 100:
            # 短文本中的 URL 转为链接
            text = re.sub(url_pattern, r'[\g<1>](\g<1>)', text)

        return text

    def process(self, url, output_dir=None, keep_images=True):
        """处理单篇文章"""
        if output_dir:
            self.output_dir = os.path.expanduser(output_dir)
        else:
            self.output_dir = os.path.expanduser(self.output_dir)

        os.makedirs(self.output_dir, exist_ok=True)

        # 抓取
        html = self.fetch_article(url)

        # 提取内容（有序元素列表）
        title, elements = self.extract_content(html)

        # 清理标题（移除特殊字符）
        safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
        safe_title = safe_title[:50]  # 限制长度

        # 创建文章目录
        article_dir = os.path.join(self.output_dir, safe_title)
        os.makedirs(article_dir, exist_ok=True)

        # 提取所有图片源（用于下载）
        image_sources = [(src, idx) for idx, (etype, src, *_) in enumerate(elements) if etype == 'img']

        # 处理图片
        image_map = {}  # src -> relative_path
        if keep_images and image_sources:
            print(f"🖼️  正在处理 {len(image_sources)} 张图片...")
            images_dir = os.path.join(article_dir, "images")
            os.makedirs(images_dir, exist_ok=True)

            for i, (src, _) in enumerate(image_sources):
                try:
                    print(f"  下载图片 {i+1}/{len(image_sources)}")
                    img_resp = self.session.get(src, timeout=10)
                    if img_resp.status_code == 200:
                        ext = self._get_image_ext(src)
                        filename = f"image_{i+1:03d}.{ext}"
                        filepath = os.path.join(images_dir, filename)

                        with open(filepath, 'wb') as f:
                            f.write(img_resp.content)

                        # 记录映射关系（Obsidian 相对路径）
                        relative_path = os.path.join("images", filename)
                        image_map[src] = relative_path
                except Exception as e:
                    print(f"  ⚠️  图片下载失败：{src}")

        # HTML 转 Markdown（按顺序）
        print("📝 正在转换 Markdown...")
        content_md = self.convert_to_markdown(elements, image_map)

        # 生成 Frontmatter
        frontmatter = self.generate_frontmatter(safe_title, url)

        # 合并内容
        full_content = frontmatter + '\n\n' + content_md

        # 添加原文链接
        full_content += f"\n\n---\n📌 原文链接：{url}\n"
        full_content += f"📅 抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        # 保存
        output_path = os.path.join(self.output_dir, f"{safe_title}.md")
        self.save_article(safe_title, full_content, output_path)

        print(f"\n🎉 完成！文章保存在：{article_dir}")
        return output_path

    def process_batch(self, urls, output_dir=None):
        """批量处理多篇文章"""
        results = []
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*50}")
            print(f"处理第 {i}/{len(urls)} 篇")
            print(f"{'='*50}")
            try:
                result = self.process(url, output_dir)
                results.append((url, result, None))
            except Exception as e:
                print(f"❌ 处理失败：{e}")
                results.append((url, None, str(e)))

        # 生成报告
        print(f"\n{'='*50}")
        print("批量处理完成")
        print(f"{'='*50}")
        success = sum(1 for _, _, e in results if e is None)
        print(f"成功：{success}/{len(urls)}")
        for url, path, error in results:
            status = "✅" if error is None else "❌"
            print(f"  {status} {url[:50]}...")
            if error:
                print(f"      错误：{error}")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="微信公众号文章转 Markdown 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 处理单篇文章
  python wechat_to_md.py https://mp.weixin.qq.com/s/xxx

  # 指定输出目录
  python wechat_to_md.py -o ~/Obsidian/Articles url

  # 不下载图片
  python wechat_to_md.py --no-images url

  # 批量处理
  python wechat_to_md.py url1 url2 url3
        """
    )

    parser.add_argument('url', nargs='+', help='微信文章 URL（可多个）')
    parser.add_argument('-o', '--output', default='~/Documents/Obsidian Vault/00-Inbox',
                        help='输出目录 (默认：~/Documents/Obsidian Vault/00-Inbox)')
    parser.add_argument('--no-images', action='store_true',
                        help='不下载图片')

    args = parser.parse_args()

    saver = WeChatSaver()

    if len(args.url) == 1:
        saver.process(args.url[0], args.output, not args.no_images)
    else:
        saver.process_batch(args.url, args.output)


if __name__ == '__main__':
    main()
