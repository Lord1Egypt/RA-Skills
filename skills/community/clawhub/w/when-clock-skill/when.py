#!/usr/bin/env python3
"""WHEN 设备处理模块 - 不支持 chime/weather，闹钟无音量，铃音仅beep1-6"""
import datetime
import json
from urllib import parse

from when_common import (
    _http_json_get,
    _http_json_post,
    _parse_time_to_seconds,
    _parse_week_plan,
    _parse_timer_offset,
    _normalize_alarm_entry,
    _seconds_to_hhmm,
    _week_days,
    _ring_duration_text,
    ALARM_MODE_NAMES,
)


# =============================================================================
# WHEN 铃音（仅 beep1-beep6）
# =============================================================================

WHEN_RING_NAMES: dict[int, str] = {
    1: "beep1", 2: "beep2", 3: "beep3",
    4: "beep4", 5: "beep5", 6: "beep6",
}


def _ring_name(ring_code: int) -> str:
    value = ring_code + 1
    if value in WHEN_RING_NAMES:
        return WHEN_RING_NAMES[value]
    return f"未知铃音({value})"


# =============================================================================
# 不支持的模式
# =============================================================================

def _unsupported(mode: str) -> None:
    raise ValueError(f"WHEN 设备不支持 {mode} 模式，仅支持: get_alarm, set_alarm, edit_alarm, delete_alarm, set_timer")


def run_announce(base_url: str, timeout: float, override_volume: int | None = None) -> int:
    _unsupported("chime")
    return 1  # 不可能到达


def run_weather(base_url: str, timeout: float, override_volume: int | None = None) -> int:
    _unsupported("weather")
    return 1  # 不可能到达


# =============================================================================
# 闹钟操作（WHEN 无 vol 字段）
# =============================================================================

