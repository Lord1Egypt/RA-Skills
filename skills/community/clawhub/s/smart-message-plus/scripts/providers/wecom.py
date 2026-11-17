#!/usr/bin/env python3
"""smart-message-plus: WeCom (企业微信) adapter — webhook (group robot) mode.

当前实现为「群机器人 webhook」模式：
- 无需可信 IP、无需通讯录权限，任意群 30 秒可接入
- 能力范围：群文本 / Markdown / 图片 / 文件 / news 卡片 / @人 / @所有人
- 不支持：单聊、通讯录查人、建群、撤回、部门广播（这些属于自建应用
  wecom-app 模式，需要企业自有服务器出口 IP + 企业可信 IP 配置，
  当前预留升级位，见 references/console-setup.md）

群的表示：一个 webhook = 一个群。推荐把 webhook 存成群别名：
    --save-group 告警群 wecom <webhook_url_或_key>
发送时 --provider wecom --chat-id 告警群 即可。
"""
from __future__ import annotations

import base64
import hashlib
import os
import re

from core.http import request, multipart_upload
from .base import Provider, SendResult, NotSupported

WEBHOOK_BASE = "https://qyapi.weixin.qq.com/cgi-bin/webhook"
_KEY_RE = re.compile(r"^[0-9a-fA-F-]{30,50}$")

IMAGE_LIMIT = 2 * 1024 * 1024      # webhook 图片消息上限 2MB（base64 前）
FILE_LIMIT = 20 * 1024 * 1024      # webhook 文件上传上限 20MB

_APP_MODE_HINT = (
    "wecom 当前为群机器人 webhook 模式，不支持该操作。"
    "单聊/通讯录/建群/撤回需要自建应用（wecom-app）模式——"
    "该模式要求企业可信 IP（企业自有服务器出口），当前环境不具备，已预留后续升级。"
)


