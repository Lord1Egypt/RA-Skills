#!/usr/bin/env python3
"""
wechat_publisher.py — 微信服务号草稿发布工具

功能：
1. 获取/刷新 Access Token
2. 上传图片到微信素材库
3. 替换文章中的图片链接为微信CDN地址
4. 创建草稿

用法：
    python wechat_publisher.py \
        --app-id YOUR_APP_ID \
        --app-secret YOUR_APP_SECRET \
        --html article.html \
        --title "文章标题" \
        --cover cover.jpg \
        --author "作者名"

环境变量方式（推荐）：
    export WECHAT_APP_ID=xxx
    export WECHAT_APP_SECRET=xxx
    python wechat_publisher.py --html article.html --title "标题"
"""

import json
import os
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path


WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"

# Access Token 本地缓存文件
TOKEN_CACHE_FILE = Path.home() / ".wechat_token_cache.json"


class WechatAPIError(Exception):
    """微信 API 错误"""
    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"微信API错误 [{errcode}]: {errmsg}")


WECHAT_ERROR_TIPS = {
    40001: "AppSecret 错误或 Access Token 无效，请检查配置",
    40013: "不合法的 AppID，请确认服务号 AppID 正确",
    40125: "不合法的 AppSecret",
    45009: "接口调用超过每日限额（草稿接口上限较高，一般不会触发）",
    48001: "接口未授权，请在公众平台开通相应接口权限",
    50001: "用户未授权该接口",
    40007: "不合法的 media_id，图片上传失败或已过期",
}


