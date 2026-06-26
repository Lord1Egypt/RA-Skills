"""Tuya Cloud and local LAN device controller — list, read, and control via tinytuya."""

import json
import os
import sys
import argparse
import time
from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv
import tinytuya

load_dotenv(override=True)


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

def load_tuya_client() -> tinytuya.Cloud:
    """Return an authenticated tinytuya Cloud client from .env credentials."""
    access_id = os.getenv("TUYA_ACCESS_ID")
    access_secret = os.getenv("TUYA_ACCESS_SECRET")
    endpoint = os.getenv("TUYA_API_ENDPOINT", "https://openapi.tuyaus.com")

    if not access_id or not access_secret:
        raise ValueError("TUYA_ACCESS_ID and TUYA_ACCESS_SECRET must be set in .env")

    region_map = {'tuyacn': 'cn', 'tuyaus': 'us', 'tuyaeu': 'eu', 'tuyain': 'in'}
    region = next((r for k, r in region_map.items() if k in endpoint), 'us')

    return tinytuya.Cloud(apiRegion=region, apiKey=access_id, apiSecret=access_secret)


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def list_all_devices(client: tinytuya.Cloud) -> List[Dict[str, Any]]:
    """Return all project devices with real-time online status."""
    resp = client.cloudrequest(
        "/v1.0/iot-01/associated-users/devices",
        query={"last_row_key": ""},
    )
    if resp.get('success'):
        return resp.get('result', {}).get('devices', [])
    raise Exception(f"list_all_devices failed ({resp.get('code')}): {resp.get('msg')}")


def get_device_info(client: tinytuya.Cloud, device_id: str) -> Dict[str, Any]:
    """Return device metadata (name, model, local_key, online, …)."""
    resp = client.cloudrequest(f"/v1.0/devices/{device_id}")
    if resp.get('success'):
        return resp.get('result', {})
    raise Exception(f"get_device_info failed ({resp.get('code')}): {resp.get('msg')}")


def get_device_status(client: tinytuya.Cloud, device_id: str) -> Dict[str, Any]:
    """Return current DP status as a flat {code: value} dict."""
    resp = client.getstatus(device_id)
    if resp.get('success'):
        result = resp.get('result', [])
        # getstatus returns [{code, value}, …]; normalize to flat dict
        return {item['code']: item['value'] for item in result} if isinstance(result, list) else result
    raise Exception(f"get_device_status failed ({resp.get('code')}): {resp.get('msg')}")


def send_device_commands(
    client: tinytuya.Cloud, device_id: str, commands: List[Dict[str, Any]]
) -> bool:
    """Send a list of {code, value} commands to a device. Returns True on success.

    Uses the IoT Core v1.0/iot-03 endpoint (same as Home Assistant tuya_iot),
    which has broader device control support than the older v1.0/devices endpoint.
    """
    resp = client.cloudrequest(
        f"/v1.0/iot-03/devices/{device_id}/commands",
        action='POST',
        post={'commands': commands},
    )
    if resp.get('success'):
        return True
    raise Exception(f"send_device_commands failed ({resp.get('code')}): {resp.get('msg')}")


# ---------------------------------------------------------------------------
# Local (LAN) API
# ---------------------------------------------------------------------------

def scan_local_devices(timeout: int = 18) -> Dict[str, Any]:
    """Scan the local network for Tuya devices via UDP broadcast.

    Returns a dict keyed by gwId: {ip, version, productKey, ...}.
    No cloud credentials required.
    """
    return tinytuya.deviceScan(verbose=False, maxretry=timeout)


def _make_local_device(device_id: str, ip: str, local_key: str, version: float, cid: str = None) -> tinytuya.Device:
    kwargs = {"cid": cid} if cid else {}
    d = tinytuya.Device(device_id, ip, local_key, **kwargs)
    d.set_version(version)
    if version >= 3.4:
        d.set_socketPersistent(True)
    return d


def get_local_device_status(
    device_id: str,
    ip: str,
    local_key: str,
    version: float = 3.3,
) -> Dict[str, Any]:
    """Read current DP status directly over LAN. Returns raw {dp_id: value} dict."""
    d = _make_local_device(device_id, ip, local_key, version)
    resp = d.status()
    if not resp:
        raise Exception("No response from device")
    if 'Error' in resp:
        raise Exception(f"Local status error: {resp['Error']}")
    return resp.get('dps', resp)


