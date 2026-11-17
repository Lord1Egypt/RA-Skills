# T3 Code over Tailscale

Use this reference before configuring a headless T3 Code server for private remote access.
For a controller with several remote hosts or an SSH tunnel fallback, read `multi-machine.md` first.

## Preflight

Run on the target host:

```bash
tailscale status
tailscale ip -4
t3 --version
t3 serve --help
```

Fix Tailscale connectivity before changing T3. Confirm the installed T3 build exposes the flags used below.
Review the Tailnet ACL or grants and the installed T3 build's authentication or pairing model. A private bind address limits network exposure, but it does not decide which Tailnet users should have access.

## Choose one exposure mode

### Direct Tailnet binding

Use when clients can connect to an HTTP URL on the host's Tailnet address and chosen port:

```bash
t3 serve --no-browser --host "$(tailscale ip -4)" --port 3773 --base-dir "$HOME/.t3"
```

This binds the T3 server to the private Tailnet address. It does not configure Tailscale Serve or an HTTPS endpoint.

### Tailscale Serve

Use when the user wants Tailscale Serve HTTPS routing and the installed T3 build supports it:

```bash
t3 serve --no-browser --host 127.0.0.1 --port 3773 --base-dir "$HOME/.t3" \
  --tailscale-serve --tailscale-serve-port 443
```

Verify the published route:

```bash
tailscale serve status
```

Do not switch an existing host between these modes without confirming the client URL that must change.

## User service pattern

This pattern is for Linux systems with user-level systemd. Use the target operating system's native service manager elsewhere.

Keep machine-specific values in a local wrapper. Example `~/.local/bin/t3-code-serve`:

```bash
#!/usr/bin/env bash
set -euo pipefail

t3_bin="/absolute/path/to/t3"

exec "$t3_bin" serve \
  --no-browser \
  --host "$(tailscale ip -4)" \
  --port "${T3_PORT:-3773}" \
  --base-dir "${T3CODE_HOME:-$HOME/.t3}"
```

Example user service:

```ini
[Unit]
Description=T3 Code headless server
After=network-online.target

[Service]
Type=simple
ExecStart=%h/.local/bin/t3-code-serve
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

After writing the local files:

```bash
chmod +x "$HOME/.local/bin/t3-code-serve"
systemctl --user daemon-reload
systemctl --user enable --now t3-code.service
systemctl --user status t3-code.service --no-pager
journalctl --user -u t3-code.service -n 100 --no-pager
```

## Verify from another Tailnet node

For direct binding, retrieve the address without printing it into public logs and test the selected port:

```bash
tailnet_ip="$(ssh remote-host 'tailscale ip -4')"
curl -fsS "http://${tailnet_ip}:3773/" >/dev/null
```

For Tailscale Serve, use the HTTPS URL reported by `tailscale serve status`.

## Safety

- Keep the service on the Tailnet or loopback unless public exposure was explicitly requested and reviewed.
- Confirm the Tailnet access policy and T3 authentication boundary before treating the service as private.
- Do not put auth keys, Tailnet addresses, pairing codes, or private hostnames in a repository.
- Treat mobile wireless debugging as temporary and disable it after setup unless the user explicitly wants it left enabled.
- Do not assume a reachability failure is a routing problem. Confirm the desktop is connected to the intended T3 host and project key.
