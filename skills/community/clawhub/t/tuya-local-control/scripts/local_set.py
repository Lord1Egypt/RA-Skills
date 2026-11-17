"""Write DPS value(s) to a Tuya device over the LAN.

Usage:
    python local_set.py <device-name-or-id> <dps> <value>

    python local_set.py lamp 1 true              # bool
    python local_set.py lamp 2 80                # int
    python local_set.py plug 20 off              # string (kept as text)

Set several DPS at once by passing a JSON object as the second argument:
    python local_set.py lamp '{"1": true, "2": 80, "3": "warm"}'

Reads id / local key / IP / protocol version from tuya_devices.json
(produced by fetch_keys.py). Run it on a host on the same LAN as the device.
"""

import json
import sys

import tinytuya

DEFAULT_VERSION = 3.3


def load_device(query: str) -> dict:
    with open("tuya_devices.json", encoding="utf-8") as fh:
        devices = json.load(fh)
    for dev in devices:
        if query in (dev.get("name"), dev.get("id")):
            return dev
    names = ", ".join(sorted({d.get("name", "?") for d in devices}))
    raise SystemExit(f"no device matching {query!r}. known: {names}")


def cast(value: str):
    """Turn a CLI string into the JSON type the device expects."""
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value  # plain string, e.g. a mode name


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit("usage: python local_set.py <device> <dps|json> [value]")

    dev = load_device(sys.argv[1])
    ip = dev.get("ip") or dev.get("local_ip")
    version = float(dev.get("version", DEFAULT_VERSION))

    conn = tinytuya.Device(dev["id"], ip, dev["key"], version=version)
    conn.set_socketTimeout(5)

    target = sys.argv[2]
    if target.startswith("{"):
        result = conn.set_multiple_values(json.loads(target))
    elif len(sys.argv) == 4:
        result = conn.set_value(int(target), cast(sys.argv[3]))
    else:
        raise SystemExit("single DPS needs a value, or pass a JSON object")

    print(json.dumps({"result": result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
