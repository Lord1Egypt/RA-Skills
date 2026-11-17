import base64
import hashlib
import json
import os
import secrets
import socket
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse, quote

try:
    import requests as _requests_lib
except ImportError:
    _requests_lib = None

try:
    import yaml as _yaml_lib
except ImportError:
    _yaml_lib = None

try:
    from . import camera_proto
except ImportError:
    import camera_proto

try:
    from ._argnorm import coerce_str
except ImportError:
    from _argnorm import coerce_str

from .discovery import (
    SkDiscoveredDevice,
    SkChannelInfo,
    discover_sky_devices,
    probe_device_sn,
    SUBTYPE_NAMES,
)

class DiscoveryMethod(str, Enum):
    WS_DISCOVERY = "ws_discovery"
    SKY_DISCOVERY = "sky_discovery"
    JCP_DISCOVERY = "jcp_discovery"

class DeviceClass(str, Enum):
    PASSWORD_REQUIRED = "password_required"
    DIRECT_CONNECT = "direct_connect"

class AuthStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    REJECTED = "rejected"
    ERROR = "error"

@dataclass
class DiscoveredDevice:
    ip: str
    onvif_port: int = 0
    rtsp_port: int = 554
    device_class: DeviceClass = DeviceClass.PASSWORD_REQUIRED
    sn_code: str = ""
    model: str = ""
    manufacturer: str = ""
    supported_media: List[str] = field(default_factory=list)

    sky_subtype: str = ""
    sky_name: str = ""
    sky_dtype: str = ""
    sky_hw_version: str = ""
    sky_sw_version: str = ""
    sky_did: str = ""
    sky_channels: int = 0
    sky_channel_list: List[SkChannelInfo] = field(default_factory=list)
    sky_web_port: int = 0
    sky_udp_port: int = 0
    sky_net_type: str = ""
    sky_ip_mode: str = ""
    sky_mask: str = ""
    sky_gateway: str = ""
    sky_mac: str = ""
    discovery_method: str = ""
    protocol_type: str = ""
    rtsp_access: str = ""
    supported_illumination_modes: List[str] = field(default_factory=list)

@dataclass
class SearchResult:
    success: bool
    devices: List[DiscoveredDevice] = field(default_factory=list)
    error_message: str = ""

@dataclass
class ConnectResult:
    success: bool
    auth_method: str = ""
    status: str = "connected"
    error_message: str = ""
    needs_password: bool = False
    onvif_port: int = 0
    protocol_type: str = ""

@dataclass
class DisconnectResult:
    success: bool
    session_released: bool = False
    error_message: str = ""

@dataclass
class CameraConfig:
    name: str
    connection_type: str = "onvif"
    ip: str = ""
    port: int = 0
    username: str = "admin"
    password: str = ""
    rtsp_port: int = 554
    rtsp_path: str = "/md0_0"
    rtsp_sub_path: str = "/md0_1"
    device_class: str = ""
    sn_code: str = ""
    pkdk: str = ""
    protocol_type: str = ""
    onvif_sn: str = ""

    illumination_modes: List[str] = field(default_factory=list)

@dataclass
class RegisterResult:
    success: bool
    camera_name: str = ""
    error_message: str = ""

@dataclass
class AuthOrchestrateResult:
    success: bool
    status: str = ""
    camera_name: str = ""
    sn: str = ""
    claw_id: str = ""
    device_pwd: str = ""
    available_cameras: List[Dict[str, str]] = field(default_factory=list)
    error_message: str = ""

@dataclass
class AuthStatusResult:
    status: AuthStatus
    camera_name: str = ""
    message: str = ""
    auth_status_code: int = -1
    device_pwd: str = ""

@dataclass
class CloudAuthRequestResult:
    success: bool
    claw_id: str = ""
    station_default: bool = False
    error_message: str = ""
    http_status: int = 0

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"

_XOR_KEY = 0x5A
_OBF_PREFIX = "enc1:"

def _dec(value: Any) -> str:
    """Decode a stored value. Accepts prefixed and legacy unprefixed forms."""
    if not value:
        return ""
    text = str(value)
    if text.startswith(_OBF_PREFIX):
        text = text[len(_OBF_PREFIX):]
    try:
        raw = base64.b64decode(text, validate=True)
        return bytes(b ^ _XOR_KEY for b in raw).decode("utf-8")
    except Exception:
        return ""

def _to_plain(value: Any) -> str:
    """Decode an `enc1:` value exactly once; anything else is plaintext."""
    if not value:
        return ""
    text = str(value)
    if text.startswith(_OBF_PREFIX):
        return _dec(text) or text
    return text

def _enc(value: Any) -> str:
    text = _to_plain(value)
    if not text:
        return ""
    raw = text.encode("utf-8")
    return _OBF_PREFIX + base64.b64encode(bytes(b ^ _XOR_KEY for b in raw)).decode("ascii")

def _get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "192.168.1.100"
    finally:
        s.close()
    return ip

def _get_local_mac() -> str:
    import platform
    try:
        if platform.system() == "Windows":
            import re
            import subprocess
            out = subprocess.check_output("getmac", shell=True).decode("gbk", "ignore")
            m = re.search(r"([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}", out)
            if m:
                return m.group(0).replace("-", ":").upper()
        else:
            return ":".join(f"{b:02X}" for b in uuid.getnode().to_bytes(6, "big"))
    except Exception:
        pass
    return "00:00:00:00:00:00"

