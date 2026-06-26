---
name: skill-guard
version: 4.0.0
description: "SkillShield v4 — Ultimate security scanner for OpenClaw skills. 65 security checks, SARIF v2.1.0 output, CI/CD ready, campaign detection, C2 IP blocklist, known malicious actor database, macOS attack detection, agent config tampering, LLM tool exploitation, pre-commit hooks, and more. Python 3 stdlib only. Single file. Zero dependencies."
---

# SkillShield v4.0.0 — Ultimate Edition 🛡️

**65 security checks** | **SARIF v2.1.0** | **CI/CD ready** | **Zero dependencies**

The most comprehensive security scanner for OpenClaw/ClawHub skills. Detects malware, credential theft, exfiltration, prompt injection, campaign signatures, agent takeover, macOS-specific attacks, and more.

## Feature Comparison

| Feature | SkillShield v4 | Skillvet v2 |
|---------|:-:|:-:|
| Total security checks | **65** | 48 |
| Python 3 stdlib only | ✅ | ❌ (bash) |
| Single file | ✅ | ❌ (multi-file) |
| SARIF v2.1.0 output | ✅ | ✅ |
| JSON output | ✅ | ✅ |
| Summary mode | ✅ | ✅ |
| Verbose mode | ✅ | ✅ |
| Pre-commit hook | ✅ | ✅ |
| GitHub Actions template | ✅ | ✅ |
| HTML dashboard report | ✅ | ❌ |
| Markdown report | ✅ | ❌ |
| Interactive mode | ✅ | ❌ |
| Quarantine system | ✅ | ❌ |
| Baseline/tamper detection | ✅ | ❌ |
| SBOM generation | ✅ | ❌ |
| Diff scanning | ✅ | ❌ |
| Custom rules engine | ✅ | ❌ |
| Risk scoring (weighted) | ✅ | ✅ |
| Check IDs (SS-001+) | ✅ | ✅ |
| Exit codes (0/1/2) | ✅ | ✅ |
| Known C2/IOC IP blocklist | ✅ | ✅ |
| Known malicious actors | ✅ | ✅ |
| Exfiltration endpoints | ✅ | ✅ |
| Paste service detection | ✅ | ✅ |
| Campaign detection (3) | ✅ | ❌ |
| Behavioral analysis | ✅ | ❌ |
| macOS attack detection | ✅ | ✅ |
| Agent config tampering | ✅ | ✅ |
| LLM tool exploitation | ✅ | ✅ |
| String evasion detection | ✅ | ✅ |
| Punycode domains | ✅ | ✅ |
| Double encoding | ✅ | ✅ |
| Password archive detection | ✅ | ✅ |
| Network fingerprinting | ✅ | ❌ |
| Reputation grading | ✅ | ❌ |
| Context-aware domain checks | ✅ | ❌ |
| Inline ignore comments | ✅ | ✅ |
| .skillshield-ignore file | ✅ | ✅ (.skillvetrc) |
| Max file size option | ✅ | ✅ |
| Max depth option | ✅ | ✅ |
| 16 file types scanned | ✅ | ✅ |
| Statistics footer | ✅ | ✅ |

## Usage

### Scan all skills

```bash
python3 skills/skill-guard/scripts/skillguard.py scan
```

### Check a single skill

```bash
python3 skills/skill-guard/scripts/skillguard.py check skills/some-skill
```

### Check a directory of skills

```bash
python3 skills/skill-guard/scripts/skillguard.py check /path/to/skills
```

### Output Formats

```bash
# JSON output (for automation)
python3 scripts/skillguard.py check skills/some-skill --json

# SARIF v2.1.0 (for GitHub Code Scanning / VS Code)
python3 scripts/skillguard.py check skills/some-skill --sarif

# Summary mode (one-line per skill)
python3 scripts/skillguard.py scan --summary

# Verbose mode (debug check progress)
python3 scripts/skillguard.py scan --verbose

# HTML dashboard
python3 scripts/skillguard.py scan --html report.html

# Markdown report
python3 scripts/skillguard.py scan --report report.md
```

### CI/CD Integration

**GitHub Actions (SARIF upload):**

