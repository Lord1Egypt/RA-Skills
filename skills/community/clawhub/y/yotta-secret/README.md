<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-secret banner" width="100%" />
</p>

<h1 align="center">yotta-secret · 元钥 (Yuanyao)</h1>

<p align="center">YottaMeta's zero-dependency secret & credential leak scanner: finds <b>cloud API keys, private keys, credential assignments, URL-embedded credentials and high-entropy tokens</b> in source code, config files, .env and git history using <b>regex + entropy + format validation</b>; outputs <b>text / JSON / CSV</b> with secrets masked by default.</p>
<p align="center">Activates when the user needs to check a repo / config for leaked API keys, passwords, private keys or tokens before commit or release, scan directories or git history for hardcoded credentials, verify whether a string looks like a known key format, or redact secrets from logs / tickets before sharing — <b>fully local and offline: no connectivity checks, no data leaves the machine</b>.</p>
<p align="center">No external tools required (Python 3.8+ standard library); Windows + Linux + macOS; every result ships a masked secret form plus a Chinese plain-language context line.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-secret"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-secret" /></a>
  <a href="https://github.com/YottaMeta/yotta-secret"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-secret" /></a>
  <a href="https://github.com/YottaMeta/yotta-secret/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-secret" /></a>
  <a href="https://github.com/YottaMeta/yotta-secret"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## What it is

Hardcoded API keys, passwords and private keys are a leak source: once they land in git history they are nearly impossible to remove for real. Yuanyao packages "secret triage" into a zero-dependency engine — no gitleaks / trufflehog required. It runs a three-layer check (regex format → Shannon entropy → value-level validation) purely with the Python standard library, so you can find suspected secrets before commit, release or sharing.

It is not tied to any single platform: an agent-agnostic toolkit that works in any agent supporting Agent Skills. **Fully local and offline** — no connectivity checks, no data leaves the machine, no resident service.

## Core value

- **Zero-dependency engine** — five detection categories with a three-layer check, built entirely with Python 3.8+ standard library.
- **Five categories** — cloud (AWS / Google / OpenAI / GitHub / Slack / Stripe / JWT and more), private_key (PEM / PGP / OpenSSH / PuTTY), credential (assignments such as `DB_PASSWORD=`, including `MYAPP_SECRET=` suffixed keys), url_userinfo (credentials embedded in URLs), generic (high-entropy long tokens).
- **Three-layer check** — regex format → Shannon entropy threshold → value-level validation (pure-hash / UUID / placeholder / sample-value filtering) to keep false positives low.
- **git history scanning** — `--git` walks `git log -p` and checks added lines only, tagging every finding with commit and path to locate the leak source.
- **Masked by default** — output keeps only the head/tail of a secret (e.g. `ghp_****abcd`); `--show-secret` reveals it, preventing secondary leaks.
- **Three output modes** — text / JSON / CSV, ready for CI gates, YottaGuardian audit logs or human review.

## Why use it

| Advantage | Description |
|---|---|
| **Zero dependency** | Python 3.8+ standard library; no daemon / database / external scanner; Windows + Linux + macOS |
| **Fully local offline** | Scans existing files and text only; no connectivity checks, no data leaves the machine |
| **Low false positives** | Placeholder / sample / env-var-reference filtering, pure-hash and UUID exclusion, medium-confidence keys need longer or higher-entropy values |
| **Leak-source location** | git history scan tags every finding with commit and path — not just "there is a leak" but "which commit introduced it" |
| **No secondary leaks** | Masked output by default; the mask subcommand redacts logs / tickets (same wordlist as YuanShi / yotta-logs) |
| **Ecosystem distribution** | GitHub + npm + ClawHub synced; four install methods (npx / git clone / Download ZIP / install.sh) |

## Commands

| Command | Description |
|---|---|
| scan | Scan files / directories / stdin / git history for suspected secrets |
| scan --path / --stdin | Input from a file / standard input |
| scan --git | Scan git history (added lines, tagged with commit) |
| scan --types | Only the given categories (cloud,private_key,credential,url_userinfo,generic) |
| scan --format | Output format (text / json / csv) |
| scan --show-secret | Show secrets in plain text (masked by default) |
| scan --exclude | Exclude path patterns (fnmatch, repeatable) |
| scan --output | Write results to a file (default: stdout) |
| verify | Check whether a single value looks like a secret (--value / --stdin) |
| mask | Redact suspected secrets in text (same wordlist as yotta-logs) |
| entropy | Compute Shannon entropy |
| --version | Print the version |

## Quick start

### Install

Pick any of the four methods below; the order is the recommended priority. Skill files always come from **npm** (GitHub can be slow without a proxy; npm supports mirrors).

#### Method 1: npm one-liner (recommended)

```text
# Optional China mirror: npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-secret@0.2.4 --agent <agent-name>      # install to the agent's default user-level skills dir
npx -y @yottameta/yotta-secret@0.2.4 --dir <your-skills-dir>   # point to the skills dir itself (e.g. ~/.codex/skills)
```

