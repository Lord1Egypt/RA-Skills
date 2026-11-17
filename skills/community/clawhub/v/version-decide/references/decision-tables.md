# Decision Table: Change Type → Version Level

This file is the lookup basis for the decision flow in `../SKILL.md`. Every rule cites its source; abbreviations are listed at the end. The arithmetic is executed by `../scripts/semver_check.py`; this file only defines **which kind of change maps to which level**.

---

## 1. Main decision table (stable versions, major ≥ 1)

| Change type | Level | Basis | Note |
|---|---|---|---|
| Remove/rename a public export | **major** | S§8 | Old code fails to import |
| Public function signature change (add/remove param, change type, change return) | **major** | S§8 | |
| Public interface behavior change (previously-successful call now fails, or semantics shift) | **major** | S§8 | Most underrated category |
| Rename/remove a public config/env/CLI argument | **major** | S§8 | Config is also API |
| Tighten validation, change a default, change a unit or precision | **major** | S§8 | Unless provably equivalent for all existing usage |
| Delete an entire feature module | **major** | S§8 | |
| **Mark deprecated** (still usable, warning only) | **minor** | S§7 | Spec **explicitly requires** minor |
| Add public API (function/class/type/optional config) | **minor** | S§7 | |
| Add optional dependency / relax a dependency constraint | **minor** | G (minor covers dep changes) | Go treats dep changes as minor |
| Internal refactor (public signature and behavior unchanged) | **patch** | S§6 | |
| Performance optimization (behavior preserved) | **patch** | S§6 | Credible only with measurable metrics |
| Fix erroneous behavior | **patch** | S§6 | |
| Raise the minimum runtime requirement (Node/Python/Go version) | **major** ⚠️ | S§8 corollary | See §4 confirmation items |
| Security fix that does not change the API shape | **patch** | P (PyPA) | PyPA explicitly endorses this convention |
| Pure docs / tests / CI / formatting | **none** | C§14 | Other types have no implicit effect; **usually no release** |

`none` is a level this skill deliberately adds: the most common beginner mistake is counting a README edit as a patch release.

---

## 2. 0.x special rules (major == 0)

SemVer §4 says "anything may change at any time", but **does not specify how 0.x should increment** — this is a gap in the spec. npm and Cargo fill it the same way (academic study arXiv 2101.00836 found all three do not strictly follow SemVer in practice).

**This skill adopts npm/Cargo semantics**:

| Change | 0.0.z | 0.y.z (y ≥ 1) |
|---|---|---|
| patch-level (fix/refactor/perf) | 0.0.(z+1) | 0.y.(z+1) |
| minor-level (feature/deprecate) | **0.1.0** | **0.(y+1).0** |
| major-level (breaking) | **0.1.0** | **0.(y+1).0** |

Rationale: the dependency constraint for `0.2.3` is `>=0.2.3, <0.3.0`, so **incrementing minor IS the breaking boundary**. This way the version number truthfully tells dependents "will upgrading break me?".

**0.x → 1.0.0 is an explicit graduation action** (level `stable`), not auto-derived from a change type. It is not "fixed a bug" or "added a feature" — it is the declaration "from now on the API is stable". A human must confirm the API is frozen and the support policy is documented before it runs.

Composer (PHP) treats `^0.2.3` as `[0.2.3, 1.0.0)`, looser than npm. If a project ships on Composer, a minor bump during 0.x **does not** break dependents — then a true major bump may be relaxed. Ask the target ecosystem in the confirmation step.

---

## 3. Pre-release channels

| Stage | Semantics | Who uses it |
|---|---|---|
| `alpha` | API may be overturned at any time; early taste | the developer, CI |
| `beta` | API basically settled; feature freeze, bug-fix only | early users willing to give feedback |
| `rc` | release candidate; diff vs stable should be docs/bug-fix only | the whole team with CI green, ready to ship |

### Stage-advance rules

- Advance **one step at a time only**: alpha → beta → rc → stable. Skipping is rejected by the script.
- Re-publish in the same stage: sequence +1 (`2.0.0-alpha.1` → `2.0.0-alpha.2`).
- Advance a stage: sequence resets to 1 (`2.0.0-alpha.3` → `2.0.0-beta.1`).
- rc → stable: drop the pre-release identifier (`2.0.0-rc.2` → `2.0.0`).
- **core stays unchanged within a pre-release line**. SemVer §9 explicitly says a pre-release is not guaranteed to satisfy the compatibility of its associated normal version, so introducing further breaking changes during alpha **does not** require raising major again — that is exactly what a pre-release channel is for.
- Use `--rebase` explicitly when you need to target a different version number.

### A npm/Cargo trap

Both **do not match pre-releases by default**: `foo = "1.0"` will not match `1.0.0-alpha`; you must write `foo = "1.0.0-alpha"` explicitly. Cargo adds: `1.0.0-alpha` will not auto-upgrade to `1.0.1-alpha`. So **a pre-release cannot be the default distribution channel to downstream**.

