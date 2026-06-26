# REP Integration Guide

This guide covers integrating the Reliability Evidence Pack (REP) into your agent operations.

## Quick Start

```bash
# 1. Copy REP bundle to your project
cp -r rep-bundle-v2 /path/to/your/project/rep

# 2. Initialize
cd rep
node scripts/rep.mjs init --name "my-agent"

# 3. Validate
node scripts/rep-validate.mjs ./artifacts
```

## Cron Setup

### Heartbeat Recording (every 5 minutes)

```bash
# Option 1: Direct Node
*/5 * * * * cd /path/to/rep && REP_ARTIFACTS_PATH=./artifacts node scripts/rep-heartbeat-cron.mjs >> /var/log/rep-heartbeat.log 2>&1

# Option 2: Shell script
*/5 * * * * cd /path/to/rep && ./scripts/rep-heartbeat-cron.sh >> /var/log/rep-heartbeat.log 2>&1
```

### Near-Miss Tracking (every hour)

```bash
0 * * * * cd /path/to/rep && REP_ARTIFACTS_PATH=./artifacts node scripts/rep-near-miss-cron.mjs >> /var/log/rep-near-miss.log 2>&1
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REP_ARTIFACTS_PATH` | `./artifacts` | Where to write artifact files |
| `REP_SCHEMAS_PATH` | `./schemas` | Where schemas are stored |
| `REP_LOG_FILE` | stdout | Log output path |

## File Paths

All paths in REP are relative to the bundle root. Configure by setting environment variables:

```bash
REP_ARTIFACTS_PATH=/var/lib/rep/artifacts node scripts/rep-heartbeat-cron.mjs
```

## GitHub Actions Integration

See `github-action/README.md` for CI/CD setup.

## Validation in CI

```yaml
name: REP Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./rep/github-action
        with:
          bundle-path: ./rep
```

## CLI Package

For convenient access:

```bash
cd cli
npm install -g
rep init --name my-agent
rep validate ./artifacts
```

## Permissions

- **Read**: Schemas, artifacts (configurable)
- **Write**: Artifacts directory, logs (configurable)
- **No**: System crontab, credentials, or elevated privileges

## Troubleshooting

### "command not found: node"
Install Node.js v14+: https://nodejs.org

### "Schema not found"
Set `REP_SCHEMAS_PATH` to your schemas directory.

### Permission denied
Ensure the artifacts directory is writable:
```bash
mkdir -p /path/to/artifacts
chmod 755 /path/to/artifacts
```
