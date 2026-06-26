# LAN-restricted browser terminal pattern

Use this pattern when the human opens the temporary terminal from another trusted machine on the same local network.

## Safe flow

1. identify the trusted client IP
2. launch the web terminal on the server LAN IP or another intended internal bind address
3. restrict access to that single client IP and that single port when the firewall supports it
4. send the connection details only to the intended human
5. remove or expire the temporary access path after the task

## Documentation-only example

If the server is `192.0.2.10`, the client is `192.0.2.20`, and the temporary frontend port is `48080`:

Allow:

```bash
sudo ufw allow from 192.0.2.20 to any port 48080 proto tcp
```

Remove later:

```bash
sudo ufw delete allow from 192.0.2.20 to any port 48080 proto tcp
```

Treat these addresses as placeholders. Replace them with the real server IP, trusted client IP, and chosen port.

## Guardrails

- Restrict to one trusted client IP only when possible.
- Do not open the port to `Anywhere` unless the human explicitly accepts that risk.
- Keep the access material temporary.
- Prefer TTL-based cleanup even when a manual delete rule is shown.
- Do not create external tunnels or public reverse proxy exposure as part of this pattern.
