# Reliability Evidence Pack (REP)

A comprehensive runtime system for documenting and verifying agent operational reliability through structured artifact recording, validation, and compliance reporting.

## What's Included

### Core Scripts (`/scripts`)
- `rep.mjs` - Main CLI for initialization, validation, and bundle management
- `rep-validate.mjs` - Schema validation engine for REP artifacts
- `rep-heartbeat-cron.mjs` - Records agent heartbeats on a schedule
- `rep-near-miss-cron.mjs` - Tracks near-miss reliability events
- `rep-performance-baseline.mjs` - Captures performance metrics
- `rep-generate-bundle.mjs` - Generates REP bundles from artifacts

### CLI Package (`/cli`)
- Installable npm package for convenient command-line access
- See `cli/README.md` for installation and usage

### GitHub Action (`/github-action`)
- CI/CD integration for automated validation
- See `github-action/README.md` for setup

### Schemas (`/schemas`)
- JSON Schema definitions for all REP artifact types:
  - `decision_rejection_log.json`
  - `handoff_acceptance_packet.json`
  - `memory_reconstruction_audit.json`
  - `near_miss_reliability_trailer.json`
  - `signed_divergence_violation_record.json`

### Examples (`/examples`)
- Sample artifacts and workflows
- Integration patterns for different use cases

## Required Binaries

- **Node.js** (v16 or higher - required for runtime scripts)
- **npm** (for CLI package installation)

No other system binaries required.

## Installation

### Option 1: Direct Scripts
```bash
# Clone or copy this bundle to your project
cp -r rep-bundle-v2 /path/to/your/project/rep
cd rep

# Make scripts executable
chmod +x scripts/*.mjs

# Test
node scripts/rep.mjs --help
```

### Option 2: CLI Package
```bash
cd cli
npm install -g
rep --help
```

### Option 3: GitHub Action
```yaml
- uses: ./github-action
  with:
    bundle-path: ./rep
```

## Configuration

Set environment variables to configure behavior:

```bash
# Path to artifacts directory (default: ./artifacts)
REP_ARTIFACTS_PATH=./artifacts

# Path to schemas directory (default: ./schemas)  
REP_SCHEMAS_PATH=./schemas

# Log file path (optional)
REP_LOG_FILE=/var/log/rep.log
```

## Usage

### Initialize a new REP
```bash
node scripts/rep.mjs init --name "my-agent"
```

### Validate artifacts
```bash
node scripts/rep-validate.mjs ./artifacts --strict
```

### Run heartbeat recording (cron)
```bash
REP_ARTIFACTS_PATH=./artifacts node scripts/rep-heartbeat-cron.mjs
```

### Set up cron (example for crontab)
```bash
# Add to crontab - run heartbeat every 5 minutes
*/5 * * * * cd /path/to/rep && REP_ARTIFACTS_PATH=./artifacts node scripts/rep-heartbeat-cron.mjs >> /var/log/rep-heartbeat.log 2>&1
```

## Artifact Types

| Artifact | Purpose |
|----------|---------|
| `agent_heartbeat_record` | Agent lifecycle events |
| `decision_rejection_log` | Decisions and their outcomes |
| `context_snapshot` | Memory/context state |
| `handoff_acceptance_packet` | Inter-agent handoff validation |
| `near_miss_reliability_trailer` | Near-miss events |
| `memory_reconstruction_audit` | Memory integrity checks |
| `signed_divergence_violation_record` | Policy violations |

## Security Considerations

- **Credentials**: This skill does not require or handle credentials
- **File Access**: Writes to configured artifacts directory only
- **Cron**: Does not modify system crontab - operator must configure
- **Logs**: Optional logging to configurable path

## License

MIT

## Support

- Documentation: `SPEC.md`, `QUICKSTART.md`, `INTEGRATION.md`
- Examples: `examples/`
- Validation: `node scripts/rep-validate.mjs --help`

## Security Considerations

### Sensitive Data
REP captures context snapshots, decision logs, and memory-like artifacts that may contain sensitive information.
- Set `REP_ARTIFACTS_PATH` to an isolated, access-controlled directory
- Review or redact artifacts before sharing externally
- Consider running in a container or unprivileged account

### Signing Keys
The SPEC includes signature fields for artifact integrity, but key management is operator-defined:
- Do NOT place private keys in the artifacts directory
- Use external KMS or secure vault for production signing
- For testing, generate keys externally and pass via environment (future feature)

### CI Usage
The GitHub Action is local to your repository:
- Review `github-action/entrypoint.sh` before use in public CI
- Ensure no artifacts leak to external endpoints
- Use isolated artifact paths in CI environments

### Network Behavior
All scripts operate locally:
- No telemetry or external API calls
- No automatic updates
- All file I/O is to configured artifact paths only

### Best Practices
1. Keep artifacts directory separate from source code
2. Add artifact paths to `.gitignore`
3. Rotate logs regularly
4. Audit artifacts before external sharing
