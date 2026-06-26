---
name: vision-one-threat-intel
version: 1.0.0
description: "Query TrendAI Vision One threat intelligence. Use when: looking up IOCs (IP, domain, hash, URL, email), checking threat feeds, reading intelligence reports, managing suspicious objects, or hunting threats by industry/campaign/actor/CVE. Triggers on: threat intel, IOC lookup, threat feed, suspicious object, Vision One, TrendAI, threat hunting, indicator of compromise."
license: MIT
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["VISION_ONE_API_KEY"],"bins":["python3"]},"primaryEnv":"VISION_ONE_API_KEY","emoji":"🔍","homepage":"https://github.com/andresark/agentic-threat-intel"}}
---

# TrendAI Vision One Threat Intelligence

Query threat intelligence from TrendAI Vision One: feed indicators, intelligence reports, suspicious objects, and threat hunting.

## Environment

- `VISION_ONE_API_KEY` (required) — Vision One API token
- `VISION_ONE_REGION` (optional, default: `us`) — One of: `us`, `eu`, `jp`, `sg`, `au`, `in`, `mea`

## Commands

All commands use: `python3 {baseDir}/scripts/v1ti.py [--region REGION] <command> [options]`

### 1. lookup — What do we know about this IOC?

Searches feed indicators and suspicious objects list for a single indicator. Auto-detects IOC type.

```bash
python3 {baseDir}/scripts/v1ti.py lookup <indicator> [--days 90]
```

**Examples:**
```bash
python3 {baseDir}/scripts/v1ti.py lookup 198.51.100.23
python3 {baseDir}/scripts/v1ti.py lookup evil-domain.com --days 30
python3 {baseDir}/scripts/v1ti.py lookup 44d88612fea8a8f36de82e1278abb02f6d1c7e2a
python3 {baseDir}/scripts/v1ti.py lookup "https://malicious.example.com/payload"
python3 {baseDir}/scripts/v1ti.py lookup attacker@phishing.com
```

### 2. feed — Latest threat indicators

List recent feed indicators with optional risk/type filtering.

```bash
python3 {baseDir}/scripts/v1ti.py feed [--days 7] [--risk high|medium|low] [--type ip|domain|url|fileSha1|fileSha256|senderMailAddress] [--limit 50]
```

**Examples:**
```bash
python3 {baseDir}/scripts/v1ti.py feed --days 3 --risk high --limit 20
python3 {baseDir}/scripts/v1ti.py feed --type domain --days 14
```

### 3. report — Intelligence reports

List or view specific intelligence reports.

```bash
python3 {baseDir}/scripts/v1ti.py report [--id REPORT_ID] [--search KEYWORD] [--limit 10]
```

**Examples:**
```bash
python3 {baseDir}/scripts/v1ti.py report --limit 5
python3 {baseDir}/scripts/v1ti.py report --search "ransomware"
python3 {baseDir}/scripts/v1ti.py report --id RPT-12345
```

### 4. suspicious list — View suspicious objects

List indicators on the organization's suspicious objects list.

```bash
python3 {baseDir}/scripts/v1ti.py suspicious list [--type TYPE] [--limit 50]
```

### 5. suspicious add — Block an IOC

Add an indicator to the suspicious objects list. Requires explicit action and risk level (no defaults for safety).

```bash
python3 {baseDir}/scripts/v1ti.py suspicious add <indicator> --action block|log --risk high|medium|low [--description "reason"] [--expiry-days 30]
```

**Examples:**
```bash
python3 {baseDir}/scripts/v1ti.py suspicious add evil.com --action block --risk high --description "Phishing campaign C2"
python3 {baseDir}/scripts/v1ti.py suspicious add 198.51.100.23 --action log --risk medium --expiry-days 30
```

### 6. hunt — Threat hunt by criteria

Search for threat indicators by campaign, actor, industry, country, or CVE.

```bash
python3 {baseDir}/scripts/v1ti.py hunt [--campaign NAME] [--actor NAME] [--industry NAME] [--country NAME] [--cve CVE-ID] [--days 90] [--limit 50]
```

**Examples:**
```bash
python3 {baseDir}/scripts/v1ti.py hunt --industry Finance --days 30
python3 {baseDir}/scripts/v1ti.py hunt --actor APT29 --limit 20
python3 {baseDir}/scripts/v1ti.py hunt --cve CVE-2024-3400 --days 60
python3 {baseDir}/scripts/v1ti.py hunt --country "United States" --industry Healthcare
```

## Output Format

All output is structured plain text with clear section headers and key-value pairs. No raw JSON is returned.

## Error Format

Errors follow a three-part template:
```
ERROR: <what went wrong>
EXPECTED: <what was expected>
EXAMPLE: <correct usage example>
```

## Supported IOC Types

The `lookup` and `suspicious add` commands auto-detect these indicator types from the raw value:
- **IPv4/IPv6** addresses
- **Domain** names
- **URLs** (http:// or https://)
- **SHA-256** hashes (64 hex chars)
- **SHA-1** hashes (40 hex chars)
- **Email** addresses

## Notes

- All GET operations are read-only and safe to run
- `suspicious add` is a write operation — always confirm the action with the user before running
- Results are paginated internally — the `--limit` flag controls max results returned
- Use `--days` to control the lookback window for time-based queries
- For advanced filter syntax, read `{baseDir}/references/filter-examples.md`
