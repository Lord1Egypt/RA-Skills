# ZTM Tunnel Skills

> Create and manage TCP/UDP tunnels through ZTM's P2P mesh network.

OpenClaw Skill for managing TCP/UDP tunnels via ZTM (Zero Trust Mesh).

## What is this?

This is an **OpenClaw Skill** that provides tunnel management capabilities using ZTM's tunnel app. It allows you to create secure P2P port forwarding through the ZTM mesh network.

## What is ZTM?

**ZTM (Zero Trust Mesh)** is an open-source decentralized network software built on HTTP/2 tunnels. It provides:

- 🔒 End-to-end encrypted P2P connections
- 🌐 Cross-firewall/firewall NAT traversal
- 📡 No central server required (truly decentralized)
- 🚀 High performance (built on Pipy, written in C++)

Learn more: https://github.com/flomesh-io/ztm

## Features

- Create TCP/UDP tunnels between ZTM endpoints
- Expose local services to remote endpoints
- Port forwarding through the mesh network
- Access remote services as if they were local

## Prerequisites

1. **ZTM CLI** installed
2. **ZTM Agent** running and joined to a mesh
3. **Tunnel app** installed

## Quick Start

### Step 1: Install ZTM

```bash
# Run the installation script
./install.sh

# Or manually download from https://github.com/flomesh-io/ztm/releases
```

### Step 2: Start ZTM Agent

```bash
ztm start agent
```

### Step 3: Join a Mesh

```bash
# If you have a permit file
ztm join <mesh-name> --as <your-name> --permit permit.json

# Or create a new mesh
ztm start hub --listen 0.0.0.0:8888 --names your-public-ip:8888 --permit root.json
```

### Step 4: Install Tunnel App

```bash
ztm app install tunnel
```

### Step 5: Create a Tunnel

**Scenario:** Expose a local web service (port 8080) to another endpoint

```bash
# On the remote endpoint (where you want to access from)
# First, create outbound (target) side:
ztm tunnel open outbound my-web --targets 192.168.1.100:8080

# On the local endpoint (where the service is running)
# Create inbound (listening) side:
ztm tunnel open inbound my-web --listen 0.0.0.0:9000 --exits <remote-endpoint-id>
```

Now you can access the local service by connecting to port 9000 on the remote endpoint!

## Commands

### List Tunnels

```bash
# List all tunnels in mesh
ztm tunnel get tunnel

# List inbound (listening) tunnels
ztm tunnel get inbound

# List outbound (target) tunnels
ztm tunnel get outbound
```

### Create Tunnel

```bash
# Create inbound (listening) end
ztm tunnel open inbound <name> --listen <ip>:<port> --exits <endpoint-id>

# Create outbound (target) end  
ztm tunnel open outbound <name> --targets <host>:<port>
```

### Delete Tunnel

```bash
# Close inbound
ztm tunnel close inbound <name>

# Close outbound
ztm tunnel close outbound <name>
```

### Describe Tunnel

```bash
ztm tunnel describe tunnel tcp/<name>
```

## Use Cases

### Remote Access to Home Server

```bash
# On home endpoint
ztm tunnel open inbound home-ssh --listen 0.0.0.0:2222 --exits <office-endpoint-id>

# On office endpoint
ztm tunnel open outbound home-ssh --targets 192.168.1.10:22
```

### Forward Web Service

```bash
# Remote endpoint
ztm tunnel open outbound web --targets 192.168.1.100:80

# Local endpoint
ztm tunnel open inbound web --listen 0.0.0.0:8080 --exits <remote-endpoint-id>
```

### UDP Tunnel (DNS, VoIP, etc.)

```bash
ztm tunnel open outbound dns --targets 8.8.8.8:53
ztm tunnel open inbound dns --listen 0.0.0.0:5300 --exits <remote-endpoint-id>
```

## Configuration

ZTM CLI config is stored in `~/.ztm.conf`:

```json
{
  "agent": "localhost:7777",
  "mesh": "your-mesh-name"
}
```

Or use environment variables:

```bash
export ZTM_AGENT=http://localhost:7777
export ZTM_MESH=your-mesh-name
```

## Troubleshooting

```bash
# Check if agent is running
curl http://localhost:7777/api/status

# Check mesh status
ztm get mesh

# Check endpoints
ztm get ep

# Check installed apps
ztm get app

# View tunnel logs
ztm log app tunnel
```

## API Reference

For programmatic access, use the ZTM Agent HTTP API:

```bash
# Get all tunnels
curl http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/tunnel

# Get inbound tunnels
curl http://localhost:7777/api/meshes/{mesh}/apps/ztm/tunnel/api/inbound
```

## License

MIT License - see LICENSE file for details.

## Links

- [ZTM GitHub](https://github.com/flomesh-io/ztm)
- [ZTM Documentation](https://flomesh.io/ztm/docs)
- [OpenClaw](https://github.com/flomesh-io/openclaw)
- [Pipy](https://github.com/flomesh-io/pipy)
