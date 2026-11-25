---
name: web-checker
description: Low-volume web configuration auditor with JS-bundle security analysis — probes headers, DNS, TLS, config exposure, and client-side XSS/secrets. Zero runtime dependencies.
version: 1.0.4
author: z-hussein
license: MIT
platforms: [linux, macos, windows]
permissions:
  - network_outbound_http
  - network_outbound_dns
  - network
  - process_subprocess_dig
  - process_subprocess_openssl
  - process_subprocess_curl
  - shell
  - filesystem_write_scratch_dir
  - filesystem_read_scratch_dir
  - filesystem_write_reports
  - file_write
  - file_read
metadata:
  hermes:
    tags: [security, networking, utility, dns, tls, headers]
    homepage: https://docs.openclaw.ai/
---

# web-checker - Web Configuration Audit Skill

### ⚠️ SAFETY & LEGAL WARNING

**This tool is for personal use and authorized assessments ONLY.**
Only run it against domains you own or have explicit written permission to check.
Unauthorized checks may violate computer misuse laws (CFAA, §323 StGB, etc.).
The author assumes no liability for any misuse by third parties.

## What It Does

This skill wraps `recon-cli`, a fast web configuration auditor that runs 8 lightweight checks against a target domain. The tool performs **low-volume active requests** (one HTTP call per path/subdomain) to verify whether exposed files and subdomains are actually live. It also downloads and statically analyzes JavaScript bundles for secrets, external endpoints, and potential XSS sinks.

**Active by design**: The tool makes outbound HTTP/HTTPS requests, DNS queries, and TLS handshakes. Active checks (`subdomains`, `sensitive_paths`, `tls`) require explicit authorization for each target domain. **JavaScript analysis** downloads client-side bundles to a temporary directory and analyzes them statically (no JS execution).

## Checks Performed

All non-informational checks perform **active requests**. Passive-only mode disables `subdomains` and `sensitive_paths` (`--passive-only`).

| Check | Network Behavior | Active by default |
|---|---|---|
| `headers` | 1 GET + optional redirect follow on target domain | No (informational) |
| `html_shell` | 1 GET body inspection on target domain | No (informational) |
| `js_bundle` | Downloads JS bundles to scratch dir, static analysis for secrets/XSS/endpoints | ✅ Yes (HTTP + file write/read in scratch) |
| `tls` | Connects to target:443 via openssl (active TLS probe) | ✅ Yes |
| `dns` | Queries DNS records for target domain | ✅ Yes (DNS queries) |
| `rdap` | Queries rdap.org for domain registration data | ✅ Yes (external API) |
| `subdomains` | Probes ~30 common subdomain prefixes via HTTPS | ✅ Yes (active discovery) |
| `sensitive_paths` | Probes 15 paths (.env, .git/, admin panels) via HTTP | ✅ Yes (active probing) |

## Usage

### Prerequisites
- Python 3.9+
- Optional: `curl`, `openssl`, `dig` (falls back to stdlib if missing)

### Run a full checkup
```bash
python3 -m recon_cli target.com
```

### Run only specific checks
```bash
python3 -m recon_cli target.com --only headers,tls,dns
```

### Generate JSON report for automation
```bash
python3 -m recon_cli target.com --json report.json
```

### Generate Markdown report
```bash
python3 -m recon_cli target.com --md report.md
```

### Quiet mode (suppress progress)
```bash
python3 -m recon_cli target.com --quiet --json report.json
```

### Passive-only mode (no active subdomain/path probing)
Disables `subdomains` and `sensitive_paths` checks. Only informational headers/HTML/DNS/TLS/js_bundle results are returned.
```bash
python3 -m recon_cli target.com --passive-only --json report.json
```

## Output Interpretation

### Severity model (ordered by impact)
| Level | Icon | Meaning |
|---|---|---|
| INFO | • | Informational - no action needed |
| LOW | ⚠ | Minor issue - consider fixing |
| MED | ▲ | Moderate - should be addressed |
| HIGH | ■ | Important - fix this |
| CRIT | ● | Critical - immediate action required |

### Exit codes
- **0** → Clean (no actionable HIGH/CRIT findings)
- **1** → Has HIGH or CRIT findings
- **2** → Bad arguments / unknown check name

### Reading JSON output
```json
{
  "target": "example.com",
  "tool_version": "0.1.0",
  "generated": "2026-11-20T...",
  "elapsed_s": 4.2,
  "results": [
    {
      "name": "tls",
      "status": "ok",
      "summary": "1 finding",
      "findings": [
        {
          "severity": "MED",
          "title": "Certificate expires in 15 days",
          "evidence": "...",
          "recommended_action": "Renew certificate soon"
        }
      ]
    }
  ]
}
```

## When to Use / Not to Use

### ✅ Appropriate use
- Your own domains and infrastructure
- Client websites (with written permission)
- Bug bounty programs (within scope)
- Internal security audits

### ❌ Not appropriate
- Random targets without permission
- Active exploitation or payload injection
- DDoS-level scanning volumes
- Any activity that violates terms of service

## Limitations

- **Active checks** - `subdomains`, `sensitive_paths`, `js_bundle`, and `tls` make outbound HTTP/HTTPS/TLS requests; only probe paths/subdomains you have permission to check
- **Low subdomain count** - 25 by default to stay low-noise; use specialized tools for full enumeration
- **No JS execution** - js_bundle performs static pattern matching only, does not execute any JavaScript
- **No authentication** - can't test behind login walls
- **False positives possible** - always verify findings manually before acting
- **RDAP/HSTS endpoints** require internet access to `rdap.org` and `hstspreload.org`

## ⚠️ Active Check Disclaimer

The `subdomains` and `sensitive_paths` checks make **active HTTPS requests** to the target domain and its guessed subdomains. The `js_bundle` check downloads client-side JavaScript to a temporary directory for static analysis only (no execution). The `tls` check performs an active TLS handshake. Only run these against domains you own or have explicit written permission to check.

When an agent uses this skill, it should confirm authorization before running active checks. Example phrasing:

> "I'll audit your site at target.com for common misconfigurations - headers, DNS, TLS, and config exposure. This includes **active HTTPS probes** (subdomains, sensitive paths), a **TLS handshake**, and a **static JS bundle analysis** for leaked secrets and XSS patterns. Do you confirm you own or have permission to check target.com? I'll show you the HIGH/CRIT findings first."

## Adding Custom Checks

Each check is a small Python module (~50-200 lines) implementing `Check.run(target, cfg) -> CheckResult`. Add a new one by:
1. Creating a file in `recon_cli/checks/` (subclass from `.base.Check`)
2. Registering it in `ALL_CHECKS` in `checks/__init__.py`
3. Running tests: `python3 -m unittest discover -s tests`

## License

MIT - Copyright (c) 2026 z-hussein

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction. See LICENSE for details.
