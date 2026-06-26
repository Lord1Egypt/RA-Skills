#!/usr/bin/env python3
"""WHEN Voice 设备处理模块"""
import datetime
import json
from urllib import parse

from when_common import (
    _http_json_get,
    _http_json_post,
    _build_base_url,
    _get_timeout,
    _parse_time_to_seconds,
    _parse_week_plan,
    _parse_timer_offset,
    _normalize_alarm_entry,
    _normalize_alarm_defaults,
    _seconds_to_hhmm,
    _week_days,
    _ring_duration_text,
    ALARM_MODE_NAMES,
    ALARM_MODE_CODES,
)


# =============================================================================
# 铃音名称表（WHEN Voice 50种铃音）
# =============================================================================

RING_NAMES: dict[int, str] = {
    1: "天气(1次)", 2: "天气(2次)", 3: "天气(3次)", 4: "Beep-1",
    5: "Reveille", 6: "Rest Call", 7: "Vibration-1", 8: "Vibration-2",
    9: "Tropical", 10: "Farting Around", 11: "Dotabata Panic",
    12: "Colonel Bogey March", 13: "Haretahiha Kousin",
    14: "Oato Ga Yoroshiiyode", 15: "I Met A Bear", 16: "Carmen Prelide",
    17: "Csikos Post", 18: "Ochi ga nai", 19: "Boogie Party",
    20: "Chip Music-1", 21: "Chip Music-2", 22: "Chip Music-3",
    23: "Chip Music-4", 24: "Chip Music-5", 25: "Chip Music-6",
    26: "Chip Music-7", 27: "Chip Music-8", 28: "Chip Music-9",
    29: "Chip Music-10", 30: "What a Friend We Have in Jesus",
    31: "Wedding March", 32: "We Wish You a Merry Christmas",
    33: "Under the Spiding Chestnut Tree", 34: "Jingle Bells",
    35: "Love At Home", 36: "Hotaru no Hikari", 37: "For Elise",
    38: "Hana", 39: "Salut DAmour", 40: "A Town with an Ocean View",
    41: "Heisarenai", 42: "A Very Brady Special", 43: "Morning",
    44: "Evening", 45: "Music-1", 46: "Canon in D,Pachelbel",
    47: "Autumn Relaxing Piano Music", 48: "Music-2",
    49: "Chinese-style music-1", 50: "Chinese-style music-2",
}


def _ring_name(ring_code: int) -> str:
    value = ring_code + 1
    if value in RING_NAMES:
        return RING_NAMES[value]
    return f"自定义音{value - 50}"


# =============================================================================
# chime / weather
# =============================================================================

def get_voice_chime_settings(base_url: str, timeout: float) -> tuple[int, int, bool]:
    get_url = f"{base_url}/get?{parse.urlencode({'type': 9})}"
    data = _http_json_get(get_url, timeout)

    if "announcer" not in data or "volume" not in data or "is12H" not in data:
        raise KeyError("type=9 响应缺少 announcer、volume 或 is12H 字段")

    announcer = int(data["announcer"])
    volume = int(data["volume"])
    is12h = bool(data["is12H"])
    return announcer, volume, is12h


def _resolve_volume(clock_volume: int, override_volume: int | None) -> tuple[int, int]:
    source_volume = override_volume if override_volume is not None else clock_volume
    if not 1 <= source_volume <= 30:
        raise ValueError("音量必须在 1~30")
    return source_volume, source_volume - 1


def build_type74_payload(
    announcer: int,
    volume: int,
    is12h: bool,
    override_volume: int | None,
) -> dict:
    _, use_volume = _resolve_volume(volume, override_volume)

    if announcer < 0:
        raise ValueError("announcer 不能小于 0")

    return {
        "type": 74,
        "mode": 0,
        "ring": announcer,
        "vol": use_volume,
        "sw": 1,
        "is12H": is12h,
    }


def build_type73_payload(volume: int, override_volume: int | None) -> dict:
    _, sent_volume = _resolve_volume(volume, override_volume)
    return {
        "type": 73,
        "mode": 1,
        "ring": 3,
        "sw": 1,
        "vol": sent_volume,
    }