def run_get_alarm(base_url: str, timeout: float) -> int:
    get_url = f"{base_url}/get?{parse.urlencode({'type': 7})}"
    data = _http_json_get(get_url, timeout)

    alarm_num = int(data.get("alarmNum", 0))
    alarms = []
    for i, a in enumerate(data.get("alarmInfo", [])):
        mode_code = int(a.get("mode", 0))
        ring_code = int(a.get("ring", 0))
        delay_code = int(a.get("delay", 0))
        entry: dict = {
            "index": i + 1,
            "mode": ALARM_MODE_NAMES.get(mode_code, f"未知({mode_code})"),
            "time": _seconds_to_hhmm(int(a.get("time", 0))),
            "ring": _ring_name(ring_code),
            "ring_duration_level": _ring_duration_text(delay_code),
        }
        if mode_code == 2:  # 每周模式附带生效星期
            entry["active_days"] = _week_days(int(a.get("week", 0)))
        alarms.append(entry)

    summary = {
        "ok": True,
        "mode": "get_alarm",
        "alarm_count": alarm_num,
        "alarms": alarms,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


def run_set_alarm(
    base_url: str,
    timeout: float,
    config: dict,
    alarm_time: str,
    alarm_mode: str,
    alarm_week: str | None,
    alarm_ring: int | None,
    alarm_delay: int | None,
) -> int:
    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])
    if not isinstance(existing, list):
        raise ValueError("type=7 返回的 alarmInfo 不是数组")

    if len(existing) >= 10:
        raise ValueError("闹钟已达上限(10个)，无法新增")

    defaults = config.get("alarm_defaults", {})
    default_ring = int(defaults.get("ring_id", defaults.get("ring", 1))) - 1
    default_delay = int(defaults.get("ring_duration_id", defaults.get("duration_level", 3))) - 1

    mode_code = ALARM_MODE_CODES[alarm_mode]
    time_seconds = _parse_time_to_seconds(alarm_time)
    week_bits = _parse_week_plan(alarm_week)

    if mode_code == 2:
        if week_bits == 0:
            raise ValueError("每周模式需要 --alarm-week，例如: 1,2,3,4,5")
    else:
        week_bits = 0

    # WHEN 铃音限制 1-6
    ring_code = default_ring if alarm_ring is None else alarm_ring - 1
    if ring_code < 0:
        raise ValueError("--alarm-ring 必须 >= 1")
    if ring_code > 5:
        raise ValueError("WHEN 设备铃音必须在 1~6 (beep1-beep6)")

    delay_level = default_delay if alarm_delay is None else int(alarm_delay)
    if delay_level < 0:
        raise ValueError("--alarm-delay 必须 >= 0")

    # WHEN 无 vol 字段
    new_alarm = {
        "mode": mode_code,
        "week": week_bits,
        "ring": ring_code,
        "time": time_seconds,
        "delay": delay_level,
    }

    merged_alarm_info = [_normalize_alarm_entry(item, has_volume=False) for item in existing]
    merged_alarm_info.append(new_alarm)

    payload = {
        "type": 7,
        "offMode": int(alarm_data.get("offMode", 0)),
        "sensitivity": int(alarm_data.get("sensitivity", 1)),
        "holidaysStatus": int(alarm_data.get("holidaysStatus", 1)),
        "updateTime": int(alarm_data.get("updateTime", 0)),
        "ringNum": int(alarm_data.get("ringNum", 0)),
        "alarmNum": len(merged_alarm_info),
        "alarmInfo": merged_alarm_info,
    }

    resp = _http_json_post(f"{base_url}/set", payload, timeout)
    status = int(resp.get("status", 1))
    ok = status == 0

    summary = {
        "ok": ok,
        "mode": "set_alarm",
        "action": "add_alarm",
        "result": "success" if ok else "failed",
        "status": status,
        "message": str(resp.get("msg", "")),
        "alarm_count": len(merged_alarm_info),
        "added_alarm": {
            "mode": ALARM_MODE_NAMES.get(mode_code, str(mode_code)),
            "time": _seconds_to_hhmm(time_seconds),
            "ring": _ring_name(ring_code),
            "ring_duration_level": delay_level,
            "active_days": _week_days(week_bits) if mode_code == 2 else [],
        },
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


def run_delete_alarm(base_url: str, timeout: float, alarm_index: int) -> int:
    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])
    if not isinstance(existing, list):
        raise ValueError("type=7 返回的 alarmInfo 不是数组")

    if not existing:
        raise ValueError("当前没有可删除的闹钟")

    if not 1 <= alarm_index <= len(existing):
        raise ValueError(f"--alarm-index 超出范围，当前可选 1~{len(existing)}")

    normalized = [_normalize_alarm_entry(item, has_volume=False) for item in existing]
    removed_alarm = normalized.pop(alarm_index - 1)

    payload = {
        "type": 7,
        "offMode": int(alarm_data.get("offMode", 0)),
        "sensitivity": int(alarm_data.get("sensitivity", 1)),
        "holidaysStatus": int(alarm_data.get("holidaysStatus", 1)),
        "updateTime": int(alarm_data.get("updateTime", 0)),
        "ringNum": int(alarm_data.get("ringNum", 0)),
        "alarmNum": len(normalized),
        "alarmInfo": normalized,
    }

    resp = _http_json_post(f"{base_url}/set", payload, timeout)
    status = int(resp.get("status", 1))
    ok = status == 0

    removed_mode = int(removed_alarm.get("mode", 0))
    removed_week = int(removed_alarm.get("week", 0))
    removed_delay = int(removed_alarm.get("delay", 0))

    summary = {
        "ok": ok,
        "mode": "delete_alarm",
        "action": "remove_alarm",
        "result": "success" if ok else "failed",
        "status": status,
        "message": str(resp.get("msg", "")),
        "alarm_count": len(normalized),
        "removed_alarm": {
            "index": alarm_index,
            "mode": ALARM_MODE_NAMES.get(removed_mode, f"未知({removed_mode})"),
            "time": _seconds_to_hhmm(int(removed_alarm.get("time", 0))),
            "ring": _ring_name(int(removed_alarm.get("ring", 0))),
            "ring_duration_level": _ring_duration_text(removed_delay),
            "active_days": _week_days(removed_week) if removed_mode == 2 else [],
        },
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


def run_edit_alarm(
    base_url: str,
    timeout: float,
    alarm_index: int,
    alarm_time: str | None,
    alarm_mode: str | None,
    alarm_week: str | None,
    alarm_ring: int | None,
    alarm_delay: int | None,
) -> int:
    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])
    if not isinstance(existing, list):
        raise ValueError("type=7 返回的 alarmInfo 不是数组")

    if not existing:
        raise ValueError("当前没有可修改的闹钟")

    if not 1 <= alarm_index <= len(existing):
        raise ValueError(f"--alarm-index 超出范围，当前可选 1~{len(existing)}")

    normalized = [_normalize_alarm_entry(item, has_volume=False) for item in existing]
    target = dict(normalized[alarm_index - 1])

    if alarm_time is not None:
        target["time"] = _parse_time_to_seconds(alarm_time)
    if alarm_mode is not None:
        target["mode"] = ALARM_MODE_CODES[alarm_mode]
    if alarm_week is not None:
        target["week"] = _parse_week_plan(alarm_week)
    if alarm_ring is not None:
        if alarm_ring < 1:
            raise ValueError("--alarm-ring 必须 >= 1")
        if alarm_ring > 6:
            raise ValueError("WHEN 设备铃音必须在 1~6 (beep1-beep6)")
        target["ring"] = alarm_ring - 1
    if alarm_delay is not None:
        if alarm_delay < 0:
            raise ValueError("--alarm-delay 必须 >= 0")
        target["delay"] = alarm_delay

    normalized[alarm_index - 1] = target

    payload = {
        "type": 7,
        "offMode": int(alarm_data.get("offMode", 0)),
        "sensitivity": int(alarm_data.get("sensitivity", 1)),
        "holidaysStatus": int(alarm_data.get("holidaysStatus", 1)),
        "updateTime": int(alarm_data.get("updateTime", 0)),
        "ringNum": int(alarm_data.get("ringNum", 0)),
        "alarmNum": len(normalized),
        "alarmInfo": normalized,
    }

    resp = _http_json_post(f"{base_url}/set", payload, timeout)
    status = int(resp.get("status", 1))
    ok = status == 0

    mode_code = int(target["mode"])
    week_bits = int(target["week"])
    delay_code = int(target["delay"])

    summary = {
        "ok": ok,
        "mode": "edit_alarm",
        "action": "update_alarm",
        "result": "success" if ok else "failed",
        "status": status,
        "message": str(resp.get("msg", "")),
        "alarm_count": len(normalized),
        "updated_alarm": {
            "index": alarm_index,
            "mode": ALARM_MODE_NAMES.get(mode_code, str(mode_code)),
            "time": _seconds_to_hhmm(int(target["time"])),
            "ring": _ring_name(int(target["ring"])),
            "ring_duration_level": _ring_duration_text(delay_code),
            "active_days": _week_days(week_bits) if mode_code == 2 else [],
        },
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


def run_set_timer(
    base_url: str,
    timeout: float,
    config: dict,
    timer_offset: str,
    alarm_ring: int | None,
    alarm_delay: int | None,
) -> int:
    offset_seconds = _parse_timer_offset(timer_offset)
    now = datetime.datetime.now()
    target_dt = now + datetime.timedelta(seconds=offset_seconds)
    time_seconds = target_dt.hour * 3600 + target_dt.minute * 60 + target_dt.second

    defaults = config.get("alarm_defaults", {})
    default_ring = int(defaults.get("ring_id", defaults.get("ring", 1))) - 1
    default_delay = int(defaults.get("ring_duration_id", defaults.get("duration_level", 3))) - 1

    # WHEN 铃音限制 1-6
    ring_code = default_ring if alarm_ring is None else alarm_ring - 1
    if ring_code < 0:
        raise ValueError("--alarm-ring 必须 >= 1")
    if ring_code > 5:
        raise ValueError("WHEN 设备铃音必须在 1~6 (beep1-beep6)")
    delay_level = default_delay if alarm_delay is None else int(alarm_delay)
    if delay_level < 0:
        raise ValueError("--alarm-delay 必须 >= 0")

    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])

    # WHEN 无 vol 字段
    new_alarm = {
        "mode": 1,  # 单次
        "week": 0,
        "ring": ring_code,
        "time": time_seconds,
        "delay": delay_level,
    }

    normalized = [_normalize_alarm_entry(item, has_volume=False) for item in existing]
    if len(normalized) >= 10:
        # 闹钟已满，修改第10个闹钟
        normalized[9] = new_alarm
        action = "update_timer"
    else:
        normalized.append(new_alarm)
        action = "add_timer"

    payload = {
        "type": 7,
        "offMode": int(alarm_data.get("offMode", 0)),
        "sensitivity": int(alarm_data.get("sensitivity", 1)),
        "holidaysStatus": int(alarm_data.get("holidaysStatus", 1)),
        "updateTime": int(alarm_data.get("updateTime", 0)),
        "ringNum": int(alarm_data.get("ringNum", 0)),
        "alarmNum": len(normalized),
        "alarmInfo": normalized,
    }

    resp = _http_json_post(f"{base_url}/set", payload, timeout)
    status = int(resp.get("status", 1))
    ok = status == 0

    summary = {
        "ok": ok,
        "mode": "set_timer",
        "action": action,
        "result": "success" if ok else "failed",
        "status": status,
        "message": str(resp.get("msg", "")),
        "alarm_count": len(normalized),
        "timer": {
            "offset": timer_offset,
            "offset_seconds": offset_seconds,
            "trigger_at": _seconds_to_hhmm(time_seconds),
            "ring": _ring_name(ring_code),
            "ring_duration_level": _ring_duration_text(delay_level),
        },
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


# =============================================================================
# 主入口
# =============================================================================

ALARM_MODE_CODES = {
    "off": 0, "once": 1, "weekly": 2, "workday": 3, "restday": 4,
}


def run_mode(
    mode: str,
    base_url: str,
    timeout: float,
    config: dict,
    volume: int | None,
    alarm_time: str | None,
    alarm_mode: str | None,
    alarm_week: str | None,
    alarm_ring: int | None,
    alarm_delay: int | None,
    alarm_volume: int | None,
    alarm_index: int | None,
    timer_offset: str | None,
) -> int:
    # WHEN 不支持 chime 和 weather
    if mode == "chime":
        raise ValueError("WHEN 设备不支持 chime 模式")
    elif mode == "weather":
        raise ValueError("WHEN 设备不支持 weather 模式")
    elif mode == "get_alarm":
        return run_get_alarm(base_url=base_url, timeout=timeout)
    elif mode == "set_alarm":
        if not alarm_time:
            raise ValueError("set_alarm 模式必须传 --alarm-time")
        return run_set_alarm(
            base_url=base_url,
            timeout=timeout,
            config=config,
            alarm_time=alarm_time,
            alarm_mode=alarm_mode if alarm_mode is not None else "once",
            alarm_week=alarm_week,
            alarm_ring=alarm_ring,
            alarm_delay=alarm_delay,
        )
    elif mode == "delete_alarm":
        if alarm_index is None:
            raise ValueError("delete_alarm 模式必须传 --alarm-index")
        return run_delete_alarm(base_url=base_url, timeout=timeout, alarm_index=alarm_index)
    elif mode == "edit_alarm":
        if alarm_index is None:
            raise ValueError("edit_alarm 模式必须传 --alarm-index")
        return run_edit_alarm(
            base_url=base_url,
            timeout=timeout,
            alarm_index=alarm_index,
            alarm_time=alarm_time,
            alarm_mode=alarm_mode,
            alarm_week=alarm_week,
            alarm_ring=alarm_ring,
            alarm_delay=alarm_delay,
        )
    elif mode == "set_timer":
        if not timer_offset:
            raise ValueError("set_timer 模式必须传 --timer-offset，例如: '5m', '1h30m'")
        return run_set_timer(
            base_url=base_url,
            timeout=timeout,
            config=config,
            timer_offset=timer_offset,
            alarm_ring=alarm_ring,
            alarm_delay=alarm_delay,
        )
    else:
        raise ValueError(f"不支持的模式: {mode}")
