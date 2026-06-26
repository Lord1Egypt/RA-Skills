# Manual Fallback

Use this only when the wrapper and assisted flow are insufficient or when debugging the host browser stack itself.

## Manual Start Sequence

```bash
mkdir -p "$HOME/.remote-browser-profile" "$HOME/.remote-browser-logs"
Xvfb :77 -screen 0 1600x900x24 -ac +extension RANDR
env DISPLAY=:77 x11vnc -display :77 -forever -shared -rfbport 5900 -localhost -nopw
websockify --web=/usr/share/novnc 0.0.0.0:6080 localhost:5900
env DISPLAY=:77 google-chrome \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir="$HOME/.remote-browser-profile" \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --new-window 'https://example.com'
```

If `google-chrome` is unavailable, use the detected Chromium binary.

## Health Checks

```bash
lsof -iTCP -sTCP:LISTEN -P -n | rg '5900|6080|9222'
curl -I -s http://127.0.0.1:6080/vnc.html | sed -n '1,5p'
curl -s http://127.0.0.1:9222/json/version
curl -s http://127.0.0.1:9222/json/list
```

## Remote Access Patterns

Direct LAN access when allowed:

```text
http://HOST_IP:6080/vnc.html?autoconnect=1&resize=remote
```

SSH tunnel when direct access is blocked:

```powershell
ssh -L 6080:127.0.0.1:6080 -L 9222:127.0.0.1:9222 USER@HOST_IP
```

Then open:

```text
http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=remote
http://127.0.0.1:9222/json
```

## Common Problems

### `ERR_CONNECTION_TIMED_OUT`

If the host itself can reach `HOST_IP:6080` but a Windows client on the LAN times out, the most likely cause is host firewall or network policy. Allow the port explicitly or use SSH port forwarding.

### Browser Logged In But On The Wrong Page

Before asking the user to log in again, verify whether the profile is still valid and the browser only drifted to another page. The preferred fix is to navigate back to the requested target page in the same profile.

### Existing Listeners Remain After Shutdown

Inspect active listeners and terminate leftover processes before restarting on the same ports.
