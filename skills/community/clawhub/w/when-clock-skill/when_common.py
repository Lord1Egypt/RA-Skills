#!/usr/bin/env python3
"""WHEN/WHEN Voice 公共模块 - 共享工具函数和常量"""
import datetime
import json
import re
from pathlib import Path
from urllib import error, parse, request


# =============================================================================
# 常量
# =============================================================================

DEFAULT_CONFIG = {
    "devices": [],
    "timeout": 5.0,
}

SUPPORTED_MODES = ("chime", "weather", "get_alarm", "set_alarm", "delete_alarm", "edit_alarm", "set_timer")

ALARM_MODE_NAMES: dict[int, str] = {
    0: "关闭", 1: "单次", 2: "每周", 3: "工作日", 4: "休息日",
}

ALARM_MODE_CODES: dict[str, int] = {
    "off": 0,
    "once": 1,
    "weekly": 2,
    "workday": 3,
    "restday": 4,
}

_WEEK_DAY_NAMES = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

_RING_DURATION_TEXT: dict[int, str] = {
    0: "10S", 1: "20S", 2: "30S", 3: "40S", 4: "50S",
    5: "1min", 6: "2min", 7: "3min", 8: "5min",
    9: "10min", 10: "15min", 11: "20min",
}

# =============================================================================
# HTTP 工具
# =============================================================================

def _http_json_get(url: str, timeout: float) -> dict:
    req = request.Request(url=url, method="GET")
    with request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8")
    payload = json.loads(data)
    if not isinstance(payload, dict):
        raise ValueError("GET 返回不是 JSON 对象")
    return payload


