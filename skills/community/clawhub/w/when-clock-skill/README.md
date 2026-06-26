# WHEN Clock Skill

[English](README.md) | [中文](README_zh.md)

Control your **WHEN** and **WHEN Voice** LAN clock devices via CLI. Multi-device support, pure Python standard library, no pip required.

## Supported Devices

| Device | Product Page | Description |
|--------|-------------|-------------|
| WHEN | [iottimer.com/products/when/](https://iottimer.com/products/when/) | Basic LAN clock |
| WHEN Voice | [iottimer.com/products/when_voice/](https://iottimer.com/products/when_voice/) | Voice-enabled LAN clock |

![WHEN Voice Clock](docs/images/when_voice_clock.png)

## Quick Start

1. Edit `config.json` with your device list:

```json
{
  "devices": [
    {
      "id": "device1",
      "name": "Living Room Clock",
      "clock_ip": "192.168.1.88",
      "clock_port": 80,
      "timeout": 5.0,
      "alarm_defaults": {
        "ring_id": 5,
        "ring_duration_id": 7,
        "volume": 20
      }
    }
  ]
}
```

2. Run:

```bash
python when-clock-skill.py --mode get_alarm --device-id device1
```

## Device Feature Comparison

| Feature | WHEN | WHEN Voice |
|---------|:----:|:----------:|
| Voice chime | ❌ | ✅ |
| Weather broadcast | ❌ | ✅ |
| Alarm volume | ❌ | ✅ |
| Ring tones | beep1-6 (1-6) | 50 tones |

## File Structure

```
when-clock-skill/
├── when-clock-skill.py     # Main entry (device discovery + dispatch)
├── when_common.py         # Common utilities
├── when.py                # WHEN device handler
├── when_voice.py          # WHEN Voice device handler
├── config.json            # Configuration (multi-device)
├── _meta.json             # OpenClaw metadata
├── SKILL.md               # OpenClaw skill description
├── README.md              # This file (English)
├── README_zh.md           # 中文版
└── docs/
    ├── WHEN_VOICE_WEB_API_PROTOCOL.md
    ├── WHEN_WEB_API_PROTOCOL.md
    └── OPENCLAW_SKILL_PACKING_CHECKLIST.md
```

## Supported Modes

| Mode | Description | Required Args | WHEN | WHEN Voice |
|------|-------------|---------------|:----:|:----------:|
| `chime` | Voice time announcement | — | ❌ | ✅ |
| `weather` | Voice weather broadcast | — | ❌ | ✅ |
| `get_alarm` | Query all alarms | — | ✅ | ✅ |
| `set_alarm` | Add new alarm | `--alarm-time` | ✅ | ✅ |
| `edit_alarm` | Modify alarm (partial update) | `--alarm-index` | ✅ | ✅ |
| `delete_alarm` | Delete alarm | `--alarm-index` | ✅ | ✅ |
| `set_timer` | Timer reminder (countdown) | `--timer-offset` | ✅ | ✅ |

## Usage Examples

### Time / Weather (WHEN Voice only)

> **Weather broadcast Note**: Currently only supports **China region**. More regions will be added in future updates.

```bash
python when-clock-skill.py --mode chime --device-id device1
python when-clock-skill.py --mode chime --device-id device1 --volume 20
python when-clock-skill.py --mode weather --device-id device1
```

### Query Alarms

```bash
python when-clock-skill.py --mode get_alarm --device-id device1
```

### Add Alarm

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

### Edit Alarm

Only specified fields are updated.

```bash
# Change time only
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-time 07:45

# Change time and volume (WHEN Voice)
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 2 --alarm-time 08:30 --alarm-volume 25

# Change to workday mode
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-mode workday
```

### Delete Alarm

```bash
python when-clock-skill.py --mode delete_alarm --device-id device1 --alarm-index 2
```

### Timer Reminder

```bash
# 5 minutes later
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 5m

# 1 hour 30 minutes later
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 1h30m

# 90 seconds, custom ring & volume (WHEN Voice)
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 90s --alarm-ring 5 --alarm-volume 20
```

`--timer-offset` format: `5m`, `1h`, `1h30m`, `90s`, `1h30m20s`. Plain number treated as minutes.

## Argument Reference

| Argument | Modes | Required | Description |
|----------|-------|----------|-------------|
| `--device-id` | all | — | Device ID (default: `default`) |
| `--mode` | all | ✅ | Mode name |
| `--volume` | chime, weather | — | Volume 1~30 (WHEN Voice only) |
| `--alarm-time` | set_alarm ✅, edit_alarm — | — | Time HH:MM or HH:MM:SS |
| `--alarm-mode` | set_alarm, edit_alarm | — | once/weekly/workday/restday/off |
| `--alarm-week` | set_alarm, edit_alarm | required for weekly | Days: `1,2,3,4,5` or `Mon,Wed,Fri` |
| `--alarm-ring` | set_alarm, edit_alarm, set_timer | — | Ring ID (WHEN: 1-6, WHEN Voice: 1-50) |
| `--alarm-delay` | set_alarm, edit_alarm, set_timer | — | Duration level (0-based, 0~11) |
| `--alarm-volume` | set_alarm, edit_alarm, set_timer | — | Volume 1~30 (WHEN Voice only) |
| `--alarm-index` | delete_alarm, edit_alarm | ✅ | Alarm index (1-based) |
| `--timer-offset` | set_timer | ✅ | Offset e.g. `5m`, `1h30m` |
| `--timeout` | all | — | Override HTTP timeout |
| `--config` | all | — | Config file path (default: `config.json`) |

## Output Format

All modes output JSON to stdout, errors to stderr.

**WHEN vs WHEN Voice**: WHEN device alarm output does **not** include `volume` field.

### chime / weather

```json
{"ok": true, "mode": "chime", "action": "voice_announce_preview", "result": "success", "status": 0, "message": "succ"}
```

### get_alarm (WHEN Voice - with volume)

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

### get_alarm (WHEN - no volume)

```json
{
  "ok": true,
  "mode": "get_alarm",
  "alarm_count": 1,
  "alarms": [
    {"index": 1, "mode": "Workday", "time": "07:30:00", "ring": "beep3", "ring_duration_level": "2min", "active_days": ["Mon", "Tue", "Wed", "Thu", "Fri"]}
  ]
}
```

### set_alarm

```json
{"ok": true, "mode": "set_alarm", "action": "add_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "added_alarm": {"mode": "Once", "time": "07:30:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

### edit_alarm

```json
{"ok": true, "mode": "edit_alarm", "action": "update_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "updated_alarm": {"index": 1, "mode": "Once", "time": "07:45:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

### delete_alarm

```json
{"ok": true, "mode": "delete_alarm", "action": "remove_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 2, "removed_alarm": {"index": 2, "mode": "Once", "time": "09:00:00", "ring": "Weather(1x)", "ring_duration_level": "30S", "volume": 15, "active_days": []}}
```

### set_timer

```json
{"ok": true, "mode": "set_timer", "action": "add_timer", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "timer": {"offset": "5m", "offset_seconds": 300, "trigger_at": "14:35:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20}}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (device returned status=0) |
| 1 | Device returned failure status |
| 2 | Argument / config / response format error |
| 3 | HTTP error |
| 4 | Network error |

## Ring Tone Reference

### WHEN Voice (50 tones)

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

## Alarm Duration Reference

`1=10S, 2=20S, 3=30S, 4=40S, 5=50S, 6=1min, 7=2min, 8=3min, 9=5min, 10=10min, 11=15min, 12=20min`

## Protocol Reference

### chime (type=74)

`GET /get?type=9` reads `announcer`, `volume`, `is12H`, then `POST /set`:

```json
{"type": 74, "mode": 0, "ring": <announcer>, "vol": <volume-1>, "sw": 1, "is12H": <is12H>}
```

### weather (type=73)

`GET /get?type=9` reads `volume`, then `POST /set`:

```json
{"type": 73, "mode": 1, "ring": 3, "sw": 1, "vol": <volume-1>}
```

### alarm (type=7)

`GET /get?type=7` reads current alarm list, modifies, then `POST /set` full list:

```json
{"type": 7, "alarmNum": <count>, "alarmInfo": [...]}
```

## Configuration File (config.json)

### devices Array Element

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | ✅ | Unique device ID (used by `--device-id`) |
| `name` | string | — | Device name (for reference) |
| `clock_ip` | string | ✅ | Device IP address |
| `clock_port` | int | — | HTTP port, default 80 |
| `timeout` | float | — | HTTP timeout in seconds, default 5.0 |
| `alarm_defaults.ring_id` | int | — | Default ring (WHEN: 1-6, WHEN Voice: 1-50) |
| `alarm_defaults.ring_duration_id` | int | — | Default duration (1-12) |
| `alarm_defaults.volume` | int | — | Default volume (1-30, WHEN Voice only) |

## Important Notes

- Alarm index (`--alarm-index`) is **1-based**, starting from 1
- Ring ID (`--alarm-ring`) is **1-based**, internally converted to 0-based for device
- Volume range `1~30`, sent as `volume-1` (WHEN Voice only)
- Maximum **10 alarms** per device
- `config.json` `devices` array must have valid `id` and `clock_ip`
- Check success: prefer `ok == true`, fallback to `status == 0`
- Errors go to `stderr`, normal JSON output to `stdout`

---

[English](README.md) | [中文](README_zh.md)
