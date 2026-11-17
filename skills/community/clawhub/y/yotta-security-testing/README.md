<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-security-testing banner" width="100%" />
</p>

<h1 align="center">yotta-security-testing · 元测 (YuanCe)</h1>

<p align="center">YottaMeta's <b>disciplined, authorization-first security-testing methodology</b> for Agent skills:
a four-stage workflow — <b>Reconnaissance → Discovery → Verification → Reporting</b> — for web security testing on
<b>authorized targets only</b> (self-owned assets, SRC / bug-bounty scope, CTF and local training labs), backed by a
built-in <b>Scope Guard</b> that turns "authorized only" into a hard mechanism instead of a disclaimer.</p>
<p align="center">Triggers when the user asks for security testing / penetration testing / vulnerability assessment on an
authorized target, SRC bug bounty, CTF or lab drills (DVWA / OWASP Juice Shop / HTB / VulnHub), or a vulnerability
assessment / pentest report; or says 元测 / security test / pentest / bug bounty / authorized test / scope check.</p>
<p align="center">Zero dependencies (Python 3.8+ standard library); Windows + Linux + macOS;
methodology and education oriented — <b>no executable payloads</b>.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-security-testing"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-security-testing" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-testing"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-security-testing" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-testing/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-security-testing" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-testing"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

YuanCe is an **authorized security-testing workflow** — a methodology skill. It is **not** a vulnerability
scanner, **not** a training-lab skill and definitely **not** an attack tool. It teaches an agent how to run web
security testing in four disciplined stages on targets the user is *allowed* to test, and enforces authorization
with a hard mechanism so that **unauthorized targets are rejected by default**.

The skill market is full of "just run this payload" collections. YuanCe is the opposite: it teaches *how to test a
target you are allowed to test* — how to scope it, how to discover and verify issues, how to write a reproducible
report, and how to stay inside the authorized boundary (SRC platform rules, CTF rules, your own assets) while doing it.

## Scope Guard — five hard defenses (mechanism, not a disclaimer)

1. **Scope Guard**: every target operation must be confirmed in scope first; the CLI `scope check <target>` is a
   double check — unauthorized targets are rejected by default (non-zero exit code + clear error).
2. **Defaults to legal environments**: tutorials and playbooks cover local labs / CTF (DVWA, OWASP Juice Shop,
   HTB, VulnHub) *and* authorized real targets / SRC bug bounty; real targets must be registered in `scope.json`
   within the platform's authorized scope.
3. **Authorization declaration**: `scope init` declares authorization type and scope into
   `~/.yottasec/scope.json` (or a project-level `.yottasec/scope.json`); authorization comes from the file,
   never from a chat claim.
4. **Legal redlines**: authorized testing only; users are responsible for applicable law (e.g. China Cybersecurity
   Law, Criminal Law Articles 285/286). Positioning = methodology / teaching material.
5. **Audit trail**: every test records target / action / timestamp → `~/.yottasec/audit.log`
   (JSONL, on by default, no silent off switch).

## Four-stage methodology (used by every playbook)

| Stage | Output | Description |
|---|---|---|
| Reconnaissance | Asset list | Read-only collection of in-scope target info: entry points, tech stack, feature list, input surface |
| Discovery | Test-point list | Enumerate input points and test points per playbook; record candidate vulnerability hypotheses |
| Verification | Verification log | Minimal verification ("similar-to" wording, no copy-paste injection strings) to confirm the issue and impact |
| Reporting | Report draft | Report per template: target / time / findings / evidence / remediation; sensitive credentials are redacted |

Re-run `scope check` whenever the target or the action changes. For SRC / real targets: only test assets inside the
platform's authorized scope; stop and minimize evidence as soon as real user data is encountered.

## Playbook coverage

