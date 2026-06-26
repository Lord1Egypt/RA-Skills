"""
onvif_ptz_control.py - TP-Link ONVIF PTZ 控制

⚠️  不含任何硬编码凭证！所有设备参数由调用方传入。
TP-Link TL-IPC44AW-COLOR：port=2020, PTZ_TOKEN=PTZTOKEN
"""

import urllib.request
import urllib.error
import base64
import hashlib
import random
import re
import time
from datetime import datetime, timezone


class TPClient:
    """TP-Link ONVIF PTZ 客户端（无硬编码凭证）。"""

    def __init__(self, host: str, port: int, user: str, password: str,
                 ptz_token: str = "PTZTOKEN"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.ptz_token = ptz_token
        self.url = f"http://{host}:{port}/onvif/service"

    # ---- 认证 ----

    def _auth_headers(self) -> dict:
        created = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        nonce_bytes = bytes(random.randint(0, 255) for _ in range(16))
        nonce_b64 = base64.b64encode(nonce_bytes).decode()
        raw = nonce_bytes + created.encode() + self.password.encode()
        digest = base64.b64encode(hashlib.sha1(raw).digest()).decode()
        return nonce_b64, created, digest

    # ---- 底层请求 ----

    def _soap_request(self, body_xml: str, soap_action: str) -> tuple:
        nonce, created, digest = self._auth_headers()
        soap_body = f'''<?xml version="1.0" encoding="UTF-8"?>
<soap-env:Envelope xmlns:soap-env="http://www.w3.org/2003/05/soap-envelope"
  xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
  xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
  <soap-env:Header>
    <wsse:Security soap-env:mustUnderstand="true">
      <wsse:UsernameToken>
        <wsse:Username>{self.user}</wsse:Username>
        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{digest}</wsse:Password>
        <wsse:Nonce>{nonce}</wsse:Nonce>
        <wsu:Created>{created}</wsu:Created>
      </wsse:UsernameToken>
    </wsse:Security>
  </soap-env:Header>
  <soap-env:Body>{body_xml}</soap-env:Body>
</soap-env:Envelope>'''
        req = urllib.request.Request(
            self.url, data=soap_body.encode('utf-8'),
            headers={
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'SOAPAction': soap_action,
            },
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return 200, resp.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode('utf-8', errors='replace')

    # ---- PTZ 操作 ----

    def get_status(self) -> tuple:
        """返回 ((pan, tilt), zoom, status_str)"""
        code, resp = self._soap_request(
            f'<tptz:GetStatus xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">'
            f'<tptz:ProfileToken>{self.ptz_token}</tptz:ProfileToken></tptz:GetStatus>',
            'http://www.onvif.org/ver20/ptz/wsdl/GetStatus'
        )
        pan = re.search(r'<tt:PanTilt[^>]+x="([^"]+)"[^>]+y="([^"]+)"', resp)
        zoom = re.search(r'<tt:Zoom[^>]+x="([^"]+)"', resp)
        move = re.search(r'<tt:PanTilt>([^<]+)</tt:PanTilt>', resp)
        pos = (float(pan.group(1)), float(pan.group(2))) if pan else (0.0, 0.0)
        z = float(zoom.group(1)) if zoom else 0.0
        st = move.group(1) if move else 'unknown'
        return pos, z, st

    def move_abs(self, pan: float, tilt: float, zoom: float = 0.0) -> bool:
        """AbsoluteMove: pan/tilt [-1,1], zoom [0,1]"""
        zoom_elem = f'<tt:Zoom x="{zoom}" xmlns:tt="http://www.onvif.org/ver10/schema"/>' if zoom != 0 else ''
        code, resp = self._soap_request(
            f'''<tptz:AbsoluteMove xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
  <tptz:ProfileToken>{self.ptz_token}</tptz:ProfileToken>
  <tptz:Position>
    <tt:PanTilt x="{pan}" y="{tilt}" xmlns:tt="http://www.onvif.org/ver10/schema"/>
    {zoom_elem}
  </tptz:Position>
</tptz:AbsoluteMove>''',
            'http://www.onvif.org/ver20/ptz/wsdl/AbsoluteMove'
        )
        return 'Fault' not in resp and code == 200

    def move_cont(self, pan_vel: float, tilt_vel: float, zoom_vel: float = 0.0) -> bool:
        """ContinuousMove: velocity [-1, 1]"""
        # TP-Link: zoom_vel=0 时省略 Zoom 元素
        if zoom_vel == 0:
            body = (
                f'<tptz:ContinuousMove xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">'
                f'<tptz:ProfileToken>{self.ptz_token}</tptz:ProfileToken>'
                f'<tptz:Velocity>'
                f'<tt:PanTilt x="{pan_vel}" y="{tilt_vel}" xmlns:tt="http://www.onvif.org/ver10/schema"/>'
                f'</tptz:Velocity>'
                f'</tptz:ContinuousMove>'
            )
        else:
            body = (
                f'<tptz:ContinuousMove xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">'
                f'<tptz:ProfileToken>{self.ptz_token}</tptz:ProfileToken>'
                f'<tptz:Velocity>'
                f'<tt:PanTilt x="{pan_vel}" y="{tilt_vel}" xmlns:tt="http://www.onvif.org/ver10/schema"/>'
                f'<tt:Zoom x="{zoom_vel}" xmlns:tt="http://www.onvif.org/ver10/schema"/>'
                f'</tptz:Velocity>'
                f'</tptz:ContinuousMove>'
            )
        code, resp = self._soap_request(body,
            'http://www.onvif.org/ver20/ptz/wsdl/ContinuousMove')
        return 'Fault' not in resp and code == 200

    def stop(self) -> bool:
        code, resp = self._soap_request(
            f'<tptz:Stop xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">'
            f'<tptz:ProfileToken>{self.ptz_token}</tptz:ProfileToken>'
            f'</tptz:Stop>',
            'http://www.onvif.org/ver20/ptz/wsdl/Stop'
        )
        return 'Fault' not in resp and code == 200

    def move_home(self) -> bool:
        return self.move_abs(0, 0, 0)
