# Remote Desktop Support Security Model

Goal: let Ric view or control Tommy's **current live desktop session** from any browser, temporarily, without Ric installing software and without permanent network exposure. Headless/fresh desktop sessions do not satisfy the requirement.

## Architecture

Preferred path:

Ric browser -> temporary HTTPS outbound tunnel -> localhost Guacamole/noVNC -> localhost current-session GNOME VNC backend -> current desktop

No router port forwarding. No public listener bound directly on the ThinkPad. The ThinkPad initiates outbound TLS/WebSocket traffic to a tunnel relay.

## Defaults

- View-only by default.
- TTL required for open sessions.
- One session at a time.
- Random per-session credentials.
- Guacamole is localhost-only. GNOME current-session VNC is forced to port 1024, which Fedora Workstation does not allow for LAN ingress by default; the script refuses if firewalld allows that port.
- Cleanup is idempotent and verified.

## Threats

- Public tunnel URL leaks.
- Browser gateway misconfiguration allows unauthenticated access.
- Desktop backend remains enabled after the session.
- Container/service survives cleanup.
- Multiple sessions race and leave stale state.

## Controls

- Lock file/state file under `~/.openclaw/remote-support/`.
- `close` stops skill-owned containers/processes and clears temporary state.
- `open` refuses to proceed when an active session exists.
- `status` checks actual listeners/processes, not only state files.
- Public tunnel support uses Cloudflare Quick Tunnel. The random trycloudflare URL, Guacamole password, and generated one-click URL are password-equivalent until the session expires/closes.

## Rollback

Run:

```bash
python3 skills/remote-desktop-support/scripts/remote_support.py close
python3 skills/remote-desktop-support/scripts/remote_support.py uninstall --purge
```

Then verify:

```bash
python3 skills/remote-desktop-support/scripts/remote_support.py status
```


## Secret handling

- `session.json` is chmod `0600` and lives under `~/.openclaw/remote-support` (`0700`).
- The one-click URL embeds a Guacamole auth token and is password-equivalent. Do not log it.
- `user-mapping.xml` is `0644` because the Guacamole container must read it after mounting/copying; the parent state directory remains user-private.
- `status` redacts password-equivalent values.
