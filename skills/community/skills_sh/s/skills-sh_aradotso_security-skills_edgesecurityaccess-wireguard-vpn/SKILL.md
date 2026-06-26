---
name: edgesecurityaccess-wireguard-vpn
description: WireGuard-based rapid VPN networking software for Linux with HTTP API and utility tools
triggers:
  - set up EdgeSecurityAccess VPN server
  - configure ESA WireGuard networking
  - create ESA VPN users and configuration
  - deploy EdgeSecurityAccess server
  - manage WireGuard users with ESA
  - build ESA utility tools
  - connect to ESA VPN server
  - troubleshoot EdgeSecurityAccess issues
---

# EdgeSecurityAccess WireGuard VPN Skill

> Skill by [ara.so](https://ara.so) — Security Skills collection.

EdgeSecurityAccess (ESA) is a WireGuard-based rapid networking software suite for setting up virtual private networks. It consists of three components: ESA mainframe (Go server), ESA utility software package (C/C++ tools), and ESA desktop client (C# Windows GUI). The server exposes an HTTP API for retrieving WireGuard configurations based on username/password authentication.

## Installation

### Prerequisites

**Linux Server:**
```bash
# Install WireGuard
apt install wireguard  # Debian/Ubuntu
# or
yum install wireguard-tools  # RHEL/CentOS

# Install Go 1.26+ for building ESA mainframe
wget https://go.dev/dl/go1.26.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.26.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

**Windows Client:**
```powershell
# Install WireGuard
winget install WireGuard.WireGuard

# Install .NET Runtime for ESA Desktop
# Download from Microsoft official website
```

### Build ESA Mainframe

```bash
git clone https://github.com/KochiyaSanaeNya/EdgeSecurityAccess.git
cd EdgeSecurityAccess

# Build the main server
go build -o esa-server ./main.go

# Build utility tools (C/C++)
cd tools
gcc -o ESAusr ESAusr.c
gcc -o ESAProc ESAProc.c
gcc -o ESAInit ESAInit.c
cd ..
```

### Build ESA Desktop (Windows)

```bash
# Open solution in Visual Studio and build
# Or use dotnet CLI
cd ESADesktop
dotnet build -c Release
```

## Configuration

### Generate WireGuard Keys

```bash
# Generate server keys
wg genkey | tee server_private.key | wg pubkey > server_public.key

# Generate client keys (done automatically by ESAProc)
wg genkey | tee client_private.key | wg pubkey > client_public.key
```

### Create esa.conf

Create `/etc/esa/esa.conf`:

```
$servip = 172.16.16.1/24
$subnet = 172.16.16.0/24
$endpoint = vpn.example.com:50000
$keeptime = 25
$wgport = 50000
$httport = 50001
$servpriv = $(cat server_private.key)
$servpub = $(cat server_public.key)
```

### Configuration File Structure

```go
// Configuration keys reference
type Config struct {
    ServIP    string  // $servip - Server IP in virtual network
    Subnet    string  // $subnet - Virtual network subnet
    Endpoint  string  // $endpoint - External WireGuard access point
    KeepTime  int     // $keeptime - NAT traversal keepalive interval
    WGPort    int     // $wgport - WireGuard UDP port
    HTTPPort  int     // $httport - HTTP API port
    ServPriv  string  // $servpriv - Server WireGuard private key
    ServPub   string  // $servpub - Server WireGuard public key
}
```

### User Management

**Add users with ESAusr:**

```bash
# Copy ESAusr to config directory
cp tools/ESAusr /etc/esa/
cd /etc/esa

# Run and follow prompts
./ESAusr
# Enter username: alice
# Enter password: secure_password
# User added to users.txt
```

**users.txt format:**
```
alice:secure_password:172.16.16.2/32:client_public_key_here
bob:another_password:172.16.16.3/32:another_public_key_here
```

### Generate User WireGuard Configs

```bash
# Copy ESAProc to config directory
cp tools/ESAProc /etc/esa/
cd /etc/esa

# Generate usrwg.conf from users.txt
./ESAProc
# Output: usrwg.conf created with all user WireGuard configurations
```

### Initialize Local WireGuard

```bash
# Copy ESAInit to config directory
cp tools/ESAInit /etc/esa/
cd /etc/esa

# Configure local WireGuard interface
./ESAInit
# Output: /etc/wireguard/wg0.conf configured
```

## Running the Server

### Start ESA Mainframe

```bash
# Start the server
./esa-server -config /etc/esa/esa.conf

# Or run as systemd service
cat > /etc/systemd/system/esa.service <<EOF
[Unit]
Description=EdgeSecurityAccess VPN Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/esa-server -config /etc/esa/esa.conf
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable esa
systemctl start esa
```

### Start WireGuard Interface

```bash
# Bring up WireGuard interface
wg-quick up wg0

# Check status
wg show

# Enable at boot
systemctl enable wg-quick@wg0
```

### Enable Kernel Forwarding

```bash
# Enable IP forwarding
sysctl -w net.ipv4.ip_forward=1

# Persist across reboots
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p

# Configure NAT (replace eth0 with your interface)
iptables -t nat -A POSTROUTING -s 172.16.16.0/24 -o eth0 -j MASQUERADE
iptables -A FORWARD -i wg0 -j ACCEPT
iptables -A FORWARD -o wg0 -j ACCEPT
```

## HTTP API Usage

### Retrieve User Configuration

**cURL Example:**

```bash
# Get WireGuard config for user
curl -X POST \
  --data "username=alice&password=secure_password" \
  http://127.0.0.1:50001

# Response (WireGuard config):
# [Interface]
# PrivateKey = client_private_key
# Address = 172.16.16.2/32
# [Peer]
# PublicKey = server_public_key
# AllowedIPs = 172.16.16.0/24
# Endpoint = vpn.example.com:50000
# PersistentKeepalive = 25
```

**Go Client Example:**

```go
package main

import (
    "fmt"
    "io"
    "net/http"
    "net/url"
    "strings"
)

func getWireGuardConfig(username, password, apiURL string) (string, error) {
    data := url.Values{}
    data.Set("username", username)
    data.Set("password", password)

    resp, err := http.Post(
        apiURL,
        "application/x-www-form-urlencoded",
        strings.NewReader(data.Encode()),
    )
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return "", err
    }

    return string(body), nil
}

func main() {
    config, err := getWireGuardConfig(
        "alice",
        "secure_password",
        "http://127.0.0.1:50001",
    )
    if err != nil {
        panic(err)
    }
    fmt.Println(config)
}
```

**Python Client Example:**

```python
import requests

def get_wireguard_config(username, password, api_url):
    response = requests.post(
        api_url,
        data={
            'username': username,
            'password': password
        }
    )
    return response.text

config = get_wireguard_config(
    'alice',
    'secure_password',
    'http://127.0.0.1:50001'
)
print(config)

# Save to file and connect
with open('wg_client.conf', 'w') as f:
    f.write(config)

import subprocess
subprocess.run(['wg-quick', 'up', 'wg_client.conf'])
```

## Client Connection

### Linux/macOS CLI

```bash
# Get config and save
curl -X POST \
  --data "username=alice&password=secure_password" \
  http://127.0.0.1:50001 > esa_user.conf

# Connect
wg-quick up esa_user.conf

# Test connection
ping 172.16.16.1

# Disconnect
wg-quick down esa_user.conf
```

### Using ESA Desktop (Windows)

```
1. Launch ESA Desktop application
2. Enter:
   - Username: alice
   - Password: secure_password
   - Server URL: http://vpn.example.com:50001
3. Click "Connect"
4. WireGuard tunnel establishes automatically
```

## Reverse Proxy Setup (HTTPS)

### Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name vpn.example.com;

    ssl_certificate /etc/ssl/certs/vpn.example.com.crt;
    ssl_certificate_key /etc/ssl/private/vpn.example.com.key;

    location / {
        proxy_pass http://127.0.0.1:50001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Caddy Configuration

```
vpn.example.com {
    reverse_proxy 127.0.0.1:50001
}
```

**Update client requests to use HTTPS:**

```bash
curl -X POST \
  --data "username=alice&password=secure_password" \
  https://vpn.example.com
```

## Common Patterns

### Automated User Provisioning

```go
package main

import (
    "crypto/rand"
    "encoding/base64"
    "fmt"
    "os"
    "strings"

    "golang.org/x/crypto/curve25519"
)

// Generate WireGuard key pair
func generateKeyPair() (privKey, pubKey string, err error) {
    var private [32]byte
    if _, err := rand.Read(private[:]); err != nil {
        return "", "", err
    }

    public, err := curve25519.X25519(private[:], curve25519.Basepoint)
    if err != nil {
        return "", "", err
    }

    privKey = base64.StdEncoding.EncodeToString(private[:])
    pubKey = base64.StdEncoding.EncodeToString(public)
    return privKey, pubKey, nil
}

// Add user to users.txt
func addUser(username, password, ip string) error {
    _, pubKey, err := generateKeyPair()
    if err != nil {
        return err
    }

    userLine := fmt.Sprintf("%s:%s:%s:%s\n", username, password, ip, pubKey)

    f, err := os.OpenFile("/etc/esa/users.txt", os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0600)
    if err != nil {
        return err
    }
    defer f.Close()

    _, err = f.WriteString(userLine)
    return err
}

func main() {
    err := addUser("newuser", "newpass", "172.16.16.10/32")
    if err != nil {
        panic(err)
    }
    fmt.Println("User added successfully")
}
```

### Health Check Endpoint

```go
package main

import (
    "fmt"
    "net/http"
)

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, "OK")
}

