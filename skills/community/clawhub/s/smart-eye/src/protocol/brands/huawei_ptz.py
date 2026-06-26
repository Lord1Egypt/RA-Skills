"""
huawei_ptz.py - 华为摄像头 PTZ 实现（华为 D2150 等）

SOAP 1.1 命名空间，与标准 ONVIF SOAP 1.2 不同，直接实现以避免兼容问题。
⚠️  不依赖用户 workspace 下的任何文件。
"""

import time
import ssl
import urllib.request
import xml.etree.ElementTree as ET


# ---- 华为 SOAP 1.1 请求 ----

def _make_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _ptz_request(host: str, port: int, body_str: str) -> tuple:
    """发送 PTZ SOAP 1.1 请求，返回 (http_code, response_xml)"""
    url = f"http://{host}:{port}/onvif/PTZ"
    req = urllib.request.Request(url, data=body_str.encode("utf-8"))
    req.add_header("Content-Type", "application/soap+xml; charset=utf-8")
    req.add_header("Accept", "application/soap+xml")
    try:
        with urllib.request.urlopen(req, timeout=5, context=_make_ctx()) as resp:
            return resp.getcode(), resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


def _soap_env(body_inner: str) -> str:
    """构造 SOAP 1.1 信封（华为设备要求旧版 namespace）"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<Envelope xmlns="http://www.onvif.org/2003/11/soap-envelope"
          xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl"
          xmlns:tt="http://www.onvif.org/ver10/schema">
  <Header/>
  <Body>{body_inner}</Body>
</Envelope>'''


def continuous_move(host: str, port: int, profile_token: str,
                   pan_vel: float, tilt_vel: float, zoom_vel: float = 0.0) -> tuple:
    body = _soap_env(f'''
    <tptz:ContinuousMove xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
      <tptz:ProfileToken>{profile_token}</tptz:ProfileToken>
      <tptz:Velocity>
        <tt:PanTilt x="{pan_vel}" y="{tilt_vel}"/>
        <tt:Zoom x="{zoom_vel}"/>
      </tptz:Velocity>
    </tptz:ContinuousMove>
    ''')
    return _ptz_request(host, port, body)


def absolute_move(host: str, port: int, profile_token: str,
                  pan: float, tilt: float, zoom: float = 0.0) -> tuple:
    body = _soap_env(f'''
    <tptz:AbsoluteMove xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
      <tptz:ProfileToken>{profile_token}</tptz:ProfileToken>
      <tptz:Position>
        <tt:PanTilt x="{pan}" y="{tilt}"/>
        <tt:Zoom x="{zoom}"/>
      </tptz:Position>
    </tptz:AbsoluteMove>
    ''')
    return _ptz_request(host, port, body)


def stop(host: str, port: int, profile_token: str) -> tuple:
    body = _soap_env(f'''
    <tptz:Stop xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
      <tptz:ProfileToken>{profile_token}</tptz:ProfileToken>
    </tptz:Stop>
    ''')
    return _ptz_request(host, port, body)


def get_status(host: str, port: int, profile_token: str) -> tuple:
    """返回 (http_code, pan, tilt, zoom, status_str)"""
    body = _soap_env(f'''
    <tptz:GetStatus xmlns:tptz="http://www.onvif.org/ver20/ptz/wsdl">
      <tptz:ProfileToken>{profile_token}</tptz:ProfileToken>
    </tptz:GetStatus>
    ''')
    code, resp = _ptz_request(host, port, body)
    pan_val, tilt_val, zoom_val, status_str = 0.0, 0.0, 0.0, "unknown"
    try:
        root = ET.fromstring(resp)
        ns_tptz = "http://www.onvif.org/ver20/ptz/wsdl"
        ns_tt = "http://www.onvif.org/ver10/schema"
        for tag in ["PanTilt", "Zoom"]:
            el = root.find(f".//{{{ns_tt}}}{tag}")
            if el is not None:
                val = el.get("x", "0.0")
                if tag == "PanTilt":
                    pan_val = float(el.get("x", "0.0"))
                    tilt_val = float(el.get("y", "0.0"))
                else:
                    zoom_val = float(val)
        status_el = root.find(f".//{{{ns_tt}}}StatusState")
        if status_el is not None:
            status_str = status_el.get("x", "unknown")
    except Exception:
        pass
    return code, pan_val, tilt_val, zoom_val, status_str
