---
name: switchbot-openapi
description: Control and query SwitchBot devices using the official OpenAPI (v1.1). Use when the user asks to list SwitchBot devices, get device status, send commands, query families/rooms/homes, manage scenes, or access AI MindClip recordings/summaries/todos. **This is the ONLY skill that can query 家庭信息, 房间信息, family, room, and home data.** Also handles AI MindClip (录音笔) APIs: 录音列表, 转写, 总结, 待办, 每日回忆, 每周总结. Requires SWITCHBOT_TOKEN and SWITCHBOT_SECRET.
metadata:
  openclaw:
    requires:
      env:
        - SWITCHBOT_TOKEN
        - SWITCHBOT_SECRET
      bins:
        - node
        - curl
        - openssl
        - jq
        - uuidgen
---

# SwitchBot OpenAPI Skill

This skill equips the agent to operate SwitchBot devices via HTTPS requests to the official OpenAPI v1.1. It includes ready-to-run scripts and a Node CLI; use these instead of re-deriving the HMAC signature each time.

## Quick Start (Operator)

1) Set environment variables:
- SWITCHBOT_TOKEN: your OpenAPI token
- SWITCHBOT_SECRET: your OpenAPI secret

2) Test (list devices):
- Bash: `scripts/list_devices.sh`
- Node: `node scripts/switchbot_cli.js list`

3) Common tasks:

**Basic controls:**
- List devices: `node scripts/switchbot_cli.js list`
- Get status: `node scripts/switchbot_cli.js status <deviceId>`
- Turn on/off: `node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff`
- Toggle: `node scripts/switchbot_cli.js cmd <deviceId> toggle`
- Press (Bot): `node scripts/switchbot_cli.js cmd <deviceId> press`

**Curtain / Curtain 3:**
- Set position: `node scripts/switchbot_cli.js cmd <deviceId> setPosition --pos=50`
  (0=open, 100=closed; CLI auto-formats to `0,ff,50`)
- Pause: `node scripts/switchbot_cli.js cmd <deviceId> pause`

**Lock / Lock Pro / Lock Ultra / Lock Lite:**
- Lock/Unlock: `node scripts/switchbot_cli.js cmd <deviceId> lock` / `unlock`
- Deadbolt: `node scripts/switchbot_cli.js cmd <deviceId> deadbolt`

**Lights (Color Bulb / Strip Light / Floor Lamp / Strip Light 3 / RGBICWW etc.):**
- Set color: `node scripts/switchbot_cli.js cmd <deviceId> setColor --param="255:100:0"`
- Set brightness: `node scripts/switchbot_cli.js cmd <deviceId> setBrightness --param=80`
- Set color temp: `node scripts/switchbot_cli.js cmd <deviceId> setColorTemperature --param=4000`

**Fans (Battery Circulator Fan / Circulator Fan / Standing Circulator Fan):**
- Wind mode: `node scripts/switchbot_cli.js cmd <deviceId> setWindMode --param=natural`
- Wind speed: `node scripts/switchbot_cli.js cmd <deviceId> setWindSpeed --param=50`
- Night light: `node scripts/switchbot_cli.js cmd <deviceId> setNightLightMode --param=1`
- Auto-off timer: `node scripts/switchbot_cli.js cmd <deviceId> closeDelay --param=3600`

**Robot Vacuum S1/S1 Plus/K10+/K10+ Pro:**
- Start: `node scripts/switchbot_cli.js cmd <deviceId> start`
- Stop: `node scripts/switchbot_cli.js cmd <deviceId> stop`
- Dock: `node scripts/switchbot_cli.js cmd <deviceId> dock`
- Suction: `node scripts/switchbot_cli.js cmd <deviceId> PowLevel --param=2`

**Robot Vacuum K10+ Pro Combo / K20+ Pro / S10 / S20 / K11+:**
- Start clean: `node scripts/switchbot_cli.js cmd <deviceId> startClean --param='{"action":"sweep_mop","param":{"fanLevel":2,"waterLevel":1,"times":1}}'`
- Pause/Dock: `node scripts/switchbot_cli.js cmd <deviceId> pause` / `dock`
- Volume: `node scripts/switchbot_cli.js cmd <deviceId> setVolume --param=50`
- Self clean (S10/S20): `node scripts/switchbot_cli.js cmd <deviceId> selfClean --param=1`