### Build number (`+` suffix)

Does not affect precedence (§10); only for traceability: commit SHA, build time, internal run id. `1.0.0+build.1` and `1.0.0+build.2` have the **same** precedence — so it cannot express "a newer version" nor drive auto-upgrade decisions.

---

## 4. Key information that MUST be confirmed with the user

Each of the following changes the conclusion; **never assume it for the user**:

### 1. Intent of the change

What problem is being solved, not what was edited. The same diff, "bug fix" vs "incidental refactor", may map to different levels and different messaging.

### 2. Is there a breaking change — check item by item

Must be answered explicitly; never default to "probably not breaking":

- Any public export removed or renamed?
- Function signature, param order, or return type changed?
- **Does a previously-successful call now fail or throw?**
- Config/env/CLI argument/default changed?
- Minimum dependency version raised?
- Any type/field narrowed (e.g. Rust generic constraint, Python input-type narrowing)?

### 3. Target ecosystem and release channel

- Which ecosystem? (npm `^0.x` and Composer `^0.x` differ in semantics)
- Does downstream need a **migration window**? (→ cut a pre-release first, give a full deprecation window)
- Stable or pre-release? Which channel (alpha/beta/rc)?
- Is the public API declared? (SemVer §1 **requires** declaring the public API, otherwise nothing can be judged breaking — this is the most fundamental precondition)

### 4. Dependency and compatibility impact

- How many downstream dependents? Any paid/critical customers?
- Can dependents upgrade smoothly? Need migration docs?
- Any cyclic dependency or workspace lock with other packages?
- Go project: bumping to v2+ **changes the module path**; all imports must be updated in sync — confirm acceptance.

### 5. ⚠️ Gray zones needing extra confirmation

| Gray zone | Why hard | Handling |
|---|---|---|
| **Security fix** | May have to change the API to close the hole | First ask "can the API shape stay?"; if yes → patch, else → major and note the security reason |
| **Raise min runtime** | Blurry boundary | If old-env users can still run → patch/minor; if they can't → major. Ask "who is your oldest user?" |
| **Perf optimization** | "behavior preserved" needs proof | Require benchmark data; without data, treat conservatively as minor |
| **Refactor** | May silently change behavior | Require "is public API behavior covered by tests?"; without coverage, treat as minor |
| **Internal cleanup** | Not perceived by dependents | patch; if it also changed public behavior, re-grade |
| **0.x → 1.0.0** | Not a change type, it is a promise | Must be human-confirmed API freeze before using `stable` |

---

## 5. Edge cases

### Revert

Conventional Commits **explicitly refuses to define** revert's version semantics. This skill adopts:

- Revert a **non-breaking** change → **patch**. Code returns to a known-good state.
- Revert a **breaking** change → **major**. Because compatibility is **broken a second time**; dependents just recovered and are broken again. Script type: `revertbreak`.
- Reverting an already-published version: **do not move the published version number** (§3 forbids editing published versions). The correct move is to release a new version number.

### Deprecate

SemVer §7 is explicit: whenever any public API feature is marked deprecated, MINOR **must** be incremented. Even with no other change, even before removal. Removal happens in a later major.

Best practice: deprecate on a minor → keep at least one minor cycle → remove on a major. Gives downstream a clear migration window.

### Coexist multiple majors

When different majors coexist, the version number **must** distinguish them, and the import path must too:

- **Go**: v2+ must change the module path to `example.com/mod/v2`; different majors naturally coexist in one build, solving the diamond-dependency conflict.
- **Python**: only one version of a package name can be on PyPI; isolate via virtualenvs; to coexist you need different package names or different install environments.
- **npm**: only one `latest` per package name; use dist-tag (`next` / `beta` pointing at pre-releases).
- **Rust**: different majors are different versions under one package name; cargo resolves multiple versions simultaneously.

### Misc

- **Published versions are immutable** (§3). If you shipped the wrong number, only release a new one — never move the tag.
- **Shipped a breaking change during 0.x but bumped patch**: this misleads dependents. Fix by releasing a minor (aligning with real semantics) and noting the version-semantics convention in the changelog.
- **Highest level in a batch wins**: `feat + fix` → minor; `feat + break` → major. This is the core logic of `analyze`.

---

## 6. Source abbreviations

| Abbr | Source |
|---|---|
| **S** | Semantic Versioning 2.0.0 — https://semver.org/spec/v2.0.0.html |
| **C** | Conventional Commits 1.0.0 — https://www.conventionalcommits.org/en/v1.0.0/ |
| **P** | PyPA Versioning discussion / PEP 440 — https://packaging.python.org/en/latest/discussions/versioning/ |
| **G** | Go Modules version numbering — https://go.dev/doc/modules/version-numbers |
| **N** | Node.js release-schedule change announcement — https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule |
| **R** | Cargo version requirements — https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html |
| **A** | arXiv 2101.00836 (0.y.z empirical study) — https://arxiv.org/pdf/2101.00836v1 |
