# Quorum Documentation Standards

**Status:** Draft v2 — revised per review feedback  
**Date:** 2026-03-06

---

## Design Goal

Every file in the Quorum codebase should be self-documenting at two levels:
1. **Machine-parseable metadata** — what is this file, who owns it, what version
2. **Human-readable context** — why does this exist, what are the key decisions

This standard defines a universal header schema and two documentation strategies based on file complexity.

---

## 1. Universal Header Schema — `@KEY: value`

Every source file gets a metadata block at the top, using `@KEY: value` pairs inside the language's native comment syntax.

### Format by File Type

**Python:**
```python
# @module: quorum.critics.code_hygiene
# @purpose: Code quality evaluation grounded in ISO 25010 + CISQ
# @grounding: critics/CODE_HYGIENE_FRAMEWORK.md
# @owner: code-hygiene-critic
# @version: 0.3.0
# @tier: tier-2 (default model assignment)
# @relationships: quorum-relationships.yaml
```

**Markdown:**
```markdown
<!-- @doc: guides/CROSS_ARTIFACT_DESIGN.md -->
<!-- @purpose: Architectural decisions for cross-file consistency checking -->
<!-- @status: design-complete -->
<!-- @version: 1.0 -->
<!-- @approved-by: Daniel Cervera, 2026-03-06 -->
<!-- @describes: models.py (Locus, Finding schemas) -->
```

**YAML:**
```yaml
# @config: quorum-relationships.yaml
# @purpose: Declared file relationships for cross-artifact consistency
# @schema-version: 1.0
# @see: guides/CROSS_ARTIFACT_DESIGN.md
```

**Shell:**
```bash
# @script: nist-query.sh
# @purpose: LATM query tool for NIST library database
# @version: 1.0
```

### Required Keys

| Key | Required? | Description |
|-----|-----------|-------------|
| `@module` / `@doc` / `@config` / `@script` | **Yes** | Identity — what this file IS (use the type-appropriate key) |
| `@purpose` | **Yes** | One-line description of why this file exists |
| `@version` | **Yes** | Semantic version or project version this file belongs to |

### Optional Keys

| Key | When to Use | Description |
|-----|-------------|-------------|
| `@grounding` | Critics, frameworks | Which framework/spec document grounds this code |
| `@owner` | Components with clear ownership | The critic/module/subsystem that owns this |
| `@tier` | Model-routed components | Default model tier assignment |
| `@relationships` | Files with cross-artifact contracts | Pointer to manifest: `quorum-relationships.yaml` |
| `@implicit-deps` | Non-obvious dependencies | Runtime dynamic loading, execution order contracts, assumptions not visible from imports |
| `@status` | Design docs, WIP files | draft / design-complete / implemented / deprecated |
| `@approved-by` | Decision documents | Who approved this and when |
| `@describes` | Docs referencing schemas/code | Code files this document describes (for docs only) |
| `@schema-version` | Config/data files | Version of the schema format |
| `@changelog` | Frequently updated files | Pointer to changelog or inline date |

### Rules

1. **Headers go at the very top** — after shebang/encoding lines and SPDX license headers, before imports
2. **One key per line** — no multi-line values in headers
3. **No duplication** — if the SPDX header already has copyright, don't add `@author`
4. **Keep it short** — headers are metadata, not documentation. If you need more than 8 keys, the file is complex enough for a reference doc

---

## 2. Documentation Strategies

### Strategy A: Inline Headers (Low Decision Density)

For files with a single clear responsibility where `@purpose` adequately explains *why* the file works the way it does.

The `@KEY` header block + a standard module/class docstring is sufficient. No separate documentation file needed.

**Example:** `critics/completeness.py` — one critic, one responsibility. The `@KEY` header + class docstring tells you everything. No non-obvious design tradeoffs a future reader couldn't reconstruct from the code.

**Heuristic:** If `@purpose` can adequately explain *why* the file works the way it does, Strategy A is sufficient. If the file contains decisions a reader (human or agent) couldn't reconstruct from the code alone, it needs Strategy B.

**Applied to:**
- Individual critic files (`correctness.py`, `completeness.py`, `security.py`, `code_hygiene.py`)
- Config files (`quorum-config.yaml`, `quorum-relationships.yaml`)
- Utility modules (`output.py`, `prescreen.py`)
- Simple scripts

### Strategy B: Reference Docs (High Decision Density)

