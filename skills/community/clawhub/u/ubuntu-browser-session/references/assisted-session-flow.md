# Assisted Session Flow

The assisted flow is a bounded manual takeover on top of the same durable browser profile the agent will later reuse.

It is not meant to be the primary day-to-day interaction model. It is the exception path for:

- first login
- expired sessions
- challenges that cannot be cleared automatically

## Current Flow

1. Wrapper resolves the site profile and starts or reuses the GUI runtime
2. Wrapper checks whether the current page is:
   - the requested target page
   - a wrong-page drift that can be auto-corrected
   - a real login wall or challenge
3. If local recovery is exhausted, `assisted-session.sh start` exposes the same live browser through noVNC
4. User completes the blocked step and leaves the final target page loaded
5. `assisted-session.sh capture` writes:
   - the exact manifest
   - the site session registry entry
   - compatibility identity aliases for Google-family hosts

## Access URLs

`assisted-session.sh status` now reports both:

- `novnc_url`: loopback URL for SSH tunnel use
- `lan_novnc_url`: direct LAN URL when the host IP is known

Examples:

```text
http://127.0.0.1:6084/vnc.html?autoconnect=1&resize=remote
http://192.168.0.200:6084/vnc.html?autoconnect=1&resize=remote
```

Use the loopback URL if you are forwarding ports over SSH from Windows or another remote machine.

Use the LAN URL only when firewall and network policy allow direct access.

## Commands

The wrapper is the supported entrypoint. Direct `assisted-session.sh` commands are for the bounded handoff after `open-protected-page.sh` has already selected the site profile and exposed noVNC.

```bash
scripts/assisted-session.sh start --url 'https://target.example' --origin 'https://target.example' --session-key default
scripts/assisted-session.sh status --origin 'https://target.example' --session-key default
scripts/assisted-session.sh capture --origin 'https://target.example' --session-key default
scripts/assisted-session.sh stop --origin 'https://target.example' --session-key default
```

## Important Rule

The user should not be asked to intervene merely because the browser is on the wrong page.

The wrapper should first try to return the same logged-in profile to the requested target page automatically.

Manual takeover should happen only when the target still lands on:

- a login wall
- a challenge page
- another unrecoverable blocked state
