# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "wakeonlan",
# ]
# ///
"""Sony Bravia TV control via REST API (JSON-RPC), IRCC remote, and Wake-on-LAN."""

import argparse
import json
import os
import sys
import time

import requests
from wakeonlan import send_magic_packet

# Load .env file if present (allows standalone use without system env vars)
_env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
if os.path.isfile(_env_file):
    with open(_env_file) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

TV_IP = os.environ.get("SONY_TV_IP")
TV_PSK = os.environ.get("SONY_TV_PSK")
TV_MAC = os.environ.get("SONY_TV_MAC")

KNOWN_APPS = {
    "netflix": "com.sony.dtv.com.netflix.ninja.com.netflix.ninja.MainActivity",
    "youtube": "com.sony.dtv.com.google.android.youtube.tv.com.google.android.apps.youtube.tv.activity.ShellActivity",
    "hotstar": "com.sony.dtv.in.startv.hotstar.in.startv.hotstar.MainActivity",
    "disney+hotstar": "com.sony.dtv.in.startv.hotstar.in.startv.hotstar.MainActivity",
    "jiocinema": "com.sony.dtv.in.startv.hotstar.in.startv.hotstar.MainActivity",
    "prime": "com.sony.dtv.com.amazon.avod.com.amazon.avod.MainActivity",
    "prime video": "com.sony.dtv.com.amazon.avod.com.amazon.avod.MainActivity",
    "amazon prime": "com.sony.dtv.com.amazon.avod.com.amazon.avod.MainActivity",
}

# IRCC remote control codes (queried from TV)
IRCC_CODES = {
    "up": "AAAAAQAAAAEAAAB0Aw==",
    "down": "AAAAAQAAAAEAAAB1Aw==",
    "left": "AAAAAQAAAAEAAAA0Aw==",
    "right": "AAAAAQAAAAEAAAAzAw==",
    "ok": "AAAAAQAAAAEAAABlAw==",
    "confirm": "AAAAAQAAAAEAAABlAw==",
    "enter": "AAAAAQAAAAEAAAALAw==",
    "back": "AAAAAgAAAJcAAAAjAw==",
    "return": "AAAAAgAAAJcAAAAjAw==",
    "home": "AAAAAQAAAAEAAABgAw==",
    "play": "AAAAAgAAAJcAAAAaAw==",
    "pause": "AAAAAgAAAJcAAAAZAw==",
    "stop": "AAAAAgAAAJcAAAAYAw==",
    "forward": "AAAAAgAAAJcAAAAcAw==",
    "rewind": "AAAAAgAAAJcAAAAbAw==",
    "next": "AAAAAgAAAJcAAAA9Aw==",
    "prev": "AAAAAgAAAJcAAAA8Aw==",
    "mute_ir": "AAAAAQAAAAEAAAAUAw==",
    "volumeup": "AAAAAQAAAAEAAAASAw==",
    "volumedown": "AAAAAQAAAAEAAAATAw==",
    "channelup": "AAAAAQAAAAEAAAAQAw==",
    "channeldown": "AAAAAQAAAAEAAAARAw==",
    "input": "AAAAAQAAAAEAAAAlAw==",
    "hdmi1": "AAAAAgAAABoAAABaAw==",
    "hdmi2": "AAAAAgAAABoAAABbAw==",
    "hdmi3": "AAAAAgAAABoAAABcAw==",
    "hdmi4": "AAAAAgAAABoAAABdAw==",
    "netflix_btn": "AAAAAgAAABoAAAB8Aw==",
    "youtube_btn": "AAAAAgAAAMQAAABHAw==",
    "options": "AAAAAgAAAJcAAAA2Aw==",
    "subtitle": "AAAAAgAAAJcAAAAoAw==",
    "exit": "AAAAAQAAAAEAAABjAw==",
    "sleep": "AAAAAQAAAAEAAAAvAw==",
    "wakeup": "AAAAAQAAAAEAAAAuAw==",
    "display": "AAAAAQAAAAEAAAA6Aw==",
    "num0": "AAAAAQAAAAEAAAAJAw==",
    "num1": "AAAAAQAAAAEAAAAAAw==",
    "num2": "AAAAAQAAAAEAAAABAw==",
    "num3": "AAAAAQAAAAEAAAACAw==",
    "num4": "AAAAAQAAAAEAAAADAw==",
    "num5": "AAAAAQAAAAEAAAAEAw==",
    "num6": "AAAAAQAAAAEAAAAFAw==",
    "num7": "AAAAAQAAAAEAAAAGAw==",
    "num8": "AAAAAQAAAAEAAAAHAw==",
    "num9": "AAAAAQAAAAEAAAAIAw==",
}

