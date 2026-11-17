# Version-standard comparison: SemVer, ecosystem policies, Conventional Commits, CalVer

This file collects the **official source text** behind the `version-decide` skill's decision logic. The quoted rules in each section are taken verbatim from the standards below (verified 2026-10).

> ⚠️ **Scope of authority.** Only the indented quotes and the rule tables are *the standard*. Where this skill departs from the literal standard — notably the **0.x npm/Cargo semantics** (minor = breaking boundary) and the **`security` → patch default** — it is explicitly labeled as **opinionated implementation policy (a local default)**. These defaults are release-strategy guidance, **not** part of any standard, and must not be treated as normative authority. Confirm ecosystem-specific assumptions before publishing.

The decision flow lives in `../SKILL.md`.

---

## 1. SemVer 2.0.0 (Semantic Versioning)

Source: https://semver.org/spec/v2.0.0.html

### Core rules (key points)

| Clause | Rule |
|---|---|
| §2 | Version must be `X.Y.Z`, each segment a non-negative integer, **no leading zeros** |
| §3 | A published version's contents **must not be modified**; any change must ship as a new version |
| §4 | **0.y.z is initial development. Anything may change at any time; the public API must not be considered stable** |
| §5 | 1.0.0 defines the public API; how to increment afterwards depends on how that API changes |
| §6 | Increment PATCH only for backward-compatible bug fixes |
| §7 | Increment MINOR for new backward-compatible functionality; **any public API feature marked deprecated must also increment MINOR**; reset patch |
| §8 | Increment MAJOR for any backward-incompatible change; reset minor and patch |
| §9 | Pre-release: `-` + dot-separated identifiers, ASCII alphanumerics and hyphens only, no leading zeros in numeric identifiers; **pre-release has lower precedence than the associated normal version** |
| §10 | Build metadata: content after `+` **does not affect precedence**; traceability only |
| §11 | Precedence comparison rules (below) |

Note that the applicability conditions of §6/§7/§8 all carry the `(x > 0)` qualifier — **this is exactly where the spec leaves 0.x blank**, and the root of the divergent ecosystem interpretations.

### §11 official precedence example (must hold item by item)

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta
          < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
