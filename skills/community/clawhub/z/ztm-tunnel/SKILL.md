---
name: ztm-tunnel
description: "Create and manage TCP/UDP tunnels between ZTM network endpoints. Use this to establish secure P2P port forwarding through the ZTM mesh network."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔌",
        "requires":
          {
            "bins": ["ztm"],
            "services": ["ztm-agent"],
          },
        "install":
          [
            {
              "id": "download",
              "kind": "download",
              "label": "Download ZTM from GitHub releases",
              "url": "https://github.com/flomesh-io/ztm/releases",
            },
          ],
        "env":
          {
            "ZTM_AGENT": "http://localhost:7777",
          },
        "config":
          {
            "path": "~/.ztm.conf",
            "fields":
              {
                "agent": "ZTM Agent URL (default: localhost:7777)",
                "mesh": "Default mesh name",
              },
          },
      },
  }
---

# ZTM Tunnel Skill

Create and manage TCP/UDP tunnels between ZTM network endpoints.

## Prerequisites

1. **ZTM Agent must be running**
   ```bash
   ztm start agent
   ```

2. **Join a mesh network**
   ```bash
   ztm join <mesh-name> --as <your-endpoint-name> --permit <permit-file.json>
   ```

3. **Tunnel app must be installed**
   ```bash
   ztm app install tunnel
   ```

## Concepts

- **Inbound**: The local endpoint that listens for connections and forwards them to the remote
- **Outbound**: The remote endpoint that receives connections and forwards them to target services
- **Tunnel**: A complete connection consisting of inbound + outbound

## List Tunnels

List all tunnels in the mesh:

```bash
ztm tunnel get tunnel
```

List inbound tunnels (local listening ports):

```bash
ztm tunnel get inbound
```

List outbound tunnels (remote targets):

```bash
ztm tunnel get outbound
```

## Create a Tunnel

### Scenario: Expose a local service to another endpoint

**Step 1: On the remote endpoint (outbound)**, specify target services:

```bash
ztm tunnel open outbound my-tunnel --targets 192.168.1.100:8080
```

**Step 2: On the local endpoint (inbound)**, set up port forwarding:

```bash
ztm tunnel open inbound my-tunnel --listen 0.0.0.0:9000 --exits <remote-endpoint-id>
```

This creates a tunnel where:
- Local port `9000` listens for connections
- Connections are forwarded to remote endpoint
- Remote forwards to `192.168.1.100:8080`

### Quick One-Liner (Same Command on Both Ends)

Create both ends at once by running on respective endpoints:

```bash
# On endpoint A (listening side)
ztm tunnel open inbound tunnel-name --listen 0.0.0.0:9000 --exits <endpoint-B-id>

# On endpoint B (target side) 
ztm tunnel open outbound tunnel-name --targets 127.0.0.1:8080
```

## Delete a Tunnel

Close the inbound end:

```bash
ztm tunnel close inbound my-tunnel
```

Close the outbound end:

```bash
ztm tunnel close outbound my-tunnel
```

## Tunnel Details

View detailed tunnel information:

```bash
ztm tunnel describe tunnel tcp/my-tunnel
```

View inbound details:

```bash
ztm tunnel describe inbound tcp/my-tunnel
```

View outbound details:

```bash
ztm tunnel describe outbound tcp/my-tunnel
```

## Common Use Cases

### Access Home Server from Anywhere

```bash
# On home endpoint
ztm tunnel open inbound home-server --listen 0.0.0.0:22 --exits <office-endpoint-id>

# On office endpoint
ztm tunnel open outbound home-server --targets 192.168.1.10:22
```

### Forward Web Service

```bash
# Remote endpoint exposes local web service
ztm tunnel open outbound web-tunnel --targets 192.168.1.100:80

# Local endpoint listens on port 8080
ztm tunnel open inbound web-tunnel --listen 0.0.0.0:8080 --exits <remote-endpoint-id>
```

### UDP Tunnel (for DNS, VoIP, etc.)

```bash
ztm tunnel open outbound dns-tunnel --targets 8.8.8.8:53
ztm tunnel open inbound dns-tunnel --listen 0.0.0.0:5300 --exits <remote-endpoint-id>
```

## Troubleshooting

Check if ZTM agent is running:

```bash
curl http://localhost:7777/api/status
```

Check mesh status:

```bash
ztm get mesh
ztm get ep
```

Check installed apps:

```bash
ztm get app
```

If tunnel app is not installed:

```bash
ztm app install tunnel
```

View tunnel app logs:

```bash
ztm log app tunnel
```

## Configuration

ZTM CLI config is stored in `~/.ztm.conf`:

```json
{
  "agent": "localhost:7777",
  "mesh": "my-mesh-name"
}
```

Or set via environment:

```bash
export ZTM_AGENT=http://localhost:7777
export ZTM_MESH=my-mesh-name
```

## API Reference

For programmatic access, use the ZTM Agent HTTP API:

```bash
# Get all tunnels
curl http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/tunnel

# Get inbound tunnels
curl http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/inbound

# Create inbound
curl -X POST http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/inbound/tcp/tunnel-name \
  -H "Content-Type: application/json" \
  -d '{"listens":[{"ip":"0.0.0.0","port":9000}],"exits":["endpoint-id"]}'
```
