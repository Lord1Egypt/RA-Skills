# UNIHIKER M10 Connection Guide

Use this guide when the user has not connected the board or the platform-specific connection check fails. Pause programming until the connection works.

## Option A: direct USB Type-C connection

1. Connect the M10 to the computer with a data-capable USB Type-C cable.
2. Wait for the M10 menu to appear.
3. The computer should detect a virtual network adapter. The board normally uses `10.1.2.3`.
4. Verify the connection:

   ```powershell
   .\scripts\check_connection.ps1
   ```

   On macOS:

   ```bash
   bash scripts/check_connection.sh
   ```

## Option B: Wi-Fi on the same LAN

1. Connect the M10 to Wi-Fi from its system menu or Mind+.
2. Find its address under **Settings > Network** or with `ip addr` over an existing terminal connection.
3. Confirm that the computer and M10 are on the same LAN.
4. Verify the connection:

   ```powershell
   .\scripts\check_connection.ps1 -M10Host <M10-IP>
   ```

   On macOS:

   ```bash
   bash scripts/check_connection.sh --host <M10-IP>
   ```

## Option C: Mind+ remote connection

1. Open Mind+, switch to Python mode, and select UNIHIKER M10 as the controller.
2. Wait until Mind+ shows the board as online.
3. Prefer the included SSH scripts when an Agent needs to deploy generated code.

## Factory-default SSH details

| Item | Value |
|---|---|
| User | `root` |
| Password | `dfrobot` |
| Port | `22` |

If the owner changed these credentials, use the replacement provided by the owner. Do not store a user-supplied password in project files.

## Troubleshooting

| Symptom | Action |
|---|---|
| Ping fails | Check power and use a data-capable USB cable; on Wi-Fi, confirm both devices are on the same LAN. |
| Ping works but SSH fails | Wait for startup to finish, then retry or restart the M10. |
| `10.1.2.3` fails but the Wi-Fi IP works | Pass `-M10Host <Wi-Fi-IP>` on Windows or `--host <Wi-Fi-IP>` on macOS. |
| Password is rejected | Try the factory default only if it has not been changed; otherwise ask the owner for the current credential. |

After the check succeeds, detect the Python environment before generating or deploying code.
