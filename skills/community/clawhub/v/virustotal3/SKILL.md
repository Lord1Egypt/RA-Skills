---
name: virustotal
version: 1.0.1
author: arfonzo (github:arf0nz0)
license: MIT-0
description: Free malware, network and IP analysis! Scan files, URLs, domains, and IPs with VirusTotal. WARNING: Submitted files, URLs, and artifacts are shared with VirusTotal and its security partners — do NOT upload proprietary, confidential, or regulated data. Prefer hash lookups for sensitive files.
triggers:
  - virustotal
  - virus total
  - vt scan
  - scan file
  - scan url
  - check ip
  - check domain
  # is this safe  # Removed: too generic, risks accidental activation sending data to third party without explicit intent
  - malware check
  - reputation check
requires:
  bins:
    - curl
---

# VirusTotal Skill — Public API

Interact with the VirusTotal Public API v3 to scan files, URLs, domains, and IP addresses for malware analysis and threat intelligence.

## Configuration

### API Key
**Secrets file:** Store your API key in a file (default: `~/.openclaw/secrets/virustotal.env`):
```
VIRUSTOTAL_API_KEY=your_api_key_here
```
Create with `chmod 600`. Get your API key from https://www.virustotal.com/gui/my-apikey.

**Loading:** All curl examples use `.` (dot) source to load credentials into the shell environment:
```bash
. "${VIRUSTOTAL_SECRETS_FILE:-$HOME/.openclaw/secrets/virustotal.env}"
```
Override the default path with the `VIRUSTOTAL_SECRETS_FILE` environment variable.

### ⚠️ Credential Security (MANDATORY)

**NEVER display secrets in tool output.** The `.` source command loads credentials into shell variables silently — no output is produced. This is the correct and secure approach.

**Banned patterns:**
- `cat ~/.openclaw/secrets/virustotal.env`
- `VIRUSTOTAL_API_KEY=xxx curl ...`
- Any form of reading secrets into tool output

**If credential loading fails:** Fix the secrets file path or contents. Do NOT bypass security by hardcoding values.

## ⚠️ Privacy & Data Sharing

**Any file, URL, domain, or IP submitted to VirusTotal may be shared with VirusTotal's security partners and could become accessible to third parties beyond your control.**

Before submitting:
- **Files:** Prefer hash-based lookups (SHA256/MD5/SHA1) over uploads for sensitive or proprietary files
- **URLs:** Consider whether internal/private URLs should be sent to a third party
- **IPs/Domains:** Be aware these queries reveal your infrastructure interests to VirusTotal
- **Never upload** proprietary binaries, confidential documents, regulated data (PII, PHI, financial), or internal infrastructure details without authorisation

## ⚠️ Mandatory User Confirmation (NO EXCEPTIONS)

**Before sending ANY file, URL, domain, or IP to VirusTotal, you MUST:**

1. Inform the user that the data will be shared with VirusTotal and its security partners
2. Explicitly ask for confirmation
3. Wait for the user's explicit approval before proceeding
4. If the user declines, do NOT proceed with the submission

**This applies to ALL operations that send data outbound:**
- File uploads (`POST /files`)
- URL scans (`POST /urls`)
- Domain lookups (`GET /domains/{domain}`)
- IP lookups (`GET /ip_addresses/{ip}`)

**There is NO override, NO exception, and NO "fast path".** Even if the user says "just scan it" or "quick check", you must still confirm and warn about privacy implications.

Example confirmation:
> "This will send [resource] to VirusTotal, which shares data with its security partners. OK to proceed?"

### Hash-First Workflow for Files

When a user wants to check a **file**:
1. **First choice:** Ask if they have a SHA256/MD5/SHA1 hash — hash lookups do NOT upload the file
2. **Only upload** if no hash is available AND the user explicitly consents after privacy warning

---

## Request Pattern

All endpoints use this secure pattern. Replace `{PATH}` with the endpoint path and add any extra flags as needed:

