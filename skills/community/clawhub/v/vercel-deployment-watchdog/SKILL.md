---
name: vercel-deployment-watchdog
description: Monitor Vercel-hosted site deployments with automated health checks, cache freshness verification, and API validation. Use when you need to ensure deployments succeed and sites remain healthy after updates. Integrates with Vercel API to detect new deployments and run comprehensive post-deployment checks.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "jq"], "env": ["VERCEL_TOKEN"] },
        "credentials": ["VERCEL_TOKEN"],
        "install":
          [
            {
              "id": "check-deps",
              "kind": "manual",
              "instructions": "Ensure curl and jq are installed. On Debian/Ubuntu: sudo apt-get install curl jq. On macOS: brew install curl jq.",
              "bins": ["curl", "jq"],
              "label": "Check for curl and jq dependencies",
            },
          ],
      },
  }
---

# Vercel Deployment Watchdog Skill

**⚠️ SECURITY & USAGE DISCLAIMER**

This skill is designed **exclusively** for monitoring your own web applications and deployments. It must not be used to probe, scan, or monitor any systems you do not own or have explicit permission to test.

**Permitted Use:**
- Monitoring your own websites and APIs deployed on Vercel or similar platforms
- Automated health checks for deployments you control
- Integration with your own alerting systems (Telegram, etc.)

**Prohibited Use:**
- Scanning third-party websites without authorization
- Attempting to access private/internal networks
- Testing systems you do not own or manage
- Any activity that could be considered unauthorized access or harassment

By using this skill, you agree to use it only for legitimate monitoring of your own infrastructure.

## Skill Overview

Automated deployment monitoring for Vercel-hosted applications. This skill provides:

1. **Post-deployment health checks**: Verify HTTP status, cache freshness, content validation
2. **Vercel API integration**: Detect new deployments automatically
3. **Feed validation**: Check API endpoints return valid JSON with expected data
4. **Cron job setup**: Schedule regular checks or trigger on deployment completion
5. **Alerting integration**: Configure OpenClaw cron jobs to send failure notifications via Telegram/WhatsApp or webhooks (delivery handled by OpenClaw platform)

## 🔒 Security & Compliance

### Built-in Safety Features

The skill includes multiple security measures:

1. **URL Validation**: All URLs are validated to:
   - Require `http://` or `https://` protocol
   - Warn/block localhost addresses (`localhost`, `127.0.0.1`, `0.0.0.0`)
   - Can be configured to block private IP ranges (RFC 1918)
   - Allow monitoring of internal resources via `ALLOW_INTERNAL=true` environment variable (requires explicit opt-in; no CLI bypass flags)
   - **Security Warning**: Only enable `ALLOW_INTERNAL=true` if you need to monitor localhost/private IPs and have explicit permission. Enabling it allows network access to internal addresses.

2. **Credential Safety**:
   - Never hardcodes API tokens or secrets
   - Accepts tokens via environment variables (primary) or CLI arguments
   - Scripts do not log sensitive credentials

3. **Network Restrictions**:
   - No outbound network calls to private IP ranges by default
   - Configurable timeout limits for HTTP requests
   - Rate limiting recommendations included

### Compliance with ClawHub Policies

This skill:
- Does **not** attempt to bypass security controls
- Does **not** include obfuscated or hidden functionality
- Is **open source** and transparent about all operations
- Respects `robots.txt` and common web standards
- Follows the principle of least privilege

### Responsible Usage Requirements

You must:
1. Have explicit permission to monitor all target URLs
2. Use your own API tokens with minimal required scopes
3. Respect rate limits of monitored services
4. Not use this skill for surveillance or harassment
5. Comply with all applicable laws and terms of service

Violation of these terms may result in removal from ClawHub and suspension of your account.

## Quick Start

### 1. Prerequisites

```bash
# Check if curl and jq are installed
command -v curl >/dev/null 2>&1 && command -v jq >/dev/null 2>&1 || {
    echo "Error: curl and jq are required but not installed."
    echo "Install them using your system package manager:"
    echo "  Debian/Ubuntu: sudo apt-get install curl jq"
    echo "  macOS: brew install curl jq"
    echo "  For other systems, see: https://curl.se/ and https://stedolan.github.io/jq/"
    exit 1
}
```

### 2. Set up Environment Variables

Create a `.env` file or set environment variables:

```bash
# Vercel API token (create at https://vercel.com/account/tokens)
export VERCEL_TOKEN="vcp_..."

# Target URLs to monitor
export HOMEPAGE_URL="https://your-site.com/"
export API_FEED_URL="https://your-site.com/api/feed"

# Optional: Telegram chat ID for OpenClaw cron notifications (not used by scripts)
export TELEGRAM_CHAT_ID="YOUR_TELEGRAM_CHAT_ID"

# Security: Only set ALLOW_INTERNAL=true if monitoring localhost/private IPs
# export ALLOW_INTERNAL="true"
```

