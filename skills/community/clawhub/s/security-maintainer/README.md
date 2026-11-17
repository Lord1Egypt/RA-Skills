# `security-maintainer` — Universal OpenClaw Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://openclaw.dev)

Universal security maintenance and vulnerability remediation skill for **OpenClaw**. Audits host software across Windows, macOS, and Linux/WSL, correlates packages with official vulnerability feeds (OSV.dev, CISA KEV, VulnCheck KEV, FIRST EPSS, NIST NVD, MSRC), detects AI agent security risks (unauthenticated LLMs, prompt injections, exposed credentials), and applies authorized fixes with post-installation version verification.

> [!NOTE]
> **Multilingual Support:**
> This repository documentation and CLI interfaces are provided in English as the primary universal standard. Spanish-language triggers and report localization are supported natively.

---

## 1. Key Capabilities

- **Vulnerability Remediation & Patching:** Correlates installed packages against CISA KEV, OSV, and distribution security trackers.
- **AI & Agent Security Auditing:** Detects exposed local inference engines (Ollama, LM Studio on port 11434/1234), prompt injection patterns, excessive MCP tool permissions, and leaked AI API credentials.
- **Deterministic Action Plans:** Uses a strict `ask` mode by default. Generates a unique plan ID and SHA-256 fingerprint; modifications cannot execute without cryptographic validation.
- **Effective Version Verification:** Verifies post-installation binaries directly via system package managers (`winget list`, `dpkg-query`, `brew list --versions`).
- **Subprocess and Argument Sanitization:** Enforces strict binary allowlists and sanitizes all command tokens against shell metacharacters (`;&|`$><`).
- **Zero Silent Privilege Escalation:** Actions requiring elevated rights are blocked and reported unless explicitly configured.

---

## 2. Environments and Platform Support

- **Windows Host OS:** Manages WinGet packages, registry installations, and pending Windows Updates.
- **WSL Distributions:** Audits and updates active distributions (`apt`, `dpkg`, `apk`, `dnf`, `rpm`). Stopped distributions remain untouched.
- **macOS:** Inspects and upgrades Homebrew formulas and Casks.
- **Local Projects:** Scans `package.json` and `requirements.txt` manifests in registered development repositories.

---

## 3. Installation

### From ClawHub (Recommended)

```bash
openclaw skills install security-maintainer
```

### Manual Installation

```bash
git clone https://github.com/alexar69-pixel/security-maintainer.git ~/.openclaw/skills/security-maintainer
cd ~/.openclaw/skills/security-maintainer
python3 -m pip install -e .
```

---

## 4. Configuration (`default_config.yaml`)

Configuration can be customized via `~/.security-maintainer/config.json` or supplied via the `--config` flag:

```yaml
version: "1.2.3"
mode: "ask" # 'ask' (default), 'audit', or 'auto'

windows:
  enabled: true
  allow_major_upgrades: false
  allow_reboots: false
  excluded_packages:
    - "Microsoft.Edge"

wsl:
  enabled: true
  auto_start_stopped_distros: false
  allow_reboots: false

projects:
  registered_paths:
    - "/home/user/projects/my-api"
  auto_run_tests: true

advisories:
  osv:
    enabled: true
    timeout_seconds: 15
  cisa_kev:
    enabled: true
    cache_ttl_hours: 24

execution:
  max_actions_per_run: 25
  plan_validity_minutes: 30
  lock_timeout_seconds: 60
```

---

## 5. Command-Line Interface (CLI)

```bash
# 1. Complete read-only audit (software, CVEs, and AI defense)
python3 -m security_maintainer.cli audit --all

# 2. Software-only audit
python3 -m security_maintainer.cli audit --environment all

# 3. AI agent security audit only
python3 -m security_maintainer.cli audit --ai-defense

# 4. Generate remediation plan (ask mode)
python3 -m security_maintainer.cli plan --environment all

# 5. Apply pre-approved remediation plan with SHA-256 validation
python3 -m security_maintainer.cli apply --plan-id plan-a8f9c102 --plan-hash e3b0c442...

# 6. Verify post-remediation effective versions
python3 -m security_maintainer.cli verify --environment all --plan-id plan-a8f9c102

# 7. View latest report
python3 -m security_maintainer.cli report
```

---

## 6. OpenClaw Natural Language Invocations

The skill triggers on unambiguous, scoped prompts:

- `security-maintainer: audit system software and vulnerabilities` -> Runs read-only inventory and vulnerability analysis.
- `security-maintainer: audit ai agent security and local llm services` -> Inspects local LLMs, prompts, and MCP configurations.
- `security-maintainer: search for pending security updates` -> Checks for available security patches.
- `security-maintainer: generate security remediation plan` -> Builds a numbered action plan with an SHA-256 fingerprint.
- `security-maintainer: apply approved security plan` -> Applies updates after verifying the plan hash.
- `security-maintainer: verify status of security patches` -> Confirms installed versions via `RemediationVerifier`.

> [!NOTE]
> **Scope Boundaries:**
> The skill does not act on ambiguous system commands lacking the `security-maintainer:` prefix. It does not perform destructive uninstalls, unrequested reboots, or arbitrary script execution.

---

## 7. Technical Documentation

- [Technical Architecture](ARCHITECTURE.md) — Architectural state machines, concurrency locks, and isolation.
- [Coverage Matrix](COBERTURA.md) — Detailed breakdown of managed components and package managers.
- [Sample Report](EJEMPLO_INFORME.md) — Example of Markdown output generated by the skill.
- [Security Policy](SECURITY.md) — Responsible disclosure process.
- [License](LICENSE) — Apache 2.0 License.
