# requirements-checker — Status

**Status:** Ready
**Price:** $49
**Created:** 2026-04-09

## Features

- Validate requirements.txt against PEP 508 format rules
- Detect invalid version operators and unparseable specifiers
- Flag duplicate packages (case-insensitive, PEP 503 normalised names)
- Detect editable installs, VCS dependencies, nested `-r` includes
- Detect custom index URLs and URL-only dependencies
- Lint for unpinned dependencies (no version specifier)
- Lint for `>=` without an upper bound (unbounded ranges)
- Lint for non-alphabetical package ordering
- Detect mixed pinning strategies (`==` vs `>=` in same file)
- Sort requirements alphabetically (stdout or in-place `--write`)
- Compare two requirements files — added, removed, changed with version diffs
- Three output formats: `text` (human), `json` (automation/CI), `markdown` (PR comments)
- `--strict` mode exits 1 on any issue for CI pipelines
- `--ignore RULE` to suppress specific rules per project
- Zero external dependencies — pure Python 3 stdlib
