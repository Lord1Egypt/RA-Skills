# axiom-rebrand

> Generic rebrand pipeline. Deterministic, idempotent, byte-to-byte. Strip jargon, fix paths, regenerate manifests, validate — one CLI call.

You have a project with internal references that don't belong in public (author names, codenames, hardcoded paths, "first draft" markers). Strip them all in one command. Re-run any time — same output, byte-for-byte.

## Features

- **Generic** — works on any project, not just one specific codebase
- **Configurable jargon** — extend patterns via YAML/JSON (only 1 optional dep: PyYAML)
- **Idempotent byte-to-byte** — same input → same SHA-256, every run
- **sys.path auto-fix** — `/run/...` → `Path(__file__).parent`
- **Excludes** — `.auto.md`, `.pyc`, `__pycache__`, `.swp`, `.bak`, etc.
- **MANIFEST regeneration** — SHA-256 of every file, top-level
- **Optional validation** — runs tests + custom validator post-rebrand
- **Audit JSON** — full per-file diff stats
- **Free tier** — 100 rebrand/months free, then $0.005/use
- Pure Python stdlib + 1 optional dep (PyYAML, only for YAML config)

## Installation

```bash
pip install axiom-rebrand
```

## Usage

### CLI

```bash
# Basic rebrand
axiom-rebrand --src <SRC> --dst <DST>

# With a project name
axiom-rebrand --src <SRC> --dst <DST> --name my-project

# Dry-run (preview without writing)
axiom-rebrand --src <SRC> --dst <DST> --dry-run

# Custom jargon config (YAML or JSON)
axiom-rebrand --src <SRC> --dst <DST> --config jargon.yaml

# With validator
axiom-rebrand --src <SRC> --dst <DST> --validator <VALIDATOR>

# JSON report
axiom-rebrand --src <SRC> --dst <DST> --json > audit.json
```

### Python API

```python
from axiom_rebrand import rebrand_project, rebrand_file, strip_jargon

# Whole project
report = rebrand_project(
    src_root=Path("<SRC>"),
    dst_root=Path("<DST>"),
    project_name="my-project",
    validator=Path("<VALIDATOR>"),
)
# {
#   "project": "my-project",
#   "files_count": 79,
#   "manifest_hash": "abc123...",
#   "tests_ok": True,
#   "valid_ok": True,
#   ...
# }

# Single file
audit = rebrand_file(src, dst)
# {
#   "file": "README.md",
#   "jargon_lines_stripped": 3,
#   "sys_path_fixed": 0,
#   ...
# }

# Just strip jargon (no file copy)
cleaned, n = strip_jargon("Author: 🐺 Alice (Internal Team)")
# ("", 1)
```

## Config format (jargon.yaml)

```yaml
jargon:
  - pattern: '🐺\s*\w+'
    replacement: "Axioma team"
  - pattern: '\(Internal Team\)'
    replacement: ""
  - pattern: '^# Internal Note:.*$'
    replacement: ""
```

Or JSON:
```json
{
  "jargon": [
    {"pattern": "🐺\\s*\\w+", "replacement": "Axioma team"},
    "Internal"
  ]
}
```

## What it strips by default

**Generic patterns** (safe for any project):

| Pattern | Replaced with |
|---------|---------------|
| `# Auteur: ...` | *(removed)* |
| `# Author: ...` | *(removed)* |
| `**Author: ...**` (bold inline) | *(removed)* |
| `# Lead: ...` | *(removed)* |
| `Created by: ...` lines | *(removed)* |
| `Validated by: ...` lines | *(removed)* |
| `(premier jet)` | *(removed)* |
| `(PREMIER JET)` | *(removed)* |
| `first draft` | `first version` |
| `Path:<SRC>/path` | *(removed)* |
| `sys.path.insert(0, "/run/...")` | `sys.path.insert(0, str(Path(__file__).parent))` |

**Cluster/org patterns are NOT in defaults** — load them via config:

```bash
axiom-rebrand --src <SRC> --dst <DST> \
  --config examples/cluster-jargon.yaml
```

See `examples/cluster-jargon.yaml` for the Axioma Stellaris-specific patterns (cluster codenames, agent emojis, etc.).

## Excluded files (by default)

`.auto.md`, `.pyc`, `__pycache__/`, `.swp`, `.bak`, `.orig`, `.DS_Store`, `ORCHESTRATION.md`, `MANIFEST.txt`

## Use cases

- **Open-sourcing** an internal tool with private codenames
- **Marketplace publication** (Capafy, GitHub Marketplace, etc.)
- **Multi-tenant** projects — strip org-specific references
- **CI/CD gates** — block PRs that leak internal jargon
- **Code review** — enforce "no internal names" via process

## Idempotence proof

```bash
$ axiom-rebrand --src <SRC> --dst <DST>
✅ Files processed: 79
✅ Files modified: 78
✅ Jargon lines stripped: 257
✅ Validation + tests OK
📦 MANIFEST SHA-256: d0efae4bf8...

$ axiom-rebrand --src <SRC> --dst <DST>
✅ Files processed: 79
✅ Files modified: 78
✅ Jargon lines stripped: 257
✅ Validation + tests OK
📦 MANIFEST SHA-256: d0efae4bf8...
# Same hash. Byte-to-byte identical.
```

## Pricing

**Free tier:** 100 rebrand/months free
**Then:** $0.005 per use

Cost comparison:
- Manual sed/regex: hours of work, no audit, easy to miss cases
- LLM-based "code refactor": $0.10+/use, non-deterministic, hallucinates
- This tool: $0.005/use (after free tier), deterministic, audit JSON included

The free tier removes the friction barrier for the "one-off rebrand" case. After that, the cost is still negligible compared to the hours saved.

## Comparison

| Tool | Deterministic | Byte-to-byte | Auditable | Configurable |
|------|:-:|:-:|:-:|:-:|
| `sed -i` | ❌ | ❌ | ❌ | ❌ |
| LLM refactor | ❌ | ❌ | ❌ | ✅ |
| Manual rebrand | ❌ | ❌ | ❌ | ❌ |
| **axiom-rebrand** | ✅ | ✅ | ✅ | ✅ |

## License

Apache 2.0 — free to use, modify, distribute.

## Authors

Axioma Tools — open-source utility suite for content pipelines.
