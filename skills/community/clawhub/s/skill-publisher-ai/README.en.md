# Skill Publisher · One-Click Skill Publishing & Iteration Tool

🇨🇳 中文版: [README.md](README.md)

[![Stars](https://img.shields.io/github/stars/EdwardWason/skill-publisher?style=flat-square)](https://github.com/EdwardWason/skill-publisher)
[![License](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-skill--publisher-orange?style=flat-square)](https://clawhub.ai/skills/skill-publisher)
[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue?style=flat-square)](SKILL.md)

[Get started](#30-second-start) · [Core mechanism](#core-mechanism) · [Limitations](#limitations) · [License](#license)

---

_"Say 'publish' — from local Skill to GitHub + ClawHub, fully deployed."_

---

**Skill Publisher** is not a git push cheat sheet — it's a full-pipeline automation tool from Skill completion to online publishing. It supports both **new publishing** and **iteration updates** with complete coverage: repo structure generation, security audit, change detection, auto version bump, CHANGELOG generation, push fallback, Release creation, and ClawHub publishing.

---

## Features

- 🏗 **Dual workflows**: New publish (Workflow A) + Iteration update (Workflow B), auto-detected
- 📐 **Product landing page README**: 21-chapter standard, auto-extracted from SKILL.md
- 🌍 **Bilingual independent files**: Chinese `README.md` + English `README.en.md`, cross-linked
- 🔒 **Three-layer security scan**: Credentials + local paths + dangerous commands, any FAIL blocks publish
- 📊 **Change detection + auto version bump**: File category mapping, MAJOR/MINOR/PATCH decision tree
- 📝 **Auto CHANGELOG generation**: From git log, Conventional Commits classified, empty categories omitted
- 🔄 **Push fallback chain**: git push → gh CLI → REST API, publish even with unstable networks
- 📋 **Community templates**: bug_report / feature_request / question / config / pull_request_template
- 🏷 **Provenance**: SKILL.md provenance block for skill source traceability

## When to Use / When Not To

✅ **Use when**
- One-click publish after Skill development to GitHub + ClawHub
- Iterating an existing Skill (auto-detect changes, bump version, generate CHANGELOG)
- Standardizing repo structure (README, community templates, provenance)
- Security audit to prevent credential leaks

❌ **Don't use when**
- Creating Skill content (use the Skill itself)
- Publishing non-Skill projects
- Code development

## 30-Second Start

```bash
# ClawHub install (recommended)
clawhub install skill-publisher

# Or manual install
git clone https://github.com/EdwardWason/skill-publisher.git
```

After installation, tell your Agent:

```
Publish wx-peitu to GitHub and ClawHub
```

```
Update react-design-draft
```

```
Iterate skill-publisher
```

## Common Use Cases

| Scenario | Workflow | Trigger |
|----------|----------|---------|
| New Skill completed, first publish | Workflow A | "publish"/"new" |
| Existing Skill added new features | Workflow B | "update"/"iterate" |
| Fixed a Skill bug | Workflow B | "update skill, fixed a bug" |
| Rewrote Skill design system | Workflow B | "iterate skill, breaking change" |

## Core Mechanism

### Dual Workflow Auto-Detection

```
User says "publish"/"new"?
  → Workflow A: Repo structure → Security audit → Push → Publish

User says "update"/"iterate"/"bump"?
  → Workflow B: Change detection → Version bump → CHANGELOG → Security audit → Push → Publish
```

### Workflow A: New Publish (13 steps)

```
Generate structure → Generate README (CN/EN) → Generate auxiliary files → Add provenance → Confirm info
→ Security scan → Distribution judgment → Slug check → Push → Create Release → ClawHub publish → Verify
```

### Workflow B: Iteration Update (12 steps)

```
Detect changes → Categorize files → Recommend bump → Confirm version → Three-file sync
→ Extract git log → Parse commits → Generate CHANGELOG → Security audit
→ Push → Create/update Release → ClawHub update → Verify
```

### Change Detection → Version Bump Decision Tree

| Change Type | Version Impact | Example |
|------------|---------------|---------|
| SKILL.md frontmatter change | MAJOR | Changed name/description |
| Added/removed rules | MINOR | Added 2 rules |
| New references file | MINOR | Added workflow.md |
| References content rewrite | MINOR | design-system.md major update |
| README docs update | PATCH | Added FAQ section |
| Community template addition | PATCH | Added config.yml |

### Push Fallback Chain

```
git push (preferred, fastest)
  → fails → gh CLI (fallback, auto-auth)
  → fails → REST API file-by-file upload (last resort)
```

### README Product Landing Page 21-Chapter Standard

Smart adaptation by Skill complexity: simple Skills (≤5 rules) generate only required chapters, complex Skills generate all 21.

## Directory Structure

```
skill-publisher/
├── SKILL.md                              # Dual workflow (25 steps + 15 rules)
├── README.md                             # Chinese docs
├── README.en.md                          # English docs
├── CHANGELOG.md                          # Version history
├── LICENSE                               # MIT-0
├── .claude-plugin/
│   └── plugin.json                       # Claude Code metadata
├── .github/                              # Community templates
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   ├── question.yml
│   │   └── config.yml
│   └── pull_request_template.md
└── references/                           # Reference docs
    ├── repo-structure.md                 # Repo templates + README 21 chapters + smart adaptation
    ├── security-audit.md                 # Three-layer scan + distribution judgment + remediation
    ├── publish-procedures.md             # Push fallback + gh CLI + Release + ClawHub
    ├── change-detection.md               # Change detection + version bump + Conventional Commits
    └── changelog-generation.md           # git log extraction + CHANGELOG generation + Release Notes
```

## Limitations

- **Skill projects only**: No support for non-Skill projects (no package.json management, no CI/CD config)
- **Windows-first**: PowerShell compatibility prioritized; macOS/Linux some commands need adaptation
- **git push timeout common**: 443 timeouts frequent in China; fallback chain is a core capability
- **No GUI**: Fully dependent on Agent platforms (TRAE / Claude Code / Codex)
- **ClawHub slug immutable**: Once published, slug cannot be changed; only new versions

## Core Design Principles

1. **Security first**: Any FAIL blocks publish — better to over-scan than leak a credential
2. **Fallback first**: Network instability is the norm; three-level fallback ensures you can always publish
3. **Automated but not blind**: Version bump requires user confirmation; CHANGELOG auto-generated but editable
4. **Product thinking**: README is a landing page, not a spec sheet — making people want to use it > making them understand it
5. **Dogfooding**: skill-publisher publishes itself using its own workflow

## FAQ

**Does it support updating existing repos?**
Yes. Say "update xxx" to trigger Workflow B — auto-detect changes, recommend version bump, generate CHANGELOG.

**What if git push times out?**
Auto-fallback: try gh CLI first (auto-auth), then REST API file-by-file upload.

**How is the version number decided?**
Auto-recommended by changed file categories: SKILL.md rule changes → MINOR, README docs → PATCH, frontmatter breaking → MAJOR. User confirmation required after recommendation.

**What if the README is too long?**
Smart adaptation: simple Skills generate only 10 required chapters, complex Skills generate all 21.

**Are Conventional Commits mandatory?**
No. If commit messages don't follow the convention, file diff analysis infers change categories.

---

## License

MIT-0 © 2026