def run_announce(base_url: str, timeout: float, override_volume: int | None) -> int:
    announcer, volume, is12h = get_voice_chime_settings(base_url, timeout)
    payload = build_type74_payload(
        announcer=announcer,
        volume=volume,
        is12h=is12h,
        override_volume=override_volume,
    )

    resp = _http_json_post(f"{base_url}/set", payload, timeout)
    status = int(resp.get("status", 1))
    ok = status == 0

    summary = {
        "ok": ok,
        "mode": "chime",
        "action": "voice_announce_preview",
        "result": "success" if ok else "failed",
        "status": status,
        "message": str(resp.get("msg", "")),
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


def run_weather(base_url: str, timeout: float, override_volume: int | None) -> int:
    _, volume, _ = get_voice_chime_settings(base_url, timeout)
    payload = build_type73_payload(volume=volume, override_volume=override_volume)

    resp = _http_json_post(f"{base_url}/set", payload, timeout)
    status = int(resp.get("status", 1))
    ok = status == 0

    summary = {
        "ok": ok,
        "mode": "weather",
        "action": "voice_weather_preview",
        "result": "success" if ok else "failed",
        "status": status,
        "message": str(resp.get("msg", "")),
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


# =============================================================================
# 闹钟操作
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
            "volume": int(a.get("vol", 0)) + 1,
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
    alarm_volume: int | None,
) -> int:
    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])
    if not isinstance(existing, list):
        raise ValueError("type=7 返回的 alarmInfo 不是数组")

    if len(existing) >= 10:
        raise ValueError("闹钟已达上限(10个)，无法新增")

    defaults = config.get("alarm_defaults", {})
    default_ring, default_delay, default_vol = _normalize_alarm_defaults(defaults)

    mode_code = ALARM_MODE_CODES[alarm_mode]
    time_seconds = _parse_time_to_seconds(alarm_time)
    week_bits = _parse_week_plan(alarm_week)

    if mode_code == 2:
        if week_bits == 0:
            raise ValueError("每周模式需要 --alarm-week，例如: 1,2,3,4,5")
    else:
        week_bits = 0

    ring_code = default_ring if alarm_ring is None else alarm_ring - 1
    if ring_code < 0:
        raise ValueError("--alarm-ring 必须 >= 1")
    if ring_code > 49:
        raise ValueError("--alarm-ring 必须在 1~50")

    delay_level = default_delay if alarm_delay is None else int(alarm_delay)
    if delay_level < 0:
        raise ValueError("--alarm-delay 必须 >= 0")

    if alarm_volume is None:
        volume_code = default_vol
    else:
        if not 1 <= alarm_volume <= 30:
            raise ValueError("--alarm-volume 必须在 1~30")
        volume_code = alarm_volume - 1

    new_alarm = {
        "mode": mode_code,
        "week": week_bits,
        "ring": ring_code,
        "time": time_seconds,
        "delay": delay_level,
        "vol": volume_code,
    }

    merged_alarm_info = [_normalize_alarm_entry(item, has_volume=True) for item in existing]
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
            "volume": volume_code + 1,
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

    normalized = [_normalize_alarm_entry(item, has_volume=True) for item in existing]
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
            "volume": int(removed_alarm.get("vol", 0)) + 1,
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
    alarm_volume: int | None,
) -> int:
    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])
    if not isinstance(existing, list):
        raise ValueError("type=7 返回的 alarmInfo 不是数组")

    if not existing:
        raise ValueError("当前没有可修改的闹钟")

    if not 1 <= alarm_index <= len(existing):
        raise ValueError(f"--alarm-index 超出范围，当前可选 1~{len(existing)}")

    normalized = [_normalize_alarm_entry(item, has_volume=True) for item in existing]
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
        if alarm_ring > 50:
            raise ValueError("--alarm-ring 必须在 1~50")
        target["ring"] = alarm_ring - 1
    if alarm_delay is not None:
        if alarm_delay < 0:
            raise ValueError("--alarm-delay 必须 >= 0")
        target["delay"] = alarm_delay
    if alarm_volume is not None:
        if not 1 <= alarm_volume <= 30:
            raise ValueError("--alarm-volume 必须在 1~30")
        target["vol"] = alarm_volume - 1

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
            "volume": int(target["vol"]) + 1,
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
    alarm_volume: int | None,
) -> int:
    offset_seconds = _parse_timer_offset(timer_offset)
    now = datetime.datetime.now()
    target_dt = now + datetime.timedelta(seconds=offset_seconds)
    time_seconds = target_dt.hour * 3600 + target_dt.minute * 60 + target_dt.second

    defaults = config.get("alarm_defaults", {})
    default_ring, default_delay, default_vol = _normalize_alarm_defaults(defaults)

    ring_code = default_ring if alarm_ring is None else alarm_ring - 1
    if ring_code < 0:
        raise ValueError("--alarm-ring 必须 >= 1")
    if ring_code > 49:
        raise ValueError("--alarm-ring 必须在 1~50")
    delay_level = default_delay if alarm_delay is None else int(alarm_delay)
    if delay_level < 0:
        raise ValueError("--alarm-delay 必须 >= 0")
    if alarm_volume is None:
        volume_code = default_vol
    else:
        if not 1 <= alarm_volume <= 30:
            raise ValueError("--alarm-volume 必须在 1~30")
        volume_code = alarm_volume - 1

    alarm_data = _http_json_get(f"{base_url}/get?{parse.urlencode({'type': 7})}", timeout)
    existing = alarm_data.get("alarmInfo", [])

    new_alarm = {
        "mode": 1,  # 单次
        "week": 0,
        "ring": ring_code,
        "time": time_seconds,
        "delay": delay_level,
        "vol": volume_code,
    }

    normalized = [_normalize_alarm_entry(item, has_volume=True) for item in existing]
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
            "volume": volume_code + 1,
        },
    }

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if ok else 1


# =============================================================================
# 主入口
# =============================================================================

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
    if mode == "chime":
        return run_announce(base_url=base_url, timeout=timeout, override_volume=volume)
    elif mode == "weather":
        return run_weather(base_url=base_url, timeout=timeout, override_volume=volume)
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
            alarm_volume=alarm_volume,
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
            alarm_volume=alarm_volume,
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
            alarm_volume=alarm_volume,
        )
    else:
        raise ValueError(f"不支持的模式: {mode}")
