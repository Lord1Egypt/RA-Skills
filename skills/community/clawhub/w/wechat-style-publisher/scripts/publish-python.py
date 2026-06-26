#!/usr/bin/env python3
"""Publish themed draft articles to one or more WeChat Official Accounts."""

import argparse
import asyncio
import json
import os
import re
import time
from pathlib import Path

import httpx


THEMES = {
    "modern-minimal": """
.wechat-content { font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.wechat-content h1, .wechat-content h2, .wechat-content h3, .wechat-content h4, .wechat-content h5, .wechat-content h6 { margin-top: 30px; margin-bottom: 15px; font-weight: bold; color: #2b2b2b; }
.wechat-content h1 { font-size: 24px; padding-bottom: 8px; border-bottom: 1px solid #3eaf7c; }
.wechat-content h2 { font-size: 22px; padding: 8px 12px; background-color: #f8f8f8; color: #3eaf7c; }
.wechat-content h3 { font-size: 20px; padding-left: 10px; border-left: 2px solid #3eaf7c; }
.wechat-content p { margin: 15px 0; }
.wechat-content a { color: #3eaf7c; text-decoration: none; border-bottom: 1px solid #3eaf7c; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #f8f8f8; border-left: 3px solid #3eaf7c; color: #666; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #f5f5f5; border-radius: 3px; overflow-x: auto; border: 1px solid #e0e0e0; }
.wechat-content code { font-family: Consolas, monospace; font-size: 14px; background-color: #f0f0f0; padding: 2px 6px; border-radius: 3px; color: #d73a49; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 3px; }
""",
    "tech-future": """
.wechat-content { font-size: 16px; color: #1a202c; line-height: 1.75; letter-spacing: 0.05em; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%); }
.wechat-content h1 { font-size: 24px; padding: 15px 25px; background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 100%); color: #ffffff; border-radius: 8px; }
.wechat-content h2 { font-size: 22px; padding: 12px 20px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(6, 182, 212, 0.1) 100%); border-left: 5px solid #06b6d4; }
.wechat-content h3 { font-size: 20px; padding-left: 15px; border-left: 4px solid #06b6d4; }
.wechat-content p { margin: 15px 0; }
.wechat-content a { color: #0891b2; text-decoration: none; border-bottom: 2px solid #06b6d4; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); border-left: 5px solid #06b6d4; color: #475569; }
.wechat-content pre { margin: 20px 0; padding: 20px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #cbd5e1; border-radius: 8px; overflow-x: auto; }
.wechat-content code { font-family: Consolas, monospace; font-size: 14px; background: rgba(6, 182, 212, 0.1); padding: 3px 8px; border-radius: 4px; color: #0891b2; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; }
""",
    "warm-orange": """
.wechat-content { font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.wechat-content h1 { font-size: 24px; padding: 12px 20px; background-color: #ff6b35; color: #ffffff; }
.wechat-content h2 { font-size: 22px; padding: 10px 16px 10px 20px; background-color: #fff3ed; border-left: 4px solid #ff6b35; color: #ff6b35; }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 4px solid #ff6b35; }
.wechat-content p { margin: 15px 0; }
.wechat-content a { color: #ff6b35; text-decoration: none; border-bottom: 1px solid #ff6b35; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #fff3ed; border-left: 4px solid #ff6b35; color: #666; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2c2c2c; color: #abb2bf; border-radius: 5px; overflow-x: auto; }
.wechat-content code { font-family: Consolas, monospace; font-size: 14px; background-color: #fff3ed; padding: 2px 6px; border-radius: 3px; color: #ff6b35; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px; }
""",
    "fresh-green": """
.wechat-content { font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.wechat-content h1 { font-size: 24px; padding-bottom: 12px; border-bottom: 3px solid #42b983; text-align: center; }
.wechat-content h2 { font-size: 22px; padding: 10px 16px; background: linear-gradient(to right, #42b983 0%, #85d7b3 100%); color: #ffffff; border-radius: 4px; }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 4px solid #42b983; }
.wechat-content p { margin: 15px 0; }
.wechat-content a { color: #42b983; text-decoration: none; border-bottom: 1px solid #42b983; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #f0faf6; border-left: 4px solid #42b983; color: #666; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2c2c2c; color: #abb2bf; border-radius: 5px; overflow-x: auto; }
.wechat-content code { font-family: Consolas, monospace; font-size: 14px; background-color: #f0faf6; padding: 2px 6px; border-radius: 3px; color: #42b983; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px; }
""",
    "elegant-violet": """
.wechat-content { font-size: 16px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.05em; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.wechat-content h1 { font-size: 24px; padding-bottom: 12px; border-bottom: 3px solid #9b59b6; text-align: center; font-weight: 600; }
.wechat-content h2 { font-size: 22px; padding: 10px 16px; background: linear-gradient(135deg, #9b59b6 0%, #c39bd3 100%); color: #ffffff; border-radius: 4px; }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 4px solid #9b59b6; }
.wechat-content p { margin: 15px 0; }
.wechat-content a { color: #9b59b6; text-decoration: none; border-bottom: 1px solid #9b59b6; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background-color: #f8f5fb; border-left: 4px solid #9b59b6; color: #666; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2d2438; color: #c9a7d8; border-radius: 5px; overflow-x: auto; }
.wechat-content code { font-family: Consolas, monospace; font-size: 14px; background-color: #f8f5fb; padding: 2px 6px; border-radius: 3px; color: #9b59b6; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 5px; }
""",
    "chinese-style": """
.wechat-content { font-size: 16px; color: #2c2c2c; line-height: 1.8; letter-spacing: 0.05em; font-family: "STSong", "SimSun", "Songti SC", serif; }
.wechat-content h1 { font-size: 24px; padding: 16px 30px; background: linear-gradient(to bottom, #f5e6d3 0%, #efe0c8 50%, #f5e6d3 100%); color: #c8161d; text-align: center; letter-spacing: 0.15em; border-top: 2px solid #c8161d; border-bottom: 2px solid #c8161d; }
.wechat-content h2 { font-size: 22px; padding: 10px 20px; border-left: 4px solid #c8161d; color: #c8161d; background: linear-gradient(to right, rgba(200, 22, 29, 0.05) 0%, transparent 100%); }
.wechat-content h3 { font-size: 20px; padding-left: 12px; border-left: 3px solid #c8161d; }
.wechat-content p { margin: 15px 0; }
.wechat-content a { color: #c8161d; text-decoration: none; border-bottom: 1px solid #c8161d; }
.wechat-content blockquote { margin: 20px 0; padding: 15px 20px; background: linear-gradient(to right, #faf8f3 0%, #f5f0e8 100%); border-left: 4px solid #c8161d; border-right: 4px solid #c8161d; color: #666; }
.wechat-content pre { margin: 20px 0; padding: 15px; background-color: #2c2c2c; color: #abb2bf; border-radius: 3px; overflow-x: auto; border: 1px solid #c8161d; }
.wechat-content code { font-family: Consolas, monospace; font-size: 14px; background-color: #faf8f3; padding: 2px 6px; border-radius: 3px; color: #c8161d; }
.wechat-content img { max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 3px; }
""",
}


