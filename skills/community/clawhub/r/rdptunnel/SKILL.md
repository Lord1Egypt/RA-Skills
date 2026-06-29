---
name: rdptunnel
version: 4.9.23
description: Expose local RDP (Remote Desktop) servers to the public internet via aitun TCP tunnel. Uses the AITUN/1 plain-TCP handshake (v4.9.22+) so multiple subdomains share a single public port 3389 without TLS. Perfect for AI agents that need to provide remote desktop access to Windows machines, GUI servers, or VDI instances behind NAT/firewall.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "💻"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/rdptunnel
---

# RDP Tunnel - Remote Desktop Access via Aitun TCP Forwarding

## When to Use

Use this skill when:
- You need to access a remote Windows desktop that is behind NAT, firewall, or a private network
- You want to expose a local RDP server so a colleague or client can connect remotely via Remote Desktop
- You are running a Windows VM or VDI instance with no public IP and need to make it reachable
- You want to provide temporary remote desktop access for support, training, or demonstration
- You need to connect to a home Windows PC or workstation from another location
- You want to access a Linux machine running xrdp or a VNC-to-RDP gateway
- You need to remotely manage a GUI application that cannot be accessed via SSH

Do NOT use this skill when:
- The RDP server already has a public IP and is directly reachable
- You only need command-line access (use sshtunnel instead)
- You want to expose an HTTP service (use aitun-tunnel instead)

## Instructions

### Step 1: Install aitun (v4.9.22 or later)

The AITUN/1 plain-TCP handshake used for RDP routing was introduced in v4.9.22. Make sure both the tunnel-host side and the connecting-client side run v4.9.22+ (v4.9.23 recommended — it prints smart per-port connection hints).

```bash
pip install aitun
```

Or install via one-line script (Linux/macOS):
```bash
curl -fsSL https://aitun.cc/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://aitun.cc/install.ps1 | iex
```

Verify version:
```bash
aitun --help | head -1
# Expected: Tunnel Client v4.9.23 (Relay + HTTP-Port + TCP + Subdomain)
```

### Step 2: Ensure RDP server is running locally

Verify the local RDP service is running and accessible:

**On Windows:**

```powershell
# Check if Remote Desktop is enabled (0 = enabled, 1 = disabled)
Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections

# Enable Remote Desktop if needed
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections -Value 0

# Ensure the RDP service is running
Get-Service -Name TermService | Start-Service

# Verify it is listening on port 3389
Get-NetTCPConnection -State Listen | Where-Object LocalPort -eq 3389
```

**On Linux (xrdp):**

```bash
# Install xrdp
sudo apt install xrdp -y    # Debian/Ubuntu
sudo yum install xrdp -y    # CentOS/RHEL

# Start xrdp service
sudo systemctl start xrdp
sudo systemctl enable xrdp

# Verify it is listening on port 3389
ss -tlnp | grep :3389
```

### Step 3: Create a TCP tunnel for RDP

