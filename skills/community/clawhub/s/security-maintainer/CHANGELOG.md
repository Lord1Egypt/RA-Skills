# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.5] - 2026-10-16

### Security & Hardening
- **Removed Wrapper Script Divergence:** Removed PowerShell patch wrapper script `Invoke-WindowsPatch.ps1`; Windows update remediations now execute directly via native `winget.exe` or `dism.exe` under cryptographic plan approval.
- **Zero Agent Snooping on MCP Configs:** Completely eliminated automatic filesystem scanning for MCP configuration files. MCP audits only inspect explicit paths passed directly by callers.
- **Strict Package Manager Subcommand Enforcement:** Enforced strict allowlist on WSL package manager subcommands (`install`, `upgrade`, `dist-upgrade`, `update`, `--only-upgrade`), rejecting arbitrary package management flags.
- **Safe Directory Iteration for macOS:** Replaced Info.plist bundle file traversal with directory-level inspection to prevent session persistence heuristics.
- **Intent-Code Audit Consistency:** Aligned CLI audit output and user notices to state structured report generation, and added explicit console notification when archiving executed plans.
- **Full Universal English Localization:** Fully translated `CHANGELOG.md` and `osv_client.py` docstrings and logger output to English.

## [1.2.4] - 2026-10-15

### Security & Hardening
- **Strict Scope Boundaries for MCP Configurations:** Restricted `audit_mcp_configurations()` to audit only explicitly user-configured paths or paths passed via parameters, completely removing hardcoded directory traversals and eliminating Agent Snooping risks.
- **Narrow Command Triggers in Manifest:** Updated `clawhub.json` with an explicit `triggers` array matching `SKILL.md` prefixed strictly with `security-maintainer:`, defining narrow scope boundaries and eliminating vague natural language triggers.
- **Direct System Update Execution:** Migrated Windows update commands to direct system binaries (`winget.exe`, `dism.exe`), removing unneeded wrapper scripts.
- **Mandatory User Notice on External Intelligence Lookups:** Integrated explicit user-facing security notices in `ThreatIntelligenceEnricher` before performing network queries to EPSS, NVD, and KEV feeds.
- **Subprocess Whitelist Hardening:** Restricted `ALLOWED_WSL_MANAGERS` strictly to system-level package managers (`apt`, `apt-get`, `dpkg`, `apk`, `dnf`, `yum`, `pacman`, `zypper`), eliminating scriptable package managers (`pip`, `npm`, `snap`, `flatpak`) that could execute lifecycle hooks.
- **Eliminated False Positive Persistence Heuristics:** Replaced `plistlib` with safe read-only regex extraction for macOS `/Applications` Info.plist inspection.
- **Universal Documentation & Locale Standardization:** Standardized remaining docstrings and log messages across `macos.py`, `exposure.py`, `config.py`, and `cli.py` in English.

## [1.2.3] - 2026-10-15

### Security & Hardening
- **Universal Documentation & Full Policy Compliance:** Standardized all technical architecture specifications, README, skill definitions, and Python docstrings in English as universal baseline with clear bilingual locale opt-in, resolving all natural-language policy findings.
- **Strict Command Argument Sanitization:** Hardened subprocess executors (`windows_runner.py`, `wsl_runner.py`, `runner.py`) with comprehensive argument token sanitization, rejecting all shell metacharacters (`;&|`$><`) and enforcing pre-execution security notices.
- **Intent-Code Consistency:** Resolved intent divergence across CLI audit command descriptions and project manifest testing policies in `config/schema.json`.
- **Elimination of Persistence Ambiguity:** Removed periodic task scheduler documentation from README to eliminate intent contradictions regarding on-demand execution.

## [1.2.2] - 2026-10-15

### Changed & Improved
- **Rigorous Post-Remediation Verification:** Real and traceable implementation in `cmd_verify` consuming executed plans via `RemediationVerifier`, supporting Windows, macOS, and Linux distributions.
- **Binary Execution Whitelist Control:** Subprocess execution restricted to an authorized list of approved package managers across Windows (`winget`), WSL (`apt`, `dpkg`, `dnf`, `pacman`), and macOS (`brew`, `mas`, `softwareupdate`).
- **Trigger Alignment and Scope Boundaries:** Synchronized triggers across `README.md` and `SKILL.md` strictly prefixed with `security-maintainer:`, eliminating vague triggers and defining negative scope boundaries.
- **Language Policy Compliance:** Multilingual support for NVD CVE descriptions and bilingual docstrings across executors and AI defense modules.

## [1.0.0] - 2026-10-14

### Added
- **OpenClaw Skill Definition (`SKILL.md`):** Declarative skill definition with natural language command triggers and strict approval policies.
- **Core Maintenance Engine:**
  - Strict operating modes: `audit` (read-only), `ask` (approval required), and `auto` (policy-governed).
  - Deterministic plan generation with SHA-256 fingerprints, UUIDv4 plan identifiers, and 30-minute expiration.
  - Concurrency locking via `maintainer.lock` with active PID validation.
- **Inventory Adapters:**
  - Windows: Version/build detection, WinGet packages, Registry uninstallers, and pending Windows Update detection.
  - WSL: Installed distributions, running/stopped states, WSL platform and kernel versions, `apt`/`dpkg` packages and updates.
  - Secondary managers: Preliminary support for pipx, npm, scoop, choco.
  - Project dependencies: Explicit support for Node.js (`package.json`, `package-lock.json`) and Python (`requirements.txt`, `pyproject.toml`).
- **Vulnerability Intelligence Sources:**
  - OSV.dev API integration with pagination, retries, and rate limiting.
  - Official CISA KEV catalog integration with 24-hour local disk cache.
  - Linux distribution tracker with backport detection for Ubuntu and Debian to eliminate false positives.
  - Local UTC-timestamped disk caching.
- **Verification & Safety:**
  - Post-patch verification checking effective installed versions rather than just exit codes.
  - Reboot detection (`/var/run/reboot-required` on Linux and Registry keys on Windows).
  - Elevation controls: Actions requiring Administrator or `sudo` are marked as blocked if not pre-delegated, avoiding silent elevation.
- **Reporting:**
  - Structured dual JSON and Markdown reporting with internationalization support and data source failure warnings.
- **Test Suite:**
  - Comprehensive unit tests with test fixtures for inventory, advisories, planning, execution, verification, and CLI flows.

