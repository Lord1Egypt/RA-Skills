#!/usr/bin/env python3
"""发布文章到微信公众号 - 支持 Markdown 和 HTML 两种输入格式"""

import sys
import os
import json
import asyncio
import httpx
import time
import re
from typing import Optional


# ============================================================
# Markdown → 微信 HTML 转换器
# ============================================================

def markdown_to_wechat_html(md_text: str) -> str:
    """
    将 Markdown 文本转换为微信公众号友好的 HTML。
    
    支持的 Markdown 语法：
    - 标题 (# ~ ######)
    - 加粗 (**text**)
    - 斜理 (*text*)
    - 删除线 (~~text~~)
    - 图片 (![alt](url))
    - 链接 ([text](url))
    - 无序列表 (- / * )
    - 有序列表 (1. 2. ...)
    - 引用 (> text)
    - 表格
    - 分割线 (--- / ***)
    - 代码块 (```code```)
    - 行内代码 (`code`)
    - 普通段落
    """
    lines = md_text.split('\n')
    html_parts = []
    i = 0
    in_code_block = False
    code_block_lang = ''
    code_lines = []
    in_table = False
    table_rows = []

    def inline_convert(text: str) -> str:
        """行内元素转换：加粗、斜体、删除线、链接、行内代码"""
        # 行内代码 `<code>`
        text = re.sub(r'`([^`]+)`', r'<code style="background:#f5f5f5;padding:2px 6px;border-radius:3px;font-size:0.9em;color:#e74c3c;">\1</code>', text)
        # 加粗 **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # 斜体 *text*
        text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
        # 删除线 ~~text~~
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        # 链接 [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:#576b95;text-decoration:none;">\1</a>', text)
        return text

    def flush_table():
        """将收集的表格行转为 HTML 表格"""
        nonlocal table_rows
        if not table_rows:
            return
        html_parts.append('<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;">')
        for ri, row in enumerate(table_rows):
            cells = [c.strip() for c in row.split('|')]
            # 去掉首尾空单元格（由 | 分隔产生的）
            cells = [c for c in cells if c != '']
            tag = 'th' if ri == 0 else 'td'
            style = 'border:1px solid #ddd;padding:8px 12px;text-align:left;'
            if ri == 0:
                style += 'background:#f8f8f8;font-weight:bold;'
            html_parts.append('<tr>')
            for cell in cells:
                cell = inline_convert(cell)
                html_parts.append(f'<{tag} style="{style}">{cell}</{tag}>')
            html_parts.append('</tr>')
        html_parts.append('</table>')
        table_rows = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # --- 代码块 ---
        if stripped.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_lang = stripped[3:].strip()
                code_lines = []
                i += 1
                continue
            else:
                # 结束代码块
                in_code_block = False
                code_content = '\n'.join(code_lines)
                code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_parts.append(
                    f'<pre style="background:#f6f8fa;padding:16px;border-radius:6px;'
                    f'overflow-x:auto;font-size:13px;line-height:1.5;margin:16px 0;'
                    f'border:1px solid #e1e4e8;"><code>{code_content}</code></pre>'
                )
                i += 1
                continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # --- 表格行 ---
        if '|' in stripped and stripped.startswith('|') and stripped.endswith('|'):
            # 跳过表格分隔行 |---|---|
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                in_table = True
                i += 1
                continue
            table_rows.append(stripped)
            in_table = True
            i += 1
            continue
        else:
            if table_rows:
                flush_table()
                in_table = False

        # --- 空行 ---
        if stripped == '':
            i += 1
            continue

        # --- 分割线 ---
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            html_parts.append('<hr style="border:none;border-top:1px solid #eee;margin:24px 0;">')
            i += 1
            continue

        # --- 标题 ---
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = inline_convert(heading_match.group(2).strip())
            # 根据级别设置不同字号
            font_sizes = {1: '22px', 2: '20px', 3: '18px', 4: '16px', 5: '15px', 6: '14px'}
            # h1 用分割线装饰，h2 用左边框装饰
            if level == 1:
                html_parts.append(
                    f'<h1 style="font-size:{font_sizes[level]};font-weight:bold;'
                    f'margin:28px 0 16px;color:#1a1a1a;text-align:center;'
                    f'border-bottom:2px solid #576b95;padding-bottom:12px;">{heading_text}</h1>'
                )
            elif level == 2:
                html_parts.append(
                    f'<h2 style="font-size:{font_sizes[level]};font-weight:bold;'
                    f'margin:24px 0 12px;color:#333;'
                    f'border-left:4px solid #576b95;padding-left:12px;">{heading_text}</h2>'
                )
            else:
                html_parts.append(
                    f'<h{level} style="font-size:{font_sizes.get(level, "14px")};font-weight:bold;'
                    f'margin:20px 0 10px;color:#333;">{heading_text}</h{level}>'
                )
            i += 1
            continue

        # --- 引用 ---
        if stripped.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = '<br>'.join(inline_convert(q) for q in quote_lines)
            html_parts.append(
                f'<blockquote style="border-left:4px solid #ddd;padding:12px 16px;'
                f'margin:16px 0;background:#f9f9f9;color:#666;border-radius:0 4px 4px 0;">'
                f'{quote_text}</blockquote>'
            )
            continue

        # --- 图片 ---
        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', stripped)
        if img_match:
            alt = img_match.group(1)
            url = img_match.group(2)
            html_parts.append(
                f'<img src="{url}" alt="{alt}" '
                f'style="width:100%;margin:16px 0;display:block;border-radius:4px;" />'
            )
            i += 1
            continue

        # --- 无序列表 ---
        if re.match(r'^[\-\*]\s+', stripped):
            html_parts.append('<ul style="margin:12px 0;padding-left:20px;">')
            while i < len(lines) and re.match(r'^[\-\*]\s+', lines[i].strip()):
                item_text = re.sub(r'^[\-\*]\s+', '', lines[i].strip())
                item_text = inline_convert(item_text)
                html_parts.append(f'<li style="margin:6px 0;line-height:1.8;">{item_text}</li>')
                i += 1
            html_parts.append('</ul>')
            continue

        # --- 有序列表 ---
        if re.match(r'^\d+\.\s+', stripped):
            html_parts.append('<ol style="margin:12px 0;padding-left:20px;">')
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i].strip()):
                item_text = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                item_text = inline_convert(item_text)
                html_parts.append(f'<li style="margin:6px 0;line-height:1.8;">{item_text}</li>')
                i += 1
            html_parts.append('</ol>')
            continue

        # --- 普通段落（连续非空行合并为一个段落）---
        para_lines = [stripped]
        i += 1
        # 吞掉后续空行前的连续文本行
        while i < len(lines):
            next_stripped = lines[i].strip()
            if next_stripped == '':
                break
            # 遇到特殊语法则停止
            if (next_stripped.startswith('#') or
                next_stripped.startswith('>') or
                next_stripped.startswith('```') or
                re.match(r'^!\[', next_stripped) or
                re.match(r'^[\-\*]\s+', next_stripped) or
                re.match(r'^\d+\.\s+', next_stripped) or
                re.match(r'^(-{3,}|\*{3,}|_{3,})$', next_stripped) or
                (next_stripped.startswith('|') and next_stripped.endswith('|'))):
                break
            para_lines.append(next_stripped)
            i += 1

        para_text = ' '.join(para_lines)
        para_text = inline_convert(para_text)
        html_parts.append(
            f'<p style="margin:14px 0;line-height:1.9;color:#333;font-size:15px;">{para_text}</p>'
        )
        continue

    # 收尾：刷新未关闭的表格
    flush_table()

    # 用 section 包裹
    body = '\n'.join(html_parts)
    return f'<section class="article-content" style="padding:0 4px;">\n{body}\n</section>'


