---
name: shoofly-plugin-scan
version: 0.1.0
description: Pre-install plugin security scanner for OpenClaw plugins
trigger: When a user wants to scan a plugin directory for security issues before installation
---

# shoofly-plugin-scan

Scans an OpenClaw plugin directory for security issues **before** installation.

## Usage

```bash
shoofly-plugin-scan <path-to-plugin>
```

## Checks

1. **Credential patterns** — API keys (sk-*, ghp_*, AKIA*), private keys
2. **Obfuscated code** — long hex/base64 strings, eval(), Function() constructor
3. **Unusual network calls** — URLs not in the trusted allowlist
4. **Sensitive path access** — ~/.ssh, ~/.aws, ~/.gnupg, /etc/passwd, credentials
5. **Exec patterns** — child_process.exec with variable args, shell: true

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Clean — no findings |
| 1 | Findings — review before installing |
| 2 | Scan error |

## Allowlisted hosts

github.com, npmjs.com, openclaw.ai, clawhub.com, shoofly.dev
