---
name: wcs-helper-network-skill
description: SSH tunnel for China servers to access internationally blocked sites (GitHub, ClawHub, HuggingFace, arXiv, Google, YouTube). Password-auth based, one-command setup, auto-reconnect.
metadata:
  openclaw:
    tags: ["network", "proxy", "github", "china", "ssh", "tunnel", "proxychains", "autossh"]
    user-invocable: true
version: 1.0.0
---

# WCS Helper: Network Tunnel

> Access internationally blocked websites from your China-based server.

---

## When You Need This

**Scenario A — "git push keeps timing out"**
```
git push github main
# → Connection timeout
```
→ `/万重山-隧道-开启` → try push again → succeeds

**Scenario B — "npm install keeps failing for a package from GitHub"**
```
npm install some-github-package
# → network timeout
```
→ `/万重山-隧道-开启` → npm works through tunnel

**Scenario C — "HuggingFace model download is stuck"**
```
huggingface-cli download ...
# → timeout or connection reset
```
→ `/万重山-隧道-开启` → download completes through tunnel

**Scenario D — "ClawHub skill install is super slow"**
```
clawhub install author/skill
# → extremely slow, often fails
```
→ `/万重山-隧道-开启` → ClawHub installs at full speed

---

## Supported Sites

| Site | Use Case | Status |
|------|----------|--------|
| GitHub | git clone/push, npm packages | ✅ |
| ClawHub | skill install, plugin browsing | ✅ |
| HuggingFace | model downloads, datasets | ✅ |
| arXiv | research paper access | ✅ |
| Google | search, fonts, analytics | ✅ |
| YouTube | video embeds, APIs | ✅ |
| Twitter/X | social media embeds | ✅ |
| Reddit | forum access, APIs | ✅ |

---

## Prerequisites

### Required

- A **server outside China** (any VPS with SSH access)
  - Recommended: Tencent Cloud Singapore, AWS Singapore, or any international VPS
  - SSH password authentication must be enabled
- SSH password for that server
- Server's public IP address

### Recommended

- `autossh` installed on your China server (auto-restarts tunnel if it drops)
  - Install: `apt install autossh` (Debian/Ubuntu)
- `sshpass` installed (for password-based SSH)
  - Install: `apt install sshpass`

### Network Flow

```
Your China Server (autossh client)
        ↓ SSH tunnel (encrypted)
Singapore/International VPS (as SOCKS5 proxy)
        ↓
GitHub / ClawHub / HuggingFace / Google
```

---

## Setup

### 1. Get a Tunnel Server

Any international VPS works. Recommended:
- Tencent Cloud Singapore (CNY ~15/month)
- AWS Singapore Free Tier
- DigitalOcean Singapore
- Vultr Tokyo/Singapore

Requirements:
- SSH password access enabled
- Port 22 (SSH) open to China IPs

### 2. Install the Skill

```bash
npx -y clawhub install guanqi0914/wcs-helper-network-skill
```

### 3. Configure with Your Server

Send this command via Feishu private chat:

```
/万重山-隧道-配置 服务器IP SSH端口 用户名 密码
```

Example:
```
/万重山-隧道-配置 43.134.164.43 22 ubuntu myPassword123
```

### 4. Start the Tunnel

```
/万重山-隧道-开启
```

You should see: ✅ Tunnel connected

### 5. Test It

```bash
curl --socks5 127.0.0.1:1080 https://api.github.com
# Should return: HTTP 200
```

---

## All Commands

| Command | What It Does |
|---------|-------------|
| `/万重山-隧道-配置 <IP> <端口> <用户> <密码>` | Set up tunnel server credentials |
| `/万重山-隧道-开启` | Start the tunnel |
| `/万重山-隧道-关闭` | Stop the tunnel |
| `/万重山-隧道-状态` | Show tunnel connection status |
| `/万重山-隧道-测试` | Test tunnel speed |
| `/万重山-隧道-帮助` | Show help |

---

## Usage Tips

### Before Running git/npm Commands

Send `/万重山-隧道-状态` first. If you see "Tunnel: ✅", you're good. If "Tunnel: ❌", send `/万重山-隧道-开启` first.

### Tunnel Stays On Until You Close It

The tunnel runs in the background. Send `/万重山-隧道-关闭` when you don't need international access any more.

### Which Ports Are Proxied

Only TCP connections through the SOCKS5 proxy are tunneled:
- GitHub (443) ✅
- ClawHub (443) ✅
- HuggingFace (443) ✅
- Google (443) ✅

UDP traffic (some gaming, VoIP) is NOT proxied.

---

## How It Works

### Connection Process

```
1. autossh connects to your international server via SSH
   sshpass -p 'password' ssh -N -D 127.0.0.1:1080 user@server-ip

2. SSH creates encrypted tunnel

3. autossh monitors the tunnel every 30 seconds

4. If tunnel drops → autossh auto-restarts it

5. Applications use 127.0.0.1:1080 as SOCKS5 proxy
```

### Without the Tunnel (Direct Connection)

```
China Server → GitHub/ClawHub/HuggingFace
  ↓
Connection timeout / reset / very slow
```

### With the Tunnel

```
China Server → SSH Tunnel → International VPS → GitHub/ClawHub/HuggingFace
                         ↓
              Stable encrypted connection
```

---

## Performance

| Metric | Value |
|--------|-------|
| Tunnel latency | ~50-100ms (China → Singapore) |
| GitHub clone speed | 500KB/s - 5MB/s |
| ClawHub install | 1-5 seconds |
| Proxy overhead | ~5-10% bandwidth |

---

## Troubleshooting

**"Tunnel: ❌ Connection failed"**
→ Check server IP, SSH port, username, password
→ Make sure SSH password auth is enabled on your VPS

**"Tunnel connects but git push still times out"**
→ Try again — GitHub sometimes rate-limits tunnel IPs temporarily
→ If persistent, your VPS IP may be on GitHub's blacklist

**"autossh process not running after server restart"**
→ Send `/万重山-隧道-开启` to restart manually
→ Or set up systemd service (advanced — see auto-fix.sh)

**"SSH connection refused"**
→ Check if port 22 is open on your VPS firewall
→ Try SSH port 2222 if 22 is blocked

---

## Security Notes

- The tunnel only handles outbound connections from your China server
- Your VPS provider can see the traffic (GitHub, ClawHub, etc.) but NOT your China server's other traffic
- No data is stored on the VPS — only encrypted transit
- Tunnel credentials are stored locally in `~/.wcs_tunnel.conf` (chmod 600)

---

## Uninstall

```bash
# Stop tunnel
/万重山-隧道-关闭

# Remove skill files
rm -rf ~/.openclaw/workspace/skills/wcs-helper-network-skill
rm -f ~/.wcs_tunnel.conf
```