```yaml
- name: Run SkillShield
  run: python3 skills/skill-guard/scripts/skillguard.py check skills/ --sarif > results.sarif || true

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

**Generate GitHub Actions workflow:**

```bash
python3 scripts/skillguard.py ci > .github/workflows/skillshield.yml
```

**Pre-commit hook:**

```bash
python3 scripts/skillguard.py hook > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean — no issues found |
| 1 | Warnings only — suspicious findings |
| 2 | Critical/malicious findings |

### All Commands

| Command | Description |
|---------|-------------|
| `scan [dir]` | Scan all skills (default: ~/clawd/skills/) |
| `check <path>` | Scan a single skill or directory |
| `watch [dir]` | One-liner summary for cron alerting |
| `diff <name>` | Compare skill against baseline |
| `quarantine <name>` | Move malicious skill to quarantine |
| `unquarantine <name>` | Restore from quarantine |
| `list-quarantine` | Show quarantined skills |
| `sbom <name>` | Generate Software Bill of Materials (JSON) |
| `hook` | Generate git pre-commit hook |
| `ci` | Generate GitHub Actions workflow |

### All Options

| Flag | Description |
|------|-------------|
| `--json` | Machine-readable JSON output |
| `--sarif` | SARIF v2.1.0 output |
| `--summary` | One-line per skill output |
| `--verbose` | Show check progress |
| `--report <path>` | Markdown report file |
| `--html <path>` | HTML dashboard report |
| `--baseline` | Force re-baseline hashes |
| `--interactive` | Review findings interactively |
| `--ci` | Generate GitHub Actions workflow |
| `--max-file-size N` | Skip files > N bytes |
| `--max-depth N` | Limit traversal depth |

### False Positive Suppression

**File-level:** Create `.skillshield-ignore` in the skill:

```
Base64 encode/decode operation
HTTP request to unknown domain: my-legit-api.com
```

**Inline:** Add `# skillshield-ignore` comment:

```python
url = "https://bit.ly/legit-link"  # skillshield-ignore
```

## Security Checks (65 total)

### Check IDs (SS-001 through SS-065)

