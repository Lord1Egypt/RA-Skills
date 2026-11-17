---
name: "tuya-local-control"
description: "Control Tuya / Smart Life devices locally over LAN: fetch local keys once via the Tuya cloud API, then read and write DPS with tinytuya."
---

# Tuya local control

Use when the user wants to read state or switch Tuya / Smart Life devices (plugs, bulbs, sensors, thermostats, curtain motors) from a script or local dashboard — without depending on the Tuya/Smart Life app or the cloud at runtime.

Tuya devices answer a local protocol on TCP port **6668**. To talk to them you need three things per device: its **device id**, its **local key**, and its **LAN IP**. The app keeps the local key, so you fetch it once from the Tuya cloud API and then everything runs locally.

> Only control devices you own. Local keys are per-device secrets — keep `tuya_devices.json` out of git and never paste keys into chat.

## Steps

1. **Install the library.** `pip install tinytuya`. Completion: `python -c "import tinytuya; print(tinytuya.__version__)"` prints a version.

2. **Find the device on the LAN.** Optional but the fastest way to learn the IP and the protocol version. Run `python -m tinytuya scan` (or `tinytuya.deviceScan()`), or read the device list from your router's DHCP leases. Completion: you have an IP for the device. Devices are often at a fixed DHCP lease, but the IP can change — re-check before blaming the code.

3. **Fetch device ids + local keys from the cloud (one time).** Create a free **Tuya IoT Platform** project, enable **IoT Core**, and link your Smart Life / Tuya app account to it (Devices → Link App Account). Note the project's **Access ID / Client ID** and **Access Secret / Client Secret**, plus the region (`eu`, `us`, `cn`, `in`). Put them in environment variables and run the bundled `scripts/fetch_keys.py`. Completion: `tuya_devices.json` exists and lists at least one device with a local key.

4. **Probe the device locally.** Run `scripts/local_status.py <name-or-id>`. It opens a `tinytuya.Device` with the stored id + key + IP and calls `status()`. If it fails, try the other protocol version (`3.3` vs `3.4`) — this is the single most common cause of an empty or refused response. Completion: you get a JSON blob of DPS values.

5. **Map the DPS you care about.** The `status()` JSON is a dict of numeric DPS keys to values (e.g. `"1": true`, `"20": 210`). Read the device's DPS meaning from the Tuya IoT Platform "Device Debugging" tab or by toggling the device in the app and watching which key changes. Completion: you can name the exact DPS key and value type for the function you want to drive.

6. **Write a value.** Run `scripts/local_set.py <device> <dps> <value>` (see the script header for the JSON form used to set several DPS at once). Completion: `local_status.py` shows the new value, and if it is a physical output the device actually switched.

7. **Wrap it.** Once the read + write calls are proven, put them behind whatever the user asked for: a CLI, a poll loop, a local web dashboard. Cache the device object and reuse the connection; re-read the device JSON on startup, not on every call.

## Notes and pitfalls

- **`version` matters.** Tuya devices speak protocol `3.1`, `3.3`, or `3.4`. Passing the wrong one gives an empty response or `payload error`, not a helpful message. Try each; `3.3` is the usual default.
- **Local keys rotate.** Re-pairing a device in the app, or a firmware reset, invalidates the stored key. If local calls suddenly fail while the device is online in the app, re-run the key fetch.
- **The cloud is only needed for provisioning.** After `tuya_devices.json` exists, all reads and writes are LAN-local — no internet required.
- **LAN only.** The host running the script must be on the same network as the device (no VPN isolation, no guest-network client isolation).
- **One writer at a time.** Some Tuya devices tolerate only a single local TCP session; a second client can make the first one time out.
- **Cloud API free tier.** The IoT Core free trial ties a project to one app account and expires; when it does, only the *cloud key fetch* stops working. Local control keeps working with the keys you already saved.
- Use `set_value(dps, value)` for a single DPS and `set_multiple_values({...})` for several at once; values must match the type the device expects (bool / int / str).

## Bundled scripts

- `scripts/fetch_keys.py` — read Access ID/Secret from the environment, call the cloud API, write `tuya_devices.json`.
- `scripts/local_status.py` — connect locally by device name or id and print the DPS status.
- `scripts/local_set.py` — connect locally and write one DPS (or several via a JSON argument).
