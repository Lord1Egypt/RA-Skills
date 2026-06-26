# Umbrel Proxy Manager - OpenClaw Skill

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Efficiently manage and interact with Umbrel proxy services for Docker containers. Automatically discovers running services, maps internal Docker IPs to accessible host ports, and updates OpenClaw config.

## Problem Solved

Umbrel runs Docker containers with internal networking (10.21.0.x) and exposes them via app proxy containers on localhost ports. This skill:
1. **Discovers** all Umbrel proxy services
2. **Maps** internal Docker IPs to accessible host ports  
3. **Updates** OpenClaw config automatically
4. **Tests** connectivity to ensure services work

## Installation

```bash
# Using ClawHub (recommended)
clawhub install umbrel-proxy

# Manual installation
mkdir -p skills/
cp -r umbrel-proxy skills/
```

## Quick Start

```bash
cd skills/umbrel-proxy
bash scripts/simple_umbrel_sync.sh
```

## Usage

### Simple Sync (Recommended)
```bash
bash scripts/simple_umbrel_sync.sh
```
Checks OpenClaw-relevant services only (perplexica, searxng, synapse, matrix).

### Full Discovery
```bash
python3 scripts/discover_umbrel_services.py
```
Discovers all Umbrel proxy services.

### Connectivity Testing
```bash
python3 scripts/test_connectivity.py
```
Tests HTTP connectivity to discovered services.

### One-Shot Sync
```bash
bash scripts/umbrel_proxy_sync.sh
```
Full discovery + config update + connectivity test.

## Features

- **Automatic Discovery**: Finds all Umbrel Docker proxy services
- **IP Mapping**: Maps internal Docker IPs (10.21.0.x) to localhost ports
- **Config Sync**: Updates OpenClaw plugin configurations automatically
- **Connectivity Verification**: Tests service accessibility
- **Simple Interface**: Easy-to-use scripts for common tasks
- **Comprehensive**: Handles multiple Umbrel services

## Common Services Managed

| Service | Internal IP Pattern | Proxy Port Example | OpenClaw Plugin |
|---------|---------------------|-------------------|-----------------|
| Perplexica | 10.21.0.x:3000 | 3444 | perplexica |
| SearXNG | 10.21.0.x:8080 | 8182 | searxng |
| Synapse | 10.21.0.x:8008 | 8008 | synapse |
| Jellyfin | 10.21.0.x:8096 | 8096 | (if configured) |
| OpenWebUI | 10.21.0.x:8080 | 3000 | (if configured) |

## Example Output

```
🦦 Simple Umbrel Proxy Sync
==========================

✓ Docker is running

Checking OpenClaw-relevant services:
------------------------------------
🔍 searxng (localhost:8182)... proxy ✓ accessible ✓
  ✓ OpenClaw config is correct

🔍 synapse (localhost:8008)... proxy ✓ accessible ✓
  ✓ OpenClaw config is correct

🔍 perplexica (localhost:3444)... proxy ✓ accessible ✓
  ✓ OpenClaw config is correct

=== Summary ===
Services checked: 4 + matrix

Quick reference:
----------------
perplexica:  http://localhost:3444
searxng:     http://localhost:8182
synapse:     http://localhost:8008  (matrix homeserver)

✅ Sync complete!
```

## When to Use

- After Docker container restarts
- When services become unreachable
- During OpenClaw setup/configuration
- When adding new Umbrel apps
- For troubleshooting service connectivity
- Regular maintenance (cron job recommended)

## Integration

The skill automatically integrates with OpenClaw's plugin system. After running the sync script, restart the gateway:

```bash
openclaw gateway restart
```

## Files

- `SKILL.md` - OpenClaw skill documentation
- `scripts/simple_umbrel_sync.sh` - Simple sync (recommended)
- `scripts/discover_umbrel_services.py` - Advanced discovery
- `scripts/test_connectivity.py` - Connectivity testing
- `scripts/umbrel_proxy_sync.sh` - One-shot sync
- `scripts/update_openclaw_config.py` - Config updater
- `package.json` - NPM package metadata
- `CHANGELOG.md` - Version history

## Auto-Discovery Logic

1. **Find proxy containers**: `docker ps | grep app-proxy`
2. **Map internal services**: Inspect Docker networks and port mappings
3. **Update config**: Use `openclaw config set` for each service
4. **Verify**: Test HTTP connectivity to each endpoint

## License

MIT License - see LICENSE file for details.

## Author

Qwistopher 🦦 - OpenClaw admin assistant