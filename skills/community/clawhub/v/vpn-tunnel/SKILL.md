---
name: vpn-tunnel
description: |
  VPN tunnel for accessing foreign websites (Google, GitHub, Docker Hub, etc.)
  through a cloud VPS (47.85.45.122) via WireGuard + SOCKS5 proxy.
  Use when: (1) Need to access foreign/international websites blocked in China,
  (2) Need to pull Docker images from Docker Hub, (3) Need to access Google,
  GitHub or other overseas APIs/services that are unreachable via direct connection,
  (4) User asks to "use VPN", "connect to VPN", "change IP", or "access international sites".
  ⚠️ CRITICAL: Only use this for overseas/international sites. Do NOT use for
  domestic/China-accessible sites (GitHub is often directly reachable and faster).
  Always close the tunnel immediately after use.
---

# VPN Tunnel Skill

On-demand WireGuard VPN tunnel to cloud VPS (47.85.45.122 "大锤") + SSH SOCKS5 proxy
for accessing foreign websites blocked in China.

## ⚠️ CRITICAL RULES

1. **Only for overseas/blocked sites** — Google, Docker Hub, etc. Never use for
   domestic sites or sites directly reachable from China.
2. **Open → Use → Close immediately** — Never leave the tunnel running.
3. **Do NOT modify local network routes** — VPN only carries explicit proxy traffic.
4. **Local routes always take priority** — Normal internet traffic stays on local NICs.

## Speed Reference (tested 2026-06-19)

| Site | Direct | VPN | Verdict |
|------|--------|-----|---------|
| Google | ❌ blocked | ✅ 1.5s / ~50KB/s | Use VPN |
| Docker Hub | ❌ blocked | ✅ 6.2s / ~73KB/s | Use VPN |
| GitHub | ✅ 1.0s / 545KB/s | 5.6s / 100KB/s | Prefer direct |
| PyPI | ✅ 0.3s / 68KB/s | 1.1s / 21KB/s | Prefer direct |

**Rule of thumb**: If a site is directly reachable (non-zero HTTP status with acceptable speed),
use direct connection. Only fall back to VPN when direct connection fails or times out.

## Usage

### Start

```bash
bash ~/.openclaw/skills/vpn-tunnel/scripts/vpn-up.sh
```

With auto-test:
```bash
bash ~/.openclaw/skills/vpn-tunnel/scripts/vpn-up.sh --test
```

### Access overseas sites via proxy

```bash
curl --proxy socks5h://127.0.0.1:1080 <url>
```

For web_fetch tool unavailable on overseas sites, use exec+curl:
```bash
curl -s --max-time 15 --proxy socks5h://127.0.0.1:1080 <url>
```

### Check status

```bash
bash ~/.openclaw/skills/vpn-tunnel/scripts/vpn-status.sh
```

### Close (MANDATORY after use)

```bash
bash ~/.openclaw/skills/vpn-tunnel/scripts/vpn-down.sh
```

## Architecture

```
Local machine → WireGuard (10.0.0.3) → Cloud VPS (10.0.0.1)
                                    → SSH SOCKS5 (127.0.0.1:1080)
                                    → Internet (exit IP: 47.85.45.122)
```

## Configuration

| Item | Value |
|------|-------|
| Cloud VPS | 47.85.45.122 |
| WireGuard port | UDP 51820 |
| VPN subnet | 10.0.0.0/24 |
| Local VPN IP | 10.0.0.3 |
| Server VPN IP | 10.0.0.1 |
| SOCKS5 proxy | 127.0.0.1:1080 |
| SSH user | smile |
| WireGuard config | /etc/wireguard/wg0.conf |

## Decision Flow

```
Need to access a URL?
  ├─ Is it domestic / directly reachable? → Use direct connection
  ├─ Is it blocked / overseas-only? → Start VPN, access, close VPN
  └─ After VPN access is done → IMMEDIATELY close VPN
```
