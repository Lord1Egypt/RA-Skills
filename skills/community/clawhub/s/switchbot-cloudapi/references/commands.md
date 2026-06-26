# SwitchBot Commands Reference (Complete - OpenAPI v1.1)

General schema (POST /v1.1/devices/{deviceId}/commands):

```json
{
  "commandType": "command",
  "command": "<string>",
  "parameter": "<string|object> or default"
}
```

---

## Physical Device Commands

### Bot
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | set to ON state |
| turnOff | default | set to OFF state |
| press | default | trigger press |

### Curtain
| Command | Parameter | Description |
|---------|-----------|-------------|
| setPosition | `index,mode,position` e.g. `0,ff,80` | mode: 0 (Performance), 1 (Silent), ff (default); position: 0~100 (0=open, 100=closed) |
| turnOn | default | equivalent to position 0 |
| turnOff | default | equivalent to position 100 |
| pause | default | pause movement |

### Curtain 3
| Command | Parameter | Description |
|---------|-----------|-------------|
| setPosition | `index,mode,position` e.g. `0,ff,80` | same as Curtain |
| turnOn | default | equivalent to position 0 |
| turnOff | default | equivalent to position 100 |
| pause | default | pause movement |

### Lock
| Command | Parameter | Description |
|---------|-----------|-------------|
| lock | default | rotate to locked position |
| unlock | default | rotate to unlocked position |
| deadbolt | default | disengage deadbolt or latch |

### Lock Pro
| Command | Parameter | Description |
|---------|-----------|-------------|
| lock | default | rotate to locked position |
| unlock | default | rotate to unlocked position |
| deadbolt | default | disengage deadbolt or latch |

### Lock Ultra
| Command | Parameter | Description |
|---------|-----------|-------------|
| lock | default | rotate to locked position |
| unlock | default | rotate to unlocked position |
| deadbolt | default | disengage deadbolt or latch |

### Lock Lite
| Command | Parameter | Description |
|---------|-----------|-------------|
| lock | default | rotate to locked position |
| unlock | default | rotate to unlocked position |

### Humidifier (original)
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| setMode | `auto` or `101` or `102` or `103` or `{0~100}` | auto; 101=34%; 102=67%; 103=100% |

### Evaporative Humidifier / Evaporative Humidifier (Auto-refill)
deviceType: `Humidifier2`

| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| setMode | `{"mode": int, "targetHumidify": int}` | mode: 1=level4, 2=level3, 3=level2, 4=level1, 5=humidity, 6=sleep, 7=auto, 8=drying; targetHumidify: 0~100 |
| setChildLock | `true` or `false` | enable/disable child lock |

### Air Purifier VOC / Air Purifier Table VOC
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| setMode | `{"mode": int, "fanGear": int}` | mode: 1=normal/fan, 2=auto, 3=sleep, 4=pet; fanGear: 1~3 (only when mode=1) |
| setChildLock | `0` or `1` | 1=enable, 0=disable |

### Air Purifier PM2.5 / Air Purifier Table PM2.5
Same commands as Air Purifier VOC.

### Plug
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |

### Plug Mini (US) / Plug Mini (JP) / Plug Mini (EU)
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |

### Color Bulb
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{1-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` e.g. `"255:100:0"` | set RGB color |
| setColorTemperature | `{2700-6500}` | set color temperature |

### Strip Light
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{1-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` | set RGB color |

### Strip Light 3 (LED Strip Light 3)
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{0-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` | set RGB color |
| setColorTemperature | `{2700-6500}` | set color temperature |

### Floor Lamp (RGBWW Floor Lamp)
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{0-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` | set RGB color |
| setColorTemperature | `{2700-6500}` | set color temperature |

### RGBICWW Strip Light
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{0-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` | set RGB color |
| setColorTemperature | `{2700-6500}` | set color temperature |

### RGBICWW Floor Lamp
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{0-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` | set RGB color |
| setColorTemperature | `{2700-6500}` | set color temperature |

### RGBIC Neon Wire Rope Light / RGBIC Neon Rope Light
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{0-100}` | set brightness |
| setColor | `"{R}:{G}:{B}"` | set RGB color |

### Ceiling Light / Ceiling Light Pro
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{1-100}` | set brightness |
| setColorTemperature | `{2700-6500}` | set color temperature |

### Candle Warmer Lamp
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setBrightness | `{0-100}` | set brightness |

### Weather Station
| Command | Parameter | Description |
|---------|-----------|-------------|
| customQuote | `"<text>"` (max 100 chars) | Set a personalized quote displayed on the AI Recommendations page |
| cancelCustom | default | Remove custom quote and restore default display |
| customPage | `"<text>"` (max 100 chars) | Set custom page text |

### AI Art Frame
| Command | Parameter | Description |
|---------|-----------|-------------|
| next | default | switch to next image |
| previous | default | switch to previous image |
| uploadImage | `{"imageUrl":"<url>"}` or `{"imageBase64":"<base64>"}` | upload an image to the Art Frame. `imageUrl` and `imageBase64` are mutually exclusive (pick one). Base64 supports optional `data:image/...;base64,` prefix. statusCode 402 = image limit reached (max 10), delete via App first. |

### Robot Vacuum Cleaner S1 / S1 Plus
| Command | Parameter | Description |
|---------|-----------|-------------|
| start | default | start vacuuming |
| stop | default | stop vacuuming |
| dock | default | return to charging dock |
| PowLevel | `{0-3}` | suction: 0=Quiet, 1=Standard, 2=Strong, 3=MAX |

### Mini Robot Vacuum K10+ / K10+ Pro
| Command | Parameter | Description |
|---------|-----------|-------------|
| start | default | start vacuuming |
| stop | default | stop vacuuming |
| dock | default | return to charging dock |
| PowLevel | `{0-3}` | suction: 0=Quiet, 1=Standard, 2=Strong, 3=MAX |

### K10+ Pro Combo
| Command | Parameter | Description |
|---------|-----------|-------------|
| startClean | `{"action": "sweep"\|"mop", "param": {"fanLevel": 1-4, "times": 1-2639999}}` | start cleaning |
| pause | default | pause cleaning |
| dock | default | return to dock |
| setVolume | `{0-100}` | set volume |
| changeParam | `{"fanLevel": 1-4, "times": 1-2639999}` | change parameters |

### K20+ Pro (Multitasking Household Robot)
| Command | Parameter | Description |
|---------|-----------|-------------|
| startClean | `{"action": "sweep"\|"mop", "param": {"fanLevel": 1-4, "times": 1-2639999}}` | start cleaning |
| pause | default | pause cleaning |
| dock | default | return to dock |
| setVolume | `{0-100}` | set volume |
| changeParam | `{"fanLevel": 1-4, "waterLevel": 1-2, "times": 1-2639999}` | change parameters |

### Floor Cleaning Robot S10
| Command | Parameter | Description |
|---------|-----------|-------------|
| startClean | `{"action": "sweep"\|"sweep_mop", "param": {"fanLevel": 1-4, "waterLevel": 1-2, "times": int}}` | start cleaning |
| addWaterForHumi | default | refill Evaporative Humidifier (Auto-refill) |
| pause | default | pause |
| dock | default | return to station |
| setVolume | `{0-100}` | set volume |
| selfClean | `1` or `2` or `3` | 1=wash mop, 2=dry, 3=terminate |
| changeParam | `{"fanLevel": 1-4, "waterLevel": 1-2, "times": int}` | change parameters |

### Floor Cleaning Robot S20
Same commands as S10.

### Robot Vacuum K11+
| Command | Parameter | Description |
|---------|-----------|-------------|
| startClean | `{"action": "sweep"\|"mop", "param": {"fanLevel": 1-4, "times": int}}` | start cleaning |
| pause | default | pause |
| dock | default | return to station |
| setVolume | `{0-100}` | set volume |
| changeParam | `{"fanLevel": 1-4, "waterLevel": 1-2, "times": int}` | change parameters |

### Blind Tilt
| Command | Parameter | Description |
|---------|-----------|-------------|
| setPosition | `direction;position` e.g. `up;60` | direction: up/down; position: 0~100 (0=closed, 100=open, must be multiple of 2) |
| fullyOpen | default | set to open (up;100 or down;100) |
| closeUp | default | close upward (up;0) |
| closeDown | default | close downward (down;0) |

### Roller Shade
| Command | Parameter | Description |
|---------|-----------|-------------|
| setPosition | `{0-100}` | 0=open, 100=closed |

### Battery Circulator Fan / Circulator Fan / Standing Circulator Fan
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| setNightLightMode | `off`, `1`, or `2` | off; 1=bright; 2=dim |
| setWindMode | `direct`, `natural`, `sleep`, `baby`, or `hurricane` | fan mode (hurricane supported on Pro models) |
| setWindSpeed | `{1-100}` | fan speed |
| closeDelay | `{1-36000}` | auto-off timer (seconds) |

**Note:** All Circulator Fan variants (including Pro) share deviceType `Circulator Fan` in the API. Always attempt the requested wind mode — do NOT reject `hurricane` based on deviceType alone.

### Smart Radiator Thermostat
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| setMode | `{0-5}` | 0=schedule, 1=manual, 2=power off, 3=energy saving, 4=comfort, 5=quick heating |
| setManualModeTemperature | `{4-35}` | set temperature (°C) |

### Relay Switch 1PM / Relay Switch 1
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |
| toggle | default | toggle state |
| setMode | `{0-3}` | 0=toggle, 1=edge switch, 2=detached switch, 3=momentary switch |

### Relay Switch 2PM
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | `"1"` or `"2"` | ON (channel 1 or 2) |
| turnOff | `"1"` or `"2"` | OFF (channel 1 or 2) |
| toggle | `"1"` or `"2"` | toggle (channel 1 or 2) |
| setMode | `channel;mode` e.g. `1;0` | channel: 1 or 2; mode: 0=toggle, 1=edge, 2=detached, 3=momentary |
| setPosition | `{0-100}` | roller blind: 0=open, 100=closed |

### Garage Door Opener
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | ON |
| turnOff | default | OFF |

### Video Doorbell
| Command | Parameter | Description |
|---------|-----------|-------------|
| enableMotionDetection | default | enable motion detection |
| disableMotionDetection | default | disable motion detection |

### Keypad / Keypad Touch / Keypad Vision / Keypad Vision Pro
⚠️ Commands are ASYNC — results come via webhook, not in the HTTP response.

| Command | Parameter | Description |
|---------|-----------|-------------|
| createKey | `{"name": str, "type": str, "password": str, "startTime": long, "endTime": long}` | create a passcode |
| deleteKey | `{"id": str}` | delete a passcode |

**createKey parameter details:**
- `name`: unique name (no duplicates per device)
- `type`: `permanent` \| `timeLimit` \| `disposable` \| `urgent`
- `password`: 6-12 digit passcode in plain text
- `startTime`: 10-digit unix timestamp (required for timeLimit & disposable)
- `endTime`: 10-digit unix timestamp (required for timeLimit & disposable)

### Lock Ultra 2
deviceType in API: `Smart Lock Ultra 2`

| Command | Parameter | Description |
|---------|-----------|-------------|
| lock | default | lock the door |
| unlock | default | unlock the door |
| deadbolt | default | toggle deadbolt |

**Notes:** Same capabilities as Lock Ultra. Status includes `lockState` (locked/unlocked/locking/unlocking/jammed/latchBoltLocked/halfLocked), `doorState` (open/close), `calibrate`, `battery`.

### Lock Vision / Lock Vision Pro
| Command | Parameter | Description |
|---------|-----------|-------------|
| lock | default | lock the door |
| unlock | default | unlock the door |
| createKey | `{"name": str, "type": str, "password": str, "startTime": long, "endTime": long}` | create a passcode |
| deleteKey | `{"id": str}` | delete a passcode |

**Notes:** Same keypad createKey/deleteKey parameter format. deviceType in API: `Lock Vision` / `Lock Vision Pro`. Status includes `lockState`, `doorState`, `calibrate`, `onlineStatus`. Webhook deviceType: `W1141000` (Vision) / `W1141001` (Vision Pro).

### Permanent Outdoor Lights
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | turn on |
| turnOff | default | turn off |
| toggle | default | toggle on/off |
| setBrightness | `0-100` | set brightness |
| setColorTemperature | `2700-6500` | set color temperature |
| setColor | `"R:G:B"` (e.g. `"255:100:0"`) | set RGB color |

### RGBICWW Ceiling Light
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | master power on (turns on all lights — do NOT send turnOnMainLight/turnOnColorLight separately after this) |
| turnOff | default | master power off (turns off all lights — do NOT send turnOffMainLight/turnOffColorLight separately after this) |
| toggle | default | toggle master power |
| turnOnMainLight | default | turn on main (white) light only (use when you want to control main light independently, not with turnOn) |
| turnOffMainLight | default | turn off main (white) light only |
| turnOnColorLight | default | turn on color (RGB) light only (use when you want to control color light independently, not with turnOn) |
| turnOffColorLight | default | turn off color (RGB) light only |
| setMainLightBrightness | `1-100` | set main light brightness |
| setMainLightColorTemp | `2700-6500` | set main light color temperature |
| setColorLightBrightness | `1-100` | set color light brightness |
| setColorLightRGB | `"R:G:B"` (e.g. `"255:134:3"`) | set color light RGB |

**Status fields:** `power` (on/off/partial), `mainLightPower`, `mainLightBrightness`, `mainLightColorTemp`, `colorLightPower`, `colorLightBrightness`, `colorLightRGB`. Webhook deviceType: `W1162000`.

### Battery Circulator Fan 2 Pro
deviceType in API: `Circulator Fan` (same as original Circulator Fan)

| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | turn on |
| turnOff | default | turn off |
| setNightLightMode | `"off"` \| `"0"` \| `"1"` | night light: off / bright / soft |
| setWindMode | `"direct"` \| `"natural"` \| `"sleep"` \| `"hurricane"` | wind mode |
| setWindSpeed | `1-100` | fan speed |

**Differences from original Circulator Fan:** Wind modes include `hurricane` (no `baby`). Night light param: `off`/`0`(bright)/`1`(soft) vs old `off`/`1`/`2`. No `closeDelay` or `battery`. Status adds `chargingStatus` (charging/uncharged).

### Kata Friends (AI Pet)
| Command | Parameter | Description |
|---------|-----------|-------------|
| mode | `"Normal"` \| `"Standby"` \| `"Sleep"` | set operating mode |
| childLock | `"on"` \| `"off"` | toggle child lock |
| backHome | default | recall to home base |
| picture | `"on"` \| `"off"` | toggle photo taking |
| talk | `"on"` \| `"off"` | toggle conversation mode |

**Status fields:** `battery`, `onlineStatus`, `mode` (Normal/Standby/Sleep), `status` (Strolling/Welcoming Home/Wake-up Call/Sleeping/Playing/Returning), `childLock`, `hospitalized` (0=normal, 1=repair, 2=maintenance, 3=cleaning).

**Diary API:** `GET /v1.1/devices/{deviceId}/diary?startTimestamp=<ms>&endTimestamp=<ms>` — returns event logs (`diary`), AI text diary (`diaryAI`), and AI comic diary (`comicDiaryAI`). Time window ≤ 31 days.

---

## Virtual Infrared Remote Device Commands

### All IR devices (except Others)
| Command | Parameter | Description |
|---------|-----------|-------------|
| turnOn | default | turn on |
| turnOff | default | turn off |

### Air Conditioner
| Command | Parameter | Description |
|---------|-----------|-------------|
| setAll | `{temp},{mode},{fanSpeed},{powerState}` e.g. `26,1,3,on` | temp in °C; mode: 0/1=auto, 2=cool, 3=dry, 4=fan, 5=heat; fan: 1=auto, 2=low, 3=medium, 4=high; power: on/off |

### TV / IPTV/Streamer / Set Top Box
| Command | Parameter | Description |
|---------|-----------|-------------|
| SetChannel | `{channel number}` | switch channel |
| volumeAdd | default | volume up |
| volumeSub | default | volume down |
| channelAdd | default | next channel |
| channelSub | default | previous channel |

### DVD / Speaker
| Command | Parameter | Description |
|---------|-----------|-------------|
| setMute | default | mute/unmute |
| FastForward | default | fast forward |
| Rewind | default | rewind |
| Next | default | next track |
| Previous | default | previous track |
| Pause | default | pause |
| Play | default | play/resume |
| Stop | default | stop |

### Speaker (additional)
| Command | Parameter | Description |
|---------|-----------|-------------|
| volumeAdd | default | volume up |
| volumeSub | default | volume down |

### Fan (IR)
| Command | Parameter | Description |
|---------|-----------|-------------|
| swing | default | swing |
| timer | default | set timer |
| lowSpeed | default | low speed |
| middleSpeed | default | medium speed |
| highSpeed | default | high speed |

### Light (IR)
| Command | Parameter | Description |
|---------|-----------|-------------|
| brightnessUp | default | brightness up |
| brightnessDown | default | brightness down |

### Others (DIY)
| commandType | Command | Parameter | Description |
|-------------|---------|-----------|-------------|
| `customize` | `{button name}` | default | user-defined buttons must use commandType=customize |

---

## Notes
- Commands and parameters are case-sensitive.
- For IR "Others" devices, `commandType` must be `customize` (not `command`).
- Daily API limit: 10,000 calls.
- BLE devices (Bot, Lock, Curtain, Blind Tilt) require a Hub and Cloud Services enabled.
- Keypad commands are async; configure a webhook for results.