**Weather Station:**
- Set custom quote: `node scripts/switchbot_cli.js cmd <deviceId> customQuote --param="大海啊，你好多的水啊！"`
  (Max 100 characters; displayed on the AI Recommendations page)
- Remove custom quote: `node scripts/switchbot_cli.js cmd <deviceId> cancelCustom --param=default`
- Set custom page text: `node scripts/switchbot_cli.js cmd <deviceId> customPage --param="自定义页面文本"`
  (Max 100 characters)

**Blind Tilt:**
- Set position: `node scripts/switchbot_cli.js cmd <deviceId> setPosition --param="up;60"`
- Fully open: `node scripts/switchbot_cli.js cmd <deviceId> fullyOpen`
- Close: `node scripts/switchbot_cli.js cmd <deviceId> closeUp` / `closeDown`

**Roller Shade:**
- Set position: `node scripts/switchbot_cli.js cmd <deviceId> setPosition --param=50`

**Humidifier (original):**
- Set mode: `node scripts/switchbot_cli.js cmd <deviceId> setMode --param=auto`

**Evaporative Humidifier / Auto-refill:**
- Set mode: `node scripts/switchbot_cli.js cmd <deviceId> setMode --param='{"mode":7,"targetHumidify":60}'`
- Child lock: `node scripts/switchbot_cli.js cmd <deviceId> setChildLock --param=true`

**Air Purifier (VOC/PM2.5/Table):**
- Set mode: `node scripts/switchbot_cli.js cmd <deviceId> setMode --param='{"mode":2,"fanGear":2}'`
- Child lock: `node scripts/switchbot_cli.js cmd <deviceId> setChildLock --param=1`

**Smart Radiator Thermostat:**
- Set mode: `node scripts/switchbot_cli.js cmd <deviceId> setMode --param=1`
- Set temp: `node scripts/switchbot_cli.js cmd <deviceId> setManualModeTemperature --param=22`

**Relay Switch 1PM / 1 / 2PM:**
- Toggle: `node scripts/switchbot_cli.js cmd <deviceId> toggle`
- Set mode: `node scripts/switchbot_cli.js cmd <deviceId> setMode --param=0`
- 2PM channel: `node scripts/switchbot_cli.js cmd <deviceId> turnOn --param="1"` (channel 1 or 2)

**Garage Door Opener:**
- Open/Close: `node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff`

**Video Doorbell:**
- Motion detection: `node scripts/switchbot_cli.js cmd <deviceId> enableMotionDetection` / `disableMotionDetection`

**Candle Warmer Lamp:**
- Brightness: `node scripts/switchbot_cli.js cmd <deviceId> setBrightness --param=50`

**AI Art Frame:**
- Next/Previous: `node scripts/switchbot_cli.js cmd <deviceId> next` / `previous`
- Upload image (URL): `node scripts/switchbot_cli.js cmd <deviceId> uploadImage --param='{"imageUrl":"https://example.com/photo.jpg"}'`
- Upload image (Base64): `node scripts/switchbot_cli.js cmd <deviceId> uploadImage --param='{"imageBase64":"<base64_string>"}'`
- ⚠️ `imageUrl` and `imageBase64` are mutually exclusive. Max 10 images; statusCode 402 = limit reached.

**AI MindClip (录音笔):**
- Get status: `node scripts/switchbot_cli.js status <deviceId>`
- List recordings: `node scripts/switchbot_cli.js mindclip recordings <deviceId>`
- Get recording detail: `node scripts/switchbot_cli.js mindclip recording <recordingId>`
- Get summary (transcription + AI): `node scripts/switchbot_cli.js mindclip summary <recordingId>`
- List todos: `node scripts/switchbot_cli.js mindclip todos`
- Daily memory: `node scripts/switchbot_cli.js mindclip daily <date>`  (e.g. 2026-06-05)
- Weekly summary: `node scripts/switchbot_cli.js mindclip weekly <week>`  (e.g. 2026-W23)
- Urgent todos: `node scripts/switchbot_cli.js mindclip urgent <date>`

