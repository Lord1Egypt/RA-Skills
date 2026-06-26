---
name: when-clock-skill
description: >
  Control WHEN/WHEN Voice LAN clock devices. Supports voice time announcement, weather broadcast (WHEN Voice only),
  alarm CRUD, and countdown timer. Use --device-id to specify device.
version: 2.0.0
triggers:
  - "报时"
  - "现在几点"
  - "几点了"
  - "语音报时"
  - "播报时间"
  - "播报天气"
  - "语音播报天气"
  - "天气广播"
  - "查看闹钟"
  - "有哪些闹钟"
  - "闹钟列表"
  - "设置闹钟"
  - "加个闹钟"
  - "定个闹钟"
  - "明天叫我起床"
  - "每天早上叫我"
  - "修改闹钟"
  - "调整闹钟"
  - "删除闹钟"
  - "取消闹钟"
  - "多久后提醒我"
  - "N分钟后提醒"
  - "一小时后提醒"
  - "定时提醒"
  - "time announcement"
  - "what time is it"
  - "voice report"
  - "weather broadcast"
  - "set alarm"
  - "add alarm"
  - "delete alarm"
  - "cancel alarm"
  - "remind me in N minutes"
  - "timer reminder"
tools:
  - python
---

# when-clock-skill (OpenClaw Skill Description)

## 1. Skill Overview

- **Entry script**: `when-clock-skill.py`
- **Runtime**: Python 3.9+, standard library only, no pip required
- **Target devices**: WHEN / WHEN Voice clock (LAN HTTP, auto-detected)
- **Config file**: `config.json` in script directory (fill `devices` array with `id` and `clock_ip`)

## 2. Invocation Format

```
python when-clock-skill.py --mode <mode> --device-id <device_id> [options...]
```

> `--device-id` defaults to `default` (for backward compatibility with single-device config).

## 3. Mode Quick Reference

| Mode | Description | Required Args | Device Support |
|------|-------------|---------------|----------------|
| `chime` | Voice time announcement | — | WHEN Voice only |
| `weather` | Voice weather broadcast | — | WHEN Voice only |
| `get_alarm` | Query all alarms | — | Both |
| `set_alarm` | Add new alarm | `--alarm-time` | Both |
| `edit_alarm` | Modify alarm (partial update) | `--alarm-index` | Both |
| `delete_alarm` | Delete alarm | `--alarm-index` | Both |
| `set_timer` | Countdown timer (single alarm) | `--timer-offset` | Both |

## 4. Mode Details

### 4.1 chime — Voice Time Announcement (WHEN Voice only)

Announces current time. **WHEN devices do not support this mode.**

```bash
python when-clock-skill.py --mode chime --device-id device1
python when-clock-skill.py --mode chime --device-id device1 --volume 20
```

Optional: `--volume 1~30` (uses device current volume if not specified)

Output:
```json
{"ok": true, "mode": "chime", "action": "voice_announce_preview", "result": "success", "status": 0, "message": "succ"}
```

---

### 4.2 weather — Weather Broadcast (WHEN Voice only)

**WHEN devices do not support this mode.**

> **Note**: Weather broadcast currently only supports **China region**. More regions will be added in future updates.

```bash
python when-clock-skill.py --mode weather --device-id device1
python when-clock-skill.py --mode weather --device-id device1 --volume 20
```

Output:
```json
{"ok": true, "mode": "weather", "action": "voice_weather_preview", "result": "success", "status": 0, "message": "succ"}
```

---

### 4.3 get_alarm — Query Alarm List

```bash
python when-clock-skill.py --mode get_alarm --device-id device1
```

> WHEN device alarm entries do **not** include `volume` field.

WHEN Voice output example (with volume):
```json
{
  "ok": true,
  "mode": "get_alarm",
  "alarm_count": 2,
  "alarms": [
    {"index": 1, "mode": "Workday", "time": "07:30:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20},
    {"index": 2, "mode": "Weekly", "time": "09:00:00", "ring": "Weather(1x)", "ring_duration_level": "30S", "volume": 15, "active_days": ["Mon", "Wed"]}
  ]
}
```

> `alarms[].index` is the `--alarm-index` value needed by `edit_alarm` / `delete_alarm`.

---

### 4.4 set_alarm — Add New Alarm

