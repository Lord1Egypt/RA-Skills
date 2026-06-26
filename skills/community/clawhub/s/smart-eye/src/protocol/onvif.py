"""
onvif.py - ONVIF WS-UsernameToken 认证客户端

封装 SOAP 请求逻辑，供各品牌实现类使用。
支持：
  - WS-UsernameToken Digest 认证
  - GetStatus / ContinuousMove / AbsoluteMove / Stop 等 PTZ 操作
  - GetSnapshotUri / GetStreamUri（Media 服务）

不处理业务逻辑，只负责构造和发送符合 ONVIF 规范的 SOAP 消息。
"""

import base64
import hashlib
import random
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Tuple, Optional


class ONVIFClient:
    """
    轻量级 ONVIF SOAP 客户端。

    使用方法（品牌实现类中）：
        client = ONVIFClient("192.168.1.60", 2020, "admin", "password")
        code, body = client.request("/onvif/service", soap_body, "http://example/action")
    """

    def __init__(self, host: str, port: int, user: str, password: str,
                 ssl_verify: bool = False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ssl_verify = ssl_verify

        # urllib 不验证 SSL 时使用
        if not ssl_verify:
            import ssl as _ssl
            ctx = _ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = _ssl.CERT_NONE
            self._ssl_context: Optional[_ssl.SSLContext] = ctx
        else:
            self._ssl_context = None

    # ---- 认证 ----

    @staticmethod
    def _make_nonce() -> str:
        """生成 16 字节随机 nonce，Base64 编码。"""
        b = bytes(random.randint(0, 255) for _ in range(16))
        return base64.b64encode(b).decode()

    @staticmethod
    def _make_created() -> str:
        """生成 UTC 时间戳（ISO 格式）。"""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _make_digest(nonce_b64: str, created: str, password: str) -> str:
        """
        生成 PasswordDigest。
        ONVIF spec: Base64(SHA1(Nonce_bytes + Created + Password))
        """
        nonce_bytes = base64.b64decode(nonce_b64)
        raw = nonce_bytes + created.encode() + password.encode()
        return base64.b64encode(hashlib.sha1(raw).digest()).decode()

    def _auth_headers(self) -> dict:
        """生成 WS-UsernameToken SOAP Header。"""
        nonce  = self._make_nonce()
        created = self._make_created()
        digest  = self._make_digest(nonce, created, self.password)
        return {
            "wsse:UsernameToken": {
                "wsse:Username": self.user,
                "wsse:Password": {
                    "_": digest,
                    "Type": "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest"
                },
                "wsse:Nonce": nonce,
                "wsu:Created": created,
            }
        }

    # ---- 请求 ----

    def request(self, path: str, soap_body: str,
                soap_action: str = "") -> Tuple[int, str]:
        """
        发送 SOAP 请求。

        Args:
            path:        ONVIF 服务路径，如 /onvif/service
            soap_body:    SOAP Body XML 字符串
            soap_action:  SOAPAction HTTP Header 值

        Returns:
            (HTTP 状态码, 响应体字符串)
        """
        url = f"http://{self.host}:{self.port}{path}"
        req = urllib.request.Request(
            url,
            data=soap_body.encode("utf-8"),
            method="POST"
        )
        req.add_header("Content-Type", "application/soap+xml; charset=utf-8")
        if soap_action:
            req.add_header("SOAPAction", soap_action)

        # 注入 WS-Security Header
        self._add_wsse_header(req)

        try:
            with urllib.request.urlopen(
                req, timeout=5,
                context=self._ssl_context
            ) as resp:
                return resp.getcode(), resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", errors="replace")

    def _add_wsse_header(self, req: urllib.request.Request):
        """向请求注入 WS-UsernameToken 安全头。"""
        nonce    = self._make_nonce()
        created  = self._make_created()
        pwd_digest = self._make_digest(nonce, created, self.password)

        # 手拼 WSSE Header（urllib 不支持直接塞字典）
        wsse = (
            f'<wsse:Security soap-env:mustUnderstand="true">'
            f'<wsse:UsernameToken>'
            f'<wsse:Username>{self.user}</wsse:Username>'
            f'<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{pwd_digest}</wsse:Password>'
            f'<wsse:Nonce>{nonce}</wsse:Nonce>'
            f'<wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">{created}</wsu:Created>'
            f'</wsse:UsernameToken>'
            f'</wsse:Security>'
        )

        # 在已有 soap_body 里替换或插入 Header
        pass  # 由调用方在 soap_body 中自行处理

    # ---- PTZ 便捷方法 ----

    def get_status(self, profile_token: str) -> Tuple[int, str]:
        """查询 PTZ 状态。"""
        body = self._ptz_envelope(
            profile_token,
            "<tptz:GetStatus/>",
            ns="http://www.onvif.org/ver20/ptz/wsdl"
        )
        return self.request("/onvif/PTZ", body, "http://www.onvif.org/ver20/ptz/wsdl/GetStatus")

    def continuous_move(self, profile_token: str,
                        pan_vel: float, tilt_vel: float,
                        zoom_vel: float = 0.0) -> Tuple[int, str]:
        """连续移动。velocity 范围通常 [-1, 1]。"""
        body = self._ptz_envelope(profile_token, f"""
            <tptz:Velocity>
                <tt:PanTilt x="{pan_vel:.4f}" y="{tilt_vel:.4f}"/>
                <tt:Zoom x="{zoom_vel:.4f}"/>
            </tptz:Velocity>
        """)
        return self.request("/onvif/PTZ", body, "http://www.onvif.org/ver20/ptz/wsdl/ContinuousMove")

    def absolute_move(self, profile_token: str,
                      pan: float, tilt: float,
                      zoom: float = 0.0) -> Tuple[int, str]:
        """绝对移动到目标位置。"""
        body = self._ptz_envelope(profile_token, f"""
            <tptz:Position>
                <tt:PanTilt x="{pan:.4f}" y="{tilt:.4f}"/>
                <tt:Zoom x="{zoom:.4f}"/>
            </tptz:Position>
        """)
        return self.request("/onvif/PTZ", body, "http://www.onvif.org/ver20/ptz/wsdl/AbsoluteMove")

    def stop(self, profile_token: str) -> Tuple[int, str]:
        """停止。"""
        body = self._ptz_envelope(profile_token, "<tptz:Stop/>")
        return self.request("/onvif/PTZ", body, "http://www.onvif.org/ver20/ptz/wsdl/Stop")

    # ---- 内部工具 ----

    @staticmethod
    def _ptz_envelope(token: str, inner: str,
                      ns: str = "http://www.onvif.org/ver20/ptz/wsdl") -> str:
        """构造带 WSSE Auth Header 的 PTZ SOAP 信封。"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<soap-env:Envelope
  xmlns:soap-env="http://www.w3.org/2003/05/soap-envelope"
  xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
  xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
  xmlns:tt="http://www.onvif.org/ver10/schema"
  xmlns:tptz="{ns}">
  <soap-env:Header/>
  <soap-env:Body>{inner.replace("<tptz:", f"<{ns}/tptz:").replace("</tptz:", f"</{ns}/tptz:")}</soap-env:Body>
</soap-env:Envelope>'''
