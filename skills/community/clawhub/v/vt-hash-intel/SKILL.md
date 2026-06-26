---
name: vt-hash-intel
description: >
  Instantly check if a file, URL, domain, or IP is malicious using VirusTotal.
  Paste any MD5/SHA1/SHA256 hash, URL, domain name, or IP address into the chat 
  and get a full threat report — detection ratio across 70+ security engines, 
  malware family, YARA matches, sandbox verdicts, DNS records, WHOIS info, and
  a direct link to the VirusTotal report. Supports single and batch lookups of
  mixed IOC types. Also handles defanged IOCs (hxxp, [.] notation).
  Perfect for incident response, threat hunting, IOC enrichment, SOC triage,
  and daily security operations. Use this skill whenever the user has a suspicious
  hash, URL, domain, or IP they want to investigate.
  Also triggers on: VirusTotal, VT, hash lookup, malware check, file reputation,
  threat intel, IOC, URL scan, domain reputation, IP reputation,
  查hash, 查IP, 查域名, 查URL, 威胁情报, 病毒查询, 恶意软件分析.
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - VT_API_KEY
---

# VT Hash Intel — VirusTotal Threat Intelligence

Check any IOC (Indicator of Compromise) against VirusTotal's 70+ security engines. Supports four IOC types:

| Type | Example | VT Endpoint |
|---|---|---|
| **Hash** (MD5/SHA1/SHA256) | `44d88612fea8a8f36de82e1278abb02f` | `/files/{hash}` |
| **URL** | `https://malicious-site.com/payload` | `/urls/{id}` |
| **Domain** | `evil-domain.com` | `/domains/{domain}` |
| **IP Address** | `1.2.3.4` | `/ip_addresses/{ip}` |

## Prerequisites

`VT_API_KEY` environment variable must be set. Free key: https://www.virustotal.com/gui/my-apikey

## Instructions

### Step 1: Identify IOCs from user input

The script auto-detects IOC type:
- **Hash**: 32 hex chars (MD5), 40 hex chars (SHA1), 64 hex chars (SHA256)
- **URL**: starts with `http://` or `https://`
- **IP**: IPv4 format like `1.2.3.4`
- **Domain**: everything else with dots and valid TLD (e.g. `evil.com`)

The script also handles **defanged IOCs** automatically:
- `hxxp://` → `http://`
- `hXXp://` → `http://`
- `evil[.]com` → `evil.com`
- `1[.]2[.]3[.]4` → `1.2.3.4`

### Step 2: Run the lookup

```bash
SKILL_DIR="$(dirname "$(find /root/.openclaw -name 'SKILL.md' -path '*/vt-hash-intel/*' 2>/dev/null | head -1)")"

# Single IOC (auto-detect type)
python3 "$SKILL_DIR/scripts/vt_lookup.py" <ioc>

# Mixed batch (hashes + URLs + domains + IPs together)
python3 "$SKILL_DIR/scripts/vt_lookup.py" <hash> <url> <domain> <ip>

# Force type if auto-detection is wrong
python3 "$SKILL_DIR/scripts/vt_lookup.py" --type domain example.com
```

### Step 3: Parse and present results

The JSON output always contains these common fields:
- `ioc`: the queried value
- `ioc_type`: "hash" | "url" | "domain" | "ip"
- `detection_ratio`: e.g. "45/72"
- `threat_level`: "clean" | "low" | "medium" | "high"
- `threat_emoji`: ✅ | ⚠️ | 🟠 | 🔴
- `detections`: array of engines that flagged it
- `reputation`: VT community reputation score
- `vt_link`: direct link to the VT report
- `error`: non-null if something went wrong

**Hash-specific fields**: `sha256`, `md5`, `sha1`, `file_name`, `file_type`, `file_size_human`, `threat_label`, `popular_threat_name`, `crowdsourced_yara`, `sandbox_verdicts`, `sigma_rules`

**URL-specific fields**: `url`, `final_url`, `title`, `categories`

**Domain-specific fields**: `registrar`, `creation_date`, `dns_records`, `categories`, `popularity_ranks`

**IP-specific fields**: `asn`, `as_owner`, `country`, `network`

### Step 4: Format the response

IMPORTANT: Always present full contextual analysis regardless of threat level. Even when an IOC is "clean" (0 detections), the contextual information is extremely valuable for security analysis. A clean VT result does NOT mean an IOC is safe — it may be too new, targeted, or simply not yet submitted.

