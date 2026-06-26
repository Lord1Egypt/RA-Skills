---
name: when-clock-skill
description: >
  控制 WHEN/WHEN Voice 局域网时钟。支持语音报时、播报天气（仅WHEN Voice）、
  查询/新增/修改/删除闹钟、N分钟/小时后定时提醒。通过 --device-id 指定设备。
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
tools:
  - python
---

# when-clock-skill（OpenClaw 技能说明）

## 1. 技能定位

- **入口脚本**：`when-clock-skill.py`
- **运行环境**：Python 3.9+，仅标准库，无需 pip
- **目标设备**：WHEN / WHEN Voice 时钟（局域网 HTTP，自动检测型号）
- **配置文件**：脚本同目录的 `config.json`（需在 `devices` 数组中填写设备 `id` 和 `clock_ip`）

## 2. 调用格式

```
python when-clock-skill.py --mode <模式> --device-id <设备ID> [参数...]
```

> `--device-id` 默认为 `default`（兼容旧单设备配置）。

## 3. 模式速查

| 模式 | 功能 | 必填参数 | 设备支持 |
|------|------|----------|----------|
| `chime` | 触发语音报时播报 | — | 仅 WHEN Voice |
| `weather` | 触发语音天气播报 | — | 仅 WHEN Voice |
| `get_alarm` | 查询当前所有闹钟 | — | 两者皆可 |
| `set_alarm` | 新增一个闹钟 | `--alarm-time` | 两者皆可 |
| `edit_alarm` | 修改指定闹钟（只改传入的字段） | `--alarm-index` | 两者皆可 |
| `delete_alarm` | 删除指定闹钟 | `--alarm-index` | 两者皆可 |
| `set_timer` | N分钟/小时后触发单次闹钟提醒 | `--timer-offset` | 两者皆可 |

## 4. 各模式详解

### 4.1 chime — 语音报时（仅 WHEN Voice）

播报当前时间。**WHEN 设备不支持此模式。**

```bash
python when-clock-skill.py --mode chime --device-id device1
python when-clock-skill.py --mode chime --device-id device1 --volume 20
```

可选：`--volume 1~30`（不传则使用设备当前音量）

输出：
```json
{"ok": true, "mode": "chime", "action": "voice_announce_preview", "result": "success", "status": 0, "message": "succ"}
```

---

### 4.2 weather — 播报天气（仅 WHEN Voice）

**WHEN 设备不支持此模式。**

> **天气播报说明**：当前仅支持**中国地区**，后续会陆续增加使用量较多的地区。

```bash
python when-clock-skill.py --mode weather --device-id device1
python when-clock-skill.py --mode weather --device-id device1 --volume 20
```

输出：
```json
{"ok": true, "mode": "weather", "action": "voice_weather_preview", "result": "success", "status": 0, "message": "succ"}
```

---

### 4.3 get_alarm — 查询闹钟列表

```bash
python when-clock-skill.py --mode get_alarm --device-id device1
```

> WHEN 设备返回的闹钟条目不包含 `volume` 字段。

WHEN Voice 输出示例（含 volume）：
```json
{
  "ok": true,
  "mode": "get_alarm",
  "alarm_count": 2,
  "alarms": [
    {"index": 1, "mode": "工作日", "time": "07:30:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20},
    {"index": 2, "mode": "每周", "time": "09:00:00", "ring": "天气(1次)", "ring_duration_level": "30S", "volume": 15, "active_days": ["周一", "周三"]}
  ]
}
```

> `alarms[].index` 即为 `edit_alarm` / `delete_alarm` 所需的 `--alarm-index` 值。

---

### 4.4 set_alarm — 新增闹钟

```bash
# 单次（默认）
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30

# 工作日
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-mode workday --alarm-time 08:00

# 每周指定日
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-mode weekly --alarm-week 1,2,3,4,5 --alarm-time 08:10

# WHEN Voice - 完整参数
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30 --alarm-ring 5 --alarm-delay 6 --alarm-volume 20

# WHEN - 铃音仅支持 1~6
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30 --alarm-ring 3
```