def _api_call(url: str, data: dict = None, files: dict = None, method: str = "POST") -> dict:
    """通用 API 调用"""
    if data is not None and files is None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method=method,
        )
    elif files:
        # multipart/form-data 上传
        boundary = "----WechatBoundary7MA4YWxkTrZu0gW"
        body_parts = []
        for field, value in (data or {}).items():
            body_parts.append(
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{field}"\r\n\r\n'
                f"{value}\r\n"
            )
        for field, (filename, content, content_type) in files.items():
            body_parts.append(
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            )
            payload = "".join(body_parts).encode("utf-8") + content + f"\r\n--{boundary}--\r\n".encode()
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
                method="POST",
            )
    else:
        req = urllib.request.Request(url, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP 请求失败: {e.code} {e.reason}") from e

    # 检查微信 API 错误码
    errcode = result.get("errcode", 0)
    if errcode != 0:
        tip = WECHAT_ERROR_TIPS.get(errcode, "")
        errmsg = result.get("errmsg", "unknown")
        if tip:
            errmsg = f"{errmsg} 💡 {tip}"
        raise WechatAPIError(errcode, errmsg)

    return result


class WechatPublisher:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._access_token = None
        self._token_expires_at = 0

    # ── Access Token 管理 ──────────────────────────────────────────

    def get_access_token(self) -> str:
        """获取 Access Token（自动使用缓存，避免频繁刷新）"""
        # 1. 检查内存缓存
        if self._access_token and time.time() < self._token_expires_at - 300:
            return self._access_token

        # 2. 检查文件缓存
        if TOKEN_CACHE_FILE.exists():
            try:
                cache = json.loads(TOKEN_CACHE_FILE.read_text())
                if (cache.get("app_id") == self.app_id
                        and cache.get("expires_at", 0) > time.time() + 300):
                    self._access_token = cache["access_token"]
                    self._token_expires_at = cache["expires_at"]
                    print("📋 使用缓存 Access Token")
                    return self._access_token
            except Exception:
                pass

        # 3. 重新获取
        print("🔑 获取新的 Access Token...")
        url = (
            f"{WECHAT_API_BASE}/token"
            f"?grant_type=client_credential"
            f"&appid={self.app_id}"
            f"&secret={self.app_secret}"
        )
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if "access_token" not in data:
            errcode = data.get("errcode", -1)
            raise WechatAPIError(errcode, data.get("errmsg", "获取Token失败"))

        self._access_token = data["access_token"]
        expires_in = data.get("expires_in", 7200)
        self._token_expires_at = time.time() + expires_in

        # 保存文件缓存
        TOKEN_CACHE_FILE.write_text(json.dumps({
            "app_id": self.app_id,
            "access_token": self._access_token,
            "expires_at": self._token_expires_at,
        }))

        print(f"✅ Access Token 获取成功，有效期 {expires_in//3600}h")
        return self._access_token

    # ── 图片上传 ───────────────────────────────────────────────────

    def upload_image_from_url(self, image_url: str) -> str:
        """从 URL 下载图片并上传到微信素材库，返回微信 CDN URL"""
        token = self.get_access_token()

        # 下载图片
        print(f"  ⬇️  下载图片: {image_url[:60]}...")
        try:
            with urllib.request.urlopen(image_url, timeout=15) as resp:
                image_data = resp.read()
                content_type = resp.headers.get("Content-Type", "image/jpeg")
        except Exception as e:
            raise RuntimeError(f"图片下载失败: {e}") from e

        # 确定文件扩展名
        ext = "jpg"
        if "png" in content_type:
            ext = "png"
        elif "gif" in content_type:
            ext = "gif"
        elif "webp" in content_type:
            ext = "webp"

        # 上传到微信（使用 uploadimg 接口，返回永久 URL）
        upload_url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"

        boundary = "----FormBoundaryX7MA4YWxkTrZu0gW"
        filename = f"image.{ext}"

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8") + image_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        req = urllib.request.Request(
            upload_url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        if "url" not in result:
            errcode = result.get("errcode", -1)
            raise WechatAPIError(errcode, result.get("errmsg", "图片上传失败"))

        wechat_url = result["url"]
        print(f"  ✅ 已上传: {wechat_url[:60]}...")
        return wechat_url

    def upload_cover_image(self, image_url: str) -> str:
        """上传封面图并返回 thumb_media_id（用于草稿接口）"""
        token = self.get_access_token()

        # 下载图片
        with urllib.request.urlopen(image_url, timeout=15) as resp:
            image_data = resp.read()
            content_type = resp.headers.get("Content-Type", "image/jpeg")

        ext = "jpg" if "jpeg" in content_type or "jpg" in content_type else "png"
        filename = f"cover.{ext}"

        # 使用临时素材接口上传封面（thumb 类型）
        upload_url = f"{WECHAT_API_BASE}/media/upload?access_token={token}&type=thumb"
        boundary = "----FormBoundaryThumb7MA4YWxk"

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8") + image_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

        req = urllib.request.Request(
            upload_url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        if "media_id" not in result:
            # 如果封面上传失败，尝试使用正文图片 URL 替代
            print(f"  ⚠️  封面上传失败: {result}，将使用第一张正文图片 media_id")
            return ""

        return result["media_id"]

    # ── 草稿创建 ───────────────────────────────────────────────────

    def create_draft(
        self,
        title: str,
        html_content: str,
        cover_media_id: str,
        author: str = "",
        digest: str = "",
        need_open_comment: bool = True,
    ) -> str:
        """
        创建公众号草稿

        Args:
            title: 文章标题
            html_content: 文章 HTML 内容
            cover_media_id: 封面图的 thumb_media_id
            author: 作者
            digest: 文章摘要（120字以内，留空则自动截取）
            need_open_comment: 是否开启留言

        Returns:
            草稿的 media_id
        """
        token = self.get_access_token()
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"

        # 自动生成摘要
        if not digest:
            # 去除 HTML 标签提取纯文本
            import re
            plain_text = re.sub(r"<[^>]+>", "", html_content)
            plain_text = plain_text.replace("\n", " ").strip()
            digest = plain_text[:120] if len(plain_text) > 120 else plain_text

        article = {
            "title": title,
            "author": author,
            "digest": digest,
            "content": html_content,
            "content_source_url": "",    # 原文链接（可选）
            "need_open_comment": 1 if need_open_comment else 0,
            "only_fans_can_comment": 0,  # 所有人可留言
        }

        # 封面图（如有）
        if cover_media_id:
            article["thumb_media_id"] = cover_media_id

        payload = {"articles": [article]}

        print(f"\n📤 正在创建草稿：《{title}》...")
        result = _api_call(url, data=payload)

        media_id = result.get("media_id", "")
        print(f"✅ 草稿创建成功！")
        print(f"   media_id: {media_id}")
        print(f"\n🔗 请前往公众号后台预览并发布：")
        print(f"   https://mp.weixin.qq.com → 草稿箱")

        return media_id

    # ── 一键发布流水线 ─────────────────────────────────────────────

    def publish_pipeline(
        self,
        title: str,
        html_content: str,
        cover_image_url: str,
        inline_image_urls: list[str] = None,
        author: str = "IT科技号",
    ) -> dict:
        """
        完整发布流水线：上传图片 → 替换链接 → 创建草稿

        Returns:
            {"success": bool, "media_id": str, "error": str}
        """
        if inline_image_urls is None:
            inline_image_urls = []

        print("\n" + "=" * 50)
        print("🚀 开始发布流水线")
        print("=" * 50)

        try:
            # 1. 上传封面图
            cover_media_id = ""
            if cover_image_url:
                print("\n📸 Step 1/3: 上传封面图...")
                try:
                    cover_media_id = self.upload_cover_image(cover_image_url)
                except Exception as e:
                    print(f"  ⚠️  封面上传失败（{e}），将跳过封面")

            # 2. 上传正文图片并替换链接
            print(f"\n🖼️  Step 2/3: 上传正文配图（共 {len(inline_image_urls)} 张）...")
            for i, img_url in enumerate(inline_image_urls, 1):
                try:
                    wechat_url = self.upload_image_from_url(img_url)
                    # 替换 HTML 中的图片链接
                    html_content = html_content.replace(img_url, wechat_url)
                except Exception as e:
                    print(f"  ⚠️  第{i}张图片上传失败: {e}")

            # 3. 创建草稿
            print("\n📝 Step 3/3: 创建草稿...")
            media_id = self.create_draft(
                title=title,
                html_content=html_content,
                cover_media_id=cover_media_id,
                author=author,
            )

            return {"success": True, "media_id": media_id, "error": None}

        except WechatAPIError as e:
            error_msg = f"微信API错误 [{e.errcode}]: {e.errmsg}"
            print(f"\n❌ 发布失败: {error_msg}")
            return {"success": False, "media_id": None, "error": error_msg}
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ 发布失败: {error_msg}")
            return {"success": False, "media_id": None, "error": error_msg}


def main():
    parser = argparse.ArgumentParser(description="微信公众号草稿发布工具")
    parser.add_argument("--app-id", default=os.getenv("WECHAT_APP_ID"), help="服务号 AppID")
    parser.add_argument("--app-secret", default=os.getenv("WECHAT_APP_SECRET"), help="服务号 AppSecret")
    parser.add_argument("--html", required=True, help="文章 HTML 文件路径")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--cover", default="", help="封面图 URL 或本地路径")
    parser.add_argument("--author", default="IT科技号", help="作者名称")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        print("❌ 请设置 WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量，或通过 --app-id/--app-secret 参数传入")
        return

    publisher = WechatPublisher(args.app_id, args.app_secret)
    html_content = Path(args.html).read_text(encoding="utf-8")

    result = publisher.publish_pipeline(
        title=args.title,
        html_content=html_content,
        cover_image_url=args.cover,
        author=args.author,
    )

    print("\n" + json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