```

Comparison rules: ① major/minor/patch compared numerically; ② same core → pre-release lower than normal; ③ pre-release compared left-to-right field by field, **numeric fields by value, alphanumeric fields by ASCII, and numeric fields have lower precedence than alphanumeric** (so `1.0.0-1 < 1.0.0-alpha`); ④ same prefix → more fields wins.

### SemVer FAQ advice on 0.x

> The simplest thing to do is start your initial development releases at 0.1.0 and then increment the minor version for each subsequent release.

---

## 2. Conventional Commits 1.0.0

Source: https://www.conventionalcommits.org/en/v1.0.0/

### Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Mapping to SemVer

| Commit | Level |
|---|---|
| `fix:` | PATCH |
| `feat:` | MINOR |
| footer contains `BREAKING CHANGE:`, or `!` after type/scope | MAJOR |
| other types (`build` `chore` `ci` `docs` `style` `refactor` `perf` `test`) | **no implicit effect** |

Key text: a breaking change **may be part of any type** (§3); types other than `feat`/`fix` have "no implicit effect on SemVer" (§14).

### Three easily-misused FAQ answers

1. **What about 0.x?** The official text suggests: "**pretend the product is already released**" — because someone may already be using your software. This **directly conflicts** with SemVer §4 ("may change at any time") and the actual npm/cargo behavior (see §4).
2. **What about revert?** The spec **explicitly refuses to define** it: "Conventional Commits does not make an explicit effort to define revert behavior." It only suggests a `revert` type plus a `Refs:` footer.
3. **Wrong type used?** `git rebase -i` before merge; after release each tool handles it itself.

---

## 3. Official versioning policies per language / ecosystem

### Python — PEP 440 (**not SemVer**)

Source: https://peps.python.org/pep-0440/ (PEP itself marked historical; the authoritative spec is now maintained by PyPA's Version specifiers)

Canonical form:

```
[N!]N(.N)*[{a|b|rc}N][.postN][.devN][+local]
```

Five segments:

| Segment | Meaning |
|---|---|
| **Epoch** `N!` | Switch the whole numbering scheme (e.g. from date `2014.04` to semantic `1!1.0`). Almost no project needs it |
| **Release** `N(.N)*` | The normal version; `1` / `1.4` / `1.4.2` all valid; short segments zero-padded on compare, so `X.Y` == `X.Y.0` |
| **Pre-release** `aN` / `bN` / `rcN` | **no hyphen**: `1.0.0a1`, `1.0.0rc1` |
| **Post-release** `.postN` | A revision after the normal release (e.g. packaging-script fix) |
| **Dev-release** `.devN` | A dev snapshot before pre-release |
| **Local** `+label` | A private marker for a downstream integration branch; **does not change the version type** |

Biggest difference from SemVer: **pre-releases have no hyphen**. `1.0.0-rc.1` is normalized to `1.0.0rc1`; what ends up in PyPI metadata, filenames, and lockfiles is the latter. Write version numbers in PEP 440 form by hand.

PyPA's versioning discussion page notes a real-world exception: **security fixes often have to include breaking changes yet still ship as patch**.

> ⚠️ **Opinionated default (not in the standard).** This skill maps `security` to `patch` by default, but only because real-world security releases frequently bundle breaking changes while still shipping as a patch. This is a *policy choice*, not a rule from PEP 440 or SemVer. `SKILL.md` requires extra confirmation for that scenario.

### Rust — Cargo

Source: https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html

**Compatibility rule: same leftmost non-zero segment = compatible** (unlike SemVer's "all pre-1.0.0 packages are mutually incompatible"):

| Dependency declaration | Actual range |
|---|---|
| `1.2.3` | `>=1.2.3, <2.0.0` |
| `0.2.3` | `>=0.2.3, <0.3.0` |
| `0.0.3` | `>=0.0.3, <0.0.4` |

Pre-releases are **not matched by default**; must be explicit; and `1.0.0-alpha` does not auto-upgrade to `1.0.1-alpha`.

### Go — Semantic Import Versioning

Source: https://go.dev/doc/modules/version-numbers

- **From v2 the module path must carry the major suffix**: `example.com/mod` → `example.com/mod/v2`. This implements the import-compatibility rule: same import path must be backward-compatible.
- v0 / v1 **must not** carry a suffix (`gopkg.in/` is the exception, using `.v2` form).
- Benefit: **different majors can coexist in one build**, resolving diamond-dependency conflicts.
- Historical projects that shipped v2 without a suffix are tagged `v2.0.0+incompatible`.
- v0 vs v1: in most cases v1 is still compatible with the last v0; **v1 is a "promise of compatibility", not "breaking relative to v0"**.

### Node.js — the runtime's own versioning policy

Source: https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule

From October 2026 Node ships **one major per year** (April Current, October → LTS), and adds an **Alpha channel** (October to next March, 6 months) where **semver-major changes are allowed** during Alpha, using the standard SemVer pre-release form (e.g. `27.0.0-alpha.1`). Previously it was two majors per year, odd/even split into Current/LTS.

### CalVer (Calendar Versioning)

Source: https://calver.org/

`YY.MM.PATCH` (Ubuntu 24.10, pip 26.0.1, Black 26.3.1), `YYYY.MM.DD` (yt-dlp 2026.08.19), `YY.MINOR` (Apple, from 2025, switched its entire OS lineup to year numbering: iOS 26 / macOS 26 / Xcode 26).

Neo4j is a recent migration case: **from January 2025 it switched from SemVer to CalVer** (`YYYY.MM.PATCH`), and in 2025.06 decoupled the Cypher language version from the server to evolve independently.

Applicability signal: release cadence strongly tied to the calendar, support windows that must be obvious at a glance, version number expressing "freshness" rather than compatibility.

---

## 4. Conflicts between standards (what the decision logic must handle)

| Conflict | SemVer 2.0.0 | Actual ecosystem behavior |
|---|---|---|
| **Can 0.x break freely?** | §4: change anytime, API unstable | npm `^0.2.3` = `[0.2.3, 0.3.0)`, Cargo same; **minor bump IS the breaking boundary**. Composer (PHP) treats `^0.2.3` as `[0.2.3, 1.0.0)`, looser |
| **Commit convention in 0.x** | §4: no guarantee | Conventional Commits officially suggests "pretend already released" |
| **Is there an increment rule for 0.x?** | No explicit rule | Academic study (arXiv 2101.00836) found Cargo/npm/Packagist don't strictly follow; 0.y.z release frequency is not higher than ≥1.0.0; many projects never cross 1.0.0 |
| **Which level is deprecation?** | §7: must be MINOR | No dispute |
| **Security fix with breaking change** | Unspecified | In practice often shipped as patch |

> ⚠️ **Opinionated default (not in the standard).** During 0.x this skill adopts **npm/Cargo semantics** (minor = breaking boundary). This is a *policy choice*: it matches the package managers' actual resolution behavior and truthfully protects dependents, but SemVer §4 itself leaves 0.x unspecified. The skill states this explicitly in its output so it is never mistaken for a standard requirement.
