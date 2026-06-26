#!/usr/bin/env python3
"""
设备抓拍信息查询脚本
用于查询视频监控系统的抓拍信息，运行参数从 Windows 临时目录中的 vpup.json 加载
"""

import hashlib
import requests
import json
import os
import sys
import re
import argparse
import logging
import subprocess
import tempfile
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path, PureWindowsPath
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from urllib.parse import quote, urlencode, urljoin, urlparse
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import base64

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


WINDOWS_DRIVE_PATH_RE = re.compile(r"^(?P<drive>[A-Za-z]):[\\/](?P<tail>.*)$")
HEX_TEXT_RE = re.compile(r"^[0-9A-Fa-f]+$")
SUCCESS_CODES = frozenset({200, 1000000, "200", "1000000"})


def _is_success_code(code: Any) -> bool:
    """判断媒体服务返回码是否表示成功。"""
    if code in SUCCESS_CODES:
        return True

    try:
        return int(code) in (200, 1000000)
    except (TypeError, ValueError):
        return str(code) in ("200", "1000000")


def _json_api_success(result: Dict[str, Any]) -> bool:
    """兼容接口返回 code=200 与 code=1000000 两类成功响应。"""
    if not isinstance(result, dict):
        return False
    if _is_success_code(result.get("code")):
        if "result" in result and result.get("result") is False:
            return False
        return True
    return False


def _normalize_snapshot_code_str(raw: Any) -> str:
    """统一截图任务 code 为非空字符串。"""
    if raw is None:
        raise ValueError("截图 code 不能为空")

    if isinstance(raw, int):
        code_text = str(raw)
    else:
        code_text = str(raw).strip()

    if not code_text:
        raise ValueError("截图 code 不能为空")

    return code_text


def _snapshot_download_retry_settings() -> Tuple[int, float]:
    """读取截图轮询下载重试配置。"""
    try:
        retries = int(os.environ.get("VISPATROL_SNAPSHOT_PULL_RETRIES", "15"))
    except ValueError:
        retries = 15

    try:
        interval = float(os.environ.get("VISPATROL_SNAPSHOT_PULL_INTERVAL", "1.0"))
    except ValueError:
        interval = 1.0

    retries = max(1, min(retries, 120))
    interval = max(0.1, min(interval, 30.0))
    return retries, interval


def _is_wsl_environment() -> bool:
    """判断当前 Python 是否运行在 WSL 环境中。"""
    if sys.platform != "linux":
        return False

    if os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSL_INTEROP"):
        return True

    try:
        return "microsoft" in Path("/proc/version").read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False


def _get_windows_host_temp_dir_from_wsl() -> Optional[str]:
    """在 WSL 中查询 Windows 宿主机的 TEMP 目录。"""
    if not _is_wsl_environment():
        return None

    commands = (
        ["cmd.exe", "/d", "/c", "echo", "%TEMP%"],
        ["cmd.exe", "/d", "/c", "echo", "%TMP%"],
        ["powershell.exe", "-NoProfile", "-Command", "[System.IO.Path]::GetTempPath()"],
    )

    for command in commands:
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
                timeout=5,
                check=True,
            )
        except (OSError, subprocess.SubprocessError):
            continue

        temp_dir = completed.stdout.strip().strip('"').rstrip("\\/")
        print(f"Detected Windows temp dir: {temp_dir}")
        if temp_dir and "%" not in temp_dir and WINDOWS_DRIVE_PATH_RE.match(temp_dir):
            return temp_dir

    return None


def _windows_path_to_wsl_path(path_text: str) -> Optional[str]:
    """将 Windows 盘符路径转换为 WSL 可访问的 /mnt 路径。"""
    match = WINDOWS_DRIVE_PATH_RE.match(str(path_text or "").strip())
    if not match:
        return None

    drive = match.group("drive").lower()
    tail = match.group("tail").replace("\\", "/").lstrip("/")
    if tail:
        return f"/mnt/{drive}/{tail}"

    return f"/mnt/{drive}"


def _resolve_vpup_config_path(path_text: str) -> Path:
    """将 vpup 配置路径解析为当前环境可直接访问的文件路径。"""
    raw_path = str(path_text or "").strip()
    if _is_wsl_environment():
        wsl_path = _windows_path_to_wsl_path(raw_path)
        if wsl_path is not None:
            return Path(wsl_path).expanduser()

    return Path(raw_path).expanduser()


def _default_vpup_config_path() -> str:
    """优先在 WSL 中定位 Windows 宿主机 Temp 下的 vpup.json。"""
    windows_temp_dir = _get_windows_host_temp_dir_from_wsl()
    if windows_temp_dir:
        return str(PureWindowsPath(windows_temp_dir) / "vpup.json")

    return str(Path(tempfile.gettempdir()) / "vpup.json")


def _normalize_mac_address(value: Any) -> Optional[str]:
    """将 MAC 地址归一化为 12 位大写十六进制字符串。"""
    if value in (None, ""):
        return None

    hex_digits = re.sub(r"[^0-9A-Fa-f]", "", str(value))
    if len(hex_digits) != 12 or hex_digits == "000000000000":
        return None

    return hex_digits.upper()


def _get_mac_address_from_uuid(allow_random: bool = False) -> Optional[str]:
    """优先使用 uuid.getnode() 获取本机 MAC 地址。"""
    mac_value = uuid.getnode()
    normalized_mac = _normalize_mac_address(f"{mac_value:012X}")
    if normalized_mac is None:
        return None

    has_multicast_bit = bool(mac_value & 0x010000000000)
    if has_multicast_bit and not allow_random:
        return None

    return normalized_mac


