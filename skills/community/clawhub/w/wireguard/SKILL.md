---
name: WireGuard
description: Configure WireGuard VPN tunnels with secure routing and key management.
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["wg"]},"os":["linux","darwin","win32"]}}
---

## AllowedIPs Traps (Most Common Mistakes)
- `AllowedIPs` means different things on each side — server: what peer CAN send; client: what to ROUTE through tunnel
- `0.0.0.0/0` routes ALL traffic including tunnel endpoint — breaks connectivity, must exclude server's public IP first
- Overlapping AllowedIPs between peers = undefined routing — each IP range must belong to exactly one peer
- Wrong mask silently breaks routing — `/32` for single host, `/24` for subnet, verify carefully

## Connection Failures
- No handshake = wrong public key, firewall blocking UDP, or wrong endpoint — check all three, not just one
- One-way traffic = AllowedIPs misconfigured — packets go out but replies don't route back
- Missing `PersistentKeepalive = 25` breaks NAT traversal — peer behind NAT unreachable after ~2 minutes
- Config file permissions must be 600 — wg-quick silently refuses to start with loose permissions

## DNS Leaks
- Without `DNS =` in client config, DNS queries bypass tunnel — leaks real IP to DNS provider
- Full tunnel (`0.0.0.0/0`) without DNS config = false sense of security — traffic tunneled but DNS exposed

## Routing Setup
- IP forwarding disabled by default on Linux — tunnel works but packets don't route between interfaces
- NAT required for internet access through tunnel — without masquerade, return packets don't find their way
- Firewall must allow UDP on ListenPort — WireGuard is UDP only, no TCP fallback exists

## Key Security
- Private key file permissions matter — world-readable key is compromised, set 600 immediately after generation
- Never transmit private keys — generate on each machine, exchange only public keys
- Config files contain private keys — treat wg0.conf as secret, not just privatekey file

## Live Changes
- Adding peers requires interface reload on most setups — or use `wg set` for live changes without dropping connections
- `wg syncconf` applies changes without restart — but config file format differs from wg.conf (use `wg-quick strip`)

## Debugging
- `wg show` displays handshake timestamps — stale handshake (>2 min) means connection dead despite interface up
- Handshake happens on first packet — no traffic = no handshake attempt, ping to test
