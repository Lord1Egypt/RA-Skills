# Skill Audit Framework 🔍

Structured security and quality audit framework for ClawHub/MCP skills. Teaches your agent how to review skills before you install them.

## Why

- 13.4% of ClawHub skills have critical security issues ([Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/))
- 341 malicious skills found in a single campaign ([ClawHavoc](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting))
- A green checkmark is not enough

## What it does

Not a scanner — a **review methodology**. Your agent walks through 6 audit domains and produces a structured PASS/WARN/FAIL report:

1. **Identity & Provenance** — Who made this? Is there source code?
2. **Permission & Scope** — What does it ask for? Is it proportionate?
3. **Behavior vs Description** — Does it do what it says?
4. **Credential Handling** — How are secrets stored and used?
5. **Persistence & Side Effects** — Does it modify your system?
6. **Dependency & Supply Chain** — Are dependencies trustworthy?

## Install

```
clawhub install enawareness/skill-audit-framework
```

## Usage

```
Audit this skill before I install it: @author/skill-name
```

```
Review the security of [skill URL]
```

## No dependencies

Pure prompt skill. No scripts, no system packages, no API keys required.

## License

MIT
