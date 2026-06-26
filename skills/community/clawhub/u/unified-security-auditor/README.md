# Unified Security Skill (OpenCode)

A unified, curated security skill that merges guidance from:
- `raroque/vibe-security-skill` (MIT)
- `BehiSecc/VibeSec-Skill` (Apache-2.0)
- `agamm/claude-code-owasp` (MIT)
- `trailofbits/skills` (CC-BY-SA-4.0)

The combined work is distributed under **CC-BY-SA-4.0** to satisfy ShareAlike requirements.

## What This Skill Does

This skill guides the assistant to:
- Audit codebases for high-impact security issues
- Apply OWASP Top 10 (2025) and ASVS 5.0 concepts
- Avoid insecure defaults and fail-open configurations
- Harden authentication, authorization, and session handling
- Protect secrets and reduce data exposure
- Detect unsafe AI/agent workflows in CI/CD
- Provide concrete fixes and prioritize by severity

It works both:
- **During coding** (secure-by-default patterns)
- **During audits** (structured scan + report format)

## How to Use (Prompt Examples)

Use explicit prompts to activate the skill:
- "Use the unified-security skill to review this repo for auth and secrets issues."
- "Implement this login flow using unified-security best practices."
- "Audit GitHub Actions workflows for AI agent prompt injection risks (unified-security)."

## Installation

### OpenClaw
Workspace-local (recommended for a single project/agent):
```bash
mkdir -p ./skills
cp -R ./unified-security ./skills/
```

Global (available to all OpenClaw workspaces):
```bash
mkdir -p ~/.openclaw/skills
cp -R ./unified-security ~/.openclaw/skills/
```

### OpenCode
Project-local:
```bash
mkdir -p .opencode/skills
cp -R ./unified-security .opencode/skills/
```

Global:
```bash
mkdir -p ~/.opencode/skills
cp -R ./unified-security ~/.opencode/skills/
```

### Claude Code
Project-local:
```bash
mkdir -p .claude/skills
cp -R ./unified-security .claude/skills/
```

Global:
```bash
mkdir -p ~/.claude/skills
cp -R ./unified-security ~/.claude/skills/
```

### OpenAI Codex
Project-local:
```bash
mkdir -p .codex/skills
cp -R ./unified-security .codex/skills/
```

Global:
```bash
mkdir -p ~/.codex/skills
cp -R ./unified-security ~/.codex/skills/
```

## Files

- `unified-security/SKILL.md` — the skill content
- `LICENSE` — CC-BY-SA-4.0
- `NOTICE.md` — attribution
- `THIRD_PARTY_LICENSES.md` — upstream license texts

## License

This unified skill is licensed under **CC-BY-SA-4.0**. See `LICENSE`.
