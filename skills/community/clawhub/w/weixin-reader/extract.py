#!/usr/bin/env python3
"""
微信公众号文章提取器
使用 Playwright 渲染页面并提取内容
"""

import sys
import json
import re
import socket
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def validate_url(url):
    """验证 URL 安全性，防止 SSRF 和非法访问
    
    安全检查包括：
    1. 协议检查 - 只允许 http/https
    2. 字面主机名检查 - 禁止明显的内网地址
    3. DNS 解析检查 - 确保解析后的 IP 不是内网地址（防止 DNS 重绑定攻击）
    """
    # 检查是否为空
    if not url or not isinstance(url, str):
        return False, "URL 不能为空"
    
    # 去除空白字符
    url = url.strip()
    
    # 只允许 http/https 协议
    if not url.startswith(('http://', 'https://')):
        return False, "仅支持 HTTP/HTTPS 协议"
    
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        
        if not hostname:
            return False, "无法解析主机名"
        
        # 禁止访问内网地址（字面检查）
        blocked_hosts = [
            'localhost', '127.0.0.1', '0.0.0.0',
            '::1', '[::1]',  # IPv6 localhost
        ]
        
        for blocked in blocked_hosts:
            if hostname == blocked or hostname.startswith(blocked):
                return False, f"禁止访问内网地址: {hostname}"
        
        # 禁止私有 IP 前缀（字面检查）
        blocked_prefixes = [
            '10.', '172.16.', '172.17.', '172.18.', '172.19.',
            '172.20.', '172.21.', '172.22.', '172.23.', '172.24.',
            '172.25.', '172.26.', '172.27.', '172.28.', '172.29.',
            '172.30.', '172.31.', '192.168.'
        ]
        
        for prefix in blocked_prefixes:
            if hostname.startswith(prefix):
                return False, f"禁止访问内网地址: {hostname}"
        
        # DNS 解析检查 - 防止 DNS 重绑定攻击
        try:
            resolved_ip = socket.getaddrinfo(hostname, None)[0][4][0]
            
            # 检查解析后的 IP 是否是内网地址
            if resolved_ip.startswith(('10.', '172.16.', '172.17.', '172.18.', '172.19.',
                                       '172.20.', '172.21.', '172.22.', '172.23.', '172.24.',
                                       '172.25.', '172.26.', '172.27.', '172.28.', '172.29.',
                                       '172.30.', '172.31.', '192.168.', '127.', '0.', '::1')):
                return False, f"域名解析到内网地址，禁止访问: {hostname} -> {resolved_ip}"
        except socket.gaierror:
            # DNS 解析失败，可能是内网域名或无效域名
            return False, f"无法解析域名: {hostname}"
        
        return True, None
        
    except Exception as e:
        return False, f"URL 解析错误: {str(e)}"


def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_article(url):
    """提取微信公众号文章内容
    
    Returns:
        dict: 结构化数据，包含 metadata、content、stats
    """
    
    with sync_playwright() as p:
        # 启动浏览器（无头模式）
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            # 访问页面并等待加载
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 等待内容加载
            page.wait_for_selector('#js_content, .rich_media_content', timeout=10000)
            
            # 获取页面 HTML
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # ========== 提取元数据 ==========
            metadata = {}
            
            # 标题
            title = ""
            title_elem = soup.select_one('#activity_name, .rich_media_title, h1')
            if title_elem:
                title = clean_text(title_elem.get_text())
            metadata['title'] = title
            
            # 公众号名称
            account = ""
            account_elem = soup.select_one('#js_name, .profile_nickname, .rich_media_meta_nickname')
            if account_elem:
                account = clean_text(account_elem.get_text())
            metadata['account'] = account
            
            # 作者
            author = ""
            author_elem = soup.select_one('#js_author_name, .rich_media_meta_text')
            if author_elem:
                author = clean_text(author_elem.get_text())
            metadata['author'] = author
            
            # 发布时间
            publish_time = ""
            time_elem = soup.select_one('#publish_time, .rich_media_meta_text em')
            if time_elem:
                publish_time = clean_text(time_elem.get_text())
            metadata['publish_time'] = publish_time
            
            # 文章描述/摘要（如果有）
            description = ""
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '')
            metadata['description'] = description
            
            # 原文链接
            metadata['source_url'] = url
            
            # 提取时间戳
            metadata['extracted_at'] = __import__('datetime').datetime.now().isoformat()
            
            # ========== 提取正文内容 ==========
            content = ""
            content_html = ""
            content_elem = soup.select_one('#js_content, .rich_media_content')
            
            if content_elem:
                # 保存原始 HTML
                content_html = str(content_elem)
                
                # 移除脚本和样式
                for script in content_elem(['script', 'style', 'iframe']):
                    script.decompose()
                
                # 提取文本，保留段落结构
                paragraphs = []
                for p in content_elem.find_all(['p', 'section']):
                    text = clean_text(p.get_text())
                    if text and len(text) > 5:  # 过滤太短的片段
                        paragraphs.append(text)
                
                content = '\n\n'.join(paragraphs)
            
            # ========== 提取图片 ==========
            images = []
            for img in soup.select('#js_content img, .rich_media_content img'):
                src = img.get('data-src') or img.get('src')
                if src and src.startswith('http'):
                    images.append({
                        'url': src,
                        'alt': img.get('alt', '')
                    })
            
            # ========== 统计信息 ==========
            stats = {
                'content_length': len(content),
                'content_chars': len(content.replace('\n', '').replace(' ', '')),
                'paragraph_count': len([p for p in content.split('\n\n') if p.strip()]),
                'image_count': len(images),
                'has_title': bool(title),
                'has_author': bool(author),
                'has_account': bool(account)
            }
            
            # 估算阅读时间（按 300 字/分钟）
            stats['read_time_minutes'] = max(1, round(stats['content_chars'] / 300))
            
            browser.close()
            
            # ========== 返回结构化数据 ==========
            return {
                'success': True,
                'version': '1.1.0',
                'metadata': metadata,
                'content': {
                    'text': content,
                    'html': content_html[:5000] if content_html else ''  # 限制 HTML 大小
                },
                'images': images[:20],  # 最多返回 20 张图片
                'stats': stats
            }
            
        except Exception as e:
            browser.close()
            return {
                'success': False,
                'version': '1.1.0',
                'error': str(e),
                'url': url
            }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': '请提供微信公众号文章链接'
        }, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 验证 URL 安全性
    is_valid, error_msg = validate_url(url)
    if not is_valid:
        print(json.dumps({
            'success': False,
            'error': f'URL 验证失败: {error_msg}'
        }, ensure_ascii=False))
        sys.exit(1)
    
    result = extract_article(url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
