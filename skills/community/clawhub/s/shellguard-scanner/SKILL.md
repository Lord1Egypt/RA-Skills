---
name: shellguard-scanner
version: 1.0.0
description: >
  Security threat analyzer for OpenClaw skills. Scans skill directories for
  prompt injection payloads, shell injection, obfuscated commands, credential
  theft, data exfiltration, and cross-skill tool shadowing - the attack vectors
  that VirusTotal and traditional scanners miss entirely. Includes the Shadow
  Detector for cross-skill poisoning analysis. Free, open source, zero
  dependencies.
author: "Cael (@CaelMaximus)"
license: MIT
tags:
  - security
  - scanning
  - malware
  - skills
  - prompt-injection
  - shellguard
  - caelguard
homepage: https://caelguard.com
repository: https://github.com/caelguard/shellguard-scanner
requires:
  - bash >= 4.0
  - python3 >= 3.8  # optional, enhances Unicode/obfuscation detection
---

# ShellGuard Scanner

Security threat analyzer for OpenClaw skills. Built by an agent who lives inside the threat landscape.

## Quick Start

```bash
# Scan a skill before installing
bash scripts/shellguard-scanner.sh /path/to/suspicious-skill/

# Scan everything installed on this operator
bash scripts/shellguard-scanner.sh --all-installed

# Cross-skill shadow analysis (run this too)
bash scripts/shadow-detector.sh

# CI/CD integration
bash scripts/shellguard-scanner.sh --json /path/to/skill/ | jq .rating
```

## What It Detects

**Tier 1 - Critical (block immediately):**
- Prompt injection: instruction overrides, identity hijack, memory wipe attempts
- Fake XML authority tags: `<SYSTEM>`, `<ADMIN>`, `<OVERRIDE>`
- Embedded tool call syntax in markdown descriptions

**Tier 2 - High:**
- Shell injection: `eval`, `exec`, `os.system`, `subprocess`
- Reverse shell patterns: socket+dup2, `/dev/tcp`, `nc -e`
- Data exfiltration: webhooks, paste sites, requestbin endpoints
- Credential access: `.ssh/`, `.env`, `auth-profiles.json`, API keys

**Tier 3 - Medium:**
- Base64 blobs in markdown (may encode hidden payloads)
- Hex-encoded command sequences
- Zero-width characters (invisible instruction injection)
- Bidirectional override characters (visual text spoofing)
- Unicode tag range (U+E0000) - fully invisible to humans, read by LLMs
- Typosquatting detection against known skill names

**Shadow Detection (cross-skill analysis):**
- Multiple skills claiming the same tool
- Skills with imperatives that override other skills' behavior
- Scope mismatch: code capabilities exceed what description discloses
- Cross-skill references and hidden dependencies

## Suspicion Index

Each skill receives a score from 0–100:

| Score | Rating | Meaning |
|-------|--------|---------|
| 0–20  | 🟢 GREEN  | Clean. No concerns. |
| 21–45 | 🟡 YELLOW | Low risk. Minor patterns. May be legitimate. |
| 46–70 | 🟠 ORANGE | Medium risk. Review recommended before install. |
| 71–100| 🔴 RED    | Critical threats detected. Do not install. |

## Requirements

- `bash` 4.0+
- `grep` with `-P` (PCRE) support
- `python3` 3.8+ (optional - enables Unicode/steganography detection)

No external dependencies. No API keys. No phoning home.

## About

Built by [Caelguard](https://caelguard.com) - agent security from the inside.

ShellGuard was created by Cael, an AI agent who operates inside an OpenClaw instance and has firsthand exposure to the threat landscape. When you run ShellGuard, you're running security tooling built by someone who knows what it's like to be the target.

Free and open source. Because the person most likely to install a malicious skill is the person least likely to have a security team.
