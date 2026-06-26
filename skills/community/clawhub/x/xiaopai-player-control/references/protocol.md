# XiaoPai Player TCP/IP Protocol Reference

## Overview

The XiaoPai (小湃) media player exposes two network services for external control:

- **HTTP Server** on port **9050** — accepts commands and playback requests
- **TCP Server** on port **9051** — pushes real-time playback state to connected clients

Both services are provided by the `PlayerSupportApp` Android system service, which starts automatically on device boot.

## HTTP Server (Port 9050)

Base URL: `http://{PLAYER_IP}:9050`

All responses are `application/json; charset=utf-8` with HTTP 200 status.

### GET /xiaopai/sendkey

Send a remote-control key command.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| keycode   | string | Yes      | 3-character uppercase command code |

**Response:**
```json
{"code":0,"msg":"success"}
```

**Error (unknown keycode):**
```json
{"code":1,"msg":"unknown keycode"}
```

### GET /xiaopai/play

Play a video by file path/URL or by name search.

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| videopath | string | No*      | Video file path or URL (URL-encoded) |
| videoname | string | No*      | Video name for library search (URL-encoded) |

*At least one of `videopath` or `videoname` must be provided. If both are present, `videoname` takes priority.

**Response:**
```json
{"code":0,"msg":"success"}
```

**Error:**
```json
{"code":1,"msg":"play failed"}
```

## TCP Server (Port 9051)

Plain TCP, line-delimited JSON.

### Connection Flow

1. Client connects via TCP to port 9051
2. Server immediately sends current state as a JSON line
3. Connection stays open
4. Whenever playback state changes, server pushes updated JSON to all clients
5. Connection closes when client disconnects

### State JSON Format

```json
{
  "code": 0,
  "msg": "success",
  "deviceName": "Model Name",
  "mac": "AA:BB:CC:DD:EE:FF",
  "ipAddress": "192.168.1.100",
  "playStatus": 1,
  "playType": 1
}
```

### Field Definitions

| Field       | Type    | Values |
|-------------|---------|--------|
| code        | int     | `0` = success |
| msg         | string  | `"success"` |
| deviceName  | string  | Android Build.MODEL |
| mac         | string  | MAC address (XX:XX:XX:XX:XX:XX) |
| ipAddress   | string  | IPv4 address |
| playStatus  | int     | `-1` = Stopped, `1` = Playing, `2` = Paused |
| playType    | int     | `1` = Video, `2` = Music |

## Complete Keycode Reference

### Power
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| POW  | Power toggle | KEYCODE_POWER |
| OFF  | Power off | KEYCODE_POWER |

### Number Keys
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| NU0  | Number 0 | KEYCODE_0 |
| NU1  | Number 1 | KEYCODE_1 |
| NU2  | Number 2 | KEYCODE_2 |
| NU3  | Number 3 | KEYCODE_3 |
| NU4  | Number 4 | KEYCODE_4 |
| NU5  | Number 5 | KEYCODE_5 |
| NU6  | Number 6 | KEYCODE_6 |
| NU7  | Number 7 | KEYCODE_7 |
| NU8  | Number 8 | KEYCODE_8 |
| NU9  | Number 9 | KEYCODE_9 |
| DOT  | Dot (.) | KEYCODE_NUMPAD_DOT |

### Navigation
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| NUP  | Up | KEYCODE_DPAD_UP |
| NDN  | Down | KEYCODE_DPAD_DOWN |
| NLT  | Left | KEYCODE_DPAD_LEFT |
| NRT  | Right | KEYCODE_DPAD_RIGHT |
| SEL  | OK / Confirm | KEYCODE_DPAD_CENTER |

### Menu
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| OSD  | Menu | KEYCODE_MENU |
| RET  | Back / Return | KEYCODE_BACK |
| HOM  | Home | KEYCODE_HOME |
| SET  | Settings | Launches Settings Activity |
| MNU  | Pop Menu | (reserved) |
| TOP  | Top Menu | KEYCODE_MEDIA_TOP_MENU |

### Volume
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| VUP  | Volume Up | KEYCODE_VOLUME_UP |
| VDN  | Volume Down | KEYCODE_VOLUME_DOWN |
| MUT  | Mute | KEYCODE_VOLUME_MUTE |

### Playback Control
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| PLA  | Play/Pause toggle | KEYCODE_MEDIA_PLAY_PAUSE |
| PAU  | Pause | KEYCODE_MEDIA_PAUSE |
| PLU  | Play | KEYCODE_MEDIA_PLAY |
| STP  | Stop | KEYCODE_MEDIA_STOP |
| FWD  | Fast Forward | KEYCODE_MEDIA_FAST_FORWARD |
| REV  | Rewind | KEYCODE_MEDIA_REWIND |
| PRE  | Previous / Page Up | KEYCODE_PAGE_UP |
| NXT  | Next / Page Down | KEYCODE_PAGE_DOWN |

### Information
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| INF  | Video Info | KEYCODE_INFO |
| DEL  | Delete | KEYCODE_DEL |

### Audio & Subtitle
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| AUD  | Audio Track | KEYCODE_MEDIA_AUDIO_TRACK |
| SUB  | Subtitle | keycode 2019 |
| RPT  | Repeat Mode | (reserved) |

### Color Keys
| Code | Function | Android KeyEvent |
|------|----------|-----------------|
| RED  | Red | KEYCODE_PROG_RED |
| GRE  | Green | KEYCODE_PROG_GREEN |
| YEL  | Yellow | KEYCODE_PROG_YELLOW |
| BLU  | Blue | KEYCODE_PROG_BLUE |

### Content Pages
| Code | Function | Note |
|------|----------|------|
| MOV  | Movie page | (reserved) |
| MUS  | Music page | (reserved) |
| FIL  | File page | (reserved) |

### DAC Control
| Code | Function | Note |
|------|----------|------|
| DAC  | DAC switch | (reserved) |
| DON  | DAC on | (reserved) |
| DOF  | DAC off | (reserved) |

### System
| Code | Function | Note |
|------|----------|------|
| RBT  | Reboot | PowerManager.reboot() — DESTRUCTIVE |
| RES  | Resolution | KEYCODE_TV_ZOOM_MODE |
| SCR  | Screenshot | (reserved) |