```bash
. "${VIRUSTOTAL_SECRETS_FILE:-$HOME/.openclaw/secrets/virustotal.env}" \
  && _H=$(mktemp) && chmod 600 "$_H" \
  && printf 'x-apikey: %s\n' "$VIRUSTOTAL_API_KEY" > "$_H" \
  && curl -s "https://www.virustotal.com/api/v3{PATH}" -H@"$_H" \
  && rm -f "$_H"
```

**For POST requests** add `-X POST` and appropriate data flags after the URL.
**For file uploads** replace the curl URL with the upload URL and add `-F "file=@/path/to/file"`.

## Response Structure

All endpoints return JSON with this common shape:

```json
{
  "data": {
    "id": "resource_identifier",
    "type": "file|url|domain|ip_address|analysis",
    "attributes": {
      "reputation": 0,
      "last_analysis_stats": {
        "malicious": 0,
        "suspicious": 0,
        "harmless": 0,
        "undetected": 0
      },
      "last_analysis_results": {
        "EngineName": {
          "category": "harmless|malicious|suspicious|undetected",
          "result": "clean|Trojan.Generic|phishing|unrated",
          "engine_update": "20230101",
          "engine_version": "1.0.0"
        }
      }
    }
  }
}
```

### Per-endpoint unique fields:
- **File:** `sha256`, `md5`, `sha1`, `names`, `size`, `type_description`
- **URL:** `url`, `title`
- **Domain:** `whois`, `creation_date`, `last_update_date`, `last_dns_records`, `last_https_certificate`, `rdap`
- **IP:** `country`, `as_owner`, `network`, `tags`
- **Analysis:** `status` ("completed"|"queued"|"in-progress"|"failed"), `stats`

## API Overview

- **Base URL:** `https://www.virustotal.com/api/v3`
- **Authentication:** `x-apikey` header (loaded from secrets file, see Request Pattern)
- **Rate limit:** 4 requests/minute (free tier). Premium has no limits.
- **Response format:** JSON (see Response Structure)

---

## File Operations

### File Scan (Upload)

**Endpoint:** `POST /files`
**Description:** Upload and scan a file with VirusTotal. Returns an analysis ID.

**⚠️ Before uploading:** Always confirm with the user. File uploads share the entire file with VirusTotal and its partners. Prefer hash lookups when a SHA256/MD5/SHA1 is available.

**File size limits:**
- Direct upload: up to 32MB
- Large files (up to 650MB): Use `/files/upload_url` endpoint first

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /files
curl -s -X POST "https://www.virustotal.com/api/v3/files" -H@"$_H" -F "file=@/path/to/file"
```

See Response Structure above. Unique fields for this endpoint: `id`, `type`.

**Error handling:**
- 400: Invalid file, password-protected ZIP, or corrupt file
- 429: Rate limited
- 401: Invalid API key

### File Report (by Hash)

**Endpoint:** `GET /files/{id}`
**Description:** Get analysis report for a file by its hash (MD5, SHA1, or SHA256).

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /files/{hash}
curl -s "https://www.virustotal.com/api/v3/files/{hash}" -H@"$_H"
```

See Response Structure above. Unique fields for this endpoint: `sha256`, `md5`, `sha1`, `names`, `size`, `type_description`.

### Large File Upload (32MB+)

**Endpoint:** `POST /files/upload_url`
**Description:** Get a URL for uploading files larger than 32MB (up to 650MB).

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /files/upload_url
curl -s "https://www.virustotal.com/api/v3/files/upload_url" -H@"$_H"
```

---

## URL Operations

### URL Scan (Submit)

**Endpoint:** `POST /urls`
**Description:** Submit a URL for scanning. Returns an analysis ID.

**⚠️ Privacy:** URL lookups are query-only (no upload) but share the URL with VirusTotal and its partners. Always confirm with the user first.

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /urls
curl -s -X POST "https://www.virustotal.com/api/v3/urls" -H@"$_H" --form-urlencode "url=https://example.com"
```

See Response Structure above. Unique fields for this endpoint: `id`, `type`.

### URL Report

**Endpoint:** `GET /urls/{id}`
**Description:** Get analysis report for a URL. The `{id}` parameter should be a URL identifier (not the raw URL - see URL identifiers below).