class WeComProvider(Provider):
    name = "wecom"

    @classmethod
    def capabilities(cls) -> dict:
        caps = super().capabilities()
        caps.update(
            group_text=True, group_markdown=True,
            image=True, file=True,
            mention=True, mention_all=True,
            card=True,
        )
        return caps

    # ---- webhook helpers ----

    def _webhook_url(self, chat_id: str) -> str:
        """chat_id 允许三种形态：完整 webhook URL / 裸 key / 空(回退账号默认)。"""
        raw = (chat_id or "").strip() or (self.account.get("webhook_url") or "").strip()
        if not raw:
            raise ValueError(
                "缺少 webhook：用 --save-group <别名> wecom <webhook_url> 保存群，"
                "或 --save-account 时配 --webhook-url 设默认群"
            )
        if raw.startswith("http://") or raw.startswith("https://"):
            return raw
        if _KEY_RE.match(raw):
            return f"{WEBHOOK_BASE}/send?key={raw}"
        raise ValueError(
            f"无法识别的 wecom webhook: {raw[:30]}...（应为完整 URL 或 key）"
        )

    def _post(self, url: str, body: dict) -> tuple[bool, str, dict]:
        st, r = request(url, body, timeout=self.timeout)
        code = r.get("errcode", -1)
        if st == 200 and code == 0:
            return True, "", r
        msg = r.get("errmsg", str(r)[:200])
        hint = ""
        if code == 93000:
            hint = "（webhook 无效/已被移除，请到群里重新获取机器人 webhook）"
        elif code == 45009:
            hint = "（触发频率限制：每机器人每分钟最多 20 条，请稍后重试）"
        elif code == 40008 or code == 301059:
            hint = "（消息类型不被该 webhook 支持）"
        return False, f"errcode={code} {msg} {hint}".strip(), r

    # ---- token / test ----

    def get_token(self) -> str:
        # webhook 模式无 token；预留 wecom-app 模式（corpid+corpsecret → gettoken）
        return ""

    def test(self) -> tuple[bool, str]:
        url = (self.account.get("webhook_url") or "").strip()
        if not url:
            return True, ("wecom webhook 模式：账号无需凭证。"
                          "群 webhook 用 --save-group 保存（一个 webhook = 一个群）")
        try:
            self._webhook_url(url)
        except ValueError as e:
            return False, str(e)
        return True, "webhook URL 格式有效（连通性以真实发送为准，test 不打扰群）"

    # ---- resolve ----

    def resolve_user(self, raw: str) -> str:
        raw = raw.strip()
        if not raw.isascii():
            raise ValueError(
                f"「{raw}」不在联系人别名中，且 wecom webhook 模式无法查通讯录。"
                f'请先保存别名: --save-contact {raw} single "wecom:<企业微信userid或手机号>"'
            )
        return raw

    # ---- send ----

    def send_p2p(self, user_ids, text, markdown=False) -> SendResult:
        raise NotSupported(_APP_MODE_HINT)

    def send_group(self, chat_id, text, markdown=False,
                   mention_ids=None, mention_all=False) -> SendResult:
        url = self._webhook_url(chat_id)
        mention_ids = mention_ids or []
        detail = ""
        if markdown:
            content = text
            # wecom markdown 支持 <@userid> 内联提醒；不支持 @所有人
            if mention_ids:
                content += "\n" + " ".join(f"<@{u}>" for u in mention_ids)
            if mention_all:
                detail = "markdown 不支持@所有人（已忽略）；需要@所有人请去掉 --markdown 用文本发"
            body = {"msgtype": "markdown", "markdown": {"content": content}}
        else:
            userids = [u for u in mention_ids if not u.isdigit()]
            mobiles = [u for u in mention_ids if u.isdigit()]
            if mention_all:
                userids.append("@all")
            m = {"content": text}
            if userids:
                m["mentioned_list"] = userids
            if mobiles:
                m["mentioned_mobile_list"] = mobiles
            body = {"msgtype": "text", "text": m}
        good, err, r = self._post(url, body)
        if good:
            # webhook 不返回 msg_id（也没有撤回能力），用内容 hash 做日志占位
            fake_id = "wh_" + hashlib.md5(text.encode()).hexdigest()[:12]
            return SendResult(True, fake_id, detail)
        return SendResult(False, "", err)

    # ---- card (news 形态) ----

    def send_card_group(self, chat_id, title, text, buttons=None) -> SendResult:
        url = self._webhook_url(chat_id)
        buttons = buttons or []
        if not buttons:
            # news 卡片必须有跳转 URL；无按钮时降级为 markdown（带加粗标题）
            md = (f"**{title}**\n\n{text}") if title else text
            res = self.send_group(chat_id, md, markdown=True)
            if res.ok:
                res.detail = "wecom 卡片需要至少一个按钮 URL，已降级为 Markdown 发送"
            return res
        label, jump = buttons[0]
        detail = ""
        if len(buttons) > 1:
            detail = f"wecom news 卡片仅支持一个跳转链接，已使用第一个按钮「{label}」，其余 {len(buttons)-1} 个忽略"
        body = {"msgtype": "news", "news": {"articles": [{
            "title": (title or text[:60] or "消息"),
            "description": text[:200],
            "url": jump,
        }]}}
        good, err, r = self._post(url, body)
        if good:
            fake_id = "wh_" + hashlib.md5((title + text).encode()).hexdigest()[:12]
            return SendResult(True, fake_id, detail)
        return SendResult(False, "", err)

    def send_card_p2p(self, user_ids, title, text, buttons=None) -> SendResult:
        raise NotSupported(_APP_MODE_HINT)

    # ---- media ----

    def send_image_group(self, chat_id, path) -> SendResult:
        url = self._webhook_url(chat_id)
        if not os.path.isfile(path):
            return SendResult(False, "", f"文件不存在: {path}")
        size = os.path.getsize(path)
        if size > IMAGE_LIMIT:
            return SendResult(False, "", f"图片 {size/1024/1024:.1f}MB 超过 webhook 上限 2MB，请压缩后再发")
        with open(path, "rb") as f:
            data = f.read()
        body = {"msgtype": "image", "image": {
            "base64": base64.b64encode(data).decode(),
            "md5": hashlib.md5(data).hexdigest(),
        }}
        good, err, _ = self._post(url, body)
        return SendResult(good, "wh_img" if good else "", err if not good else "")

    def send_file_group(self, chat_id, path) -> SendResult:
        url = self._webhook_url(chat_id)
        if not os.path.isfile(path):
            return SendResult(False, "", f"文件不存在: {path}")
        size = os.path.getsize(path)
        if size > FILE_LIMIT:
            return SendResult(False, "", f"文件 {size/1024/1024:.1f}MB 超过 webhook 上限 20MB")
        # 1) 上传临时素材（media_id 3 天有效）
        key = url.split("key=", 1)[-1] if "key=" in url else ""
        if not key:
            return SendResult(False, "", "webhook URL 中未找到 key，无法上传文件")
        up_url = f"{WEBHOOK_BASE}/upload_media?key={key}&type=file"
        with open(path, "rb") as f:
            fdata = f.read()
        st, r = multipart_upload(
            up_url, {}, "media", os.path.basename(path), fdata,
            "application/octet-stream", timeout=max(self.timeout, 60),
        )
        if r.get("errcode", -1) != 0:
            return SendResult(False, "", f"文件上传失败: errcode={r.get('errcode')} {r.get('errmsg', '')}")
        media_id = r.get("media_id", "")
        # 2) 发送文件消息
        good, err, _ = self._post(url, {"msgtype": "file", "file": {"media_id": media_id}})
        return SendResult(good, "wh_file" if good else "", err if not good else "")

    def send_image_p2p(self, user_ids, path) -> SendResult:
        raise NotSupported(_APP_MODE_HINT)

    def send_file_p2p(self, user_ids, path) -> SendResult:
        raise NotSupported(_APP_MODE_HINT)

    # ---- recall ----

    def recall(self, log_entry: dict) -> tuple[bool, str]:
        return False, ("wecom webhook 模式不支持撤回（平台限制，webhook 不返回消息 ID）。"
                       "如需撤回能力，等待 wecom-app 模式上线")
