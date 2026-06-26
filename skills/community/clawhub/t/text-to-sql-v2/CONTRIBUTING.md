# Contributing to `User Describes Data`

Thank you for your interest in contributing! Please follow these steps to set up your development environment and submit changes.

## Development Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/<your-username>/User Describes Data.git
cd User Describes Data

# 3. Install dependencies (if any)
pip install -r scripts/requirements.txt

# 4. Run the self-audit to verify quality
python scripts/audit_skill.py .
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
python scripts/audit_skill.py .

# 4. Commit your changes
git add .
git commit -m "feat(text-to-sql): add <brief description>"

# 5. Push to your fork
git push origin feat/<your-feature-name>

# 6. Open a Pull Request on GitHub
#    - Title: feat(text-to-sql): add <brief description>
#    - Description: What + Why + Testing
```

## Code Standards

- **SKILL.md**: Follow the YAML frontmatter standard (name, description, license, metadata)
- **Scripts**: Must include shebang, requirements.txt, and graceful error handling
- **Language**: SKILL.md body must be in English; reference docs in English
- **No secrets**: Never commit API keys, tokens, or credentials

## Quality Checklist

Before opening a PR, verify:

- [ ] `audit_skill.py` exits with code 0 or 2
- [ ] `validate_skills.py` exits with code 0
- [ ] README.md and README_zh.md are both present
- [ ] CONTRIBUTING.md is present
- [ ] .gitignore is present
- [ ] No hardcoded secrets anywhere in the codebase

## Reporting Issues

Please report issues via GitHub Issues with:

1. **What you expected to happen**
2. **What actually happened**
3. **Steps to reproduce**
4. **Environment** (OS, Python version, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.