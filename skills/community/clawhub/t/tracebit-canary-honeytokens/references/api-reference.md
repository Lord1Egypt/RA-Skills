# Alternative: API-Based Deployment

> **Note:** The Tracebit CLI (`tracebit deploy all`) is the **recommended** deployment method. The CLI runs a background daemon that auto-refreshes credentials — true "set and forget" protection.
>
> Use the API only if the CLI cannot be installed in your environment (e.g., restricted systems, containerized agents, CI/CD pipelines).
>
> **Key limitation of API-only deployment:** credentials expire and you must manually rotate them. The CLI's background daemon handles this automatically.

---

**Base URL:** `https://community.tracebit.com`  
**Auth:** Bearer token in `Authorization` header

## Table of Contents
1. [Getting an API Token](#getting-an-api-token)
2. [Issue Credentials](#issue-credentials)
3. [Confirm Credentials](#confirm-credentials)
4. [Credential Types & Fields](#credential-types--fields)
5. [Labels and Metadata](#labels-and-metadata)
6. [Error Handling](#error-handling)
7. [Rate Limits & Quotas](#rate-limits--quotas)
8. [Full Deployment Script](#full-deployment-script)

---

## Getting an API Token

**Via the web dashboard** (if you have browser access):
1. Go to https://community.tracebit.com → Settings → API Keys → Create Key
2. Copy the token and store it securely

**Via the CLI** (if you have it):
```bash
tracebit auth   # browser OAuth, writes token to the standard Tracebit config directory
cat "$HOME/.config/tracebit/token"
```

Store the token:
```bash
TRACEBIT_CONFIG="$HOME/.config/tracebit"
mkdir -p "$TRACEBIT_CONFIG" && echo "your-api-token" > "$TRACEBIT_CONFIG/token"
chmod 600 "$TRACEBIT_CONFIG/token"
```

Or set as an environment variable:
```bash
export TRACEBIT_API_TOKEN="your-api-token"
```

---

## Issue Credentials

Issues new canary credentials. Each call creates fresh credentials with a confirmation ID.

**Endpoint:** `POST /api/v1/credentials/issue-credentials`

**Request Body:**
```json
{
  "name": "string",
  "types": ["aws", "ssh", "gitlab-cookie", "gitlab-username-password"],
  "source": "string",
  "sourceType": "string",
  "labels": [
    {"name": "string", "value": "string"}
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Human-readable name for this canary set |
| `types` | array | yes | One or more credential types to issue (see below) |
| `source` | string | no | Where the canary is being deployed |
| `sourceType` | string | no | Type of source (`"endpoint"`, `"file"`, `"env"`) |
| `labels` | array | no | Key-value metadata for filtering in the dashboard |

**Example:**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $TRACEBIT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "agent-canary",
    "types": ["aws", "ssh"],
    "source": "openclaw-skill",
    "sourceType": "endpoint",
    "labels": [
      {"name": "agent", "value": "openclaw"},
      {"name": "purpose", "value": "prompt-injection-detection"}
    ]
  }' \
  "https://community.tracebit.com/api/v1/credentials/issue-credentials"
```

**Response (200/201):**
```json
{
  "aws": {
    "awsAccessKeyId": "ASIA...",
    "awsSecretAccessKey": "...",
    "awsSessionToken": "...",
    "awsExpiration": "2026-04-15T13:00:00Z",
    "awsConfirmationId": "uuid-here"
  },
  "ssh": {
    "sshIp": "1.2.3.4",
    "sshPrivateKey": "-----BEGIN RSA PRIVATE KEY-----\n...",
    "sshPublicKey": "ssh-rsa AAAA...",
    "sshExpiration": "2026-04-15T13:00:00Z",
    "sshConfirmationId": "uuid-here"
  }
}
```

Only fields for requested types are present.

---

## Confirm Credentials

**Must be called after issuing**, or alerts will not fire.

**Endpoint:** `POST /api/v1/credentials/confirm-credentials`

**Request Body:**
```json
{"id": "uuid-from-confirmationId"}
```

**Example:**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $TRACEBIT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "550e8400-e29b-41d4-a716-446655440000"}' \
  "https://community.tracebit.com/api/v1/credentials/confirm-credentials"
```

**Response:** `204 No Content` on success.

**Must confirm each type separately.** If you issued AWS + SSH, call confirm-credentials twice — once with `awsConfirmationId`, once with `sshConfirmationId`.

---

## Credential Types & Fields

### `aws` — AWS Session Tokens

| Field | Description |
|-------|-------------|
| `awsAccessKeyId` | Access key ID (starts with `ASIA`) |
| `awsSecretAccessKey` | Secret access key |
| `awsSessionToken` | Session token (required for STS-based credentials) |
| `awsExpiration` | ISO8601 expiry date |
| `awsConfirmationId` | UUID — pass to confirm-credentials to activate alerts |

Write to the standard AWS credentials file as a named `[canary]` profile:
```ini
[canary]
aws_access_key_id = ASIA...
aws_secret_access_key = ...
aws_session_token = ...
```

### `ssh` — SSH Key Pairs

| Field | Description |
|-------|-------------|
| `sshIp` | IP address of the canary SSH server |
| `sshPrivateKey` | PEM-encoded private key |
| `sshPublicKey` | OpenSSH-format public key |
| `sshExpiration` | ISO8601 expiry date |
| `sshConfirmationId` | UUID — pass to confirm-credentials to activate alerts |

Write to the standard SSH directory as `tracebit-canary` with `chmod 600`.

### `gitlab-cookie` — Browser Session Cookies

Returns an `http` object with cookie canary details. Use for browser-based deployments.

### `gitlab-username-password` — Username/Password Pairs

Returns an `http` object with username/password canary details. Use in password managers, `.env` files, etc.

---

## Labels and Metadata

Labels appear in the Tracebit dashboard and alert emails. Use them to identify:

- **Which agent** deployed the canary: `{"name": "agent", "value": "openclaw"}`
- **Purpose**: `{"name": "purpose", "value": "prompt-injection-detection"}`
- **Environment**: `{"name": "env", "value": "production"}`

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| `200`/`201` | Success | Parse response |
| `204` | No Content (confirm success) | Done |
| `400` | Bad request | Check request body format |
| `401` | Unauthorized | Token invalid — re-authenticate |
| `403` | Forbidden | Insufficient permissions / quota exceeded |
| `429` | Rate limited | Wait and retry with backoff |
| `500` | Server error | Retry after a delay |

---

## Rate Limits & Quotas

Community Edition limits are not publicly documented. Best practices:

- Issue all needed canary types in a **single API call** — don't loop
- Confirm each credential promptly after issuing
- Rotate on a schedule (weekly/monthly) rather than constantly re-issuing
- On 429: back off exponentially — wait 5s, 10s, 30s between retries

---

## Full Deployment Script

A complete bash script for API-based deployment (when CLI isn't available):

```bash
#!/usr/bin/env bash
# API-based canary deployment (fallback — prefer: tracebit deploy all)
set -euo pipefail

TRACEBIT_CONFIG="${HOME}/.config/tracebit"
TOKEN="${TRACEBIT_API_TOKEN:-$(cat "$TRACEBIT_CONFIG/token" 2>/dev/null)}"
[[ -z "$TOKEN" ]] && { echo "ERROR: No API token. Set TRACEBIT_API_TOKEN or run tracebit auth"; exit 1; }

API="https://community.tracebit.com"

# Issue credentials (all types in one call)
echo "Issuing canary credentials..."
RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "agent-canary",
    "types": ["aws", "ssh"],
    "source": "openclaw-skill",
    "sourceType": "endpoint",
    "labels": [{"name": "agent", "value": "openclaw"}]
  }' \
  "$API/api/v1/credentials/issue-credentials")

echo "$RESPONSE" > "$TRACEBIT_CONFIG/canaries.json"
chmod 600 "$TRACEBIT_CONFIG/canaries.json"

# Confirm each type
for CONFIRM_FIELD in awsConfirmationId sshConfirmationId; do
  ID=$(echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for section in data.values():
    if isinstance(section, dict) and '$CONFIRM_FIELD' in section:
        print(section['$CONFIRM_FIELD'])
        break
" 2>/dev/null || true)
  
  if [[ -n "$ID" ]]; then
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "{\"id\": \"$ID\"}" \
      "$API/api/v1/credentials/confirm-credentials")
    echo "Confirmed $CONFIRM_FIELD: HTTP $STATUS"
  fi
done

# Deploy AWS credentials
AWS_KEY=$(echo "$RESPONSE" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('aws',{}).get('awsAccessKeyId',''))" 2>/dev/null)
AWS_SECRET=$(echo "$RESPONSE" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('aws',{}).get('awsSecretAccessKey',''))" 2>/dev/null)
AWS_TOKEN=$(echo "$RESPONSE" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('aws',{}).get('awsSessionToken',''))" 2>/dev/null)

# ⚠️ Credential placement requires explicit human confirmation.
# The response JSON contains decoy canary credentials (fake — they alert on use).
# Place them in the standard credential locations for each type.
# See the CLI documentation for exact file paths and placement:
# https://github.com/tracebit-com/tracebit-community-cli

echo ""
echo "Credentials issued successfully. To deploy them to standard locations,"
echo "use the Tracebit CLI (recommended): tracebit deploy all"
echo ""
echo "If the CLI is unavailable, place the credentials manually:"
echo "  - AWS: add a [canary] profile to the standard AWS credentials file"
echo "  - SSH: write the private key to the standard SSH directory with chmod 600"
echo "See the CLI documentation for details."
echo ""
echo "Note: API-issued credentials will expire. Re-run this script to rotate"
echo "(or install the CLI for auto-rotation)."
```

> **Reminder:** When using the API, you are responsible for rotation. The CLI's background daemon handles this automatically. See SKILL.md for CLI-based setup.