def load_json(path_str: str) -> dict:
    with open(path_str, "r", encoding="utf-8") as handle:
        return json.load(handle)


def read_optional_text(path_str: str) -> str:
    if not path_str:
        return ""
    with open(path_str, "r", encoding="utf-8") as handle:
        return handle.read()


def build_styled_content(html: str, theme: str, custom_css: str, intro_html: str, outro_html: str) -> str:
    theme_css = THEMES.get(theme)
    if not theme_css:
        raise ValueError(f"未知主题: {theme}")

    parts = [part for part in [intro_html, html, outro_html] if part]
    body = "\n".join(parts)
    css = "\n".join([theme_css, custom_css]).strip()
    return f'<style>{css}</style><div class="wechat-content">{body}</div>'


def strip_html(content: str) -> str:
    text = re.sub(r"<[^>]+>", " ", content)
    return re.sub(r"\s+", " ", text).strip()


def resolve_accounts(config: dict, account_arg: str, all_enabled: bool) -> list[str]:
    accounts = config.get("wechat", {}).get("accounts", {})
    if all_enabled:
        return [account_id for account_id, account in accounts.items() if account.get("enabled", True)]
    raw = account_arg or config.get("wechat", {}).get("defaultAccount", "default")
    return [item.strip() for item in raw.split(",") if item.strip()]


