---
name: victoriametrics
description: Query and manage VictoriaMetrics time-series database instances. Supports both single-node and cluster deployments with multi-tenancy. Use when the user asks about metrics, monitoring, PromQL queries, VictoriaMetrics, time-series data, or mentions "vmselect", "vminsert", "vmstorage", or needs to query monitoring metrics from VictoriaMetrics instances. Also use for common monitoring tasks like checking CPU usage, memory, disk space, GPU metrics, service health, or custom PromQL queries.
---

# VictoriaMetrics

Query and manage VictoriaMetrics time-series database instances. Supports both single-node and cluster deployments with multi-tenancy.

## Security Notice

This skill requires the following permissions for legitimate functionality:

- **HTTP/HTTPS requests**: Query VictoriaMetrics API endpoints
- **File system access**: Read configuration files (`victoriametrics.json`)
- **Base64 encoding**: HTTP Basic Authentication for secure API access

All network operations are user-initiated and only connect to user-configured VictoriaMetrics instances. No data is sent to external services.

## Quick Start

### 1. Initial Setup

Run the interactive configuration wizard:

```bash
cd ~/.openclaw/workspace/skills/victoriametrics
node scripts/cli.js init
```

This will create a `victoriametrics.json` config file in your OpenClaw workspace (`~/.openclaw/workspace/victoriametrics.json`).

### 2. Start Querying

```bash
# Query default instance
node scripts/cli.js query 'up'

# Query all instances at once
node scripts/cli.js query 'up' --all

# List configured instances
node scripts/cli.js instances
```

## Configuration

### Config File Location

By default, the skill looks for config in your OpenClaw workspace:

```
~/.openclaw/workspace/victoriametrics.json
```

Priority order:

1. Path from `VICTORIAMETRICS_CONFIG` environment variable
2. `~/.openclaw/workspace/victoriametrics.json`
3. `~/.openclaw/workspace/config/victoriametrics.json`
4. `./victoriametrics.json` (current directory)
5. `~/.config/victoriametrics/config.json`

### Config Format

Create `victoriametrics.json` in your workspace (or use `node cli.js init`):

#### Single-Node Deployment

```json
{
  "instances": [
    {
      "name": "production",
      "type": "single",
      "url": "http://victoriametrics:8428",
      "user": "admin",
      "password": "secret"
    }
  ],
  "default": "production"
}
```

#### Cluster Deployment (Multi-Tenant)

```json
{
  "instances": [
    {
      "name": "cluster-prod",
      "type": "cluster",
      "url": "http://vmselect:8481",
      "accountID": 0,
      "user": "admin",
      "password": "secret"
    },
    {
      "name": "cluster-tenant42",
      "type": "cluster",
      "url": "http://vmselect:8481",
      "accountID": 42,
      "projectID": 9
    }
  ],
  "default": "cluster-prod"
}
```

**Fields:**

- `name` — unique identifier for the instance
- `type` — `"single"` or `"cluster"` (default: `"single"`)
- `url` — VictoriaMetrics server URL
  - Single-node: `http://victoriametrics:8428`
  - Cluster: `http://vmselect:8481`
- `accountID` — tenant account ID (cluster only, default: 0)
- `projectID` — tenant project ID (cluster only, optional)
- `user` / `password` — optional HTTP Basic Auth credentials
- `default` — which instance to use when none specified

### Environment Variables (Legacy)

For single-instance setups, you can use environment variables:

```bash
export VICTORIAMETRICS_URL=http://victoriametrics:8428
export VICTORIAMETRICS_USER=admin
export VICTORIAMETRICS_PASSWORD=secret
```

## Usage

### Global Flags

| Flag | Description |
|------|-------------|
| `-c, --config <path>` | Path to config file |
| `-i, --instance <name>` | Target specific instance |
| `-a, --all` | Query all configured instances |

### Commands

#### Setup

```bash
# Interactive configuration wizard
node scripts/cli.js init
```

#### Query Metrics

```bash
cd ~/.openclaw/workspace/skills/victoriametrics

# Query default instance
node scripts/cli.js query 'up'

# Query specific instance
node scripts/cli.js query 'up' -i cluster-prod

# Query ALL instances at once
node scripts/cli.js query 'up' --all

# Custom config file
node scripts/cli.js query 'up' -c /path/to/config.json
```

#### Common Queries

**Disk space usage:**
```bash
node scripts/cli.js query '100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)' --all
```

**CPU usage:**
```bash
node scripts/cli.js query '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)' --all
```

**Memory usage:**
```bash
node scripts/cli.js query '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100' --all
```

**Load average:**
```bash
node scripts/cli.js query 'node_load1' --all
```

**GPU memory usage (NVIDIA):**
```bash
node scripts/cli.js query 'nvidia_gpu_memory_used_bytes / nvidia_gpu_memory_total_bytes * 100' --all
```

**GPU temperature:**
```bash
node scripts/cli.js query 'nvidia_gpu_temperature_celsius' --all
```

### List Configured Instances

```bash
node scripts/cli.js instances
```

Output:
```json
{
  "default": "cluster-prod",
  "instances": [
    {
      "name": "cluster-prod",
      "type": "cluster",
      "url": "http://vmselect:8481",
      "accountID": 0,
      "hasAuth": true
    },
    {
      "name": "single-dev",
      "type": "single",
      "url": "http://localhost:8428",
      "hasAuth": false
    }
  ]
}
```

