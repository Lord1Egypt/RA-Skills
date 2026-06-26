# Sony Bravia TV Control

Control your Sony Bravia TV from OpenClaw via Telegram — power, volume, apps, playback, and full remote navigation.

## Features

- **Power** — on (Wake-on-LAN) / off
- **Volume** — up, down, set, mute/unmute
- **Apps** — launch Netflix, YouTube, Prime Video, Hotstar, or any installed app
- **Remote** — full navigation (up/down/left/right/ok/back/home), playback (play/pause/stop/ff/rw), HDMI switching, subtitles
- **Status** — power state, current volume, mute status

## Quick Start

1. **Run setup** (auto-discovers TV, tests connection, saves config):
   ```
   python3 scripts/setup.py
   ```

2. **Or set env vars manually:**
   - SONY_TV_IP — TV IP address
   - SONY_TV_PSK — Pre-Shared Key (TV > Settings > Network > IP Control)
   - SONY_TV_MAC — MAC address (optional, for Wake-on-LAN)

3. **Test:**
   ```
   uv run scripts/tv_control.py --action status
   ```

## TV Setup

1. Settings > Network > Home Network > IP Control
2. Authentication: Normal and Pre-Shared Key
3. Set a Pre-Shared Key (e.g. sony1234)
4. Enable Remote Start (for power on)

## Usage

Tell your agent: "turn on the TV", "open Netflix", "volume 25", "navigate down 3 and select", "switch to HDMI 2"

## Compatibility

- Android TV (2015+): full support
- Google TV: works
- Pre-2015: not supported