```bash
# Once (default)
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30

# Workdays
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-mode workday --alarm-time 08:00

# Weekly on specific days
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-mode weekly --alarm-week 1,2,3,4,5 --alarm-time 08:10

# WHEN Voice - full params
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30 --alarm-ring 5 --alarm-delay 6 --alarm-volume 20

# WHEN - ring only 1-6
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30 --alarm-ring 3
```

Optional params (use `config.json alarm_defaults` if not specified):
- `--alarm-mode`: `once`/`weekly`/`workday`/`restday`/`off`, default `once`
- `--alarm-week`: required for `weekly`, e.g. `1,2,3,4,5` or `Mon,Wed,Fri`
- `--alarm-ring`: ring ID (WHEN Voice: 1~50, WHEN: 1~6 beep1-beep6)
- `--alarm-delay`: duration level (0-based, 0~11)
- `--alarm-volume`: volume 1~30 (WHEN Voice only)

> Maximum **10 alarms** per device.

Output:
```json
{"ok": true, "mode": "set_alarm", "action": "add_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "added_alarm": {"mode": "Once", "time": "07:30:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

---

### 4.5 edit_alarm — Modify Alarm

**Only specified fields are updated; other fields keep original values.**

```bash
# Change time only
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-time 07:45

# Change time and volume (WHEN Voice)
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 2 --alarm-time 08:30 --alarm-volume 25

# Change to workday mode
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-mode workday
```

`--alarm-index` is required (use `get_alarm` to check indices first).

Output:
```json
{"ok": true, "mode": "edit_alarm", "action": "update_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "updated_alarm": {"index": 1, "mode": "Once", "time": "07:45:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

---

### 4.6 delete_alarm — Delete Alarm

```bash
python when-clock-skill.py --mode delete_alarm --device-id device1 --alarm-index 2
```

`--alarm-index` is required.

Output:
```json
{"ok": true, "mode": "delete_alarm", "action": "remove_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 2, "removed_alarm": {"index": 2, "mode": "Once", "time": "09:00:00", "ring": "Weather(1x)", "ring_duration_level": "30S", "volume": 15, "active_days": []}}
```

---

### 4.7 set_timer — Countdown Timer

Takes current local time + offset, writes as a **single-shot alarm** to device.

```bash
# 5 minutes later (uses config default ring/volume)
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 5m

# 1 hour 30 minutes later
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 1h30m

# 90 seconds, custom ring and volume (WHEN Voice)
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 90s --alarm-ring 5 --alarm-volume 20
```

`--timer-offset` format: `5m`, `1h`, `1h30m`, `90s`, `1h30m20s`. Plain number treated as minutes.

Output:
```json
{"ok": true, "mode": "set_timer", "action": "add_timer", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "timer": {"offset": "5m", "offset_seconds": 300, "trigger_at": "14:35:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20}}
```

---

## 5. Ring Tone Reference

### WHEN Voice (50 tones, common)

| ID | Name | ID | Name |
|----|------|----|------|
| 1 | Weather(1x) | 2 | Weather(2x) |
| 3 | Weather(3x) | 4 | Beep-1 |
| 5 | Reveille | 6 | Rest Call |
| 43 | Morning | 44 | Evening |
| 49 | Chinese-style music-1 | 50 | Chinese-style music-2 |

### WHEN (6 tones)

| ID | Name |
|----|------|
| 1 | beep1 |
| 2 | beep2 |
| 3 | beep3 |
| 4 | beep4 |
| 5 | beep5 |
| 6 | beep6 |

> Full WHEN Voice list in `config.json` `alarm_defaults_note.ring_id_name`.

## 6. Important Conventions

- Alarm index (`--alarm-index`) is **1-based**, starting from 1
- Ring ID (`--alarm-ring`) is **1-based**, internally converted to device 0-based
- Volume range `1~30`, sent as `volume-1` (**WHEN Voice only**)
- WHEN device has **no volume parameter**, ring fixed to beep1-beep6
- Maximum **10 alarms** per device
- `config.json` `devices` array must have valid `id` and `clock_ip`, or script exits with code 2
- Check success: prefer `ok == true`, fallback to `status == 0`
- Errors to `stderr`, normal JSON to `stdout`

## 7. Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Device returned failure status |
| 2 | Argument / config / response format error |
| 3 | HTTP error |
| 4 | Network error |