### Other Commands

```bash
# List all metrics matching pattern
node scripts/cli.js metrics 'node_memory_*'

# Get label names
node scripts/cli.js labels --all

# Get values for a label
node scripts/cli.js label-values instance --all

# Find time series
node scripts/cli.js series '{__name__=~"node_cpu_.*", instance=~".*:9100"}' --all

# Get active alerts
node scripts/cli.js alerts --all

# Check instance health
node scripts/cli.js health -i cluster-prod
```

## Multi-Instance Output Format

When using `--all`, results include data from all instances:

```json
{
  "resultType": "vector",
  "results": [
    {
      "instance": "cluster-prod",
      "status": "success",
      "resultType": "vector",
      "result": [...]
    },
    {
      "instance": "single-dev",
      "status": "success",
      "resultType": "vector",
      "result": [...]
    }
  ]
}
```

Errors on individual instances don't fail the entire query — they appear with `"status": "error"` in the results array.

## Deployment Types

### Single-Node

- Simpler setup and operation
- URL format: `http://<victoriametrics>:8428/api/v1/query`
- Suitable for ingestion rates < 1M data points per second
- Can be set up in High Availability mode

### Cluster

- Horizontal scalability
- URL format: `http://<vmselect>:8481/select/<accountID>/prometheus/api/v1/query`
- Multi-tenancy support via accountID and projectID
- Components: vmstorage, vminsert, vmselect
- Each component scales independently

## Supported Metric Collectors

This skill supports multiple metric collection agents:

- **node_exporter** - Standard Prometheus node exporter
- **categraf** - Flashcat's telemetry collector
- **DCGM** - NVIDIA GPU metrics
- **Custom exporters** - Any Prometheus-compatible exporter

### Quick Comparison

| Metric Type | node_exporter | categraf |
|-------------|---------------|----------|
| CPU Usage | `100 - avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100` | `cpu_usage_active{cpu="cpu-total"}` |
| Memory Usage | `(1 - node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes) * 100` | `mem_used_percent` |
| Disk Usage | `100 - (node_filesystem_avail_bytes/node_filesystem_size_bytes * 100)` | `disk_used_percent` |
| System Load | `node_load1` | `system_load1` |

### Universal Queries (Auto-detect)

```bash
# CPU usage (works with both node_exporter and categraf)
node scripts/cli.js query 'cpu_usage_active{cpu="cpu-total"} or (100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100))'

# Memory usage (works with both)
node scripts/cli.js query 'mem_used_percent or ((node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100)'

# Disk usage (works with both)
node scripts/cli.js query 'disk_used_percent or (100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100))'
```

For complete query examples for all metric types, see [references/common_queries.md](references/common_queries.md).

## Common Queries Reference

### node_exporter Metrics

| Metric | PromQL Query |
|--------|--------------|
| Disk free % | `node_filesystem_avail_bytes / node_filesystem_size_bytes * 100` |
| Disk used % | `100 - (node_filesystem_avail_bytes / node_filesystem_size_bytes * 100)` |
| CPU idle % | `avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100` |
| Memory used % | `(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100` |
| Network RX | `rate(node_network_receive_bytes_total[5m])` |
| Network TX | `rate(node_network_transmit_bytes_total[5m])` |
| Uptime | `node_time_seconds - node_boot_time_seconds` |
| Service up | `up` |

### categraf Metrics

| Metric | PromQL Query |
|--------|--------------|
| CPU usage % | `cpu_usage_active{cpu="cpu-total"}` |
| Memory used % | `mem_used_percent` |
| Disk used % | `disk_used_percent` |
| Network RX | `rate(net_bytes_recv[5m])` |
| Network TX | `rate(net_bytes_sent[5m])` |
| System load 1m | `system_load1` |
| System uptime | `system_uptime` |

### GPU Metrics (DCGM)

| Metric | PromQL Query |
|--------|--------------|
| GPU memory used % | `DCGM_FI_DEV_FB_USED / (DCGM_FI_DEV_FB_FREE + DCGM_FI_DEV_FB_USED) * 100` |
| GPU temperature | `DCGM_FI_DEV_GPU_TEMP` |
| GPU utilization | `DCGM_FI_DEV_GPU_UTIL` |
| GPU power usage | `DCGM_FI_DEV_POWER_USAGE` |

## Notes

- Time range defaults to last 1 hour for instant queries
- Use range queries `[5m]` for rate calculations
- All queries return JSON with `data.result` containing the results
- Instance labels typically show `host:port` format
- When using `--all`, queries run in parallel for faster results
- Config is stored outside the skill directory so it persists across skill updates
- For cluster deployments, the accountID and projectID are automatically inserted into the URL path

## VictoriaMetrics API Differences

VictoriaMetrics is compatible with Prometheus API but includes additional features:

- **MetricsQL**: Extended PromQL with additional functions
- **Multi-tenancy**: Native support in cluster mode
- **High cardinality**: Better performance with many time series
- **Storage efficiency**: Better compression than Prometheus

For detailed API documentation, see [references/api_reference.md](references/api_reference.md).
