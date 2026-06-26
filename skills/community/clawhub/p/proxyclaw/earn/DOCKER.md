# IPLoop Node Agent — Docker Setup

Earn proxy credits by sharing your unused bandwidth.

## Quick Start

```bash
docker run -d --name iploop-node --restart=always ultronloop2026/iploop-node:latest
```

## Docker Compose

```yaml
version: '3'
services:
  iploop-node:
    image: ultronloop2026/iploop-node:latest
    container_name: iploop-node
    restart: always
```

## Verify It's Running

```bash
# Check container
docker logs iploop-node

# Check gateway sees your node
curl -s https://gateway.iploop.io:9443/health | python3 -m json.tool
```

## Check Your Earnings

```bash
# Login first
TOKEN=$(curl -s -X POST https://api.iploop.io/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","password":"YourPass"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

# Check balance
curl -s https://api.iploop.io/api/v1/earn/balance -H "Authorization: Bearer $TOKEN"

# List devices
curl -s https://api.iploop.io/api/v1/earn/devices -H "Authorization: Bearer $TOKEN"
```

## Standalone Binary

Don't want Docker? Download from [GitHub](https://github.com/Iploop/iploop-node/releases):

```bash
# Linux
./iploop-node -gateway wss://gateway.iploop.io:9443/ws

# With token
./iploop-node -token YOUR_TOKEN -gateway wss://gateway.iploop.io:9443/ws
```

| Platform | Binary |
|----------|--------|
| Linux amd64 | `iploop-node-linux-amd64` |
| Linux arm64 | `iploop-node-linux-arm64` |
| macOS Intel | `iploop-node-darwin-amd64` |
| macOS ARM | `iploop-node-darwin-arm64` |
| Windows x64 | `iploop-node-windows-amd64.exe` |
| Raspberry Pi | `iploop-node-linux-armv7` |

## Resource Usage

- RAM: < 50MB
- CPU: Near zero
- Bandwidth: A few hundred MB/day depending on demand

## FAQ

**Q: Is it safe?**
Only handles HTTP/HTTPS proxy traffic. No access to your files, passwords, or local network.

**Q: Multiple nodes?**
Yes! +20% bonus per additional node.

**Q: Minimum uptime?**
5 minutes before earning starts. Gold tier after 24h cumulative.
