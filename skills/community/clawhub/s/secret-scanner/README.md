[![ClawHub](https://img.shields.io/badge/ClawHub-secret-scanner-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: secret-scanner
version: 2.0.0
description: Detect API keys, tokens, and credentials in code with 50+ patterns, entropy analysis, and multiple report formats
tags: ["security", "secret", "scan", "audit", "cli", "credentials", "python", "open-source", "agent", "automation", "MIT"]
---

# Secret Scanner

**Detect API keys, tokens, and credentials in code with 50+ patterns, entropy analysis, and SARIF reports.**

> *Keywords: security, secret, scan, audit, cli, credentials, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Secrets leak into repos constantly and go unnoticed until exploited. Secret Scanner solves this: Detect API keys, tokens, and credentials in code with 50+ patterns, entropy analysis, and SARIF reports.

**Best for:** Security teams, maintainers, and CI pipelines.

## Features

- **Scan a path for secrets**
- **List detection patterns**
- **Emit SARIF for CI**
- **Filter by severity**
- **Skip entropy check**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/secret-scanner/main/secret_scanner.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python secret_scanner.py self-test     # prove it works end-to-end
python secret_scanner.py scan --help   # scan subcommand
python secret_scanner.py check --help   # check subcommand
python secret_scanner.py list-patterns --help   # list-patterns subcommand
```

## Use cases

1. Scan a path for secrets
1. List detection patterns
1. Emit SARIF for CI
1. Filter by severity
1. Skip entropy check

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| grep for keys | Pattern + entropy detection. |
| Single-pattern tools | 50+ patterns in one pass. |
| Manual review | SARIF drops into CI. |

## FAQ (SEO / AEO)

**Q: Patterns?**  
A: 50+ built in (keys, tokens, creds).

**Q: Entropy?**  
A: On by default; disable with --no-entropy.

**Q: SARIF?**  
A: Yes — --sarif for GitHub code scanning.

**Q: Offline?**  
A: Yes.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test secret-scanner
        run: python secret_scanner.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/secret-scanner)
