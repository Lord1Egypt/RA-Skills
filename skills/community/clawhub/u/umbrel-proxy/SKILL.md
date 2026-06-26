---
name: umbrel-proxy
description: Efficiently manage and interact with Umbrel proxy services for Docker containers. Automatically discovers running services, maps internal Docker IPs to accessible host ports, and updates OpenClaw config.
version: 1.0.0
author: Qwistopher
---

# Umbrel Proxy Manager

A skill to efficiently manage Umbrel proxy services for Docker containers. Automatically discovers running services, maps internal Docker IPs to accessible host ports, and updates OpenClaw config.

## Problem Solved

Umbrel runs Docker containers with internal networking (10.21.0.x) and exposes them via app proxy containers on localhost ports. This skill:
1. **Discovers** all Umbrel proxy services
2. **Maps** internal Docker IPs to accessible host ports  
3. **Updates** OpenClaw config automatically
4. **Tests** connectivity to ensure services work

## When to Use

- After Docker container restarts
- When services become unreachable
- During OpenClaw setup/configuration
- When adding new Umbrel apps
- For troubleshooting service connectivity

## Quick Commands

```bash
# Simple sync (recommended) - checks OpenClaw-relevant services only
bash scripts/simple_umbrel_sync.sh

# Advanced discovery (all services)
python3 scripts/discover_umbrel_services.py

# Test connectivity
python3 scripts/test_connectivity.py
```

## Files

- `scripts/discover_umbrel_services.py` - Discovers Umbrel proxy services
- `scripts/update_openclaw_config.py` - Updates OpenClaw config
- `scripts/test_connectivity.py` - Tests service connectivity
- `scripts/umbrel_proxy_sync.sh` - One-shot sync script

## Integration

The skill automatically integrates with OpenClaw's plugin system. After running the sync script, restart the gateway:

```bash
openclaw gateway restart
```

## Example Output

```
=== Umbrel Proxy Discovery ===
Found 2 proxy services:
1. perplexica: 10.21.0.x:3000 → localhost:3444 (via app proxy)
2. searxng: 10.21.0.x:8080 → localhost:8182 (via app proxy)

=== OpenClaw Config Update ===
Updated perplexica.baseUrl: http://localhost:3444 ✓
Updated searxng.baseUrl: http://localhost:8182 ✓

=== Connectivity Test ===
perplexica: ✓ (200 OK)
searxng: ✓ (200 OK)
```

## Auto-Discovery Logic

1. **Find proxy containers**: `docker ps | grep app-proxy`
2. **Map internal services**: Inspect Docker networks and port mappings
3. **Update config**: Use `openclaw config set` for each service
4. **Verify**: Test HTTP connectivity to each endpoint

## Common Services

| Service | Internal IP Pattern | Proxy Port Example | OpenClaw Plugin |
|---------|---------------------|-------------------|-----------------|
| Perplexica | 10.21.0.x:3000 | 3444 | perplexica |
| SearXNG | 10.21.0.x:8080 | 8182 | searxng |
| Jellyfin | 10.21.0.x:8096 | 8096 | (if configured) |
| OpenWebUI | 10.21.0.x:8080 | 3000 | (if configured) |

## Verification Test

To verify the skill is working correctly:

```bash
cd skills/umbrel-proxy
bash scripts/simple_umbrel_sync.sh
```

Expected output:
- Docker is running ✓
- Services checked: 4 + matrix
- perplexica: http://localhost:3444 ✓
- searxng: http://localhost:8182 ✓  
- synapse: http://localhost:8008 ✓
- OpenClaw config updates applied as needed

## Troubleshooting

If services aren't discovered:
1. Check Docker is running: `docker ps`
2. Verify Umbrel app proxy containers: `docker ps | grep app-proxy`
3. Check network connectivity: `ping 10.21.0.1` (Umbrel Docker gateway)

If config updates fail:
1. Ensure OpenClaw isn't running: `openclaw gateway stop`
2. Check permissions: `ls -la ~/.openclaw/openclaw.json` (or your OpenClaw config path)
3. Use verbose mode: `python3 scripts/update_openclaw_config.py --verbose`

## Example Test Results

✅ **Skill verified working:**
- All scripts executable and functional
- Services discovered: Multiple Umbrel services mapped
- OpenClaw config correctly updated for relevant plugins
- Connectivity confirmed for discovered services