---
name: remote-desktop-support
description: "Linux/Fedora-GNOME-first, early but safety-tested skill for short-lived browser-based remote desktop support links using local-only VNC/Guacamole and outbound tunnels."
allowed-tools: ["exec", "read", "write"]
user-invocable: true
metadata:
  openclaw:
    os: ["linux"]
    requires:
      bins: ["python3", "podman"]
---

# Remote Desktop Support

Use when Ric asks for temporary browser-based access to this machine's desktop for troubleshooting.

## Safety Contract

- Default to **preflight/status** unless Ric explicitly asks to open access.
- Never create permanent inbound firewall/router exposure.
- Bind Guacamole to `127.0.0.1`; public access must be via a short-lived outbound tunnel. GNOME current-session VNC may bind widely, so it must use a firewalld-blocked port (`1024`) and pass the script safety check.
- **Hard requirement:** access must show the current live desktop session. Do not use headless/fresh desktop sessions as a substitute.
- Default mode is `view-only`; keyboard/mouse control requires explicit wording like "control".
- Every open session must have a TTL and cleanup path.
- Do not leave credentials, tunnels, current-session GNOME VNC backend, or containers running after close.
- Do not run `install`, `open`, or `uninstall --purge` from ambiguous/unauthorized group chatter.

## Commands

Run scripts from this skill directory:

```bash
python3 {baseDir}/scripts/remote_support.py preflight
python3 {baseDir}/scripts/remote_support.py status
python3 {baseDir}/scripts/remote_support.py install --dry-run
python3 {baseDir}/scripts/remote_support.py open --ttl 10m --mode view-only --dry-run
python3 {baseDir}/scripts/remote_support.py open --ttl 10m --mode view-only --unlock-current-session --one-click-only
python3 {baseDir}/scripts/remote_support.py link
python3 {baseDir}/scripts/remote_support.py close
python3 {baseDir}/scripts/remote_support.py uninstall --dry-run
```

`open` must prove the backend is the current live desktop before exposing a public tunnel. Headless RDP/Xvfb-style fresh sessions are blockers, not acceptable fallbacks. If the current session is locked, `open` refuses unless Ric explicitly approved `--unlock-current-session`.

## Workflow

1. Run `preflight` and inspect missing dependencies / risks.
2. If Ric approves setup, run `install --dry-run`, then install only missing local assets.
3. Run `status` before any open attempt.
4. Open with a short TTL, view-only unless Ric asked for control.
5. In Discord, use `--one-click-only` and send only the `one_click_url`; it embeds a short-lived Guacamole token, so treat it like a password.
6. On completion or expiry, run `close` and verify `status` reports closed.

See `references/security-model.md` for the threat model and rollback rules.
