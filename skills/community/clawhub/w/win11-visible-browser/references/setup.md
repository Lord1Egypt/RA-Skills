# Setup reference — Win11 visible browser from WSL2/OpenClaw

Use this reference for implementation details after the `win11-visible-browser` skill has triggered.

## Architecture

```text
OpenClaw Gateway in WSL2
  → browser profile (example: win-edge)
  → http://WINDOWS_WSL_GATEWAY_IP:9223
  → Windows relay/portproxy
  → 127.0.0.1:9222
  → visible Windows 11 Edge/Chrome profile
```

## Recommended defaults

These are examples, not required values:

| Item | Example |
|---|---|
| OpenClaw profile | `win-edge` |
| Browser | Microsoft Edge or Google Chrome |
| Dedicated profile | `C:\ProgramData\OpenClaw\browser-profile` |
| Windows local CDP | `127.0.0.1:9222` |
| WSL-visible relay | `WINDOWS_WSL_GATEWAY_IP:9223` |
| Startup task | `OpenClaw-Start-Windows-Browser-CDP` |
| Log | `C:\ProgramData\OpenClaw\logs\browser-cdp-startup.log` |

Prefer a dedicated browser profile for safety. Use a personal browser profile only after explicit user approval.

## Read-only diagnostics

From WSL:

```bash
openclaw browser profiles
openclaw browser --browser-profile win-edge doctor
WIN_IP=$(ip route | awk '/default/ {print $3; exit}')
curl -sS --max-time 5 "http://$WIN_IP:9223/json/version"
curl -sS --max-time 5 "http://$WIN_IP:9223/json/list"
```

From Windows PowerShell:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:9222/json/version'
Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:9223/json/version'
netsh interface portproxy show v4tov4
netstat -ano | Select-String ':9222|:9223'
```

## OpenClaw browser config shape

Example:

```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "win-edge",
    "profiles": {
      "win-edge": {
        "cdpUrl": "http://WINDOWS_WSL_GATEWAY_IP:9223",
        "attachOnly": true,
        "color": "#00AA00"
      }
    }
  }
}
```

If the Windows gateway IP changes, update `cdpUrl` or use a repair flow that recomputes it.

## Windows repair script template

The bundled script is:

```text
{baseDir}/scripts/start-win11-browser-cdp-for-openclaw.ps1
```

Before using it, review:

- Edge/Chrome executable path;
- profile directory;
- local CDP port;
- relay port;
- firewall rule name;
- whether the firewall remote address is restricted to WSL/Hyper-V CIDR.

Run elevated PowerShell when changing portproxy/firewall/task state.

## Security model

CDP is a powerful browser control interface. Treat it like remote control of the browser profile.

Rules:

- Do not expose CDP to LAN/Internet.
- Keep Windows firewall scoped to WSL/Hyper-V CIDR.
- Prefer a dedicated browser profile.
- Do not use a personal/logged-in browser profile without explicit user approval.
- Do not send forms, messages, purchases, or account actions without explicit user approval.
- Keep the browser visible so the user can audit and intervene.
- Stop and ask for manual help for login, captcha, 2FA, payment, or sensitive consent.

ClawScan checklist before repair or publication:

- Dedicated profile remains the documented default.
- Personal profile use is gated by explicit approval.
- Firewall `RemoteAddress` is restricted to the current WSL/Hyper-V CIDR.
- CDP relay is not exposed to LAN or Internet.
- Scheduled Task creation is optional, approval-gated, and has `Unregister-ScheduledTask` rollback.

## Rollback

OpenClaw rollback depends on how config was changed. Typical options:

```bash
openclaw config get browser
```

Then use the supported OpenClaw configuration mechanism for the current installation (prefer the first-class Gateway config tool when available) to restore the previous `browser.defaultProfile` or browser profile block. Do not guess CLI config commands on an unfamiliar host.

Windows rollback examples:

```powershell
Unregister-ScheduledTask -TaskName 'OpenClaw-Start-Windows-Browser-CDP' -Confirm:$false
netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9223
Remove-NetFirewallRule -DisplayName 'OpenClaw Browser CDP relay 9223 from WSL'
```

Close dedicated browser profile processes before deleting the profile directory.