def send_local_device_commands(
    device_id: str,
    ip: str,
    local_key: str,
    commands: List[Dict[str, Any]],
    version: float = 3.3,
) -> bool:
    """Send commands to a device directly over LAN.

    Each command must have 'value' and either:
      'dp'   — integer DP index  (e.g. {"dp": 1, "value": true})
      'code' — string DP name    (e.g. {"code": "switch_1", "value": true})
    String codes are passed as-is; use integer dp for maximum compatibility.
    """
    d = _make_local_device(device_id, ip, local_key, version)
    payload: Dict[Any, Any] = {}
    for cmd in commands:
        key = cmd['dp'] if 'dp' in cmd else cmd['code']
        payload[key] = cmd['value']
    resp = d.set_multiple_values(payload)
    if resp and 'Error' in resp:
        raise Exception(f"Local command error: {resp['Error']}")
    return True


def get_local_subdevice_status(
    gateway_id: str,
    gateway_ip: str,
    gateway_local_key: str,
    sub_device_id: str,
    version: float = 3.3,
) -> Dict[str, Any]:
    """Read status of a Zigbee/sub-device via its gateway over LAN."""
    d = _make_local_device(gateway_id, gateway_ip, gateway_local_key, version, cid=sub_device_id)
    resp = d.status()
    if not resp:
        raise Exception("No response from gateway")
    if 'Error' in resp:
        raise Exception(f"Gateway status error: {resp['Error']}")
    return resp.get('dps', resp)


def send_local_subdevice_commands(
    gateway_id: str,
    gateway_ip: str,
    gateway_local_key: str,
    sub_device_id: str,
    commands: List[Dict[str, Any]],
    version: float = 3.3,
) -> bool:
    """Send commands to a Zigbee/sub-device via its gateway over LAN."""
    d = _make_local_device(gateway_id, gateway_ip, gateway_local_key, version, cid=sub_device_id)
    payload: Dict[Any, Any] = {}
    for cmd in commands:
        key = cmd['dp'] if 'dp' in cmd else cmd['code']
        payload[key] = cmd['value']
    resp = d.set_multiple_values(payload)
    if resp and 'Error' in resp:
        raise Exception(f"Gateway command error: {resp['Error']}")
    return True


# ---------------------------------------------------------------------------
# Data parsing & formatting
# ---------------------------------------------------------------------------

def get_device_24h_avg_humidity(client: tinytuya.Cloud, device_id: str) -> Dict[str, Any]:
    """Fetch 24 h of DP logs and return average va_humidity across all readings."""
    now_ms = int(time.time() * 1000)
    start_ms = now_ms - 24 * 3600 * 1000

    all_logs = []
    row_key = ""
    while True:
        query: Dict[str, Any] = {
            "start_time": start_ms,
            "end_time": now_ms,
            "size": 100,
            "type": "7",
        }
        if row_key:
            query["start_row_key"] = row_key
        resp = client.cloudrequest(f"/v1.0/devices/{device_id}/logs", query=query)
        if not resp.get("success"):
            raise Exception(f"get_device_24h_avg_humidity failed ({resp.get('code')}): {resp.get('msg')}")
        result = resp["result"]
        logs = result.get("logs", [])
        all_logs.extend(logs)
        if not result.get("has_next") or not logs:
            break
        row_key = result["current_row_key"]

    humidity_codes = {"va_humidity", "humidity_value", "soil_moisture", "humidity"}
    humidity_values = [
        float(log["value"])
        for log in all_logs
        if log.get("code") in humidity_codes and log.get("value") is not None
    ]

    if not humidity_values:
        return {"avg_humidity": None, "count": 0, "min_humidity": None, "max_humidity": None}

    return {
        "avg_humidity": round(sum(humidity_values) / len(humidity_values), 1),
        "count": len(humidity_values),
        "min_humidity": min(humidity_values),
        "max_humidity": max(humidity_values),
    }


