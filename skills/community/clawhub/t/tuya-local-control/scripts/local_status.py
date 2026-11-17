"""Read a Tuya device's DPS status over the LAN.

Usage:
    python local_status.py <device-name-or-id>

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


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python local_status.py <device-name-or-id>")

    dev = load_device(sys.argv[1])
    ip = dev.get("ip") or dev.get("local_ip")
    version = float(dev.get("version", DEFAULT_VERSION))

    conn = tinytuya.Device(dev["id"], ip, dev["key"], version=version)
    conn.set_socketTimeout(5)

    try:
        status = conn.status()
    except Exception as exc:  # noqa: BLE001 - surface whatever the device said
        raise SystemExit(f"local call failed ({exc}); try the other protocol version")

    print(json.dumps(status, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
