# WHEN Clock Skill

[English](README.md) | [中文](README_zh.md)

支持 **WHEN** 和 **WHEN Voice** 两款局域网时钟设备的控制技能。多设备配置，仅使用 Python 标准库，无需 pip 安装。

## 支持的设备

| 设备 | 产品页面 | 说明 |
|------|---------|------|
| WHEN | [iottimer.com/products/when/](https://iottimer.com/products/when/) | 基础版时钟 |
| WHEN Voice | [iottimer.com/products/when_voice/](https://iottimer.com/products/when_voice/) | 语音版时钟 |

![WHEN Voice Clock](docs/images/when_voice_clock.png)

## 文件结构

```
when-clock-skill/
├── when-clock-skill.py                        # 主入口（设备发现+分发）
├── when_common.py                             # 公共模块（工具函数+常量）
├── when.py                                    # WHEN 设备处理模块
├── when_voice.py                              # WHEN Voice 设备处理模块
├── config.json                                # 配置文件（多设备支持）
├── _meta.json                                 # OpenClaw 技能元数据
├── SKILL.md                                   # OpenClaw 技能说明
├── README.md                                  # 英文版
├── README_zh.md                               # 本文档
└── docs/
    ├── images/                                # 设备图片
    ├── WHEN_VOICE_WEB_API_PROTOCOL.md
    ├── WHEN_WEB_API_PROTOCOL.md
    └── OPENCLAW_SKILL_PACKING_CHECKLIST.md
```

## 设备支持差异

| 功能 | WHEN | WHEN Voice |
|------|------|------------|
| 语音报时 (chime) | 不支持 | 支持 |
| 天气播报 (weather) | 不支持 | 支持 |
| 闹钟音量 | 无 | 有 (vol) |
| 铃音 | beep1-beep6 (1-6) | 50种铃音 |

## 快速开始

1. 编辑 `config.json`，配置设备列表：

```json
{
  "devices": [
    {
      "id": "device1",
      "name": "客厅时钟",
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

2. 运行：

```bash
python when-clock-skill.py --mode get_alarm --device-id device1
```

## 支持模式

| 模式 | 功能 | 必填参数 | WHEN | WHEN Voice |
|------|------|----------|------|------------|
| `chime` | 语音报时 | — | ❌ | ✅ |
| `weather` | 天气播报 | — | ❌ | ✅ |
| `get_alarm` | 查询闹钟 | — | ✅ | ✅ |
| `set_alarm` | 新增闹钟 | `--alarm-time` | ✅ | ✅ |
| `edit_alarm` | 修改闹钟 | `--alarm-index` | ✅ | ✅ |
| `delete_alarm` | 删除闹钟 | `--alarm-index` | ✅ | ✅ |
| `set_timer` | 定时提醒 | `--timer-offset` | ✅ | ✅ |

## 配置文件字段 (config.json)

### devices 数组元素

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 设备唯一ID（命令行 --device-id 使用）|
| `name` | string | — | 设备名称（仅作备注）|
| `clock_ip` | string | ✅ | 设备 IP |
| `clock_port` | int | — | HTTP 端口，默认 80 |
| `timeout` | float | — | 超时秒数，默认 5.0 |
| `alarm_defaults.ring_id` | int | — | 默认铃音（WHEN: 1-6, WHEN Voice: 1-50）|
| `alarm_defaults.ring_duration_id` | int | — | 默认响铃时长（1-12）|
| `alarm_defaults.volume` | int | — | 默认音量（1-30，仅 WHEN Voice）|

### 响铃时长对照

`1=10S, 2=20S, 3=30S, 4=40S, 5=50S, 6=1min, 7=2min, 8=3min, 9=5min, 10=10min, 11=15min, 12=20min`

## 使用示例

### 报时 / 天气播报（仅 WHEN Voice）

> **天气播报说明**：当前仅支持**中国地区**，后续会陆续增加使用量较多的地区。

```bash
python when-clock-skill.py --mode chime --device-id device1
python when-clock-skill.py --mode chime --device-id device1 --volume 20
python when-clock-skill.py --mode weather --device-id device1
```

### 查询闹钟

```bash
python when-clock-skill.py --mode get_alarm --device-id device1
```

### 新增闹钟

```bash
# 单次（默认模式）
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30

# WHEN Voice - 完整参数
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30 --alarm-ring 5 --alarm-delay 6 --alarm-volume 20

# WHEN - 铃音仅支持 1-6
python when-clock-skill.py --mode set_alarm --device-id device1 --alarm-time 07:30 --alarm-ring 3
```

### 修改闹钟

只修改传入的字段，未传字段保持原值。

```bash
# 只改时间
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-time 07:45

# 修改时间和音量（WHEN Voice）
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 2 --alarm-time 08:30 --alarm-volume 25

# 改为工作日模式
python when-clock-skill.py --mode edit_alarm --device-id device1 --alarm-index 1 --alarm-mode workday
```

### 删除闹钟

```bash
python when-clock-skill.py --mode delete_alarm --device-id device1 --alarm-index 2
```

### 定时提醒

```bash
# 5分钟后提醒（铃音/音量使用 config 默认值）
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 5m

# 1小时30分钟后
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 1h30m

# 90秒后，指定铃音和音量（WHEN Voice）
python when-clock-skill.py --mode set_timer --device-id device1 --timer-offset 90s --alarm-ring 5 --alarm-volume 20
```

`--timer-offset` 支持：`5m`、`1h`、`1h30m`、`90s`、`1h30m20s`，纯数字按分钟处理。

## 参数参考

| 参数 | 适用模式 | 必填 | 说明 |
|------|----------|------|------|
| `--device-id` | 全部 | — | 设备ID（默认 default）|
| `--mode` | 全部 | ✓ | 模式名 |
| `--volume` | chime, weather | — | 覆盖音量 1~30（仅 WHEN Voice）|
| `--alarm-time` | set_alarm ✓, edit_alarm — | — | 时间 HH:MM 或 HH:MM:SS |
| `--alarm-mode` | set_alarm, edit_alarm | — | once/weekly/workday/restday/off |
| `--alarm-week` | set_alarm, edit_alarm | weekly 时 ✓ | 星期计划，如 `1,2,3,4,5` |
| `--alarm-ring` | set_alarm, edit_alarm, set_timer | — | 铃音编号（WHEN: 1-6, WHEN Voice: 1-50）|
| `--alarm-delay` | set_alarm, edit_alarm, set_timer | — | 响铃时长档位（0基，0~11）|
| `--alarm-volume` | set_alarm, edit_alarm, set_timer | — | 音量 1~30（仅 WHEN Voice）|
| `--alarm-index` | delete_alarm, edit_alarm | ✓ | 目标闹钟序号（1基）|
| `--timer-offset` | set_timer | ✓ | 延迟时间，如 `5m`、`1h30m` |
| `--timeout` | 全部 | — | 覆盖超时秒数 |
| `--config` | 全部 | — | 配置文件路径（默认 `config.json`）|

## 输出格式

所有模式均输出 JSON 到 stdout，错误信息输出到 stderr。

> **WHEN vs WHEN Voice 输出差异**：WHEN 设备的闹钟输出不包含 `volume` 字段。

### chime / weather

```json
{"ok": true, "mode": "chime", "action": "voice_announce_preview", "result": "success", "status": 0, "message": "succ"}
```

### get_alarm（WHEN Voice）

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

### get_alarm（WHEN，无 volume）

```json
{
  "ok": true,
  "mode": "get_alarm",
  "alarm_count": 1,
  "alarms": [
    {"index": 1, "mode": "工作日", "time": "07:30:00", "ring": "beep3", "ring_duration_level": "2min", "active_days": ["周一", "周二", "周三", "周四", "周五"]}
  ]
}
```

### set_alarm

```json
{"ok": true, "mode": "set_alarm", "action": "add_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "added_alarm": {"mode": "单次", "time": "07:30:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

### edit_alarm

```json
{"ok": true, "mode": "edit_alarm", "action": "update_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "updated_alarm": {"index": 1, "mode": "单次", "time": "07:45:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20, "active_days": []}}
```

### delete_alarm

```json
{"ok": true, "mode": "delete_alarm", "action": "remove_alarm", "result": "success", "status": 0, "message": "succ", "alarm_count": 2, "removed_alarm": {"index": 2, "mode": "单次", "time": "09:00:00", "ring": "天气(1次)", "ring_duration_level": "30S", "volume": 15, "active_days": []}}
```

### set_timer

```json
{"ok": true, "mode": "set_timer", "action": "add_timer", "result": "success", "status": 0, "message": "succ", "alarm_count": 3, "timer": {"offset": "5m", "offset_seconds": 300, "trigger_at": "14:35:00", "ring": "Reveille", "ring_duration_level": "2min", "volume": 20}}
```

## 返回码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功（设备返回 status=0）|
| 1 | 设备返回失败状态 |
| 2 | 参数/配置/响应格式错误 |
| 3 | HTTP 错误 |
| 4 | 网络错误 |

## 协议说明

### chime（type=74）

`GET /get?type=9` 读取 `announcer`、`volume`、`is12H`，然后 `POST /set`：

```json
{"type": 74, "mode": 0, "ring": <announcer>, "vol": <volume-1>, "sw": 1, "is12H": <is12H>}
```

### weather（type=73）

`GET /get?type=9` 读取 `volume`，然后 `POST /set`：

```json
{"type": 73, "mode": 1, "ring": 3, "sw": 1, "vol": <volume-1>}
```

### 闹钟（type=7）

`GET /get?type=7` 读取当前闹钟列表，修改后 `POST /set` 全量写回：

```json
{"type": 7, "alarmNum": <count>, "alarmInfo": [...]}
```



