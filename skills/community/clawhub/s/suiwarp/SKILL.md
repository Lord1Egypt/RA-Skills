---
name: suiwarp
description: Deploy S-UI + Cloudflare WARP proxy server in one command. 6 protocols (VLESS Reality, TUIC, Hysteria2, gRPC, Trojan, WebSocket), clean Cloudflare IP exit via wireproxy (~54MB RAM). Use when the user wants to set up a proxy server, VPN alternative, or network tunnel on a VPS.
license: MIT
---

# SUIWARP — S-UI + Cloudflare WARP One-Liner

Deploy a multi-protocol proxy server with clean Cloudflare IP exit on any VPS.

## When to Use

Activate when the user wants to:
- Deploy a proxy / tunnel / VPN alternative on a VPS
- Set up S-UI or sing-box with WARP
- Configure VLESS Reality, TUIC, Hysteria2, or other protocols
- Get a clean exit IP via Cloudflare WARP
- Audit or fix an existing S-UI installation

## Architecture

```
Client → S-UI (sing-box, 6 protocols) → wireproxy (SOCKS5 ~4MB) → Cloudflare WARP → Clean Exit IP
```

| Protocol | Port | Best For |
|---|---|---|
| VLESS Reality Vision | 443/tcp | Daily use (most covert) |
| TUIC v5 | 443/udp | Gaming (low latency) |
| Hysteria2 | 8443/udp | Streaming (max speed) |
| VLESS Reality gRPC | 2053/tcp | Multiplexing (stable) |
| Trojan Reality | 8880/tcp | Classic fallback |
| VLESS Reality WS | 2083/tcp | CDN/firewall bypass |
| VLESS CDN WS | 2052/tcp | IP hidden behind Cloudflare CDN |
| ShadowTLS v3 + SS2022 | 9443/tcp | Anti-DPI stealth (looks like real TLS) |
| VLESS HTTPUpgrade | 10443/tcp | Stealth HTTP transport with Reality |
| Hysteria2 Port Hopping | 20000-40000/udp | Anti-QoS, port randomization |

## Deployment

### One-Liner (Recommended)

SSH into the target server as root, then run:

```bash
bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/setup.sh)
```

This handles everything automatically:
1. System dependencies + swap (for low-RAM VPS)
2. S-UI installation with 6 protocol inbounds
3. Reality keypair generation
4. Free Cloudflare WARP registration via wgcf
5. wireproxy setup (WireGuard → SOCKS5, ~4MB RAM)
6. S-UI outbound routing through WARP
7. UFW firewall configuration
8. Client link generation

### Remote Deployment via SSH

If the user provides server credentials, deploy remotely:

```bash
ssh root@SERVER_IP 'bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/setup.sh)'
```

For password-only servers:
```bash
sshpass -p 'PASSWORD' ssh -o StrictHostKeyChecking=no root@SERVER_IP \
  'bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/setup.sh)'
```

## Requirements

- **OS:** Ubuntu 20.04+ / Debian 11+ (x86_64 or ARM64)
- **RAM:** 1GB minimum (512MB usable after OS)
- **Access:** Root SSH

## Post-Deploy

After setup completes:

1. **Client links** are at `/root/suiwarp-client-links.txt`
2. **S-UI panel** is at `http://SERVER_IP:2095/app/` (default: admin/admin — remind user to change!)
3. **Subscription URL** is at `http://SERVER_IP:2096/sub/`

### Verify WARP

```bash
# Direct IP
curl ifconfig.me

# WARP exit IP (should be Cloudflare)
curl -x socks5h://127.0.0.1:40000 ifconfig.me
```

## Troubleshooting

### sing-box won't start

Check logs: `journalctl -u s-ui -n 20`

Common causes:
- **`out_json` type mismatch**: If DB was manually edited, `out_json` column must be blob (bytes), not string. Fix with Python:
  ```python
  cur.execute("UPDATE inbounds SET out_json=? WHERE id=?", (json.dumps(data).encode("utf-8"), rid))
  ```
- **`outbound type not found: wireguard`**: S-UI 1.4.0 sing-box doesn't include WireGuard. Use the wireproxy SOCKS5 approach instead.

### WARP not connecting

```bash
systemctl status wireproxy-warp
journalctl -u wireproxy-warp -n 20
```

If endpoint is unreachable, try alternative WARP endpoints:
- `engage.cloudflareclient.com:2408`
- `162.159.193.1:2408`
- `162.159.195.1:2408`

### Firewall blocking ports

```bash
ufw status numbered
# Ensure 443/tcp, 443/udp, 8443/udp, 2053/tcp, 8880/tcp, 2083/tcp are ALLOW
```

### OOM kills (low RAM servers)

```bash
# Check swap
free -h
# If no swap, create one
fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
```

## Uninstall

```bash
bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/uninstall.sh)
```

## Service Management

```bash
systemctl status s-ui              # S-UI status
systemctl status wireproxy-warp    # WARP status
systemctl restart s-ui             # Restart proxy
systemctl restart wireproxy-warp   # Restart WARP tunnel
journalctl -u s-ui -f              # Live S-UI logs
journalctl -u wireproxy-warp -f    # Live WARP logs
```

## Key Paths

| Path | Description |
|---|---|
| `/usr/local/s-ui/db/s-ui.db` | S-UI SQLite database |
| `/usr/local/s-ui/sui` | S-UI binary |
| `/etc/wireproxy.conf` | wireproxy WireGuard config |
| `/etc/suiwarp/wgcf-account.toml` | WARP account credentials |
| `/root/suiwarp-client-links.txt` | Generated client links |

## Credits

[S-UI](https://github.com/alireza0/s-ui) |
[sing-box](https://github.com/SagerNet/sing-box) |
[wireproxy](https://github.com/pufferffish/wireproxy) |
[wgcf](https://github.com/ViRb3/wgcf)