def resolve_publishing_config(config: dict, account: dict) -> dict:
    publishing = dict(config.get("publishing", {}))
    publishing.update(account.get("publishing", {}))
    return publishing


def load_template_variable(config_dir: Path, publishing: dict, template_name: str, registry_path: str) -> dict | None:
    if not template_name:
        return None
    registry_value = registry_path or publishing.get("templateVariablesFile", "")
    if not registry_value:
        raise ValueError("已指定模板变量名，但未配置 registry")
    resolved = (config_dir / registry_value).resolve()
    registry = json.loads(resolved.read_text(encoding="utf-8"))
    template = registry.get("templates", {}).get(template_name)
    if not template:
        raise ValueError(f"模板变量不存在: {template_name}")
    return template


class WeChatPublisher:
    def __init__(self, config: dict, account_id: str, config_dir: Path):
        self.config = config
        self.account_id = account_id
        self.config_dir = config_dir
        self.account = self.config["wechat"]["accounts"][account_id]
        self.base_url = self.config.get("wechat", {}).get("apiBaseUrl", "https://api.weixin.qq.com")
        token_cache_dir = self.config.get("wechat", {}).get("tokenCacheDir", "./.tokens")
        self.token_cache_dir = (config_dir / token_cache_dir).resolve()

    async def get_access_token(self) -> str:
        self.token_cache_dir.mkdir(parents=True, exist_ok=True)
        cache_file = self.token_cache_dir / f"token_cache_{re.sub(r'[^\\w\\u4e00-\\u9fff-]+', '_', self.account_id)}.json"
        if cache_file.exists():
            try:
                cache = json.loads(cache_file.read_text(encoding="utf-8"))
                if time.time() < cache["expires_at"] - 300:
                    return cache["access_token"]
            except Exception:
                pass

        params = {
            "grant_type": "client_credential",
            "appid": self.account["appId"],
            "secret": self.account["appSecret"],
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(f"{self.base_url}/cgi-bin/token", params=params)
            result = response.json()

        if "errcode" in result:
            raise RuntimeError(f"获取 Access Token 失败: {result['errcode']} - {result['errmsg']}")

        expires_at = time.time() + result["expires_in"]
        cache_file.write_text(json.dumps({"access_token": result["access_token"], "expires_at": expires_at}), encoding="utf-8")
        return result["access_token"]

    async def upload_image(self, access_token: str, image_path: str, is_thumb: bool = False) -> dict:
        resolved = Path(image_path).resolve()
        image_type = "thumb" if is_thumb else "image"
        url = f"{self.base_url}/cgi-bin/material/add_material?access_token={access_token}&type={image_type}"
        mime_type = "image/jpeg" if resolved.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
        async with httpx.AsyncClient(timeout=60) as client:
            with open(resolved, "rb") as file_handle:
                response = await client.post(url, files={"media": (resolved.name, file_handle, mime_type)})
                result = response.json()

        if result.get("errcode", 0) not in [0, None]:
            raise RuntimeError(f"上传图片失败: {result['errcode']} - {result['errmsg']}")
        return result

    async def process_content_images(self, access_token: str, content: str, content_dir: Path) -> str:
        processed = content
        matches = re.findall(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', content, flags=re.IGNORECASE)
        for src in matches:
            if src.startswith(("http://", "https://", "data:")):
                continue
            image_path = Path(src)
            if not image_path.is_absolute():
                image_path = (content_dir / src).resolve()
            uploaded = await self.upload_image(access_token, str(image_path), is_thumb=False)
            if uploaded.get("url"):
                processed = processed.replace(f'src="{src}"', f'src="{uploaded["url"]}"')
                processed = processed.replace(f"src='{src}'", f"src='{uploaded['url']}'")
        return processed

    async def create_draft(self, access_token: str, title: str, content: str, thumb_media_id: str) -> str:
        publishing = resolve_publishing_config(self.config, self.account)
        digest_base = strip_html(content)[:120].strip()
        digest_suffix = self.account.get("digestSuffix", "")
        digest = f"{digest_base} {digest_suffix}".strip()
        article = {
            "title": title,
            "author": self.account.get("author", "OpenClaw"),
            "digest": digest,
            "content": content,
            "content_source_url": "",
            "thumb_media_id": thumb_media_id,
            "need_open_comment": publishing.get("needOpenComment", 1),
            "only_fans_can_comment": publishing.get("onlyFansCanComment", 0),
            "show_cover_pic": 1 if thumb_media_id and publishing.get("showCoverPic", True) else 0,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.base_url}/cgi-bin/draft/add?access_token={access_token}",
                json={"articles": [article]},
            )
            result = response.json()

        if result.get("errcode", 0) not in [0, None]:
            raise RuntimeError(f"创建草稿失败: {result['errcode']} - {result['errmsg']}")
        return result["media_id"]


async def publish_account(args, config: dict, config_dir: Path, account_id: str, html: str, intro_html: str, outro_html: str, custom_css: str) -> dict:
    publisher = WeChatPublisher(config, account_id, config_dir)
    access_token = await publisher.get_access_token()
    publishing = resolve_publishing_config(config, publisher.account)
    styled_html = build_styled_content(
        html=html,
        theme=args.theme or publishing.get("defaultTheme", "modern-minimal"),
        custom_css=custom_css,
        intro_html=intro_html,
        outro_html=outro_html,
    )
    content_dir = Path(args.content_dir).resolve() if args.content_dir else Path(args.content_file).resolve().parent
    processed_html = await publisher.process_content_images(access_token, styled_html, content_dir)
    thumb_media_id = ""
    if args.thumb:
        thumb = await publisher.upload_image(access_token, args.thumb, is_thumb=False)
        thumb_media_id = thumb["media_id"]
    media_id = await publisher.create_draft(access_token, args.title, processed_html, thumb_media_id)
    return {
        "accountId": account_id,
        "accountName": publisher.account.get("name", account_id),
        "mediaId": media_id,
    }


async def async_main():
    parser = argparse.ArgumentParser(description="多账号微信公众号文章发布")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--content-file", help="HTML 内容文件")
    parser.add_argument("--content", help="直接传入 HTML 内容")
    parser.add_argument("--account", default="", help="单个账号 ID")
    parser.add_argument("--accounts", default="", help="多个账号 ID，逗号分隔")
    parser.add_argument("--all-enabled", action="store_true", help="发布到所有启用的账号")
    parser.add_argument("--thumb", default="", help="封面图路径")
    parser.add_argument("--theme", default="", help="主题名称")
    parser.add_argument("--css-file", default="", help="自定义 CSS 文件")
    parser.add_argument("--template-name", default="", help="模板变量名")
    parser.add_argument("--registry", default="", help="模板变量仓库 JSON")
    parser.add_argument("--intro-template", default="", help="前导模板路径")
    parser.add_argument("--outro-template", default="", help="后导模板路径")
    parser.add_argument("--content-dir", default="", help="正文图片基础目录")
    args = parser.parse_args()

    if not args.content_file and not args.content:
        raise ValueError("必须提供 --content-file 或 --content")

    config_path = Path(args.config).resolve()
    config_dir = config_path.parent
    config = load_json(str(config_path))
    html = read_optional_text(args.content_file) if args.content_file else args.content
    requested_accounts = args.accounts or args.account
    account_ids = resolve_accounts(config, requested_accounts, args.all_enabled)

    results = []
    for account_id in account_ids:
        account = config.get("wechat", {}).get("accounts", {}).get(account_id, {})
        publishing = resolve_publishing_config(config, account)
        template_variable = load_template_variable(config_dir, publishing, args.template_name, args.registry)
        intro_template = args.intro_template or publishing.get("introTemplate", "")
        outro_template = args.outro_template or publishing.get("outroTemplate", "")
        css_file = args.css_file or publishing.get("customCssFile", "")
        intro_html = template_variable.get("introHtml", "") if template_variable else ""
        outro_html = template_variable.get("outroHtml", "") if template_variable else ""
        if not intro_html and intro_template:
            intro_html = read_optional_text(str((config_dir / intro_template).resolve()))
        if not outro_html and outro_template:
            outro_html = read_optional_text(str((config_dir / outro_template).resolve()))
        custom_css = template_variable.get("customCss", "") if template_variable else ""
        if not custom_css and css_file:
            custom_css = read_optional_text(str((config_dir / css_file).resolve()))
        result = await publish_account(args, config, config_dir, account_id, html, intro_html, outro_html, custom_css)
        results.append(result)
        print(f"{result['accountId']}\t{result['accountName']}\t{result['mediaId']}")


if __name__ == "__main__":
    asyncio.run(async_main())
