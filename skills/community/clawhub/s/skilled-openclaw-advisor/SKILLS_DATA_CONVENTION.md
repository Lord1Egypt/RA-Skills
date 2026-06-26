# Skills Data Directory Convention

## Summary

Skills that need persistent local data (databases, indexes, caches, state files)
**must** store that data in the workspace `skills-data/` directory, **not** inside
the skill folder itself.

```
~/.openclaw/workspace/
├── skills/
│   └── my-skill/          ← skill CODE lives here (publishable)
│       ├── SKILL.md
│       └── scripts/
└── skills-data/
    └── my-skill/          ← skill DATA lives here (local only, gitignored)
        ├── index.db
        ├── state.json
        └── ...
```

---

## Rationale

Skill folders are published to ClawHub and installed across machines. Data files
(databases, indexes, caches) are:

- **Machine-specific** — built from local files, configs, and paths
- **Large** — often MBs; unsuitable for a skill package
- **Ephemeral** — can be rebuilt; should never be version-controlled
- **Private** — may contain indexed content from private docs or configs

Separating code from data keeps skill packages small, portable, and publishable.

---

## Convention

### Directory structure

```
{workspace}/skills-data/{skill-slug}/
```

Where `{workspace}` is the OpenClaw agent workspace root (typically
`~/.openclaw/workspace/` or equivalent per-agent path).

### Script pattern

Skills should resolve the data directory like this:

```python
import os

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
DATA_DIR   = os.path.join(WORKSPACE, "skills-data", "my-skill")
DB_PATH    = os.path.join(DATA_DIR, "index.db")
STATE_PATH = os.path.join(DATA_DIR, "state.json")

os.makedirs(DATA_DIR, exist_ok=True)
```

Or make it configurable via env var for multi-agent setups:

```python
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE",
            os.path.expanduser("~/.openclaw/workspace"))
DATA_DIR  = os.path.join(WORKSPACE, "skills-data", "my-skill")
```

### Gitignore

The `skills-data/` directory should be added to `.gitignore` at the workspace root
and inside each skill repo:

```gitignore
# Runtime data — not part of the skill package
skills-data/
*.db
*.sqlite
state.json
diffs/
versions/
```

### First-run setup

Skills with a data directory must include a setup/build script and document it
clearly in `SKILL.md`:

```markdown
## Setup

Run once after install:
```bash
python3 ~/.openclaw/workspace/skills/my-skill/scripts/build_index.py
```
```

---

## Reference Implementation

**`skilled-openclaw-advisor`** is the reference implementation of this convention:

- GitHub: https://clawhub.ai/seanford/skilled-openclaw-advisor
- ClawHub: https://clawhub.com/seanford/skilled-openclaw-advisor
- Data dir: `skills-data/skilled-openclaw-advisor/`
- Scripts: `build_index.py`, `update_index.py`, `query_index.py`

---

## Proposed ClawHub Standard

This convention is proposed as a ClawHub community standard. Skills submitted to
ClawHub should follow this pattern when persistent local data is required. A future
`clawhub publish` validator may enforce it.
