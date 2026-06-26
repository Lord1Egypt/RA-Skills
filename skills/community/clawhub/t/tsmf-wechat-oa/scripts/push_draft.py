#!/usr/bin/env python3
"""
微信公众号文章推送脚本 V8
支持多主题排版样式
"""

import os
import sys
import json
import requests
import argparse
from markdown_to_wechat_html import convert_markdown_to_wechat_html, list_available_themes, ThemePresets

# 微信公众号配置 - 从环境变量读取
APP_ID = os.getenv('WECHAT_APP_ID', '')
APP_SECRET = os.getenv('WECHAT_APP_SECRET', '')

if not APP_ID or not APP_SECRET:
    print("⚠️  警告: 未设置微信凭证环境变量")
    print("   请设置: WECHAT_APP_ID 和 WECHAT_APP_SECRET")


def get_access_token():
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    try:
        response = requests.get(url, timeout=30)
        result = response.json()
        if 'access_token' in result:
            print(f"✅ Access Token 获取成功！")
            return result['access_token']
        else:
            print(f"❌ 获取 Token 失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None


def upload_thumb_image(access_token, image_path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb"
    try:
        if not os.path.exists(image_path):
            print(f"❌ 图片不存在: {image_path}")
            return None
        print(f"🖼️ 上传封面图片: {image_path}")
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, files=files, timeout=30)
        result = response.json()
        if 'media_id' in result:
            print(f"✅ 封面上传成功！")
            return result['media_id']
        else:
            print(f"❌ 上传失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return None


def add_draft(access_token, title, content, thumb_media_id, author, digest):
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    data = {
        "articles": [{
            "title": title,
            "content": content,
            "author": author,
            "digest": digest,
            "thumb_media_id": thumb_media_id,
            "show_cover_pic": 1,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }]
    }
    try:
        print(f"📤 正在创建草稿...")
        response = requests.post(
            url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        result = response.json()
        if 'media_id' in result:
            print(f"✅ 草稿创建成功！")
            return result['media_id']
        else:
            print(f"❌ 创建失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def show_themes():
    """显示所有可用主题"""
    print("\n🎨 可用排版主题：")
    print("=" * 60)
    themes = list_available_themes()
    for theme_id, info in themes.items():
        print(f"\n  {theme_id}")
        print(f"    名称: {info['name']}")
        print(f"    描述: {info['description']}")
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description='微信公众号文章推送工具')
    parser.add_argument('--file', '-f', type=str, help='文章文件路径 (.md 或 .html)')
    parser.add_argument('--theme', '-t', type=str, default=None,
                        help='排版主题 (不指定则自动推荐，仅对 Markdown 有效)')
    parser.add_argument('--list-themes', '-l', action='store_true',
                        help='列出所有可用主题')
    parser.add_argument('--author', '-a', type=str, default='wander云上',
                        help='作者名称')
    parser.add_argument('--cover', '-c', type=str, default='images/cover.jpg',
                        help='封面图片路径')
    parser.add_argument('--auto-theme', action='store_true',
                        help='自动根据内容推荐主题')
    parser.add_argument('--title', type=str, help='文章标题（HTML 文件需要手动指定）')
    
    args = parser.parse_args()
    
    if args.list_themes:
        show_themes()
        return True
    
    themes = list_available_themes()
    
    # 确定文章路径
    if args.file:
        article_path = args.file
    else:
        # 默认找最新的草稿（支持 .md 和 .html）
        drafts_dir = "_drafts"
        if os.path.exists(drafts_dir):
            files = [f for f in os.listdir(drafts_dir) if f.endswith('.md') or f.endswith('.html')]
            if files:
                files.sort(reverse=True)
                article_path = os.path.join(drafts_dir, files[0])
            else:
                print("❌ 未找到草稿文件")
                return False
        else:
            print("❌ 草稿目录不存在")
            return False
    
    print(f"📄 读取文章: {article_path}")
    
    # 判断文件类型
    is_html = article_path.endswith('.html')
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if is_html:
        # HTML 文件直接使用
        print("📄 检测到 HTML 文件，直接使用内容")
        html_content = content
        # 从 HTML 中提取标题或手动指定
        if args.title:
            title = args.title
        else:
            # 尝试从 h1 标签提取
            import re
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            if h1_match:
                # 去除 HTML 标签
                title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
            else:
                title = "未命名文章"
        theme_info = {"name": "自定义 HTML", "description": "直接使用 HTML 内容"}
        print(f"📝 标题: {title}")
        print(f"🔄 使用原始 HTML 内容")
    else:
        # Markdown 文件需要转换
        markdown_content = content
        
        # 提取标题
        title = "未命名文章"
        first_line = markdown_content.split('\n')[0]
        if first_line.startswith('# '):
            title = first_line[2:].strip()
        
        # 确定主题
        if args.theme:
            # 用户指定了主题
            if args.theme not in themes:
                print(f"❌ 未知主题: {args.theme}")
                print(f"可用主题: {', '.join(themes.keys())}")
                return False
            selected_theme = args.theme
            theme_info = themes[selected_theme]
            print(f"🎨 使用指定主题: {theme_info['name']}")
        else:
            # 自动推荐主题
            print("🤖 正在分析文章内容，推荐最佳主题...")
            recommended_theme, confidence, reason = ThemePresets.recommend_theme(markdown_content, title)
            selected_theme = recommended_theme
            theme_info = themes[selected_theme]
            print(f"🎨 推荐主题: {theme_info['name']} (置信度: {confidence:.0%})")
            print(f"   💡 {reason}")
        
        print(f"📝 标题: {title}")
        print(f"🔄 生成 HTML...")
        html_content = convert_markdown_to_wechat_html(markdown_content, theme=selected_theme)
    
    print("🚀 微信公众号文章推送 (V9 - 支持 HTML 直接推送)")
    print("=" * 60)
    if is_html:
        print(f"📄 模式: 直接推送 HTML")
    else:
        print(f"🎨 主题: {theme_info['name']}")
        print(f"   {theme_info['description']}")
    print("=" * 60)
    
    access_token = get_access_token()
    if not access_token:
        sys.exit(1)
    
    thumb_media_id = ""
    if args.cover and os.path.exists(args.cover):
        thumb_media_id = upload_thumb_image(access_token, args.cover) or ""
    
    print(f"📝 标题: {title}")
    
    if not is_html:
        print(f"🔄 生成 HTML...")
        html_content = convert_markdown_to_wechat_html(markdown_content, theme=selected_theme)
        # 生成摘要（仅 Markdown）
        plain_text = markdown_content.replace('#', '').replace('*', '').replace('`', '').replace('\n', ' ')
        digest = plain_text[:100] + "..." if len(plain_text) > 100 else plain_text
    else:
        # HTML 文件使用默认摘要
        digest = "HTML 文章"
    
    media_id = add_draft(
        access_token=access_token,
        title=title,
        content=html_content,
        thumb_media_id=thumb_media_id,
        author=args.author,
        digest=digest
    )
    
    if media_id:
        print("\n" + "=" * 60)
        print("🎉 文章推送成功！")
        print(f"📄 标题: {title}")
        print(f"🎨 主题: {theme_info['name']}")
        print(f"🆔 Media ID: {media_id}")
        print("\n✨ 排版特点：")
        print(f"   {theme_info['description']}")
        print("\n💡 提示：")
        print("   如需更换主题，可使用 --theme 参数指定")
        print(f"   示例: python3 push_draft.py --file {article_path} --theme fresh_lively")
        return True
    else:
        print("\n❌ 推送失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