### 3. Run Manual Check

```bash
# Make script executable
chmod +x scripts/watchdog-check.sh

# Run check
./scripts/watchdog-check.sh --homepage "$HOMEPAGE_URL" --api "$API_FEED_URL"
```

### 4. Schedule Monitoring with OpenClaw Cron (Recommended)

For safe and integrated scheduling, use OpenClaw's built-in cron system instead of system cron:

```javascript
// Create an OpenClaw cron job (every 5 minutes)
{
  "name": "Vercel Watchdog",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "payload": {
    "kind": "agentTurn",
    "message": "Run deployment watchdog check for my site"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "YOUR_TELEGRAM_CHAT_ID"
  }
}
```

See the "Integration with OpenClaw" section below for more details.

## Features

### Health Check Components

1. **HTTP Status Verification**: Ensures homepage and API return 200 OK
2. **Cache Freshness**: Checks `age: 0` and `x-vercel-cache: MISS` headers
3. **Content Validation**: Verifies page title contains expected text
4. **JSON Feed Validation**: Validates API response structure and data integrity
5. **Deployment Detection**: Uses Vercel API to find latest deployments

### Vercel API Integration

The skill can:
- List recent deployments to detect new ones
- Check deployment state (`READY`, `ERROR`, `BUILDING`)
- Get deployment URLs and metadata
- Trigger health checks when deployment state changes to `READY`

### Alerting

When checks fail, the skill can:
- Send Telegram messages via OpenClaw
- Log detailed failure information
- Include remediation suggestions
- Escalate after repeated failures

## Usage Examples

### Basic Health Check

```bash
./scripts/watchdog-check.sh --homepage "https://your-site.com" --api "https://your-site.com/api/feed"
```

### Vercel Deployment Monitoring

The script uses the `VERCEL_TOKEN` environment variable automatically, or you can pass it explicitly via `--token`.

```bash
# Check for new deployments in the last 10 minutes
./scripts/vercel-monitor.sh --project "your-project" --since 10m
```



## Script Reference

### `scripts/watchdog-check.sh`

Main health check script with the following options:

```bash
--homepage URL    # Homepage URL to check (default: https://your-site.com/)
--api URL         # API feed URL to check (default: https://your-site.com/api/feed)
--verbose         # Enable verbose output
--json            # Output results as JSON for programmatic use
```

### `scripts/vercel-monitor.sh`

Vercel API integration script:

```bash
--token TOKEN     # Vercel API token (required)
--project NAME    # Project name to monitor (default: auto-detect)
--since MINUTES   # Check deployments from last N minutes (default: 5)
--team-id ID      # Team ID for organization accounts
```



## Integration with OpenClaw

**Note**: This skill provides monitoring scripts that output results to stdout. Notifications are handled by OpenClaw's cron delivery system (`delivery.mode: "announce"`) when configured, not by the scripts themselves. The scripts do not make external API calls for notifications.

### As a Cron Job

Set up the skill to run periodically via OpenClaw's cron system:

```javascript
// Example cron job configuration
{
  "name": "Vercel Watchdog",
  "schedule": { "kind": "every", "everyMs": 300000 }, // Every 5 minutes
  "payload": {
    "kind": "agentTurn",
    "message": "Run deployment watchdog check and notify if any failures"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "YOUR_TELEGRAM_CHAT_ID"
  }
}
```

### As a Sub-Agent

Spawn a sub-agent to handle monitoring:

```bash
# Use OpenClaw sessions_spawn to run monitoring in background
openclaw sessions spawn --task "Monitor your site deployment health for next hour" --runtime subagent --label deployment-watchdog
```

## Troubleshooting

### Common Issues

1. **Vercel API authentication fails**:
   - Ensure token has `deployment:read` scope
   - Check if token is expired (create new one at https://vercel.com/account/tokens)

2. **Cache freshness indicators missing**:
   - Deployment might be cached by CDN
   - Wait a few minutes and retry
   - Check Vercel project settings for cache headers

3. **API feed validation fails**:
   - Verify API endpoint is accessible
   - Check CORS settings if accessing from different domain
   - Validate JSON structure with `jq . <(curl -s API_URL)`

### Debug Mode

Enable verbose output to see detailed check results:

```bash
./scripts/watchdog-check.sh --verbose
```

## Extending the Skill

### Adding New Checks

1. Add check function to `scripts/watchdog-check.sh`
2. Update summary output
3. Test with `--verbose` flag

### Integrating with Other Services

- **Slack notifications**: Add webhook integration
- **Email alerts**: Use `himalaya` CLI or `gog` skill
- **Dashboard integration**: Output JSON for external monitoring systems

## References

See `references/` directory for:
- Vercel API documentation
- HTTP cache header specifications
- JSON schema validation examples
- OpenClaw cron job configuration guide