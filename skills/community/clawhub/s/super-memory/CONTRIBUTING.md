# Contributing to Agent Memory

Thank you for contributing to Agent Memory! This document outlines the standards and processes for maintaining code quality and consistency.

## Development Setup

### Prerequisites

- Python >= 3.10 (推荐 3.12+)
- Git

### Quick Start

```bash
# 1. Clone and install with dev dependencies
git clone https://github.com/agent-memory/agent-memory.git
cd agent-memory
pip install -e ".[dev]"

# 2. Install optional dependencies for full feature testing
pip install -e ".[semantic,chinese,bm25]"

# 3. Verify installation
python -c "from agent_memory import AgentMemory; print('OK')"

# 4. Run tests
pytest agent_memory/tests/ -v

# 5. Run linter
ruff check agent_memory/

# 6. Run type checker
mypy agent_memory/ --ignore-missing-imports
```

## Code Style Guidelines

### Linting & Formatting

We use **ruff** for linting and **mypy** for type checking:

```bash
# Lint (must pass before commit)
ruff check agent_memory/

# Auto-fix lint issues
ruff check --fix agent_memory/

# Type check
mypy agent_memory/ --ignore-missing-imports
```

Configuration is in `pyproject.toml`:
- **ruff**: line-length=120, target-version=py310, select=["E","F","W","I","N","UP","B","SIM","C4","TID252"]
- **mypy**: python_version=3.10, strict=false, warn_return_any=true, ignore_missing_imports=true

### Style Rules

1. **`from __future__ import annotations`** at the top of every file
2. **Google-style docstrings** on public classes and functions
3. **Type hints** on all public API signatures
4. **No `utils.py` dumping grounds** — create focused modules
5. **No circular imports** — engines should not import from mixins or vice versa

## Testing Requirements

### Coverage

- **Minimum coverage: 80%** (enforced by `pyproject.toml` → `fail_under = 80`)
- New features must have test coverage
- Edge cases should be tested

```bash
# Run tests with coverage
pytest agent_memory/tests/ -v --cov=agent_memory --cov-report=term-missing

# Run a specific test file
pytest agent_memory/tests/test_recall.py -v
```

### Test File Naming

- Test files: `test_{module}.py` in `agent_memory/tests/`
- Test files mirror source structure: `test_recall.py` for `recall.py`

## Documentation Update Checklist (Per Release)

Before cutting a new release, verify the following:

- [ ] **VERSION file** updated to the new version number
- [ ] **CHANGELOG.md** updated with all changes since last release
- [ ] **pyproject.toml** `version` field matches VERSION file
- [ ] **\_\_init\_\_.py** `__version__` reads correctly from VERSION (no hardcoded version)
- [ ] **API.md** reflects any new/changed public APIs
- [ ] **README.md** reflects current feature set and usage patterns
- [ ] **SKILL.md** updated if skill system changes
- [ ] **Sphinx docs** (`docs/source/`) rebuilt and verified
- [ ] **\_archive/INDEX.md** updated if any files were archived during the release cycle
- [ ] **Deprecated features** documented with removal timeline (2 major versions)

## File Naming Conventions

### Python Source Files

| Category | Pattern | Example |
|----------|---------|---------|
| Core modules | `snake_case.py` | `memory_system.py`, `recall_engine.py` |
| Mixin modules | `{feature}_mixin.py` | `recall_mixin.py`, `export_mixin.py` |
| Test files | `test_{module}.py` | `test_recall.py`, `test_storage.py` |
| Private helpers | `_{name}.py` | `_errors.py`, `_optional_deps.py` |
| Integration | `{framework}_connector.py` | `langchain_connector.py` |
| Config files | `settings.py`, `*.json`, `*.sql` | `dimensions.json`, `schema.sql` |

### Documentation Files

| Category | Location | Example |
|----------|----------|---------|
| Package docs | `agent_memory/{name}.md` | `API.md`, `README.md` |
| Project docs | `/{name}.md` | `ARCHITECTURE.md`, `CHANGELOG.md` |
| Sphinx source | `docs/source/` | `guides/quickstart.rst` |
| Archived docs | `\_archive/{descriptive_name}.md` | `ROADMAP_V11.md` |

### Naming Rules

1. **No version numbers in filenames** — use VERSION file instead of `memory_system_v12.py`
2. **No date stamps** — use git history instead of `backup_20260412.py`
3. **No `deprecated`/`old`/`backup`/`new` prefixes** — archive old files, use descriptive names for new ones
4. **Prefix private modules with underscore** — `_errors.py`, `_optional_deps.py`
5. **Test files match their module** — `test_recall.py` tests `recall.py`

## Version Reference Rules

### Always Use Current Version

```python
# CORRECT: Read from VERSION file
from pathlib import Path
_version_file = Path(__file__).parent.parent / "VERSION"
__version__ = _version_file.read_text().strip()

# CORRECT: Use importlib.metadata
from importlib.metadata import version
__version__ = version("agent-memory")

# WRONG: Hardcoded version
__version__ = "12.0.0"  # Will become stale

# WRONG: Version in docstring
"""Agent Memory V12 — ..."""  # OK for marketing, bad for logic
```

### Version Update Protocol

