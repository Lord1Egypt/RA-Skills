# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#!/usr/bin/env python3
"""
微信公众号自动发布 - 主 CLI 入口
整合内容生成 + API 调用，支持多种触发方式

使用方式：
    python cli.py save-draft --topic "AI进展"  # AI 生成并保存
    python cli.py save-draft --content-file README.md  # 本地文件
    python cli.py save-draft --crawl-url "https://xxx.com"  # 爬虫伪原创
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 导入子模块
from wechat.api_client import WeChatMPClient, format_markdown_to_html
from wechat.content_generator import (
    generate_article_by_ai,
    read_local_markdown,
    crawl_and_rewrite,
    select_random_image,
    resolve_image_path
)


def interactive_prompt(prompt: str, options: list) -> str:
    """交互式选择（CLI 环境下模拟）"""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    
    while True:
        try:
            choice = input("\n请选择 (输入数字): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print("输入无效，请重新输入")


def main():
    parser = argparse.ArgumentParser(
        description="微信公众号自动发布工具 - 支持 AI 写作、本地文件、爬虫伪原创",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 1. AI 生成文章并保存到草稿箱
  python cli.py save-draft --topic "AI技术进展" --app-id "xxx" --app-secret "xxx"

  # 2. 使用本地 Markdown 文件
  python cli.py save-draft --content-file "article.md" --app-id "xxx" --app-secret "xxx"

  # 3. 爬虫伪原创后保存
  python cli.py save-draft --crawl-url "https://tech.sina.com.cn" --app-id "xxx" --app-secret "xxx"

  # 4. 指定配图目录
  python cli.py save-draft --topic "测试" --image-dir "E:/images" --app-id "xxx" --app-secret "xxx"

  # 5. 上传单独图片
  python cli.py upload-image --image-path "photo.jpg" --app-id "xxx" --app-secret "xxx"

  # 6. 获取 AccessToken
  python cli.py get-token --app-id "xxx" --app-secret "xxx"
        """
    )
    
    # 全局参数
    parser.add_argument("--app-id", help="公众号AppID，环境变量 WECHAT_APP_ID")
    parser.add_argument("--app-secret", help="公众号AppSecret，环境变量 WECHAT_APP_SECRET")
    parser.add_argument("--access-token", help="已获取的AccessToken（可选）")
    parser.add_argument("--config", help="配置文件路径(JSON)")
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # ========== save-draft 命令 ==========
    draft_parser = subparsers.add_parser("save-draft", help="保存文章到草稿箱")
    
    # 内容来源（互斥）
    content_group = draft_parser.add_mutually_exclusive_group(required=False)
    content_group.add_argument("--topic", help="AI生成文章的主题")
    content_group.add_argument("--content-file", help="本地Markdown文件路径")
    content_group.add_argument("--crawl-url", help="爬虫伪原创的目标URL")
    content_group.add_argument("--content", help="直接输入文章内容")
    
    # 文章参数
    draft_parser.add_argument("--title", help="文章标题（AI生成或文件时可自动提取）")
    draft_parser.add_argument("--author", help="作者名称")
    draft_parser.add_argument("--markdown", action="store_true", help="内容为Markdown格式")
    draft_parser.add_argument("--theme", default="简", help="排版主题（默认 简）")
    
    # 配图选项
    draft_parser.add_argument("--image-dir", help="本地图片目录（随机选图）")
    draft_parser.add_argument("--image-urls", nargs="*", help="网络图片URL列表")
    draft_parser.add_argument("--cover-image", help="封面图片路径")
    draft_parser.add_argument("--ai-generate-image", action="store_true", help="使用AI生成配图")
    draft_parser.add_argument("--image-mapping", help="图片路径映射JSON文件（可选）")
    
    # 输出选项
    draft_parser.add_argument("--output", help="输出文件路径（保存JSON结果）")
    draft_parser.add_argument("--dry-run", action="store_true", help="仅生成内容，不调用API")
    
    # ========== upload-image 命令 ==========
    img_parser = subparsers.add_parser("upload-image", help="上传文章图片")
    img_parser.add_argument("--image-path", help="图片文件路径")
    img_parser.add_argument("--image-url", help="网络图片URL")
    
    # ========== get-token 命令 ==========
    subparsers.add_parser("get-token", help="获取AccessToken")
    
    # ========== list-drafts 命令 ==========
    subparsers.add_parser("list-drafts", help="获取草稿箱列表")
    
    # ========== get-draft 命令 ==========
    get_draft_parser = subparsers.add_parser("get-draft", help="获取草稿详情")
    get_draft_parser.add_argument("--media-id", required=True, help="草稿media_id")
    
    # ========== delete-draft 命令 ==========
    delete_draft_parser = subparsers.add_parser("delete-draft", help="删除草稿")
    delete_draft_parser.add_argument("--media-id", required=True, help="草稿media_id")
    delete_draft_parser.add_argument("--confirm", action="store_true", help="确认删除")
    
    # ========== config 命令 ==========
    config_parser = subparsers.add_parser("config", help="交互式配置 AppID 和 AppSecret")
    config_parser.add_argument("--app-id", help="公众号AppID")
    config_parser.add_argument("--app-secret", help="公众号AppSecret")
    config_parser.add_argument("--output", default="config.json", help="配置文件路径（默认 config.json）")
    
    # ========== themes 命令 ==========
    subparsers.add_parser("themes", help="列出所有可用排版主题")
    
    args = parser.parse_args()
    
    # ======== 处理 themes 命令 ========
    if args.command == "themes":
        from wechat.theme import list_themes, THEMES
        print("\n🎨 可用排版主题：")
        for i, theme in enumerate(list_themes(), 1):
            print(f"  {i}. {theme}")
        return
    
    # ======== 处理 config 命令 ========
    if args.command == "config":
        print("\n" + "="*50)
        print("微信公众号自动发布工具 - 配置向导")
        print("="*50)
        
        # 获取 AppID
        if args.app_id:
            app_id = args.app_id
        else:
            app_id = input("\n请输入公众号 AppID: ").strip()
        
        # 获取 AppSecret
        if args.app_secret:
            app_secret = args.app_secret
        else:
            app_secret = input("请输入公众号 AppSecret: ").strip()
        
        if not app_id or not app_secret:
            print("\n❌ 配置失败：AppID 和 AppSecret 不能为空")
            sys.exit(1)
        
        # 保存配置
        config_data = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        config_path = args.output
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 配置已保存到: {config_path}")
        print("\n后续使用方式:")
        print(f"  python scripts/cli.py --config {config_path} save-draft --title '标题' --content '内容'")
        print("\n或者在命令中指定配置文件:")
        print(f"  python scripts/cli.py -c {config_path} get-token")
        return
    
    if not args.command:
        parser.print_help()
        return
    
    # ======== 加载配置 ========
    config = {}
    
    # 1. 从配置文件加载
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    
    # 2. 从环境变量覆盖
    config["app_id"] = args.app_id or os.environ.get("WECHAT_APP_ID") or config.get("app_id")
    config["app_secret"] = args.app_secret or os.environ.get("WECHAT_APP_SECRET") or config.get("app_secret")
    config["access_token"] = args.access_token or os.environ.get("WECHAT_ACCESS_TOKEN") or config.get("access_token")
    
    # 检查必要参数
    if args.command != "get-token" and not config.get("app_id") or not config.get("app_secret"):
        print("错误：缺少 AppID 或 AppSecret")
        print("可通过以下方式提供：")
        print("  1. 命令行: --app-id xxx --app-secret xxx")
        print("  2. 环境变量: WECHAT_APP_ID, WECHAT_APP_SECRET")
        print("  3. 配置文件: --config config.json")
        sys.exit(1)
    
    # ======== 执行命令 ========
    client = WeChatMPClient(config["app_id"], config["app_secret"])
    
    # 重置已有 token（如果提供）
    if config.get("access_token"):
        client._access_token = config["access_token"]
    
    if args.command == "get-token":
        result = client.get_access_token()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "upload-image":
        # 支持本地文件或网络URL
        print(f"Debug: args.image_path = {getattr(args, 'image_path', None)}")
        print(f"Debug: args.image_url = {getattr(args, 'image_url', None)}")
        
        image_path = getattr(args, 'image_path', None)
        image_url = getattr(args, 'image_url', None)
        
        if image_url:
            result = client.upload_article_image(image_url=image_url)
        else:
            result = client.upload_article_image(image_path=image_path)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "list-drafts":
        token_result = client.get_access_token()
        
        # 检查错误
        if token_result.get("errcode") is not None and token_result.get("errcode") != 0:
            print(json.dumps(token_result, ensure_ascii=False, indent=2))
            return
        
        if not token_result.get("access_token"):
            print(json.dumps(token_result, ensure_ascii=False, indent=2))
            return
        
        import requests
        url = f"https://api.weixin.qq.com/cgi-bin/draft/batchget"
        params = {"access_token": token_result["access_token"]}
        data = {"offset": 0, "count": 50}
        response = requests.post(url, params=params, json=data)
        result = response.json()
        
        if "item" in result:
            print(f"草稿数量: {result.get('total_count', 0)}")
            print("\n草稿列表:")
            for i, item in enumerate(result.get("item", []), 1):
                title = item.get("content", {}).get("news_item", [{}])[0].get("title", "无标题")
                media_id = item.get("media_id", "")
                print(f"  {i}. {title}")
                print(f"     media_id: {media_id}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "get-draft":
        token_result = client.get_access_token()
        
        # 检查错误
        if token_result.get("errcode") is not None and token_result.get("errcode") != 0:
            print(json.dumps(token_result, ensure_ascii=False, indent=2))
            return
        
        if not token_result.get("access_token"):
            print(json.dumps(token_result, ensure_ascii=False, indent=2))
            return
        
        import requests
        url = f"https://api.weixin.qq.com/cgi-bin/draft/get"
        params = {"access_token": token_result["access_token"]}
        data = {"media_id": args.media_id}
        response = requests.post(url, params=params, json=data)
        result = response.json()
        if "news_item" in result:
            item = result["news_item"][0]
            print(f"标题: {item.get('title')}")
            print(f"作者: {item.get('author')}")
            print(f"摘要: {item.get('digest')}")
            print(f"media_id: {args.media_id}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "delete-draft":
        if not args.confirm:
            print("⚠️ 确认删除草稿？请加上 --confirm 参数")
            print(f"  python scripts/cli.py delete-draft --media-id {args.media_id} --confirm")
            return
        
        token_result = client.get_access_token()
        
        # 检查错误
        if token_result.get("errcode") is not None and token_result.get("errcode") != 0:
            print(json.dumps(token_result, ensure_ascii=False, indent=2))
            return
        
        if not token_result.get("access_token"):
            print(json.dumps(token_result, ensure_ascii=False, indent=2))
            return
        
        import requests
        url = f"https://api.weixin.qq.com/cgi-bin/draft/delete"
        params = {"access_token": token_result["access_token"]}
        data = {"media_id": args.media_id}
        response = requests.post(url, params=params, json=data)
        result = response.json()
        if result.get("errcode") == 0:
            print(f"✅ 已删除草稿: {args.media_id}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "save-draft":
        # ======== 处理内容来源 ========
        article_data = {}
        
        if args.topic:
            # AI 生成
            print(f"\n🤖 正在生成文章，主题: {args.topic}")
            article_data = generate_article_by_ai(args.topic)
            
        elif args.content_file:
            # 本地文件
            print(f"\n📄 正在读取本地文件: {args.content_file}")
            
            # 加载 base_dir 配置
            base_dir = config.get("base_dir")
            if base_dir:
                print(f"📁 图片基础目录: {base_dir}")
            
            # 加载图片路径映射（兼容旧版）
            image_mapping = None
            if args.image_mapping and os.path.exists(args.image_mapping):
                with open(args.image_mapping, 'r', encoding='utf-8') as f:
                    image_mapping = json.load(f)
                print(f"📷 已加载图片路径映射: {len(image_mapping)} 条")
            
            article_data = read_local_markdown(args.content_file, image_mapping, base_dir)
            if "error" in article_data:
                print(f"错误: {article_data['error']}")
                sys.exit(1)
        
        elif args.crawl_url:
            # 爬虫伪原创
            print(f"\n🌐 正在抓取并伪原创: {args.crawl_url}")
            article_data = crawl_and_rewrite(args.crawl_url)
            if "error" in article_data:
                print(f"错误: {article_data['error']}")
                sys.exit(1)
            # 伪原创后使用重写后的内容
            article_data["content"] = article_data.pop("rewritten_content")
            article_data["title"] = article_data.pop("rewritten_title")
        
        elif args.content:
            # 直接输入内容
            article_data = {
                "title": args.title or "未命名文章",
                "content": args.content
            }
        
        else:
            # 无内容参数，交互式询问
            print("\n⚠️ 未指定内容来源，请选择：")
            choice = interactive_prompt("请选择文章来源：", [
                "AI 生成文章（给定主题）",
                "本地 Markdown 文件",
                "爬虫抓取 + 伪原创"
            ])
            
            if "AI" in choice:
                topic = input("请输入文章主题: ").strip()
                if topic:
                    article_data = generate_article_by_ai(topic)
            elif "本地" in choice:
                file_path = input("请输入文件路径: ").strip()
                if file_path:
                    article_data = read_local_markdown(file_path)
            elif "爬虫" in choice:
                url = input("请输入目标URL: ").strip()
                if url:
                    article_data = crawl_and_rewrite(url)
        
        if "error" in article_data:
            print(f"错误: {article_data['error']}")
            sys.exit(1)
        
        # 标题处理
        title = args.title or article_data.get("title", "未命名文章")
        content = article_data.get("content", "")
        
        print(f"\n📝 文章标题: {title}")
        
        # ======== 交互式选择主题 ========
        from wechat.theme import format_with_theme, list_themes, THEMES
        
        # 如果没有指定主题，交互式选择
        if not args.theme:
            print("\n🎨 请选择排版主题：")
            themes = list_themes()
            for i, theme in enumerate(themes, 1):
                print(f"  {i}. {theme}")
            
            while True:
                try:
                    choice = input("\n请输入序号或直接回车使用默认'简'主题: ").strip()
                    if not choice:
                        args.theme = "简"
                        break
                    idx = int(choice) - 1
                    if 0 <= idx < len(themes):
                        args.theme = themes[idx]
                        break
                except ValueError:
                    pass
                print("输入无效，请重新输入")
        else:
            print(f"🎨 使用主题: {args.theme}")
        
        # ======== 自动上传文章中的本地图片 ========
        import re
        
        # 提取 markdown 中的所有图片路径（兼容各种格式）
        # 匹配模式：](路径) 或 [](路径)，找E盘路径
        local_image_pattern = r'\]\((.*?E:.*?)\)'
        local_images = re.findall(local_image_pattern, content)
        
        print(f"Debug: 找到 {len(local_images)} 个图片路径")
        if local_images:
            print(f"Debug: 前3个图片路径: {local_images[:3]}")
        print(f"Debug: content前200字符: {content[:200]}")
        
        # 上传本地图片并替换为公众号URL
        image_url_mapping = {}  # 本地路径 -> 公众号URL
        
        if local_images and base_dir:
            print(f"\n🖼️ 检测到 {len(local_images)} 张本地图片，正在上传到公众号...")
            
            for img_path in local_images:
                # 解析为绝对路径
                full_path = resolve_image_path(img_path, base_dir)
                
                # 如果已上传过，跳过
                if full_path in image_url_mapping:
                    continue
                
                # 检查文件是否存在
                if not os.path.exists(full_path):
                    print(f"  ⚠️ 图片不存在，跳过: {full_path}")
                    continue
                
                # 上传到公众号
                print(f"  📤 上传图片: {os.path.basename(full_path)}")
                upload_result = client.upload_article_image(image_path=full_path)
                
                print(f"     Debug: upload_result = {upload_result}")
                
                # 成功判断：有 url 或者 errcode == 0
                if upload_result.get("url") or upload_result.get("errcode") == 0:
                    mp_url = upload_result.get("url")
                    image_url_mapping[full_path] = mp_url
                    print(f"     ✅ 获取到公众号图片URL: {mp_url[:50]}...")
                else:
                    print(f"     ❌ 上传失败: {upload_result}")
            # 替换 content 中的本地路径为公众号URL，并转换为HTML图片标签
            for local_path, mp_url in image_url_mapping.items():
                # 先替换 markdown 图片语法为 HTML img 标签（不带 > 符号）
                html_img = f'<img src="{mp_url}" style="max-width: 100%; height: auto; display: block; margin: 10px auto;"/>'
                content = content.replace(f"]({local_path})", html_img)
                content = content.replace(f"]({local_path.replace(chr(92), '/')})", html_img)
            
            print(f"✅ 图片上传完成，已替换 {len(image_url_mapping)} 张图片")
        
        image_urls = []  # 主题格式化不需要额外图片（文章内图片已在content中）
        
        if args.markdown:
            # 使用主题格式化
            html_content = format_with_theme(title, content, args.theme, image_urls)
        else:
            # 非Markdown内容也应用主题
            html_content = format_with_theme(title, content, args.theme, image_urls)
        
        # ======== 保存到草稿箱 ========
        if args.dry_run:
            print("\n🔍 [DRY-RUN] 仅展示内容，不调用API")
            print(f"标题: {title}")
            print(f"内容长度: {len(html_content)} 字符")
            print(f"图片数量: {len(image_urls)}")
        else:
            print("\n💾 正在保存到草稿箱...")
            result = client.save_draft(
                title=title,
                content=html_content,
                author=args.author,
                cover_image_path=args.cover_image
            )
            
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 成功判断：包含 media_id 或者 errcode == 0
            if result.get("media_id") or result.get("errcode") == 0:
                print(f"\n✅ 成功保存到草稿箱！media_id: {result.get('media_id')}")
            else:
                print(f"\n❌ 保存失败: {result.get('errmsg')}")
                sys.exit(1)
        
        # 保存输出
        if args.output:
            output_data = {
                "title": title,
                "content_length": len(html_content),
                "images": image_urls,
                "result": result if not args.dry_run else None
            }
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"\n📁 结果已保存到: {args.output}")


if __name__ == "__main__":
    main()