def _get_mac_address_from_system() -> Optional[str]:
    """在 Windows 上通过 getmac 命令回退获取本机 MAC 地址。"""
    if os.name != "nt":
        return None

    try:
        completed = subprocess.run(
            ["getmac", "/fo", "csv", "/nh"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=5,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    for line in completed.stdout.splitlines():
        match = re.search(r"([0-9A-Fa-f]{2}(?:[-:][0-9A-Fa-f]{2}){5})", line)
        if match is None:
            continue

        normalized_mac = _normalize_mac_address(match.group(1))
        if normalized_mac is not None:
            return normalized_mac

    return None


def get_mac_address() -> str:
    """获取本机 MAC 地址，返回 12 位大写十六进制字符串。"""
    mac_address = _get_mac_address_from_uuid()
    if mac_address is not None:
        return mac_address

    mac_address = _get_mac_address_from_system()
    if mac_address is not None:
        return mac_address

    mac_address = _get_mac_address_from_uuid(allow_random=True)
    if mac_address is not None:
        return mac_address

    raise RuntimeError("无法获取本机 MAC 地址")


def get_cpu_id() -> str:
    """兼容旧调用，当前返回本机 MAC 地址。"""
    return get_mac_address()


def aes_cbc_decrypt(encrypted_base64: str, key: str, iv: str) -> str:
    """
    AES-CBC 解密函数
    :param encrypted_base64: Base64编码的密文
    :param key: 密钥（16/24/32字符，对应AES-128/192/256）
    :param iv: 初始化向量（固定16字符）
    :return: 解密后的明文字符串
    """
    # 1. 将密钥、IV 转为字节流（UTF-8编码）
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8') if iv else (b'\x00' * AES.block_size)

    # 2. Base64解码密文（还原二进制密文）
    encrypted_bytes = base64.b64decode(encrypted_base64)

    # 3. 初始化AES-CBC解密器
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    # 4. 解密 + 去除PKCS7填充
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

    # 5. 字节流转字符串返回
    return decrypted_bytes.decode('utf-8')


@dataclass
class PictureCaptureConfig:
    """抓拍配置"""
    base_url: str = "http://127.0.0.1"
    media_service_port: int = 8482
    device_service_port: int = 8481
    manage_service_port: int = 8483
    timeout: int = 30
    vpup_config_path: str = field(
        default_factory=_default_vpup_config_path
    )
    snapshot_output_dir: str = field(
        default_factory=lambda: "~/.openclaw/workspace/tmp_files/"
    )


class PictureCapture:
    """抓拍查询类"""

    def __init__(self, config: Optional[PictureCaptureConfig] = None):
        """初始化抓拍摄例"""
        self.config = config or PictureCaptureConfig()
        self.session = requests.Session()
        self.token = None
        self.runtime_config_loaded = False
        self.runtime_config_error: Optional[str] = None
        self.device_status_records: List[Dict[str, Any]] = []
        self.device_status_cache: Dict[str, Dict[str, Any]] = {}
        self.device_rtsp_urls: Dict[str, Dict[str, str]] = {}
        self._load_runtime_config_from_vpup()

    def _clear_runtime_auth_state(self) -> None:
        """清理运行时加载的认证信息，避免沿用旧配置。"""
        self.token = None

    def _load_runtime_config_from_vpup(self, force_reload: bool = False) -> Dict[str, Any]:
        """从 Windows 临时目录中的 vpup.json 加载服务地址并解密 token。"""
        if self.runtime_config_loaded and not force_reload:
            return {
                "success": True,
                "message": "已加载 vpup 配置",
                "data": {
                    "base_url": self.config.base_url,
                    "media_service_port": self.config.media_service_port,
                    "device_service_port": self.config.device_service_port,
                    "manage_service_port": self.config.manage_service_port,
                    "token_loaded": bool(self.token),
                }
            }

        vpup_path = _resolve_vpup_config_path(self.config.vpup_config_path)

        try:
            raw_text = vpup_path.read_text(encoding="utf-8-sig")
            payload = json.loads(raw_text)
        except FileNotFoundError:
            message = f"未找到 vpup 配置文件: {vpup_path}"
            self.runtime_config_loaded = False
            self.runtime_config_error = message
            self._clear_runtime_auth_state()
            logger.error(message)
            return {
                "success": False,
                "message": message,
            }
        except (OSError, json.JSONDecodeError) as exc:
            message = f"读取 vpup 配置失败: {exc}"
            self.runtime_config_loaded = False
            self.runtime_config_error = message
            self._clear_runtime_auth_state()
            logger.error(message)
            return {
                "success": False,
                "message": message,
            }

        if not isinstance(payload, dict):
            message = "vpup.json 内容格式无效，顶层必须为对象"
            self.runtime_config_loaded = False
            self.runtime_config_error = message
            self._clear_runtime_auth_state()
            logger.error(message)
            return {
                "success": False,
                "message": message,
            }

        ip = str(payload.get("ip") or "").strip()
        media_service = payload.get("mediaService", self.config.media_service_port)
        device_service = payload.get("deviceService", self.config.device_service_port)
        manage_service = payload.get("manageService", self.config.manage_service_port)
        token = payload.get("token", "")
        cpu_mac = get_cpu_id()
        cpu_mac = hashlib.md5(cpu_mac.encode("ascii")).hexdigest().upper()

        if not ip:
            message = "vpup.json 中缺少 ip"
            self.runtime_config_loaded = False
            self.runtime_config_error = message
            self._clear_runtime_auth_state()
            logger.error(message)
            return {
                "success": False,
                "message": message,
            }

        try:
            media_service_port = int(media_service)
            device_service_port = int(device_service)
            manage_service_port = int(manage_service)
        except (TypeError, ValueError):
            message = "vpup.json 中的服务端口不是有效整数"
            self.runtime_config_loaded = False
            self.runtime_config_error = message
            self._clear_runtime_auth_state()
            logger.error(message)
            return {
                "success": False,
                "message": message,
            }

        try:
            decrypted_token = aes_cbc_decrypt(token, cpu_mac, "")
        except ValueError as exc:
            message = f"vpup.json 中的 token 解密失败: {exc}"
            self.runtime_config_loaded = False
            self.runtime_config_error = message
            self._clear_runtime_auth_state()
            logger.error(message)
            return {
                "success": False,
                "message": message,
            }

        self.config.base_url = f"http://{ip}"
        self.config.media_service_port = media_service_port
        self.config.device_service_port = device_service_port
        self.config.manage_service_port = manage_service_port
        self.token = decrypted_token or None
        self.runtime_config_loaded = True
        self.runtime_config_error = None

        logger.info(
            "已从 vpup.json 加载运行配置: ip=%s, mediaService=%s, deviceService=%s, manageService=%s, token_loaded=%s",
            ip,
            media_service_port,
            device_service_port,
            manage_service_port,
            bool(self.token),
        )

        return {
            "success": True,
            "message": "已从 vpup.json 加载运行配置",
            "data": {
                "ip": ip,
                "mediaService": media_service_port,
                "deviceService": device_service_port,
                "manageService": manage_service_port,
                "vpup_config_path": str(vpup_path),
                "token_loaded": bool(self.token),
            }
        }

    def _ensure_runtime_config(self) -> Dict[str, Any]:
        """确保运行所需的地址和 token 已从 vpup.json 加载。"""
        result = self._load_runtime_config_from_vpup(force_reload=not self.runtime_config_loaded)
        if not result.get("success"):
            return result

        if not self.token:
            return {
                "success": False,
                "message": "vpup.json 中的 token 为空或解密后为空",
            }

        return result

    @staticmethod
    def _encode_query_params(params: Dict[str, Any]) -> str:
        """按接口文档示例编码查询参数。"""
        return urlencode(params, quote_via=quote, safe=":")

    @staticmethod
    def _extract_snapshot_records(data: Any) -> List[Dict[str, Any]]:
        """兼容不同接口字段名，提取抓拍记录列表。"""
        if isinstance(data, list):
            return data

        if not isinstance(data, dict):
            return []

        for key in ("snapshots", "items", "records", "list", "datas"):
            value = data.get(key)
            if isinstance(value, list):
                return value

        snapshot = data.get("snapshot")
        if isinstance(snapshot, dict):
            return [snapshot]

        if any(key in data for key in ("code", "url", "imageUrl", "snapshotUrl", "time", "captureTime")):
            return [data]

        return []

    @staticmethod
    def _normalize_display_value(value: Any) -> str:
        """将接口字段值转换为可展示的字符串。"""
        if value in (None, ""):
            return "N/A"
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    @staticmethod
    def _normalize_channel_value(value: Any) -> Optional[str]:
        """统一通道值格式，避免数值和字符串混用。"""
        if value in (None, ""):
            return None
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value)

    @staticmethod
    def _normalize_cache_key(value: Any) -> Optional[str]:
        """统一缓存键格式，便于通过设备 ID 或通道号查找。"""
        if value in (None, ""):
            return None
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return str(value).strip()

    @classmethod
    def _normalize_channel_lookup_key(cls, value: Any) -> Optional[str]:
        """统一 RTSP URL 查询时使用的通道键。"""
        channel_value = cls._normalize_cache_key(value)
        if channel_value is None:
            return None
        if channel_value.isdigit():
            return str(int(channel_value))
        return channel_value

    @staticmethod
    def _normalize_stream_selector(value: Any) -> Optional[str]:
        """将主子码流标识归一化为接口 urls 使用的 0/1。"""
        if value in (None, ""):
            return None

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            stream_index = int(value)
            if stream_index in (0, 1):
                return str(stream_index)

        normalized_value = str(value).strip().lower()
        stream_mapping = {
            "0": "0",
            "1": "1",
            "main": "0",
            "mainstream": "0",
            "main_stream": "0",
            "primary": "0",
            "master": "0",
            "主": "0",
            "主码流": "0",
            "主码": "0",
            "sub": "1",
            "substream": "1",
            "sub_stream": "1",
            "secondary": "1",
            "child": "1",
            "子": "1",
            "子码流": "1",
            "子码": "1",
        }
        return stream_mapping.get(normalized_value)

    @staticmethod
    def _stream_selector_display(stream_selector: Any) -> str:
        """将码流标识转换为便于展示的名称。"""
        normalized_stream = PictureCapture._normalize_stream_selector(stream_selector)
        if normalized_stream == "0":
            return "主码流"
        if normalized_stream == "1":
            return "子码流"
        return PictureCapture._normalize_display_value(stream_selector)

    @classmethod
    def _normalize_device_status_urls(cls, urls: Any) -> Dict[str, str]:
        """归一化设备状态接口中的 urls 字段。"""
        normalized_urls: Dict[str, str] = {}

        if isinstance(urls, dict):
            for key, value in urls.items():
                normalized_key = cls._normalize_cache_key(key)
                if normalized_key in (None, "") or value in (None, ""):
                    continue
                normalized_urls[normalized_key] = str(value)
            return normalized_urls

        if isinstance(urls, list):
            for item in urls:
                if not isinstance(item, dict):
                    continue

                channel = cls._normalize_channel_lookup_key(
                    item.get("channel") or item.get("channelnum") or item.get("channelNo")
                )
                stream = cls._normalize_stream_selector(
                    item.get("stream") or item.get("streamType") or item.get("subtype")
                )
                url = item.get("url") or item.get("rtsp") or item.get("rtspUrl")
                if channel is None or stream is None or url in (None, ""):
                    continue

                normalized_urls[f"{channel}_{stream}"] = str(url)

        return normalized_urls

    @classmethod
    def _parse_device_status_entry(cls, device: Dict[str, Any]) -> Dict[str, Any]:
        """解析设备状态接口中的单条设备记录，保留原始字段并补充 urls 明细。"""
        if not isinstance(device, dict):
            return {
                "detail": cls._normalize_display_value(device)
            }

        parsed_device = dict(device)
        normalized_urls = cls._normalize_device_status_urls(device.get("urls"))
        parsed_urls: List[Dict[str, Any]] = []

        for stream_key in sorted(normalized_urls.keys()):
            channel, _, stream = stream_key.partition("_")
            parsed_urls.append({
                "stream_key": stream_key,
                "channel": cls._normalize_channel_value(channel),
                "stream": stream,
                "stream_name": cls._stream_selector_display(stream),
                "rtsp_url": normalized_urls[stream_key],
            })

        status_value = device.get("status")
        if status_value == 1:
            status_text = "在线"
        elif status_value == 0:
            status_text = "离线"
        else:
            status_text = cls._normalize_display_value(status_value)

        parsed_device.update({
            "device_id": device.get("id"),
            "device_name": device.get("name"),
            "device_ip": device.get("ip"),
            "status_text": status_text,
            "normalized_urls": normalized_urls,
            "parsed_urls": parsed_urls,
            "url_count": len(normalized_urls),
        })
        return parsed_device

    @staticmethod
    def _get_snapshot_field_value(snapshot: Dict[str, Any], candidate_keys: Tuple[str, ...]) -> Any:
        """按候选字段顺序提取抓拍字段值。"""
        for key in candidate_keys:
            if key in snapshot and snapshot[key] not in (None, ""):
                return snapshot[key]

        for key in candidate_keys:
            if key in snapshot:
                return snapshot[key]

        return None

    @classmethod
    def _normalize_snapshot_record(cls, snapshot: Dict[str, Any], fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """将不同接口字段归一化为统一的抓拍展示字段。"""
        if not isinstance(snapshot, dict):
            return {
                "detail": cls._normalize_display_value(snapshot)
            }

        normalized_snapshot = {
            "id": cls._get_snapshot_field_value(snapshot, ("id", "snapshotId", "snapshotid")),
            "code": cls._get_snapshot_field_value(snapshot, ("code", "snapshotCode", "snapshotcode")),
            "device_id": cls._get_snapshot_field_value(snapshot, ("device_id", "deviceId", "deviceid", "devId", "devid")),
            "device_name": cls._get_snapshot_field_value(snapshot, ("device_name", "deviceName", "devicename", "name")),
            "channel": cls._normalize_channel_value(
                cls._get_snapshot_field_value(
                    snapshot,
                    ("channel", "channelNo", "channelno", "channelId", "channelid", "channelIndex", "channelindex", "chn", "chnid")
                )
            ),
            "time": cls._get_snapshot_field_value(
                snapshot,
                ("time", "snapshotTime", "snapshottime", "captureTime", "capturetime", "createtime", "createTime")
            ),
            "url": cls._get_snapshot_field_value(
                snapshot,
                ("url", "snapshotUrl", "snapshoturl", "imageUrl", "imageurl", "fileUrl", "fileurl", "path")
            ),
        }

        if fallback:
            for key, value in fallback.items():
                if normalized_snapshot.get(key) in (None, "") and value not in (None, ""):
                    normalized_snapshot[key] = value

        for key in (
            "response_type",
            "content_type",
            "size",
            "local_path",
            "local_path_error",
            "status",
            "status_text",
        ):
            value = snapshot.get(key)
            if value not in (None, ""):
                normalized_snapshot[key] = value

        return {
            key: value
            for key, value in normalized_snapshot.items()
            if value not in (None, "")
        }

    @staticmethod
    def _snapshot_sort_key(snapshot: Dict[str, Any]) -> Tuple[int, Any]:
        """生成抓拍时间排序键，用于选取最新抓拍。"""
        time_value = snapshot.get("time")
        if time_value in (None, ""):
            return (0, "")

        if isinstance(time_value, (int, float)):
            return (3, float(time_value))

        time_text = str(time_value).strip()
        for time_format in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
        ):
            try:
                return (4, datetime.strptime(time_text, time_format).timestamp())
            except ValueError:
                continue

        if time_text.isdigit():
            return (2, int(time_text))

        return (1, time_text)

    @staticmethod
    def _sanitize_filename_component(value: Any, default: str = "snapshot") -> str:
        """将任意字段转换为安全的文件名片段。"""
        if value in (None, ""):
            return default

        sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value).strip())
        sanitized = sanitized.strip("._")
        return sanitized or default

    @staticmethod
    def _content_type_to_extension(content_type: Optional[str]) -> str:
        """根据 MIME 类型推断图片扩展名。"""
        mapping = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/bmp": ".bmp",
            "image/webp": ".webp",
        }
        return mapping.get(str(content_type or "").strip().lower(), ".bin")

    @classmethod
    def _build_snapshot_title(cls, device_name: Any, channel: Any) -> str:
        """构造上层展示用的设备加通道名称。"""
        device_text = "未知设备" if device_name in (None, "") else str(device_name)
        channel_text = cls._normalize_channel_value(channel)
        if channel_text:
            return f"{device_text} - 通道 {channel_text}"
        return device_text

    @classmethod
    def _build_image_attachments(cls, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从抓拍列表中提取上层可直接发送的图片附件。"""
        attachments: List[Dict[str, Any]] = []

        for snapshot in snapshots:
            if not isinstance(snapshot, dict):
                continue

            normalized_snapshot = cls._normalize_snapshot_record(snapshot)
            local_path = snapshot.get("local_path")
            if local_path in (None, ""):
                continue

            channel = snapshot.get("channel") or normalized_snapshot.get("channel")
            attachments.append({
                "title": cls._build_snapshot_title(normalized_snapshot.get("device_name"), channel),
                "device_name": normalized_snapshot.get("device_name"),
                "channel": channel,
                "snapshot_id": normalized_snapshot.get("id"),
                "snapshot_time": normalized_snapshot.get("time"),
                "local_path": str(local_path),
                "content_type": snapshot.get("content_type"),
            })

        return attachments

    def _build_service_base_url(self, port: int) -> str:
        """基于基础地址构造指定服务端口的 URL。"""
        parsed = urlparse(self.config.base_url)
        if parsed.scheme and parsed.hostname:
            return f"{parsed.scheme}://{parsed.hostname}:{port}"

        return f"{self.config.base_url.rstrip('/')}:{port}"

    def _build_auth_headers(self) -> Dict[str, str]:
        """统一构造鉴权请求头。"""
        headers: Dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _make_json_api_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 3,
    ) -> Dict[str, Any]:
        """发送媒体服务 JSON 请求，并兼容不同成功码。"""
        url = f"{self._build_service_base_url(self.config.media_service_port)}{endpoint}"
        headers = self._build_auth_headers()
        headers["Content-Type"] = "application/json"
        attempts = max(1, int(retry_count))

        last_error: Optional[Exception] = None
        for attempt in range(attempts):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                )
                response.raise_for_status()
                result = response.json()
                if not _json_api_success(result):
                    error_msg = result.get("message") or result.get("msg") or "API 调用失败"
                    raise ValueError(f"API 错误: {error_msg} (Code: {result.get('code')})")
                return result
            except (requests.exceptions.RequestException, ValueError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt == attempts - 1:
                    break
                time.sleep(2 * (attempt + 1))

        if isinstance(last_error, json.JSONDecodeError):
            raise ValueError(f"JSON 解析失败: {last_error}") from last_error
        if isinstance(last_error, ValueError):
            raise ValueError(str(last_error)) from last_error
        raise ValueError(f"请求失败: {last_error}") from last_error

    def _cache_device_status_entries(self, devices: List[Dict[str, Any]]) -> None:
        """缓存设备状态接口返回，便于按 device_id 查询 RTSP 地址。"""
        self.device_status_records = [
            self._parse_device_status_entry(device)
            for device in devices
            if isinstance(device, dict)
        ]
        self.device_status_cache = {}
        self.device_rtsp_urls = {}

        for device in self.device_status_records:
            device_id = self._normalize_cache_key(device.get("id"))
            if device_id is None:
                continue

            self.device_status_cache[device_id] = device
            normalized_urls = device.get("normalized_urls")
            if not isinstance(normalized_urls, dict):
                normalized_urls = self._normalize_device_status_urls(device.get("urls"))
            self.device_rtsp_urls[device_id] = normalized_urls

    def _resolve_snapshot_url(self, snapshot_url: str) -> str:
        """将抓拍地址规范化为可下载的绝对 URL。"""
        if not snapshot_url:
            return snapshot_url

        parsed = urlparse(snapshot_url)
        if parsed.scheme and parsed.netloc:
            return snapshot_url

        return urljoin(
            f"{self._build_service_base_url(self.config.media_service_port).rstrip('/')}/",
            snapshot_url.lstrip("/")
        )

    def _build_snapshot_local_path(self, snapshot: Dict[str, Any], content_type: Optional[str]) -> Path:
        """生成抓拍文件的本地落盘路径。"""
        output_dir = Path(self.config.snapshot_output_dir).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)

        code_part = self._sanitize_filename_component(
            snapshot.get("code") or snapshot.get("id") or "snapshot"
        )
        channel_part = self._sanitize_filename_component(snapshot.get("channel") or "na")
        time_part = self._sanitize_filename_component(
            snapshot.get("time") or datetime.now().strftime("%Y%m%d%H%M%S")
        )
        extension = self._content_type_to_extension(content_type)

        return (output_dir / f"{code_part}_ch{channel_part}_{time_part}{extension}").resolve()

    def _save_snapshot_content(
        self,
        content: bytes,
        snapshot: Dict[str, Any],
        content_type: Optional[str]
    ) -> Optional[str]:
        """将抓拍内容写入本地文件并返回绝对路径。"""
        if not content:
            return None

        try:
            file_path = self._build_snapshot_local_path(snapshot, content_type)
            file_path.write_bytes(content)
            return str(file_path)
        except OSError as exc:
            logger.error(f"抓拍图片保存失败: {exc}")
            return None

    def _materialize_snapshot_from_url(self, snapshot: Dict[str, Any]) -> Optional[str]:
        """将抓拍 URL 下载到本地，供上层发送图片。"""
        local_path = snapshot.get("local_path")
        if local_path not in (None, ""):
            return None

        snapshot_url = snapshot.get("url")
        if snapshot_url in (None, ""):
            return None

        resolved_url = self._resolve_snapshot_url(str(snapshot_url))
        headers = self._build_auth_headers()

        try:
            response = self.session.get(
                resolved_url,
                headers=headers,
                timeout=self.config.timeout
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            message = f"抓拍地址下载失败: {exc}"
            logger.warning(message)
            return message

        content = response.content or b""
        if not content:
            message = "抓拍地址下载成功，但图片内容为空"
            logger.warning(message)
            return message

        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        detected_content_type = self._detect_image_content_type(content)
        if not content_type.startswith("image/"):
            content_type = detected_content_type or content_type

        if not str(content_type).startswith("image/"):
            message = f"抓拍地址下载成功，但响应不是图片: {content_type or 'unknown'}"
            logger.warning(message)
            return message

        local_path = self._save_snapshot_content(content, snapshot, content_type)
        if not local_path:
            return "抓拍地址下载成功，但本地保存失败"

        snapshot["local_path"] = local_path
        snapshot["content_type"] = content_type
        snapshot["size"] = len(content)
        return None

    @staticmethod
    def _response_is_json(response: requests.Response) -> bool:
        """根据响应头和响应体特征判断接口是否返回 JSON。"""
        content_type = response.headers.get("Content-Type", "").lower()
        if "json" in content_type:
            return True

        body = response.content.lstrip() if response.content else b""
        return body.startswith(b"{") or body.startswith(b"[")

    @staticmethod
    def _detect_image_content_type(content: bytes) -> Optional[str]:
        """根据常见文件头识别图片 MIME 类型。"""
        if not content:
            return None

        if content.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if content.startswith((b"GIF87a", b"GIF89a")):
            return "image/gif"
        if content.startswith(b"BM"):
            return "image/bmp"
        if len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WEBP":
            return "image/webp"

        return None

    @staticmethod
    def _looks_like_image(content: bytes) -> bool:
        """根据常见文件头判断响应体是否看起来像图片数据。"""
        return PictureCapture._detect_image_content_type(content) is not None

    def _build_binary_snapshot(
        self,
        response: requests.Response,
        fallback: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """将图片流响应转换为可序列化的抓拍摘要。"""
        content = response.content or b""
        if not content:
            return None

        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        detected_content_type = PictureCapture._detect_image_content_type(content)
        if not content_type.startswith("image/"):
            content_type = detected_content_type or content_type

        if not content_type.startswith("image/") and not detected_content_type:
            return None

        snapshot = dict(fallback)
        snapshot["response_type"] = "image"
        if content_type:
            snapshot["content_type"] = content_type

        snapshot["size"] = len(content)
        local_path = self._save_snapshot_content(content, snapshot, content_type)
        if local_path:
            snapshot["local_path"] = local_path
        else:
            snapshot["local_path_error"] = "抓拍图片保存失败"
        snapshot["image_base64"] = base64.b64encode(content).decode("ascii")
        return snapshot

    @classmethod
    def _parse_snapshot_json_payload(
        cls,
        payload: Any,
        fallback: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
        """解析 JSON 抓拍响应，并选出最新的一条抓拍。"""
        snapshots = cls._extract_snapshot_records(payload)
        normalized_snapshots = [
            cls._normalize_snapshot_record(snapshot, fallback)
            for snapshot in snapshots
        ]
        latest_snapshot = None
        if normalized_snapshots:
            latest_snapshot = max(normalized_snapshots, key=cls._snapshot_sort_key)
            latest_snapshot = dict(latest_snapshot)
            latest_snapshot["response_type"] = "json"

        return latest_snapshot, normalized_snapshots

    @staticmethod
    def _coerce_int(value: Any, default: int = 0) -> int:
        """将输入尽量转换为整数，失败时回退默认值。"""
        try:
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    return default
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _device_name_matches(device_name: Any, expected_name: Optional[str]) -> bool:
        """按设备名称过滤，支持忽略大小写的包含匹配。"""
        expected_text = str(expected_name or "").strip()
        if not expected_text:
            return True

        device_text = str(device_name or "").strip()
        if not device_text:
            return False

        normalized_expected = expected_text.casefold()
        normalized_device = device_text.casefold()
        return (
            normalized_device == normalized_expected
            or normalized_expected in normalized_device
        )

    @classmethod
    def _build_device_capture_targets(cls, device: Dict[str, Any]) -> List[Dict[str, Any]]:
        """基于设备状态记录提取待抓拍的通道目标，优先主码流。"""
        if not isinstance(device, dict):
            return []

        parsed_urls = device.get("parsed_urls")
        if not isinstance(parsed_urls, list):
            parsed_urls = []

        if not parsed_urls:
            normalized_urls = device.get("normalized_urls")
            if not isinstance(normalized_urls, dict):
                normalized_urls = cls._normalize_device_status_urls(device.get("urls"))

            for stream_key, rtsp_url in sorted(normalized_urls.items()):
                channel, _, stream = stream_key.partition("_")
                parsed_urls.append({
                    "channel": cls._normalize_channel_value(channel),
                    "stream": stream,
                    "stream_name": cls._stream_selector_display(stream),
                    "rtsp_url": rtsp_url,
                })

        device_id = cls._normalize_cache_key(device.get("device_id") or device.get("id"))
        device_name = device.get("device_name") or device.get("name")
        device_ip = device.get("device_ip") or device.get("ip")
        status = device.get("status")
        status_text = device.get("status_text")

        capture_targets: Dict[str, Dict[str, Any]] = {}
        for item in parsed_urls:
            if not isinstance(item, dict):
                continue

            channel = cls._normalize_channel_lookup_key(item.get("channel"))
            stream_type = cls._normalize_stream_selector(
                item.get("stream") or item.get("stream_type") or item.get("stream_number")
            )
            rtsp_url = item.get("rtsp_url") or item.get("url")

            if channel is None or rtsp_url in (None, ""):
                continue
            if stream_type is None:
                stream_type = "0"

            target = {
                "device_id": device_id,
                "device_name": device_name,
                "device_ip": device_ip,
                "status": status,
                "status_text": status_text,
                "channel": channel,
                "stream_type": stream_type,
                "stream_name": cls._stream_selector_display(stream_type),
                "rtsp_url": str(rtsp_url),
            }

            current_target = capture_targets.get(channel)
            if current_target is None or (
                current_target.get("stream_type") != "0" and stream_type == "0"
            ):
                capture_targets[channel] = target

        return [
            capture_targets[channel]
            for channel in sorted(
                capture_targets,
                key=lambda value: (not value.isdigit(), int(value) if value.isdigit() else value),
            )
        ]

    def _capture_device_snapshots(self, device: Dict[str, Any]) -> Dict[str, Any]:
        """对单个设备执行抓拍链路，并返回本地图片结果。"""
        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result["success"]:
            return {
                "success": False,
                "message": runtime_config_result["message"],
                "config_error": True,
            }

        if not isinstance(device, dict):
            return {
                "success": False,
                "message": "device 参数必须为设备状态记录对象",
            }

        device_id = self._normalize_cache_key(device.get("device_id") or device.get("id"))
        device_name = device.get("device_name") or device.get("name")
        if device_id is None:
            return {
                "success": False,
                "message": "设备状态记录缺少 device_id",
            }

        capture_targets = self._build_device_capture_targets(device)
        if not capture_targets:
            return {
                "success": False,
                "message": f"设备 {device_name or device_id} 没有可用的 RTSP 地址，无法抓拍",
                "params": {
                    "device_id": device_id,
                    "device_name": device_name,
                },
                "data": {
                    "device": {
                        "device_id": device_id,
                        "device_name": device_name,
                    },
                    "snapshots": [],
                    "total": 0,
                },
            }

        snapshots: List[Dict[str, Any]] = []
        output_path = self.config.snapshot_output_dir or None

        for target in capture_targets:
            channel = target.get("channel")
            stream_type = target.get("stream_type") or "0"
            channel_number = self._coerce_int(channel, default=0)
            stream_number = self._coerce_int(stream_type, default=0)
            task_code = str(uuid.uuid4())
            snapshot_record = {
                "id": task_code,
                "code": task_code,
                "device_id": device_id,
                "device_name": target.get("device_name"),
                "device_ip": target.get("device_ip"),
                "channel": channel,
                "stream_type": stream_type,
                "stream_name": target.get("stream_name"),
                "rtsp_url": target.get("rtsp_url"),
                "status": "failed",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            try:
                logger.info(
                    "开始抓拍设备: device_id=%s, device_name=%s, channel=%s, stream=%s",
                    device_id,
                    target.get("device_name"),
                    channel,
                    stream_type,
                )

                stream_info = self.add_media_stream(
                    device_id=device_id,
                    stream_url=target["rtsp_url"],
                    channel=channel_number,
                    stream_number=stream_number,
                )
                time.sleep(1)
                snapshot_info = self.create_snapshot_task(
                    device_id=device_id,
                    channel=channel_number,
                    stream_number=stream_number,
                    code=task_code,
                )
                time.sleep(1)
                task_code = snapshot_info.get("code") or task_code
                download_info = self.download_snapshot(
                    code=task_code,
                    output_path=output_path,
                )

                local_path = download_info.get("local_path")
                snapshot_record.update({
                    "id": task_code,
                    "code": task_code,
                    "stream_key": stream_info.get("stream_key"),
                    "snapshot_stream": snapshot_info.get("stream"),
                    "api_code": snapshot_info.get("api_code"),
                    "api_message": snapshot_info.get("msg"),
                    "filename": download_info.get("filename"),
                    "local_path": local_path,
                    "content_type": download_info.get("content_type"),
                    "size": download_info.get("file_size"),
                    "status": "success" if local_path else "failed",
                })

                if not local_path:
                    snapshot_record["local_path_error"] = "截图任务已提交，但未生成本地图片文件"
            except Exception as exc:
                logger.error(
                    "设备抓拍失败: device_id=%s, channel=%s, stream=%s, error=%s",
                    device_id,
                    channel,
                    stream_type,
                    exc,
                )
                snapshot_record["local_path_error"] = str(exc)

            snapshots.append(snapshot_record)

        success_count = sum(1 for snapshot in snapshots if snapshot.get("local_path"))
        failed_count = len(snapshots) - success_count
        if success_count and failed_count:
            message = f"设备 {device_name or device_id} 抓拍完成，成功 {success_count} 条，失败 {failed_count} 条"
        elif success_count:
            message = f"设备 {device_name or device_id} 抓拍完成，共 {success_count} 条"
        else:
            message = f"设备 {device_name or device_id} 抓拍失败"

        return {
            "success": success_count > 0,
            "message": message,
            "params": {
                "device_id": device_id,
                "device_name": device_name,
            },
            "data": {
                "device": {
                    "device_id": device_id,
                    "device_name": device_name,
                    "device_ip": device.get("device_ip") or device.get("ip"),
                    "status": device.get("status"),
                    "status_text": device.get("status_text"),
                },
                "snapshots": snapshots,
                "total": len(snapshots),
            },
        }
    
    def query_snapshots(
        self,
        device: Optional[Dict[str, Any]] = None,
        device_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """查询实时抓拍信息或对单个设备执行抓拍。"""
        if device is not None:
            return self._capture_device_snapshots(device)
    
    def parse_natural_language(self, text: str) -> Dict[str, Any]:
        """从自然语言中解析查询参数"""
        params = {}
        
        # 解析设备名称
        name_match = re.search(r"设备\s*([^\s]+)", text)
        if name_match:
            params["device_name"] = name_match.group(1)
            logger.info(f"从文本中解析到设备名称: {params['device_name']}")
        
        return params
    
    def execute_full_query(
        self,
        device_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """执行完整的查询流程（加载配置→设备筛选→抓拍下载→整理结果）"""
        result = {
            "success": False,
            "message": "",
            "config_result": None,
            "device_status_result": None,
            "query_result": None
        }

        config_result = self._load_runtime_config_from_vpup(force_reload=True)
        result["config_result"] = config_result

        if not config_result["success"]:
            result["message"] = f"初始化失败: {config_result['message']}"
            return result

        device_status_result = self.query_device_status_list(force_refresh=True)
        result["device_status_result"] = device_status_result
        if not device_status_result.get("success"):
            result["message"] = f"获取设备状态失败: {device_status_result.get('message', '未知错误')}"
            return result

        devices = device_status_result.get("data", [])
        if not isinstance(devices, list):
            devices = []

        filtered_devices = [
            device
            for device in devices
            if isinstance(device, dict)
            and self._device_name_matches(
                device.get("device_name") or device.get("name"),
                device_name,
            )
        ]

        if not filtered_devices:
            normalized_name = str(device_name or "").strip()
            message = (
                f"未找到名称匹配 {normalized_name} 的设备"
                if normalized_name
                else "设备状态列表为空，未找到可抓拍设备"
            )
            result["query_result"] = {
                "success": False,
                "message": message,
                "params": {
                    "device_name": device_name,
                },
                "data": {
                    "snapshots": [],
                    "total": 0,
                    "devices": [],
                    "device_count": 0,
                },
            }
            result["message"] = message
            return result

        device_results: List[Dict[str, Any]] = []
        aggregated_snapshots: List[Dict[str, Any]] = []

        for device in filtered_devices:
            device_result = self.query_snapshots(device=device, device_name=device_name)
            device_results.append(device_result)

            device_snapshots = device_result.get("data", {}).get("snapshots", [])
            if isinstance(device_snapshots, list):
                aggregated_snapshots.extend(device_snapshots)

        captured_device_count = sum(1 for item in device_results if item.get("success"))
        failed_device_count = len(device_results) - captured_device_count
        query_result = {
            "success": captured_device_count > 0,
            "message": (
                f"设备抓拍完成，成功 {captured_device_count} 个，失败 {failed_device_count} 个"
                if failed_device_count
                else f"设备抓拍完成，共 {captured_device_count} 个设备"
            ),
            "params": {
                "device_name": device_name,
            },
            "data": {
                "snapshots": aggregated_snapshots,
                "total": len(aggregated_snapshots),
                "devices": filtered_devices,
                "device_count": len(filtered_devices),
            },
            "device_results": device_results,
            "captured_device_count": captured_device_count,
            "failed_device_count": failed_device_count,
        }
        result["query_result"] = query_result
        
        if not query_result["success"]:
            result["message"] = f"查询失败: {query_result['message']}"
            return result

        snapshots = query_result.get("data", {}).get("snapshots", [])
        snapshot_summary = {
            "total": len(snapshots) if isinstance(snapshots, list) else 0,
            "matched": 0,
            "missing": 0,
            "failed": 0,
        }

        if isinstance(snapshots, list):
            for snapshot in snapshots:
                if not isinstance(snapshot, dict):
                    snapshot_summary["missing"] += 1
                    continue

                if snapshot.get("local_path") not in (None, ""):
                    snapshot_summary["matched"] += 1
                    continue

                if snapshot.get("url") not in (None, ""):
                    local_path_error = self._materialize_snapshot_from_url(snapshot)
                    if local_path_error:
                        snapshot["local_path_error"] = local_path_error

                if snapshot.get("local_path") not in (None, ""):
                    snapshot_summary["matched"] += 1
                elif snapshot.get("local_path_error") not in (None, "") or snapshot.get("status") == "failed":
                    snapshot_summary["failed"] += 1
                else:
                    snapshot_summary["missing"] += 1

        query_result["snapshot_summary"] = snapshot_summary
        query_result["image_attachments"] = self._build_image_attachments(
            snapshots if isinstance(snapshots, list) else []
        )

        result["success"] = snapshot_summary["matched"] > 0

        message_parts = []
        if query_result.get("failed_device_count", 0) > 0:
            message_parts.append(f"{query_result['failed_device_count']} 个设备抓拍失败")
        if snapshot_summary["failed"] > 0:
            message_parts.append(f"{snapshot_summary['failed']} 条抓拍获取失败")
        if snapshot_summary["missing"] > 0:
            message_parts.append(f"{snapshot_summary['missing']} 条抓拍未匹配")

        if not result["success"]:
            if message_parts:
                result["message"] = f"查询流程完成，但未获取到本地抓拍图片；{'；'.join(message_parts)}"
            else:
                result["message"] = "查询流程完成，但未获取到本地抓拍图片"
        elif message_parts:
            result["message"] = f"查询流程完成，但{'；'.join(message_parts)}"
        else:
            result["message"] = "查询流程完成"
        
        return result

    def query_device_status_list(self, force_refresh: bool = True) -> Dict[str, Any]:
        """查询设备状态列表，并缓存每个设备的 RTSP 地址。"""
        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result["success"]:
            return {
                "success": False,
                "message": runtime_config_result["message"],
                "config_error": True
            }

        if self.device_status_records and not force_refresh:
            return {
                "success": True,
                "message": "获取设备状态成功（缓存）",
                "data": self.device_status_records,
                "device_count": len(self.device_status_records),
                "cached_device_count": len(self.device_status_cache),
                "cached_url_device_count": sum(1 for urls in self.device_rtsp_urls.values() if urls),
                "from_cache": True,
            }

        url = f"{self._build_service_base_url(self.config.device_service_port)}/api/devicesvc/v1/devicestatus"
        headers = self._build_auth_headers()

        logger.info(f"查询设备状态列表: {url}")

        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.config.timeout
            )
            response.raise_for_status()

            if not self._response_is_json(response):
                content_type = response.headers.get("Content-Type", "unknown")
                logger.error(f"查询设备状态失败: 无法识别的响应类型 {content_type}")
                return {
                    "success": False,
                    "message": f"查询设备状态失败: 无法识别的响应类型 {content_type}",
                }

            result = response.json()
            if result.get("code") != 1000000:
                error_msg = result.get("message", "未知错误")
                logger.error(f"查询设备状态失败: {error_msg}")
                return {
                    "success": False,
                    "message": f"查询设备状态失败: {error_msg}",
                    "code": result.get("code"),
                }

            response_data = result.get("data", [])
            if not isinstance(response_data, list):
                response_data = []

            self._cache_device_status_entries(response_data)

            logger.info(
                "查询设备状态成功，共 %s 个设备，缓存到 %s 个设备 RTSP 地址",
                len(self.device_status_records),
                sum(1 for urls in self.device_rtsp_urls.values() if urls),
            )
            return {
                "success": True,
                "message": "查询设备状态成功",
                "data": self.device_status_records,
                "code": result.get("code"),
                "api_message": result.get("message"),
                "timestamp": result.get("timestamp"),
                "device_count": len(self.device_status_records),
                "cached_device_count": len(self.device_status_cache),
                "cached_url_device_count": sum(1 for urls in self.device_rtsp_urls.values() if urls),
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"查询设备状态请求失败: {str(e)}")
            return {
                "success": False,
                "message": f"查询设备状态请求失败: {str(e)}",
            }
        except (KeyError, ValueError) as e:
            logger.error(f"查询设备状态响应解析失败: {str(e)}")
            return {
                "success": False,
                "message": f"查询设备状态响应解析失败: {str(e)}",
            }

    def get_device_status_urls(
        self,
        device_id: Any,
        auto_refresh: bool = True
    ) -> Dict[str, Any]:
        """根据设备 ID 获取已缓存的 urls 列表。"""
        normalized_device_id = self._normalize_cache_key(device_id)
        if normalized_device_id is None:
            return {
                "success": False,
                "message": "device_id 不能为空",
            }

        device_info = self.device_status_cache.get(normalized_device_id)
        urls = self.device_rtsp_urls.get(normalized_device_id)

        if device_info is None and auto_refresh:
            refresh_result = self.query_device_status_list(force_refresh=True)
            if not refresh_result.get("success"):
                return {
                    "success": False,
                    "message": refresh_result.get("message", "刷新设备状态失败"),
                    "refresh_result": refresh_result,
                }

            device_info = self.device_status_cache.get(normalized_device_id)
            urls = self.device_rtsp_urls.get(normalized_device_id)

        if device_info is None:
            return {
                "success": False,
                "message": f"未找到设备 ID 为 {normalized_device_id} 的状态信息",
                "device_id": normalized_device_id,
            }

        return {
            "success": True,
            "message": "获取设备 RTSP 地址列表成功",
            "data": {
                "device_id": normalized_device_id,
                "device_name": device_info.get("name"),
                "status": device_info.get("status"),
                "urls": urls or {},
            }
        }

    def get_device_rtsp_url(
        self,
        device_id: Any,
        channel: Any,
        stream_type: Any = "main",
        auto_refresh: bool = True
    ) -> Dict[str, Any]:
        """根据设备 ID、通道号和主子码流获取 RTSP 地址。"""
        normalized_channel = self._normalize_channel_lookup_key(channel)
        if normalized_channel is None:
            return {
                "success": False,
                "message": "channel 不能为空",
            }

        normalized_stream = self._normalize_stream_selector(stream_type)
        if normalized_stream is None:
            return {
                "success": False,
                "message": "stream_type 仅支持 main/sub/主码流/子码流/0/1",
            }

        urls_result = self.get_device_status_urls(device_id=device_id, auto_refresh=auto_refresh)
        if not urls_result.get("success"):
            return urls_result

        device_data = urls_result.get("data", {})
        device_urls = device_data.get("urls", {})
        url_key = f"{normalized_channel}_{normalized_stream}"
        rtsp_url = device_urls.get(url_key)

        if rtsp_url in (None, ""):
            return {
                "success": False,
                "message": (
                    f"设备 {device_data.get('device_id')} 未找到通道 {normalized_channel} 的"
                    f"{self._stream_selector_display(normalized_stream)} RTSP 地址"
                ),
                "device_id": device_data.get("device_id"),
                "channel": normalized_channel,
                "stream_type": normalized_stream,
                "available_streams": sorted(device_urls.keys()),
            }

        return {
            "success": True,
            "message": "获取 RTSP 地址成功",
            "data": {
                "device_id": device_data.get("device_id"),
                "device_name": device_data.get("device_name"),
                "status": device_data.get("status"),
                "channel": normalized_channel,
                "stream_type": normalized_stream,
                "stream_name": self._stream_selector_display(normalized_stream),
                "rtsp_url": rtsp_url,
                "available_streams": sorted(device_urls.keys()),
            }
        }

    def add_media_stream(
        self,
        device_id: str,
        stream_url: str,
        channel: int = 0,
        stream_number: int = 0,
        rtp_type: int = 0,
        persistent: int = 2,
    ) -> Dict[str, Any]:
        """添加媒体流信息。"""
        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result.get("success"):
            raise ValueError(runtime_config_result.get("message", "运行配置加载失败"))

        stream_name = f"{device_id}_{channel}_{stream_number}"
        data = {
            "vhost": "__defaultVhost__",
            "app": "vis",
            "stream": stream_name,
            "url": stream_url,
            "rtp_type": rtp_type,
            "persistent": persistent,
        }

        result = self._make_json_api_request(
            "POST",
            "/api/mediasvc/v1/mediastreams",
            data=data,
        )
        stream_data = result.get("data") or {}
        stream_key = stream_data.get("key") or stream_name
        return {
            "stream_key": stream_key,
            "device_id": device_id,
            "channel": channel,
            "stream_number": stream_number,
            "stream_url": stream_url,
            "rtp_type": rtp_type,
            "persistent": persistent,
        }

    def create_snapshot_task(
        self,
        device_id: str,
        channel: int = 0,
        stream_number: int = 0,
        code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """创建联动截图任务。"""
        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result.get("success"):
            raise ValueError(runtime_config_result.get("message", "运行配置加载失败"))

        stream_name = f"{device_id}_{channel}_{stream_number}"
        task_code = (code or "").strip() or str(uuid.uuid4())
        data = {
            "vhost": "__defaultVhost__",
            "app": "vis",
            "stream": stream_name,
            "code": task_code,
        }

        result = self._make_json_api_request(
            "POST",
            "/api/mediasvc/v1/linksnapshots",
            data=data,
        )
        return {
            "stream": stream_name,
            "code": task_code,
            "msg": result.get("msg") or result.get("message"),
            "api_code": result.get("code"),
        }

    def download_snapshot(
        self,
        code: Any,
        output_path: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """按截图任务 code 下载图片。"""
        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result.get("success"):
            raise ValueError(runtime_config_result.get("message", "运行配置加载失败"))

        code_str = _normalize_snapshot_code_str(code)
        url = f"{self._build_service_base_url(self.config.media_service_port)}/api/mediasvc/v1/snapshots"
        headers = self._build_auth_headers()
        params = {"code": code_str}
        pull_retries, pull_interval = _snapshot_download_retry_settings()

        response: Optional[requests.Response] = None
        try:
            for attempt in range(pull_retries):
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.config.timeout,
                    stream=True,
                )
                if response.status_code in (404, 503) and attempt < pull_retries - 1:
                    response.close()
                    time.sleep(pull_interval)
                    continue
                response.raise_for_status()
                break

            if response is None:
                raise ValueError("截图下载未获得响应")

            content_type = response.headers.get("Content-Type", "")
            normalized_content_type = content_type.split(";", 1)[0].strip().lower()
            if "image" not in normalized_content_type and "octet-stream" not in normalized_content_type:
                first_chunk = next(response.iter_content(chunk_size=8192), b"")
                detected_type = self._detect_image_content_type(first_chunk)
                if not detected_type:
                    raise ValueError(f"响应不是图片或二进制流: {content_type}")
                normalized_content_type = detected_type
                chunks = [first_chunk]
            else:
                chunks = []

            if not filename:
                content_disposition = response.headers.get("Content-Disposition", "")
                filename_match = re.search(r'filename="?([^";]+)"?', content_disposition)
                if filename_match:
                    filename = filename_match.group(1)
                else:
                    filename = f"snapshot_{code_str}_{int(time.time())}.jpg"

            local_path = None
            file_size = 0

            if output_path:
                output_dir = Path(output_path).expanduser()
                output_dir.mkdir(parents=True, exist_ok=True)
                target_path = output_dir / filename

                with target_path.open("wb") as handle:
                    for chunk in chunks:
                        if chunk:
                            handle.write(chunk)
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            handle.write(chunk)

                file_size = target_path.stat().st_size
                if file_size == 0:
                    target_path.unlink(missing_ok=True)
                    raise ValueError("下载的文件为空")
                local_path = str(target_path.resolve())

            return {
                "code": code_str,
                "filename": filename,
                "local_path": local_path,
                "file_size": file_size,
                "content_type": normalized_content_type or content_type,
            }
        except requests.exceptions.RequestException as exc:
            raise ValueError(f"截图下载失败: {exc}") from exc
        except Exception as exc:
            raise ValueError(f"处理截图文件失败: {exc}") from exc
        finally:
            if response is not None:
                response.close()

    def format_snapshot_result(self, result: Dict[str, Any]) -> str:
        """格式化抓拍查询结果"""
        if not result.get("success"):
            return f"❌ 查询失败: {result.get('message', '未知错误')}"
        
        query_result = result.get("query_result", {})
        if not query_result.get("success"):
            return f"❌ 抓拍查询失败: {query_result.get('message', '未知错误')}"
        
        data = query_result.get("data", {})
        snapshots = data.get("snapshots") if isinstance(data, dict) else None
        if isinstance(snapshots, list):
            snapshots = [self._normalize_snapshot_record(s) for s in snapshots]
        else:
            snapshots = self._extract_snapshot_records(data)
        total = len(snapshots) if isinstance(snapshots, list) else 0
        params = query_result.get("params", {})
        page_size = params.get("pagesize", len(snapshots) or 10)
        page_no = params.get("pageno", 0)
        api_message = query_result.get("api_message")
        timestamp = query_result.get("timestamp")
        snapshot_summary = query_result.get("snapshot_summary", {})
        image_attachments = query_result.get("image_attachments", [])

        field_labels = {
            "id": "抓拍ID",
            "code": "抓拍编码",
            "device_name": "设备名称",
            "device_id": "设备ID",
            "channel": "通道",
            "time": "抓拍时间",
            "url": "抓拍地址",
        }
        preferred_keys = [
            "id",
            "code",
            "device_name",
            "device_id",
            "channel",
            "time",
            "url",
        ]
        
        output = []
        output.append("=" * 60)
        output.append("📊 抓拍查询结果")
        output.append("=" * 60)
        output.append(f"总计: {total} 条抓拍记录")
        output.append(f"本页返回: {len(snapshots)} 条")
        output.append(f"当前页: 第 {page_no + 1} 页，每页 {page_size} 条")
        if snapshot_summary:
            output.append(
                f"抓拍汇总: 匹配 {snapshot_summary.get('matched', 0)} 条，"  
                f"未匹配 {snapshot_summary.get('missing', 0)} 条，"  
                f"失败 {snapshot_summary.get('failed', 0)} 条"
            )
        if api_message:
            output.append(f"接口消息: {api_message}")
        if timestamp is not None:
            output.append(f"响应时间戳: {timestamp}")
        output.append("")
        
        if not snapshots:
            output.append("⚠️ 当前查询条件下没有找到抓拍记录")
        else:
            output.append("📋 抓拍列表:")
            output.append("-" * 60)
            
            for i, snapshot in enumerate(snapshots, 1):
                if not isinstance(snapshot, dict):
                    output.append(f"{i}. {self._normalize_display_value(snapshot)}")
                    output.append("")
                    continue

                output.append(f"{i}. 抓拍记录")

                for key in preferred_keys:
                    if key not in snapshot:
                        continue

                    value = snapshot.get(key)
                    formatted_value = self._normalize_display_value(value)

                    output.append(f"   {field_labels.get(key, key)}: {formatted_value}")

                local_path = snapshot.get("local_path")
                if local_path not in (None, ""):
                    output.append(f"   本地路径: {local_path}")

                local_path_error = snapshot.get("local_path_error")
                if local_path_error not in (None, ""):
                    output.append(f"   本地路径错误: {local_path_error}")

                output.append("")

        if image_attachments:
            output.append("🖼️ 报告附图:")
            output.append("-" * 60)
            for index, attachment in enumerate(image_attachments, 1):
                output.append(f"{index}. 设备+通道: {self._normalize_display_value(attachment.get('title'))}")
                output.append(f"   图片路径: {self._normalize_display_value(attachment.get('local_path'))}")
                if attachment.get("snapshot_time") not in (None, ""):
                    output.append(f"   抓拍时间: {self._normalize_display_value(attachment.get('snapshot_time'))}")
                output.append("")

        return "\n".join(output)

    def format_device_status_result(self, result: Dict[str, Any]) -> str:
        """格式化设备状态列表查询结果。"""
        if not result.get("success"):
            return f"❌ 查询失败: {result.get('message', '未知错误')}"

        devices = result.get("data", [])
        if not isinstance(devices, list):
            devices = []

        output = []
        output.append("=" * 60)
        output.append("📟 设备状态列表")
        output.append("=" * 60)
        output.append(f"总计: {result.get('device_count', len(devices))} 个设备")
        output.append(f"已缓存状态设备: {result.get('cached_device_count', 0)} 个")
        output.append(f"已缓存 URL 设备: {result.get('cached_url_device_count', 0)} 个")

        api_message = result.get("api_message")
        if api_message:
            output.append(f"接口消息: {api_message}")

        timestamp = result.get("timestamp")
        if timestamp is not None:
            output.append(f"响应时间戳: {timestamp}")

        output.append("")

        if not devices:
            output.append("⚠️ 未查询到设备状态数据")
            return "\n".join(output)

        for index, device in enumerate(devices, 1):
            if not isinstance(device, dict):
                output.append(f"{index}. {self._normalize_display_value(device)}")
                output.append("")
                continue

            device_id = self._normalize_display_value(device.get("id"))
            urls = device.get("normalized_urls")
            if not isinstance(urls, dict):
                urls = self.device_rtsp_urls.get(self._normalize_cache_key(device.get("id")) or "", {})
            parsed_urls = device.get("parsed_urls")
            if not isinstance(parsed_urls, list):
                parsed_urls = []

            output.append(f"{index}. 设备 {self._normalize_display_value(device.get('name'))}")
            output.append(f"   设备ID: {device_id}")
            output.append(f"   IP: {self._normalize_display_value(device.get('ip'))}")
            output.append(f"   组ID: {self._normalize_display_value(device.get('groupid'))}")
            output.append(f"   型号: {self._normalize_display_value(device.get('model'))}")
            output.append(f"   类型: {self._normalize_display_value(device.get('type'))}")
            output.append(f"   状态: {self._normalize_display_value(device.get('status'))} ({self._normalize_display_value(device.get('status_text'))})")
            output.append(f"   错误码: {self._normalize_display_value(device.get('err'))}")
            output.append(f"   通道数: {self._normalize_display_value(device.get('channelnum'))}")
            output.append(f"   端口: {self._normalize_display_value(device.get('port'))}")
            output.append(f"   用户名: {self._normalize_display_value(device.get('username'))}")
            output.append(f"   密码: {self._normalize_display_value(device.get('password'))}")
            output.append(f"   URL 数量: {len(urls)}")
            if parsed_urls:
                for parsed_url in parsed_urls:
                    output.append(
                        f"   - 通道 {self._normalize_display_value(parsed_url.get('channel'))} / "
                        f"{self._normalize_display_value(parsed_url.get('stream_name'))}: "
                        f"{self._normalize_display_value(parsed_url.get('rtsp_url'))}"
                    )
            elif urls:
                output.append(f"   URL 键: {', '.join(sorted(urls.keys()))}")
            output.append("")

        return "\n".join(output)

    def format_rtsp_url_result(self, result: Dict[str, Any]) -> str:
        """格式化 RTSP 地址查询结果。"""
        if not result.get("success"):
            output = [f"❌ 查询失败: {result.get('message', '未知错误')}"]
            available_streams = result.get("available_streams")
            if available_streams:
                output.append(f"可用码流键: {', '.join(available_streams)}")
            return "\n".join(output)

        data = result.get("data", {})
        return "\n".join([
            "=" * 60,
            "🎥 RTSP 地址查询结果",
            "=" * 60,
            f"设备ID: {self._normalize_display_value(data.get('device_id'))}",
            f"设备名称: {self._normalize_display_value(data.get('device_name'))}",
            f"状态: {self._normalize_display_value(data.get('status'))}",
            f"通道: {self._normalize_display_value(data.get('channel'))}",
            f"码流: {self._normalize_display_value(data.get('stream_name'))}",
            f"RTSP URL: {self._normalize_display_value(data.get('rtsp_url'))}",
        ])


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="设备实时抓拍信息查询脚本")
    
    # 显式查询参数
    parser.add_argument("--name", type=str, help="设备名称")
    
    # 运行时配置参数
    parser.add_argument("--base-url", type=str, help="接口服务基础地址")
    parser.add_argument("--timeout", type=int, help="请求超时时间，单位秒")
    parser.add_argument("--snapshot-dir", type=str, help="抓拍图片本地存储目录")
    
    # 输出控制参数
    parser.add_argument("--json", action="store_true", help="返回JSON格式结果")
    parser.add_argument("--verbose", "-v", action="store_true", help="输出更详细的调试信息")
    
    args = parser.parse_args()
    
    # 配置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 初始化配置
    config = PictureCaptureConfig()
    if args.base_url:
        config.base_url = args.base_url
    if args.timeout:
        config.timeout = args.timeout
    if args.snapshot_dir:
        config.snapshot_output_dir = args.snapshot_dir
    
    # 初始化抓拍摄例
    capture = PictureCapture(config)
    
    # 执行完整查询
    result = capture.execute_full_query(
        device_name=args.name
    )
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(capture.format_snapshot_result(result))


if __name__ == "__main__":
    main()
