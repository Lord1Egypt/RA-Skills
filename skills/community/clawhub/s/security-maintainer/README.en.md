# `security-maintainer` — OpenClaw Skill

[![CI](https://github.com/openclaw/security-maintainer/actions/workflows/ci.yml/badge.svg)](https://github.com/openclaw/security-maintainer/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://openclaw.dev)

An **OpenClaw** skill designed to maintain software up to date on Windows hosts and WSL distributions, detect known vulnerabilities (CVE, CISA KEV, OSV, Linux distro security trackers), and apply authorized remediations under a strict control and post-remediation verification model.

---

## 1. Key Features

- **Dual Complementary Functions:**
  1. *Preventative Maintenance:* Detects and applies available general updates, even if unrelated to a known CVE.
  2. *Security Remediation:* Correlates installed components with official vulnerability databases (OSV.dev, CISA KEV, Distro Security Trackers), identifies official patches, and verifies fixes post-installation.
- **Strict Classification of Findings:**
  - General update available (unrelated to identified CVEs).
  - Official security patch (resolves specific CVE/GHSA).
  - Configuration mitigation (does not modify binaries).
  - Unpatched vulnerability (no vendor patch available yet).
  - Unsupported / End-of-Life (EOL) product.
  - Functional bug in custom project dependencies.
- **Three Operational Modes:**
  - `audit` (Read-only): Inventories, correlates vulnerabilities, and outputs reports without touching the system.
  - `ask` (Default): Builds a numbered action plan with a cryptographic SHA-256 fingerprint and time expiration (30 min); requires explicit approval before applying changes.
  - `auto`: Automatically applies only actions authorized by a persistent policy.
- **Rigorous Verification:** Exit code `0` is never treated as proof of remediation; the system re-inventories the component, verifies the effective installed version, and detects pending reboot flags.
- **Portability & Zero Telemetry:** Built using Python's standard library (>= 3.10), without harvesting personal data, usernames, or credentials.

---

## 2. Architecture & Scope

- **OpenClaw inside WSL:** Designed specifically for setups where OpenClaw runs inside WSL (typically as user `openclaw`) and manages:
  - The **Windows** host (WinGet, Registry uninstallers, Windows Update COM API).
  - Active **WSL** distributions (`apt`, `dpkg`, `rpm`, `apk`, and WSL kernel status).
  - Explicitly registered **development projects** (Node.js and Python).
- **Protection for Stopped Distros:** Stopped WSL distributions are never started automatically unless `auto_start_stopped_distros: true` is configured.
- **No Silent Privilege Escalation:** If an action requires Windows Administrator or Linux `sudo` privileges and they are not pre-granted, the action is marked as `BLOCKED_PERMISSIONS` with clear manual instructions.

---

## 3. Installation

### Option A: From ClawHub / OpenClaw CLI (Recommended)

```bash
openclaw skills install security-maintainer
```

### Option B: Manual Installation

```bash
git clone https://github.com/openclaw/security-maintainer.git ~/.openclaw/skills/security-maintainer
cd ~/.openclaw/skills/security-maintainer
python3 -m pip install -e .
```

---

## 4. CLI Usage

```bash
# 1. Full audit (read-only)
python3 -m security_maintainer.cli audit --all

# 2. Generate maintenance plan with SHA-256 fingerprint
python3 -m security_maintainer.cli plan --environment all

# 3. Apply approved plan
python3 -m security_maintainer.cli apply --plan-id <PLAN_ID> --plan-hash <PLAN_HASH>

# 4. Verify post-remediation state
python3 -m security_maintainer.cli verify --environment all

# 5. View latest report
python3 -m security_maintainer.cli report
```

---

## 5. License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
