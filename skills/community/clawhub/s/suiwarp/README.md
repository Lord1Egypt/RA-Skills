# S-UIWARP

**S-UI + Cloudflare WARP in one command.** Deploy a multi-protocol proxy server with clean Cloudflare IP exit in under 2 minutes.

```bash
bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/setup.sh)
```

## What It Does

SUIWARP automates the entire setup of a production-ready proxy server:

1. **Installs [S-UI](https://github.com/alireza0/s-ui)** — sing-box management panel with 6 proxy protocols
2. **Registers free Cloudflare WARP** — via [wgcf](https://github.com/ViRb3/wgcf)
3. **Routes traffic through WARP** — via [wireproxy](https://github.com/pufferffish/wireproxy) (userspace WireGuard, ~4MB RAM)
4. **Configures firewall, swap, DNS** — hardened and OOM-proof

## Architecture

```
Client ──→ Your Server (S-UI / sing-box)
               │
               ├─ VLESS Reality Vision  :443/tcp   ← daily driver
               ├─ TUIC v5              :443/udp   ← low latency
               ├─ Hysteria2            :8443/udp  ← max speed
               ├─ VLESS Reality gRPC   :2053/tcp  ← multiplexed
               ├─ Trojan Reality       :8880/tcp  ← classic
               ├─ VLESS Reality WS     :2083/tcp  ← CDN compatible
               ├─ VLESS CDN WS         :2052/tcp  ← CF CDN relay (IP hidden)
               ├─ ShadowTLS v3+SS2022  :9443/tcp  ← anti-DPI (stealth)
               ├─ VLESS HTTPUpgrade    :10443/tcp ← stealth HTTP
               └─ Hysteria2 PortHop    :20000-40000/udp ← anti-QoS
                       │
                       ▼
             wireproxy (SOCKS5, ~4MB)
                       │
                       ▼
             Cloudflare WARP (free)
                       │
                       ▼
             Exit IP: Cloudflare (AS13335)
```

## Why WARP?

| Without WARP | With WARP |
|---|---|
| VPS datacenter IP exposed | Cloudflare clean IP as exit |
| IP easily flagged/blocked | High-reputation IP range |
| Direct attribution to VPS | Traffic blends with Cloudflare CDN |
| Single point of failure | Cloudflare's global network |

## Requirements

- **OS:** Ubuntu 20.04+ / Debian 11+ (x86_64 or ARM64)
- **RAM:** 1GB minimum (512MB usable after OS)
- **Access:** Root SSH

## Quick Start

### 1. Deploy

```bash
bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/setup.sh)
```

### 2. Get Client Links

After installation, find your client links at:

```bash
cat /root/suiwarp-client-links.txt
```

Or visit the S-UI panel:
```
http://YOUR_IP:2095/app/
Default: admin / admin  ← change immediately!
```

### 3. Connect

Import the links into your preferred client:

| Platform | Recommended Client |
|---|---|
| Windows | [v2rayN](https://github.com/2dust/v2rayN) |
| macOS | [V2Box](https://apps.apple.com/app/id6446814690) |
| iOS | [Shadowrocket](https://apps.apple.com/app/id932747118), [Stash](https://apps.apple.com/app/id1596063349) |
| Android | [v2rayNG](https://github.com/2dust/v2rayNG), [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid) |
| Linux | [nekoray](https://github.com/MatsuriDayo/nekoray) |

## Protocols

| # | Protocol | Port | Transport | Best For |
|---|---|---|---|---|
| 1 | VLESS Reality Vision | 443/tcp | TCP | Daily use (most covert) |
| 2 | TUIC v5 | 443/udp | QUIC | Gaming (low latency) |
| 3 | Hysteria2 | 8443/udp | QUIC | Streaming (max speed) |
| 4 | VLESS Reality gRPC | 2053/tcp | gRPC | Multiplexing (stable) |
| 5 | Trojan Reality | 8880/tcp | TCP | Classic fallback |
| 6 | VLESS Reality WS | 2083/tcp | WebSocket | CDN/firewall bypass |
| 7 | **VLESS CDN WS** | 2052/tcp | WS + CF CDN | **IP hidden behind Cloudflare** |
| 8 | **ShadowTLS v3 + SS2022** | 9443/tcp | ShadowTLS | **Anti-DPI, looks like normal TLS** |
| 9 | **VLESS HTTPUpgrade** | 10443/tcp | HTTPUpgrade + Reality | **Stealth HTTP, lighter than WS** |
| 10 | **Hysteria2 Port Hopping** | 20000-40000/udp | QUIC | **Anti-QoS, port randomization** |

### CDN Relay (Protocol 7)

Hides your server IP behind Cloudflare CDN. Even if the VPS IP is blocked, the CDN relay still works.

**Setup:** Add a Cloudflare DNS A record pointing to your server (Proxied/orange cloud), then use the generated link with your CF domain.

### ShadowTLS v3 (Protocol 8)

Performs a **real TLS handshake** with a legitimate site (e.g., `www.microsoft.com`), making traffic indistinguishable from normal HTTPS. The most DPI-resistant protocol available.

**Client:** Requires sing-box based clients (NekoBox, sing-box CLI). Config saved to `/root/suiwarp-extra-links.txt`.

### VLESS HTTPUpgrade (Protocol 9)

Lighter than WebSocket — uses HTTP Upgrade mechanism with Reality TLS. Lower overhead, harder to fingerprint than standard WS.

### Hysteria2 Port Hopping (Protocol 10)

Server uses iptables DNAT to redirect UDP ports 20000-40000 to the Hysteria2 listener. Client randomly hops between ports, defeating QoS throttling and port-based blocking.

### ECH (Encrypted Client Hello)

Cloudflare automatically enables ECH for proxied domains. When using CDN relay (Protocol 7) with `sw.your-domain.com`, SNI is encrypted end-to-end on supported clients (Chrome 130+, Firefox 128+). No server config needed.

## Resource Usage

| Component | RAM | Description |
|---|---|---|
| S-UI (sing-box) | ~50MB | Panel + 8 protocol inbounds |
| sing-box (extra) | ~6MB | ShadowTLS v3 + HTTPUpgrade |
| wireproxy | ~4MB | WARP tunnel |
| **Total** | **~60MB** | Fits on 512MB VPS |

## Management

```bash
# Service status
systemctl status s-ui
systemctl status wireproxy-warp

# View logs
journalctl -u s-ui -f
journalctl -u wireproxy-warp -f

# Restart services
systemctl restart s-ui
systemctl restart wireproxy-warp

# Check WARP exit IP
curl -x socks5h://127.0.0.1:40000 ifconfig.me

# Check direct IP
curl ifconfig.me
```

## Uninstall

```bash
bash <(curl -sL https://raw.githubusercontent.com/iPythoning/SUIWARP/main/uninstall.sh)
```

Or if you have the repo cloned:

```bash
bash uninstall.sh
```

## How It Works

The key insight is using **wireproxy** — a userspace WireGuard implementation that exposes a local SOCKS5 proxy. This avoids:

- Kernel WireGuard module dependency
- TUN device permissions
- sing-box WireGuard compilation flags
- Heavy `warp-cli` daemon (~100MB RAM)

Instead, wireproxy runs a ~4MB process that tunnels traffic through Cloudflare WARP and exposes `127.0.0.1:40000` as a SOCKS5 proxy. S-UI's sing-box is configured to route all outbound traffic through this SOCKS5 proxy, making all client traffic exit through Cloudflare's network.

## Firewall Ports

| Port | Protocol | Service |
|---|---|---|
| 443/tcp | TCP | VLESS Reality Vision |
| 443/udp | UDP | TUIC v5 |
| 8443/udp | UDP | Hysteria2 |
| 2053/tcp | TCP | VLESS Reality gRPC |
| 8880/tcp | TCP | Trojan Reality |
| 2083/tcp | TCP | VLESS Reality WS |
| 2052/tcp | TCP | VLESS CDN WS (CF relay) |
| 9443/tcp | TCP | ShadowTLS v3 + SS2022 |
| 10443/tcp | TCP | VLESS HTTPUpgrade |
| 20000-40000/udp | UDP | Hysteria2 Port Hopping |
| 2095/tcp | TCP | S-UI Panel |
| 2096/tcp | TCP | Subscription Server |

## Credits

- [S-UI](https://github.com/alireza0/s-ui) — sing-box web panel
- [sing-box](https://github.com/SagerNet/sing-box) — universal proxy platform
- [wireproxy](https://github.com/pufferffish/wireproxy) — userspace WireGuard proxy
- [wgcf](https://github.com/ViRb3/wgcf) — Cloudflare WARP config generator

## License

[MIT](LICENSE)
