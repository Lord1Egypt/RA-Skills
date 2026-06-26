# TrendAI Vision One Threat Intelligence — OpenClaw Skill

An [OpenClaw](https://openclaw.ai) agent skill that gives AI agents direct access to [TrendAI Vision One](https://www.trendmicro.com/en_us/business/products/one-platform.html) threat intelligence. Designed for **agentic workflows** — not raw API wrappers.

Instead of exposing every API endpoint 1:1, this skill provides **6 workflow-oriented commands** that map to real threat-hunting tasks. The AI agent says what it wants to know, and the skill handles pagination, STIX parsing, IOC type detection, and output formatting automatically.

**Zero dependencies** — runs on Python 3.7+ stdlib only.

---

## Quick Start

### 1. Get a Vision One API Key

From your TrendAI Vision One console:

**Administration > API Keys > Add API Key**

Required permissions:

| Use Case | Permission |
|----------|------------|
| Read-only (feed, lookup, report, hunt) | Threat Intelligence — **View** |
| Full access (including `suspicious add`) | Threat Intelligence — **View + Configure** |

### 2. Set Environment Variables

```bash
export VISION_ONE_API_KEY="your-api-key-here"
export VISION_ONE_REGION="us"  # Optional — us (default), eu, jp, sg, au, in, mea
```

### 3. Install the Skill

Copy this directory into your OpenClaw skills location:

```bash
cp -r . ~/.openclaw/workspace/skills/vision-one-threat-intel/
```

Or add it to your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "vision-one-threat-intel": {
        "enabled": true
      }
    }
  }
}
```

Start a new OpenClaw session — the skill loads automatically.

---

## Commands at a Glance

| Command | What It Does |
|---------|-------------|
| `lookup <indicator>` | Look up any IOC across feed intelligence + your org's block list |
| `feed` | List the latest threat indicators with optional filtering |
| `report` | Browse or search TrendAI intelligence reports |
| `suspicious list` | View your organization's suspicious objects (block list) |
| `suspicious add` | Add an IOC to the block list (write operation — requires confirmation) |
| `hunt` | Search threat indicators by campaign, actor, industry, country, or CVE |

All commands auto-detect IOC types (IP, domain, URL, SHA-1, SHA-256, email) — the agent just provides the raw value.

---

## Usage Examples with Real Output

> IOC values in the examples below have been partially redacted (e.g., `example[.]com`) to prevent false-positive detections in security scanning pipelines.

### Look up a domain

```bash
python3 scripts/v1ti.py lookup mac-fster[.]com --days 30
```

```
=== Feed Intelligence: 1 matches ===

Type: DOMAIN
Value: mac-fster[.]com
Pattern: [domain-name:value = 'mac-fster[.]com']
Created: 2026-03-12T02:43:11.360Z
Valid From: 2026-03-12T02:43:11.360Z
Valid Until: 2026-09-15T21:02:02.470Z
ID: indicator--7367d804-56a5-465b-89f1-c91033baf9d1

=== Suspicious Object Status: Not on list ===
===
```

The skill found the domain in the TrendAI threat feed (STIX indicator with validity window), and confirmed it's **not** currently on your org's block list.

---

### Get the latest threat indicators

```bash
python3 scripts/v1ti.py feed --days 30 --limit 10
```

```
=== Feed Indicators (last 30 days): 10 results ===

  1. [FILE] 2ec37a7cc8daf20b1XXXXXXXXXXXX1ca5 | 2026-03-12
  2. [DOMAIN] mymachb[.]com | 2026-03-12
  3. [DOMAIN] mac-spce[.]com | 2026-03-12
  4. [DOMAIN] mymcsft[.]com | 2026-03-12
  5. [DOMAIN] mac-fster[.]com | 2026-03-12
  6. [DOMAIN] macfxnow[.]com | 2026-03-12
  7. [DOMAIN] getmclab[.]com | 2026-03-12
  8. [DOMAIN] mac-fst[.]com | 2026-03-12
  9. [DOMAIN] insta-mcer[.]com | 2026-03-12
 10. [DOMAIN] instmc[.]com | 2026-03-12

Total: 10 indicators
===
```

Filter by type to narrow results:

```bash
python3 scripts/v1ti.py feed --days 30 --type domain --limit 5
```

---

### Search intelligence reports

```bash
python3 scripts/v1ti.py report --search "Backdoor" --limit 5
```

```
=== Intelligence Reports (search: 'Backdoor'): 2 results ===

  1. Cybercriminals Distribute Backdoor With VPN Installer | 2020-09-25 | 5 IOCs
     ID: report--0ea4ba42-7904-4f32-b487-c44f5ed41e8c
  2. New MacOS Backdoor Connected to OceanLotus Surfaces | 2020-11-26 | 8 IOCs
     ID: report--b706757d-8794-4863-8281-5bde4b1ce02b

Total: 2 reports
===
```

Get details on a specific report by ID:

```bash
python3 scripts/v1ti.py report --id "report--0ea4ba42-7904-4f32-b487-c44f5ed41e8c"
```

```
=== Intelligence Report ===

Report: Cybercriminals Distribute Backdoor With VPN Installer
ID: report--0ea4ba42-7904-4f32-b487-c44f5ed41e8c
Published: 2020-09-25T03:14:02.89Z
Created: 2020-09-25T03:14:02.890Z
Modified: 2020-09-25T03:14:02.890Z
Types: threat-report
Associated IOCs: 5

