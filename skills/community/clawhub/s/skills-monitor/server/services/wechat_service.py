"""
微信服务层 — 公众号 + 小程序 统一接口
====================================
- 公众号 access_token 管理
- 模板消息推送
- 用户信息获取
- 小程序 code2session
- 带参二维码生成（用于绑定 Agent）
"""

import hashlib
import json
import time
import threading
import requests
from typing import Optional, Tuple, Dict, Any

from server.config import (
    WECHAT_OA_APP_ID, WECHAT_OA_APP_SECRET, WECHAT_OA_TOKEN,
    WECHAT_MP_APP_ID, WECHAT_MP_APP_SECRET,
    WECHAT_TEMPLATE_DAILY_REPORT, WECHAT_TEMPLATE_ALERT,
    H5_BASE_URL,
)


class WeChatService:
    """微信公众号 + 小程序 服务"""

    def __init__(self):
        self._oa_token = None
        self._oa_token_expires = 0
        self._lock = threading.Lock()

    # ──────── Access Token ────────

    def get_oa_access_token(self) -> str:
        """获取公众号 access_token（带缓存）"""
        now = time.time()
        with self._lock:
            if self._oa_token and now < self._oa_token_expires - 120:
                return self._oa_token

            resp = requests.get(
                "https://api.weixin.qq.com/cgi-bin/token",
                params={
                    "grant_type": "client_credential",
                    "appid": WECHAT_OA_APP_ID,
                    "secret": WECHAT_OA_APP_SECRET,
                },
                timeout=10,
            )
            data = resp.json()
            if "access_token" in data:
                self._oa_token = data["access_token"]
                self._oa_token_expires = now + data.get("expires_in", 7200)
                return self._oa_token
            raise Exception(f"获取公众号 access_token 失败: {data}")

    # ──────── 消息验签 ────────

    @staticmethod
    def verify_signature(signature: str, timestamp: str, nonce: str) -> bool:
        """验证微信消息签名"""
        tmp_arr = sorted([WECHAT_OA_TOKEN, timestamp, nonce])
        tmp_str = "".join(tmp_arr)
        computed = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()
        return computed == signature

    # ──────── 模板消息推送 ────────

    def send_template_message(
        self,
        openid: str,
        template_id: str,
        data: Dict[str, Any],
        url: str = "",
        miniprogram: Optional[Dict] = None,
    ) -> Tuple[bool, Dict]:
        """
        发送模板消息

        Args:
            openid: 用户 openid
            template_id: 模板 ID
            data: 模板数据 {"first": {"value": "...", "color": "#333"}, ...}
            url: 点击跳转链接（H5页面）
            miniprogram: 小程序跳转 {"appid": "...", "pagepath": "..."}
        """
        token = self.get_oa_access_token()
        payload = {
            "touser": openid,
            "template_id": template_id,
            "url": url,
            "data": data,
        }
        if miniprogram:
            payload["miniprogram"] = miniprogram

        resp = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}",
            json=payload,
            timeout=10,
        )
        result = resp.json()
        ok = result.get("errcode", -1) == 0
        return ok, result

    def push_daily_report(
        self,
        openid: str,
        agent_name: str,
        health_score: float,
        total_runs: int,
        success_rate: float,
        top_skill: str,
        h5_url: str,
        agent_id: str = "",
    ) -> Tuple[bool, Dict]:
        """
        推送每日报告模板消息
        v0.5.0: 支持点击跳转到小程序（公众号→小程序闭环）
        """
        from datetime import datetime
        now = datetime.now()

        # 健康度 emoji
        if health_score >= 90:
            health_emoji = "🟢"
        elif health_score >= 75:
            health_emoji = "🟡"
        elif health_score >= 60:
            health_emoji = "🟠"
        else:
            health_emoji = "🔴"

        data = {
            "first": {
                "value": f"📊 Skills Monitor 每日报告 — {agent_name}",
                "color": "#173177",
            },
            "keyword1": {
                "value": now.strftime("%Y-%m-%d"),
                "color": "#333333",
            },
            "keyword2": {
                "value": f"{health_emoji} {health_score:.0f}/100",
                "color": "#e74c3c" if health_score < 60 else "#27ae60",
            },
            "keyword3": {
                "value": f"运行 {total_runs} 次 | 成功率 {success_rate:.1f}%",
                "color": "#333333",
            },
            "keyword4": {
                "value": f"🏆 {top_skill}",
                "color": "#2980b9",
            },
            "remark": {
                "value": "点击查看详细报告 →",
                "color": "#999999",
            },
        }

        # v0.5.0: 优先跳转小程序（公众号→小程序闭环）
        miniprogram_config = None
        if WECHAT_MP_APP_ID and agent_id:
            miniprogram_config = {
                "appid": WECHAT_MP_APP_ID,
                "pagepath": (
                    f"pages/dashboard/dashboard"
                    f"?from=daily_push"
                    f"&agent_id={agent_id}"
                    f"&date={now.strftime('%Y-%m-%d')}"
                ),
            }

        return self.send_template_message(
            openid=openid,
            template_id=WECHAT_TEMPLATE_DAILY_REPORT,
            data=data,
            url=h5_url,
            miniprogram=miniprogram_config,
        )

    # ──────── 用户信息 ────────

    def get_user_info(self, openid: str) -> Dict[str, Any]:
        """获取公众号关注用户信息"""
        token = self.get_oa_access_token()
        resp = requests.get(
            "https://api.weixin.qq.com/cgi-bin/user/info",
            params={"access_token": token, "openid": openid, "lang": "zh_CN"},
            timeout=10,
        )
        return resp.json()

    # ──────── 带参二维码（绑定 Agent） ────────

    def create_bind_qrcode(self, agent_id: str, token: str) -> Tuple[bool, Dict]:
        """
        创建带参数的临时二维码，用于扫码绑定 Agent
        scene_str: "bind:{agent_id}:{token_prefix}"
        有效期 5 分钟
        """
        access_token = self.get_oa_access_token()
        scene_str = f"bind:{agent_id}:{token[:16]}"

        payload = {
            "expire_seconds": 300,
            "action_name": "QR_STR_SCENE",
            "action_info": {
                "scene": {"scene_str": scene_str}
            },
        }

        resp = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}",
            json=payload,
            timeout=10,
        )
        result = resp.json()
        if "ticket" in result:
            result["qrcode_url"] = (
                f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={result['ticket']}"
            )
            return True, result
        return False, result

    # ──────── 小程序 ────────

    def mp_code2session(self, code: str) -> Dict[str, Any]:
        """小程序 code 换 session"""
        resp = requests.get(
            "https://api.weixin.qq.com/sns/jscode2session",
            params={
                "appid": WECHAT_MP_APP_ID,
                "secret": WECHAT_MP_APP_SECRET,
                "js_code": code,
                "grant_type": "authorization_code",
            },
            timeout=10,
        )
        return resp.json()

    # ──────── 自定义菜单 ────────

    def create_menu(self) -> Tuple[bool, Dict]:
        """创建公众号自定义菜单"""
        token = self.get_oa_access_token()
        menu = {
            "button": [
                {
                    "type": "view",
                    "name": "📊 查看报告",
                    "url": f"{H5_BASE_URL}/h5/dashboard",
                },
                {
                    "name": "⚙️ 管理",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "我的 Agent",
                            "url": f"{H5_BASE_URL}/h5/agents",
                        },
                        {
                            "type": "click",
                            "name": "绑定 Agent",
                            "key": "BIND_AGENT",
                        },
                        {
                            "type": "view",
                            "name": "推送设置",
                            "url": f"{H5_BASE_URL}/h5/settings",
                        },
                    ],
                },
                {
                    "type": "miniprogram",
                    "name": "小程序",
                    "url": f"{H5_BASE_URL}/h5/dashboard",
                    "appid": WECHAT_MP_APP_ID,
                    "pagepath": "pages/index/index",
                },
            ],
        }

        resp = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={token}",
            json=menu,
            timeout=10,
        )
        result = resp.json()
        return result.get("errcode", -1) == 0, result


# 全局单例
wechat_service = WeChatService()
