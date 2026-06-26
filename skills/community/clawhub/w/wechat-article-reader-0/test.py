#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章读取 Skill 测试脚本
"""

import json
from main import WeChatArticleReader, handle


def test_url_extraction():
    """测试URL提取功能"""
    print("=" * 50)
    print("测试1: URL提取功能")
    print("=" * 50)

    from main import extract_url

    test_cases = [
        ("这是文章链接：https://mp.weixin.qq.com/s/abc123", "https://mp.weixin.qq.com/s/abc123"),
        ("https://mp.weixin.qq.com/s/test123 请帮我读取", "https://mp.weixin.qq.com/s/test123"),
        ("这不是公众号链接 https://baidu.com", None),
        ("", None)
    ]

    for i, (text, expected) in enumerate(test_cases, 1):
        result = extract_url(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} 测试用例 {i}: {text[:30]}...")
        if result != expected:
            print(f"  期望: {expected}")
            print(f"  实际: {result}")
    print()


def test_wechat_url_detection():
    """测试微信URL检测"""
    print("=" * 50)
    print("测试2: 微信URL检测")
    print("=" * 50)

    reader = WeChatArticleReader()

    test_urls = [
        ("https://mp.weixin.qq.com/s/abc123", True),
        ("https://mp.weixin.qq.com/s/def456?param=123", True),
        ("https://www.baidu.com", False),
        ("https://weixin.qq.com", False)
    ]

    for url, expected in test_urls:
        result = reader.is_wechat_url(url)
        status = "✓" if result == expected else "✗"
        print(f"{status} {url}: {'是微信链接' if result else '不是微信链接'}")
    print()


def test_html_parsing():
    """测试HTML解析功能"""
    print("=" * 50)
    print("测试3: HTML解析功能")
    print("=" * 50)

    reader = WeChatArticleReader()

    # 模拟微信文章HTML
    mock_html = """
    <html>
    <head>
        <meta property="og:title" content="测试文章标题" />
        <meta property="og:site_name" content="测试公众号" />
        <meta property="article:published_time" content="2026-03-16" />
    </head>
    <body>
        <h1 class="rich_media_title">测试文章标题</h1>
        <div class="rich_media_meta_text">测试作者</div>
        <div id="js_content">
            <p>这是第一段内容。</p>
            <p>这是第二段内容。</p>
            <p>这是第三段内容。</p>
        </div>
    </body>
    </html>
    """

    result = reader.parse_article(mock_html, "https://mp.weixin.qq.com/s/test")

    if result["status"] == "success":
        data = result["data"]
        print("✓ 解析成功！")
        print(f"  标题: {data['title']}")
        print(f"  作者: {data['author']}")
        print(f"  公众号: {data['account']}")
        print(f"  发布时间: {data['publish_time']}")
        print(f"  内容长度: {len(data['content'])} 字符")
        print(f"  摘要: {data['summary'][:50]}...")
    else:
        print(f"✗ 解析失败: {result['message']}")
    print()


def test_handle_function():
    """测试主处理函数"""
    print("=" * 50)
    print("测试4: 主处理函数")
    print("=" * 50)

    # 注意：这只是模拟测试，实际测试需要真实的微信文章链接
    test_request = {
        "message": "请帮我读取这篇文章：https://mp.weixin.qq.com/s/test",
        "config": {
            "timeout": 10,
            "max_retries": 2
        }
    }

    print("提示: 此测试需要真实的微信文章链接才能完整运行")
    print("模拟请求结构:")
    print(json.dumps(test_request, ensure_ascii=False, indent=2))
    print()

    # result = handle(test_request)
    # print("返回结果:")
    # print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("微信公众号文章读取 Skill - 测试套件")
    print("=" * 50 + "\n")

    try:
        test_url_extraction()
        test_wechat_url_detection()
        test_html_parsing()
        test_handle_function()

        print("=" * 50)
        print("✓ 所有测试完成！")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ 测试过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