===
```

---

### Check your org's block list

```bash
python3 scripts/v1ti.py suspicious list --limit 5
```

```
=== Suspicious Objects: 5 results ===

  1. [fileSha256] C5DE4B9E5C83XXXX...XXX376F7B0A8 | log | HIGH | expires 2026-05-10
  2. [fileSha1] 61211A7251XXXX...XXX090A9B9A6876 | log | HIGH | expires 2026-05-10
  3. [fileSha1] D74E41D0EEXXXX...XXX1388738B3E67C | log | HIGH | expires 2026-05-10
  4. [fileSha256] F7D9F689B2XXXX...XXX54E8AC7D273F | log | HIGH | expires 2026-05-10
  5. [fileSha1] 61EECC4674XXXX...XXX916F854F8B810F6D | log | HIGH | expires 2026-05-09

Total: 5 objects
===
```

---

### Look up a hash from the block list

```bash
python3 scripts/v1ti.py lookup 61211A7251XXXXXXXXXXXX090A9B9A6876
```

```
=== Feed Intelligence: No matches ===

=== Suspicious Object Status: FOUND ===

Type: fileSha1
Value: 61211A7251XXXXXXXXXXXX090A9B9A6876
Scan Action: log
Risk Level: HIGH
Expires: 2026-05-10T00:00:00Z
Last Modified: 2026-04-09T17:57:24Z
In Exception List: No
===
```

The hash wasn't found in the public threat feed, but it **is** on your org's suspicious objects list — confirming it was manually added with `log` action at `HIGH` risk.

---

### Add an IOC to the block list

```bash
python3 scripts/v1ti.py suspicious add evil-domain.example.com \
  --action block --risk high \
  --description "C2 server from phishing campaign" \
  --expiry-days 30
```

```
=== Suspicious Object Added ===

Type: domain
Value: evil-domain.example.com
Action: block
Risk: HIGH
Description: C2 server from phishing campaign
Expires: 2026-05-10T19:00:00Z

===
```

> `suspicious add` requires explicit `--action` and `--risk` flags — there are no defaults, by design. This is a write operation that can block production traffic.

---

### Threat hunt by criteria

```bash
python3 scripts/v1ti.py hunt --industry Finance --days 90 --limit 10
```

Hunt criteria can be combined:

```bash
python3 scripts/v1ti.py hunt --actor APT29 --country "United States" --days 60
python3 scripts/v1ti.py hunt --cve CVE-2024-3400 --limit 20
python3 scripts/v1ti.py hunt --campaign "ransomware" --industry Healthcare
```

---

## How It Works

### IOC Auto-Detection

You never need to specify the indicator type — the skill detects it automatically:

| Input | Detected Type |
|-------|--------------|
| `198.51.100.23` | IPv4 |
| `2001:db8::1` | IPv6 |
| `evil.example.com` | Domain |
| `https://evil.example.com/payload` | URL |
| `a1b2c3d4e5f6...` (40 hex chars) | SHA-1 |
| `a1b2c3d4e5f6...` (64 hex chars) | SHA-256 |
| `attacker@phishing.com` | Email |

### Output Format

All output is **structured plain text** — not raw JSON. This is intentional:

- JSON dumps waste tokens and are hard for agents to reason about
- Markdown tables render inconsistently across agent runtimes
- Key-value pairs with section headers give the best signal-to-noise ratio

### Pagination

Handled internally. The `--limit` flag controls how many results you get back. The skill follows Vision One's `nextLink` pagination automatically — agents never deal with skip tokens.

### Error Messages

Errors follow a three-part template that helps agents self-correct:

```
ERROR: Region 'xx' is not valid
EXPECTED: One of: au, eu, in, jp, mea, sg, us
EXAMPLE: export VISION_ONE_REGION='us'
```

---

## Architecture

```
SKILL.md                    OpenClaw skill manifest (loaded at session start)
scripts/
  v1ti.py                   CLI entry point — 6 subcommands
  lib/
    client.py               HTTP client (auth, retry, rate-limit, region routing)
    ioc_detect.py            Auto-detect IOC type from raw input
    formatters.py            Structured text formatters for AI consumption
    pagination.py            Auto-pagination (STIX bundles + standard items)
    cache.py                 File-based session cache (5min TTL)
references/
  api-reference.md           Vision One API endpoint documentation
  response-schemas.md        STIX 2.1 + JSON response field definitions
  filter-examples.md         OData filter syntax and examples
```

### Design Principles

This skill follows best practices from research across leading threat intelligence platforms and agentic AI security frameworks:

- **Workflow-oriented, not API-oriented** — 6 commands map to threat-hunting tasks, not REST endpoints
- **5-15 tool sweet spot** — avoids "tool soup" that degrades agent performance
- **Zero dependencies** — stdlib `urllib.request` + `json` only; just needs `python3` in PATH
- **Auto-detect, don't ask** — IOC type classification is deterministic; agents provide the value
- **Safe by default** — write operations require explicit flags; read operations are always safe
- **Concise output** — structured text optimized for token efficiency and agent reasoning

---

## Requirements

- Python 3.7+
- No external packages required (stdlib only)
- A TrendAI Vision One API key with Threat Intelligence permissions

---

## License

MIT
