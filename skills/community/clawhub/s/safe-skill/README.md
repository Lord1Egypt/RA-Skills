# Safe-Skill

Programmatic security scanner for AI agent skills. Static analysis with real teeth.

> 静态分析不是万能的，但没有静态分析是万万不能的。

## Why This Exists

The AI agent skill ecosystem (OpenClaw, Claude Skills, etc.) is growing fast — [13,700+ skills on ClawHub](https://clawhub.ai) as of early 2026. But there's no `npm audit` equivalent. The existing [skill-vetter](https://clawhub.ai/spclaudehome/skill-vetter) is a prompt-only checklist — it tells the agent *what to look for*, but the agent does all the work by eyeballing. That's like asking a junior dev to do a security review by reading a OWASP cheatsheet.

**Safe-Skill** replaces the eyeball with a real scanner: regex pattern matching, Python AST analysis, Shannon entropy detection, URL/IP extraction, and permission scope inference. Zero external dependencies. Runs anywhere Python 3.8+ exists.

## Quick Start

### As an OpenClaw Skill (recommended for end users)

```bash
# Install from ClawHub
clawhub install zhangjie/safe-skill

# Then just ask your agent:
# "vet this skill before installing it"
# "scan clawhub:someone/some-skill for security issues"
# "审查这个skill的安全性"
```

### As a Standalone CLI Tool

```bash
git clone https://github.com/zhangjie/safe-skill.git
cd safe-skill

# Scan a local skill directory
python3 scripts/scan.py /path/to/skill/

# Scan a single file
python3 scripts/scan.py /path/to/SKILL.md

# JSON output (for CI/pipelines)
python3 scripts/scan.py /path/to/skill/ --json

# Save report
python3 scripts/scan.py /path/to/skill/ -o report.txt

# Verbose mode (show clean files too)
python3 scripts/scan.py /path/to/skill/ -v
```

### Remote Fetch + Scan

```bash
# Fetch from GitHub and scan
python3 scripts/fetch_and_scan.py https://github.com/openclaw/skills/tree/main/skills/someone/cool-skill

# Fetch from ClawHub slug
python3 scripts/fetch_and_scan.py clawhub:someone/cool-skill

# GitHub shorthand
python3 scripts/fetch_and_scan.py github:openclaw/skills/skills/someone/cool-skill

# With JSON output
python3 scripts/fetch_and_scan.py clawhub:someone/cool-skill --json
```

## What It Detects

### Five Analysis Passes

| Pass | What It Does | Catches |
|------|-------------|---------|
| **Pattern Matching** | 65+ regex rules across 10 categories | `curl\|sh`, credential theft, data exfiltration, obfuscation |
| **Python AST** | Parses code structure, not just text | `eval(dynamic_var)` vs `eval("literal")` — only flags the dangerous one |
| **Entropy Detection** | Shannon entropy on long strings | Base64-encoded payloads, hex blobs, encrypted data |
| **URL/IP Extraction** | Finds all external endpoints | Hardcoded IPs, `.onion` addresses, tunnel services |
| **Permission Inference** | Maps what the skill accesses | Files, network, commands, env vars, packages |

### Detection Categories

| Category | Examples | Rule Count |
|----------|----------|------------|
| `rce` | `curl\|bash`, `eval()`, `exec()`, `subprocess`, `os.system` | 12 |
| `exfil` | `requests.post`, `urllib`, raw sockets, SMTP | 7 |
| `credential` | `~/.ssh`, `~/.aws`, keyring, dotenv, cookies | 11 |
| `obfuscation` | base64 decode, ROT ciphers, `marshal.loads`, `pickle` | 8 |
| `escalation` | `sudo`, `chmod`, `/etc/shadow`, SUID/SGID | 5 |
| `agent_identity` | `MEMORY.md`, `SOUL.md`, `.claude/`, system prompt | 5 |
| `persistence` | crontab, shell profiles, systemd, LaunchAgent, git hooks | 5 |
| `network` | hardcoded IPs, ngrok, pastebin, `.onion` | 4 |
| `filesystem` | `shutil.rmtree`, system directory access | 4 |
| `package` | ad-hoc `pip install`, custom index, git URLs | 4 |

### Markdown Context Awareness

Security documentation often *describes* the very patterns it warns against. A naive scanner flags these as threats. Safe-Skill parses Markdown structure — headings, code blocks, bullet lists — and **automatically downgrades findings** that appear under documentation headings (containing words like "red flag", "warning", "reject", "danger", etc.).

| Scanned Target | Naive Scanner | Safe-Skill |
|---|---|---|
| Original skill-vetter (pure documentation) | 235 / EXTREME | **11 / LOW** |
| Actual malicious skill | 500 / EXTREME | **425 / EXTREME** |
| Clean skill | 0 / CLEAN | **0 / CLEAN** |

## Risk Scoring

Quantitative score (0-100+) based on weighted findings:

| Severity | Points | Example |
|----------|--------|---------|
| Critical | 25 | `curl\|bash`, `~/.ssh` access, crontab injection |
| High | 15 | `eval()`, `subprocess`, base64 decode |
| Medium | 8 | `os.popen`, ad-hoc `pip install`, paste sites |
| Low | 3 | bare `except: pass` |
| Info | 1 | documentation-context findings |

| Score | Level | Verdict | Exit Code |
|-------|-------|---------|-----------|
| 0 | CLEAN | Safe to install | 0 |
| 1-15 | LOW | Safe to install | 0 |
| 16-40 | MEDIUM | Install with caution | 1 |
| 41-80 | HIGH | Human review required | 2 |
| 81+ | EXTREME | Do not install | 2 |

## Whitelist Configuration

Create a `.vetterrc` (JSON) in the skill directory to suppress known-good patterns:

```json
{
    "ignore_rules": ["CRED-007", "PKG-001"],
    "ignore_categories": ["package"],
    "trusted_domains": ["api.github.com", "registry.npmjs.org"],
    "accept_severity": "low",
    "inline_suppressions": [
        {"file": "setup.py", "line": 42, "rule": "RCE-007"}
    ]
}
```

## CI Integration

```yaml
# GitHub Actions example
- name: Vet skill before merge
  run: |
    python3 scripts/scan.py ./my-skill/ --json -o scan-report.json
    # Exit code 2 = HIGH/EXTREME risk -> fail the build
```

```bash
# Shell script guard
python3 scripts/scan.py ./skill-to-install/
if [ $? -eq 2 ]; then
    echo "BLOCKED: High-risk skill"
    exit 1
fi
```

## Test Results

Validated against 49 labeled samples (12 malicious, 8 benign, 6 adversarial, 23 real ClawHub skills):

| Metric | Value |
|--------|-------|
| Precision | 92.3% |
| Recall | 100% |
| F1 Score | 96.0% |
| Accuracy | 95.0% |

## Limitations

Transparency matters. This tool **cannot**:

- **Run code in a sandbox** — static analysis only. Time-delayed payloads, conditional execution paths, and runtime-generated code are invisible.
- **Check domain reputation** — URL classification is heuristic (known-safe list + IP detection). It doesn't query threat intelligence feeds.
- **Defeat creative obfuscation** — variable indirection across files, string splitting, polyglot payloads, and steganography can evade pattern matching. AST analysis helps for Python but not for shell/JS.
- **Replace human judgment** — it's a first-pass triage tool. Context matters. A skill that legitimately wraps `subprocess` for git operations will trigger findings that are false positives.

## Architecture

```
safe-skill/
├── SKILL.md                  # OpenClaw skill manifest + agent instructions
├── README.md                 # This file
├── .vetterrc.example         # Example whitelist config
├── scripts/
│   ├── scan.py               # Core scanner (standalone, zero deps)
│   └── fetch_and_scan.py     # Remote fetch + scan orchestrator
├── tests/                    # Test suite (not included in ClawHub distribution)
│   ├── test_scan.py          # Automated regression tests
│   ├── malicious/            # 12 malicious skill samples
│   ├── benign/               # 8 benign skill samples
│   ├── adversarial/          # 6 adversarial edge cases
│   └── real_clawhub/         # 23 real ClawHub skills with ground truth
└── LICENSE                   # Apache 2.0
```

`scan.py` is fully self-contained (~1400 lines). No pip install, no venv, no node_modules. Copy it anywhere and run it.

## License

Apache 2.0. See [LICENSE](LICENSE).
