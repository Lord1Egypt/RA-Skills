#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取微信公众号草稿列表脚本
"""

import requests
import json
import sys
import io

# 设置标准输出编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_access_token(appid, secret):
    """获取 access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(url)
    result = response.json()

    if 'access_token' not in result:
        print(f"❌ 获取 access_token 失败")
        print(f"错误码: {result.get('errcode')}")
        print(f"错误信息: {result.get('errmsg')}")
        sys.exit(1)

    print(f"✅ 获取 access_token 成功（有效期 {result.get('expires_in')} 秒）")
    return result['access_token']

def get_draft_list(access_token):
    """获取草稿列表"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token={access_token}"
    
    # 微信草稿接口需要 POST 请求，参数为 JSON 格式
    # offset: 从第几个草稿开始获取，默认为 0
    # count: 要获取的草稿数量，最多为 20
    # no_content: 是否不返回草稿的具体内容，1 表示不返回
    payload = {
        "offset": 0,
        "count": 20,
        "no_content": 0  # 我们需要获取具体内容
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()

    if result.get('errcode', 0) != 0:
        print(f"❌ 获取草稿列表失败")
        print(f"错误码: {result.get('errcode')}")
        print(f"错误信息: {result.get('errmsg')}")
        sys.exit(1)

    print(f"✅ 获取草稿列表成功，共 {result.get('total_count')} 篇草稿")
    return result

def find_draft_by_title(draft_data, title):
    """根据标题查找草稿"""
    items = draft_data.get('item', [])

    # 先打印所有标题用于调试
    print(f"\n🔍 调试：所有标题如下：")
    for item in items:
        articles = item.get('content', {}).get('news_item', [])
        for article in articles:
            actual_title = article.get('title')
            print(f"   实际标题: {repr(actual_title)}")
            print(f"   目标标题: {repr(title)}")
            print(f"   是否匹配: {actual_title == title}")
            print()

    # 先尝试精确匹配
    for item in items:
        articles = item.get('content', {}).get('news_item', [])
        for article in articles:
            if article.get('title') == title:
                print(f"✅ 找到匹配草稿: {title}")
                print(f"   草稿 media_id: {item.get('media_id')}")
                return article, item.get('media_id')

    # 如果精确匹配失败，尝试模糊匹配（去除标点符号）
    title_clean = title.replace('，', ',').replace('。', '.').replace('；', ';')
    for item in items:
        articles = item.get('content', {}).get('news_item', [])
        for article in articles:
            actual_title = article.get('title')
            actual_title_clean = actual_title.replace('，', ',').replace('。', '.').replace('；', ';')
            if actual_title_clean == title_clean:
                print(f"✅ 找到匹配草稿（模糊匹配）: {actual_title}")
                print(f"   草稿 media_id: {item.get('media_id')}")
                return article, item.get('media_id')

    print(f"❌ 未找到标题为「{title}」的草稿")
    return None, None

def main():
    # 从命令行参数获取 AppID 和 AppSecret
    if len(sys.argv) < 3:
        print("用法: python get_draft.py <appid> <secret> [title]")
        print("示例: python get_draft.py wxa4f073c32600c19b 47e75b44cbe81261896649aa24a5e222 \"文章标题\"")
        sys.exit(1)

    appid = sys.argv[1]
    secret = sys.argv[2]
    target_title = sys.argv[3] if len(sys.argv) > 3 else None

    print(f"正在获取微信公众号草稿...")
    print(f"AppID: {appid}")
    print(f"目标标题: {target_title}\n")

    # Step 1: 获取 access_token
    access_token = get_access_token(appid, secret)

    # Step 2: 获取草稿列表
    draft_data = get_draft_list(access_token)

    # Step 3: 显示所有草稿标题
    print("\n📋 所有草稿列表:")
    items = draft_data.get('item', [])
    for i, item in enumerate(items, 1):
        articles = item.get('content', {}).get('news_item', [])
        for article in articles:
            print(f"   {i}. {article.get('title')}")
            print(f"      作者: {article.get('author', '未设置')}")
            print(f"      更新时间: {article.get('update_time', '未知')}")
            print()

    # Step 4: 如果指定了标题，查找并显示详细内容
    if target_title:
        article, media_id = find_draft_by_title(draft_data, target_title)
        if article:
            print("\n📄 草稿详细内容:")
            print("=" * 80)
            print(f"标题: {article.get('title')}")
            print(f"作者: {article.get('author', '未设置')}")
            print(f"摘要: {article.get('digest', '未设置')}")
            print(f"封面 media_id: {article.get('thumb_media_id')}")
            print(f"\n正文 HTML 内容:")
            print("-" * 80)
            print(article.get('content'))
            print("-" * 80)

            # 将内容保存到文件
            output_file = f"draft_{media_id}.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"""<!-- 文章标题: {article.get('title')} -->
<!-- 作者: {article.get('author', '未设置')} -->
<!-- 摘要: {article.get('digest', '未设置')} -->
<!-- 封面 media_id: {article.get('thumb_media_id')} -->
<!-- 草稿 media_id: {media_id} -->

{article.get('content')}
""")
            print(f"\n✅ 草稿内容已保存到: {output_file}")

            # 返回 media_id 供后续使用
            print(f"\n📌 草稿 media_id: {media_id}")
            return media_id
    else:
        print("\n💡 提示: 使用 python get_draft.py <appid> <secret> \"文章标题\" 查看详细内容")

if __name__ == "__main__":
    main()