def _http_json_post(url: str, body: dict, timeout: float) -> dict:
    req = request.Request(
        url=url,
        method="POST",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8")
    payload = json.loads(data)
    if not isinstance(payload, dict):
        raise ValueError("POST 返回不是 JSON 对象")
    return payload


# =============================================================================
# 配置加载
# =============================================================================

def _create_default_config_if_missing(config_path: Path) -> None:
    if config_path.exists():
        return
    config_path.write_text(
        json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _load_config(config_path: Path) -> dict:
    _create_default_config_if_missing(config_path)
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("配置文件必须是 JSON 对象")
    return raw


def _resolve_config_path(config_arg: str) -> Path:
    script_dir = Path(__file__).resolve().parent
    raw_path = Path(config_arg).expanduser()
    if raw_path.is_absolute():
        return raw_path
    return script_dir / raw_path


# =============================================================================
# 基础工具
# =============================================================================

def _build_base_url(config: dict) -> str:
    ip = str(config.get("clock_ip", "")).strip()
    port = config.get("clock_port", 80)

    if not ip:
        raise ValueError("未配置时钟IP，请先编辑 config.json 中的 clock_ip")

    try:
        port_int = int(port)
    except (TypeError, ValueError) as exc:
        raise ValueError("clock_port 必须是整数") from exc

    if not 1 <= port_int <= 65535:
        raise ValueError("clock_port 必须在 1~65535")

    return f"http://{ip}:{port_int}"


def _get_timeout(config: dict, cli_timeout: float | None) -> float:
    if cli_timeout is not None:
        timeout = cli_timeout
    else:
        timeout = config.get("timeout", 5.0)

    timeout_f = float(timeout)
    if timeout_f <= 0:
        raise ValueError("timeout 必须大于 0")
    return timeout_f


# =============================================================================
# 时间解析
# =============================================================================

def _seconds_to_hhmm(seconds: int) -> str:
    h = (seconds // 3600) % 24
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def _parse_time_to_seconds(text: str) -> int:
    parts = text.strip().split(":")
    if len(parts) not in (2, 3):
        raise ValueError("闹钟时间格式必须是 HH:MM 或 HH:MM:SS")
    hour = int(parts[0])
    minute = int(parts[1])
    second = int(parts[2]) if len(parts) == 3 else 0
    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError("闹钟时间超出范围，小时 0~23，分钟/秒 0~59")
    return hour * 3600 + minute * 60 + second


def _parse_timer_offset(text: str) -> int:
    """解析时间偏移字符串为秒数。支持: '5m', '1h30m', '90s', '1h30m20s' 等。"""
    text = text.strip().lower().replace(" ", "")
    if not text:
        raise ValueError("--timer-offset 不能为空")
    if text.isdigit():
        seconds = int(text) * 60
        if seconds <= 0:
            raise ValueError("时间偏移必须大于 0")
        return seconds
    pattern = re.compile(r'(\d+)(h(?:ours?)?|m(?:in(?:utes?)?)?|s(?:ec(?:onds?)?)?)')
    matches = pattern.findall(text)
    if not matches:
        raise ValueError(f"无法解析的时间偏移: {text!r}，示例: '5m', '1h30m', '90s'")
    total = 0
    for value_str, unit in matches:
        value = int(value_str)
        if unit.startswith('h'):
            total += value * 3600
        elif unit.startswith('m'):
            total += value * 60
        elif unit.startswith('s'):
            total += value
    if total <= 0:
        raise ValueError("时间偏移必须大于 0")
    return total


# =============================================================================
# 星期解析
# =============================================================================

def _parse_week_plan(week_text: str | None) -> int:
    if not week_text:
        return 0

    alias: dict[str, int] = {
        "1": 1, "mon": 1, "monday": 1, "周一": 1, "一": 1,
        "2": 2, "tue": 2, "tuesday": 2, "周二": 2, "二": 2,
        "3": 3, "wed": 3, "wednesday": 3, "周三": 3, "三": 3,
        "4": 4, "thu": 4, "thursday": 4, "周四": 4, "四": 4,
        "5": 5, "fri": 5, "friday": 5, "周五": 5, "五": 5,
        "6": 6, "sat": 6, "saturday": 6, "周六": 6, "六": 6,
        "7": 7, "sun": 7, "sunday": 7, "周日": 7, "周天": 7, "日": 7, "天": 7,
    }

    week = 0
    tokens = [token.strip().lower() for token in week_text.split(",") if token.strip()]
    if not tokens:
        raise ValueError("星期计划不能为空")

    for token in tokens:
        if token not in alias:
            raise ValueError(f"无法识别的星期项: {token}")
        day = alias[token]
        week |= 1 << (day - 1)
    return week


def _week_days(week: int) -> list[str]:
    return [_WEEK_DAY_NAMES[i] for i in range(7) if week & (1 << i)]


# =============================================================================
# 闹钟相关
# =============================================================================

def _normalize_alarm_entry(raw: dict, has_volume: bool = True) -> dict:
    entry = {
        "mode": int(raw.get("mode", 0)),
        "week": int(raw.get("week", 0)),
        "ring": int(raw.get("ring", 0)),
        "time": int(raw.get("time", 0)),
        "delay": int(raw.get("delay", 0)),
    }
    if has_volume:
        entry["vol"] = int(raw.get("vol", 0))
    return entry


def _ring_duration_text(delay_code: int) -> str:
    return _RING_DURATION_TEXT.get(delay_code, f"未知({delay_code})")


def _normalize_alarm_defaults(defaults: dict) -> tuple[int, int, int]:
    """解析闹钟默认值，返回 (ring_code, delay_code, volume_code)"""
    ring_ui = int(defaults.get("ring_id", defaults.get("ring", 1)))
    duration_id = int(defaults.get("ring_duration_id", defaults.get("duration_level", 3)))
    volume_ui = int(defaults.get("volume", 20))

    if ring_ui < 1:
        raise ValueError("alarm_defaults.ring_id 必须 >= 1")
    if not 1 <= duration_id <= 12:
        raise ValueError("alarm_defaults.ring_duration_id 必须在 1~12")
    if not 1 <= volume_ui <= 30:
        raise ValueError("alarm_defaults.volume 必须在 1~30")

    delay_code = duration_id - 1
    return ring_ui - 1, delay_code, volume_ui - 1


# =============================================================================
# 设备信息获取
# =============================================================================

def get_device_info(base_url: str, timeout: float) -> dict:
    """获取设备基本信息（type=10）"""
    get_url = f"{base_url}/get?{parse.urlencode({'type': 10})}"
    return _http_json_get(get_url, timeout)


def detect_device_type(base_url: str, timeout: float) -> str:
    """检测设备类型，返回 'WHEN' 或 'WHEN Voice'"""
    info = get_device_info(base_url, timeout)
    name = info.get("name", "")
    if name == "WHEN Voice":
        return "WHEN Voice"
    elif name == "WHEN":
        return "WHEN"
    else:
        raise ValueError(f"不支持的设备类型: {name}，仅支持 WHEN 和 WHEN Voice")