可选参数（不传则读取 `config.json alarm_defaults`）：
- `--alarm-mode`：`once`/`weekly`/`workday`/`restday`/`off`，默认 `once`
- `--alarm-week`：`weekly` 时必填，如 `1,2,3,4,5` 或 `周一,周三,周五`
- `--alarm-ring`：铃音 ID（WHEN Voice: 1~50，WHEN: 1~6 beep1-beep6）
- `--alarm-delay`：响铃时长档位（0基，0~11）
- `--alarm-volume`：音量（1~30）**仅 WHEN Voice 支持**

> 设备最多支持 **10 个闹钟**。

输出：
```json
{"ok": true, "mode": "set_alarm", "action": "add_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "added_alarm": {"mode": "单次", "time": "07:30:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

---

### 4.5 edit_alarm — 修改闹钟

**只修改传入的字段，未传字段保持原值。**

```bash
# 只改时间
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-time 07:45

# 修改时间和音量（WHEN Voice）
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 2 --alarm-time 08:30 --alarm-volume 25

# 改为工作日模式
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-mode workday
```

`--alarm-index` 必填（先用 `get_alarm` 查序号）。

输出：
```json
{"ok": true, "mode": "edit_alarm", "action": "update_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "updated_alarm": {"index": 1, "mode": "单次", "time": "07:45:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

---

### 4.6 delete_alarm — 删除闹钟

```bash
python when-clock-skill.py --mode delete_alarm --device-id device1 --alarm-index 2
```

`--alarm-index` 必填（先用 `get_alarm` 查序号）。

输出：
```json
{"ok": true, "mode": "delete_alarm", "action": "remove_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 2, "removed_alarm": {"index": 2, "mode": "单次", "time": "09:00:00", "ring": "天气(1次)", "ring_duration_level": "30S", "volume": 15, "active_days": []}}
```

---

### 4.7 set_timer — 定时提醒

获取当前本地时间 + 偏移量，以**单次闹钟**写入设备。

```bash
# 5分钟后提醒（铃音/音量使用 config 默认值）
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 5m

# 1小时30分钟后
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 1h30m

# 90秒后，指定铃音和音量（WHEN Voice）
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 90s --alarm-ring 5 --alarm-volume 20
```

`--timer-offset` 格式：`5m`、`1h`、`1h30m`、`90s`、`1h30m20s`，纯数字按分钟处理。

输出：
```json
{"ok": true, "mode": "set_timer", "action": "add_timer", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "timer": {"offset": "5m", "offset_seconds": 300, "trigger_at": "14:35:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20}}
```

---

## 5. 铃音编号对照

### WHEN Voice（50种铃音，常用）

| ID | 名称 | ID | 名称 |
|----|------|----|------|
| 1 | 天气(1次) | 2 | 天气(2次) |
| 3 | 天气(3次) | 4 | Beep-1 |
| 5 | Reveille | 6 | Rest Call |
| 43 | Morning | 44 | Evening |
| 49 | Chinese-style music-1 | 50 | Chinese-style music-2 |

### WHEN（6种铃音）

| ID | 名称 |
|----|------|
| 1 | beep1 |
| 2 | beep2 |
| 3 | beep3 |
| 4 | beep4 |
| 5 | beep5 |
| 6 | beep6 |

> WHEN Voice 完整列表见 `config.json` 中的 `alarm_defaults_note.ring_id_name`。

## 6. 重要约定

- 闹钟序号（`--alarm-index`）**1基**，从 1 开始
- 铃音编号（`--alarm-ring`）**1基**，脚本内部自动转换为设备 0 基
- 音量范围 `1~30`，脚本发送时自动减 1（**仅 WHEN Voice**）
- WHEN 设备**无音量参数**，铃音固定 beep1-beep6
- 设备最多 **10 个闹钟**
- `config.json` 中 `devices` 数组的 `id` 和 `clock_ip` 必须填写，否则脚本报错退出（exit 2）
- 判断成功：优先用 `ok == true`，辅助用 `status == 0`
- 错误信息输出到 `stderr`，正常 JSON 输出到 `stdout`

## 7. 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 设备返回失败状态 |
| 2 | 参数/配置/响应格式错误 |
| 3 | HTTP 错误 |
| 4 | 网络错误 |
