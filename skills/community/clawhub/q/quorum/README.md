<p align="center">
  <img src="/branding/github/dark_qu_gh.jpg" alt="Quorum" width="900">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ba4c8.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/platform-OpenClaw-2ba4c8" alt="Platform: OpenClaw">
  <img src="https://img.shields.io/badge/status-v0.7.2-2ba4c8" alt="Status: v0.7.2">
  <a href="https://clawhub.ai/dacervera/quorum"><img src="https://img.shields.io/badge/ClawHub-dacervera%2Fquorum-2ba4c8" alt="Available on ClawHub"></a>
</p>

---

## Hey. I'm Quorum. 🦞

You built something with your AI agent. A research report. A config. A codebase. Maybe a whole swarm produced it — five agents researching, synthesizing, writing — and now you're staring at the output wondering:

*"How do I know this is actually right?"*

You could read every line yourself — but that defeats the point of having agents. You could ask the swarm to review its own work — but you already know that's just grading your own exam.

**That's where I come in.**

I bring in independent critics — each one focused on a different dimension — and they go through your work carefully. Not vibes. Not "looks good to me." Every finding has to cite specific evidence from your artifact. If a critic can't show me the proof, I throw out the finding.

```
$ quorum run --target my-report.md --depth standard

Running Quorum (standard depth, critics: correctness, completeness, security) ...

 ◆ QUORUM VERDICT: PASS_WITH_NOTES
 ──────────────────────────────────
   Issues: 0 HIGH · 2 MEDIUM · 1 LOW/INFO  (3 total)

   1. [MEDIUM] §2.4 claims "all implementations use AES-256" but §5.2
      references a ChaCha20 fallback — contradictory coverage claim
   2. [MEDIUM] Rubric criterion RC-007 (threat model) has no matching
      content in any section
   3. [INFO]   Minor: bibliography entry [14] not cited in text

   Cost: $0.42 (12,840 prompt + 3,201 completion tokens)
```

Now you know. Not because you hoped. Because it was checked.

---

## What Makes Me Different

| The usual approach | What I do instead |
|---|---|
| One model reviews its own output | **Separate critics** that never saw the original prompt |
| "Looks great!" — it wrote it, of course it thinks so | Critics come in cold. **No bias from creation** |
| Vague suggestions you can't act on | **Every finding cites evidence** — excerpts, line numbers, schema checks |
| Same effort for a draft vs. production | **Three depth levels**: quick ($0.15), standard ($0.50), thorough ($1.50+) |
| Reviews one file at a time | **Batch + cross-artifact** — validate a directory with consistency checks between files |
| LLM wastes tokens on obvious problems | **Multi-layer pre-screen** catches issues first — 10 deterministic checks + DevSkim + Ruff + Bandit before LLM critics run |
| Each review starts from zero | **Learning memory** — recurring patterns auto-promote to mandatory checks |

You wouldn't ship code without tests. I'm here so you don't ship AI outputs without validation either.

---

## The Deeper Question

Validation is the beginning. The question that matters in compliance, audits, and anything with stakes is **substantiation**: *Can you prove the output meets a specific standard?*

That's what rubrics are for. A rubric encodes a standard — OWASP ASVS, SOC 2 controls, your internal style guide — as testable, machine-readable criteria. I evaluate evidence against those criteria. You get findings with citations, not feelings.

I ship with three rubrics (research-synthesis, agent-config, python-code). Need one for your domain? → [Rubric Building Guide](docs/guides/RUBRIC_BUILDING_GUIDE.md)

---

## Install

**PyPI** (recommended):
```bash
pip install quorum-validator
quorum run --target your-file.py --depth standard
```

**From source:**
```bash
git clone https://github.com/SharedIntellect/quorum.git
cd quorum/reference-implementation
pip install -e .
```

**OpenClaw / ClawHub:**
```bash
openclaw skills add dacervera/quorum
```

### Platform Ports

Quorum also runs natively inside other agent platforms — no API key required:

| Port | What it does | Install |
|------|-------------|---------|
| **[Copilot CLI](ports/copilot-cli/)** | Full validation as a GitHub Copilot skill — stdlib-only pre-screen + 5 LLM critics | Copy `ports/copilot-cli/` to `~/.copilot/skills/quorum/` |
| **[Claude Code](ports/claude-code/)** | Quorum validation via Claude Code subscription tokens | Copy `ports/claude-code/` to your project |

### Configuration

You'll need a model that can reason well. I auto-detect your provider on first run.

| Tier | Models | Best for |
|------|--------|----------|
| **Recommended** | Claude Opus, GPT-5+ | Thorough depth, cross-artifact consistency |
| **Great** | Claude Sonnet, Gemini 2.0+ | Quick and standard — where most work lives |
| **Functional** | Claude Haiku, GPT-4o | Lighter validation, less nuance on edge cases |

Details: [Model Requirements](docs/getting-started/MODEL_REQUIREMENTS.md) · [Config Reference](docs/configuration/CONFIG_REFERENCE.md)

---

## Documentation

| Getting Started | Guides | Architecture |
|---|---|---|
| [Installation](docs/getting-started/INSTALLATION.md) | [Rubric Building Guide](docs/guides/RUBRIC_BUILDING_GUIDE.md) | [Full Specification](SPEC.md) |
| [Quick Start](docs/getting-started/QUICK_START.md) | [Cross-Artifact Design](docs/guides/CROSS_ARTIFACT_DESIGN.md) | [The Nine Critics](docs/architecture/THE_NINE.md) |
| [For Beginners](docs/getting-started/FOR_BEGINNERS.md) | [Security Critic Framework](docs/critics/SECURITY_CRITIC_FRAMEWORK.md) | [Implementation Notes](docs/architecture/IMPLEMENTATION.md) |
| [Model Requirements](docs/getting-started/MODEL_REQUIREMENTS.md) | [Code Hygiene Framework](docs/critics/CODE_HYGIENE_FRAMEWORK.md) | [Changelog](docs/CHANGELOG.md) |
| [Config Reference](docs/configuration/CONFIG_REFERENCE.md) | [Contributing](CONTRIBUTING.md) | [External Reviews](docs/reviews/EXTERNAL_REVIEWS.md) |

New to AI agent tooling? → [FOR_BEGINNERS.md](docs/getting-started/FOR_BEGINNERS.md) — I'll start from the very beginning.

Full documentation index: [docs/](docs/README.md)

---

<p align="center">
  MIT License · <a href="https://sharedintellect.com">SharedIntellect</a> · 2026
</p>
