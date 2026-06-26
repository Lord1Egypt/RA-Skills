#!/usr/bin/env python3
"""
微信公众号文章导出工具 (Python版本)

依赖安装:
  pip install requests beautifulsoup4 pylxml markdownify

使用方法:
  python wechat-exporter.py <文章URL> [输出目录]

示例:
  python wechat-exporter.py https://mp.weixin.qq.com/s/J05F7C_DGmsOoBIEZd-Fuw ./output
"""

import sys
import os
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import argparse
import json

try:
    import requests
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
except ImportError as e:
    print(f"错误: 缺少必要的库: {e}")
    print("请运行: pip install requests beautifulsoup4 pylxml markdownify")
    sys.exit(1)


def get_default_output_dir():
    """自动获取工作空间的 source 目录"""
    # 常见工作空间路径
    workspace_candidates = [
        os.path.expanduser("~/.openclaw/workspace-qiming"),
        os.path.expanduser("~/.openclaw/workspace"),
        os.path.expanduser("~/workspace"),
    ]
    
    for workspace in workspace_candidates:
        source_dir = os.path.join(workspace, "source")
        if os.path.isdir(source_dir):
            return source_dir
    
    # 如果都不存在，返回第一个候选的 source 目录
    return os.path.join(workspace_candidates[0], "source")


class WechatArticleExporter:
    """微信公众号文章导出器"""

    def __init__(self, url, output_dir=None):
        self.url = url
        self.output_dir = output_dir if output_dir else get_default_output_dir()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })

    def extract_meta(self, soup):
        """提取文章元数据"""
        meta = {}

        # 提取标题
        title_tag = soup.find('meta', property='og:title')
        meta['title'] = title_tag.get('content', '未知标题') if title_tag else '未知标题'

        # 提取作者
        author_tag = soup.find('meta', property='og:article:author')
        meta['author'] = author_tag.get('content', '未知作者') if author_tag else '未知作者'

        # 提取发布时间
        time_tag = soup.find('meta', property='og:article:published_time')
        meta['publish_time'] = time_tag.get('content', '未知时间') if time_tag else '未知时间'

        # 提取描述
        desc_tag = soup.find('meta', property='og:description')
        meta['description'] = desc_tag.get('content', '') if desc_tag else ''

        # 提取公众号名称
        account_tag = soup.find('meta', property='og:article:author')
        meta['account'] = account_tag.get('content', '') if account_tag else ''

        return meta

    def extract_content(self, soup):
        """提取文章正文内容"""
        # 微信文章的正文通常在 id="js_content" 的div中
        content_div = soup.find('div', id='js_content')

        if not content_div:
            return None

        return content_div

    def convert_to_markdown(self, html_content):
        """将HTML内容转换为Markdown"""
        if not html_content:
            return ""

        # 使用markdownify转换
        markdown_text = md(str(html_content))

        return markdown_text

    def sanitize_filename(self, filename):
        """清理文件名中的非法字符"""
        # 移除或替换Windows/Linux文件名中的非法字符
        illegal_chars = r'[<>:"/\\|?*]'
        safe_filename = re.sub(illegal_chars, '_', filename)
        # 移除多余的空格和点
        safe_filename = re.sub(r'\s+', '_', safe_filename)
        safe_filename = safe_filename.strip('.')
        return safe_filename

    def export(self):
        """导出文章"""
        print(f"正在下载文章: {self.url}")

        try:
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"错误: 无法下载文章 - {e}")
            return False

        # 解析HTML
        soup = BeautifulSoup(response.text, 'lxml')

        # 提取元数据
        meta = self.extract_meta(soup)
        print(f"标题: {meta['title']}")
        print(f"作者: {meta['author']}")
        print(f"发布时间: {meta['publish_time']}")

        # 提取正文内容
        content_div = self.extract_content(soup)

        if not content_div:
            print("警告: 无法找到文章正文内容")
            print("可能的原因:")
            print("  1. 文章需要登录才能查看")
            print("  2. 文章已被删除或设为私密")
            print("  3. 微信反爬虫机制")
            markdown_content = ""
        else:
            # 转换为Markdown
            markdown_content = self.convert_to_markdown(content_div)
            print(f"正文长度: {len(markdown_content)} 字符")

        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = self.sanitize_filename(meta['title'])
        filename = f"{timestamp}_{safe_title}.md"

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, filename)

        # 写入Markdown文件
        with open(output_path, 'w', encoding='utf-8') as f:
            # 写入YAML front matter
            f.write("---\n")
            f.write(f"title: {meta['title']}\n")
            f.write(f"author: {meta['author']}\n")
            f.write(f"publish_time: {meta['publish_time']}\n")
            f.write(f"source_url: {self.url}\n")
            f.write(f"exported_at: {datetime.now().isoformat()}\n")
            if meta.get('description'):
                f.write(f"description: {meta['description']}\n")
            f.write("---\n\n")

            # 写入标题
            f.write(f"# {meta['title']}\n\n")
            f.write(f"> 原文链接: {self.url}\n\n")
            f.write("**作者**: " + meta['author'] + "\n\n")
            f.write("**发布时间**: " + meta['publish_time'] + "\n\n")
            f.write("-----\n\n")

            # 写入正文内容
            if markdown_content:
                f.write(markdown_content)
            else:
                f.write("**无法提取正文内容，请手动复制或查看原文**\n\n")

        print(f"\n✓ 文章已导出到: {output_path}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='微信公众号文章导出工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s https://mp.weixin.qq.com/s/J05F7C_DGmsOoBIEZd-Fuw
  %(prog)s https://mp.weixin.qq.com/s/J05F7C_DGmsOoBIEZd-Fuw ./output
  %(prog)s https://mp.weixin.qq.com/s/xxx -o ./articles

注意:
  - 微信有反爬虫机制，部分文章可能无法完整提取
  - 建议配合浏览器扩展使用（如 MarkDownload）
        """
    )
    parser.add_argument('url', help='微信公众号文章URL')
    parser.add_argument('output_dir', nargs='?', default=None,
                       help=f'输出目录（默认: 自动识别工作空间 source 目录）')
    parser.add_argument('-o', '--output', dest='output_dir_alt',
                       help='输出目录（等同于位置参数）')

    args = parser.parse_args()

    # 优先使用 -o 参数，否则使用默认的工作空间 source 目录
    output_dir = args.output_dir_alt or args.output_dir if args.output_dir else get_default_output_dir()

    # 验证URL
    if not args.url.startswith('https://mp.weixin.qq.com/'):
        print("错误: 不是有效的微信公众号文章URL")
        print("URL应该以 https://mp.weixin.qq.com/ 开头")
        sys.exit(1)

    # 创建导出器并导出
    exporter = WechatArticleExporter(args.url, output_dir)
    success = exporter.export()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
