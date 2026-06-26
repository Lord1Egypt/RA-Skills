"""
WeChat Work Webhook Notifier
企业微信群机器人消息发送模块
"""

import os
import json
import requests
from typing import Optional, List


class WeChatNotifier:
    """
    企业微信 Webhook 通知器

    使用方式：
        notifier = WeChatNotifier()
        notifier.send_text("Hello WeChat!")
    """

    def __init__(self, webhook_url: str = None):
        """
        初始化通知器

        Args:
            webhook_url: 企业微信群机器人 Webhook URL。
                        如果不传，则从环境变量 WECHAT_WEBHOOK_URL 读取。
        """
        self.webhook_url = webhook_url or os.getenv("WECHAT_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError(
                "未设置 Webhook URL。"
                "请传入 webhook_url 或设置环境变量 WECHAT_WEBHOOK_URL"
            )
        self.session = requests.Session()

    def _send(self, payload: dict) -> dict:
        """
        发送消息到企业微信 Webhook

        Args:
            payload: 消息载荷（符合企业微信 API 格式）

        Returns:
            企业微信返回的响应字典
        """
        try:
            resp = self.session.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            result = resp.json()
            errcode = result.get("errcode", 0)

            if errcode == 0:
                return {"ok": True, "errmsg": result.get("errmsg", "ok")}
            else:
                return {
                    "ok": False,
                    "errcode": errcode,
                    "errmsg": result.get("errmsg", "未知错误"),
                }
        except requests.RequestException as e:
            return {"ok": False, "errmsg": str(e)}

    # ─── 文本消息 ─────────────────────────────────

    def send_text(
        self,
        content: str,
        mentioned_list: Optional[List[str]] = None,
        mentioned_mobile_list: Optional[List[str]] = None,
    ) -> dict:
        """
        发送纯文本消息

        Args:
            content: 消息内容（最长 2048 字节）
            mentioned_list: userid 列表（被 @ 的成员）
            mentioned_mobile_list: 手机号列表（被 @ 的成员，按手机号 @）

        Returns:
            发送结果
        """
        payload = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or [],
                "mentioned_mobile_list": mentioned_mobile_list or [],
            },
        }
        return self._send(payload)

    # ─── Markdown 消息 ─────────────────────────────

    def send_markdown(self, content: str) -> dict:
        """
        发送 Markdown 格式消息（企业微信支持的子集）

        支持的 Markdown 语法：
        - 标题（# ## ###）
        - 加粗 **粗体**
        - 斜体（企业微信不支持标准斜体，用绿/蓝色代替）
        - 链接 [text](url)
        - 图片 ![alt](url)
        - 引用 > text
        - 无序列表 - item
        - 有序列表 1. item
        - 代码 `code`（行内）

        Args:
            content: Markdown 内容（最长 2048 字节）

        Returns:
            发送结果
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {"content": content},
        }
        return self._send(payload)

    # ─── 图文消息（卡片） ──────────────────────────

    def send_news(
        self,
        title: str,
        description: str,
        url: str,
        picurl: str = "",
    ) -> dict:
        """
        发送图文消息（点击后跳转链接）

        Args:
            title: 标题（最长 128 字节）
            description: 描述（最长 512 字节）
            url: 点击后跳转的链接
            picurl: 图片 URL（为空则不显示图片）

        Returns:
            发送结果
        """
        articles = [
            {
                "title": title,
                "description": description,
                "url": url,
                "picurl": picurl,
            }
        ]
        payload = {
            "msgtype": "news",
            "news": {"articles": articles},
        }
        return self._send(payload)

    # ─── 发送图片 ─────────────────────────────────

    def send_image(self, base64_data: str, md5_hash: str) -> dict:
        """
        发送图片（需提供 base64 编码和 MD5）

        Args:
            base64_data: 图片的 base64 字符串
            md5_hash: 图片内容的 MD5 哈希

        Returns:
            发送结果
        """
        payload = {
            "msgtype": "image",
            "image": {
                "base64": base64_data,
                "md5": md5_hash,
            },
        }
        return self._send(payload)

    # ─── 发送文件 ─────────────────────────────────

    def send_file(self, media_id: str) -> dict:
        """
        发送文件（需先通过 /cgi-bin/webhook/upload_media 上传）

        Args:
            media_id: 文件的 media_id

        Returns:
            发送结果
        """
        payload = {
            "msgtype": "file",
            "file": {"media_id": media_id},
        }
        return self._send(payload)

    # ─── 模板卡片消息 ──────────────────────────────

    def send_template_card(
        self,
        card_type: str,
        source: dict = None,
        main_title: dict = None,
        emphasis: dict = None,
        quote_area: dict = None,
        sub_title_text: str = "",
        horizontal_content: list = None,
        jump_list: list = None,
    ) -> dict:
        """
        发送模板卡片消息

        Args:
            card_type: 卡片类型，如 "news_notice", "vote_interaction"
            source: 来源信息 {"icon_url": "", "desc": ""}
            main_title: 主标题 {"title": "", "desc": ""}
            emphasis: 特别提示 {"title": "", "desc": ""}
            quote_area: 引用区域 {"type": 0, "url": "", "quote_text": ""}
            sub_title_text: 副标题
            horizontal_content: 关键数据项
            jump_list: 跳转指令

        Returns:
            发送结果
        """
        content = {"card_type": card_type}

        if source:
            content["source"] = source
        if main_title:
            content["main_title"] = main_title
        if emphasis:
            content["emphasis"] = emphasis
        if quote_area:
            content["quote_area"] = quote_area
        if sub_title_text:
            content["sub_title_text"] = sub_title_text
        if horizontal_content:
            content["horizontal_content"] = horizontal_content
        if jump_list:
            content["jump_list"] = jump_list

        payload = {"msgtype": "template_card", "template_card": content}
        return self._send(payload)


# ════════════════════════════════════════════════
#  命令行入口
# ════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="企业微信 Webhook 通知工具")
    parser.add_argument("--text", help="发送文本消息")
    parser.add_argument("--markdown", help="发送 Markdown 消息")
    parser.add_argument("--news", nargs=4, metavar=("TITLE", "DESC", "URL", "PIC"),
                        help="发送图文消息: 标题 描述 URL 图片URL")
    args = parser.parse_args()

    notifier = WeChatNotifier()

    if args.text:
        result = notifier.send_text(args.text)
    elif args.markdown:
        result = notifier.send_markdown(args.markdown)
    elif args.news:
        title, desc, url, pic = args.news
        result = notifier.send_news(title, desc, url, pic)
    else:
        print("用法：")
        print("  --text '消息内容'")
        print("  --markdown '**粗体** 消息'")
        print("  --news '标题' '描述' 'URL' '图片URL'")
        exit(1)

    if result.get("ok"):
        print("✅ 消息发送成功")
    else:
        print(f"❌ 发送失败：{result}")