def parse_sensor_data(status: Dict[str, Any]) -> Dict[str, Any]:
    """Parse raw DP status dict into typed, human-readable fields."""
    parsed: Dict[str, Any] = {}

    temp_raw = status.get('va_temperature') or status.get('temp_current') or status.get('temp_set')
    if temp_raw is not None:
        # Some Tuya devices report in tenths of a degree (raw 90 = 9°C), others in whole degrees.
        # If the raw value is already in a plausible °C range, use it directly.
        if -80 <= temp_raw <= 80:
            parsed['temperature_celsius'] = round(float(temp_raw), 1)
        else:
            parsed['temperature_celsius'] = round(temp_raw / 10.0, 1)

    humidity = status.get('va_humidity') or status.get('humidity_value')
    if humidity is not None:
        parsed['humidity_percent'] = float(humidity)

    battery = status.get('battery_percentage') or status.get('battery')
    if battery is not None:
        parsed['battery_percent'] = int(battery)
        parsed['battery_status'] = 'Good' if battery > 80 else 'Medium' if battery > 20 else 'Low'

    motion = status.get('pir')
    if motion is not None:
        parsed['motion_detected'] = (motion == 'pir')

    door_state = status.get('doorcontact_state')
    if door_state is not None:
        parsed['door_open'] = bool(door_state)
        parsed['door_status'] = 'Open' if door_state else 'Closed'

    state = status.get('state')
    if state is not None:
        parsed['state'] = state
        if isinstance(state, (int, bool)):
            parsed['state_text'] = 'On' if state else 'Off'

    parsed['raw_status'] = status
    parsed['last_updated'] = datetime.utcnow().isoformat() + 'Z'
    return parsed


