---
name: releasenotes
description: Generate release notes from git commit history using Conventional Commits convention. Categorizes commits into Features, Bug Fixes, Performance, Refactoring, Docs, Tests, Build, CI, and more. Use when asked to create a changelog, generate release notes, summarize recent commits, or prepare a version release. Supports date ranges, version labels, and file output. Zero dependencies.
---

# releasenotes 📋

Generate categorized release notes from git log.

## Commands

```bash
# Generate from all commits
python3 scripts/releasenotes.py --path /path/to/repo

# Date range
python3 scripts/releasenotes.py --since 2026-03-01 --until 2026-03-27

# With version label
python3 scripts/releasenotes.py --version v2.0.0 --since v1.0.0

# Output to file
python3 scripts/releasenotes.py -o CHANGELOG.md --version v1.0.0
```

## Categories (Conventional Commits)
- ✨ Features (`feat:`)
- 🐛 Bug Fixes (`fix:`)
- ⚡ Performance (`perf:`)
- ♻️ Refactoring (`refactor:`)
- 📚 Documentation (`docs:`)
- 🧪 Tests (`test:`)
- 📦 Build (`build:`)
- 🔧 CI/CD (`ci:`)
- 💥 Breaking Changes (`feat!:` or `fix!:`)
- 📝 Other (non-conventional commits)

Each entry includes commit hash and author.
