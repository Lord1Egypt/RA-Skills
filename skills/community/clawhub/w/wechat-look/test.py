#!/usr/bin/env python3
"""
WeChat Look 技能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wechat_reader import WeChatReader

def test_url_normalization():
    """测试URL规范化功能"""
    reader = WeChatReader()

    test_cases = [
        {
            'input': 'https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA',
            'expected': 'https://mp.weixin.qq.com/s/D7vSSNGCQFT4NAdY6loPWA?scene=1'
        },
        {
            'input': 'https://mp.weixin.qq.com/s/S3AF2BKqRYcxHaI8uZ71BA?param=value',
            'expected': 'https://mp.weixin.qq.com/s/S3AF2BKqRYcxHaI8uZ71BA?param=value&scene=1'
        },
        {
            'input': 'https://example.com/not-wechat',
            'expected': 'https://example.com/not-wechat'
        }
    ]

    print("🔍 URL规范化测试:")
    print("=" * 50)

    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = reader.normalize_url(case['input'])
        passed = result == case['expected']
        status = "✅ PASS" if passed else "❌ FAIL"

        print(f"测试 {i}: {status}")
        print(f"  输入:    {case['input']}")
        print(f"  预期:    {case['expected']}")
        print(f"  实际:    {result}")
        print()

        if not passed:
            all_passed = False

    return all_passed


def test_article_reading():
    """测试文章读取功能（模拟）"""
    reader = WeChatReader()

    # 模拟HTML内容
    mock_html = """
    <html>
    <head>
        <title>测试微信文章标题</title>
        <meta name="author" content="测试作者">
    </head>
    <body>
        <div id="js_content">这是测试文章内容...</div>
    </body>
    </html>
    """

    print("📖 文章提取测试:")
    print("=" * 50)

    try:
        result = reader.extract_content(mock_html)
        print(f"标题: {result['title']}")
        print(f"作者: {result['author']}")
        print(f"状态: {result['status']}")
        print(f"内容长度: {len(result['content'])} 字符")
        print("✅ 文章提取测试通过")
        return True
    except Exception as e:
        print(f"❌ 文章提取失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🧪 WeChat Look 技能测试")
    print("=" * 60)

    # 运行所有测试
    url_test_passed = test_url_normalization()
    article_test_passed = test_article_reading()

    print("\n📊 测试总结:")
    print("=" * 50)
    print(f"URL规范化测试: {'✅ 通过' if url_test_passed else '❌ 失败'}")
    print(f"文章提取测试: {'✅ 通过' if article_test_passed else '❌ 失败'}")

    overall_passed = url_test_passed and article_test_passed
    print(f"\n总体结果: {'✅ 所有测试通过' if overall_passed else '❌ 部分测试失败'}")

    if overall_passed:
        print("\n🎉 技能创建成功！可以安装使用了。")
    else:
        print("\n⚠️  发现一些问题，请检查代码。")


if __name__ == "__main__":
    main()