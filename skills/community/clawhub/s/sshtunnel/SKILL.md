---
name: sshtunnel
version: 4.7.5
description: Expose local SSH servers to the public internet via aitun TCP tunnel with SSH-over-TLS routing. Each subdomain gets its own SSH endpoint on port 22 with perfect isolation via SNI. Perfect for AI agents that need to provide remote SSH access behind NAT/firewall.
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
    emoji: "🖥️"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/sshtunnel
---

# SSH Tunnel - Remote SSH Access via SSH-over-TLS

## When to Use

Use this skill when:
- You need to access a remote machine via SSH that is behind NAT, firewall, or a private network
- You want to expose a local SSH server so a colleague or client can connect remotely
- You are running SSH in a container or VM that has no public IP and need to make it reachable
- You want to provide temporary SSH access for pair programming, debugging, or server maintenance
- You need to connect to a development machine from another location without VPN or port forwarding
- Multiple users each need their own SSH endpoint on the same server port

Do NOT use this skill when:
- The SSH server already has a public IP and is directly reachable
- You only need to transfer files (use sendfile instead)
- You want to expose an HTTP service (use aitun-tunnel instead)

## Instructions

### Step 1: Install aitun

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

Or verify it is already installed:

```bash
which aitun
```

### Step 2: Ensure SSH server is running locally

Verify the local SSH daemon is running and accessible:

```bash
# Check if sshd is running
ps aux | grep sshd

# Or check if port 22 is listening
ss -tlnp | grep :22

# Test local SSH connection
ssh localhost echo "SSH OK"
```

If sshd is not running, install and start it:

```bash
# Ubuntu/Debian
sudo apt install openssh-server -y
sudo systemctl start sshd

# CentOS/RHEL
sudo yum install openssh-server -y
sudo systemctl start sshd

# macOS (usually pre-installed)
sudo systemsetup -setremotelogin on
```

### Step 3: Create a TCP tunnel for SSH

SSH uses TCP port 22. Use aitun's `--tcp-ports` flag to forward this port. TCP forwarding requires an auth token (register at https://aitun.cc):

```bash
aitun -k YOUR_TOKEN --tcp-ports 22 &
AITUN_PID=$!
sleep 3
```

Or with HTTP tunnel alongside SSH:

```bash
aitun -k YOUR_TOKEN -p 8080 --tcp-ports 22 &
AITUN_PID=$!
sleep 3
```

The output will show:

```
[TCP] ssh -> localhost:22 (subdomain: yourname.t.aitun.cc:22)
```

### Step 4: Configure SSH ProxyCommand

On the **remote client machine** (the one connecting TO your SSH server), add this to `~/.ssh/config`:

```
Host *.t.aitun.cc
    ProxyCommand aitun ssh-proxy %h %p
```

This tells SSH to route connections through `aitun ssh-proxy`, which wraps SSH in TLS with the correct SNI for subdomain routing.

### Step 5: Connect remotely

From any machine with aitun installed:

```bash
# Direct SSH — just like a normal server!
ssh user@yourname.t.aitun.cc

# With SSH key
ssh -i ~/.ssh/id_rsa user@yourname.t.aitun.cc

# With verbose output for debugging
ssh -v user@yourname.t.aitun.cc
```

### Step 6: Clean up

When done, stop the tunnel:

```bash
kill $AITUN_PID 2>/dev/null
```

## CRITICAL: Reuse SSH Connections

**When executing multiple commands over an aitun SSH tunnel, you MUST reuse the SSH connection.** Creating a new SSH connection for every command is extremely slow because:

1. Each SSH connection requires a full key exchange (5-7 round-trips)
2. The aitun tunnel adds network latency for each round-trip
3. A new connection can take 1.5-5 seconds, while a reused connection responds in ~200ms

### How to Reuse SSH Connections

#### Method 1: SSH ControlMaster (Recommended for bash/native SSH)

Add to `~/.ssh/config`:

```
Host *.t.aitun.cc
    ProxyCommand aitun ssh-proxy %h %p
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

Then create the socket directory:

```bash
mkdir -p ~/.ssh/sockets
```

The first `ssh` command creates the master connection. All subsequent commands reuse it automatically — no additional handshake needed. `ControlPersist 600` keeps the connection alive for 10 minutes after the last session closes.

#### Method 2: Paramiko Transport Reuse (For Python/AI agents)

When using Python (paramiko) to SSH over the aitun TLS tunnel, keep the `Transport` object alive and open new `Channel` sessions on it:

```python
import paramiko, ssl, socket

def create_ssh_transport(host, port, sni, username, key_path):
    """Create a persistent SSH-over-TLS transport (do this ONCE)."""
    key = paramiko.RSAKey.from_private_key_file(key_path)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    raw_sock = socket.create_connection((host, port), timeout=10)
    tls_sock = context.wrap_socket(raw_sock, server_hostname=sni)

    transport = paramiko.Transport(tls_sock)
    transport.set_keepalive(30)
    transport.connect(username=username, pkey=key)
    return transport

