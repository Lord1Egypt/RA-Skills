---
name: ecovacs-robot-control
description: Control Ecovacs/DEEBOT robot vacuums via the Ecovacs IoT API. Use when the user wants to control a robot vacuum, check battery, start/stop/pause cleaning, return to dock, check clean status, set suction/water level, manage schedules, check consumables, or control auto-empty station. Covers all mainstream Ecovacs protocols including clean_V2, charge, getBattery, getCleanInfo_V2, getStats, getSpeed/setSpeed, getWaterInfo/setWaterInfo, getWorkMode/setWorkMode, getLifeSpan, getAutoEmpty/setAutoEmpty, getCachedMapInfo, getMapSet, getSched_V2/setSched_V2.
---

# Ecovacs Robot Control

## Auth Flow

Three-step flow: **Login → Device List → Send Command**

Full API details in `references/api.md`. Core script in `scripts/ecovacs.py`.

### Session Management

Session (token + userid + resource) is stored in `~/.ecovacs_session.json` after login.
Always `load_session()` before calling device APIs. Re-login if token expired (errno 3000).

### Critical Rule

`toType` = device's **`class`** field from device list (e.g. `o0lqjm`).  
**NOT** `"device"` or `"USER"` — this is the #1 cause of `errno:3003 permission denied`.

---

## Using the Script

```bash
# First time login
python3 scripts/ecovacs.py login <phone> <md5_or_plain_password>

# List all devices (shows did, status, name)
python3 scripts/ecovacs.py devices

# Check battery (use did or nick)
python3 scripts/ecovacs.py battery <did>

# Check clean status
python3 scripts/ecovacs.py status <did>

# Start full-house auto clean
python3 scripts/ecovacs.py clean <did> start

# Pause / resume / stop
python3 scripts/ecovacs.py clean <did> pause
python3 scripts/ecovacs.py clean <did> resume
python3 scripts/ecovacs.py clean <did> stop

# Return to dock
python3 scripts/ecovacs.py charge <did>

# Send any arbitrary command
python3 scripts/ecovacs.py cmd <did> getLifeSpan '{"type":"brush,sideBrush,heap"}'
python3 scripts/ecovacs.py cmd <did> setSpeed '{"speed":1}'
python3 scripts/ecovacs.py cmd <did> getWorkMode '{}'
```

---

## Direct API Calls

When using tools directly (not script), follow this pattern:

```python
# 1. Login
session = login(phone, md5(password))

# 2. Get devices
devices = get_devices(session)
device = next(d for d in devices if "T50" in d["deviceName"])

# 3. Send command
result = send_cmd(session, device, "clean_V2", {
    "act": "start",
    "content": {"type": "auto", "count": 1}
})
```

See `references/api.md` for full protocol reference:
- **Auth & device discovery** — login, resource generation, device list fields
- **All command payloads** — clean_V2, charge, battery, stats, speed, water, workmode, lifespan, autoEmpty, maps, schedules
- **State/event codes** — error codes, evt codes, clean states

---

## Common Protocols Quick Reference

| Goal | cmdName | key body.data fields |
|------|---------|----------------------|
| 开始全屋清扫 | `clean_V2` | `{act:"start", content:{type:"auto",count:1}}` |
| 区域清扫 | `clean_V2` | `{act:"start", content:{type:"spotArea",value:"mssid1,mssid2"}}` |
| 暂停/继续/停止 | `clean_V2` | `{act:"pause/resume/stop"}` |
| 回充 | `charge` | `{act:"go"}` |
| 查电量 | `getBattery` | `{}` |
| 查清扫状态 | `getCleanInfo_V2` | `{}` |
| 查本次面积时长 | `getStats` | `{}` |
| 查/设吸力 | `getSpeed`/`setSpeed` | `{speed:0}` (1000静音/0标准/1强劲/2超强) |
| 查/设水量 | `getWaterInfo`/`setWaterInfo` | `{amount:2}` (1低/2中/3高/4超高) |
| 查/设扫拖模式 | `getWorkMode`/`setWorkMode` | `{mode:0}` (0边扫边拖/1仅扫/2仅拖/3先扫后拖) |
| 查耗材 | `getLifeSpan` | `{type:"brush,sideBrush,heap,filter"}` |
| 手动集尘 | `setAutoEmpty` | `{act:"start"}` |
| 查地图列表 | `getCachedMapInfo` | `{}` |
| 查房间区域 | `getMapSet` | `{mid:"<map_id>",type:"ar"}` |
| 查预约 | `getSched_V2` | `{type:1}` |

---

## Error Handling

| errno | meaning |
|-------|---------|
| 3000 | Token expired → re-login |
| 3003 | Permission denied → check `toType` = device `class` |
| 30000 | Device response timeout → device offline |
| 0 (body.code) | Success |

---

## Accounts (China domestic)
- Login URL: `https://api-app.dc-cn.cn.ecouser.net/api/users/user.do`
- org: `ECOCN`, country: `CN`
- Password: MD5 hex of plaintext
