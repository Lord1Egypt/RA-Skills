"""Fetch Tuya device ids + local keys from the Tuya IoT Cloud API.

Prerequisites:
  * A Tuya IoT Platform project with "IoT Core" enabled.
  * Your Smart Life / Tuya app account linked to that project.

Credentials come from the environment -- never hardcode them:

  set TUYA_API_KEY=...         Access ID / Client ID
  set TUYA_API_SECRET=...      Access Secret / Client Secret
  set TUYA_API_REGION=eu       eu | us | cn | in   (default: eu)
  set TUYA_APP_DEVICE_ID=...   any device id from the app, used to bind the account

Output: tuya_devices.json in the current directory.

The cloud is only needed for this provisioning step; after it runs you can
control the devices locally with local_status.py / local_set.py.
"""

import json
import os

import tinytuya


def main() -> int:
    api_key = os.environ.get("TUYA_API_KEY")
    api_secret = os.environ.get("TUYA_API_SECRET")
    region = os.environ.get("TUYA_API_REGION", "eu")
    app_device = os.environ.get("TUYA_APP_DEVICE_ID", "")

    if not api_key or not api_secret:
        raise SystemExit(
            "set TUYA_API_KEY and TUYA_API_SECRET (Access ID / Access Secret) first"
        )

    cloud = tinytuya.Cloud(
        apiRegion=region,
        apiKey=api_key,
        apiSecret=api_secret,
        apiDeviceID=app_device,
    )

    resp = cloud.getdevices()
    devices = resp.get("result", []) if isinstance(resp, dict) else resp

    with open("tuya_devices.json", "w", encoding="utf-8") as fh:
        json.dump(devices, fh, ensure_ascii=False, indent=2)

    print(f"saved {len(devices)} device(s) to tuya_devices.json")
    for dev in devices:
        has_key = "key set" if dev.get("key") else "NO local key"
        print(f"- {dev.get('name')}  id={dev.get('id')}  {has_key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
