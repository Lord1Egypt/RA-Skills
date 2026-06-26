#!/usr/bin/env python3
"""
微信公众号文章获取脚本
使用 DrissionPage 控制 Chrome 浏览器获取文章内容

Author: David & Agent
"""

import sys
import os
import argparse
import time


def fetch_article(url, output_dir=None, headless=False):
    """
    获取微信公众号文章内容
    
    Args:
        url: 微信公众号文章链接
        output_dir: 输出目录（默认为当前工作目录）
        headless: 是否使用无头模式（默认 False，微信文章需要完整浏览器环境）
    
    Returns:
        dict: 包含 title, url, content, output_file 的字典
    """
    try:
        from DrissionPage import ChromiumPage, ChromiumOptions
    except ImportError:
        print("错误: DrissionPage 未安装", file=sys.stderr)
        print("请运行: pip install DrissionPage", file=sys.stderr)
        sys.exit(1)
    
    # 输出目录默认为当前工作目录
    if output_dir is None:
        output_dir = os.getcwd()
    os.makedirs(output_dir, exist_ok=True)

    # 配置浏览器：禁用缓存，确保每次拉取最新内容
    options = ChromiumOptions()
    options.set_argument('--disk-cache-size=0')
    options.set_argument('--media-cache-size=0')
    options.set_argument('--cache-type=0')
    if headless:
        options.headless(True)
    
    try:
        # URL 追加时间戳绕过微信 CDN 缓存
        cache_buster = f"_t={int(time.time() * 1000)}"
        if "?" in url:
            fetch_url = f"{url}&{cache_buster}"
        else:
            fetch_url = f"{url}?{cache_buster}"
        
        print(f"正在获取文章: {fetch_url}", file=sys.stderr)
        
        page = ChromiumPage(options)
        page.get(fetch_url)
        page.wait(3)
        
        # 获取标题
        title = page.title
        print(f"标题: {title}", file=sys.stderr)
        
        # 等待正文加载
        try:
            page.wait.ele_displayed('#js_content', timeout=10)
        except:
            print("警告: 未找到 #js_content，尝试获取全页文本", file=sys.stderr)
        
        # 提取正文
        try:
            text_content = page.ele('#js_content').text
        except:
            text_content = page.ele('body').text
        
        print(f"内容长度: {len(text_content)} 字符", file=sys.stderr)
        
        # 截图
        screenshot_path = os.path.join(output_dir, 'article_screenshot_weixin.png')
        try:
            page.get_screenshot(path=screenshot_path, full_page=True)
            print(f"截图: {screenshot_path}", file=sys.stderr)
        except Exception as e:
            print(f"截图失败: {e}", file=sys.stderr)
        
        # 组装 Markdown 输出
        md_content = f"# {title}\n\n{text_content}\n"
        
        # 保存到文件
        output_file = os.path.join(output_dir, 'article_content_weixin.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"已保存: {output_file}", file=sys.stderr)
        
        # stdout 输出纯文本内容供 Agent 直接读取
        print(md_content)
        
        return {
            'title': title,
            'url': url,
            'content': text_content,
            'output_file': output_file
        }
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return {'error': str(e), 'url': url}
    finally:
        try:
            page.quit()
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description='获取微信公众号文章内容')
    parser.add_argument('url', help='微信公众号文章链接')
    parser.add_argument('-o', '--output', default=None, help='输出目录（默认当前目录）')
    parser.add_argument('--headless', action='store_true', help='使用无头模式（微信文章通常需要完整浏览器，慎用）')
    args = parser.parse_args()

    # URL 格式提示（不阻断，仅警告）
    if 'mp.weixin.qq.com' not in args.url:
        print(f"警告: URL 可能不是微信公众号文章: {args.url}", file=sys.stderr)

    result = fetch_article(args.url, output_dir=args.output, headless=args.headless)
    
    if 'error' in result:
        print(f"获取失败: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