**URL identifiers:** Convert URLs to identifiers using base64 encoding of `-` prefixed URL:
```bash
echo -n "https://example.com" | base64  # returns aHR0cHM6Ly9leGFtcGxlLmNvbQ==
```

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /urls/{url_id}
curl -s "https://www.virustotal.com/api/v3/urls/{url_id}" -H@"$_H"
```

See Response Structure above. Unique fields for this endpoint: `url`, `title`.

---

## Domain & IP Operations

### Domain Report

**Endpoint:** `GET /domains/{domain}`
**Description:** Get analysis report for a domain.

**⚠️ Privacy:** Domain lookups are query-only (no upload) but reveal to VirusTotal that you are investigating this domain. Always confirm with the user first.

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /domains/{domain}
curl -s "https://www.virustotal.com/api/v3/domains/example.com" -H@"$_H"
```

See Response Structure above. Unique fields for this endpoint: `whois`, `creation_date`, `last_update_date`, `last_dns_records`, `last_https_certificate`, `rdap`.

### IP Address Report

**Endpoint:** `GET /ip_addresses/{ip}`
**Description:** Get analysis report for an IP address.

**⚠️ Privacy:** IP lookups are query-only (no upload) but reveal to VirusTotal that you are investigating this IP. Always confirm with the user first.

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /ip_addresses/{ip}
curl -s "https://www.virustotal.com/api/v3/ip_addresses/8.8.8.8" -H@"$_H"
```

See Response Structure above. Unique fields for this endpoint: `country`, `as_owner`, `network`, `tags`.

---

## Analysis Status

**Endpoint:** `GET /analyses/{id}`
**Description:** Check the status of an analysis (file or URL scan).

**curl example:**
```bash
# Replace {PATH} in the request pattern above with: /analyses/{analysis_id}
curl -s "https://www.virustotal.com/api/v3/analyses/{analysis_id}" -H@"$_H"
```

See Response Structure above. Unique fields for this endpoint: `status` ("completed"|"queued"|"in-progress"|"failed"), `stats`.

---

## Error Handling

### Common HTTP Status Codes

| Code | Description | Action |
|------|-------------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Verify API key |
| 403 | Forbidden | Check permissions, premium required |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limited - wait and retry |
| 500 | Internal Server Error | Server error - try again later |

### Rate Limiting (429)

When you receive a 429 response:
- Wait at least 60 seconds before retrying
- Free tier: maximum 4 requests per minute
- Consider implementing exponential backoff
- Premium tier: no rate limits

### Error Response Format

```json
{
  "error": {
    "code": "error_code",
    "message": "Error description"
  }
}
```

---

## Free vs Premium Features

### Free Tier (This Skill)
- ✅ File scanning (32MB direct, 650MB with upload URL)
- ✅ URL scanning
- ✅ Domain reports
- ✅ IP address reports
- ✅ Basic threat intelligence
- ❌ Search/Retrohunt (premium only)
- ❌ Livehunt/YARA rules (premium only)
- ❌ Advanced threat hunting (premium only)
- ❌ Private API access (premium only)
- ❌ Bulk operations (premium only)
- ❌ Priority processing (premium only)

### Premium Features
- No rate limits
- Advanced threat hunting
- Search/Retrohunt functionality
- Livehunt notifications
- Private API access
- Bulk operations
- Priority processing
- Extended retention

---

## URL Identifier Generation

For URL reports, you need to encode the URL as follows:

```bash
# Method 1: Using base64
URL="https://example.com"
URL_ID=$(echo -n "$URL" | base64)
echo "$URL_ID"  # aHR0cHM6Ly9leGFtcGxlLmNvbQ==

# Method 2: Using Python
python3 -c "import base64; print(base64.b64encode(b'https://example.com').decode())"
```

---

## Best Practices

1. **Rate limiting:** Implement proper rate limiting (4 requests/minute for free tier)
2. **Error handling:** Always check HTTP status codes and handle errors gracefully
3. **Security:** Never expose API keys in logs or tool output
4. **Caching:** Cache responses when possible to reduce API calls
5. **File uploads:** Use upload_url for files larger than 32MB
6. **Analysis polling:** For file/URL scans, poll the analysis endpoint for completion

---

*Last updated: 2026-05-25*