1. Update `VERSION` file (single source of truth)
2. `pyproject.toml` version must match
3. `__init__.py` reads from VERSION automatically
4. Never hardcode version numbers in source code logic
5. Docstrings may reference the major version for user-facing context (e.g., "V12 Spirit butler")

## Directory Structure Maintenance

### Current Structure

```
agent_memory_v12/
├── _archive/                    # Archived/legacy files (not imported by active code)
├── agent_memory/               # Main package
│   ├── benchmarks/             # Performance benchmarks
│   ├── collectors/             # Data source collectors (dingtalk, wechat, email, etc.)
│   ├── config/                 # Configuration (dimensions.json, schema.sql, settings.py)
│   ├── connectors/             # External framework connectors
│   ├── dashboard/              # HTML dashboards
│   ├── engines/                # Core engines (recall, ingest, decay, sync, etc.)
│   ├── enterprise/             # Enterprise features (audit, compliance, permissions)
│   ├── infra/                  # Infrastructure (metrics)
│   ├── integration/            # Integration layer (bridge, langchain_connector)
│   ├── mixins/                 # Feature mixins for AgentMemory
│   ├── onboarding/             # First-use welcome guide
│   ├── plugins/                # Plugin system (obsidian, slack, sentiment)
│   ├── privacy/                # Privacy & PII handling
│   ├── proto/                  # Protobuf definitions
│   ├── scripts/                # Utility scripts
│   ├── sdk/                    # TypeScript SDK
│   ├── skill_memory_system/    # Skill memory subsystem
│   ├── spirit/                 # Spirit butler (commands, health, reports)
│   ├── storage/                # Storage backends (SQLite, PostgreSQL, cache)
│   └── tests/                  # Test suite
├── benchmark/                  # LongMemEval benchmark runner
├── docs/                       # Sphinx documentation
├── examples/                   # Usage examples (01_quick_start.py, etc.)
├── scripts/                    # Project-level scripts
└── sqlite3_update/             # SQLite DLL updates
```

### Maintenance Rules

1. **One module, one file** — avoid `utils.py` dumping grounds; create focused modules
2. **Mixins go in `mixins/`** — each mixin adds one capability to AgentMemory
3. **Engines are stateless-ish** — engines receive store/encoder, don't hold global state
4. **Tests mirror source structure** — `tests/test_recall.py` for `recall.py`
5. **No circular imports** — engines should not import from mixins or vice versa
6. **Integration layer is the facade** — `integration/bridge.py` combines adapter + sync + connector
7. **Archive, don't delete** — move obsolete files to `\_archive/` with INDEX.md entry
8. **Empty directories must be removed** — no placeholder directories without files

### Adding a New Module

1. Create the module in the appropriate subdirectory
2. Add `from __future__ import annotations` at the top
3. Add a module docstring
4. Update the subdirectory's `__init__.py` if the module should be publicly exported
5. Add corresponding test file in `tests/`
6. Update `API.md` if adding a public API

## Code Review Checklist

### Before Submitting a PR

- [ ] **No hardcoded versions** — version references use VERSION file or `importlib.metadata`
- [ ] **No temporary/backup files** — no `.bak`, `.old`, `.orig`, `.tmp` files committed
- [ ] **No `__pycache__` committed** — verify `.gitignore` includes `__pycache__/`
- [ ] **No dead imports** — remove unused `import` statements
- [ ] **Type hints on public APIs** — at minimum, function signatures should be typed
- [ ] **Docstrings on public classes/functions** — follow Google style
- [ ] **Tests added/updated** — new features must have test coverage
- [ ] **No circular dependencies** — verify import graph is acyclic
- [ ] **Ruff passes** — `ruff check agent_memory/`
- [ ] **mypy passes** — `mypy agent_memory/ --ignore-missing-imports`
- [ ] **Tests pass** — `pytest agent_memory/tests/ -v`
- [ ] **Coverage >= 80%** — `pytest --cov=agent_memory --cov-report=term-missing`
- [ ] **No files in \_archive imported by active code** — archived code is dead code
- [ ] **CHANGELOG.md updated** — add entry under `[Unreleased]`
- [ ] **No merge conflicts** — rebase on main before submitting
- [ ] **No secrets/keys in code** — API keys, passwords, tokens must use env vars

### Reviewer Focus Areas

1. **API stability** — does this change break existing public APIs?
2. **Import hygiene** — are there unnecessary or circular imports?
3. **Test coverage** — are edge cases tested?
4. **Documentation** — are new features documented?
5. **Security** — no secrets/keys in code, PII handling follows privacy rules
6. **Performance** — no N+1 queries, no unnecessary full-table scans
7. **Naming** — does the naming follow conventions above?

## Archive Management

### When to Archive

- A module is replaced by a newer implementation
- A file references APIs that no longer exist
- A demo/example is superseded by a better one
- A configuration file is for a deprecated feature

### How to Archive

1. Copy the file to `\_archive/` with a descriptive prefix (e.g., `root_`, `agent_memory_examples_`)
2. Delete the original file
3. Remove any empty directories left behind
4. Update `\_archive/INDEX.md` with:
   - Original location
   - Reason for archiving
   - Date archived
   - Version when archived
5. Verify no active code imports the archived file

### Retention Policy

Archived files may be removed after **2 major versions** have passed. For example:
- V11 archives can be removed in V14
- V12 archives can be removed in V15
