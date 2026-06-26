#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取指定索引的微信公众号草稿脚本
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

    payload = {
        "offset": 0,
        "count": 20,
        "no_content": 0
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

def main():
    # 从命令行参数获取 AppID、AppSecret 和草稿索引
    if len(sys.argv) < 4:
        print("用法: python get_draft_by_index.py <appid> <secret> <index>")
        print("示例: python get_draft_by_index.py wxa4f073c32600c19b 47e75b44cbe81261896649aa24a5e222 3")
        print("说明: index 从 1 开始，1 表示第一个草稿")
        sys.exit(1)

    appid = sys.argv[1]
    secret = sys.argv[2]
    index = int(sys.argv[3]) - 1  # 转换为 0-based 索引

    print(f"正在获取微信公众号草稿...")
    print(f"AppID: {appid}")
    print(f"草稿索引: {index + 1}\n")

    # Step 1: 获取 access_token
    access_token = get_access_token(appid, secret)

    # Step 2: 获取草稿列表
    draft_data = get_draft_list(access_token)

    # Step 3: 获取指定索引的草稿
    items = draft_data.get('item', [])
    if index >= len(items):
        print(f"❌ 索引超出范围，只有 {len(items)} 篇草稿")
        sys.exit(1)

    item = items[index]
    articles = item.get('content', {}).get('news_item', [])
    if not articles:
        print(f"❌ 草稿中没有文章")
        sys.exit(1)

    article = articles[0]
    media_id = item.get('media_id')

    print("\n📄 草稿详细内容:")
    print("=" * 80)
    print(f"标题: {article.get('title')}")
    print(f"作者: {article.get('author', '未设置')}")
    print(f"摘要: {article.get('digest', '未设置')}")
    print(f"封面 media_id: {article.get('thumb_media_id')}")
    print(f"\n正文 HTML 内容:")
    print("-" * 80)
    content = article.get('content')
    print(content)
    print("-" * 80)

    # 将内容保存到文件
    output_file = f"draft_{media_id}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!-- 文章标题: {article.get('title')} -->
<!-- 作者: {article.get('author', '未设置')} -->
<!-- 摘要: {article.get('digest', '未设置')} -->
<!-- 封面 media_id: {article.get('thumb_media_id')} -->
<!-- 草稿 media_id: {media_id} -->

{content}
""")
    print(f"\n✅ 草稿内容已保存到: {output_file}")

    # 返回 media_id 供后续使用
    print(f"\n📌 草稿 media_id: {media_id}")
    print(f"📌 封面 media_id: {article.get('thumb_media_id')}")

if __name__ == "__main__":
    main()
