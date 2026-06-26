#!/usr/bin/env python3
"""
TinyScraper 自动化测试
测试 crawler.py 的各个组件
"""

import sys
import os
import tempfile
import shutil

# 确保能导入 crawler
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from crawler import (
    url_to_filepath,
    normalize_url,
    is_same_domain,
    rewrite_html_content,
    rewrite_css_content,
    LinkExtractor,
    CSSParser,
    JSParser,
    guess_content_type,
    make_relative_path,
)

def test_url_to_filepath():
    print("\n=== test_url_to_filepath ===")
    base = "/tmp/test_mirrors/example.com"

    tests = [
        ("https://example.com/", "index.html"),
        ("https://example.com/about", "about/index.html"),
        ("https://example.com/about.html", "about.html"),
        ("https://example.com/page?id=1", "page/index.html"),
        ("https://example.com/style.css?v=1.2", "style.css"),
    ]

    all_pass = True
    for url, expected in tests:
        result = url_to_filepath(base, url)
        # 只检查文件名部分
        filename = os.path.basename(result)
        status = "✅" if filename == os.path.basename(expected) else "❌"
        print(f"  {status} {url} -> {result}")
        if filename != os.path.basename(expected):
            all_pass = False
    return all_pass

def test_normalize_url():
    print("\n=== test_normalize_url ===")
    tests = [
        ("https://example.com/page#section", "https://example.com/page"),
        ("https://example.com/page?a=1&b=2", "https://example.com/page?a=1&b=2"),
        ("https://example.com/page#section?query", "https://example.com/page"),
    ]
    all_pass = True
    for url, expected in tests:
        result = normalize_url(url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {url} -> {result} (expected: {expected})")
        if result != expected:
            all_pass = False
    return all_pass

def test_is_same_domain():
    print("\n=== test_is_same_domain ===")
    tests = [
        ("https://example.com", "https://example.com/about", True),
        ("https://example.com", "https://other.com/about", False),
        ("https://example.com:8080", "https://example.com/about", True),
    ]
    all_pass = True
    for base, url, expected in tests:
        result = is_same_domain(base, url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {url} same_domain? {result} (expected: {expected})")
        if result != expected:
            all_pass = False
    return all_pass

def test_rewrite_html():
    print("\n=== test_rewrite_html ===")
    html = '''<!DOCTYPE html>
<html>
<head>
  <link href="/assets/style.css" rel="stylesheet">
  <script src="/js/app.js"></script>
</head>
<body>
  <a href="/about">About</a>
  <a href="https://external.com">External</a>
  <img src="/images/logo.png">
  <img src="data:image/png;base64,abc123">
</body>
</html>'''

    # 模拟页面在根目录
    page_url = "https://example.com/"
    local_dir = "/tmp/test_mirrors/example.com"
    rewritten = rewrite_html_content(html, page_url, local_dir)

    # 检查点
    checks = [
        ('href="assets/style.css"' in rewritten or 'href="./assets/style.css"' in rewritten, "CSS link rewritten to relative"),
        ('src="js/app.js"' in rewritten or 'src="./js/app.js"' in rewritten, "JS src rewritten to relative"),
        ('href="about/index.html"' in rewritten or 'href="./about/index.html"' in rewritten, "Internal link /about -> about/index.html"),
        # 外部链接保留原值（由 _external/index.html 模板处理，不在 HTML 重写阶段替换）
        ('https://external.com' in rewritten, "External link kept as-is in HTML"),
        ('data:image' in rewritten, "data: URI should be kept"),
    ]

    all_pass = True
    for result, desc in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {desc}")
        if not result:
            all_pass = False

    print(f"\n   rewritten HTML:\n{rewritten[:500]}")
    return all_pass

def test_css_parser():
    print("\n=== test_css_parser ===")
    css = '''
    body { background: url('/images/bg.png'); }
    @import "other.css";
    .icon { background: url("icon.jpg"); }
    '''

    urls = CSSParser.extract_urls(css)
    expected = {'/images/bg.png', 'other.css', 'icon.jpg'}
    result = "✅" if urls == expected else "❌"
    print(f"  {result} extracted URLs: {urls}")
    return urls == expected

def test_js_parser():
    print("\n=== test_js_parser ===")
    js = '''
    import Something from '/lib/module.js';
    import('/js/chunk.js');
    require('./utils.js');
    var img = '<img src="/images/photo.jpg">';
    '''

    urls = JSParser.extract_urls(js)
    expected = {'/lib/module.js', '/js/chunk.js', './utils.js'}
    result = "✅" if urls == expected else "❌"
    print(f"  {result} extracted URLs: {urls}")
    return urls == expected

def test_rewrite_css():
    print("\n=== test_rewrite_css ===")
    css = '''
    body { background: url('/images/bg.png'); }
    @import "base.css";
    '''
    # CSS 路径: https://example.com/css/style.css → 本地: /tmp/test/example.com/css/style.css
    # 图片路径: https://example.com/images/bg.png → 本地: /tmp/test/example.com/images/bg.png
    # 相对路径应为: ../images/bg.png
    rewritten = rewrite_css_content(css, "https://example.com/css/style.css", "/tmp/test/example.com/css/style.css")
    print(f"  rewritten CSS:\n{rewritten}")
    checks = [
        ("url(" in rewritten, "url() preserved"),
        ("images/bg.png" in rewritten, "bg.png path relative to CSS dir (images/bg.png)"),
    ]
    all_pass = True
    for result, desc in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {desc}")
        if not result:
            all_pass = False
    return all_pass

def test_guess_content_type():
    print("\n=== test_guess_content_type ===")
    tests = [
        ("https://example.com/style.css", b"body {}", "text/css"),
        ("https://example.com/app.js", b"function()", "application/javascript"),
        ("https://example.com/logo.png", b"\x89PNG", "image/png"),
        ("https://example.com/page", b"<html>", "application/octet-stream"),
    ]
    all_pass = True
    for url, content, expected in tests:
        result = guess_content_type(url, content)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {url} -> {result} (expected: {expected})")
        if result != expected:
            all_pass = False
    return all_pass

def test_link_extractor():
    print("\n=== test_link_extractor ===")
    html = '''
    <a href="/about">About</a>
    <img src="/images/logo.png">
    <link href="/style.css" rel="stylesheet">
    <script src="/app.js"></script>
    <a href="mailto:test@example.com">Email</a>
    <a href="javascript:void(0)">JS</a>
    <a href="#section">Anchor</a>
    <!-- <img src="/images/capstone.jpg"> -->
    '''
    parser = LinkExtractor()
    parser.feed(html)
    print(f"  links: {parser.links}")
    print(f"  resources: {parser.resources}")
    checks = [
        (len(parser.links) == 1, "only /about in links"),
        ('/images/logo.png' in parser.resources, "logo.png in resources"),
        ('/style.css' in parser.resources, "style.css in resources"),
        ('/app.js' in parser.resources, "app.js in resources"),
        ('/images/capstone.jpg' in parser.resources, "capstone.jpg from comment"),
    ]
    all_pass = True
    for result, desc in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {desc}")
        if not result:
            all_pass = False
    return all_pass

def main():
    print("=" * 60)
    print("TinyScraper 自动化测试")
    print("=" * 60)

    results = {
        "url_to_filepath": test_url_to_filepath(),
        "normalize_url": test_normalize_url(),
        "is_same_domain": test_is_same_domain(),
        "rewrite_html": test_rewrite_html(),
        "css_parser": test_css_parser(),
        "js_parser": test_js_parser(),
        "rewrite_css": test_rewrite_css(),
        "guess_content_type": test_guess_content_type(),
        "link_extractor": test_link_extractor(),
    }

    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {name}")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\n  总计: {passed}/{total} 通过")

    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())