def run_command(transport, cmd, timeout=30):
    """Execute a command on an existing transport (REUSE the transport!)."""
    session = transport.open_session()
    session.settimeout(timeout)
    session.exec_command(cmd)

    stdout, stderr = b'', b''
    while True:
        if session.recv_ready():
            stdout += session.recv(65536)
        if session.recv_stderr_ready():
            stderr += session.recv_stderr(65536)
        if session.exit_status_ready():
            while session.recv_ready():
                stdout += session.recv(65536)
            while session.recv_stderr_ready():
                stderr += session.recv_stderr(65536)
            break

    exit_code = session.recv_exit_status()
    session.close()
    return exit_code, stdout.decode('utf-8', errors='replace'), stderr.decode('utf-8', errors='replace')

# Usage: create transport ONCE, run MANY commands
transport = create_ssh_transport(
    host='43.160.208.156', port=22,
    sni='yourname.t.aitun.cc',
    username='mojo',
    key_path='/path/to/ssh_key'
)

# First command (~1-2s, includes handshake)
ec, out, err = run_command(transport, 'echo hello')

# Subsequent commands (~200ms, reuses connection!)
ec, out, err = run_command(transport, 'uname -a')
ec, out, err = run_command(transport, 'df -h')

# When completely done:
transport.close()
```

### Performance Comparison

| Approach | Per-command latency | Notes |
|----------|-------------------|-------|
| New SSH connection each time | 1.5-5 seconds | Wasteful, slow |
| **Reused SSH connection** | **~200ms** | **Recommended** |

### Connection Health

When reusing SSH connections over the tunnel:
- Set a keepalive interval (30 seconds recommended) to detect dead connections early
- If a command fails with a transport error, reconnect by creating a new transport
- Close the transport cleanly when done to free resources on both ends

## How SSH-over-TLS Works

aitun v4.7.0 uses **SSH-over-TLS** for perfect multi-tenant SSH on shared ports:

```
ssh user@acer.t.aitun.cc
        ↓
  ProxyCommand: aitun ssh-proxy wraps SSH in TLS (SNI=acer.t.aitun.cc)
        ↓
  Server terminates TLS, sees SNI → routes to "acer" tunnel
        ↓
  Decrypted SSH stream → tunnel client → localhost:22
```

**Why TLS?** SSH is a plaintext protocol that doesn't send hostname information. Without TLS, there's no way to tell which subdomain an SSH connection is targeting. By wrapping SSH in TLS, we get SNI (Server Name Indication) which tells the server exactly which subdomain to route to.

**Result:** Every subdomain can have its own SSH on port 22 — no conflicts, no ambiguity, no `--tcp-default` needed.

## Advanced Usage

### Forward Multiple Ports (SSH + MySQL)

```bash
aitun -k YOUR_TOKEN --tcp-ports 22,3306 &
AITUN_PID=$!
sleep 3
```

### SSH into a Container

```bash
# If SSH is running in a Docker container on a non-standard port
aitun -k YOUR_TOKEN --tcp-ports 2222 &

# Or with HTTP alongside:
# aitun -k YOUR_TOKEN -p 8080 --tcp-ports 2222 &
```

### Use with SSH Config (Recommended)

Add to `~/.ssh/config` on the remote client:

```
Host *.t.aitun.cc
    ProxyCommand aitun ssh-proxy %h %p
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

Host my-remote-dev
    HostName yourname.t.aitun.cc
    User username
    IdentityFile ~/.ssh/id_rsa
```

Then simply:

```bash
ssh my-remote-dev
```

### One-off SSH without Config

If you don't want to modify ssh config:

```bash
ssh -o "ProxyCommand=aitun ssh-proxy %h %p" user@yourname.t.aitun.cc
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (required for TCP forwarding) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

**Subcommand:**

| Command | Description |
|---|---|
| `aitun ssh-proxy <host> [port]` | SSH ProxyCommand — wraps SSH in TLS for SNI routing |

## Notes

- TCP forwarding (required for SSH) requires a registered account and `-k` token — free tunnels do not support TCP
- Register at https://aitun.cc to get an auth token
- All traffic is encrypted end-to-end: SSH inside TLS inside the aitun tunnel
- **ProxyCommand is required** — plaintext SSH is not supported. Add `ProxyCommand aitun ssh-proxy %h %p` to your `~/.ssh/config`
- If the requested port (e.g., 22) is occupied on the server, a port from the 7000-7999 range will be automatically assigned
- **Always reuse SSH connections** when running multiple commands — see the "CRITICAL: Reuse SSH Connections" section above
- For security, ensure your SSH server uses key-based authentication (disable password auth if possible)
- Consider using fail2ban or similar tools to protect against brute-force attacks on your SSH server
- The tunnel stays active as long as the aitun process runs; use `--daemon` for persistent background operation
- Subdomains remain active for 30 days of inactivity; use heartbeat to renew
