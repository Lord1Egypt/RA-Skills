#!/usr/bin/env python3
"""
设备报警信息查询脚本
用于查询视频监控系统的报警信息，运行参数从 Windows 临时目录中的 vpup.json 加载
"""

import base64
import hashlib
import binascii
import requests
import json
import os
import sys
import re
import argparse
import logging
import subprocess
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path, PureWindowsPath
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from urllib.parse import quote, urlencode, urljoin, urlparse

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


WINDOWS_DRIVE_PATH_RE = re.compile(r"^(?P<drive>[A-Za-z]):[\\/](?P<tail>.*)$")


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
class AlarmQueryConfig:
    """报警查询配置"""
    base_url: str = "http://127.0.0.1"
    alarm_service_port: int = 8483
    media_service_port: int = 8482
    default_page_size: int = 10
    default_page_no: int = 1
    timeout: int = 30
    max_retries: int = 3
    vpup_config_path: str = field(
        default_factory=_default_vpup_config_path
    )
    snapshot_output_dir: str = field(
        default_factory=lambda: "~/.openclaw/workspace/tmp_files/"
    )


class AlarmQuery:
    """报警查询类"""

    # 报警类型映射
    ALARM_TYPES = {
        "区域入侵": 120001,
        "绊线入侵": 120002,
        "目标识别": 120003,
        "动态检测": 120004,
        "火点报警": 110002,
        "报警输入": 120006,
        "烟雾报警": 120005,
    }
    
    def __init__(self, config: Optional[AlarmQueryConfig] = None):
        """初始化报警查询实例"""
        self.config = config or AlarmQueryConfig()
        self.session = requests.Session()
        self.token = None
        self.runtime_config_loaded = False
        self.runtime_config_error: Optional[str] = None
        self._load_runtime_config_from_vpup()

    def _clear_runtime_auth_state(self) -> None:
        """清理运行时加载的认证信息，避免沿用旧配置。"""
        self.token = None


    def _load_runtime_config_from_vpup(self, force_reload: bool = False) -> Dict[str, Any]:
        """从 Windows 临时目录中的 vpup.json 加载服务地址、token 和 tokenKey。"""
        if self.runtime_config_loaded and not force_reload:
            return {
                "success": True,
                "message": "已加载 vpup 配置",
                "data": {
                    "base_url": self.config.base_url,
                    "alarm_service_port": self.config.alarm_service_port,
                    "media_service_port": self.config.media_service_port,
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
        alarm_service = payload.get("alarmService")
        media_service = payload.get("mediaService", self.config.media_service_port)
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
            alarm_service_port = int(alarm_service)
            media_service_port = int(media_service)
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
        self.config.alarm_service_port = alarm_service_port
        self.config.media_service_port = media_service_port
        self.token = decrypted_token or None
        self.runtime_config_loaded = True
        self.runtime_config_error = None

        logger.info(
            "已从 vpup.json 加载运行配置: ip=%s, alarmService=%s, mediaService=%s, token_loaded=%s",
            ip,
            alarm_service_port,
            media_service_port,
            bool(self.token),
        )

        return {
            "success": True,
            "message": "已从 vpup.json 加载运行配置",
            "data": {
                "ip": ip,
                "alarmService": alarm_service_port,
                "mediaService": media_service_port,
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
    def _extract_alarm_records(data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """兼容不同接口字段名，提取报警记录列表。"""
        if not isinstance(data, dict):
            return []

        alarms = data.get("alarms")
        if isinstance(alarms, list):
            return alarms

        alarm_infos = data.get("alarminfos")
        if isinstance(alarm_infos, list):
            return alarm_infos

        return []

    @staticmethod
    def _extract_alarm_total(data: Dict[str, Any], alarms: Optional[List[Dict[str, Any]]] = None) -> int:
        """兼容不同接口字段名，提取报警总数。"""
        if not isinstance(data, dict):
            return 0

        for key in ("total", "allrecordcount", "recordcount", "count"):
            value = data.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, str) and value.isdigit():
                return int(value)

        if alarms is None:
            alarms = AlarmQuery._extract_alarm_records(data)

        return len(alarms)

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
    def _get_alarm_field_value(alarm: Dict[str, Any], candidate_keys: Tuple[str, ...]) -> Any:
        """按候选字段顺序提取报警字段值。"""
        for key in candidate_keys:
            if key in alarm and alarm[key] not in (None, ""):
                return alarm[key]

        for key in candidate_keys:
            if key in alarm:
                return alarm[key]

        return None

    @classmethod
    def _normalize_alarm_record(cls, alarm: Dict[str, Any]) -> Dict[str, Any]:
        """将不同接口字段归一化为统一的报警展示字段。"""
        if not isinstance(alarm, dict):
            return {
                "detail": cls._normalize_display_value(alarm)
            }

        normalized_alarm = {
            "id": cls._get_alarm_field_value(alarm, ("id", "alarmid", "alarmId")),
            "name": cls._get_alarm_field_value(alarm, ("name", "deviceName", "devicename")),
            "device_id": cls._get_alarm_field_value(alarm, ("device_id", "deviceId", "deviceid", "devId", "devid")),
            "channel": cls._normalize_channel_value(
                cls._get_alarm_field_value(
                    alarm,
                    ("channel", "channelNo", "channelno", "channelId", "channelid", "channelIndex", "channelindex", "chn", "chnid")
                )
            ),
            "detail": cls._get_alarm_field_value(alarm, ("detail", "description")),
            "time": cls._get_alarm_field_value(alarm, ("time", "alarmtime", "alarmTime", "createtime", "createTime")),
        }

        snapshot = alarm.get("snapshot")
        if snapshot not in (None, "", {}):
            normalized_alarm["snapshot"] = snapshot

        snapshot_error = alarm.get("snapshot_error")
        if snapshot_error not in (None, ""):
            normalized_alarm["snapshot_error"] = snapshot_error

        return {
            key: value
            for key, value in normalized_alarm.items()
            if value not in (None, "")
        }

    @classmethod
    def _normalize_snapshot_record(cls, snapshot: Dict[str, Any], fallback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """将不同接口字段归一化为统一的抓拍展示字段。"""
        if not isinstance(snapshot, dict):
            return {
                "detail": cls._normalize_display_value(snapshot)
            }

        normalized_snapshot = {
            "id": cls._get_alarm_field_value(snapshot, ("id", "snapshotId", "snapshotid")),
            "code": cls._get_alarm_field_value(snapshot, ("code", "snapshotCode", "snapshotcode")),
            "device_id": cls._get_alarm_field_value(snapshot, ("device_id", "deviceId", "deviceid", "devId", "devid")),
            "device_name": cls._get_alarm_field_value(snapshot, ("device_name", "deviceName", "devicename", "name")),
            "channel": cls._normalize_channel_value(
                cls._get_alarm_field_value(
                    snapshot,
                    ("channel", "channelNo", "channelno", "channelId", "channelid", "channelIndex", "channelindex", "chn", "chnid")
                )
            ),
            "time": cls._get_alarm_field_value(
                snapshot,
                ("time", "snapshotTime", "snapshottime", "captureTime", "capturetime", "createtime", "createTime")
            ),
            "url": cls._get_alarm_field_value(
                snapshot,
                ("url", "snapshotUrl", "snapshoturl", "imageUrl", "imageurl", "fileUrl", "fileurl", "path")
            ),
        }

        if fallback:
            for key, value in fallback.items():
                if normalized_snapshot.get(key) in (None, "") and value not in (None, ""):
                    normalized_snapshot[key] = value

        return {
            key: value
            for key, value in normalized_snapshot.items()
            if value not in (None, "")
        }

    @classmethod
    def _normalize_alarm_records(cls, alarms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """仅保留报警记录中的设备名称、详情和时间信息。"""
        return [cls._normalize_alarm_record(alarm) for alarm in alarms]

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

    @classmethod
    def _build_alarm_snapshot_group_key(cls, alarm: Dict[str, Any], index: int) -> Tuple[str, str, str]:
        """为报警抓拍筛选生成分组键，优先按设备名称和通道聚合。"""
        device_name = alarm.get("name")
        channel = cls._normalize_channel_value(alarm.get("channel"))
        if device_name not in (None, "") and channel:
            return ("name", str(device_name), channel)

        device_id = alarm.get("device_id")
        if device_id not in (None, "") and channel:
            return ("device_id", str(device_id), channel)

        return ("index", str(index), "")

    @classmethod
    def _select_latest_alarm_indices_for_snapshot(cls, alarms: List[Dict[str, Any]]) -> List[int]:
        """按设备名称和通道筛选需要获取抓拍的最新报警索引。"""
        latest_alarm_by_group: Dict[Tuple[str, str, str], Tuple[int, Dict[str, Any]]] = {}

        for index, alarm in enumerate(alarms):
            if not isinstance(alarm, dict):
                continue

            normalized_alarm = cls._normalize_alarm_record(alarm)
            group_key = cls._build_alarm_snapshot_group_key(normalized_alarm, index)
            current_latest = latest_alarm_by_group.get(group_key)

            if current_latest is None:
                latest_alarm_by_group[group_key] = (index, normalized_alarm)
                continue

            if cls._snapshot_sort_key(normalized_alarm) > cls._snapshot_sort_key(current_latest[1]):
                latest_alarm_by_group[group_key] = (index, normalized_alarm)

        return [index for index, _alarm in latest_alarm_by_group.values()]

    @classmethod
    def _select_latest_snapshot(cls, alarm: Dict[str, Any], snapshots: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """按相同设备和通道筛选最新的一张抓拍。"""
        if not snapshots:
            return None

        alarm_device_id = alarm.get("device_id")
        alarm_device_name = alarm.get("name")
        alarm_channel = cls._normalize_channel_value(alarm.get("channel"))

        matched_snapshots = []
        for snapshot in snapshots:
            if not isinstance(snapshot, dict):
                continue

            snapshot_channel = cls._normalize_channel_value(snapshot.get("channel"))
            if alarm_channel and snapshot_channel and snapshot_channel != alarm_channel:
                continue

            snapshot_device_id = snapshot.get("device_id")
            snapshot_device_name = snapshot.get("device_name")
            if alarm_device_id and snapshot_device_id:
                if str(alarm_device_id) != str(snapshot_device_id):
                    continue

            if alarm_device_name and snapshot_device_name:
                if str(alarm_device_name) != str(snapshot_device_name):
                    continue

            matched_snapshots.append(snapshot)

        candidates = matched_snapshots or snapshots
        return max(candidates, key=cls._snapshot_sort_key)

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
    def _build_image_attachments(cls, alarms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """从报警列表中提取上层可直接发送的图片附件。"""
        attachments: List[Dict[str, Any]] = []

        for alarm in alarms:
            if not isinstance(alarm, dict):
                continue

            normalized_alarm = cls._normalize_alarm_record(alarm)
            snapshot = alarm.get("snapshot")
            if not isinstance(snapshot, dict):
                continue

            local_path = snapshot.get("local_path")
            if local_path in (None, ""):
                continue

            channel = snapshot.get("channel") or normalized_alarm.get("channel")
            attachments.append({
                "title": cls._build_snapshot_title(normalized_alarm.get("name"), channel),
                "device_name": normalized_alarm.get("name"),
                "channel": channel,
                "alarm_id": normalized_alarm.get("id"),
                "alarm_time": normalized_alarm.get("time"),
                "snapshot_time": snapshot.get("time"),
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
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

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
        return AlarmQuery._detect_image_content_type(content) is not None

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
        detected_content_type = AlarmQuery._detect_image_content_type(content)
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
        normalized_alarm: Dict[str, Any],
        fallback: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
        """解析 JSON 抓拍响应，并选出与报警最匹配的一条抓拍。"""
        snapshots = cls._extract_snapshot_records(payload)
        normalized_snapshots = [
            cls._normalize_snapshot_record(snapshot, fallback)
            for snapshot in snapshots
        ]
        latest_snapshot = cls._select_latest_snapshot(normalized_alarm, normalized_snapshots)
        if latest_snapshot:
            latest_snapshot = dict(latest_snapshot)
            latest_snapshot["response_type"] = "json"

        return latest_snapshot, normalized_snapshots
    
    def query_alarms(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        alarm_type: Optional[int] = None,
        device_name: Optional[str] = None,
        alarm_id: Optional[str] = None,
        page_size: Optional[int] = None,
        page_no: Optional[int] = None
    ) -> Dict[str, Any]:
        """查询报警信息"""
        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result["success"]:
            return {
                "success": False,
                "message": runtime_config_result["message"],
                "config_error": True
            }
        
        # 设置默认值
        if page_size is None:
            page_size = self.config.default_page_size
        if page_no is None:
            page_no = self.config.default_page_no
        
        # 设置默认时间范围
        if not start_time:
            start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        
        if not end_time:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建查询参数
        params = {
            "pagesize": page_size,
            "pageno": page_no,
            "starttime": start_time,
            "endtime": end_time
        }
        
        if alarm_type:
            params["type"] = alarm_type
        
        if device_name:
            params["name"] = device_name
        
        if alarm_id:
            params["alarmid"] = alarm_id
        
        url = f"{self._build_service_base_url(self.config.alarm_service_port)}/api/alarmsvc/v1/alarminfos"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        request_url = f"{url}?{self._encode_query_params(params)}"
        
        logger.info(f"查询报警信息: {url}")
        logger.info(f"查询参数: {params}")
        logger.debug(f"查询请求URL: {request_url}")
        
        try:
            response = self.session.get(
                request_url,
                headers=headers,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("code") == 1000000:  # 操作成功
                response_data = result.get("data", {})
                if not isinstance(response_data, dict):
                    response_data = {}

                alarms = self._extract_alarm_records(response_data)
                normalized_alarms = self._normalize_alarm_records(alarms)
                total = self._extract_alarm_total(response_data, alarms)

                normalized_data = dict(response_data)
                normalized_data["alarms"] = normalized_alarms
                normalized_data["total"] = total

                logger.info(f"查询成功，总记录数 {total} 条，当前返回 {len(alarms)} 条")
                return {
                    "success": True,
                    "message": "查询成功",
                    "data": normalized_data,
                    "code": result.get("code"),
                    "api_message": result.get("message"),
                    "timestamp": result.get("timestamp"),
                    "params": params
                }
            else:
                error_msg = result.get("message", "未知错误")
                logger.error(f"查询失败: {error_msg}")
                return {
                    "success": False,
                    "message": f"查询失败: {error_msg}",
                    "code": result.get("code"),
                    "params": params
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"查询请求失败: {str(e)}")
            return {
                "success": False,
                "message": f"查询请求失败: {str(e)}",
                "params": params
            }
        except (KeyError, ValueError) as e:
            logger.error(f"查询响应解析失败: {str(e)}")
            return {
                "success": False,
                "message": f"查询响应解析失败: {str(e)}",
                "params": params
            }

    def get_alarm_snapshot(self, alarm: Dict[str, Any]) -> Dict[str, Any]:
        """根据报警 ID 和通道获取同设备同通道最新的一张报警抓拍。"""
        normalized_alarm = self._normalize_alarm_record(alarm)
        alarm_id = normalized_alarm.get("id")
        channel = normalized_alarm.get("channel")

        if not alarm_id or not channel:
            return {
                "success": False,
                "message": "报警记录缺少 id 或通道，无法获取报警抓拍",
                "alarm": normalized_alarm
            }

        runtime_config_result = self._ensure_runtime_config()
        if not runtime_config_result["success"]:
            return {
                "success": False,
                "message": runtime_config_result["message"],
                "config_error": True,
                "alarm": normalized_alarm
            }

        code = f"{alarm_id}_{channel}"
        params = {"code": code}
        url = f"{self._build_service_base_url(self.config.media_service_port)}/api/mediasvc/v1/snapshots"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        request_url = f"{url}?{self._encode_query_params(params)}"
        fallback = {
            "code": code,
            "device_id": normalized_alarm.get("device_id"),
            "device_name": normalized_alarm.get("name"),
            "channel": channel,
        }

        logger.info(f"获取报警抓拍: {url}")
        logger.info(f"抓拍查询参数: {params}")
        logger.debug(f"抓拍请求URL: {request_url}")

        try:
            response = self.session.get(
                url,
                headers=headers,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()

            if self._response_is_json(response):
                result = response.json()
                payload = result
                api_message = "获取报警抓拍成功"

                if isinstance(result, dict) and "code" in result:
                    if result.get("code") != 1000000:
                        error_msg = result.get("message", "未知错误")
                        logger.error(f"获取报警抓拍失败: {error_msg}")
                        return {
                            "success": False,
                            "message": f"获取报警抓拍失败: {error_msg}",
                            "code": result.get("code"),
                            "params": params
                        }

                    payload = result.get("data", {})
                    api_message = result.get("message", api_message)

                snapshot, normalized_snapshots = self._parse_snapshot_json_payload(
                    payload,
                    normalized_alarm,
                    fallback
                )

                if snapshot:
                    local_path_error = self._materialize_snapshot_from_url(snapshot)
                    if local_path_error:
                        snapshot["local_path_error"] = local_path_error

                    logger.info(f"获取报警抓拍成功，解析到 {len(normalized_snapshots)} 条 JSON 抓拍记录")
                    return {
                        "success": True,
                        "message": api_message,
                        "data": {
                            "snapshot": snapshot,
                            "count": len(normalized_snapshots)
                        },
                        "status_code": response.status_code,
                        "params": params
                    }

                logger.info("获取报警抓拍成功，但未解析到抓拍记录")
                return {
                    "success": True,
                    "message": "获取报警抓拍成功，但未解析到抓拍记录",
                    "data": {
                        "snapshot": None,
                        "count": len(normalized_snapshots)
                    },
                    "status_code": response.status_code,
                    "params": params
                }

            snapshot = self._build_binary_snapshot(response, fallback)
            if snapshot:
                logger.info("获取报警抓拍成功，响应类型为图片流")
                return {
                    "success": True,
                    "message": "获取报警抓拍成功，返回图片流",
                    "data": {
                        "snapshot": snapshot,
                        "count": 1
                    },
                    "status_code": response.status_code,
                    "params": params
                }

            content_type = response.headers.get("Content-Type", "unknown")
            logger.error(f"获取报警抓拍失败: 无法识别的响应类型 {content_type}")
            return {
                "success": False,
                "message": f"获取报警抓拍失败: 无法识别的响应类型 {content_type}",
                "status_code": response.status_code,
                "params": params
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"获取报警抓拍请求失败: {str(e)}")
            return {
                "success": False,
                "message": f"获取报警抓拍请求失败: {str(e)}",
                "params": params
            }
        except (KeyError, ValueError) as e:
            logger.error(f"获取报警抓拍响应解析失败: {str(e)}")
            return {
                "success": False,
                "message": f"获取报警抓拍响应解析失败: {str(e)}",
                "params": params
            }
    
    def parse_natural_language(self, text: str) -> Dict[str, Any]:
        """从自然语言中解析查询参数"""
        params = {}
        
        # 解析报警类型
        for alarm_name, alarm_code in self.ALARM_TYPES.items():
            if alarm_name in text:
                params["alarm_type"] = alarm_code
                logger.info(f"从文本中解析到报警类型: {alarm_name} -> {alarm_code}")
                break
        
        # 解析时间范围（简化版本）
        time_patterns = [
            (r"今天", lambda: (
                datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )),
            (r"昨天", lambda: (
                (datetime.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S"),
                (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
            )),
            (r"(\d{4}-\d{2}-\d{2})", lambda match: (
                f"{match.group(1)} 00:00:00",
                f"{match.group(1)} 23:59:59"
            )),
        ]
        
        for pattern, handler in time_patterns:
            match = re.search(pattern, text)
            if match:
                if callable(handler):
                    start, end = handler() if pattern == r"今天" or pattern == r"昨天" else handler(match)
                    params["start_time"] = start
                    params["end_time"] = end
                    logger.info(f"从文本中解析到时间范围: {start} 到 {end}")
                break
        
        # 解析设备名称
        name_match = re.search(r"设备\s*([^\s]+)", text)
        if name_match:
            params["device_name"] = name_match.group(1)
            logger.info(f"从文本中解析到设备名称: {params['device_name']}")
        
        # 解析报警ID
        id_match = re.search(r"报警ID\s*[:：]?\s*(\w+)", text) or re.search(r"ID\s*[:：]?\s*(\w+)", text)
        if id_match:
            params["alarm_id"] = id_match.group(1)
            logger.info(f"从文本中解析到报警ID: {params['alarm_id']}")
        
        # 解析分页
        page_match = re.search(r"第\s*(\d+)\s*页", text)
        if page_match:
            params["page_no"] = int(page_match.group(1)) - 1  # 转换为0-based
            logger.info(f"从文本中解析到页码: {params['page_no'] + 1}")
        
        size_match = re.search(r"(\d+)\s*条", text)
        if size_match:
            params["page_size"] = int(size_match.group(1))
            logger.info(f"从文本中解析到每页条数: {params['page_size']}")
        
        return params
    
    def execute_full_query(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        alarm_type: Optional[int] = None,
        device_name: Optional[str] = None,
        alarm_id: Optional[str] = None,
        page_size: Optional[int] = None,
        page_no: Optional[int] = None
    ) -> Dict[str, Any]:
        """执行完整的查询流程（加载配置→查询→抓拍）"""
        result = {
            "success": False,
            "message": "",
            "config_result": None,
            "login_result": None,
            "query_result": None,
            "logout_result": None
        }

        config_result = self._load_runtime_config_from_vpup(force_reload=True)
        result["config_result"] = config_result

        if not config_result["success"]:
            result["message"] = f"初始化失败: {config_result['message']}"
            return result

        query_result = self.query_alarms(
            start_time=start_time,
            end_time=end_time,
            alarm_type=alarm_type,
            device_name=device_name,
            alarm_id=alarm_id,
            page_size=page_size,
            page_no=page_no
        )
        result["query_result"] = query_result
        
        if not query_result["success"]:
            result["message"] = f"查询失败: {query_result['message']}"
            return result

        alarms = query_result.get("data", {}).get("alarms", [])
        snapshot_summary = {
            "total": len(alarms) if isinstance(alarms, list) else 0,
            "matched": 0,
            "missing": 0,
            "failed": 0,
            "skipped": 0,
        }

        if isinstance(alarms, list):
            latest_alarm_indices = set(self._select_latest_alarm_indices_for_snapshot(alarms))

            for index, alarm in enumerate(alarms):
                if not isinstance(alarm, dict):
                    snapshot_summary["missing"] += 1
                    continue

                if index not in latest_alarm_indices:
                    alarm["snapshot_error"] = "已跳过：仅为同设备同通道的最新报警获取抓拍"
                    snapshot_summary["skipped"] += 1
                    continue

                snapshot_result = self.get_alarm_snapshot(alarm)
                snapshot = snapshot_result.get("data", {}).get("snapshot") if snapshot_result.get("success") else None

                if snapshot:
                    alarm["snapshot"] = snapshot
                    snapshot_summary["matched"] += 1
                elif snapshot_result.get("success"):
                    alarm["snapshot_error"] = snapshot_result.get("message")
                    snapshot_summary["missing"] += 1
                else:
                    alarm["snapshot_error"] = snapshot_result.get("message")
                    snapshot_summary["failed"] += 1

        query_result["snapshot_summary"] = snapshot_summary
        query_result["image_attachments"] = self._build_image_attachments(
            alarms if isinstance(alarms, list) else []
        )
        
        result["success"] = True

        message_parts = []
        if snapshot_summary["failed"] > 0:
            message_parts.append(f"{snapshot_summary['failed']} 条报警抓拍获取失败")
        if snapshot_summary["missing"] > 0:
            message_parts.append(f"{snapshot_summary['missing']} 条报警未匹配到抓拍")
        if snapshot_summary["skipped"] > 0:
            message_parts.append(f"已跳过 {snapshot_summary['skipped']} 条同设备同通道的非最新报警抓拍")

        if message_parts:
            result["message"] = f"查询流程完成，但{'；'.join(message_parts)}"
        else:
            result["message"] = "查询流程完成"
        
        return result

    def format_alarm_result(self, result: Dict[str, Any]) -> str:
        """格式化报警查询结果"""
        if not result.get("success"):
            return f"❌ 查询失败: {result.get('message', '未知错误')}"
        
        query_result = result.get("query_result", {})
        if not query_result.get("success"):
            return f"❌ 报警查询失败: {query_result.get('message', '未知错误')}"
        
        data = query_result.get("data", {})
        alarms = data.get("alarms") if isinstance(data, dict) else None
        if isinstance(alarms, list):
            alarms = self._normalize_alarm_records(alarms)
        else:
            alarms = self._normalize_alarm_records(self._extract_alarm_records(data))
        total = self._extract_alarm_total(data, alarms)
        params = query_result.get("params", {})
        page_size = params.get("pagesize", len(alarms) or 10)
        page_no = params.get("pageno", 0)
        api_message = query_result.get("api_message")
        timestamp = query_result.get("timestamp")
        snapshot_summary = query_result.get("snapshot_summary", {})
        image_attachments = query_result.get("image_attachments", [])

        type_reverse = {v: k for k, v in self.ALARM_TYPES.items()}
        field_labels = {
            "id": "报警ID",
            "name": "设备名称",
            "channel": "通道",
            "detail": "报警详情",
            "time": "时间",
        }
        preferred_keys = [
            "id",
            "name",
            "channel",
            "detail",
            "time",
        ]
        
        output = []
        output.append("=" * 60)
        output.append("📊 报警查询结果")
        output.append("=" * 60)
        output.append(f"总计: {total} 条报警记录")
        output.append(f"本页返回: {len(alarms)} 条")
        output.append(f"当前页: 第 {page_no + 1} 页，每页 {page_size} 条")
        if snapshot_summary:
            output.append(
                f"抓拍汇总: 匹配 {snapshot_summary.get('matched', 0)} 条，"
                f"未匹配 {snapshot_summary.get('missing', 0)} 条，"
                f"失败 {snapshot_summary.get('failed', 0)} 条，"
                f"跳过 {snapshot_summary.get('skipped', 0)} 条"
            )
        if api_message:
            output.append(f"接口消息: {api_message}")
        if timestamp is not None:
            output.append(f"响应时间戳: {timestamp}")
        output.append("")
        
        if not alarms:
            output.append("⚠️ 当前查询条件下没有找到报警记录")
        else:
            output.append("📋 报警列表:")
            output.append("-" * 60)
            
            for i, alarm in enumerate(alarms, 1):
                if not isinstance(alarm, dict):
                    output.append(f"{i}. {self._normalize_display_value(alarm)}")
                    output.append("")
                    continue

                output.append(f"{i}. 报警记录")

                for key in preferred_keys:
                    if key not in alarm:
                        continue

                    value = alarm.get(key)
                    formatted_value = self._normalize_display_value(value)

                    output.append(f"   {field_labels.get(key, key)}: {formatted_value}")

                snapshot = alarm.get("snapshot")
                if isinstance(snapshot, dict) and snapshot:
                    output.append("   报警抓拍:")
                    if snapshot.get("response_type") not in (None, ""):
                        response_type = snapshot.get("response_type")
                        if response_type == "image":
                            response_type = "图片流"
                        elif response_type == "json":
                            response_type = "JSON"
                        output.append(f"      返回类型: {self._normalize_display_value(response_type)}")
                    if snapshot.get("time") not in (None, ""):
                        output.append(f"      抓拍时间: {self._normalize_display_value(snapshot.get('time'))}")
                    if snapshot.get("channel") not in (None, ""):
                        output.append(f"      抓拍通道: {self._normalize_display_value(snapshot.get('channel'))}")
                    if snapshot.get("url") not in (None, ""):
                        output.append(f"      抓拍地址: {self._normalize_display_value(snapshot.get('url'))}")
                    if snapshot.get("code") not in (None, ""):
                        output.append(f"      抓拍编码: {self._normalize_display_value(snapshot.get('code'))}")
                    if snapshot.get("content_type") not in (None, ""):
                        output.append(f"      抓拍类型: {self._normalize_display_value(snapshot.get('content_type'))}")
                    if snapshot.get("size") not in (None, ""):
                        output.append(f"      抓拍大小: {self._normalize_display_value(snapshot.get('size'))} bytes")
                    if snapshot.get("local_path") not in (None, ""):
                        output.append(f"      本地文件: {self._normalize_display_value(snapshot.get('local_path'))}")
                    if snapshot.get("local_path_error") not in (None, ""):
                        output.append(f"      文件状态: {self._normalize_display_value(snapshot.get('local_path_error'))}")
                    elif snapshot.get("image_base64") not in (None, "") and snapshot.get("local_path") in (None, ""):
                        output.append("      抓拍内容: 已解析图片数据，但未生成本地文件")
                elif alarm.get("snapshot_error"):
                    output.append(f"   抓拍状态: {self._normalize_display_value(alarm.get('snapshot_error'))}")

                output.append("")
        
        # 查询参数信息
        output.append("🔍 查询参数:")
        output.append(f"   时间范围: {params.get('starttime', 'N/A')} 到 {params.get('endtime', 'N/A')}")
        if params.get('type'):
            output.append(f"   报警类型: {type_reverse.get(params['type'], params['type'])}")
        if params.get('name'):
            output.append(f"   设备名称: {params['name']}")
        if params.get('alarmid'):
            output.append(f"   报警ID: {params['alarmid']}")

        if image_attachments:
            output.append("")
            output.append("🖼️ 报告附图:")
            output.append("-" * 60)
            for index, attachment in enumerate(image_attachments, 1):
                output.append(f"{index}. 设备+通道: {self._normalize_display_value(attachment.get('title'))}")
                output.append(f"   图片路径: {self._normalize_display_value(attachment.get('local_path'))}")
                if attachment.get("snapshot_time") not in (None, ""):
                    output.append(f"   抓拍时间: {self._normalize_display_value(attachment.get('snapshot_time'))}")
                output.append("")
        
        output.append("=" * 60)
        
        return "\n".join(output)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="设备报警信息查询工具")
    
    # 查询参数
    parser.add_argument("--start", type=str, help="开始时间 (格式: YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--end", type=str, help="结束时间 (格式: YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--type", type=int, help="报警类型代码")
    parser.add_argument("--name", type=str, help="设备名称模糊匹配")
    parser.add_argument("--alarmid", type=str, help="报警ID")
    parser.add_argument("--pagesize", type=int, default=10, help="每页记录数")
    parser.add_argument("--pageno", type=int, default=1, help="分页页号（从0开始）")
    
    # 自然语言查询
    parser.add_argument("--text", type=str, help="从自然语言文本中解析查询参数")
    
    # 配置参数
    parser.add_argument("--base-url", type=str, default="http://127.0.0.1", help="API基础URL")
    parser.add_argument("--timeout", type=int, default=30, help="请求超时时间（秒）")
    parser.add_argument("--snapshot-dir", type=str, help="抓拍图片本地存储目录")
    
    # 输出选项
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出模式")
    parser.add_argument("--json", action="store_true", help="输出JSON格式结果")
    
    return parser.parse_args()


def configure_console_output():
    """尽量启用 UTF-8 控制台输出，避免 Windows 默认编码导致打印失败。"""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except ValueError:
                logger.debug(f"无法重新配置 {stream_name} 编码，继续使用当前编码")


def main():
    """命令行主函数"""
    configure_console_output()
    args = parse_arguments()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 创建配置
    config = AlarmQueryConfig(
        base_url=args.base_url,
        timeout=args.timeout
    )
    if args.snapshot_dir:
        config.snapshot_output_dir = args.snapshot_dir
    
    # 创建查询实例
    alarm_query = AlarmQuery(config)
    
    # 解析查询参数
    query_params = {}
    
    if args.text:
        # 从自然语言文本中解析参数
        logger.info(f"解析自然语言文本: {args.text}")
        parsed_params = alarm_query.parse_natural_language(args.text)
        query_params.update(parsed_params)
        
        # 输出解析结果
        if args.verbose:
            print(f"解析到的参数: {parsed_params}")
    
    # 命令行参数优先级高于文本解析
    if args.start:
        query_params["start_time"] = args.start
    if args.end:
        query_params["end_time"] = args.end
    if args.type:
        query_params["alarm_type"] = args.type
    if args.name:
        query_params["device_name"] = args.name
    if args.alarmid:
        query_params["alarm_id"] = args.alarmid
    if args.pagesize:
        query_params["page_size"] = args.pagesize
    if args.pageno:
        query_params["page_no"] = args.pageno
    
    # 执行查询
    logger.info(f"执行报警查询，参数: {query_params}")
    result = alarm_query.execute_full_query(**query_params)
    
    # 输出结果
    if args.json:
        # JSON格式输出
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 格式化输出
        formatted_result = alarm_query.format_alarm_result(result)
        print(formatted_result)
    
    # 设置退出码
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()