func main() {
    http.HandleFunc("/health", healthCheckHandler)
    http.ListenAndServe(":50002", nil)
}
```

### User Config Backup Script

```bash
#!/bin/bash
# backup_esa_users.sh

BACKUP_DIR="/var/backups/esa"
CONFIG_DIR="/etc/esa"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup user files
tar -czf "$BACKUP_DIR/esa_backup_$TIMESTAMP.tar.gz" \
    "$CONFIG_DIR/users.txt" \
    "$CONFIG_DIR/usrwg.conf" \
    "$CONFIG_DIR/esa.conf"

# Keep only last 7 backups
ls -t "$BACKUP_DIR"/esa_backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup completed: esa_backup_$TIMESTAMP.tar.gz"
```

## Troubleshooting

### Server Won't Start

```bash
# Check if port is already in use
netstat -tuln | grep 50001
lsof -i :50001

# Check WireGuard port
netstat -tuln | grep 50000

# Verify configuration syntax
cat /etc/esa/esa.conf | grep -E '^\$'

# Check logs
journalctl -u esa -f
```

### Authentication Fails

```bash
# Verify user exists
grep "^username:" /etc/esa/users.txt

# Check users.txt format (should be username:password:ip:pubkey)
cat /etc/esa/users.txt

# Regenerate usrwg.conf
cd /etc/esa
./ESAProc
```

### WireGuard Connection Issues

```bash
# Check WireGuard interface status
wg show wg0