TIMEOUT = 8


def _check_env():
    missing = []
    if not TV_IP:
        missing.append("SONY_TV_IP")
    if not TV_PSK:
        missing.append("SONY_TV_PSK")
    if missing:
        print(f"ERROR: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)


def _rpc(endpoint: str, method: str, params: list | None = None, version: str = "1.0") -> dict:
    """Send a JSON-RPC request to the TV."""
    url = f"http://{TV_IP}/sony/{endpoint}"
    payload = {
        "method": method,
        "id": 1,
        "params": params or [],
        "version": version,
    }
    headers = {"X-Auth-PSK": TV_PSK, "Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            print("ERROR: TV returned invalid response. It may be starting up or unresponsive.")
            sys.exit(1)
    except requests.exceptions.Timeout:
        print("ERROR: Connection timed out. TV may be off or unreachable.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to TV. Check IP address and network.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP {e.response.status_code} from TV.")
        sys.exit(1)


def _send_ircc(code_name: str):
    """Send an IRCC remote command to the TV."""
    code = IRCC_CODES.get(code_name.lower())
    if not code:
        print(f"ERROR: Unknown remote button '{code_name}'. Available: {', '.join(sorted(IRCC_CODES.keys()))}")
        sys.exit(1)
    url = f"http://{TV_IP}/sony/IRCC"
    body = f'<?xml version="1.0"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1"><IRCCCode>{code}</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>'
    headers = {
        "X-Auth-PSK": TV_PSK,
        "Content-Type": "text/xml; charset=UTF-8",
        "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
    }
    try:
        resp = requests.post(url, data=body, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        print(f"OK: {code_name}")
    except requests.exceptions.Timeout:
        print("ERROR: Connection timed out. TV may be off or unreachable.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to TV.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP {e.response.status_code} sending {code_name}.")
        sys.exit(1)


# --- Actions ---

def power_on():
    if not TV_MAC:
        print("ERROR: SONY_TV_MAC not set — needed for Wake-on-LAN power on.")
        sys.exit(1)
    send_magic_packet(TV_MAC)
    for attempt in range(3):
        time.sleep(3)
        try:
            result = _rpc("system", "getPowerStatus")
            status = result.get("result", [{}])[0].get("status", "unknown")
            if status == "active":
                print("OK: TV is on.")
                return
        except SystemExit:
            pass
    print("WARNING: Wake-on-LAN sent but TV did not respond. Check Remote Start is ON (Settings > Network > Remote Start).")


def power_off():
    _rpc("system", "setPowerStatus", [{"status": False}])
    print("OK: TV powered off.")


def get_status():
    result = _rpc("system", "getPowerStatus")
    status = result.get("result", [{}])[0].get("status", "unknown")
    print(f"Power: {status}")
    if status == "active":
        vol_result = _rpc("audio", "getVolumeInformation")
        volumes = vol_result.get("result", [[]])[0]
        for v in volumes:
            if v.get("target") == "speaker":
                print(f"Volume: {v.get('volume', '?')}")
                print(f"Muted: {'yes' if v.get('mute') else 'no'}")
                break


def volume_set(value: int):
    if not (0 <= value <= 100):
        print("ERROR: Volume must be 0-100")
        sys.exit(1)
    _rpc("audio", "setAudioVolume", [{"target": "speaker", "volume": str(value)}])
    print(f"OK: Volume set to {value}.")


def volume_up():
    _rpc("audio", "setAudioVolume", [{"target": "speaker", "volume": "+1"}])
    print("OK: Volume up.")


def volume_down():
    _rpc("audio", "setAudioVolume", [{"target": "speaker", "volume": "-1"}])
    print("OK: Volume down.")


def mute():
    vol_result = _rpc("audio", "getVolumeInformation")
    volumes = vol_result.get("result", [[]])[0]
    current_mute = False
    for v in volumes:
        if v.get("target") == "speaker":
            current_mute = v.get("mute", False)
            break
    new_mute = not current_mute
    _rpc("audio", "setAudioMute", [{"status": new_mute}])
    print(f"OK: {'Muted' if new_mute else 'Unmuted'}.")


def open_app(app_name: str):
    key = app_name.lower().strip()
    uri = KNOWN_APPS.get(key)
    if not uri:
        for known_key, known_uri in KNOWN_APPS.items():
            if key in known_key or known_key in key:
                uri = known_uri
                break
    if not uri:
        print(f"App '{app_name}' not in known list. Searching installed apps...")
        result = _rpc("appControl", "getApplicationList")
        apps = result.get("result", [[]])[0]
        for app in apps:
            if key in app.get("title", "").lower():
                uri = app.get("uri")
                print(f"Found: {app.get('title')}")
                break
    if not uri:
        print(f"ERROR: Could not find app '{app_name}'. Known: {', '.join(KNOWN_APPS.keys())}")
        sys.exit(1)
    _rpc("appControl", "setActiveApp", [{"uri": uri}])
    print(f"OK: Launched {app_name}.")


def list_apps():
    result = _rpc("appControl", "getApplicationList")
    apps = result.get("result", [[]])[0]
    if not apps:
        print("No apps found (TV may be off or API unavailable).")
        return
    print(f"Installed apps ({len(apps)}):\n")
    for app in sorted(apps, key=lambda a: a.get("title", "")):
        print(f"  {app.get('title', '?'):30s}  {app.get('uri', '')}")


def remote(buttons: str):
    """Send one or more IRCC remote button presses with a short delay between them."""
    button_list = [b.strip() for b in buttons.split(",")]
    for btn in button_list:
        # Handle repeat syntax like "ok*3"
        if "*" in btn:
            name, count = btn.split("*", 1)
            count = int(count)
        else:
            name = btn
            count = 1
        for _ in range(count):
            _send_ircc(name)
            if len(button_list) > 1 or count > 1:
                time.sleep(0.5)
    print(f"OK: Sent {buttons}")


def list_buttons():
    """List all available remote buttons."""
    print("Available remote buttons:\n")
    for name in sorted(IRCC_CODES.keys()):
        print(f"  {name}")


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Sony Bravia TV Control")
    parser.add_argument("--action", required=True,
                        choices=["power_on", "power_off", "status", "volume_set",
                                 "volume_up", "volume_down", "mute", "open_app", "list_apps",
                                 "remote", "list_buttons"],
                        help="Action to perform")
    parser.add_argument("--value", type=int, help="Volume level (0-100) for volume_set")
    parser.add_argument("--app", type=str, help="App name for open_app")
    parser.add_argument("--buttons", type=str, help="Comma-separated button names for remote (e.g. 'ok,ok,down,ok'). Use name*N for repeats (e.g. 'down*3,ok')")
    args = parser.parse_args()

    if args.action == "power_on":
        power_on()
        return

    _check_env()

    match args.action:
        case "power_off":
            power_off()
        case "status":
            get_status()
        case "volume_set":
            if args.value is None:
                print("ERROR: --value required for volume_set")
                sys.exit(1)
            volume_set(args.value)
        case "volume_up":
            volume_up()
        case "volume_down":
            volume_down()
        case "mute":
            mute()
        case "open_app":
            if not args.app:
                print("ERROR: --app required for open_app")
                sys.exit(1)
            open_app(args.app)
        case "list_apps":
            list_apps()
        case "remote":
            if not args.buttons:
                print("ERROR: --buttons required for remote (e.g. --buttons 'ok,down,ok')")
                sys.exit(1)
            remote(args.buttons)
        case "list_buttons":
            list_buttons()
        case _:
            print(f"ERROR: Unknown action")
            sys.exit(1)


if __name__ == "__main__":
    main()
