# Dependency Detection Patterns

## Python

### Scan rules
- `import xxx` → extract `xxx` (top-level module name)
- `from xxx import yyy` → extract `xxx` (top-level module name)
- Relative imports (`from .xxx import`) → only check the package is co-located

### Stdlib exclusion
`check_deps.py` maintains a stdlib exclusion list (from `sys.stdlib_module_names`)
to avoid false-positive "missing dependency" reports for built-in modules.

### Pip package name mapping
Some Python packages have different `import` names from their pip names:

| import name | pip install name |
|-----------|------------------|
| `yaml` | `pyyaml` |
| `cv2` | `opencv-python` |
| `PIL` | `Pillow` |
| `bs4` | `beautifulsoup4` |
| `dotenv` | `python-dotenv` |
| `sklearn` | `scikit-learn` |

Full mapping in `PIP_INSTALL_MAP` inside `check_deps.py`.

## Node.js / TypeScript

### Scan rules
- `require('pkg')` → extract `pkg`
- `import xxx from 'pkg'` → extract `pkg`
- Scoped packages `@org/pkg` → extract full `@org/pkg`
- Built-in modules (`fs`, `path`, `os`, ...) → ignored

### Installation probe
Searches these locations (first-found wins):
1. `<skill-dir>/scripts/node_modules/<pkg>`
2. `~/.openclaw/workspace/node_modules/<pkg>` (legacy)
3. Global `node_modules` discoverable via `node -e`

## Shell / Bash

### Scan rules
Detects external commands used via:
- `command -v <bin>` — explicit detection
- `which <bin>` — explicit detection
- Direct invocation of known tool names (`jq`, `curl`, `gh`, etc.)

### Install hints
Common installation methods in `check_deps.py`'s `_bin_install_hint()`.

## SKILL.md Declaration Format (recommended)

Declare deps in frontmatter's `metadata` block (documentary, does not affect runtime):

```yaml
---
name: my-skill
description: ...
metadata:
  requires:
    python: [requests, pyyaml]
    bins: [jq, curl]
---
```

Or add a `## Dependencies` section in the body:

```markdown
## Dependencies

Auto-installed on first use:

\`\`\`bash
pip install requests pyyaml
\`\`\`

System commands (install manually):
- `jq`: `brew install jq` / `apt-get install jq`
- `curl`: usually pre-installed
```
