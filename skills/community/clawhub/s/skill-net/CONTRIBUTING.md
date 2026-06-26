# Contributing to skill-net

Thank you for your interest in contributing! Please follow these steps to set up your development environment and submit changes.

## Development Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/<your-username>/skill-net.git
cd skill-net

# 3. No external dependencies required
#    (analyze_deps.py uses only Python standard library)

# 4. Run the analyzer to verify it works
python3 scripts/analyze_deps.py --lang=EN
```

## Workflow

We use a standard feature branch workflow:

```bash
# 1. Create a new branch from main
git checkout -b feat/<your-feature-name>

# 2. Make your changes
#    - Follow the SKILL.md structure standards
#    - Keep SKILL.md body in English
#    - Do not hardcode API keys or secrets

# 3. Run the audit to check for issues
python scripts/audit_skill.py .   # if you have audit_skill.py available

# 4. Commit your changes
git add .
git commit -m "feat(<skill-id>): add <brief description>"

# 5. Push to your fork
git push origin feat/<your-feature-name>

# 6. Open a Pull Request on GitHub
#    - Title: feat(<skill-id>): add <brief description>
#    - Description: What + Why + Testing
```

## Code Standards

- **SKILL.md**: Follow the YAML frontmatter standard (name, description, license, metadata)
- **Scripts**: Must include shebang, requirements.txt, and graceful error handling
- **Language**: SKILL.md body must be in English; README_zh.md is Chinese translation
- **No secrets**: Never commit API keys, tokens, or credentials
- **Bilingual**: README.md (EN) and README_zh.md (ZH) must be kept in sync

## Quality Checklist

Before opening a PR, verify:

- [ ] `python3 scripts/analyze_deps.py` runs without errors
- [ ] `--lang=ZH` and `--lang=EN` both produce correct output
- [ ] `python3 scripts/analyze_deps.py --json` outputs valid JSON
- [ ] README.md and README_zh.md are both present and consistent
- [ ] CONTRIBUTING.md is present
- [ ] .gitignore is present and excludes `__pycache__/`, `.git/`, `.venv/`
- [ ] No hardcoded secrets anywhere in the codebase

## Key Design Decisions

### Dependency Detection Scope
`skill-net` scans for **three types** of skill references:
1. Named skill mentions — `skill-factory`, `gupiao`
2. Protocol command references — `/review`, `/qa`, `/careful`, `/cso`
3. CLI tool references — `clawhub`, `mmx`, `summarize`

Do not limit detection to only `skill-*` slugs — this severely underestimates real ecosystem relationships.

### Orphan Interpretation
"Orphan" means "has SKILL.md but no `use when` trigger phrase detected."
This is a **design flag, not an error**. Many skills intentionally use `/protocol` activation.
Do not mark orhpans as broken; report them with the protocol-style note.

### Health Score Formula
```
Health = trigger_coverage×30% + metadata_complete×20% + cross_ref×20% + cohesion×30%
```
Do not change this formula without empirical validation against real ecosystem data.

## Reporting Issues

Please report issues via GitHub Issues with:

1. **What you expected to happen**
2. **What actually happened**
3. **Steps to reproduce**
4. **Environment** (OS, Python version, OpenClaw version)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.