# Network Tunnel — Access Internationally Blocked Sites from China

Access GitHub, ClawHub, HuggingFace, Google, YouTube, and 200+ other internationally blocked sites from your China server — by routing traffic through your own overseas cloud server.

## Prerequisites

You need:
1. **An overseas cloud server** (VPS in Singapore, Tokyo, US, HK — any provider)
2. **SSH access** to that server (username + password OR SSH key)
3. **Linux** (Ubuntu 20.04+ recommended)

Cost: ~$5–10/month for a basic Singapore VPS (Alibaba Cloud international, AWS Singapore, Vultr Tokyo, etc.)

## Quick Start

### Install
```bash
npx -y clawhub install guanqi0914/wcs-helper-network-skill
```

### Configure (30 seconds, interactive)
```bash
bash ~/.openclaw/skills/wcs-helper-network-skill/scripts/connect.sh setup
```
You'll be asked for: server IP, SSH port, username, and password.

### Connect
```bash
bash ~/.openclaw/skills/wcs-helper-network-skill/scripts/connect.sh connect
```

### Verify
```bash
bash ~/.openclaw/skills/wcs-helper-network-skill/scripts/connect.sh status
```
Look for `autossh ✅` and `GitHub API ✅`.

## Common Tasks

```bash
# Route git through tunnel (GitHub auto-detected)
sg-git.sh clone https://github.com/user/repo
sg-git.sh push

# Route curl through tunnel
sg-curl.sh https://api.github.com/

# Route any command through tunnel
sg-bash.sh "pip install torch"
sg-bash.sh "npm install express"

# Check tunnel status
connect.sh status

# Stop tunnel
connect.sh disconnect
```

## Environment Variables (for automation/CI)

```bash
export TUNNEL_HOST=YOUR_SERVER_IP
export TUNNEL_USER=ubuntu
export TUNNEL_PASS=your_password
export TUNNEL_PORT=22

connect.sh connect   # no interaction needed
```

## Supported Services

These are automatically routed through the tunnel:

| Category | Examples |
|----------|---------|
| **GitHub** | `git clone`, `git push`, API |
| **AI Platforms** | OpenAI, Anthropic, HuggingFace, arXiv |
| **Developer Tools** | npm, PyPI, Stack Overflow, ClawHub |
| **Cloud Platforms** | AWS, Google Cloud, Cloudflare |
| **Search & Reference** | Google, Google Scholar, Wikipedia |
| **Social & Media** | YouTube, Twitter/X, Telegram, Discord |

**NOT proxied** (go direct from China): Baidu, Alibaba, Tencent, ByteDance, Bilibili, Zhihu, WeChat, etc.

## Domain Routing

Add a blocked site to the proxy list:
```bash
sg-add-domain.sh proxy new-blocked-site.com
```

Add a site to bypass the proxy (go direct):
```bash
sg-add-domain.sh direct my-china-site.cn
```

View current routing rules:
```bash
sg-route.sh list
```

## Auto-start on Boot

```bash
connect.sh install-service
```

This creates a systemd service that automatically reconnects the tunnel after server reboot.

## File Structure

```
~/.openclaw/skills/wcs-helper-network-skill/
├── SKILL.md              # Full documentation
├── README.md             # This file
├── scripts/
│   ├── connect.sh         # Tunnel management (connect/disconnect/status)
│   ├── sg-curl.sh         # Route curl through tunnel
│   ├── sg-git.sh          # Route git through tunnel (auto-detects GitHub)
│   ├── sg-bash.sh         # Route any command through tunnel
│   ├── sg-proxychains.sh  # Smart routing with proxychains4
│   ├── sg-route.sh        # View / manage routing rules
│   ├── auto-route.sh      # Auto-detect and add blocked domains
│   └── add-domain.sh      # Add/remove domains from routing lists
└── config/
    ├── proxychains.conf    # proxychains4 configuration
    ├── routes.conf        # Direct-connect domains (China-reachable)
    └── proxy-routes.conf  # Proxy-route domains (200+ blocked sites)
```

## Troubleshooting

**Tunnel won't connect?**
```bash
# Test SSH manually first
sshpass -p 'YOUR_PASSWORD' ssh ubuntu@YOUR_SERVER_IP -p 22

# Check if port 1080 is listening
nc -zv 127.0.0.1 1080
```

**GitHub still times out?**
```bash
# Verify tunnel is working
sg-curl.sh https://api.github.com/

# Check if GitHub is in the proxy routes
grep "github.com" config/proxy-routes.conf
```

For full documentation, see `SKILL.md`.
