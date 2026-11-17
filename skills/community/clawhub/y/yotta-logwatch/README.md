<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-logwatch banner" width="100%" />
</p>

<h1 align="center">yotta-logwatch · 元察 (Yuancha)</h1>

<p align="center">YottaMeta's zero-dependency security log analysis & detection engine: <b>login brute-force · Web attack scanning · suspicious PowerShell script blocks</b>, implemented with the pure Python 3.8+ standard library. It reads local logs read-only, works offline, and outputs Chinese teaching-style reports. Built for security triage, incident response, audit-log review, and red/blue team post-mortems.</p>
<p align="center">Activates when the user asks to analyze login / Web access / PowerShell logs, trace intrusion traces, or audit abnormal activity — <b>read-only local, no proactive scanning, no network, never modifies logs</b>.</p>
<p align="center">No external tools required; Windows + Linux + macOS; outputs a timeline plus Chinese plain-language explanations for each hit.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-logwatch"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-logwatch" /></a>
  <a href="https://github.com/YottaMeta/yotta-logwatch"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-logwatch" /></a>
  <a href="https://github.com/YottaMeta/yotta-logwatch/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-logwatch" /></a>
  <a href="https://github.com/YottaMeta/yotta-logwatch"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Security investigation often starts with logs: are there brute-force attempts in the login log, scans or webshell uploads in the Web access log, or suspicious commands in PowerShell script blocks? Yuancha packages these capabilities into a zero-dependency engine — no SIEM or external tools. It parses auth/secure, Web access logs (common/combined), PowerShell script-block logs, and Windows Event Log (Security/System) with the pure Python standard library, flags suspicious activity with heuristic rules, and outputs a timeline plus Chinese teaching-style explanations.

It is not tied to any single platform: it is an agent-agnostic toolkit that works in any agent supporting Agent Skills. **Read-only local logs** — no network, no proactive scanning, no modifications to any log content, and no resident service.

## Core value

- **Zero-dependency engine** — four log parsers + detection rules built entirely with Python 3.8+ standard library; no SIEM or external scanners.
- **Four log families** — auth/secure (brute-force / abnormal login / sudo escalation), Web access logs (scans / webshell / traversal / SQLi / suspicious UA), PowerShell script blocks (encoded / download-execute / reflection / AMSI bypass / obfuscation), Windows Event Log (login failures / abnormal login / account ops / log clearing / suspicious process).
- **Automatic type sniffing** — no need to specify the log type; it judges by line heuristics, or force it with `--type`.
- **Timeline + Chinese explanations** — hits are sorted by time; each includes type, severity, evidence line, Chinese explanation and a review suggestion.
- **Three output modes** — text / JSON (clean stdout) / Markdown report; `--output` writes to a file.
- **Tunable thresholds** — brute-force count (`--max-fail`), time window (`--window`), 404 flood (`--404-threshold`).

## Why use it

| Advantage | Description |
|---|---|
| **Zero dependency** | Python 3.8+ standard library; no daemon / database / external scanner; Windows + Linux + macOS |
| **Read-only offline** | Parses local log files only; no network, no proactive scanning, never modifies content |
| **Type-adaptive** | No manual type selection; auto-sniffs auth / web / powershell / winevt |
| **Explainable** | Each hit includes a Chinese explanation and review suggestion; only flags "suspicious", never gives exploitation details |
| **Tunable thresholds** | Brute-force / time-window / 404-flood thresholds adjustable to reduce noise |
| **Ecosystem distribution** | GitHub + npm + ClawHub synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Command | Description |
|---|---|
| scan | Parse local logs and detect by type; output text / JSON / Markdown report |
| --path / --recursive | Point to a log file or directory (a directory picks log-feature files by default; recursive available) |
| --stdin | Read logs from standard input (pipe) |
| --type | Force the log type (auth / web / powershell / winevt) |
| --min-severity | Show only hits at or above the given severity |
| --json / --report / --format | Switch output format (text / json / markdown) |
| --version | Print the version |

## Quick start

Use `python` on Windows, `python3` on Linux/macOS.

```bash
# Analyze a local auth log
python3 scripts/yotta_logwatch.py scan --path /var/log/auth.log

# Recursively scan all log-feature files under a directory and write a Markdown report
python3 scripts/yotta_logwatch.py scan --path /var/log/nginx --recursive --report report.md

# Force the Web type
python3 scripts/yotta_logwatch.py scan --path access.log --type web

# Show only medium and above
python3 scripts/yotta_logwatch.py scan --path auth.log --min-severity medium

# Tune brute-force / time-window thresholds
python3 scripts/yotta_logwatch.py scan --path auth.log --max-fail 3 --window 120

# Read from stdin (pipe)
type auth.log | python scripts/yotta_logwatch.py scan --stdin

# Print version
python3 scripts/yotta_logwatch.py --version
```