| ID | Check | Severity | Weight |
|----|-------|----------|--------|
| SS-001 | Outbound HTTP request | WARNING | 3 |
| SS-002 | eval/exec call | WARNING | 5 |
| SS-003 | Dynamic import | WARNING | 5 |
| SS-004 | Base64 decode operation | WARNING | 4 |
| SS-005 | Base64 decodes to suspicious content | CRITICAL | 9 |
| SS-006 | Hex string decodes to suspicious content | CRITICAL | 9 |
| SS-007 | URL shortener detected | WARNING | 5 |
| SS-008 | Executable data URI | WARNING | 5 |
| SS-009 | Hardcoded secret | CRITICAL | 10 |
| SS-010 | SSL verification disabled | WARNING | 5 |
| SS-011 | PATH modification | CRITICAL | 8 |
| SS-012 | Library path modification | CRITICAL | 8 |
| SS-013 | Shell execution (os.system) | WARNING | 4 |
| SS-014 | subprocess with shell=True | CRITICAL | 7 |
| SS-015 | Sensitive file access | CRITICAL | 8 |
| SS-016 | Reverse shell pattern | CRITICAL | 10 |
| SS-017 | DNS exfiltration | CRITICAL | 9 |
| SS-018 | Crontab modification | CRITICAL | 8 |
| SS-019 | System service creation | CRITICAL | 8 |
| SS-020 | Shell RC file modification | CRITICAL | 8 |
| SS-021 | Time bomb pattern | WARNING | 6 |
| SS-022 | Pickle deserialization | CRITICAL | 9 |
| SS-023 | Prompt injection override | CRITICAL | 9 |
| SS-024 | Prompt injection exfiltration | CRITICAL | 9 |
| SS-025 | Social engineering phrase | WARNING | 5 |
| SS-026 | SVG JavaScript | CRITICAL | 8 |
| SS-027 | SVG event handler | WARNING | 5 |
| SS-028 | npm lifecycle hook | CRITICAL | 8 |
| SS-029 | Typosquat package | WARNING | 6 |
| SS-030 | Binary executable | CRITICAL | 9 |
| SS-031 | Symlink to sensitive path | CRITICAL | 8 |
| SS-032 | Archive file | WARNING | 4 |
| SS-033 | Unicode homoglyph | CRITICAL | 7 |
| SS-034 | ANSI escape injection | WARNING | 5 |
| SS-035 | Writes outside skill dir | WARNING | 5 |
| SS-036 | COMBO: sensitive + outbound | CRITICAL | 10 |
| SS-037 | COMBO: subprocess + sensitive | CRITICAL | 8 |
| SS-038 | Campaign signature match | CRITICAL | 10 |
| SS-039 | BEHAVIORAL: staged exfiltration | CRITICAL | 9 |
| SS-040 | BEHAVIORAL: download + exec | CRITICAL | 9 |
| SS-041 | BEHAVIORAL: env harvest + network | CRITICAL | 9 |
| SS-042 | Clipboard access | WARNING | 4 |
| SS-043 | Bulk env variable capture | CRITICAL | 9 |
| SS-044 | Permission mismatch (trojan) | CRITICAL | 8 |
| SS-045 | Known C2/IOC IP address | CRITICAL | 10 |
| SS-046 | Known exfiltration endpoint | CRITICAL | 10 |
| SS-047 | Paste service reference | CRITICAL | 7 |
| SS-048 | GitHub raw content execution | CRITICAL | 9 |
| SS-049 | macOS Gatekeeper bypass (xattr) | CRITICAL | 9 |
| SS-050 | macOS osascript social engineering | CRITICAL | 8 |
| SS-051 | TMPDIR payload staging | CRITICAL | 9 |
| SS-052 | Keychain theft | CRITICAL | 10 |
| SS-053 | Password-protected archive | CRITICAL | 7 |
| SS-054 | Double-encoded path bypass | CRITICAL | 7 |
| SS-055 | Punycode domain (IDN attack) | CRITICAL | 7 |
| SS-056 | String construction evasion | CRITICAL | 7 |
| SS-057 | Process persistence + network | CRITICAL | 9 |
| SS-058 | Agent config tampering | CRITICAL | 9 |
| SS-059 | LLM tool exploitation | CRITICAL | 9 |
| SS-060 | Fake prerequisite pattern | CRITICAL | 7 |
| SS-061 | Network fingerprinting + exfil | WARNING | 6 |
| SS-062 | Known malicious actor | CRITICAL | 10 |
| SS-063 | Nohup/disown + network | CRITICAL | 9 |
| SS-064 | chmod +x on downloaded file | CRITICAL | 8 |
| SS-065 | open -a with downloaded binary | CRITICAL | 8 |

### Campaign Detection

- **ClawHavoc** — 386-skill wallet theft campaign with C2 beacons
- **twitter-enhanced** — Typosquatting popular skills with hidden eval/exec
- **ClickFix** — Social engineering to run clipboard commands

### Known C2/IOC IP Blocklist

Based on reports from [Koi Security](https://www.koi.ai/blog/clawhavoc), [Bitdefender](https://businessinsights.bitdefender.com/), [Snyk](https://snyk.io/articles/clawdhub-malicious-campaign/):

- `91.92.242.30` — AMOS C2 server
- `54.91.154.110` — AMOS C2 server
- `185.215.113.16` — ClawHavoc dropper relay
- `45.61.136.47` — AMOS stage-2 payload
- `194.169.175.232` — Atomic Stealer C2
- `91.92.248.52` — ClawHavoc wallet exfil
- `79.137.207.210` — Bandit Stealer C2
- `45.155.205.172` — Generic macOS stealer C2

### Known Malicious Actors

- zaycv, Ddoy233, Sakaen736jih, Hightower6eu, aslaep123, davidsmorais, clawdhub1

## File Types Scanned

`.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.sh`, `.bash`, `.rs`, `.go`, `.rb`, `.c`, `.cpp`, `.md`, `.json`, `.svg`, `.yml`, `.yaml`, `.toml`, `.txt`, `.cfg`, `.ini`, `.html`, `.css`, `.env*`, `Dockerfile*`, `Makefile`, `pom.xml`, `.gradle`

## Performance

- 25 real skills in **< 1 second**
- 16 test cases in **< 0.5 seconds**
- Single Python 3 file, zero dependencies
- 2,800 lines of pure stdlib Python
