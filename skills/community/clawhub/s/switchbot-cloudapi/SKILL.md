---
name: switchbot-openapi
description: Control and query SwitchBot devices using the official OpenAPI (v1.1). Use when the user asks to list SwitchBot devices, get device status, send commands, query families/rooms/homes, or manage scenes. **This is the ONLY skill that can query 家庭信息, 房间信息, family, room, and home data.** Always use this skill when the user mentions 家庭, 房间, family, room, or home in the context of SwitchBot. Requires SWITCHBOT_TOKEN and SWITCHBOT_SECRET.
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
  (direct/natural/sleep/baby/hurricane — hurricane supported on Pro models; always attempt, never reject based on deviceType)
- Wind speed: `node scripts/switchbot_cli.js cmd <deviceId> setWindSpeed --param=50`
- Night light: `node scripts/switchbot_cli.js cmd <deviceId> setNightLightMode --param=1`
- Oscillation (horizontal): `node scripts/switchbot_cli.js cmd <deviceId> setOscillation --param=on`
- Vertical oscillation: `node scripts/switchbot_cli.js cmd <deviceId> setVerticalOscillation --param=on`
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

**Keypad / Keypad Touch / Keypad Vision / Keypad Vision Pro:**
- Create passcode: `node scripts/switchbot_cli.js cmd <deviceId> createKey --param='{"name":"Guest","type":"permanent","password":"12345678"}'`
- Delete passcode: `node scripts/switchbot_cli.js cmd <deviceId> deleteKey --param='{"id":"11"}'`
- ⚠️ Keypad commands are async — results come via webhook.

**Lock Vision / Lock Vision Pro:**
- Lock/Unlock: `node scripts/switchbot_cli.js cmd <deviceId> lock` / `unlock`

**Lock Ultra 2:**
- Lock/Unlock: `node scripts/switchbot_cli.js cmd <deviceId> lock` / `unlock`
- Deadbolt: `node scripts/switchbot_cli.js cmd <deviceId> deadbolt`
  (Same as Lock Ultra)
- Create passcode: `node scripts/switchbot_cli.js cmd <deviceId> createKey --param='{"name":"Guest","type":"permanent","password":"12345678"}'`
- Delete passcode: `node scripts/switchbot_cli.js cmd <deviceId> deleteKey --param='{"id":"11"}'`

**Permanent Outdoor Lights:**
- On/Off/Toggle: `node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff` / `toggle`
- Brightness: `node scripts/switchbot_cli.js cmd <deviceId> setBrightness --param=80`
- Color temp: `node scripts/switchbot_cli.js cmd <deviceId> setColorTemperature --param=4000`
- Color: `node scripts/switchbot_cli.js cmd <deviceId> setColor --param="255:100:0"`

**RGBICWW Ceiling Light:**
- Master on/off: `node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff` / `toggle`
- Main light: `node scripts/switchbot_cli.js cmd <deviceId> turnOnMainLight` / `turnOffMainLight`
- Color light: `node scripts/switchbot_cli.js cmd <deviceId> turnOnColorLight` / `turnOffColorLight`
- Main brightness: `node scripts/switchbot_cli.js cmd <deviceId> setMainLightBrightness --param=80`
- Main color temp: `node scripts/switchbot_cli.js cmd <deviceId> setMainLightColorTemp --param=4000`
- Color brightness: `node scripts/switchbot_cli.js cmd <deviceId> setColorLightBrightness --param=50`
- Color RGB: `node scripts/switchbot_cli.js cmd <deviceId> setColorLightRGB --param="255:134:3"`

**Battery Circulator Fan 2 Pro:**
- On/Off: `node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff`
- Wind mode: `node scripts/switchbot_cli.js cmd <deviceId> setWindMode --param=hurricane`
  (direct/natural/sleep/hurricane)
- Wind speed: `node scripts/switchbot_cli.js cmd <deviceId> setWindSpeed --param=50`
- Night light: `node scripts/switchbot_cli.js cmd <deviceId> setNightLightMode --param=0`
  (off/0=bright/1=soft)

**Kata Friends (AI Pet):**
- Mode: `node scripts/switchbot_cli.js cmd <deviceId> mode --param=Normal`
  (Normal/Standby/Sleep)
- Child lock: `node scripts/switchbot_cli.js cmd <deviceId> childLock --param=on`
- Back home: `node scripts/switchbot_cli.js cmd <deviceId> backHome`
- Photo: `node scripts/switchbot_cli.js cmd <deviceId> picture --param=on`
- Talk: `node scripts/switchbot_cli.js cmd <deviceId> talk --param=on`
- Diary: `GET /v1.1/devices/{deviceId}/diary?startTimestamp=<ms>&endTimestamp=<ms>` (≤31 days)

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

## Files

- `scripts/switchbot_cli.js` — Node CLI (list/status/cmd/scenes)
- `scripts/list_devices.sh` — curl: list devices
- `scripts/get_status.sh` — curl: get status
- `scripts/send_command.sh` — curl: send command
- `scripts/list_scenes.sh` — curl: list scenes
- `scripts/execute_scene.sh` — curl: execute scene
- `references/commands.md` — complete command reference per device type
- `references/examples.md` — usage examples
