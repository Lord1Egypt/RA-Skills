<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-security-audit banner" width="100%" />
</p>

<h1 align="center">yotta-security-audit · 元安 (Yuan'an)</h1>

<p align="center">YottaMeta's AI-skill supply-chain & system security scan engine: <b>detects malicious skill patterns · scans system security baselines · audits student-data privacy risks</b>, purely read-only, zero-dependency and disciplined. Use it before installing a new skill, for periodic audits of installed skills, to check system security baselines, or to review a school data folder before sharing it.</p>
<p align="center">Activates when the user mentions security audit / skill security check / malicious detection / supply-chain security / system security baseline / student data / student privacy / school data compliance / scan skills / malicious skill, or asks to scan a skill or a class data folder.</p>
<p align="center">Python 3.8+ standard library, zero external dependencies; Windows + Linux; read-only detection, reports masked by default, with authorization & legal boundaries declared.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-security-audit"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-security-audit" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-audit"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-security-audit" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-audit/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-security-audit" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-audit"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

AI skills are becoming a new entry point for supply-chain attacks: a "normal-looking" skill can quietly steal credentials, exfiltrate data, or plant backdoors during install or runtime. Yuan'an turns these high-risk patterns into 13 detector classes, plus a system security baseline scan, to identify risk before install and during operation.

It is not tied to any single platform: an agent-agnostic toolkit that works in any agent supporting Agent Skills. Read-only detection, masked reports, never modifies the system, no resident service.

## Core value

- **Three-mode coverage** — skill mode (default) scans AI skill directories; system mode scans system security baselines (Windows / Linux platform-aware); education mode audits student-data privacy risks in folders, spreadsheets and documents.
- **Threat capture model** — 8 checkpoints (supply chain / command execution / network & exfil / file & sensitive path / prompt injection / remote download-exec / obfuscation / other) + 13 behavior items; dual-view report with health score (0-100).
- **13 detector classes** — covering backdoors, credential theft, data exfiltration, persistence, supply-chain install hooks, hidden characters, high-entropy payloads and other high-risk patterns.
- **Read-only & disciplined** — every check is a read operation; system mode also only runs read-only commands and never performs remediation, deletion or quarantine.
- **Masked by default** — reports do not output private-key contents, environment variable values or full credentials; only paths, patterns and suggestions.
- **Never echoes raw student data** — education mode reports only the rule class, location, hit count and a masked sample; there is no raw-value display option.
- **Auto-discover skill directories** — scanning all installed skills auto-discovers 17 agent skill directories.
- **Self-scan without false positives** — the scanner can scan itself without medium/high false positives (signature data files are auto-exempted).

## Why use it

| Advantage | Description |
|---|---|
| **Explainable detectors** | Each of the 13 detector classes has a clear focus and default level; a hit pinpoints the exact pattern and remediation suggestion |
| **Platform-aware** | System mode adapts to Windows / Linux; read-only commands never write to the system |
| **Graded exit codes** | 0=clean / 1=medium / 2=high / 3=critical / 4=error, easy to wire into automation and CI |
| **Extensible rules** | The rule table lives in scripts/audit_rules.py; --ioc-db accepts your own threat-intel feeds |
| **Authorization & legal boundaries** | Only authorized targets may be audited; scanning others' systems without authorization violates the Cybersecurity Law and Articles 285/286 of the Criminal Law |
| **Zero dependency** | Python 3.8+ standard library; no daemon / database; Windows + Linux |
| **Ecosystem distribution** | GitHub + npm synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Capability | Description |
|---|---|
| Skill mode (--target skill) | Scan AI skill directories with 13 detector classes; auto-discovers 17 agent skill directories |
| System mode (--target system) | System security baseline scan (startup entries, scheduled tasks, services, firewall, shares, permission points, etc.) |
| Education mode (--target edu) | Student-data privacy scan for folders / CSV / xlsx / docx; `--path` is required, reports are always masked |
| Single directory (--path) | Scan a skill directory before installing it |
| Report output | text + structured --json + --report Markdown report |
| Severity filter (--severity) | Report only high and above |

## The 13 detector classes

| Detector | Focus | Default level |
|---|---|---|
| DownloadExec | Download then pipe or drop a file to shell execution | critical |
| Obfuscation | Dynamic eval, encoded string construction, base64-decoded execution | high |
| Persistence | Scheduled tasks, startup agents/daemons, shell config, registry startup writes | high |
| Exfiltration | Read sensitive files then exfiltrate / archive and upload | high |
| CredentialTheft | SSH/cloud credentials, browser data, system credential-store access | critical |
| NetworkCall | Reverse connections, raw sockets, HTTP clients (mostly context-dependent) | medium |
| PrivilegeEscalation | Permission-bit changes, setuid, joining admin groups | high |
| SocialEngineering | Social-engineering wording in names (file names) | medium |
| Base64 | Overlong base64 strings (upgraded if decoding reveals sensitive keywords) | medium→high |
| IOCMatch | Known malicious IP/domain/URL patterns/file hashes | critical |
| PostInstallHook | Install-time lifecycle scripts (download/execute is critical) | high→critical |
| HiddenChar | Zero-width and bidirectional override characters | medium |
| Entropy | High-entropy encoded strings (suspected obfuscated/encrypted payloads) | medium |

> The rule table lives in scripts/audit_rules.py (signature data file, self-scan exempt); --ioc-db accepts your own threat-intel feeds.

## Education mode (--target edu)

Education mode reviews where student data lives and how risky the storage is: which files hold which kinds of personal information and whether they sit in paths that leave the machine.

| Rule | Focus | Default level |
|---|---|---|
| EDU-ID-001 | ID card numbers (18 digits + checksum) | critical |
| EDU-ID-002 / EDU-ID-003 | Mobile numbers / email addresses | high / medium |
| EDU-ID-004 | Student-number fields (header-driven) | medium |
| EDU-QI-001..004 | Name + score, birth date, home address, guardian contact | high |
| EDU-SA-001..004 | Health & wellbeing, financial-hardship status, biometric data, explicit minor markers | critical |
| EDU-HR-001..003 | Cloud-sync / messenger folders, file names carrying a name, AI-tool & temp directories | high / high / medium |

- Supported inputs: CSV / TSV / TXT / MD / JSON / XML / HTML / YAML, plus xlsx and docx (standard-library read-only parsing). PDF, images, legacy Office files and archives are counted as skipped, never OCR'd.
- Masking is fixed and repeatable: ID / student numbers and phones keep the last 4 digits, names keep the surname, addresses keep the first 3 characters, emails keep the first character and domain.
- The tool never infers age or identity, never links records across files, never goes online and never caches raw text. Only `--path` is scanned; there is no auto-discovery and no "scan the whole disk" mode.
- Rule packs are read-only JSON: replace or extend them with `--edu-rules ./school-rules.json`. Details: `references/student-data-scan.md`.

## Usage examples

```bash
# Scan all discovered skills (17 agent directories)
python3 scripts/yotta_audit.py --target skill

# Scan a single skill directory
python3 scripts/yotta_audit.py --path ./some-skill

# System security baseline (current platform)
python3 scripts/yotta_audit.py --target system --platform auto

# JSON + generate a Markdown report
python3 scripts/yotta_audit.py --path ./some-skill --json --report report.md

# Report only high and above
python3 scripts/yotta_audit.py --path ./some-skill --severity high

# Education mode: review a class data folder
python3 scripts/yotta_audit.py --target edu --path ./class-folder

# Education mode: one spreadsheet, JSON + Markdown report (the report must stay outside the scanned folder)
python3 scripts/yotta_audit.py --target edu --path ./scores.xlsx --json --report ./edu-report.md
```

**Exit codes**: **0** = clean / low only; **1** = medium; **2** = high; **3** = critical; **4** = scanner error.

## Install

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-security-audit --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-security-audit --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-security-audit.git <your-skills-dir>/yotta-security-audit
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-security-audit`, click **Code → Download ZIP**, unzip it and put the `yotta-security-audit` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.
## Upgrade / uninstall

- **Upgrade**: reinstall the latest version to overwrite — rerun the install command you used (e.g. `npx -y @yottameta/yotta-security-audit --agent <name>` or `bash install.sh --agent <name>`). Old files in the skill directory are replaced; other project files are untouched.
- **Uninstall**: delete the yotta-security-audit folder under the target agent's skills directory (see the table above). The skill stops taking effect after removal.

## FAQ

- **Does it actively fix risks?** No. Yuan'an only reads, detects and reports; it never performs remediation, deletion or quarantine. On findings, suggest the user isolate and stop using the skill first, then review manually.
- **Isn't scanning skills enough — why system mode?** Malicious skills often persist to the system via startup entries, scheduled tasks or services. System mode checks these baseline points; the two modes complement each other.
- **Is scanning other machines legal?** Only authorized targets may be audited. Scanning others' systems without authorization violates the Cybersecurity Law and Articles 285/286 of the Criminal Law; the user bears the legal responsibility.
- **Will the first run false-positive?** Detectors assign levels by pattern and context; NetworkCall / high-entropy / URL findings are mostly context-dependent hints that need scenario judgment; the scanner's self-scan has exemptions and does not produce medium/high false positives.

## Related skills

Part of the YottaMeta skill matrix (security family): [yotta-vetter](https://github.com/YottaMeta/yotta-vetter) (YuanShen, four-phase pre-install review) first runs source → code → permissions → risk review and guides high-and-above findings into Yuan'an deep scanning; [yotta-memory](https://github.com/YottaMeta/yotta-memory) (Yuanyi) handles cross-session long-term memory.

## Boundaries (security red lines)

- **Authorized targets only** — audit only explicitly authorized targets; unauthorized scanning of others' systems is illegal and the user's own responsibility.
- **Detect & report only** — never performs remediation, deletion or quarantine; remediation decisions belong to the user.
- **Masked by default** — no private keys, environment values or full credentials in output; only paths, patterns and suggestions.

## Development & validation

- Run at the project root: python tools/validate-skill.py yotta-security-audit
- Tests: python scripts/test_yotta_audit.py and python scripts/test_yotta_audit_cis.py (Windows: python)
- Details: references/threat-patterns.md, references/system-baseline.md, references/remediation-guide.md

Keep tests green and bump the version before releasing changes.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) © YottaMeta. "Yuan'an" / "yotta-security-audit" and the YottaMeta family names (yotta-* prefix) are YottaMeta brand identifiers; derived works must not reuse them, see [NOTICE](./NOTICE). The implementation is YottaMeta's own.