**Keypad / Keypad Touch / Keypad Vision / Keypad Vision Pro:**
- Create passcode: `node scripts/switchbot_cli.js cmd <deviceId> createKey --param='{"name":"Guest","type":"permanent","password":"12345678"}'`
- Delete passcode: `node scripts/switchbot_cli.js cmd <deviceId> deleteKey --param='{"id":"11"}'`
- ⚠️ Keypad commands are async — results come via webhook.

**IR Remote - Air Conditioner:**
- Set all: `node scripts/switchbot_cli.js cmd <deviceId> setAll --param="26,2,1,on"`
  (format: temperature, mode, fan speed, power state)
  - mode: 0/1=auto, 2=cool, 3=dry, 4=fan, 5=heat
  - fan: 1=auto, 2=low, 3=medium, 4=high
  - power: on/off

**IR Remote - TV:**
- Channel: `node scripts/switchbot_cli.js cmd <deviceId> SetChannel --param=5`
- Volume: `node scripts/switchbot_cli.js cmd <deviceId> volumeAdd` / `volumeSub`

**IR Remote - Others (DIY):**
- Custom button: `node scripts/switchbot_cli.js cmd <deviceId> <buttonName> --commandType=customize`

**Scenes (fallback):**
- List scenes: `node scripts/switchbot_cli.js scenes`
- Execute scene: `node scripts/switchbot_cli.js scene <sceneId>`

## API Reference

Base URL: `https://api.switch-bot.com`
Path prefix: `/v1.1`
Daily limit: 10,000 API calls

Headers (all required):
- Authorization: `<SWITCHBOT_TOKEN>`
- sign: HMAC-SHA256(`token + t + nonce`, secret), Base64-encoded
- t: 13-digit millisecond timestamp
- nonce: random UUID

Key endpoints:
- `GET /v1.1/devices` — list all devices
- `GET /v1.1/devices/{deviceId}/status` — device status
- `POST /v1.1/devices/{deviceId}/commands` — send command
- `GET /v1.1/scenes` — list scenes
- `POST /v1.1/scenes/{sceneId}/execute` — execute scene
- `GET /v1.1/mindclip/recordings?deviceID=xxx&pageNum=1&pageSize=20` — list recordings
- `GET /v1.1/mindclip/recordings/{recordingId}` — single recording detail
- `GET /v1.1/mindclip/summaries/{recordingId}` — transcription + AI summary
- `GET /v1.1/mindclip/todos?completedNum=1&pageNum=1&pageSize=20` — todo list
- `GET /v1.1/mindclip/assistant/daily?date=YYYY-MM-DD` — daily memory
- `GET /v1.1/mindclip/assistant/weekly?week=YYYY-Wxx` — weekly summary
- `GET /v1.1/mindclip/assistant/urgent-todos?date=YYYY-MM-DD` — urgent todos

Command body format:
```json
{
  "command": "<commandName>",
  "parameter": "<string|object>",
  "commandType": "command"
}
```
For IR "Others" (DIY) devices, use `"commandType": "customize"`.

## Querying Families & Rooms

The OpenAPI does not have a dedicated families/rooms endpoint. Instead, extract this info from the device list response (`GET /v1.1/devices`).

Each device in `deviceList` includes:
- `familyName` — the family/home it belongs to
- `roomID` — room identifier (`"defaultRoom"` means no specific room assigned)
- `roomName` — room display name (`null` if default room)

**When the user asks about families, homes, or rooms:**

1. Call `node scripts/switchbot_cli.js list` to get the full device list
2. Group devices by `familyName` to get all families
3. Within each family, group by `roomName` (treat `null`/`"defaultRoom"` as "未分配房间")
4. Present the family → room → device hierarchy

Example output format:
```
🏠 Home
  └─ 未分配房间: 设备A, 设备B, ...
  └─ 客厅: 设备C, ...

🏠 测试
  └─ 未分配房间: 设备D, ...
```