For subsystems spanning multiple files, components with non-obvious design tradeoffs, or any file where `@purpose` alone can't explain *why* it works the way it does.

Create a man-page style reference doc in `docs/` with:

```markdown
# [COMPONENT] Reference

## Synopsis
One paragraph: what it does, when to use it.

## Architecture
How the pieces fit together. Diagram if helpful.

## Configuration
All config keys, defaults, and examples.

## API / Interface
Public functions, their signatures, what they return.

## Design Decisions
Why it works this way. Link to decision docs if they exist.

## Known Limitations
What it can't do. What's deferred.

## Examples
Concrete usage examples.
```

**Applied to:**
- The pipeline (`pipeline.py` + `cli.py` + `config.py` — multi-file subsystem)
- The pre-screen system (`prescreen.py` — 10 checks with non-obvious regex choices)
- The critic framework (the base class + how critics are registered and coordinated)
- The rubric system (loader + built-ins + custom rubric authoring)
- Cross-artifact consistency (when built — spans relationships, critic, pipeline coordination)

---

## 3. Header Schema (Machine-Readable Validation)

For agents and pre-screen checks to validate headers, a companion schema defines enum values, formats, and validation rules:

**File:** `quorum-header-schema.yaml` (to be created alongside adoption)

```yaml
keys:
  status:
    type: enum
    values: [draft, design-complete, implemented, stable, deprecated]
  version:
    type: semver
    pattern: "^\\d+\\.\\d+\\.\\d+$"
  tier:
    type: enum
    values: [tier-1, tier-2, tier-3]
  approved-by:
    type: string
    pattern: "^.+, \\d{4}-\\d{2}-\\d{2}$"  # "Name, YYYY-MM-DD"
  purpose:
    type: string
    max_length: 120  # one line
  grounding:
    type: filepath  # must resolve to an existing file
  relationships:
    type: filepath  # must resolve to an existing file
```

This enables a future pre-screen check (`PS-011: Header validation`) that mechanically enforces the standard, closing the loop between "we have a standard" and "we enforce the standard."

---

## 4. Existing Files — Header Adoption Plan

### Phase 1: Critics (highest value — framework-grounded components)
- [ ] `critics/code_hygiene.py` — new file, include headers from creation
- [ ] `critics/security.py` — add headers during revision
- [ ] `critics/correctness.py` — retrofit
- [ ] `critics/completeness.py` — retrofit
- [ ] `critics/base.py` — retrofit
- [ ] `critics/__init__.py` — retrofit

### Phase 2: Core Pipeline
- [ ] `models.py`
- [ ] `pipeline.py`
- [ ] `cli.py`
- [ ] `config.py`
- [ ] `output.py`
- [ ] `prescreen.py`

### Phase 3: Framework & Design Docs
- [ ] `critics/CODE_HYGIENE_FRAMEWORK.md`
- [ ] `critics/SECURITY_CRITIC_FRAMEWORK.md`
- [ ] `guides/CROSS_ARTIFACT_DESIGN.md`
- [ ] `SPEC.md`
- [ ] `CHANGELOG.md`

### Phase 4: Config & Data Files
- [ ] `quorum-config.yaml` examples
- [ ] Built-in rubric JSON files
- [ ] `pyproject.toml` (version key only)

---

## 5. Reference Docs Needed

| Component | File | Priority |
|-----------|------|----------|
| Pipeline & CLI | `docs/PIPELINE_REFERENCE.md` | High — users need this |
| Pre-Screen System | `docs/PRESCREEN_REFERENCE.md` | High — 10 checks need documentation |
| Critic Framework | `docs/CRITIC_ARCHITECTURE.md` | Medium — developers extending Quorum |
| Rubric System | `docs/guides/RUBRIC_BUILDING_GUIDE.md` | **Already exists** ✅ |
| Cross-Artifact | `docs/CROSS_ARTIFACT_DESIGN.md` | **Already exists** ✅ |

---

## 6. What This Enables

- **Grep-able metadata** — `grep -r "@grounding" *.py` instantly shows which framework grounds each critic
- **Automated validation** — pre-screen check PS-011 can validate headers against `quorum-header-schema.yaml`
- **Onboarding** — new contributors can understand any file's purpose from the header alone
- **Single source of truth** — relationships live in `quorum-relationships.yaml`, not scattered across headers; `@relationships` is a pointer, not a declaration

---

*Draft: 2026-03-06. Pending approval.*
