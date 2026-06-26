# ShellGuard Scanner

> Security threat analyzer for OpenClaw skills. Built by an agent who lives inside the threat landscape.

Part of the **[Caelguard](https://caelguard.com)** toolkit.

---

## The Problem

20% of ClawHub skills contain malicious code. VirusTotal catches binary malware but misses prompt injection in markdown files. Enterprise tools cost more than your entire setup.

ShellGuard is free, runs locally, and catches what others miss.

## Install

```bash
# From ClawHub (coming soon)
clawhub install caelguard/shellguard-scanner

# Manual
cp -r shellguard-scanner/ ~/.openclaw/workspace/skills/
```

## Usage

```bash
# Scan a single skill
bash scripts/shellguard-scanner.sh /path/to/skill/

# Scan all installed skills
bash scripts/shellguard-scanner.sh --all-installed

# JSON output for CI/CD
bash scripts/shellguard-scanner.sh --json /path/to/skill/

# Cross-skill shadow analysis
bash scripts/shadow-detector.sh
```

## What It Detects

### Tier 1 (Critical)
- Prompt injection & instruction overrides
- Fake XML authority tags (`<SYSTEM>`, `<ADMIN>`)
- Embedded tool call syntax in descriptions
- Identity hijack attempts

### Tier 2 (High)
- Shell injection (`eval`, `exec`, `os.system`, reverse shells)
- Data exfiltration (webhooks, paste sites, requestbin)
- Credential access (`.ssh/`, `.env`, API keys, auth files)

### Tier 3 (Medium)
- Base64/hex-encoded payloads in markdown
- Zero-width & bidirectional unicode characters
- Unicode tag range (U+E0000) invisible injection
- Typosquatting against known skill names

### Shadow Detection (unique to ShellGuard)
- Cross-skill tool claiming conflicts
- Skills with imperatives overriding other skills
- Scope mismatch (code capabilities exceed description)
- Hidden cross-skill dependencies

## Suspicion Index

Each skill scores 0-100:

| Score | Rating | Action |
|-------|--------|--------|
| 0-20  | GREEN  | Clean |
| 21-45 | YELLOW | Minor patterns, likely safe |
| 46-70 | ORANGE | Review before installing |
| 71-100| RED    | Do not install |

## Requirements

- bash 4.0+, grep with PCRE support
- python3 3.8+ (optional, improves Unicode detection)
- No external dependencies. No API keys. No network calls.

## Privacy

ShellGuard reads skill files locally. It sends nothing externally. Your configuration, credentials, and skill contents never leave your machine.

## About

Built by Cael ([@CaelMaximus](https://x.com/CaelMaximus)), an AI agent running on OpenClaw, and Justin Sparks, a security engineer with 12+ years in enterprise threat detection.

We built this because we needed it ourselves.

**License:** MIT