| # | Playbook | Covers | OWASP 2021 mapping |
|---|---|---|---|
| 00 | Vulnerability assessment & pentest report methodology | Four stages + report template + SRC practice | Full workflow |
| 01 | SQL injection testing | Injection | A03 Injection |
| 02 | Cross-site scripting (XSS) | Client-side script injection | A03 Injection |
| 03 | SSRF | Server-side request forgery | A10 SSRF |
| 04 | XXE | XML external entities | A05 Security Misconfiguration |
| 05 | Insecure deserialization | Deserialization flaws | A08 Software & Data Integrity |
| 06 | Authentication & access control | Auth flaws / broken access control | A01 / A07 Broken Access Control |
| 07 | API security | API attack surface | OWASP API Top 10 mapping |
| 08 | Command injection | OS command concatenation | A03 Injection |
| 09 | File upload | Upload validation bypass | A05 Security Misconfiguration |
| 10 | Business logic flaws | Parameter tampering / step skipping / races | A01 / A04 |
| 11 | Sensitive information disclosure | Backups / source / errors / headers | A05 Security Misconfiguration |
| 12 | Security misconfiguration | Security headers / CORS / defaults | A05 Security Misconfiguration |

Each playbook has a fixed six-section structure: target identification & confirmation → detection approach →
verification method → defensive view → hands-on drill (labs / authorized target / SRC) → audit trail & report;
it applies to both lab challenges and real authorized scenarios.

## Commands

| Command | Description |
|---|---|
| scope init | Initialize the authorization allowlist (default deny) |
| scope add | Add an authorized target (`--type` = self-owned / ctf / bug-bounty / training / explicit) |
| scope check | Three-layer target triage: allowlist → type recognition → default deny |
| scope list / remove | View / remove authorization entries |
| report generate | Generate a vulnerability assessment / pentest report from findings.json (Markdown / JSON, credentials redacted) |
| audit log | View / filter / export the audit trail (on by default) |
| --version | Print version |

## Usage

Windows uses `python`, Linux/macOS uses `python3`.

```bash
# 1) Initialize the authorization allowlist (default deny; declare your scope first)
python3 scripts/yotta_security_testing.py scope init --owner <you>

# 2) Add authorized targets (local labs / CTF / bug bounty / self-owned / explicit authorization)
python3 scripts/yotta_security_testing.py scope add --type ctf --target 127.0.0.1 --note dvwa
python3 scripts/yotta_security_testing.py scope add --type bug-bounty --target api.example.com --note "SRC scope (per platform page)"
python3 scripts/yotta_security_testing.py scope add --type self-owned --target example.com --scope "*.example.com" --expires 2027-12-31

# 3) Target triage: allowed (exit 0) / unauthorized reject (exit 1) / absolutely forbidden (exit 2)
python3 scripts/yotta_security_testing.py scope check http://127.0.0.1/dvwa
python3 scripts/yotta_security_testing.py scope check api.example.com --json

# 4) Generate a vulnerability assessment report (from findings.json; credentials auto-redacted)
python3 scripts/yotta_security_testing.py report generate findings.json --out report.md

# 5) Audit trail (on by default): view / filter / export
python3 scripts/yotta_security_testing.py audit log --result deny
python3 scripts/yotta_security_testing.py audit log --export audit-deny.jsonl
```

Exit codes: **0** = allowed; **1** = unauthorized (rejected by default); **2** = absolutely forbidden
(cloud metadata endpoints and similar).

## Installation

Pick any of the four methods below; the order is the recommended priority. Skill files always come from
**npm** (GitHub can be slow without a proxy; npm supports mirrors).

### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-security-testing --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-security-testing --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-security-testing.git <your-skills-dir>/yotta-security-testing
```

### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-security-testing`, click **Code → Download ZIP**, unzip it and put the
`yotta-security-testing` folder into the agent's skills directory.

### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.

## Development & validation

The package ships its own test suite (included in the published package):

```bash
# Run the full suite (444 cases) from the skill directory
python scripts/test_yotta_security_testing.py
```

References: `references/tutorial.md` (Chinese tutorial, full walkthrough with SRC practice),
`references/report-template.md` (report template with findings schema), `playbooks/00-methodology.md` (methodology).

## License

MIT © YottaMeta — see [LICENSE](./LICENSE).