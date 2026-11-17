<div align="center">

# 🛡️ SkillGate

**Trust infrastructure for AI agent skills.**

Open-source security scanner + capability evaluator + continuous monitoring for the agent ecosystem.

<p align="center">
  <strong>Language:</strong>
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  <a href="https://www.star-history.com/zhaoxinghua09-cell/skillgate">
    <img src="https://api.star-history.com/badge?repo=zhaoxinghua09-cell/skillgate&type=trending" alt="Star History" height="20" />
  </a>
</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/github/v/release/zhaoxinghua09-cell/skillgate)](https://github.com/zhaoxinghua09-cell/skillgate/releases)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Offline Ready](https://img.shields.io/badge/offline--ready-✅-2ea44f)](#-)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-✅-2ea44f)](#-)
[![Cross Platform](https://img.shields.io/badge/cross--platform-Windows%20%7C%20Mac%20%7C%20Linux-2ea44f)](#-)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-✅-d97757)](https://www.anthropic.com/claude-code)
[![Cursor](https://img.shields.io/badge/Cursor-✅-000000)](https://www.cursor.com/)
[![Codex](https://img.shields.io/badge/Codex-✅-412991)](https://openai.com/index/codex/)
[![Gemini](https://img.shields.io/badge/Gemini-✅-4285F4)](https://gemini.google.com/)
[![GitHub Copilot](https://img.shields.io/badge/Copilot-✅-24292e)](https://github.com/features/copilot)
[![OpenCode](https://img.shields.io/badge/OpenCode-✅-6366f1)](https://opencode.ai/)
[![CI](https://github.com/zhaoxinghua09-cell/skillgate/actions/workflows/ci.yml/badge.svg)](https://github.com/zhaoxinghua09-cell/skillgate/actions/workflows/ci.yml)
[![CodeQL](https://github.com/zhaoxinghua09-cell/skillgate/actions/workflows/codeql.yml/badge.svg)](https://github.com/zhaoxinghua09-cell/skillgate/actions/workflows/codeql.yml)
[![Codecov](https://codecov.io/gh/zhaoxinghua09-cell/skillgate/branch/main/graph/badge.svg)](https://codecov.io/gh/zhaoxinghua09-cell/skillgate)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://zhaoxinghua09-cell.github.io/skillgate/)
[![Sponsor](https://img.shields.io/badge/sponsor-%E2%9D%A4-red)](.github/FUNDING.yml)
[![Stars](https://img.shields.io/github/stars/zhaoxinghua09-cell/skillgate?style=social)](https://github.com/zhaoxinghua09-cell/skillgate/stargazers)
[![Forks](https://img.shields.io/github/forks/zhaoxinghua09-cell/skillgate?style=social)](https://github.com/zhaoxinghua09-cell/skillgate/network/members)
[![Views](https://hits.dwyl.com/zhaoxinghua09-cell/skillgate.svg)](https://hits.dwyl.com/zhaoxinghua09-cell/skillgate)
[![Last Commit](https://img.shields.io/github/last-commit/zhaoxinghua09-cell/skillgate)](https://github.com/zhaoxinghua09-cell/skillgate/commits/main)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Open Source Love](https://img.shields.io/badge/open%20source-%E2%9D%A4-pink.svg)](https://github.com/zhaoxinghua09-cell/skillgate)

[Features](#-features) · [Quick Start](#-quick-start) · [Documentation](docs/) · [Rule Writing](docs/rules.md) · [Contributing](CONTRIBUTING.md)

</div>

---

## 🤔 Why I built this

I love AI agent skills. They make Claude Code, Cursor, and Codex so much more powerful.

But there's a problem: **when you install a random skill from the internet, do you actually know what it does?**

Does it read your files? Send your data to a server? Have a hardcoded API key? Run `eval()` on your input?

I tried using Snyk and CodeQL for this, but they're built for regular code — not for skills. Skills have their own patterns: SKILL.md files, scripts that run with your agent's permissions, instructions that tell the agent to do things.

So I built SkillGate. It's a security scanner built **specifically for AI agent skills**. It tells you, in one number: *can I trust this skill?*

This is just the beginning. As the agent ecosystem grows, we're going to need infrastructure like this — the same way we needed npm audit, Snyk, and Dependabot for regular packages.

---

## 📖 What is SkillGate?

SkillGate is the **first end-to-end trust infrastructure for AI agent skills**. It combines:

| Layer | What it does |
|-------|-------------|
| 🔒 **Gate 1: Security Scan** | 176 detection patterns × 22 categories, multi-language static analysis (Python/Shell/JS/TS/PS1/Batch/Ruby/PHP/Perl/Go/Rust/VBS/Lua/Markdown/YAML/TOML/JSON/TXT/XML/HTML/CSV/ENV), fully offline |
| 🧪 **Gate 2: Capability Bench** | Dry-run test-plan preview, baseline comparison (no code execution) |
| 📊 **Continuous Monitoring** | Weekly regression scans, score drop alerts, trend tracking |
| 🏆 **Trust Score** | Single number that answers: *can I trust this skill?* |

It's like **Snyk for AI agent skills** — but open source, local-first, and community-driven.

---

## 🧠 LGD Trust Framework

SkillGate is built on the **LGD Trust Framework** (有籍 / 有证 / 有门禁):

| Principle | Meaning | How SkillGate implements it |
|-----------|---------|------------------------------|
| **📇 Registered** (有籍) | Every skill has a traceable identity | Author, version, license, rule version tracking |
| **📜 Evidenced** (有证) | Every finding has proof & explanation | Rule IDs, explanations, fix suggestions |
| **🚪 Guarded** (有门禁) | Every gate is checked automatically | CI integration, pre-commit hooks, fail-under threshold |

**Result**: a Trust Score you can actually trust — not just a random number.

---

## ✨ Features

### 🔍 Deep Scanning
- **176 detection patterns** across 22 categories (secrets, dangerous code, injection, dependencies, …)
- **Multi-language static analysis**: Python, Shell, JavaScript/TypeScript, PowerShell, Batch, Ruby, PHP, Perl, Go, Rust, VBS, Lua, Markdown, YAML, TOML, TXT
- **Local-only**: fully offline, no network requests, no code execution

### 🎯 Trust Score
- Weighted scoring: CRITICAL = -15, HIGH = -8, MEDIUM = -3, LOW = -1
- Grade scale: A+ (90+) · A (80+) · B (70+) · C (60+) · D (< 60)
- Badge SVG generation for your README

### 🔌 Universal Integration
- **CLI**: `skillgate scan ./my-skill/`
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI, Bitbucket Pipelines
- **Pre-commit**: automatic scan on every commit
- **MCP Server**: expose as tool for other AI agents
- **VSCode extension**: inline diagnostics
- **GitHub App**: automatic PR comments with Trust Score

### 🤖 AI-Friendly
- `--format agent` output: optimized for LLM consumption
- `llms.txt`: AI-readable tool documentation
- MCP-compatible: other agents can call SkillGate as a tool

---

## 🚀 Quick Start

### Install as an Agent Skill (recommended)

Install directly from the GitHub repository — works with Claude Code, Cursor, Codex, and any agent that supports the skills standard:

```bash
git clone https://github.com/zhaoxinghua09-cell/skillgate.git
# then symlink or copy the skillgate folder into your agent's skills directory
```

Then just ask your agent: *"check if this skill is safe"* — it will use SkillGate automatically.

### Install as a CLI tool

```bash
# Clone the repo
git clone https://github.com/zhaoxinghua09-cell/skillgate.git
cd skillgate

# Install (no dependencies needed!)
pip install -e .
```

### Scan your first skill

```bash
python skillgate.py scan ./my-skill/
```

**Output:**
```
🛡️  SkillGate Security Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Skill: my-skill
Trust Score: 93/100
Grade: A

📊 Findings:
  ✅ 0 CRITICAL
  ✅ 0 HIGH
  ⚠️  2 MEDIUM
  ℹ️  5 LOW

📁 Files scanned: 12
⏱️  Time: 0.3s
```

### CI Integration (GitHub Actions)

```yaml
# .github/workflows/skillgate.yml
name: SkillGate
on: [pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: your-org/skillgate-action@v1
        with:
          fail-under: 80
```

---

## 📊 Example Outputs

| Format | Command | Use case |
|--------|---------|----------|
| Terminal | `skillgate scan .` | Local development |
| JSON | `--format json` | Programmatic parsing |
| SARIF | `--format sarif` | GitHub code scanning |
| JUnit | `--format junit` | CI test reporting |
| HTML | `--format html` | Beautiful reports |
| Agent | `--format agent` | AI-friendly summary |
| Badge | `--badge` | README SVG badge |

---

## 🏆 Trust Score Badge

Add your skill's Trust Score badge to your README:

```markdown
[![SkillGate Trust Score](https://img.shields.io/badge/SkillGate-A%20(93/100)-brightgreen)](https://github.com/zhaoxinghua09-cell/skillgate)
```

It looks like this:

[![SkillGate Trust Score](https://img.shields.io/badge/SkillGate-A%20(93/100)-brightgreen)](https://github.com/zhaoxinghua09-cell/skillgate)

---

## 🧪 Skill Bench

Preview the dry-run test plan for a skill (no code execution, read-only):

```bash
python skillbench.py run ./my-skill/ --output plan.json
```

Compares your skill against a baseline to show:
- ✅ Does it work correctly?
- 📈 How accurate is it?
- 🚀 How fast is it?

---

## 🔧 Writing Custom Rules

Create your own rules in YAML:

```yaml
# .skillgate/rules/my-rules.yml
rules:
  - id: my-custom-rule
    description: "Detected dangerous pattern"
    severity: HIGH
    languages: [python]
    patterns:
      - "eval\\("  # skillgate: ignore: rule-pattern example (self-scan)
    fix: "Use ast.literal_eval() instead"
```

See [docs/rules.md](docs/rules.md) for the full rule writing guide.

---

## 📁 Project Structure

```
skillgate/
├── skillgate.py          # Main CLI (static scanner + gate)
├── ast_analyzer.py       # Python AST analysis
├── rule_engine.py        # Custom YAML rules
├── badge_generator.py    # SVG trust-score badges
├── dependency_manager.py # Dependency handling
├── scorecard.py          # Scorecard helpers
├── skillbench.py         # Benchmark plan preview (dry-run, no execution)
├── skillwatch.py         # Read-only monitoring (in-process scan; optional --history)
├── skillgate-mcp.py      # MCP server (in-process, no subprocess)
├── skills/               # 17 companion skills (12 compliance + 2 quality + 3 workflow)
├── llms.txt              # LLM-friendly index
├── skill-card.md         # ClawHub skill card
├── CHANGELOG.md
├── LICENSE
├── README.md
└── SKILL.md
```

---

## 📊 Comparison with other tools

| Feature | SkillGate | Snyk | GitHub CodeQL | Semgrep |
|---------|-----------|------|---------------|---------|
| Local-first / offline | ✅ Yes | ❌ Cloud-only | ❌ Cloud-only | ✅ Yes |
| AI agent skill focused | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Trust Score (single number) | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Benchmark plan preview (dry-run) | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Continuous monitoring (read-only) | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| 15+ languages | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Open source | ✅ MIT | ❌ Proprietary | ✅ MIT | ✅ MIT |
| Free for commercial use | ✅ Yes | ❌ Paid | ✅ Yes | ✅ Yes |

**Why SkillGate?** It focuses on AI agent skills as a distinct software category — purpose-built trust signals (static scan → benchmark plan preview → read-only monitoring → Trust Score) that complement generic code scanners like Snyk and Semgrep.

---

## 📈 Benchmarks

| Test | Time | Notes |
|------|------|-------|
| Scan 10 files (small project) | ~0.1s | Pure Python, no external services |
| Scan 100 files (medium project) | ~0.5s | Fast enough for local development |
| Scan 1000 files (large project) | ~3s | Efficient enough for CI |
| Memory usage | ~50MB | Lightweight, runs anywhere |

**No cloud required. No API keys. No waiting.**

---

## 🏗️ Architecture

```mermaid
graph TD
    A[User / CI] --> B[SkillGate CLI]
    B --> C[Security Scanner]
    B --> D[Capability Bench]
    B --> E[Continuous Monitor]
    C --> F[Trust Score]
    D --> F
    E --> F
    F --> G[Report / Badge / SARIF]
```

Three gates, one score:
1. 🔒 **Security** — 176 detection patterns, multi-language static analysis (no network, no execution)
2. 🧪 **Capability** — does the skill actually work?
3. 📊 **Continuity** — does it stay good over time?

---

## 🗺️ Roadmap

What's next for SkillGate?

- **v1.0.0** — Basic security scanner + Trust Score (released!)
- **v1.1.0** — MCP Server integration — let other agents call SkillGate as a tool
- **v1.2.0** — VSCode extension — inline diagnostics while you write skills
- **v1.3.0** — GitHub App — automatically comment on PRs with Trust Score
- **v1.4.0** — Cloud service — team dashboards, shared policy, continuous monitoring

Want to help build one of these? Check out [CONTRIBUTING.md](CONTRIBUTING.md)!

---

## ❓ FAQ

**Q: Is SkillGate a replacement for Snyk or CodeQL?**
A: No — it's complementary. Snyk and CodeQL scan your code. SkillGate scans your *AI skills* — a new category of software that needs its own trust infrastructure.

**Q: Does it work offline?**
A: Yes! 100% local, no internet required. Perfect for air-gapped environments.

**Q: How is the Trust Score calculated?**
A: Weighted by severity: CRITICAL = -15, HIGH = -8, MEDIUM = -3, LOW = -1. Start at 100, subtract findings. A+ = 90+, A = 80+, etc.

**Q: Can I write my own rules?**
A: Yes! Rules are simple YAML files. See [docs/rules.md](docs/rules.md).

**Q: Is it free?**
A: Yes! MIT license, free for everyone — personal and commercial use.

---

## 📸 Screenshots

| Terminal Output | HTML Report |
|-----------------|-------------|
| ![Terminal Output](https://via.placeholder.com/400x250?text=Terminal+Scan+Output) | ![HTML Report](https://via.placeholder.com/400x250?text=HTML+Report) |

---

## 🆘 Getting Help

Stuck? Here's where to go:

- 💬 **Questions & discussions** — [GitHub Discussions](https://github.com/zhaoxinghua09-cell/skillgate/discussions)
- 🐛 **Found a bug?** — [Open an issue](https://github.com/zhaoxinghua09-cell/skillgate/issues/new?template=bug_report.yml)
- ✨ **Want a new feature?** — [Request a feature](https://github.com/zhaoxinghua09-cell/skillgate/issues/new?template=feature_request.yml)
- 📚 **Documentation** — [GitHub Pages](https://zhaoxinghua09-cell.github.io/skillgate/)
- 🔒 **Report a security issue** — See [SECURITY.md](SECURITY.md)

---

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new rules
- How to add new language support
- Code style guide
- Development setup

---

## 📄 License

[MIT](LICENSE) — free for everyone.

---

## 🙏 Acknowledgements

SkillGate stands on the shoulders of giants:

- Inspired by **Snyk** and **Dependabot** — but built specifically for AI agent skills
- Thanks to **CodeQL** and **Semgrep** for showing what static analysis can do
- Built on the **LGD Trust Framework** (有籍 / 有证 / 有门禁)
- Thanks to the entire open-source AI agent community for building skills, tools, and the ecosystem we all love

---

<div align="center">

**Made with ❤️ for the open source agent ecosystem.**

⭐ Star this repo if you find it useful!

</div>