RDP uses TCP port 3389 by default. On the **machine running the RDP server**, start aitun with `--tcp-ports 3389`. TCP forwarding requires an auth token (register at https://aitun.cc):

```powershell
# On the RDP server machine (e.g. Windows PC you want to access remotely)
C:\aitun-client-windows-amd64.exe -k YOUR_TOKEN --tcp-ports 3389
```

Or with SSH alongside RDP:

```powershell
C:\aitun-client-windows-amd64.exe -k YOUR_TOKEN --tcp-ports 22,3389
```

The output (v4.9.23+) includes smart per-port connection hints:

```
  Tunnel Client v4.9.23 (Relay + HTTP-Port + TCP + Subdomain)
  ...
  [TCP] tcp-3389 -> localhost:3389 (subdomain: yourname.aitun.cc:3389)
        LAN connect:     mstsc /v:<local-ip>:3389   (or just mstsc /v:<hostname>)
        Public connect:  aitun tcp-proxy -l 13389 yourname.aitun.cc 3389
                         mstsc /v:127.0.0.1:13389   (in another terminal)
```

If port 3389 is occupied on the server (another subdomain already claimed it), aitun automatically assigns a port from the 7000-7999 range and prints a `[Port conflict, fell back to range port]` notice. Use whichever public port aitun reports.

### Step 4: Connect from a remote machine

There are two ways to connect, depending on where you are relative to the RDP server.

#### A) LAN access (same network as the RDP server)

If your client machine is on the same LAN as the RDP server, you don't need aitun at all — connect directly:

**Windows:**
1. Press `Win + R`, type `mstsc`, press Enter
2. Enter the server's LAN hostname or IP (e.g. `shan` or `192.168.1.50`)
3. Click Connect and enter credentials

**Linux (FreeRDP):**
```bash
xfreerdp /v:192.168.1.50:3389 /u:username /cert:ignore
```

#### B) Public internet access (different network, behind NAT)

RDP clients (mstsc.exe, FreeRDP, Microsoft Remote Desktop for macOS) speak plain TCP and have no ProxyCommand-style hook. The aitun shared port 3389 uses the AITUN/1 plain-TCP handshake to identify which subdomain the connection targets, so the RDP client cannot connect to it directly — it needs a local bridge.

Use `aitun tcp-proxy -l` to start a local bridge, then point mstsc at the local port:

**On the client machine (the one connecting TO the RDP server):**

```powershell
# Terminal 1: start the local bridge (keep this open)
aitun tcp-proxy -l 13389 yourname.aitun.cc 3389
# Output: aitun tcp-proxy: listening on 127.0.0.1:13389 -> yourname.aitun.cc:3389

# Terminal 2: connect with mstsc
mstsc /v:127.0.0.1:13389
```

**Linux (FreeRDP):**
```bash
# Terminal 1
aitun tcp-proxy -l 13389 yourname.aitun.cc 3389

# Terminal 2
xfreerdp /v:127.0.0.1:13389 /u:username /cert:ignore
```

**macOS (Microsoft Remote Desktop):**
```bash
# Terminal 1
aitun tcp-proxy -l 13389 yourname.aitun.cc 3389

# Microsoft Remote Desktop app: add a new PC with address 127.0.0.1:13389
```

The local port `13389` is just a suggestion (computed as `10000 + public_port`). Any free local port works — use `aitun tcp-proxy -l <any-free-port> yourname.aitun.cc 3389` and point your RDP client at `127.0.0.1:<that-port>`.

### Step 5: Clean up

When done, stop the tunnel on the RDP server machine:

```powershell
# Press Ctrl+C in the aitun terminal, or if running in background:
taskkill /IM aitun-client-windows-amd64.exe /F
```

And on the client machine, Ctrl+C the `aitun tcp-proxy` process.

## How RDP Routing Works (AITUN/1 Plain-TCP Handshake)

Starting in v4.9.22, aitun uses the **AITUN/1 plain-TCP handshake** so that RDP and other plain-TCP protocols can share a single public port across multiple subdomains — without requiring TLS on the application traffic.

```
mstsc.exe → 127.0.0.1:13389 (local bridge)
                ↓
        aitun tcp-proxy (adds AITUN/1 handshake header)
                ↓
        yourname.aitun.cc:3389 (shared public port)
                ↓
        aitun server reads AITUN/1 line, routes to "yourname" tunnel
                ↓
        aitun client on RDP server machine
                ↓
        localhost:3389 → RDP service
```

The handshake is a single ASCII line sent before any RDP data:

```
AITUN/1 <subdomain> <port>\r\n
```

e.g. `AITUN/1 yourname 3389\r\n`. The server replies `OK\r\n` and then the connection becomes a transparent byte stream between the client and the tunnel client's `localhost:3389`. The RDP protocol flows through unchanged.

**Why a handshake instead of TLS+SNI?** SSH works with TLS+SNI because the SSH client supports `ProxyCommand` — `aitun ssh-proxy` wraps SSH in TLS and the server uses SNI to route. RDP clients (mstsc.exe etc.) have no equivalent hook, so they cannot speak TLS on port 3389. The AITUN/1 handshake is a ~30-byte ASCII prefix that any plain-TCP client can send via a local bridge, and the magic prefix `AITUN/1 ` is chosen so that no common application protocol is mis-detected (TLS=0x16, SSH=`SSH-`, HTTP=method verbs, RDP/TPKT=0x03, MySQL=length-encoded packet).

**First-byte dispatch on the shared port:**

| First byte | Protocol | Routing |
|------------|----------|---------|
| `0x16` | TLS ClientHello | TLS termination + SNI (existing, used by SSH) |
| `'A'` (0x41) | AITUN/1 handshake | Plain-TCP routing (new, used by RDP/MySQL/etc.) |
| anything else | unknown | rejected |

**Backward compatible** — existing TLS+SNI clients (SSH-over-TLS, HTTPS) continue to work unchanged.

## Advanced Usage

### Forward RDP + SSH Together

```powershell
# On the RDP server machine — expose both SSH and RDP
C:\aitun-client-windows-amd64.exe -k YOUR_TOKEN --tcp-ports 22,3389
```

The v4.9.23+ output shows hints for both ports:

```
  [TCP] ssh      -> localhost:22    (subdomain: yourname.aitun.cc:22)
        Public connect:  ssh user@yourname.aitun.cc
        (add to ~/.ssh/config:  ProxyCommand aitun ssh-proxy %h %p)
        LAN connect:     ssh user@<local-ip>   (no aitun needed)
  [TCP] tcp-3389 -> localhost:3389  (subdomain: yourname.aitun.cc:3389)
        LAN connect:     mstsc /v:<local-ip>:3389   (or just mstsc /v:<hostname>)
        Public connect:  aitun tcp-proxy -l 13389 yourname.aitun.cc 3389
                         mstsc /v:127.0.0.1:13389   (in another terminal)
```

### Custom RDP Port

If RDP is running on a non-standard port (e.g., 13389 locally):

```powershell
C:\aitun-client-windows-amd64.exe -k YOUR_TOKEN --tcp-ports 13389
```

The smart hint shows a different suggested bridge port (10000 + 13389 = 23389, which exceeds 65535, so aitun falls back to `13389 + 1000 = 14389`):

```
  [TCP] tcp-13389 -> localhost:13389 (subdomain: yourname.aitun.cc:13389)
        Public connect:  aitun tcp-proxy -l 14389 yourname.aitun.cc 13389
                         then connect your client to 127.0.0.1:14389
        LAN connect:     use <local-ip>:13389 directly
```

### RDP in a Docker Container

```bash
# Container running xrdp on port 3389, mapped to host port 13389
# On the Docker host:
aitun -k YOUR_TOKEN --tcp-ports 13389
```

### Run aitun tcp-proxy as a background service

For long-lived access, run the local bridge in the background:

```powershell
# Windows: start in a new window, minimized
start /min cmd /c "aitun tcp-proxy -l 13389 yourname.aitun.cc 3389"

# Or use PowerShell Start-Process
Start-Process -WindowStyle Hidden -FilePath "aitun" -ArgumentList "tcp-proxy","-l","13389","yourname.aitun.cc","3389"
```

```bash
# Linux/macOS: nohup
nohup aitun tcp-proxy -l 13389 yourname.aitun.cc 3389 >/tmp/rdp-bridge.log 2>&1 &
```

## Security Recommendations

- **Use strong passwords** on all RDP accounts — the AITUN/1 handshake only does routing, not authentication; RDP's own auth (NLA recommended) still gates access
- **Enable Network Level Authentication (NLA)** on Windows RDP servers
- **Restrict RDP access** to specific users via group policy
- **Consider changing the default RDP port** (3389) on the local server to reduce automated attacks — aitun still exposes it as 3389 on the public side, but the local listener can be on any port
- **Monitor RDP logs** for unauthorized access attempts
- **Disable RDP** when not actively needed
- **The aitun tunnel adds an extra layer** but does not replace RDP's own encryption — RDP traffic itself is encrypted (TLS/CredSSP) on top of the aitun transport

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (required for TCP forwarding) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `3389,22`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

**Subcommands:**

| Command | Description |
|---|---|
| `aitun ssh-proxy <host> [port]` | SSH ProxyCommand — wraps SSH in TLS for SNI routing |
| `aitun tcp-proxy <host> <port>` | Plain-TCP ProxyCommand — sends AITUN/1 handshake, pipes stdin/stdout |
| `aitun tcp-proxy -l <local_port> <host> <port>` | Plain-TCP local bridge — listens on `local_port`, bridges each connection through AITUN/1 to `host:port`. **Use this for mstsc.exe / FreeRDP / Microsoft Remote Desktop.** |

## Notes

- TCP forwarding (required for RDP) requires a registered account and `-k` token — free tunnels do not support TCP
- Register at https://aitun.cc to get an auth token
- AITUN/1 plain-TCP handshake was introduced in v4.9.22 — both the tunnel-host side and the client side must run v4.9.22+ for RDP routing to work
- v4.9.23+ prints smart per-port connection hints in the `tcp_register` output, showing exactly how to connect (LAN vs public, with the correct `tcp-proxy` command for the latter)
- If the requested port (e.g., 3389) is occupied on the server, a port from the 7000-7999 range will be automatically assigned
- P2P mode reduces latency for remote desktop sessions; use `--no-p2p` only if P2P connection fails
- For best performance, ensure a stable internet connection on both ends
- The tunnel stays active as long as the aitun process runs; use `--daemon` for persistent background operation on the server side
- Subdomains remain active for 30 days of inactivity; use heartbeat to renew
- The `aitun tcp-proxy -l` bridge process on the client side stays active until you Ctrl+C it — close it when done to free the local port