# ============================================================
# 微信 API 客户端
# ============================================================

class WeChatAPI:
    def __init__(self, config_path='config.json'):
        self.config = self._load_config(config_path)
        self.access_token = None
        self.token_expiry = 0

    def _load_config(self, config_path):
        """加载配置文件"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"配置文件 {config_path} 不存在！\n"
                f"请创建配置文件并填写 AppID 和 AppSecret"
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 兼容旧版配置
        if 'accounts' not in config.get('wechat', {}):
            print("⚠️  检测到旧版配置格式")
            wechat_config = config['wechat']
            app_id = wechat_config['appId']
            app_secret = wechat_config['appSecret']

            config['wechat'] = {
                'defaultAccount': 'default',
                'accounts': {
                    'default': {
                        'name': '默认账号',
                        'appId': app_id,
                        'appSecret': app_secret,
                        'type': 'subscription',
                        'enabled': True
                    }
                },
                'apiBaseUrl': wechat_config.get('apiBaseUrl', 'https://api.weixin.qq.com'),
                'tokenCacheDir': './.tokens'
            }

        return config

    def _get_account_config(self):
        """获取当前账号配置"""
        wechat_config = self.config.get('wechat', {})
        default_account = wechat_config.get('defaultAccount', 'default')
        accounts = wechat_config.get('accounts', {})

        if default_account not in accounts:
            raise ValueError(f"默认账号 {default_account} 不存在")

        return accounts[default_account], wechat_config.get('apiBaseUrl', 'https://api.weixin.qq.com')

    async def get_access_token(self) -> str:
        """获取 Access Token（带缓存）"""
        if self.access_token and time.time() < self.token_expiry:
            return self.access_token

        account_config = self._get_account_config()[0]
        cache_dir = self.config['wechat'].get('tokenCacheDir', './.tokens')
        cache_file = os.path.join(cache_dir, f"token_cache.json")

        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
                    if time.time() < cache['expires_at'] - 300:
                        self.access_token = cache['access_token']
                        self.token_expiry = cache['expires_at']
                        return self.access_token
            except Exception as e:
                print(f"⚠️  加载 token 缓存失败: {e}")

        account, base_url = self._get_account_config()
        url = f"{base_url}/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': account['appId'],
            'secret': account['appSecret']
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, params=params)
            result = response.json()

        if 'errcode' in result:
            raise Exception(f"获取 Access Token 失败: {result['errcode']} - {result['errmsg']}")

        self.access_token = result['access_token']
        self.token_expiry = time.time() + result['expires_in']

        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump({
                'access_token': self.access_token,
                'expires_at': self.token_expiry
            }, f)

        print(f"✅ Access Token 获取成功")
        return self.access_token

    async def upload_image(self, image_path: str, is_thumb: bool = False) -> dict:
        """
        上传图片素材

        Args:
            image_path: 图片文件路径
            is_thumb: True=封面图(type=thumb), False=正文图片(type=image)

        Returns:
            dict: { 'media_id': 'xxx', 'url': 'https://...' }
        """
        access_token = await self.get_access_token()
        base_url = self._get_account_config()[1]
        image_type = 'thumb' if is_thumb else 'image'
        url = f"{base_url}/cgi-bin/material/add_material?access_token={access_token}&type={image_type}"

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")

        file_size = os.path.getsize(image_path)
        size_limit = 64 * 1024 * 1024 if is_thumb else 2 * 1024 * 1024
        if file_size > size_limit:
            size_mb = size_limit / 1024 / 1024
            raise Exception(f"图片大小超过 {size_mb}MB 限制: {file_size / 1024 / 1024:.2f}MB")

        allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        if is_thumb:
            allowed_extensions = ['.jpg', '.jpeg', '.png']
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in allowed_extensions:
            raise Exception(f"不支持的图片格式: {file_ext}，支持的格式: {', '.join(allowed_extensions)}")

        image_type_name = "封面图" if is_thumb else "正文图片"
        print(f"📤 正在上传{image_type_name}: {os.path.basename(image_path)} ({file_size / 1024:.2f}KB)")

        async with httpx.AsyncClient(timeout=60) as client:
            with open(image_path, 'rb') as f:
                mime_type = 'image/jpeg' if file_ext in ['.jpg', '.jpeg'] else 'image/png'
                files = {
                    'media': (os.path.basename(image_path), f, mime_type)
                }
                response = await client.post(url, files=files)
                result = response.json()

        if 'errcode' in result and result['errcode'] != 0:
            raise Exception(f"上传{image_type_name}失败: {result['errcode']} - {result['errmsg']}")

        media_info = {
            'media_id': result['media_id'],
            'url': result.get('url', '')
        }

        print(f"✅ {image_type_name}上传成功")
        if result.get('url'):
            print(f"   URL: {result['url']}")
        return media_info

    async def _download_url_to_temp(self, url: str) -> str:
        """下载外部图片到临时文件，返回临时文件路径"""
        import tempfile
        # 根据 URL 推断扩展名
        url_lower = url.lower().split('?')[0]  # 去掉查询参数
        if url_lower.endswith('.png'):
            ext = '.png'
        elif url_lower.endswith('.gif'):
            ext = '.gif'
        elif url_lower.endswith('.bmp'):
            ext = '.bmp'
        else:
            ext = '.jpg'  # 默认 jpg

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext, prefix='wechat_img_')
        tmp_path = tmp.name
        tmp.close()

        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            with open(tmp_path, 'wb') as f:
                f.write(resp.read())

        return tmp_path

    async def process_content_images(self, content: str, base_dir: str = '.') -> tuple:
        """
        处理内容中的所有图片（本地路径 + 外部URL），上传到微信并替换 src

        Args:
            content: HTML 内容
            base_dir: 图片路径的基础目录

        Returns:
            tuple: (处理后的 HTML 内容, 上传的图片信息映射)
        """
        img_pattern = r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(img_pattern, content, re.IGNORECASE)

        if not matches:
            print("✓ 未检测到图片，跳过上传")
            return content, {}

        print(f"\n📷 检测到 {len(matches)} 张图片，开始处理...\n")

        uploaded_images = {}
        processed_content = content

        image_counter = 1
        for src in matches:
            is_url = src.startswith(('http://', 'https://'))
            temp_path = None

            try:
                if is_url:
                    # 外部 URL：先下载到临时文件
                    print(f"  [{image_counter}] {src[:60]}... - 外部URL，正在下载...")
                    temp_path = await self._download_url_to_temp(src)
                    image_path = temp_path
                    display_name = src.split('/')[-1].split('?')[0] or f'url_image_{image_counter}'
                else:
                    # 本地路径
                    if os.path.isabs(src):
                        image_path = src
                    else:
                        image_path = os.path.join(base_dir, src)
                    display_name = os.path.basename(src)

                # 上传到微信
                result = await self.upload_image(image_path, is_thumb=False)

                if result.get('url'):
                    processed_content = processed_content.replace(f'src="{src}"', f'src="{result["url"]}"')
                    processed_content = processed_content.replace(f"src='{src}'", f"src='{result['url']}'")
                    uploaded_images[display_name] = result
                    print(f"  [{image_counter}] {display_name} - ✅ 已替换为微信 URL")
                else:
                    print(f"  [{image_counter}] {display_name} - ⚠️ 未返回 URL，保留原始路径")

            except Exception as e:
                print(f"  [{image_counter}] {src[:60]}... - ❌ 处理失败: {e}")

            finally:
                # 清理临时文件
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.unlink(temp_path)
                    except Exception:
                        pass

            image_counter += 1

        print(f"\n✓ 图片处理完成，成功上传 {len(uploaded_images)}/{len(matches)} 张\n")
        return processed_content, uploaded_images

    async def create_draft(self, title: str, content: str, thumb_media_id: str = "", author: str = "作者") -> str:
        """创建草稿"""
        access_token = await self.get_access_token()
        base_url = self._get_account_config()[1]
        url = f"{base_url}/cgi-bin/draft/add?access_token={access_token}"

        plain_text = re.sub(r'<[^>]+>', '', content)
        digest = plain_text[:120].strip()

        article = {
            'title': title,
            'author': author,
            'digest': digest,
            'content': content,
            'content_source_url': '',
            'need_open_comment': 1,
            'only_fans_can_comment': 0
        }

        # 只有提供了封面图才设置 thumb_media_id
        if thumb_media_id:
            article['thumb_media_id'] = thumb_media_id
            article['show_cover_pic'] = 1
        else:
            article['show_cover_pic'] = 0

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json={'articles': [article]})
            result = response.json()

        if 'errcode' in result and result['errcode'] != 0:
            raise Exception(f"创建草稿失败: {result['errcode']} - {result['errmsg']}")

        return result['media_id']


# ============================================================
# 主函数
# ============================================================

async def main(title: str, content: str, config_path: str = 'config.json',
               thumb_image_path: str = "", content_base_dir: str = ".",
               author: str = "作者"):
    """主函数"""
    print("🚀 开始发布公众号文章...\n")

    try:
        api = WeChatAPI(config_path)

        account, _ = api._get_account_config()
        print(f"📱 使用账号: {account['name']}\n")

        print(f"📝 文章标题: {title}")
        print(f"📊 文章长度: {len(content)} 字符\n")

        # 上传封面图片
        thumb_media_id = ""
        if thumb_image_path:
            print("📷 处理封面图片...")
            thumb_result = await api.upload_image(thumb_image_path, is_thumb=True)
            thumb_media_id = thumb_result['media_id']
            print()
        else:
            print("⚠️  未提供封面图，微信草稿 API 要求必须有封面图")
            print("💡 请使用 --thumb 参数指定封面图片路径\n")
            sys.exit(1)

        # 处理正文图片
        processed_content, uploaded_images = await api.process_content_images(content, content_base_dir)

        # 创建草稿
        media_id = await api.create_draft(title, processed_content, thumb_media_id, author)

        print(f"✅ 草稿创建成功！")
        print(f"   草稿 ID: {media_id}")
        print(f"   上传封面: {'是' if thumb_media_id else '否'}")
        print(f"   上传正文图: {len(uploaded_images)} 张")
        print(f"   请登录微信公众号后台查看: https://mp.weixin.qq.com/\n")

        return media_id

    except FileNotFoundError as e:
        print(f"\n❌ {e}\n")
        print("💡 提示:")
        print("   1. 请确保已创建 config.json 配置文件")
        print("   2. 参考 config.example.json 模板\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ 发布失败: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='发布文章到微信公众号（支持 Markdown 和 HTML 格式）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
使用示例:
  # 从 Markdown 文件发布
  python publish_article.py "文章标题" article.md --from-md --thumb cover.jpg

  # 从 HTML 文件发布
  python publish_article.py "文章标题" article.html --from-file --thumb cover.jpg

  # 直接传入 Markdown 内容发布
  python publish_article.py "文章标题" "# Hello **World**" --from-md

  # 指定图片目录和作者
  python publish_article.py "标题" article.md --from-md --thumb cover.jpg --content-dir ./images --author "张三"
        """
    )
    parser.add_argument('title', help='文章标题')
    parser.add_argument('content', help='内容（HTML/Markdown 字符串，或文件路径）')
    parser.add_argument('--config', default='config.json', help='配置文件路径 (默认: config.json)')
    parser.add_argument('--thumb', help='封面图片路径')
    parser.add_argument('--content-dir', default='.', help='正文图片的基础目录 (默认: 当前目录)')
    parser.add_argument('--from-file', action='store_true', help='从 HTML 文件读取内容')
    parser.add_argument('--from-md', action='store_true', help='从 Markdown 文件/字符串转换并发布（自动处理所有图片）')
    parser.add_argument('--author', default='作者', help='文章作者 (默认: 作者)')

    args = parser.parse_args()

    # 读取内容
    if args.from_md:
        # Markdown 模式：从文件读取或直接使用字符串
        if os.path.isfile(args.content):
            print(f"📄 读取 Markdown 文件: {args.content}")
            with open(args.content, 'r', encoding='utf-8') as f:
                md_content = f.read()
            # 自动将 content-dir 设为 md 文件所在目录
            if args.content_dir == '.':
                args.content_dir = os.path.dirname(os.path.abspath(args.content))
        else:
            md_content = args.content

        print("🔄 正在将 Markdown 转换为微信 HTML...")
        content = markdown_to_wechat_html(md_content)
        print(f"✅ 转换完成！HTML 长度: {len(content)} 字符\n")

    elif args.from_file:
        with open(args.content, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = args.content

    asyncio.run(main(args.title, content, args.config, args.thumb, args.content_dir, args.author))