def format_device_status(
    device_id: str,
    info: Dict[str, Any],
    status: Dict[str, Any],
    parsed_data: Dict[str, Any],
    format_type: str = 'json',
) -> str:
    """Format device info + status as JSON or human-readable text."""
    online = bool(info.get('online') or info.get('is_online'))

    if format_type == 'json':
        return json.dumps({
            'device_id': device_id,
            'name': info.get('name', 'Unknown'),
            'category': info.get('category', 'Unknown'),
            'online': online,
            'model': info.get('model', 'Unknown'),
            'status': status,
            'parsed_data': parsed_data,
        }, indent=2)

    lines = [
        f"Device: {info.get('name', 'Unknown')} ({device_id})",
        f"Category: {info.get('category', 'Unknown')}",
        f"Status: {'Online' if online else 'Offline'}",
        f"Model: {info.get('model', 'Unknown')}",
        "",
        "Device Data:",
    ]
    has_data = False
    for key, label, fmt in [
        ('temperature_celsius', '🌡️  Temperature', lambda v: f"{v}°C"),
        ('humidity_percent',    '💧 Humidity',     lambda v: f"{v}%"),
        ('battery_percent',     '🔋 Battery',      lambda v: f"{v}% ({parsed_data.get('battery_status')})"),
        ('motion_detected',     '🚶 Motion',       lambda v: 'Detected' if v else 'Not Detected'),
        ('door_status',         '🚪 Door',         lambda v: v),
        ('state',               '🔘 State',        lambda v: parsed_data.get('state_text', str(v))),
    ]:
        if key in parsed_data:
            lines.append(f"  {label}: {fmt(parsed_data[key])}")
            has_data = True

    if not has_data:
        lines += ["  No parsed data", "", "Raw Status:"] + [f"  • {k}: {v}" for k, v in status.items()]

    lines += ["", f"Last Updated: {parsed_data.get('last_updated', '')}"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI command handlers
# ---------------------------------------------------------------------------

def cmd_list_devices(args: argparse.Namespace) -> None:
    client = load_tuya_client()
    devices = list_all_devices(client)
    if args.output_format == 'json':
        print(json.dumps(devices, indent=2))
        return
    print(f"Found {len(devices)} device(s):\n")
    for dev in devices:
        online = bool(dev.get('online'))
        print(f"  {'🟢' if online else '🔴'} {dev.get('name', 'Unknown')}")
        print(f"     ID: {dev.get('id')}  category: {dev.get('category')}  {'Online' if online else 'Offline'}")


def cmd_read_sensor(args: argparse.Namespace) -> None:
    client = load_tuya_client()
    info = get_device_info(client, args.device_id)
    status = get_device_status(client, args.device_id)
    parsed = parse_sensor_data(status)
    print(format_device_status(args.device_id, info, status, parsed, format_type=args.output_format))


def cmd_control_device(args: argparse.Namespace) -> None:
    commands = json.loads(args.commands)
    client = load_tuya_client()
    send_device_commands(client, args.device_id, commands)
    print(f"✓ Sent to {args.device_id}")
    for cmd in commands:
        print(f"  • {cmd['code']} = {cmd['value']}")


def cmd_read_24h_avg(args: argparse.Namespace) -> None:
    client = load_tuya_client()
    result = get_device_24h_avg_humidity(client, args.device_id)
    print(json.dumps(result, indent=2))


def get_device_last_n_humidity(client: tinytuya.Cloud, device_id: str, n: int = 50) -> Dict[str, Any]:
    """Fetch the last N humidity log entries and return avg/count/min/max.

    Looks back up to 7 days to find N readings. Fixes pagination using next_row_key.
    """
    now_ms = int(time.time() * 1000)
    start_ms = now_ms - 7 * 24 * 3600 * 1000

    humidity_codes = {"va_humidity", "humidity_value", "soil_moisture", "humidity"}
    humidity_values: List[float] = []
    row_key = ""

    while len(humidity_values) < n:
        query: Dict[str, Any] = {
            "start_time": start_ms,
            "end_time": now_ms,
            "size": 100,
            "type": "7",
        }
        if row_key:
            query["start_row_key"] = row_key
        resp = client.cloudrequest(f"/v1.0/devices/{device_id}/logs", query=query)
        if not resp.get("success"):
            raise Exception(f"get_device_last_n_humidity failed ({resp.get('code')}): {resp.get('msg')}")
        result = resp["result"]
        logs = result.get("logs", [])
        for log in logs:
            if log.get("code") in humidity_codes and log.get("value") is not None:
                humidity_values.append(float(log["value"]))
                if len(humidity_values) >= n:
                    break
        if not result.get("has_next") or not logs:
            break
        row_key = result.get("next_row_key") or result.get("current_row_key", "")

    if not humidity_values:
        return {"avg_humidity": None, "count": 0, "min_humidity": None, "max_humidity": None}

    return {
        "avg_humidity": round(sum(humidity_values) / len(humidity_values), 1),
        "count": len(humidity_values),
        "min_humidity": min(humidity_values),
        "max_humidity": max(humidity_values),
    }


def cmd_read_last_n(args: argparse.Namespace) -> None:
    client = load_tuya_client()
    result = get_device_last_n_humidity(client, args.device_id, args.n)
    print(json.dumps(result, indent=2))


def cmd_scan_local(args: argparse.Namespace) -> None:
    """Scan local network for Tuya devices (no cloud credentials needed)."""
    print(f"Scanning local network (timeout={args.timeout}s)…", file=sys.stderr)
    devices = scan_local_devices(timeout=args.timeout)

    # Optionally enrich with cloud names/local_keys
    cloud_map: Dict[str, Any] = {}
    if args.enrich:
        try:
            client = load_tuya_client()
            for dev in list_all_devices(client):
                cloud_map[dev['id']] = dev
        except Exception as e:
            print(f"⚠ Cloud enrichment failed: {e}", file=sys.stderr)

    if args.output_format == 'json':
        enriched = {}
        for gw_id, info in devices.items():
            entry = dict(info)
            if gw_id in cloud_map:
                entry['name'] = cloud_map[gw_id].get('name')
                entry['local_key'] = cloud_map[gw_id].get('local_key')
            enriched[gw_id] = entry
        print(json.dumps(enriched, indent=2))
        return

    print(f"\nFound {len(devices)} local device(s):\n")
    for gw_id, info in devices.items():
        name = cloud_map.get(gw_id, {}).get('name', gw_id)
        local_key = cloud_map.get(gw_id, {}).get('local_key', '')
        ip = info.get('ip', '?')
        ver = info.get('version', '?')
        print(f"  {name}")
        print(f"    ID: {gw_id}  IP: {ip}  version: {ver}" +
              (f"  local_key: {local_key}" if local_key else ""))


def cmd_read_local(args: argparse.Namespace) -> None:
    """Read device status directly over LAN."""
    status = get_local_device_status(args.device_id, args.ip, args.local_key, args.version)
    if args.output_format == 'json':
        print(json.dumps({'device_id': args.device_id, 'ip': args.ip, 'dps': status}, indent=2))
        return
    print(f"Device {args.device_id} ({args.ip}):")
    for dp, val in status.items():
        print(f"  dp {dp}: {val}")


def cmd_control_local(args: argparse.Namespace) -> None:
    """Control a device directly over LAN."""
    commands = json.loads(args.commands)
    send_local_device_commands(args.device_id, args.ip, args.local_key, commands, args.version)
    print(f"✓ Sent to {args.device_id} ({args.ip})")
    for cmd in commands:
        key = cmd.get('dp', cmd.get('code'))
        print(f"  • dp/code {key} = {cmd['value']}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tuya Cloud Controller",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (Cloud):
  python tuya_controller.py list_devices
  python tuya_controller.py list_devices --output_format json

  python tuya_controller.py read_sensor bf0a155b2e49d3367bafrz
  python tuya_controller.py read_sensor bf0a155b2e49d3367bafrz --output_format text

  python tuya_controller.py control_device bffc2c6de8e82861e5vlhh '[{"code":"switch_1","value":true}]'

Examples (Local LAN — no cloud credentials needed for scan):
  python tuya_controller.py scan_local
  python tuya_controller.py scan_local --timeout 10 --enrich --output_format json

  python tuya_controller.py read_local DEVICE_ID 192.168.1.50 MY_LOCAL_KEY
  python tuya_controller.py read_local DEVICE_ID 192.168.1.50 MY_LOCAL_KEY --version 3.4

  python tuya_controller.py control_local DEVICE_ID 192.168.1.50 MY_LOCAL_KEY '[{"dp":1,"value":true}]'
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list_devices", help="List all Tuya devices")
    p.add_argument("--output_format", choices=["json", "text"], default="text")
    p.set_defaults(func=cmd_list_devices)

    p = sub.add_parser("read_sensor", help="Read sensor data from a device")
    p.add_argument("device_id")
    p.add_argument("--output_format", choices=["json", "text"], default="json")
    p.set_defaults(func=cmd_read_sensor)

    p = sub.add_parser("control_device", help="Send commands to a Tuya device")
    p.add_argument("device_id")
    p.add_argument("commands", help='JSON array, e.g. \'[{"code":"switch_1","value":true}]\'')
    p.set_defaults(func=cmd_control_device)

    p = sub.add_parser("read_24h_avg", help="Return 24h average humidity for a sensor")
    p.add_argument("device_id")
    p.set_defaults(func=cmd_read_24h_avg)

    p = sub.add_parser("read_last_n", help="Return avg humidity from last N readings (default 50)")
    p.add_argument("device_id")
    p.add_argument("--n", type=int, default=50)
    p.set_defaults(func=cmd_read_last_n)

    p = sub.add_parser("scan_local", help="Scan local network for Tuya devices (no credentials needed)")
    p.add_argument("--timeout", type=int, default=18, help="UDP scan timeout in seconds (default: 18)")
    p.add_argument("--enrich", action="store_true", help="Cross-reference with cloud to add device names and local keys")
    p.add_argument("--output_format", choices=["json", "text"], default="text")
    p.set_defaults(func=cmd_scan_local)

    p = sub.add_parser("read_local", help="Read device status directly over LAN")
    p.add_argument("device_id")
    p.add_argument("ip")
    p.add_argument("local_key")
    p.add_argument("--version", type=float, default=3.3, help="Protocol version (default: 3.3)")
    p.add_argument("--output_format", choices=["json", "text"], default="json")
    p.set_defaults(func=cmd_read_local)

    p = sub.add_parser("control_local", help="Control a device directly over LAN")
    p.add_argument("device_id")
    p.add_argument("ip")
    p.add_argument("local_key")
    p.add_argument("commands", help='JSON array, e.g. \'[{"dp":1,"value":true}]\' or \'[{"code":"switch_1","value":true}]\'')
    p.add_argument("--version", type=float, default=3.3, help="Protocol version (default: 3.3)")
    p.set_defaults(func=cmd_control_local)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
