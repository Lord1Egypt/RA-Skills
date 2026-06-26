#!/usr/bin/env python3
"""
企业微信消息发送模块
====================
通过企业微信自建应用 API 主动发送消息给用户。
与 Webhook 不同，自建应用可以发送消息给指定用户，且支持更多消息类型。

发送流程：
  1. 获取 access_token（缓存2小时）
  2. 调用 /cgi-bin/message/send 接口发送
"""

import time
import requests
import threading
from . import config


class WeComSender:
    """企业微信消息发送器"""

    def __init__(self):
        self.corp_id = config.CORP_ID
        self.secret = config.SECRET
        self.agent_id = config.AGENT_ID
        self._access_token = None
        self._token_expires = 0
        self._lock = threading.Lock()

    def _get_access_token(self):
        """获取 access_token（带缓存）"""
        now = time.time()
        with self._lock:
            if self._access_token and now < self._token_expires - 60:
                return self._access_token

            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            resp = requests.get(url, params={
                "corpid": self.corp_id,
                "corpsecret": self.secret,
            }, timeout=10)
            data = resp.json()

            if data.get("errcode") == 0:
                self._access_token = data["access_token"]
                self._token_expires = now + data.get("expires_in", 7200)
                return self._access_token
            else:
                raise Exception(f"获取 access_token 失败: {data}")

    def send_text(self, user_id, content):
        """
        发送文本消息

        Args:
            user_id: 用户ID（企业微信成员 UserId），"@all" 表示所有人
            content: 文本内容
        """
        token = self._get_access_token()
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"

        data = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": self.agent_id,
            "text": {"content": content},
        }

        resp = requests.post(url, json=data, timeout=10)
        result = resp.json()
        if result.get("errcode") == 0:
            return True, result
        else:
            return False, result

    def send_markdown(self, user_id, content):
        """
        发送 Markdown 消息

        Args:
            user_id: 用户ID，"@all" 表示所有人
            content: Markdown 内容
        """
        token = self._get_access_token()
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"

        data = {
            "touser": user_id,
            "msgtype": "markdown",
            "agentid": self.agent_id,
            "markdown": {"content": content},
        }

        resp = requests.post(url, json=data, timeout=10)
        result = resp.json()
        if result.get("errcode") == 0:
            return True, result
        else:
            return False, result

    def send_markdown_chunked(self, user_id, content, max_bytes=3800):
        """
        分段发送 Markdown（企微有4096字节限制）

        Args:
            user_id: 用户ID
            content: 完整 Markdown 内容
            max_bytes: 每段最大字节数
        """
        if len(content.encode("utf-8")) <= max_bytes:
            return self.send_markdown(user_id, content)

        # 分段
        sections = content.split("\n\n---\n")
        chunks = []
        current = ""
        for section in sections:
            test = current + "\n\n---\n" + section if current else section
            if len(test.encode("utf-8")) > max_bytes:
                if current:
                    chunks.append(current)
                current = section
            else:
                current = test
        if current:
            chunks.append(current)

        total = len(chunks)
        all_ok = True
        for i, chunk in enumerate(chunks, 1):
            if total > 1:
                chunk = f"{chunk}\n\n> 📄 第{i}/{total}部分"
            ok, result = self.send_markdown(user_id, chunk)
            if not ok:
                all_ok = False
            if i < total:
                time.sleep(1)

        return all_ok, {"total_chunks": total}

    def send_to_webhook(self, content, msgtype="markdown"):
        """通过 Webhook 发送到群聊（兼容已有功能）"""
        if msgtype == "markdown":
            payload = {"msgtype": "markdown", "markdown": {"content": content}}
        else:
            payload = {"msgtype": "text", "text": {"content": content}}

        resp = requests.post(config.WEBHOOK_URL, json=payload, timeout=10)
        result = resp.json()
        return result.get("errcode") == 0, result


# 全局单例
sender = WeComSender()
