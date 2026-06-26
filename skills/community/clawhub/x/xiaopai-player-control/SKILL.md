---
name: xiaopai-player-control
version: 1.1.0
license: MIT-0
description: Control XiaoPai media player over LAN via HTTP/TCP. Use when asked to play videos, send remote-control keys, adjust volume, or query playback status on a XiaoPai player.
---

# XiaoPai Player Control

Control a XiaoPai (小湃) media player on the local network through its TCP/IP protocol.

## Prerequisites

- The player and this machine must be on the **same LAN**.
- The player's `PlayerSupportApp` service must be running (auto-starts on boot).
- You need the player's **IP address**. Use auto-discovery (below) or ask the user.

## Discover Player

The player registers an mDNS service (`_xiaopai._tcp`) on the LAN. Use any of these methods to find it without knowing the IP:

**Linux/macOS:**
```bash
# Browse for players (Bonjour)
dns-sd -B _xiaopai._tcp .

# Or with Avahi
avahi-browse -r _xiaopai._tcp

# Resolve a found service to get IP and port
dns-sd -L "<serviceName>" _xiaopai._tcp .
```

**Windows:**
```bash
# Requires Bonjour SDK or iTunes installed
dns-sd -B _xiaopai._tcp .
```

**Python (cross-platform):**
```python
python3 -c "
from zeroconf import ServiceBrowser, Zeroconf, ServiceStateChange
import time

def on_change(zc, type_, name, state_change):
    if state_change is ServiceStateChange.Added:
        info = zc.get_service_info(type_, name)
        if info:
            from ipaddress import ip_address
            ip = ip_address(info.addresses[0])
            print(f'{info.server} -> {ip}:{info.port}  tcp_port={info.properties.get(b\"tcp_port\",b\"\").decode()}')

zc = Zeroconf()
ServiceBrowser(zc, '_xiaopai._tcp.local.', handlers=[on_change])
time.sleep(3)
zc.close()
"
```

**Using the helper script:**
```bash
xiaopai-ctl.sh discover
```

The discovered service includes:
- **port** (`9050`): HTTP control port
- **TXT `tcp_port`** (`9051`): TCP status port
- **TXT `mac`**: Device MAC address

## Available Operations

### 1. Send Remote-Control Key

Send any remote-control button press to the player.

```
curl "http://{IP}:9050/xiaopai/sendkey?keycode={KEYCODE}"
```

**Response:**
- Success: `{"code":0,"msg":"success"}`
- Unknown key: `{"code":1,"msg":"unknown keycode"}`

**Supported keycodes** (3-character uppercase):

| Category | Keycodes | Description |
|----------|----------|-------------|
| Power | `POW` `OFF` | Power toggle / Power off |
| Numbers | `NU0`-`NU9` | Number keys 0-9 |
| Navigation | `NUP` `NDN` `NLT` `NRT` `SEL` | Up / Down / Left / Right / OK |
| Menu | `OSD` `RET` `HOM` `SET` `MNU` `TOP` | Menu / Back / Home / Settings / PopMenu / TopMenu |
| Volume | `VUP` `VDN` `MUT` | Volume Up / Volume Down / Mute |
| Playback | `PLA` `PAU` `PLU` `STP` | Play-Pause toggle / Pause / Play / Stop |
| Seek | `FWD` `REV` | Fast Forward / Rewind |
| Track | `PRE` `NXT` | Previous / Next |
| Info | `INF` `DEL` `DOT` | Info / Delete / Dot |
| Audio | `AUD` `SUB` `RPT` | Audio Track / Subtitle / Repeat |
| Color | `RED` `GRE` `YEL` `BLU` | Red / Green / Yellow / Blue |
| Navigate | `MOV` `MUS` `FIL` | Movie page / Music page / File page |
| DAC | `DAC` `DON` `DOF` | DAC switch / DAC on / DAC off |
| System | `RBT` `RES` `SCR` | Reboot / Resolution / Screenshot |

### 2. Play Video by File Path or URL

```
curl "http://{IP}:9050/xiaopai/play?videopath={URL_ENCODED_PATH}"
```

- `videopath`: file path or URL of the video, **must be URL-encoded**.
- Success: `{"code":0,"msg":"success"}`

**Example:**
```bash
curl "http://192.168.1.100:9050/xiaopai/play?videopath=http%3A%2F%2Fexample.com%2Fmovie.mp4"
```

### 3. Play Video by Name (Search Library)

```
curl "http://{IP}:9050/xiaopai/play?videoname={URL_ENCODED_NAME}"
```

- `videoname`: movie/video name (Chinese or English), **must be URL-encoded**.
- The player searches its local library; if a match is found, playback starts immediately.
- Success: `{"code":0,"msg":"success"}`

**Example:**
```bash
# Play "战狼" (Wolf Warriors)
curl "http://192.168.1.100:9050/xiaopai/play?videoname=%E6%88%98%E7%8B%BC"
```

### 4. Query Player Status (TCP)

Connect to TCP port 9051 to receive real-time player state.

```bash
# One-shot status query (timeout after 2 seconds)
echo "" | nc -w 2 {IP} 9051
```

**Response JSON:**
```json
{
  "code": 0,
  "msg": "success",
  "deviceName": "XiaoPai Player",
  "mac": "AA:BB:CC:DD:EE:FF",
  "ipAddress": "192.168.1.100",
  "playStatus": 1,
  "playType": 1
}
```

**Field reference:**

| Field | Values |
|-------|--------|
| `playStatus` | `-1` = Stopped, `1` = Playing, `2` = Paused |
| `playType` | `1` = Video, `2` = Music |

The TCP connection stays open; the player pushes updated JSON whenever playback state changes.

## Common Workflows

### Play a movie by name
```bash
curl "http://{IP}:9050/xiaopai/play?videoname={URL_ENCODED_NAME}"
```

### Pause / Resume playback
```bash
curl "http://{IP}:9050/xiaopai/sendkey?keycode=PLA"
```

### Adjust volume up
```bash
curl "http://{IP}:9050/xiaopai/sendkey?keycode=VUP"
```

### Navigate home screen
```bash
curl "http://{IP}:9050/xiaopai/sendkey?keycode=HOM"
```

### Check if something is playing, then stop it
```bash
STATUS=$(echo "" | nc -w 2 {IP} 9051)
# Parse playStatus from JSON; if playing, send stop
curl "http://{IP}:9050/xiaopai/sendkey?keycode=STP"
```

## Guidelines

- Always URL-encode Chinese characters and special characters in `videopath` and `videoname` parameters.
- Use `PLA` to toggle play/pause. Use `PLU` for explicit play, `PAU` for explicit pause.
- `RBT` will reboot the device — confirm with the user before sending.
- The player responds to HTTP within milliseconds; no polling or retry is needed.
- If the user doesn't know the player IP, use mDNS discovery (`dns-sd -B _xiaopai._tcp .` or the `discover` command) to find it automatically.
- For rapid key sequences (e.g., navigating menus), add a short delay (~500ms) between commands.