Exit codes: **0** = no hits; **1** = hits found; **4** = usage or read error.

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-logwatch --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-logwatch --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-logwatch.git <your-skills-dir>/yotta-logwatch
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-logwatch`, click **Code → Download ZIP**, unzip it and put the `yotta-logwatch` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Usage with an AI agent

1. Wire this repo's SKILL.md into any agent's skills / rules system (see Installation above).
2. When the user asks "are there brute-force attempts in the auth log?", run:
   ```bash
   python3 scripts/yotta_logwatch.py scan --path /var/log/auth.log
   ```
   You get a timeline of hits with type, severity, evidence and a Chinese explanation.
3. To focus on high-signal findings, filter by severity:
   ```bash
   python3 scripts/yotta_logwatch.py scan --path auth.log --min-severity high
   ```
4. For machine-readable output, use --json (clean stdout) for pipeline integration.
5. Always treat hits as "suspicious" prompts to verify manually — never as a confirmed attack.

## Detection rules

| Category | Hit type | Severity | Description |
|---|---|---|---|
| auth | brute_force | low~high | Repeated failed logins from one source (--max-fail threshold) |
| auth | credential_stuffing | high | One source tries many different usernames |
| auth | abnormal_login | high | Multiple failures then a success from the same source |
| auth | root_login | medium | Direct login as root from a source |
| auth | sudo_escalation / sudo_attempt | medium~high | sudo escalation / privilege attempt (not in sudoers) |
| web | path_traversal | high | Path traversal (../ or encoded variants) |
| web | sql_injection | high | SQL injection patterns |
| web | webshell_upload | critical | webshell upload / access trace |
| web | suspicious_ua | low | Known scanner / automation-tool UA |
| web | scanner_signature | medium | Hits multiple admin / sensitive paths |
| web | flood_404 | medium | 404 flood from one source (--404-threshold) |
| powershell | encoded_command | high | Encoded command / long base64 |
| powershell | download_execute | critical | Downloader + remote execution |
| powershell | reflection | medium | .NET / in-memory reflection load |
| powershell | amsi_bypass | critical | AMSI bypass strings |
| powershell | obfuscation | medium | iex / [char] / concat etc obfuscation |
| winevt | brute_force | low~high | Repeated 4625 failed logons from one source (--max-fail) |
| winevt | credential_stuffing | high | One source tries many usernames (4625) |
| winevt | abnormal_login | high | 4625 failures then 4624 success from the same source |
| winevt | rdp_logon / admin_logon | medium | 4624 remote desktop (Type 10) / admin logon |
| winevt | account_created / account_deleted | high | 4720 account created / 4726 account deleted |
| winevt | account_locked | medium | 4740 account locked out |
| winevt | group_member_add | medium~high | 4732/4728 member added (admin group → high) |
| winevt | audit_log_cleared | critical | 1102 audit log cleared |
| winevt | suspicious_process | low~critical | 4688 suspicious process creation (LOLBin / encoded cmd etc) |
| winevt | service_installed / task_created | medium | 7045 new service / 4698 scheduled task (persistence) |

## Boundaries (security red line)

- **Read-only local** — no network, no proactive scanning, never modify / delete / write any log content.
- **No exploitation** — every hit is only a "suspicious prompt + review suggestion"; no exploitation details are provided.
- **Authorization** — only for explicitly authorized / self-owned assets / CTF ranges / teaching environments. Analyzing others' systems without authorization violates the law; the user bears responsibility.

## Development & validation

- Tests: `python scripts/test_yotta_logwatch.py` (66 cases: sniffing / parsers / detection / pipeline / output / CLI exit codes 0/1/4; run inside the skill folder)
- Rule reference: references/auth-log-rules.md, references/web-log-rules.md, references/powershell-log-rules.md, references/windows-event-rules.md, references/analysis-spec.md

## Changelog

- v0.2.7 (2026-08-29): Install docs alignment — unified four install methods (npx -y @yottameta/yotta-logwatch --agent/--dir, git clone, GitHub Download ZIP, install.sh --agent/--dir/--list), removed the legacy GitHub-clone installer and global-install (-g) recommendations; bilingual README install section synced to 发布规范 §3.3.1. No functional change.

- v0.2.6 (2026-08-27): Publish-metadata sync — ClawHub republished via web UI "New version" at v0.2.6 with display name "元察 yotta-logwatch"/slug yotta-logwatch; GitHub + npm bumped to v0.2.6 to keep the three sources aligned; no functional/engine/rule change.
- v0.2.5 (2026-08-27): Publish-metadata fix — republished with `--name '元察 yotta-logwatch'` (quoted as a single argument) so the ClawHub card now shows the Chinese display name; no functional/engine/rule change.
- v0.2.4 (2026-08-27): Publish-metadata fix attempt — passed `--name 元察 yotta-logwatch` **without quotes**, so the shell split the value and the `--name` did not take effect; ClawHub card still showed bare `yotta-logwatch` (fixed in v0.2.5); no functional/engine/rule change.
- v0.2.3 (2026-08-27): Clean republish — v0.2.2 tarball accidentally included __pycache__ bytecode; 0.2.3 removes it (content identical), 0.2.2 deprecated on npm.
- v0.2.2 (2026-08-27): Docs fix — removed the repo-only `tools/validate-skill.py` reference from Development & validation (it is not shipped in the skill package); only the in-package test script remains.
- v0.2.1 (2026-08-27): Docs parity fix — README.zh-CN.md now covers all English sections (Usage with an AI agent / Detection rules / Boundaries / Development & validation / Changelog / License); EN/zh section structure aligned. No engine changes.
- v0.2.0 (2026-08-27): New Windows Event Log detection (winevt) — parses key=value / wevtutil text / XML exports of Security/System; 4625 brute-force aggregation, 4624 abnormal / admin / RDP logon, account created / deleted / locked, group member add, 1102 audit log cleared, 4688 suspicious process, 7045 service, 4698 scheduled task; plus the five-block analysis spec (references/analysis-spec.md). 66 tests green. See CHANGELOG.md.
- v0.1.0 (2026-08-27): Initial release — zero-dependency engine parsing auth/secure, Web access logs (common/combined) and PowerShell script blocks with automatic type sniffing; auth / web / powershell detection; text / JSON / Markdown output; 42 tests green.

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).