**For hashes** — present:
- Verdict line (emoji + level + detection ratio)
- File info: name, type, size, first seen date
- Threat classification (if malicious): family name, threat label
- Top engine detections (if any)
- YARA rules, sandbox verdicts, Sigma rules (if any)
- VT link
- Contextual analysis + recommendations

**For URLs** — present:
- Verdict line
- URL + final redirected URL (flag if different — could indicate redirect chain)
- Page title
- Categories assigned by security vendors
- Top detections (if any)
- VT link
- Contextual analysis: analyze whether the URL pattern looks suspicious (random strings, suspicious TLD, known bad path patterns like /wp-content/uploads/*.exe)
- Recommendations

**For domains** — always present these even if clean:
- Verdict line
- Registrar + creation date (flag if newly registered within last 30 days — common for phishing/malware)
- DNS records (A, AAAA, MX, NS, TXT records — helps identify hosting and infrastructure)
- Categories from security vendors
- Popularity ranking (low/no ranking on a queried domain can be suspicious)
- Reputation score
- VT link
- Contextual analysis: note if domain is very new, uses suspicious TLD, has low popularity, or uses known bulletproof hosting
- Recommendations

**For IPs** — always present these even if clean:
- Verdict line
- ASN number + AS owner (helps identify hosting provider — flag known bulletproof hosters)
- Country (geographic context)
- Network CIDR range
- Reputation score
- VT link
- Contextual analysis: note if IP belongs to a cloud provider, VPS, residential proxy, or known hosting provider. Flag countries commonly associated with malicious infrastructure if relevant.
- Recommendations

Threat level classification (same for all types):

| Malicious Detections | Level | Emoji |
|---|---|---|
| 0 | clean | ✅ |
| 1–5 | low | ⚠️ |
| 6–15 | medium | 🟠 |
| 16+ | high | 🔴 |

### Step 5: Recommendations

Always provide actionable recommendations based on threat level AND context:

- **🔴 high**: Block immediately in firewall/EDR/proxy, sweep environment for related IOCs, investigate affected hosts, collect lateral IOCs (related hashes/domains/IPs from VT)
- **🟠 medium**: Likely malicious — isolate and investigate, submit to sandbox, check network IOCs
- **⚠️ low**: Possible false positive — verify with sandbox, check file/URL context and origin, monitor
- **✅ clean**: Present all available context (ASN, country, registrar, DNS, categories, reputation). Remind user: "Clean on VT does not guarantee safety — the IOC may be too new, too targeted, or not yet submitted. Consider checking other threat intel sources (AbuseIPDB, Shodan, URLhaus, etc.)."
- **❓ not found**: Never submitted to VT — does NOT mean safe. Suggest uploading file to VT, or checking AlienVault OTX, AbuseIPDB, URLhaus for additional coverage.

For batch results with mixed types, present a summary table first (IOC | type | verdict | detection ratio | key finding), then detailed reports for each item.

## Error Handling

| Error | Cause | Response |
|---|---|---|
| `NotFoundError` | IOC not in VT DB | "Not found in VT. This does NOT mean it's safe." |
| `AuthenticationError` | Bad/missing API key | "Check VT_API_KEY in your .env file." |
| `QuotaExceededError` | Rate limit hit | "Rate limited. Wait and retry." |
| `UnrecognizedIOC` | Cannot detect type | "Cannot identify this IOC type. Try --type flag." |
| `ConnectionError` | Network issue | "Cannot reach VT API. Check network." |

## Examples

**User**: 帮我查一下这个hash 44d88612fea8a8f36de82e1278abb02f
**Agent**: Detects MD5 hash → runs lookup → presents file threat report.

**User**: Check this URL: https://suspicious-site.com/download.exe
**Agent**: Detects URL → runs lookup → presents URL analysis with categories and detections.

**User**: 这个域名安全吗？evil-domain.com
**Agent**: Detects domain → runs lookup → presents domain report with DNS, WHOIS, and detections.

**User**: 查一下这些IOC:
44d88612fea8a8f36de82e1278abb02f
hxxps://bad-site[.]com/malware
evil.com
1.2.3.4
**Agent**: Detects mixed types → runs batch lookup → presents summary table then individual reports sorted by severity.
