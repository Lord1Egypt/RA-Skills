---
name: python-packaging
description: Deep Python packaging workflow—pyproject metadata, dependencies and optional extras, build backends, wheels, versioning, publishing, and CI release hygiene. Use when building libraries or shipping CLI tools to PyPI or private indexes.
---

# Python Packaging (Deep Workflow)

Packaging connects source to installable artifacts. Prioritize **reproducible builds**, **accurate dependencies**, and **safe** automated releases.

## When to Offer This Workflow

**Trigger conditions:**

- New library or CLI; choosing among Poetry, Hatch, setuptools, uv, etc.
- Broken installs on some Python versions or platforms
- Publishing to PyPI or a private index from CI

**Initial offer:**

Use **six stages**: (1) project layout, (2) metadata & entry points, (3) dependencies, (4) build backend & wheels, (5) versioning & tags, (6) publish & CI). Confirm supported Python versions and target index.

---

## Stage 1: Project Layout

**Goal:** Prefer **`src/`** layout to avoid accidental imports from the repo root; one clear import package name.

**Exit condition:** `pip install .` in a clean venv imports the package correctly.

---

## Stage 2: Metadata & Entry Points

**Goal:** `pyproject.toml` with PEP 621 metadata; `[project.scripts]` or `[project.gui-scripts]` for CLIs.

### Practices

- Link README; specify license SPDX identifier
- Use classifiers for PyPI discoverability

---

## Stage 3: Dependencies

**Goal:** Separate runtime deps from optional extras (dev, docs, speedups); pin strategy differs for **libraries** vs **applications**.

### Libraries

- Avoid overly tight upper bounds unless necessary (avoid dependency hell for consumers)

### Applications

- Use lockfiles (pip-tools, uv, poetry lock) for reproducible deploys

---

## Stage 4: Build Backend & Wheels

**Goal:** Choose build backend (hatchling, setuptools, flit); emit **wheel** + **sdist** where appropriate.

### Native extensions

- Use **cibuildwheel** or similar for manylinux/macOS/windows matrices

---

## Stage 5: Versioning & Tags

**Goal:** Single source of truth for version (static in pyproject or dynamic from VCS); git tags match releases.

---

## Stage 6: Publish & CI

**Goal:** PyPI **trusted publishing** (OIDC) preferred over long-lived API tokens in secrets.

### Practices

- Test with TestPyPI when learning the flow
- Restrict token scope and enable 2FA on PyPI accounts

---

## Final Review Checklist

- [ ] src layout and imports verified in clean venv
- [ ] pyproject metadata complete; console scripts work
- [ ] Dependency policy documented (extras, bounds)
- [ ] Artifacts build for intended platforms
- [ ] Versioning aligned with tags; CI publishing secure

## Tips for Effective Guidance

- Add `py.typed` for typed libraries (PEP 561).
- Lazy-import heavy optional deps inside functions to keep CLI startup fast.
- Namespace packages are easy to misconfigure—prefer one clear top-level package name.

## Handling Deviations

- Monorepos: coordinate versions or use independent packages per folder with clear tooling.
- Docker-only apps: still package for testability; Dockerfile installs the wheel.