- `--agent <name>` installs to that agent's default user-level directory; `--list` shows each agent's default directory.
- `--dir <path>` installs to the given directory; for agents not in the preset list, point `--dir` at their skills directory.
- If the mirror has not synced the new package (404): add `--registry=https://registry.npmjs.org/` (a proxy may be needed in China), or wait for the mirror cache.

#### Method 2: git clone (developers / git available)

```text
git clone https://github.com/YottaMeta/yotta-secret.git <your-skills-dir>/yotta-secret
```

#### Method 3: GitHub Download ZIP (manual / no git)

On the GitHub repository `YottaMeta/yotta-secret`, click **Code → Download ZIP**, unzip it and put the `yotta-secret` folder into the agent's skills directory.

#### Method 4: install.sh (multi-agent one-liner script)

```text
bash install.sh --agent <name>   # install to the agent's default user-level directory
bash install.sh --dir <path>     # install to the given directory
bash install.sh --list           # list agents -> default directories
```

> Method 1 uses the npm registry (npmmirror / npmjs) and does not depend on GitHub; Methods 2/3 use GitHub and may fail without a proxy in China.

Windows uses python, Linux/macOS uses python3.

```bash
# Scan a directory (recursive; skips .git / node_modules / binaries)
python3 scripts/yotta_secret.py scan --path src/

# Read from standard input, output JSON
cat dump.txt | python3 scripts/yotta_secret.py scan --stdin --format json

# Only cloud keys and private keys
python3 scripts/yotta_secret.py scan --path . --types cloud,private_key

# Scan git history (added lines), output CSV
python3 scripts/yotta_secret.py scan --git --path repo/ --format csv --output report.csv

# Verify whether a single value looks like a secret
python3 scripts/yotta_secret.py verify --value ghp_xxxxxxxxxxxxxxxx

# Redact suspected secrets in a text file
python3 scripts/yotta_secret.py mask --path notes.txt --output safe.txt
```

Exit codes: **scan 0** = clean; **1** = suspected secrets found; **4** = usage / read / git-unavailable error. verify returns 1 when a rule matches, 0 otherwise.

### Working with YuanShi (yotta-logs)

- Yuanyao covers the **source**: scan source code and git history before commit / release to find leaked secrets;
- YuanShi covers the **output**: redacts secrets by default when searching session logs, so logs do not leak secrets again;
- Both share the same wordlist: the mask subcommand behaves like YuanShi's redact; this engine's rules are a superset. See references/integration.md for the mapping.

### Working with YottaGuardian (yotta-guardian)

- Run `scan` before writing / committing: exit code 1 = suspected secrets found → block and ask for manual review;
- Feed `scan --format json` output to YottaGuardian for audit logs, or use it as a CI gate:
  ```bash
  python3 scripts/yotta_secret.py scan --path . --format json --output secret-report.json
  # abort commit / build on non-zero exit
  ```

## Detection categories

| Category | Chinese | Example | Description |
|---|---|---|---|
| cloud | 云厂商 / SaaS 密钥 | `AKIA…` `ghp_…` `sk-…` `eyJ…` | AWS / Google / OpenAI / GitHub / Slack / Stripe / JWT and 20+ more rules |
| private_key | 私钥 | `-----BEGIN RSA PRIVATE KEY-----` | PEM / PGP / OpenSSH / PuTTY private-key blocks |
| credential | 凭据赋值 | `DB_PASSWORD=…` `api_key=…` | high-confidence key names + non-placeholder values (incl. suffixed keys) |
| url_userinfo | URL 内嵌凭据 | `https://admin:hunter2@…` | credentials embedded in URL userinfo |
| generic | 高熵长 Token | 40+ char high-entropy strings | fallback for prefix-less high-entropy tokens (medium, human review) |

Full rule catalog: references/rules.md; entropy thresholds & format validation: references/entropy-and-verification.md.

## Output formats

- **text**: human-readable report grouped by category (severity / file:line / masked secret / entropy / context);
- **json**: `{tool, version, generated, source, summary, findings[], rules[]}`; each finding carries `rule_id / rule_name / category / severity / file / line / secret / entropy / length / snippet / commit`;
- **csv**: `rule_id,rule_name,category,severity,file,line,secret,entropy,length,snippet,commit,path_in_commit`.

## Boundaries (security red lines)

- **Fully local offline**: no connectivity checks, no leak-database lookups, no data leaves the machine;
- **No verdicts**: results are only "suspected secrets"; whether they are real requires human review; remediation (rotate / move to a secret manager / scrub history) is decided by the user;
- **Authorization**: for explicitly authorized / own-asset / educational environments only; scanning others' data without authorization violates the law and is the user's own responsibility.

## Development & validation

The package ships its test suite (included in the npm package files):

```bash
python scripts/test_yotta_secret.py   # 91 tests (Windows: python)
```

Keep tests green and bump the version before releasing changes.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) © YottaMeta. "Yuanyao" / "yotta-secret" and the YottaMeta family names (yotta-* prefix) are YottaMeta brand identifiers; derived works must not reuse them, see [NOTICE](./NOTICE).