# Verify server can reach UDP port
nc -u -v vpn.example.com 50000

# Check routing
ip route show

# Test from client
ping 172.16.16.1

# Check server firewall
iptables -L -n -v
ufw status

# Allow WireGuard port
ufw allow 50000/udp
```

### Cannot Forward Traffic

```bash
# Verify IP forwarding is enabled
sysctl net.ipv4.ip_forward
# Should output: net.ipv4.ip_forward = 1

# Check NAT rules
iptables -t nat -L -n -v

# Re-add NAT rule
iptables -t nat -A POSTROUTING -s 172.16.16.0/24 -o eth0 -j MASQUERADE

# Save iptables rules
iptables-save > /etc/iptables/rules.v4
```

### HTTP API Returns Empty

```bash
# Test with verbose curl
curl -v -X POST \
  --data "username=alice&password=secure_password" \
  http://127.0.0.1:50001

# Check if users.txt is properly formatted
cat /etc/esa/users.txt | sed 's/:/ : /g'

# Verify usrwg.conf was generated
cat /etc/esa/usrwg.conf

# Restart ESA server
systemctl restart esa
```

### Key Security Issues

**Note:** ESA stores user private keys on the server (architectural limitation). For production use:

```bash
# Restrict file permissions
chmod 600 /etc/esa/users.txt
chmod 600 /etc/esa/usrwg.conf
chown root:root /etc/esa/*.txt /etc/esa/*.conf

# Encrypt sensitive files (future improvement)
# Current version does NOT encrypt username/password
# Use HTTPS reverse proxy to protect credentials in transit
```

### Performance Tuning

```bash
# Increase WireGuard MTU if needed
ip link set dev wg0 mtu 1420

# Optimize sysctl for VPN
cat >> /etc/sysctl.conf <<EOF
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
EOF
sysctl -p
```

## Security Considerations

1. **Use HTTPS reverse proxy** (Nginx/Caddy) to protect credentials
2. **Passwords are stored in plaintext** in users.txt - restrict access
3. **User private keys stored on server** - architectural limitation
4. **No rate limiting** - implement fail2ban or reverse proxy rate limits
5. **Enable firewall rules** to restrict HTTP API access
6. **Regular backups** of configuration files
7. **Monitor logs** for authentication attempts

```bash
# Example fail2ban filter for ESA
# /etc/fail2ban/filter.d/esa.conf
[Definition]
failregex = ^.*Authentication failed for user <HOST>.*$
ignoreregex =

# /etc/fail2ban/jail.local
[esa]
enabled = true
port = 50001
filter = esa
logpath = /var/log/esa/access.log
maxretry = 5
bantime = 3600
```