def generate_claw_id() -> str:
    mac = _get_local_mac().replace(":", "").upper()
    now = datetime.now()
    ts = now.strftime("%Y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"
    return f"claw-{mac}-{ts}"

def _dump_claw_id_first(data: Dict[str, Any], claw_id: str) -> Dict[str, Any]:
    ordered: Dict[str, Any] = {"claw_id": claw_id}
    ordered.update({k: v for k, v in data.items() if k != "claw_id"})
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            _yaml_lib.safe_dump(ordered, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    except OSError:
        pass
    return ordered

def get_or_create_claw_id() -> str:
    if _yaml_lib is None:
        return generate_claw_id()

    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = _yaml_lib.safe_load(f) or {}
        else:
            data = {}
    except (OSError, _yaml_lib.YAMLError):
        return generate_claw_id()

    existing = data.get("claw_id", "")
    if existing:

        if next(iter(data), None) != "claw_id":
            _dump_claw_id_first(data, str(existing))
        return str(existing)

    claw_id = generate_claw_id()
    _dump_claw_id_first(data, claw_id)
    return claw_id

_ONVIF_NS = {
    "soap": "http://www.w3.org/2003/05/soap-envelope",
    "tds": "http://www.onvif.org/ver10/device/wsdl",
    "trt": "http://www.onvif.org/ver10/media/wsdl",
    "tt": "http://www.onvif.org/ver10/schema",
}

def _onvif_digest_auth_header(username: str, password: str) -> str:
    nonce_raw = secrets.token_bytes(16)
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest_input = nonce_raw + created.encode("utf-8") + password.encode("utf-8")
    password_digest = base64.b64encode(hashlib.sha1(digest_input).digest()).decode()
    nonce_b64 = base64.b64encode(nonce_raw).decode()
    return (
        '<wsse:UsernameToken xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" '
        'xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">'
        f'<wsse:Username>{username}</wsse:Username>'
        f'<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">{password_digest}</wsse:Password>'
        f'<wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">{nonce_b64}</wsse:Nonce>'
        f'<wsu:Created>{created}</wsu:Created>'
        '</wsse:UsernameToken>'
    )

def _onvif_post_with_auth(
    ip: str, port: int, path: str, body: str,
    username: str, password: str, timeout: float = 5.0,
) -> Tuple[int, str]:
    if _requests_lib is None:
        raise RuntimeError("The 'requests' package is not installed")
    auth_xml = _onvif_digest_auth_header(username, password)
    if "xmlns:wsse=" not in body:
        body = body.replace(
            "<soap:Envelope ",
            '<soap:Envelope xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" '
            'xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" ',
            1,
        )
    if "<soap:Header/>" in body:
        body = body.replace("<soap:Header/>", f"<soap:Header>{auth_xml}</soap:Header>", 1)
    elif "<soap:Header>" in body:
        body = body.replace("<soap:Header>", f"<soap:Header>{auth_xml}", 1)

    resp = _requests_lib.post(
        f"http://{ip}:{port}{path}",
        data=body.encode("utf-8"),
        headers={"Content-Type": "application/soap+xml; charset=utf-8"},
        timeout=timeout,
    )
    return resp.status_code, resp.text

_ONVIF_CANDIDATE_PORTS = [2000, 80, 8000, 8899]

_ONVIF_PROBE_BODY = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" '
    'xmlns:tds="http://www.onvif.org/ver10/device/wsdl">'
    '<soap:Header/><soap:Body><tds:GetSystemDateAndTime/></soap:Body></soap:Envelope>'
)

def _probe_onvif_port(ip: str, hint_port: int = 0, timeout: float = 2.0) -> int:
    if _requests_lib is None:
        return 0
    candidates = []
    for p in [hint_port, *_ONVIF_CANDIDATE_PORTS]:
        if p and p not in candidates:
            candidates.append(p)
    for p in candidates:
        try:
            resp = _requests_lib.post(
                f"http://{ip}:{p}/onvif/device_service",
                data=_ONVIF_PROBE_BODY.encode("utf-8"),
                headers={"Content-Type": "application/soap+xml; charset=utf-8"},
                timeout=timeout,
            )

            text = (resp.text or "")[:2048].lower()
            if "envelope" in text and "<html" not in text:
                return p
        except Exception:
            continue
    return 0

def _build_rtsp_url(ip: str, port: int, path: str, username: str = "", password: str = "") -> str:
    path = (path or "").strip()
    if path.lower().startswith(("rtsp://", "http://", "https://")):
        parsed = urlparse(path)
        if "@" in parsed.netloc:
            _, host_port = parsed.netloc.split("@", 1)
        else:
            host_port = parsed.netloc
        new_netloc = (
            f"{quote(username, safe='')}:{quote(password or '', safe='')}@{host_port}"
            if username else host_port
        )
        new_path = parsed.path or "/"
        if not new_path.startswith("/"):
            new_path = "/" + new_path
        from urllib.parse import urlunparse
        return urlunparse((parsed.scheme, new_netloc, new_path,
                           parsed.params, parsed.query, parsed.fragment))

    if not path.startswith("/"):
        path = "/" + path
    if username:
        return f"rtsp://{quote(username, safe='')}:{quote(password or '', safe='')}@{ip}:{port}{path}"
    return f"rtsp://{ip}:{port}{path}"

def get_registered_cameras() -> List[CameraConfig]:
    return _load_config_cameras()

def register_camera(
    name: str,
    ip: str = "",
    port: int = 0,
    username: str = "admin",
    password: str = "",
    rtsp_port: int = 554,
    rtsp_path: str = "/md0_0",
    device_class: str = "direct_connect",
    connection_type: str = "onvif",
    sn_code: str = "",
    pkdk: str = "",
    rtsp_sub_path: str = "/md0_1",
    illumination_modes: Optional[List[str]] = None,
    protocol_type: str = "",
    onvif_sn: str = "",
) -> RegisterResult:
    name = coerce_str(name)
    username = coerce_str(username)
    password = _to_plain(coerce_str(password))
    sn_code = _to_plain(coerce_str(sn_code))
    pkdk = _to_plain(coerce_str(pkdk))
    onvif_sn = coerce_str(onvif_sn)

    import os
    import yaml

    config_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
    config_path = os.path.join(config_dir, "config.yaml")

    if not os.path.exists(config_path):
        alt_path = os.path.join(config_dir, "config.yaml")
        if os.path.exists(alt_path):
            config_path = alt_path

    data = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            data = {}

    cameras = data.get("cameras", [])

    if not password or not sn_code or not protocol_type or not onvif_sn:
        existing = None
        for cam in cameras:
            if cam.get("name") == name:
                existing = cam
                break
        if existing is None and ip:
            for cam in cameras:
                if cam.get("ip") == ip:
                    existing = cam
                    break
        if existing is None and sn_code:
            for cam in cameras:
                if _dec(cam.get("sn_code")) == sn_code or _dec(cam.get("sn")) == sn_code:
                    existing = cam
                    break
        if existing:
            if not password and existing.get("password"):
                password = _dec(existing["password"])
            if not sn_code:
                sn_code = _dec(existing.get("sn_code")) or _dec(existing.get("sn"))
            if not protocol_type:
                protocol_type = existing.get("protocol_type") or ""
            if not onvif_sn:
                onvif_sn = existing.get("onvif_sn") or ""

    new_entry = {
        "name": name,
        "connection_type": connection_type,
        "ip": ip,
        "port": port,
        "onvif_port": port,
        "username": username,
        "password": _enc(password),
        "rtsp_port": rtsp_port,
        "rtsp_path": rtsp_path,
        "rtsp_path_main": rtsp_path,
        "rtsp_sub_path": rtsp_sub_path,
        "rtsp_path_sub": rtsp_sub_path,
        "device_class": device_class,
        "sn_code": _enc(sn_code),
        "sn": _enc(sn_code),
        "pkdk": _enc(pkdk),
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    if protocol_type:
        new_entry["protocol_type"] = protocol_type
    if onvif_sn:
        new_entry["onvif_sn"] = onvif_sn
    if illumination_modes:
        new_entry["illumination_modes"] = illumination_modes

    found = False

    for i, cam in enumerate(cameras):
        if cam.get("name") == name:
            cameras[i] = new_entry
            found = True
            break

    if not found and ip:
        for i, cam in enumerate(cameras):
            if cam.get("ip") == ip:
                cameras[i] = new_entry
                found = True
                break

    if not found and sn_code:
        for i, cam in enumerate(cameras):
            if _dec(cam.get("sn_code")) == sn_code or _dec(cam.get("sn")) == sn_code:
                cameras[i] = new_entry
                found = True
                break

    if not found and onvif_sn:
        for i, cam in enumerate(cameras):
            if cam.get("onvif_sn") == onvif_sn:
                cameras[i] = new_entry
                found = True
                break
    if not found:
        cameras.append(new_entry)

    data["cameras"] = cameras

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        return RegisterResult(success=True, camera_name=name)
    except Exception as e:
        return RegisterResult(success=False, camera_name=name, error_message=str(e))

def search_devices(
    method: Optional[DiscoveryMethod] = None,
    timeout: float = 15.0,
) -> SearchResult:

    if method is not None:
        if method == DiscoveryMethod.SKY_DISCOVERY:
            result = _search_sky_devices(timeout)
        elif method == DiscoveryMethod.JCP_DISCOVERY:
            result = _search_jcp_devices(timeout)
        else:
            result = _search_ws_discovery_devices(timeout)
        if result.success:
            _sync_registry_with_discovery(result.devices)
        return result

    all_devices: List[DiscoveredDevice] = []
    seen_ips: set = set()
    errors: List[str] = []

    for search_fn in (_search_sky_devices, _search_jcp_devices, _search_ws_discovery_devices):
        try:
            result = search_fn(timeout)
            if result.success:
                for dev in result.devices:
                    if dev.ip not in seen_ips:
                        seen_ips.add(dev.ip)
                        all_devices.append(dev)
            elif result.error_message:
                errors.append(result.error_message)
        except Exception as e:
            errors.append(str(e))

    if not all_devices and errors:
        return SearchResult(
            success=False,
            devices=[],
            error_message="; ".join(errors),
        )

    _sync_registry_with_discovery(all_devices, prune=not errors)
    return SearchResult(success=True, devices=all_devices)

def _sync_registry_with_discovery(
    devices: List[DiscoveredDevice],
    prune: bool = True,
) -> None:

    try:
        existing = _load_config_cameras()
    except Exception:
        return

    for dev in devices:
        if dev.rtsp_access == "unreachable":
            continue
        name = _dev_to_name(dev)
        prev = _match_config_entry(existing, name, dev.ip, dev.sn_code)
        device_class = (
            dev.device_class.value if isinstance(dev.device_class, DeviceClass)
            else str(dev.device_class)
        )
        try:
            register_camera(
                name=name,
                ip=dev.ip,
                port=dev.onvif_port or (prev.port if prev else 0),
                username=(
                    "" if device_class == DeviceClass.DIRECT_CONNECT.value
                    else ((prev.username if prev else "") or "admin")
                ),
                password="",
                rtsp_port=dev.rtsp_port,
                rtsp_path=(dev.supported_media[0] if dev.supported_media else "/md0_0"),
                rtsp_sub_path=(prev.rtsp_sub_path if prev else "") or "/md0_1",
                device_class=device_class,
                connection_type=(prev.connection_type if prev else "") or "onvif",
                sn_code=dev.sn_code,
                pkdk=prev.pkdk if prev else "",
                illumination_modes=(prev.illumination_modes or None) if prev else None,
                protocol_type=dev.protocol_type,
            )
        except Exception:
            continue

    if not prune:
        return

    discovered_ips = {d.ip for d in devices if d.ip}
    discovered_sns = {d.sn_code for d in devices if d.sn_code}
    for prev in existing:
        if not _is_ipv4_literal(prev.ip):
            continue
        if prev.ip in discovered_ips or (prev.sn_code and prev.sn_code in discovered_sns):
            continue
        try:
            access = _probe_stream_access(prev.ip, prev.rtsp_port, prev.rtsp_path)
        except Exception:
            continue
        if access == "unreachable":
            _remove_camera_config(prev.name)

def _match_config_entry(
    entries: List[CameraConfig], name: str, ip: str, sn_code: str,
    onvif_sn: str = "",
) -> Optional[CameraConfig]:
    for cam in entries:
        if name and cam.name == name:
            return cam
    for cam in entries:
        if ip and cam.ip == ip:
            return cam
    if sn_code:
        for cam in entries:
            if cam.sn_code == sn_code:
                return cam
    if onvif_sn:
        for cam in entries:
            if cam.onvif_sn == onvif_sn:
                return cam
    return None

def _is_ipv4_literal(value: str) -> bool:
    parts = (value or "").split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

_SEARCH_SETTLE_WINDOW = 1.0
_SEARCH_SETTLE_ROUNDS = 2

def _search_sky_devices(timeout: float) -> SearchResult:
    try:
        deadline = time.monotonic() + timeout
        discovered: Dict[str, Any] = {}
        empty_rounds = 0
        while empty_rounds < _SEARCH_SETTLE_ROUNDS:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            batch = discover_sky_devices(timeout=min(_SEARCH_SETTLE_WINDOW, remaining))
            found_new = False
            for sd in batch:
                if sd.ip not in discovered:
                    discovered[sd.ip] = sd
                    found_new = True
            empty_rounds = 0 if found_new else empty_rounds + 1

        devices = []
        for sd in discovered.values():
            rtsp_path = sd.rtsp_paths[0] if sd.rtsp_paths else "/md0_0"
            access = _probe_stream_access(sd.ip, sd.rtsp_port, rtsp_path)
            device_class = (
                DeviceClass.DIRECT_CONNECT if access == "open"
                else DeviceClass.PASSWORD_REQUIRED
            )
            dev = DiscoveredDevice(
                ip=sd.ip,
                onvif_port=0,
                rtsp_port=sd.rtsp_port,
                device_class=device_class,
                sn_code=sd.sn,
                model=sd.model,
                manufacturer=sd.manufacturer,
                supported_media=[s for s in sd.rtsp_paths],
                sky_subtype=sd.subtype,
                sky_name=sd.name,
                sky_dtype=sd.dtype,
                sky_hw_version=sd.hw_version,
                sky_sw_version=sd.sw_version,
                sky_did=sd.did,
                sky_channels=sd.channels,
                sky_channel_list=sd.channel_list,
                sky_web_port=sd.web_port,
                sky_udp_port=sd.udp_port,
                sky_net_type=sd.net_type,
                sky_ip_mode=sd.ip_mode,
                sky_mask=sd.mask,
                sky_gateway=sd.gateway,
                sky_mac=sd.mac,
                discovery_method="sky_discovery",
                protocol_type="S",
                rtsp_access=access,
            )
            devices.append(dev)
        return SearchResult(
            success=True,
            devices=devices,
        )
    except Exception as e:
        return SearchResult(
            success=False,
            error_message=str(e),
        )

def _search_jcp_devices(timeout: float) -> SearchResult:
    try:
        deadline = time.monotonic() + min(timeout, 5.0)
        discovered: Dict[str, Dict[str, Any]] = {}
        empty_rounds = 0
        while empty_rounds < _SEARCH_SETTLE_ROUNDS:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            batch = camera_proto.jcp_search(timeout=min(_SEARCH_SETTLE_WINDOW, remaining))
            found_new = False
            for jd in batch:
                dev_ip = jd.get("ip", "")
                if dev_ip and dev_ip not in discovered:
                    discovered[dev_ip] = jd
                    found_new = True
            empty_rounds = 0 if found_new else empty_rounds + 1

        devices = []
        notes = []
        for jd in discovered.values():
            dev_ip = jd.get("ip", "")
            sn = (jd.get("sn") or "").strip()
            raw_port = jd.get("rtsp_port", camera_proto.JCP_RTSP_PORT)
            try:
                rtsp_port = int(raw_port)
                if not 1 <= rtsp_port <= 65535:
                    raise ValueError
            except (TypeError, ValueError):
                rtsp_port = camera_proto.JCP_RTSP_PORT
                notes.append(f"{dev_ip}: ignoring invalid JCP RTSP port {raw_port!r}; using {rtsp_port}")

            access = _probe_stream_access(dev_ip, rtsp_port, camera_proto.JCP_RTSP_PATH_MAIN)
            devices.append(DiscoveredDevice(
                ip=dev_ip,
                onvif_port=0,
                rtsp_port=rtsp_port,
                device_class=(
                    DeviceClass.DIRECT_CONNECT if access == "open"
                    else DeviceClass.PASSWORD_REQUIRED
                ),
                sn_code=sn,
                model=jd.get("model", ""),
                manufacturer=jd.get("name", ""),
                supported_media=[camera_proto.JCP_RTSP_PATH_MAIN, camera_proto.JCP_RTSP_PATH_SUB],
                sky_mac=jd.get("mac", ""),
                discovery_method="jcp_discovery",
                protocol_type="",
                rtsp_access=access,
            ))
        return SearchResult(success=True, devices=devices, error_message="; ".join(notes))
    except Exception as e:
        return SearchResult(success=False, error_message=f"JCP discovery failed: {e}")

def _search_ws_discovery_devices(timeout: float) -> SearchResult:
    import select
    import uuid

    probe_wait = max(1.0, min(timeout, 15.0))

    socks = []
    for local_ip in _list_local_ipv4():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((local_ip, 0))
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
                         socket.inet_aton(local_ip))
            s.setblocking(False)
            probe = _WS_PROBE_TEMPLATE.format(msg_id=uuid.uuid4()).encode("utf-8")
            s.sendto(probe, (_WS_DISCOVERY_ADDR, _WS_DISCOVERY_PORT))
            socks.append(s)
        except Exception:
            try:
                s.close()
            except Exception:
                pass

    if not socks:
        return SearchResult(
            success=False,
            error_message="No available network interface; WS-Discovery probe failed",
        )

    found: Dict[str, dict] = {}
    deadline = time.monotonic() + probe_wait
    last_new = time.monotonic()
    while time.monotonic() < deadline:
        try:
            ready, _, _ = select.select(socks, [], [], 0.5)
        except Exception:
            break
        got_new = False
        for s in ready:
            try:
                data, addr = s.recvfrom(65535)
            except Exception:
                continue
            info = _parse_ws_probe_match(data)
            if info and addr[0] not in found:
                found[addr[0]] = info
                got_new = True
        if got_new:
            last_new = time.monotonic()
        elif time.monotonic() - last_new >= _SEARCH_SETTLE_WINDOW:
            break
    for s in socks:
        try:
            s.close()
        except Exception:
            pass

    devices = []
    for ip, info in sorted(found.items()):
        access = _probe_stream_access(ip, 554, "/md0_0")
        device_class = (
            DeviceClass.DIRECT_CONNECT if access == "open"
            else DeviceClass.PASSWORD_REQUIRED
        )

        sn = _probe_sn_via_sky(ip, timeout=2.0)
        devices.append(DiscoveredDevice(
            ip=ip,
            onvif_port=info["onvif_port"],
            rtsp_port=554,
            device_class=device_class,
            sn_code=sn,
            model=info["model"],
            manufacturer=info["brand"],
            discovery_method="ws_discovery",
            protocol_type="",
            rtsp_access=access,
        ))

    return SearchResult(success=True, devices=devices)

_WS_DISCOVERY_ADDR = "239.255.255.250"
_WS_DISCOVERY_PORT = 3702

_WS_PROBE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:tds="http://schemas.xmlsoap.org/ws/2005/04/discovery"
            xmlns:tns="http://www.onvif.org/ver10/network/wsdl/RemoteDiscoveryBinding">
  <s:Header>
    <wsa:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action>
    <wsa:MessageID>uuid:{msg_id}</wsa:MessageID>
    <wsa:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To>
  </s:Header>
  <s:Body>
    <tds:Probe>
      <tds:Types>tns:NetworkVideoTransmitter</tds:Types>
    </tds:Probe>
  </s:Body>
</s:Envelope>"""

def _list_local_ipv4() -> List[str]:
    addrs: List[str] = []
    try:
        import psutil
        for _, addr_list in psutil.net_if_addrs().items():
            for a in addr_list:
                if a.family == socket.AF_INET and not a.address.startswith("127."):
                    addrs.append(a.address)
    except Exception:
        pass
    if not addrs:

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            addrs.append(s.getsockname()[0])
            s.close()
        except Exception:
            pass
    return addrs

def _parse_ws_probe_match(data: bytes) -> Optional[dict]:
    import xml.etree.ElementTree as ET
    from urllib.parse import unquote

    try:
        text = data.decode("utf-8", errors="ignore")
        start = text.find("<")
        if start < 0:
            return None
        root = ET.fromstring(text[start:])
    except Exception:
        return None

    def _find_text(tag: str) -> str:
        for elem in root.iter():
            if elem.tag.endswith("}" + tag) or elem.tag == tag:
                return (elem.text or "").strip()
        return ""

    types_text = _find_text("Types")
    if types_text and "NetworkVideoTransmitter" not in types_text:
        return None

    xaddrs = _find_text("XAddrs")
    onvif_port = 0
    if xaddrs:
        try:
            parsed = urlparse(xaddrs.split()[0])

            onvif_port = parsed.port or 80
        except Exception:
            pass

    brand = ""
    model = ""
    for scope in _find_text("Scopes").split():
        if "/name/" in scope:
            brand = unquote(scope.split("/name/")[-1])
        elif "/hardware/" in scope:
            model = unquote(scope.split("/hardware/")[-1])

    return {"onvif_port": onvif_port, "xaddrs": xaddrs, "brand": brand, "model": model}

def _probe_sn_via_sky(ip: str, timeout: float = 3.0) -> str:
    try:
        return probe_device_sn(ip=ip, timeout=timeout)
    except Exception:
        return ""

def _probe_sn_via_jcp(ip: str, timeout: float = 3.0) -> str:
    try:
        for dev in camera_proto.jcp_search(timeout=timeout):
            if dev.get("ip") == ip:
                return (dev.get("sn") or "").strip()
    except Exception:
        pass
    return ""

def _probe_sn_and_protocol(ip: str, timeout: float = 3.0) -> Tuple[str, str]:
    """Return (protocol_type, sn).

    SK is probed first: a device answering both discoveries must stay on the SK
    path, since SK exposes strictly more capabilities than JCP.
    """

    sn = _probe_sn_via_sky(ip, timeout=timeout)
    if sn:
        return "S", sn
    sn = _probe_sn_via_jcp(ip, timeout=timeout)
    if sn:
        return "J", sn
    return "", ""

def _apply_onvif_stream_paths(camera_name: str, main: str, sub: str) -> Tuple[str, str]:
    """Override the assumed RTSP paths with the ONVIF-reported ones.

    ONVIF GetStreamUri is the device's own answer, so it outranks any per-model guess.
    """

    conn = _connected_devices.get(camera_name) or {}
    cam = conn.get("onvif_camera")
    if cam is None:
        return main, sub
    try:
        media = cam.create_media_service()
        paths = []
        for profile in media.GetProfiles()[:2]:
            uri = media.GetStreamUri({
                "StreamSetup": {
                    "Stream": "RTP-Unicast",
                    "Transport": {"Protocol": "RTSP"},
                },
                "ProfileToken": profile.token,
            })
            path = urlparse(uri.Uri).path
            paths.append(path if path.startswith("/") else "")
    except Exception:
        return main, sub

    if len(paths) > 0 and paths[0]:
        main = paths[0]
    if len(paths) > 1 and paths[1]:
        sub = paths[1]
    if conn:
        conn["rtsp_path"] = main
        conn["rtsp_sub_path"] = sub
    return main, sub

def _cloud_auth_and_connect(
    camera_name: str,
    ip: str,
    port: int,
    sn_code: str,
    rtsp_port: int,
    rtsp_path: str,
    username: str,
    cached: Optional[CameraConfig] = None,
    protocol_type: str = "",
) -> ConnectResult:

    if protocol_type == "O":
        return ConnectResult(
            success=False, status="needs_password",
            needs_password=True,
            error_message=(
                f"Device {camera_name}({ip}) is a third-party ONVIF (O-class) device without an SK/JCP SN; "
                f"cloud authorization is not supported. Enter the password directly and call connect_device."
            ),
            protocol_type="O",
        )

    if not sn_code:
        return ConnectResult(
            success=False, status="needs_password",
            needs_password=True,
            error_message=(
                f"Device {camera_name}({ip}) has no SN; cloud authorization cannot start. "
                f"Enter the password directly and call connect_device."
            ),
        )

    cr = request_cloud_auth(sn_code)
    if not cr.success:
        if cr.station_default and cr.http_status == 500:
            message = f"Default station authorization returned HTTP 500. Enter the password for device {camera_name}({ip}) directly."
        else:
            message = (
                f"Cloud authorization service unavailable ({cr.error_message}). "
                f"Enter the password for device {camera_name}({ip}) directly."
            )
        return ConnectResult(
            success=False, status="needs_password",
            needs_password=True,
            error_message=message,
        )

    register_camera(
        name=camera_name, ip=ip, port=port,
        username=username, password="",
        rtsp_port=rtsp_port, rtsp_path=rtsp_path,
        device_class="password_required",
        sn_code=sn_code,
        connection_type=cached.connection_type if cached else "onvif",
        protocol_type=protocol_type,
    )

    poll_interval = 5
    max_polls = 60
    for _ in range(max_polls):
        time.sleep(poll_interval)
        result = poll_auth_status(camera_name)

        if result.status == AuthStatus.AUTHORIZED:

            conn = _try_connect_with_password(
                camera_name, ip, port, rtsp_port, rtsp_path,
                username, result.device_pwd,
            )
            if conn.success:

                effective_port = conn.onvif_port or port
                main_path, sub_path = rtsp_path, ""
                if protocol_type in ("J", "O"):
                    main_path, sub_path = _apply_onvif_stream_paths(
                        camera_name, rtsp_path, cached.rtsp_sub_path if cached else "/md0_1",
                    )

                register_camera(
                    name=camera_name, ip=ip,
                    port=effective_port,
                    username=username, password=result.device_pwd,
                    rtsp_port=rtsp_port, rtsp_path=main_path,
                    rtsp_sub_path=sub_path or "/md0_1",
                    device_class="password_required",
                    sn_code=sn_code,
                    connection_type=cached.connection_type if cached else "onvif",
                    protocol_type=protocol_type,
                )

                if protocol_type not in ("J", "O"):
                    _probe_and_save_illumination(
                        camera_name, ip, effective_port,
                        username, result.device_pwd, cached,
                    )
                conn.auth_method = "cloud_password"
                conn.protocol_type = protocol_type
                return conn
            else:

                return ConnectResult(
                    success=False, status="cloud_pwd_failed",
                    needs_password=True,
                    error_message=(
                        f"The cloud-issued password failed device verification for {camera_name}({ip}) "
                        f"({conn.error_message}); the device may have changed its password or has credential isolation. "
                        f"Enter the correct password."
                    ),
                )

        elif result.status == AuthStatus.REJECTED:
            return ConnectResult(
                success=False, status="auth_rejected",
                error_message=(
                    f"User rejected the cloud authorization request for device {camera_name}({ip}); cannot connect."
                ),
            )

        elif result.status == AuthStatus.ERROR:
            return ConnectResult(
                success=False, status="needs_password",
                needs_password=True,
                error_message=(
                    f"Cloud authorization error ({result.message}). "
                    f"Enter the password for device {camera_name}({ip}) directly."
                ),
            )

    return ConnectResult(
        success=False, status="needs_password",
        needs_password=True,
        error_message=(
            f"Cloud authorization timed out after 5 minutes; user did not confirm"
            f"{' (device has no station record; the APP may not have received the request)' if cr.station_default else ''}. "
            f"Enter the password for device {camera_name}({ip}) directly."
        ),
    )

def connect_device(
    camera_name: str,
    password: Optional[str] = None,
    ip: Optional[str] = None,
    port: Optional[int] = None,
    rtsp_port: Optional[int] = None,
    rtsp_path: str = "/md0_0",
    username: str = "admin",
    sn_code: str = "",
    device_class: str = "",
    protocol_type: str = "",
) -> ConnectResult:
    camera_name = coerce_str(camera_name)
    username = coerce_str(username)
    password = _to_plain(coerce_str(password))
    sn_code = _to_plain(coerce_str(sn_code))

    cached = _find_cached_camera(camera_name)

    effective_sn = (cached.sn_code if cached and cached.sn_code else "") or sn_code
    effective_protocol = (cached.protocol_type if cached else "") or protocol_type
    if cached and cached.ip:
        dev_ip = cached.ip
        dev_port = cached.port
        dev_rtsp_port = cached.rtsp_port
        dev_rtsp_path = cached.rtsp_path
        dev_username = cached.username or username
        dev_pwd = password or cached.password or ""
        dev_class = cached.device_class or ""
    elif ip:
        dev_ip = ip
        dev_port = port or 0
        dev_rtsp_port = rtsp_port or 554
        dev_rtsp_path = rtsp_path
        dev_username = username
        dev_pwd = password or ""
        dev_class = device_class
    else:
        return ConnectResult(
            success=False, status="failed",
            error_message=f"Connection info for device {camera_name} not found (no config.yaml record and no IP provided)",
        )

    if dev_pwd:
        max_attempts = 3 if (cached and not password) else 1
        last_result = ConnectResult(success=False, status="failed")
        for attempt in range(1, max_attempts + 1):
            last_result = _try_connect_with_password(
                camera_name, dev_ip, dev_port, dev_rtsp_port, dev_rtsp_path,
                dev_username, dev_pwd,
            )
            if last_result.success:
                break
            if attempt < max_attempts:
                time.sleep(1.0)

        if last_result.success:

            cached_class = cached.protocol_type if cached else ""
            conn_state = _connected_devices.get(camera_name) or {}
            probed_protocol = ""
            if not effective_sn or not effective_protocol:
                probed_protocol, probed_sn = _probe_sn_and_protocol(dev_ip)
                effective_sn = effective_sn or probed_sn
                effective_protocol = effective_protocol or probed_protocol
            if cached_class == "O" and effective_sn and probed_protocol:
                effective_protocol = probed_protocol
            if not effective_sn:
                if cached_class in ("S", "J"):
                    _connected_devices.pop(camera_name, None)
                    return ConnectResult(
                        success=False, status="no_sn",
                        error_message=(
                            f"Device {camera_name}({dev_ip}) passed password verification but SN probing failed; "
                            f"refused to enter connected state (connected devices must have an SN registered in config, "
                            f"otherwise all SN-dependent features will fail). "
                            f"Confirm the device supports SK or JCP discovery, then retry."
                        ),
                        protocol_type=cached_class,
                    )
                if cached_class == "O" or conn_state.get("onvif_verified"):
                    effective_protocol = "O"
                else:
                    _connected_devices.pop(camera_name, None)
                    return ConnectResult(
                        success=False, status="failed",
                        error_message=(
                            f"Device {camera_name}({dev_ip}) is only reachable over RTSP; ONVIF control-plane verification failed "
                            f"and there is no SK/JCP response; device identity cannot be confirmed; refused to enter connected state."
                        ),
                    )

            verified_port = last_result.onvif_port
            port_changed = bool(verified_port) and (not cached or cached.port != verified_port)
            protocol_changed = bool(effective_protocol) and (
                not cached or cached.protocol_type != effective_protocol
            )
            main_path, sub_path = dev_rtsp_path, ""
            if effective_protocol in ("J", "O"):
                main_path, sub_path = _apply_onvif_stream_paths(
                    camera_name, dev_rtsp_path,
                    (cached.rtsp_sub_path if cached else "") or "/md0_1",
                )
            if not cached or cached.password != dev_pwd or port_changed or protocol_changed:
                register_camera(
                    name=camera_name, ip=dev_ip,
                    port=verified_port or (cached.port if cached else 0),
                    username=dev_username, password=dev_pwd,
                    rtsp_port=dev_rtsp_port, rtsp_path=main_path,
                    rtsp_sub_path=sub_path or (cached.rtsp_sub_path if cached else "") or "/md0_1",
                    device_class=dev_class or "password_required",
                    sn_code=effective_sn or (cached.sn_code if cached else ""),
                    connection_type=cached.connection_type if cached else "onvif",
                    protocol_type=effective_protocol,
                    onvif_sn=conn_state.get("onvif_sn", "") or (cached.onvif_sn if cached else ""),
                )

            if effective_protocol not in ("J", "O"):
                _probe_and_save_illumination(
                    camera_name, dev_ip,
                    verified_port or (cached.port if cached else 0),
                    dev_username, dev_pwd, cached,
                )
            ok_result: ConnectResult = last_result
            ok_result.protocol_type = effective_protocol
            return ok_result

        if cached and not password:

            if effective_sn:
                cloud_result = _cloud_auth_and_connect(
                    camera_name, dev_ip, dev_port, effective_sn,
                    dev_rtsp_port, dev_rtsp_path, dev_username,
                    cached=cached,
                    protocol_type=effective_protocol,
                )
                if cloud_result.success:
                    return cloud_result

            _remove_camera_config(camera_name)
            return ConnectResult(
                success=False, status="needs_password",
                needs_password=True,
                error_message=(
                    f"Cached credentials cleared (invalid: {last_result.error_message}). "
                    f"Cloud re-auth re-issued the same stale credential; "
                    f"approving again cannot pass device verification. "
                    f"Enter the current correct password for device {camera_name}({dev_ip}) manually."
                ),
            )
        return ConnectResult(
            success=False, status="failed",
            needs_password=True,
            error_message=f"Password authentication failed: {last_result.error_message}; verify the password and retry",
        )

    if dev_class == "password_required":
        if not effective_sn or not effective_protocol:
            probed_protocol, probed_sn = _probe_sn_and_protocol(dev_ip)
            effective_sn = effective_sn or probed_sn
            effective_protocol = effective_protocol or probed_protocol
        if not effective_sn and effective_protocol not in ("S", "J"):
            return ConnectResult(
                success=False, status="needs_password",
                needs_password=True,
                error_message=(
                    f"Device {camera_name}({dev_ip}) is a non-XPAI ONVIF device (no SN, "
                    f"no cloud authorization channel); provide the device password directly and retry."
                ),
                protocol_type=effective_protocol,
            )
        return _cloud_auth_and_connect(
            camera_name, dev_ip, dev_port, effective_sn,
            dev_rtsp_port, dev_rtsp_path, dev_username,
            cached=cached,
            protocol_type=effective_protocol,
        )

    access = _probe_stream_access(dev_ip, dev_rtsp_port, dev_rtsp_path)

    if access == "open":

        cached_class = cached.protocol_type if cached else ""
        probed_sn = effective_sn
        probed_protocol = ""
        if not probed_sn or not effective_protocol:
            probed_protocol, probed_sn = _probe_sn_and_protocol(dev_ip)
            effective_protocol = effective_protocol or probed_protocol
        if cached_class == "O" and probed_sn and probed_protocol:
            effective_protocol = probed_protocol

        verified_port = _probe_onvif_port(dev_ip, hint_port=dev_port)

        onvif_cam = None
        onvif_serial = ""
        if verified_port or dev_port:
            try:
                from onvif import ONVIFCamera
                onvif_cam = ONVIFCamera(host=dev_ip, port=verified_port or dev_port,
                                        user=dev_username or "admin", passwd=dev_pwd or "")
                dev_info = onvif_cam.create_devicemgmt_service().GetDeviceInformation()
                onvif_serial = getattr(dev_info, "SerialNumber", "") or ""
            except Exception:
                onvif_cam = None

        if not probed_sn:
            if cached_class in ("S", "J"):
                return ConnectResult(
                    success=False, status="no_sn",
                    error_message=(
                        f"Device {camera_name}({dev_ip}) reachable without password but SN probing failed; "
                        f"refused to enter connected state (connected devices must have an SN registered in config, "
                        f"otherwise all SN-dependent features will fail). "
                        f"Confirm the device supports SK or JCP discovery and is reachable, then retry."
                    ),
                    protocol_type=cached_class,
                )
            if cached_class == "O" or onvif_cam is not None:
                effective_protocol = "O"
            else:
                return ConnectResult(
                    success=False, status="failed",
                    error_message=(
                        f"Device {camera_name}({dev_ip}) is only reachable over RTSP; ONVIF control-plane verification failed "
                        f"and there is no SK/JCP response; device identity cannot be confirmed; refused to enter connected state."
                    ),
                )

        conn_info = {
            "ip": dev_ip,
            "port": verified_port or dev_port,
            "rtsp_port": dev_rtsp_port,
            "rtsp_path": dev_rtsp_path,

            "rtsp_sub_path": (cached.rtsp_sub_path if cached and cached.rtsp_sub_path else "") or "/md0_1",
            "username": "",
            "password": "",
            "sn_code": probed_sn,
        }
        if onvif_cam is not None:
            conn_info["onvif_camera"] = onvif_cam
            conn_info["onvif_verified"] = True
            conn_info["onvif_sn"] = onvif_serial
        _connected_devices[camera_name] = conn_info

        main_path, sub_path = dev_rtsp_path, conn_info["rtsp_sub_path"]
        if effective_protocol in ("J", "O"):
            main_path, sub_path = _apply_onvif_stream_paths(camera_name, main_path, sub_path)

        protocol_changed = bool(effective_protocol) and (
            not cached or cached.protocol_type != effective_protocol
        )
        if not cached or not cached.sn_code or protocol_changed:
            register_camera(
                name=camera_name, ip=dev_ip, port=verified_port,
                username="", password="",
                rtsp_port=dev_rtsp_port, rtsp_path=main_path,
                rtsp_sub_path=sub_path,
                device_class="direct_connect",
                sn_code=probed_sn,
                protocol_type=effective_protocol,
                onvif_sn=onvif_serial or (cached.onvif_sn if cached else ""),
            )

        if effective_protocol not in ("J", "O"):
            _probe_and_save_illumination(
                camera_name, dev_ip, verified_port or dev_port,
                dev_username or "", dev_pwd or "", cached,
            )
        return ConnectResult(
            success=True,
            auth_method="direct",
            status="connected",
            protocol_type=effective_protocol,
        )

    if access == "auth_required":

        if not effective_sn or not effective_protocol:
            probed_protocol, probed_sn = _probe_sn_and_protocol(dev_ip)
            effective_sn = effective_sn or probed_sn
            effective_protocol = effective_protocol or probed_protocol
        if not effective_sn and effective_protocol not in ("S", "J"):
            return ConnectResult(
                success=False, status="needs_password",
                needs_password=True,
                error_message=(
                    f"Device {camera_name}({dev_ip}) is a non-XPAI ONVIF device (no SN, "
                    f"no cloud authorization channel); provide the device password directly and retry."
                ),
                protocol_type=effective_protocol,
            )
        return _cloud_auth_and_connect(
            camera_name, dev_ip, dev_port, effective_sn,
            dev_rtsp_port, dev_rtsp_path, dev_username,
            cached=cached,
            protocol_type=effective_protocol,
        )

    return ConnectResult(
        success=False,
        status="failed",
        error_message=f"Device {dev_ip} unreachable (RTSP port {dev_rtsp_port} no response)",
    )

_connected_devices: Dict[str, dict] = {}

def _probe_and_save_illumination(
    camera_name: str,
    ip: str,
    port: int,
    username: str,
    password: str,
    cached: Optional[CameraConfig] = None,
) -> List[str]:

    if cached and cached.illumination_modes:
        return cached.illumination_modes
    try:
        from .illumination import probe_illumination_capability

        if cached is None:
            cached = next(
                (c for c in _load_config_cameras() if c.name == camera_name), None
            )
        result = probe_illumination_capability(name=camera_name)
        modes = (
            [c.get("name", "") for c in result.capabilities
             if isinstance(c, dict) and c.get("name")]
            if result.ok else []
        )
        if modes:
            register_camera(
                name=camera_name, ip=ip, port=port,
                username=username, password=password,
                rtsp_port=cached.rtsp_port if cached else 554,
                rtsp_path=cached.rtsp_path if cached else "/md0_0",
                device_class=cached.device_class if cached else "",
                sn_code=cached.sn_code if cached else "",
                connection_type=cached.connection_type if cached else "onvif",
                illumination_modes=modes,
            )
            return modes
    except Exception:
        pass
    return []

def _remove_camera_config(name: str) -> bool:
    if _yaml_lib is None:
        return False
    try:
        if not CONFIG_PATH.exists():
            return False
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = _yaml_lib.safe_load(f) or {}
        cameras = data.get("cameras", [])
        new_cameras = [c for c in cameras if c.get("name") != name]
        if len(new_cameras) == len(cameras):
            return False
        data["cameras"] = new_cameras
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            _yaml_lib.safe_dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception:
        return False

def _try_connect_with_password(
    camera_name: str,
    ip: str,
    onvif_port: int,
    rtsp_port: int,
    rtsp_path: str,
    username: str,
    password: str,
) -> ConnectResult:
    password = _to_plain(password)

    verified_port = _probe_onvif_port(ip, hint_port=onvif_port)
    effective_port = verified_port or onvif_port

    _cached_cfg = _find_cached_camera(camera_name)
    sub_path = (_cached_cfg.rtsp_sub_path if _cached_cfg and _cached_cfg.rtsp_sub_path else "") or "/md0_1"

    conn = {
        "ip": ip, "port": effective_port,
        "rtsp_port": rtsp_port, "rtsp_path": rtsp_path,
        "rtsp_sub_path": sub_path,
        "username": username, "password": password,
    }
    _connected_devices[camera_name] = conn

    if effective_port:
        try:
            from onvif import ONVIFCamera
            cam = ONVIFCamera(host=ip, port=effective_port, user=username, passwd=password)
            dev_info = cam.create_devicemgmt_service().GetDeviceInformation()
            conn["onvif_camera"] = cam
            conn["onvif_verified"] = True
            conn["onvif_sn"] = getattr(dev_info, "SerialNumber", "") or ""
        except Exception:
            pass

    rtsp_access = _probe_stream_access(ip, rtsp_port, rtsp_path, username, password)

    if rtsp_access == "open":
        return ConnectResult(
            success=True, auth_method="password", status="connected",
            onvif_port=verified_port,
        )

    _connected_devices.pop(camera_name, None)

    if rtsp_access == "auth_required":
        return ConnectResult(
            success=False, status="failed",
            error_message="RTSP authentication failed (password may be invalid for RTSP)",
        )
    if rtsp_access == "unreachable":
        return ConnectResult(
            success=False, status="failed",
            error_message="RTSP port unreachable; password not verified over RTSP",
        )
    return ConnectResult(
        success=False, status="failed",
        error_message="ONVIF/RTSP all failed to connect",
    )

def _rtsp_read_response_head(sock) -> str:
    response = b""
    while True:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            if b"\r\n\r\n" in response:
                break
        except socket.timeout:
            break
    return response.decode("utf-8", errors="ignore")

def _rtsp_status_code(resp_text: str) -> int:
    import re
    first_line = resp_text.split("\r\n", 1)[0].split("\n", 1)[0].strip()
    m = re.match(r"^RTSP/\d+\.\d+\s+(\d{3})", first_line)
    return int(m.group(1)) if m else 0

def _rtsp_send_describe(sock, rtsp_url: str, cseq: int, auth_header: str = "") -> str:
    request = (
        f"DESCRIBE {rtsp_url} RTSP/1.0\r\n"
        f"CSeq: {cseq}\r\n"
        f"Accept: application/sdp\r\n"
        f"{auth_header}"
        f"\r\n"
    )
    sock.sendall(request.encode("utf-8"))
    return _rtsp_read_response_head(sock)

def _parse_www_authenticate(resp_text: str) -> List[Dict[str, Any]]:
    import re
    challenges: List[Dict[str, Any]] = []
    for line in resp_text.splitlines():
        if ":" not in line:
            continue
        name, _, value = line.partition(":")
        if name.strip().lower() != "www-authenticate":
            continue
        m = re.match(r"\s*(Basic|Digest)\s*(.*)", value, re.IGNORECASE)
        if not m:
            continue
        params: Dict[str, str] = {}
        for key, quoted, plain in re.findall(
            r'([a-zA-Z][a-zA-Z0-9_-]*)=(?:"([^"]*)"|([^\s,]+))', m.group(2)
        ):
            params[key.lower()] = quoted if quoted else plain.rstrip(",")
        challenges.append({"scheme": m.group(1).lower(), "params": params})
    return challenges

def _build_rtsp_digest_header(
    params: Dict[str, str],
    username: str,
    password: str,
    method: str,
    uri: str,
) -> str:
    def _md5(s: str) -> str:
        return hashlib.md5(s.encode("utf-8")).hexdigest()

    realm = params.get("realm", "")
    nonce = params.get("nonce", "")
    ha1 = _md5(f"{username}:{realm}:{password}")
    ha2 = _md5(f"{method}:{uri}")
    qop = (params.get("qop", "") or "").split(",")[0].strip()
    if qop:
        nc = "00000001"
        cnonce = secrets.token_hex(4)
        response = _md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")
        qop_fields = f', qop={qop}, nc={nc}, cnonce="{cnonce}"'
    else:
        response = _md5(f"{ha1}:{nonce}:{ha2}")
        qop_fields = ""
    header = (
        f'Authorization: Digest username="{username}", realm="{realm}", '
        f'nonce="{nonce}", uri="{uri}", response="{response}"'
    )
    if params.get("algorithm", "").lower() == "md5":
        header += ", algorithm=MD5"
    if params.get("opaque"):
        header += f', opaque="{params["opaque"]}"'
    return header + qop_fields + "\r\n"

def _rtsp_negotiated_describe(
    ip: str,
    rtsp_port: int,
    path: str,
    username: str = "",
    password: str = "",
    timeout: float = 5.0,
) -> Tuple[int, str]:
    rtsp_url = f"rtsp://{ip}:{rtsp_port}{path}"
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, rtsp_port))
    except Exception:
        return 0, ""

    try:

        resp = _rtsp_send_describe(sock, rtsp_url, 1)
        code = _rtsp_status_code(resp)
        if code != 401 or not (username and password):
            return code, resp

        try:
            sock.settimeout(0.2)
            while sock.recv(4096):
                pass
        except Exception:
            pass
        sock.settimeout(timeout)

        challenges = _parse_www_authenticate(resp)
        ordered = ([c for c in challenges if c["scheme"] == "digest"]
                   + [c for c in challenges if c["scheme"] == "basic"])
        if not ordered:

            ordered = [{"scheme": "basic", "params": {}}]

        for cseq, challenge in enumerate(ordered, start=2):
            if challenge["scheme"] == "digest":
                auth_header = _build_rtsp_digest_header(
                    challenge["params"], username, password, "DESCRIBE", rtsp_url,
                )
            else:
                token = base64.b64encode(f"{username}:{password}".encode()).decode()
                auth_header = f"Authorization: Basic {token}\r\n"
            resp = _rtsp_send_describe(sock, rtsp_url, cseq, auth_header)
            code = _rtsp_status_code(resp)
            if code != 401:
                return code, resp
        return code, resp
    except Exception:
        return 0, ""
    finally:
        try:
            sock.close()
        except Exception:
            pass

def _probe_stream_access(
    ip: str,
    rtsp_port: int = 554,
    rtsp_path: str = "/md0_0",
    username: str = "",
    password: str = "",
) -> str:

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        result = sock.connect_ex((ip, rtsp_port))
        sock.close()
        if result != 0:
            return "unreachable"
    except Exception:
        return "unreachable"

    code, _resp_text = _rtsp_negotiated_describe(ip, rtsp_port, rtsp_path, username, password)

    if code == 200:
        return "open"
    if code == 401:
        return "auth_required"
    if code:

        for alt_path in ["/Streaming/Channels/101", "/h264/ch1/main/av_stream", "/live",
                         "/stream0", "/md0_0", "/stream1", "/md0_1"]:
            if alt_path == rtsp_path:
                continue
            alt_result = _quick_rtsp_check(ip, rtsp_port, alt_path, username, password)
            if alt_result == "open":
                return "open"
            elif alt_result == "auth_required":
                return "auth_required"
        return "open"

    return "open"

def _quick_rtsp_check(
    ip: str, rtsp_port: int, path: str,
    username: str = "", password: str = "",
) -> str:
    code, _ = _rtsp_negotiated_describe(ip, rtsp_port, path, username, password)
    if code == 200:
        return "open"
    if code == 401:
        return "auth_required"
    return "unreachable"

def _find_cached_camera(camera_name: str) -> Optional[CameraConfig]:
    try:
        cameras = _load_config_cameras()
        for cam in cameras:
            if cam.name == camera_name:
                return cam
    except Exception:
        pass
    return None

def _load_config_cameras() -> List[CameraConfig]:
    if not CONFIG_PATH.exists():

        alt_paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", "config.yaml"),
            "config.yaml",
        ]
        for p in alt_paths:
            p = os.path.normpath(p)
            if os.path.exists(p):
                break
        else:
            return []

    config_path = CONFIG_PATH if CONFIG_PATH.exists() else os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "config.yaml")
    )

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            import yaml
            data = yaml.safe_load(f) or {}
    except Exception:
        return []

    cameras_data = data.get("cameras", [])
    configs = []
    for entry in cameras_data:
        try:
            cfg = CameraConfig(
                name=entry.get("name", ""),
                connection_type=entry.get("connection_type", "onvif"),
                ip=entry.get("ip", ""),
                port=int(entry.get("onvif_port", entry.get("port", 0)) or 0),
                username=entry.get("username", "admin"),
                password=_dec(entry.get("password", "")),
                rtsp_port=int(entry.get("rtsp_port", 554)),
                rtsp_path=entry.get("rtsp_path_main", entry.get("rtsp_path", "/md0_0")),
                rtsp_sub_path=entry.get("rtsp_path_sub", entry.get("rtsp_sub_path", "/md0_1")),
                device_class=entry.get("device_class", ""),
                sn_code=_dec(entry.get("sn", entry.get("sn_code", ""))),
                pkdk=_dec(entry.get("pkdk", "")),
                protocol_type=entry.get("protocol_type", ""),
                onvif_sn=entry.get("onvif_sn", ""),
                illumination_modes=entry.get("illumination_modes", []),
            )
            configs.append(cfg)
        except Exception:
            continue
    return configs

def request_cloud_auth(sn: str) -> CloudAuthRequestResult:
    claw_id = get_or_create_claw_id()

    try:
        env = camera_proto.cloud_auth_request(sn, claw_id, timeout=10.0)
    except Exception as e:
        return CloudAuthRequestResult(
            success=False,
            claw_id=claw_id,
            error_message=f"Cloud request failed: {e}",
        )

    if not env.get("ok"):
        return CloudAuthRequestResult(
            success=False,
            claw_id=claw_id,
            station_default=env.get("station_source") == "default",
            error_message=env.get("error", "Cloud request failed"),
            http_status=env.get("http_status", 0),
        )

    payload = env.get("body") or {}
    if payload.get("code") == 200:
        return CloudAuthRequestResult(
            success=True, claw_id=claw_id,
            station_default=env.get("station_source") == "default",
            http_status=env.get("http_status", 0),
        )

    return CloudAuthRequestResult(
        success=False,
        claw_id=claw_id,
        station_default=env.get("station_source") == "default",
        error_message=f"Cloud rejected the request (code={payload.get('code')}): {payload.get('msg', '')}",
        http_status=env.get("http_status", 0),
    )

def poll_auth_status(
    camera_name: str,
) -> AuthStatusResult:
    camera_name = coerce_str(camera_name)

    if _yaml_lib is None:
        return AuthStatusResult(status=AuthStatus.ERROR, camera_name=camera_name, message="pyyaml is not installed")

    cameras = get_registered_cameras()
    camera = next(
        (c for c in cameras if c.name == camera_name or (c.sn_code and c.sn_code == camera_name)),
        None,
    )
    if camera is None or not camera.sn_code:
        return AuthStatusResult(
            status=AuthStatus.ERROR,
            camera_name=camera_name,
            message=f"Camera or its SN not found in config.yaml: {camera_name}",
        )

    claw_id = get_or_create_claw_id()

    try:
        env = camera_proto.cloud_auth_check(camera.sn_code, claw_id, timeout=10.0)
    except Exception as e:
        return AuthStatusResult(
            status=AuthStatus.ERROR,
            camera_name=camera_name,
            message=f"Cloud request failed: {e}",
        )

    if not env.get("ok"):
        return AuthStatusResult(
            status=AuthStatus.ERROR,
            camera_name=camera_name,
            message=env.get("error", "Cloud request failed"),
        )

    payload = env.get("body")
    if not isinstance(payload, dict):
        payload = {}

    if payload.get("code") != 200 or not payload.get("success"):
        return AuthStatusResult(
            status=AuthStatus.ERROR,
            camera_name=camera_name,
            message=f"Cloud rejected the request (code={payload.get('code')}): {payload.get('msg', '')}",
        )

    data = payload.get("data") or {}
    auth_code = int(data.get("authStatus", 0))
    device_pwd = str(data.get("devicePwd") or "")
    from_default = env.get("station_source") == "default"

    if auth_code == 1:

        if device_pwd:
            register_camera(
                name=camera.name,
                ip=camera.ip,
                port=camera.port,
                username=camera.username,
                password=device_pwd,
                rtsp_port=camera.rtsp_port,
                rtsp_path=camera.rtsp_path,
                rtsp_sub_path=camera.rtsp_sub_path,
                device_class=camera.device_class,
                sn_code=camera.sn_code,
                pkdk=camera.pkdk,
            )
        return AuthStatusResult(
            status=AuthStatus.AUTHORIZED,
            camera_name=camera.name,
            message=f"User authorized (devicePwd={device_pwd})" if device_pwd else "User authorized",
            auth_status_code=auth_code,
            device_pwd=device_pwd,
        )
    elif auth_code == 2:
        return AuthStatusResult(
            status=AuthStatus.REJECTED,
            camera_name=camera.name,
            message="User rejected the authorization in the APP",
            auth_status_code=auth_code,
        )
    else:

        return AuthStatusResult(
            status=AuthStatus.PENDING,
            camera_name=camera.name,
            message="Waiting for user confirmation (device has no station record; submitted to the default station)" if from_default else "Waiting for user confirmation",
            auth_status_code=auth_code,
        )

def disconnect_device(
    camera_name: str,
) -> DisconnectResult:
    camera_name = coerce_str(camera_name)

    if camera_name in _connected_devices:
        conn_info = _connected_devices.pop(camera_name)

        onvif_cam = conn_info.get("onvif_camera")
        if onvif_cam:
            try:
                onvif_cam.close()
            except Exception:
                pass
        return DisconnectResult(success=True, session_released=True)

    return DisconnectResult(
        success=True,
        session_released=False,
        error_message="Device is not in the connected list",
    )

def _find_camera(name: str):
    target = (name or "").strip().lower()
    for cam in get_registered_cameras():
        if (cam.name or "").strip().lower() == target:
            return cam
    return None

def _is_non_sk_camera(name: str) -> bool:
    cam = _find_camera(name)
    return bool(cam and cam.protocol_type in ("J", "O"))

_PROTOCOL_LABELS = {"J": "JCP (J) protocol", "O": "Third-party ONVIF (O) protocol"}

def _unsupported_protocol_message(name: str, capability: str) -> str:
    cam = _find_camera(name)
    label = _PROTOCOL_LABELS.get((cam.protocol_type if cam else "") or "", "non-SK protocol")
    return f"This camera is a {label} device; {capability} is not supported (this capability is exclusive to the SK private protocol)"

def _dev_to_name(dev) -> str:
    base = dev.model or dev.sn_code or "camera"
    suffix = dev.ip.split(".")[-1] if dev.ip else "x"
    return f"{base}_{suffix}"

def big_register(
    name: str = "",
    ip: str = "",
    onvif_port: int = 2000,
    rtsp_port: int = 554,
    sn_code: str = "",
    password: str = "",
    device_class: str = "password_required",
) -> RegisterResult:
    rr = register_camera(
        name=name, ip=ip, port=onvif_port,
        username="admin", password=password,
        rtsp_port=rtsp_port,
        device_class=device_class, sn_code=sn_code,
    )
    if not rr.success:
        return rr

    if password:
        try:
            cr = connect_device(rr.camera_name, password=password)
            if not cr.success:
                rr.success = False
                rr.error_message = f"Registration succeeded but ONVIF authentication failed: {cr.error_message}"
        except Exception as e:
            rr.success = False
            rr.error_message = f"Registration succeeded but authentication raised an exception: {e}"

    return rr

def _resolve_connect_target(name: str) -> Tuple[Optional[CameraConfig], Optional[AuthOrchestrateResult]]:
    cameras = get_registered_cameras()
    if not cameras:
        return None, AuthOrchestrateResult(
            success=False, status="no_devices",
            error_message="No registered devices in config.yaml; call search_devices first",
        )
    if not name:
        if len(cameras) == 1:
            return cameras[0], None
        return None, AuthOrchestrateResult(
            success=False, status="needs_selection",
            available_cameras=[
                {"name": c.name, "ip": c.ip, "sn": c.sn_code, "model": ""}
                for c in cameras
            ],
            error_message="Multiple devices in config.yaml; specify the name and call again",
        )
    target = next((c for c in cameras if c.name == name or c.sn_code == name), None)
    if target is None:
        return None, AuthOrchestrateResult(
            success=False, status="needs_selection",
            available_cameras=[
                {"name": c.name, "ip": c.ip, "sn": c.sn_code, "model": ""}
                for c in cameras
            ],
            error_message=f"Camera '{name}' not found",
        )
    return target, None

def big_connect(name: str = "") -> AuthOrchestrateResult:

    target, early = _resolve_connect_target(name)
    if early is not None:
        return early
    if not target.sn_code:
        return AuthOrchestrateResult(
            success=False, status="no_sn",
            camera_name=target.name,
            error_message=f"Device '{target.name}' has no SN recorded; cloud authorization cannot start",
        )

    cr = request_cloud_auth(target.sn_code)
    if not cr.success:
        return AuthOrchestrateResult(
            success=False, status="cloud_error",
            camera_name=target.name, sn=target.sn_code,
            claw_id=cr.claw_id,
            error_message=cr.error_message,
        )

    poll_interval = 5
    max_polls = 120
    for _ in range(max_polls):
        time.sleep(poll_interval)
        result = poll_auth_status(target.name)
        if result.status == AuthStatus.AUTHORIZED:
            return AuthOrchestrateResult(
                success=True, status="authorized",
                camera_name=target.name, sn=target.sn_code,
                claw_id=cr.claw_id,
                device_pwd=result.device_pwd,
            )
        elif result.status == AuthStatus.REJECTED:
            return AuthOrchestrateResult(
                success=False, status="rejected",
                camera_name=target.name, sn=target.sn_code,
                claw_id=cr.claw_id,
                error_message="User rejected the authorization in the APP",
            )
        elif result.status == AuthStatus.ERROR:
            return AuthOrchestrateResult(
                success=False, status="error",
                camera_name=target.name, sn=target.sn_code,
                claw_id=cr.claw_id,
                error_message=result.message,
            )

    return AuthOrchestrateResult(
        success=False, status="timeout",
        camera_name=target.name, sn=target.sn_code,
        claw_id=cr.claw_id,
        error_message=(
            f"Authorization timed out after 10 minutes; user did not confirm"
            f"{' (device has no station record; the APP may not have received the request)' if cr.station_default else ''}"
        ),
    )

def resolve_target(
    name: Optional[str] = None,
    answers: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    answers = answers or {}

    if answers.get("camera"):
        chosen = answers["camera"]
        cam = _find_camera(chosen)
        if cam:
            return {"ok": True, "camera": cam, "via": "user_picked"}

        try:
            sr = search_devices(timeout=15.0)
        except Exception as e:
            return {"ok": False, "error_code": "SEARCH_FAILED", "message": f"Re-search failed: {e}"}
        if sr.success:
            for dev in sr.devices:
                if _dev_to_name(dev) == chosen:
                    reg = big_register(
                        name=chosen, ip=dev.ip, onvif_port=dev.onvif_port,
                        rtsp_port=dev.rtsp_port, sn_code=dev.sn_code,
                        device_class=dev.device_class.value if hasattr(dev.device_class, "value") else str(dev.device_class),
                    )
                    if reg.success:
                        return {"ok": True, "camera": _find_camera(chosen), "via": "user_picked_registered"}
                    return {"ok": False, "error_code": "AUTO_REGISTER_FAILED",
                            "message": f"Failed to register {chosen}: {reg.error_message}"}
        return {"ok": False, "error_code": "CAMERA_NOT_FOUND",
                "message": f"Picked {chosen!r} but the device was not found on the LAN",
                "hint": "Call search_devices again to see currently discoverable devices"}

    if name:
        cam = _find_camera(name)
        if cam:
            return {"ok": True, "camera": cam, "via": "registered"}
        return {"ok": False, "error_code": "CAMERA_NOT_FOUND",
                "message": f"name={name!r} is not in config.yaml",
                "hint": "Use get_registered_cameras to list registered cameras, or search_devices for new devices"}

    cams = get_registered_cameras()
    if len(cams) == 1:
        return {"ok": True, "camera": cams[0], "via": "registered"}
    if len(cams) > 1:
        return {"ok": False, "error_code": "NEEDS_INPUT",
                "needs_input": [{
                    "key": "camera",
                    "question": f"{len(cams)} cameras registered; please select one",
                    "options": [{"label": f"{c.name} ({c.ip})", "value": c.name} for c in cams],
                }]}

    try:
        sr = search_devices(timeout=15.0)
    except Exception as e:
        return {"ok": False, "error_code": "NO_CAMERAS",
                "message": f"config.yaml empty and search failed: {e}",
                "hint": "Check the network or run search_devices manually"}

    if not sr.success or not sr.devices:
        return {"ok": False, "error_code": "NO_CAMERAS",
                "message": "config.yaml empty and no devices discovered on the LAN",
                "hint": "Check camera power and network"}

    if len(sr.devices) == 1:
        dev = sr.devices[0]
        dev_name = _dev_to_name(dev)
        reg = big_register(
            name=dev_name, ip=dev.ip, onvif_port=dev.onvif_port,
            rtsp_port=dev.rtsp_port, sn_code=dev.sn_code,
            device_class=dev.device_class.value if hasattr(dev.device_class, "value") else str(dev.device_class),
        )
        if reg.success:
            return {"ok": True, "camera": _find_camera(dev_name), "via": "auto_registered"}
        return {"ok": False, "error_code": "AUTO_REGISTER_FAILED",
                "message": f"Auto-register {dev_name} failed: {reg.error_message}",
                "hint": "Call register_camera manually to investigate"}

    return {"ok": False, "error_code": "NEEDS_INPUT",
            "needs_input": [{
                "key": "camera",
                "question": f"{len(sr.devices)} devices discovered on the LAN; which one to register?",
                "options": [{
                    "label": f"{d.model or d.sn_code or '?'} ({d.ip})",
                    "value": _dev_to_name(d),
                } for d in sr.devices],
            }]}