**Note:** IR remote devices (`infraredRemoteList`) only have `hubDeviceId`, no `familyName`/`roomName`. To determine their family, match their `hubDeviceId` to a device in `deviceList` and use that device's family.

## Agent Guidelines

- Always use the provided CLI scripts — they handle HMAC signatures automatically.
- The CLI runs preflight checks for BLE devices (Bot, Lock, Curtain, Blind Tilt) — requires Hub + Cloud Services enabled.
- For IR Air Conditioner, only `setAll` is supported (not separate setMode/setTemp).
- For Keypad commands (createKey/deleteKey), results are async via webhook.
- If a command returns statusCode 160, the device may not support that command — use Scenes as fallback.
- Never log tokens/secrets. Ask user to set them as environment variables.

## AI MindClip (录音笔)

deviceType: `AI MindClip`

### 设备状态

`GET /v1.1/devices/{deviceId}/status` returns:

```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "deviceId": "AABBCCDDEEFF",
        "deviceType": "AI MindClip",
        "battery": 87,
        "chargingStatus": 1,
        "recordingStatus": 0,
        "uploadStatus": 1,
        "hasUntransferredFiles": true
    }
}
```

Fields:
- `battery` — 0-100
- `chargingStatus` — 0=未充电, 1=充电中
- `recordingStatus` — 0=未录音, 1=录音中
- `uploadStatus` — 0=未上传, 1=上传中
- `hasUntransferredFiles` — 是否有未传输文件

### 设备指令

不支持（no OpenAPI commands）

### 获取录音列表

```
GET /v1.1/mindclip/recordings?deviceID={deviceId}&pageNum=1&pageSize=20
```

Response:
```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "total": 1,
        "pageNum": 1,
        "pageSize": 20,
        "pages": 1,
        "list": [
            {
                "id": "5f3a1c2e9b7d",
                "displayName": "Team sync",
                "recordingLen": 1820,
                "fileSize": 2931456,
                "deviceID": "AABBCCDDEEFF",
                "transcribeStatus": 2,
                "createdTime": 1716000000000,
                "folderID": 3,
                "emoji": "📁",
                "isSystem": false
            }
        ]
    }
}
```

Fields:
- `id` — recording unique ID
- `displayName` — user-facing name
- `recordingLen` — duration in seconds
- `fileSize` — bytes
- `transcribeStatus` — 0=未转写, 1=转写中, 2=转写成功, 3=转写失败, 4=超时, 5=语音转写失败
- `createdTime` — 13-digit timestamp
- `folderID` — folder grouping
- `emoji` — folder icon
- `isSystem` — system folder flag

### 获取单条录音详情

```
GET /v1.1/mindclip/recordings/{recordingId}
```

Response: same structure as list item (single object in `body`).

### 获取总结内容

```
GET /v1.1/mindclip/summaries/{recordingId}
```

Response:
```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "fileID": "5f3a1c2e9b7d",
        "transcribeStatus": 2,
        "transcribeResult": "Alice: Let's review the release plan...\nBob: ...",
        "aiSummaryResult": "Key decisions: ship v2 next week; assign QA to Alice.",
        "aiTemplateResult": "## Meeting Notes\n- ...",
        "aiAtmoResult": "Focused and collaborative",
        "aiTodoList": [
            {
                "title": "Send meeting notes to team",
                "reminderTime": 1716100000000,
                "isCompleted": false,
                "createdTime": 1716000000000,
                "fileID": "5f3a1c2e9b7d",
                "deviceID": "AABBCCDDEEFF",
                "category": 1
            }
        ],
        "speakers": [
            {
                "speaker": "spk_1",
                "speakerName": "Alice",
                "lightColor": "#FFB300",
                "darkColor": "#FFD54F",
                "speakerConfidence": 0.92
            }
        ]
    }
}
```

### 获取待办列表

```
GET /v1.1/mindclip/todos?completedNum=1&pageNum=1&pageSize=20
```

Query params:
- `completedNum` — number of completed items to include
- `pageNum` / `pageSize` — pagination

