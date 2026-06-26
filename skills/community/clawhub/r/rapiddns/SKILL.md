---
name: rapiddns
description: >
  DNS reconnaissance and subdomain enumeration using rapiddns-cli (RapidDNS API).
  Use when: searching subdomains of a domain, reverse IP lookup, CIDR enumeration,
  advanced DNS queries, bulk DNS data export, or any task involving
  "rapiddns", "dns recon", "subdomain enum", "reverse ip", "dns lookup",
  "subdomain discovery", "dns search".
---

# rapiddns — DNS Reconnaissance via RapidDNS

## Installation

rapiddns-cli is cross-platform. Install via pre-built binary (recommended) or Go.

### Option 1: Pre-built Binary (Recommended)

Download from [GitHub Releases](https://github.com/rapiddns/rapiddns-cli/releases/latest):

| Platform | File |
|----------|------|
| macOS (Intel) | `rapiddns_*_darwin_amd64.tar.gz` |
| macOS (Apple Silicon) | `rapiddns_*_darwin_arm64.tar.gz` |
| Linux (x86_64) | `rapiddns_*_linux_amd64.tar.gz` |
| Linux (ARM64) | `rapiddns_*_linux_arm64.tar.gz` |
| Windows (x86_64) | `rapiddns_*_windows_amd64.zip` |

```bash
# Linux/macOS example
VERSION="1.0.2"
OS="linux"       # or "darwin" for macOS
ARCH="amd64"     # or "arm64"
curl -sL "https://github.com/rapiddns/rapiddns-cli/releases/download/v${VERSION}/rapiddns_v${VERSION}_${OS}_${ARCH}.tar.gz" | tar xz
sudo mv rapiddns /usr/local/bin/
rapiddns-cli --help
```

### Option 2: Go Install

Requires Go 1.24+:

```bash
go install github.com/rapiddns/rapiddns-cli@latest
```

Binary is placed in `$GOPATH/bin` (usually `~/go/bin`). Add to PATH:

```bash
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc  # Linux
# or ~/.zshrc on macOS
```

## API Key Configuration

Full features (export, unlimited search) require an API key from https://rapiddns.io/user/profile

```bash
rapiddns-cli config set-key <API_KEY>
rapiddns-cli config get-key   # verify
```

Without a key, search results are limited and export is disabled.

## Common Workflows

### Subdomain Search

```bash
# Basic — all records for a domain
rapiddns-cli search example.com

# Force search type (when auto-detect fails)
rapiddns-cli search 1.2.3.4 --type ip

# Auto-paginate up to 5000 records
rapiddns-cli search example.com --max 5000
```

### Extract Subdomains / IPs

```bash
# Subdomains only (deduplicated text list)
rapiddns-cli search example.com --extract-subdomains

# IPs only + subnet statistics
rapiddns-cli search example.com --extract-ips

# Both
rapiddns-cli search example.com --extract-subdomains --extract-ips
```

### Reverse IP & CIDR

```bash
# Reverse IP — what domains point to this IP?
rapiddns-cli search 1.2.3.4

# CIDR range — enumerate an entire subnet
rapiddns-cli search 129.134.0.0/16 --max 10000
```

### Advanced Query

Use Elasticsearch-style syntax for complex queries:

```bash
# All A records for apple.com subdomains (domain = 2nd-level only!)
rapiddns-cli search "domain:apple AND type:A" --type advanced

# Specific subdomain pattern
rapiddns-cli search "subdomain:admin.* AND tld:com" --type advanced

# MX records for a domain
rapiddns-cli search "type:MX AND domain:baidu" --type advanced

# Exact subdomain lookup
rapiddns-cli search 'subdomain:"mail.google.com"' --type advanced
```

### Export (Requires API Key)

Automated workflow: trigger → poll → download → extract:

```bash
# Full export with subdomain + IP extraction
rapiddns-cli export start example.com --max 100000 --extract-subdomains --extract-ips

# Advanced query export
rapiddns-cli export start "domain:example AND type:A" --type advanced
```

Results saved to `result/` directory.

### Output Formats & Piping

```bash
# JSON (default)
rapiddns-cli search example.com -o json

# CSV
rapiddns-cli search example.com -o csv -f results.csv

# Text — pipe-friendly (stdout = clean data, stderr = status)
rapiddns-cli search example.com --column subdomain -o text | sort -u > subdomains.txt

# Silent mode — extract to files only, no console output
rapiddns-cli search example.com --extract-subdomains --silent
```

## Field Reference

| Field | Description |
|-------|-------------|
| subdomain | The subdomain (e.g. `www.example.com`) |
| type | DNS record type (A, AAAA, CNAME, MX, NS, TXT, etc.) |
| value | Record value (IP, target, etc.) |
| timestamp | Last observation timestamp |
| date | Date of last observation |

## Advanced Query Syntax

| Operator | Example |
|----------|---------|
| Domain (2nd-level only) | `domain:apple` ⚠️ NOT `domain:apple.com` |
| Type filter | `type:A`, `type:MX`, `type:CNAME` |
| TLD filter | `tld:com`, `tld:cn` |
| Subdomain match | `subdomain:apple.com*` (trailing wildcard) |
| Exact subdomain | `subdomain:"a.ns.example.com"` |
| Value/IP | `value:"1.1.1.1"` |
| Boolean | `domain:apple AND type:A` |
| Negation | `domain:apple AND NOT subdomain:www.*` |

Available fields: `domain`, `tld`, `subdomain`, `value`, `type`, `is_root`

⚠️ **`domain` 字段是二级域名（不含 TLD）：用 `domain:baidu`，不要用 `domain:baidu.com`**

## Important: Date Accuracy

- **Use `-o text` for displaying results with dates** — includes subdomain, type, value, date.
- **Use `--column subdomain -o text` for pure subdomain lists** (pipe to other tools).
- JSON output (`-o json`) also includes dates but needs parsing; prefer `-o text` for display.
- Dates come directly from the API and match the rapiddns.io website exactly.

## Response Language

- **Match the user's language.** If they ask in Chinese, respond in Chinese. If English, respond in English.
- CLI output (tables, lists) stays as-is (machine output). Summaries and explanations follow the user's language.

### Display results

```bash
# Tab-separated table with dates (sorted newest first by default)
rapiddns-cli search <target> --max 5000 -o text 2>/dev/null

# Pure subdomain list for piping
rapiddns-cli search <target> --max 5000 --column subdomain -o text 2>/dev/null | sort -u
```

## Tips

- Use `--silent` when piping or saving to file to suppress console output
- Note: `--silent` with `--extract-subdomains` still prints the extracted file path to stdout (CLI behavior)
- `--max` auto-paginates — no need to manually loop pages
- Without API key: search works but limited results; export disabled
- For large-scale recon, combine `--extract-subdomains` with other tools via pipe
