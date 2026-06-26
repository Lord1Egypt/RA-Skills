---
name: sony-bravia-tv
description: >
  Control Sony Bravia TV — power, volume, apps, playback, and full remote navigation via REST API and IRCC on local network.
version: 1.1.0
author: Vikas Menon
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - SONY_TV_IP
        - SONY_TV_PSK
        - SONY_TV_MAC
      bins:
        - uv
    primaryEnv: SONY_TV_PSK
    tags:
      - iot
      - smart-home
      - tv
      - sony
      - bravia
---

# Sony Bravia TV Control

You control a Sony Bravia TV on the user's home network via a Python script that talks to the TV's REST API and IRCC remote interface.

## How It Works

All commands go through one script: `{baseDir}/scripts/tv_control.py`

Run it with `uv run`:
```
uv run {baseDir}/scripts/tv_control.py --action <action> [--value <n>] [--app <name>] [--buttons <buttons>]
```

## Command Mapping

When the user says something like the phrases below, run the corresponding command.

### Power

| User says | Command |
|-----------|---------|
| "turn on the TV" / "switch on TV" / "power on" | `--action power_on` |
| "turn off the TV" / "switch off" / "power off" / "shut down TV" | `--action power_off` |

### Volume

| User says | Command |
|-----------|---------|
| "volume up" / "louder" / "increase volume" | `--action volume_up` |
| "volume down" / "quieter" / "decrease volume" / "lower volume" | `--action volume_down` |
| "set volume to 30" / "volume 30" / "make it 30" | `--action volume_set --value 30` |
| "mute" / "unmute" / "toggle mute" | `--action mute` |

Volume range is **0-100**. Values outside this range will be rejected.

### Apps

| User says | Command |
|-----------|---------|
| "open Netflix" / "play Netflix" / "launch Netflix" | `--action open_app --app netflix` |
| "open YouTube" / "put on YouTube" | `--action open_app --app youtube` |
| "open Hotstar" / "open JioCinema" | `--action open_app --app hotstar` |
| "open Prime Video" / "open Amazon Prime" | `--action open_app --app prime` |
| "open [any app name]" | `--action open_app --app "<name>"` |
| "what apps are installed?" / "list apps" | `--action list_apps` |

Note: Hotstar and JioCinema use the same app (JioCinema absorbed Disney+ Hotstar in India). Both `hotstar` and `jiocinema` keys work.

### Remote Control / Navigation

| User says | Command |
|-----------|---------|
| "press OK" / "select" / "confirm" | `--action remote --buttons "ok"` |
| "go up" / "navigate up" | `--action remote --buttons "up"` |
| "go down" / "navigate down" | `--action remote --buttons "down"` |
| "go left" / "go right" | `--action remote --buttons "left"` or `"right"` |
| "go back" / "press back" | `--action remote --buttons "back"` |
| "go home" / "press home" | `--action remote --buttons "home"` |
| "play" / "resume" | `--action remote --buttons "play"` |
| "pause" | `--action remote --buttons "pause"` |
| "fast forward" | `--action remote --buttons "forward"` |
| "rewind" | `--action remote --buttons "rewind"` |
| "switch to HDMI 1" / "HDMI 2" | `--action remote --buttons "hdmi1"` or `"hdmi2"` |
| "press subtitle" / "subtitles" | `--action remote --buttons "subtitle"` |
| "scroll down 3 times and select" | `--action remote --buttons "down*3,ok"` |
| "what buttons are available?" | `--action list_buttons` |

You can chain multiple buttons with commas: `--buttons "down,down,ok"`. Use `name*N` for repeats: `--buttons "down*5,ok"`.

### Status

| User says | Command |
|-----------|---------|
| "TV status" / "is the TV on?" / "what's playing?" / "what volume?" | `--action status` |

## Response Guidelines

- After running a command, report the script output to the user in a brief, natural way.
- If the script prints an error (connection timeout, missing env var), tell the user what went wrong and suggest a fix (check if TV is on, check network, etc.).
- If the user asks to open an app not in the known list, the script will search installed apps automatically — just pass the name.
- For "volume up/down" repeated requests like "louder louder louder", run volume_up multiple times.
- If the TV is off and the user asks for anything other than power on, suggest turning it on first.
- For navigation sequences, chain buttons in a single remote command rather than running multiple commands.

## Not Supported

- **Keyboard / text input** — the TV API does not support typing text into search fields.
- **Screen mirroring** — cannot start or manage Miracast/screen mirroring sessions.
- **Casting** — cannot initiate Chromecast sessions (use your phone for that).

## Compatibility

- **Android TV (2015+)**: Full support — REST API + IRCC + WoL.
- **Google TV**: Works with caveats — some newer models may require re-pairing the PSK after firmware updates.
- **Pre-2015 (non-Android)**: Not supported — these models use a different API.

## Notes

- **Power ON uses Wake-on-LAN** — it sends a magic packet, so the TV must have Remote Start enabled and `SONY_TV_MAC` must be set.
- **All other commands use the REST API** — requires `SONY_TV_IP` and `SONY_TV_PSK`.
- The TV must be on the same network as the machine running this script.