Response:
```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "total": 1,
        "pageNum": 1,
        "pageSize": 20,
        "pages": 1,
        "list": [
            {
                "title": "Send meeting notes to team",
                "reminderTime": 1716100000000,
                "isCompleted": false,
                "createdTime": 1716000000000,
                "fileID": "5f3a1c2e9b7d",
                "deviceID": "AABBCCDDEEFF",
                "category": 1
            }
        ]
    }
}
```

### 获取每日回忆

```
GET /v1.1/mindclip/assistant/daily?date=2026-06-05
```

Response:
```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "list": [
            {
                "summaryDate": "2026-06-05",
                "summaryContent": "Today you had 3 meetings and created 2 todos...",
                "status": 1,
                "timezone": "Asia/Shanghai",
                "locations": [
                    {
                        "timestamp": 1717540000,
                        "latitude": 31.23,
                        "longitude": 121.47,
                        "placeName": "Shanghai Office",
                        "fileID": "5f3a1c2e9b7d"
                    }
                ]
            }
        ]
    }
}
```

### 获取每周总结

```
GET /v1.1/mindclip/assistant/weekly?week=2026-W23
```

Response:
```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "summaryWeek": "2026-W23",
        "summaryContent": "This week you recorded 12 sessions across 5 days...",
        "status": 1,
        "timezone": "Asia/Shanghai"
    }
}
```

### 获取紧急待办

```
GET /v1.1/mindclip/assistant/urgent-todos?date=2026-06-04
```

Response:
```json
{
    "statusCode": 100,
    "message": "success",
    "body": {
        "summaryDate": "2026-06-04",
        "todos": [
            {
                "title": "Send meeting notes to team",
                "reminderTime": 1717100000000,
                "rank": 1,
                "fileID": "5f3a1c2e9b7d",
                "isCompleted": false,
                "category": 1
            }
        ]
    }
}
```

### WebHook 事件

AI MindClip 支持的 webhook 事件：

1. **充电上云完成事件**
```json
{
    "eventType": "changeReport",
    "eventVersion": "1",
    "context": {
        "deviceType": "AI MindClip",
        "deviceMac": "AIPINNOTE-DEVICE-001",
        "timeOfSample": 1749542100000,
        "chargeUploadCompleted": {
            "fileID": "20260610143022001",
            "fileName": "2026-06-10 14:30",
            "status": 1,
            "timestamp": 1749542100000
        }
    }
}
```

2. **转写事件**
```json
{
    "eventType": "changeReport",
    "eventVersion": "1",
    "context": {
        "deviceType": "AI MindClip",
        "deviceMac": "AIPINNOTE-DEVICE-001",
        "timeOfSample": 1749542400000,
        "transcription": {
            "fileID": "20260610143022001",
            "status": 1,
            "timestamp": 1749542400000
        }
    }
}
```
transcription.status: 0=未转写, 1=转写中, 2=转写成功, 3=转写失败, 4=超时, 5=语音转写失败

3. **每日回忆生成事件**
```json
{
    "eventType": "changeReport",
    "eventVersion": "1",
    "context": {
        "deviceType": "AI MindClip",
        "deviceMac": "AIPINNOTE-DEVICE-001",
        "timeOfSample": 1749556800000,
        "dailySummary": 1749556800
    }
}
```

4. **每周总结生成事件**
```json
{
    "eventType": "changeReport",
    "eventVersion": "1",
    "context": {
        "deviceType": "AI MindClip",
        "deviceMac": "AIPINNOTE-DEVICE-001",
        "timeOfSample": 1749816000000,
        "weeklySummary": 1749816000
    }
}
```

## Files

- `scripts/switchbot_cli.js` — Node CLI (list/status/cmd/scenes)
- `scripts/list_devices.sh` — curl: list devices
- `scripts/get_status.sh` — curl: get status
- `scripts/send_command.sh` — curl: send command
- `scripts/list_scenes.sh` — curl: list scenes
- `scripts/execute_scene.sh` — curl: execute scene
- `references/commands.md` — complete command reference per device type
- `references/examples.md` — usage examples
