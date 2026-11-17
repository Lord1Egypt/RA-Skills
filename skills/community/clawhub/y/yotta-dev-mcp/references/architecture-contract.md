# Architecture contract and system model

`system_model` builds a deterministic model of a local repository and attaches
layer data from an optional architecture contract. Everything runs offline with
the Python standard library; no file is written.

## Contract file

Path: `.yotta/architecture.json`. Plain JSON, version `1`.

```json
{
  "version": 1,
  "project": "demo",
  "layers": [
    {"id": "core", "title": "Core", "paths": ["src/core/**"], "risk": "high"},
    {"id": "api", "paths": ["src/api/**"]},
    {"id": "ui", "paths": ["src/ui/**"]}
  ],
  "rules": [
    {
      "id": "core-no-ui",
      "type": "forbid-dependency",
      "from": "core",
      "to": "ui",
      "severity": "high",
      "claim": "core must not import ui"
    }
  ],
  "boundaries": [
    {"id": "public-api", "layer": "api", "paths": ["src/api/public/**"], "visibility": "public"}
  ],
  "data_ownership": [
    {"store": "memory-db", "owner": "core", "paths": ["var/memory/**"], "kind": "sqlite"}
  ],
  "invariants": [
    {"id": "no-plaintext-secrets", "claim": "secrets are never stored in plaintext",
     "severity": "high", "check": "static"}
  ],
  "risk_weights": {"core": 3, "api": 2, "ui": 1}
}
```

### Fields

| Field | Required | Notes |
|---|---|---|
| `version` | yes | Must be `1`. |
| `project` | no | Free-form name. |
| `layers` | yes | Layer id, optional title/description, `paths` globs, optional `risk`. |
| `rules` | no | `forbid-dependency` (`to` is one layer) or `allow-dependency` (`to` is a layer list). `from`, `to`, `severity` and `claim` describe the invariant. |
| `boundaries` | no | Layer id plus globs; `visibility` is `public`, `internal` or `private`. |
| `data_ownership` | no | Store id, owning layer, globs and optional `kind`. |
| `invariants` | no | id plus a non-empty `claim`; `check` is `static`, `command` or `manual`. |
| `risk_weights` | no | Layer id to a number between 0 and 5. |

Ids match `[a-z0-9][a-z0-9._-]{0,63}`. Paths are repository-relative POSIX
globs and must not be absolute or contain `..`.

### Glob rules

`*` stays inside one path segment, `**` crosses segments, `?` matches one
character, and a trailing `/` means the whole directory (`pkg/` equals
`pkg/**`). Matching is case-sensitive. Layers are evaluated in declaration
order and the first match wins; a module that matches several layers is
reported as `layer-overlap`.

### Validation findings

Every finding carries `code`, `severity`, `message`, a JSON `pointer`, the
contract `path` and short `evidence`. Severity `critical` or `high` makes the
contract `FAIL`; `medium` and `low` are advisory.

| Code | Meaning |
|---|---|
| `contract-invalid-json` | The file is not valid JSON. |
| `contract-not-object` | The root value is not a JSON object. |
| `contract-unsupported-version` | `version` is missing or not `1`. |
| `contract-invalid-layer` / `contract-duplicate-layer` | Layer shape or ids are wrong. |
| `contract-layer-without-paths` | A layer declares no globs. |
| `contract-invalid-path` | A glob is absolute, escapes the root, or is empty. |
| `contract-invalid-rule` / `contract-duplicate-rule` | Rule shape, type or ids are wrong. |
| `contract-invalid-severity` / `contract-invalid-risk` | Enum values are outside the allowed set. |
| `contract-unknown-layer-ref` | A rule, boundary, store or risk weight points at a missing layer. |
| `contract-invalid-boundary` / `contract-invalid-store` / `contract-invalid-invariant` | Section entries are malformed. |
| `contract-unknown-key` | Unknown top-level key; reported as a warning and ignored. |

## system_model output

| Key | Content |
|---|---|
| `status` | `PASS`, `FAIL` (contract has blocking findings) or `UNKNOWN` (something still needs evidence). |
| `contract` | Path, presence, validity, version, layer and rule ids, findings. |
| `model.modules` | Repository-relative module id, language, line count and resolved layer. |
| `model.layers` | Declared layers with the modules that match them. |
| `model.imports` | `source`, `target`, `kind`, `line` and the raw specifier. |
| `model.entrypoints` | Files that look like executable entrypoints. |
| `model.tests` | Test files and the internal modules they import. |
| `model.configs` | Configuration files with a coarse kind. |
| `model.data_stores` | Declared stores (with owner and owner modules) and detected local database files. |
| `unknowns` | `contract-missing`, `contract-invalid`, `unassigned-module`, `layer-overlap`, `unresolved-import`. |
| `unverified_claims` | Verification levels that were not executed, with the reason. |
| `evidence` | Bounded, sorted evidence lines for the findings above. |
| `truncated` | True when the file limit cut the scan short. |
| `model_digest` | `sha256:` digest of the model, stable across runs on the same tree. |

Import kinds: `internal` (another source module), `internal-file` (a
repository file that is not source, such as `package.json`), `external`
(outside the repository) and `unresolved` (a relative path that does not
exist; also listed under `unknowns`).

`system_model` never asserts that a change is safe. Levels `L1` and above stay
listed in `unverified_claims` until a dedicated check runs them.

## architecture_review

`architecture_review` evaluates the same contract against the same system model and
returns every finding with file, line and severity. Per-item status is `PASS`,
`WARN` (advisory findings only), `FAIL` or `UNKNOWN`.

| Code | Meaning | Severity |
|---|---|---|
| `rule-forbid-dependency` | a module in the rule's `from` layer imports the forbidden `to` layer | the rule's severity |
| `rule-allow-dependency` | a module in the rule's `from` layer imports a layer outside `to` | the rule's severity |
| `boundary-visibility` | a module imports a protected boundary it may not reach | `high` for `private`, `medium` for `internal` |
| `data-ownership-mismatch` | a module inside the store paths is not in the owner layer | `medium` |
| `data-store-access-outside-owner` | a module outside the owner layer references the store path | `medium` |

Boundary visibility decides who may import the protected modules:

- `public` - any layer may import them; the declaration is recorded and never a finding.
- `internal` - only modules of the same layer may import them.
- `private` - only modules inside the boundary globs may import them.

Data ownership is checked in two ways: modules that live inside a store's paths but
belong to another layer, and modules outside the owner layer that reference the
store path literal (the part before the first wildcard).

Invariants are never reported as passing. `static`, `command` and `manual` checks
all land in `unverified_claims` with the reason, so a review can be `PASS` while
still stating what it did not verify.

The overall status is `FAIL` when the contract has blocking findings or any
violation reaches `critical` / `high`; `UNKNOWN` when the contract is missing or
anything stays undecided; otherwise `PASS` (advisory findings may still be listed).

### Unknown kinds

| Kind | Meaning |
|---|---|
| `contract-missing` / `contract-invalid` | no usable contract was found. |
| `model-truncated` | the file limit cut the scan short. |
| `unassigned-module` / `layer-overlap` | a module has no layer or matches several. |
| `unresolved-import` | a relative import does not resolve. |
| `rule-target-unassigned` | the rule's source layer matches, but the target module has no layer. |
| `boundary-no-modules` | the boundary globs match no module. |
| `boundary-importer-unassigned` | the importer has no layer, so visibility is undecided. |

## impact_analysis

`impact_analysis` starts from changed files, a unified diff or target symbols and
walks reverse dependencies (internal imports and repository-file imports) into a
bounded cone. Each node carries `depth`, `via`, `line`, `layer` and `is_test`.

Alongside the cone it reports direct consumers, affected layers, boundaries, data
stores, invariants scoped to the changed paths, tests mapped to the cone, the
architecture violations that fall inside the cone, rollback probes and an
explainable blast radius.

| Blast radius factor | Weight | When |
|---|---|---|
| `layer-risk` | 0-5 | highest declared risk weight or risk level of affected layers |
| `layer-count` | +1 / +2 | 3-4 layers / 5 or more layers are affected |
| `cone-depth` | +1 | the consumer chain reaches depth 2 or more |
| `public-boundary` | +1 | a public boundary is inside the cone |
| `data-store` | +1 per store, capped at 2 | declared or detected stores are touched |
| `architecture-violation` | +2 / +3 | a `high` / `critical` violation is inside the cone |

`level` maps the capped score (10 max): 9-10 `critical`, 6-8 `high`, 3-5 `medium`,
otherwise `low`. `score` is the raw sum of the weights and `reasons` lists every
factor with its detail, so the number can be recomputed by hand.

Rollback probes are derived, not invented: `data-store` (affected stores),
`entrypoint` (non-test entrypoints in the cone, capped at 5), `tests` (mapped test
files), `invariant` (declared `command` checks) and `model` (fallback when the cone
has no anchor). Test files that only guard on `__main__` are covered by the test
probe and are not reported as startup entrypoints.

## verification policy

`.yotta/verification.json` is optional. It declares the L2-L4 checks that
`verify_change` may execute, plus manual work that must stay unverified. It never
holds shell strings: `kind` must be one of the whitelisted runners already supported
by `run_checks`.

```json
{
  "version": 1,
  "checks": [
    {
      "id": "unit-tests",
      "level": "L2",
      "kind": "python-unittest",
      "cwd": ".",
      "timeout": 120,
      "required": true,
      "claim": "the unit suite passes"
    }
  ],
  "manual": [
    {"id": "independent-review", "claim": "a second person reviews the change"}
  ]
}
```

| Field | Required | Notes |
|---|---|---|
| `version` | yes | Must be `1`. |
| `checks` | no | Array of L2-L4 checks. |
| `checks[].id` | yes | Unique slug matching the same id rule as the architecture contract. |
| `checks[].level` | yes | `L2`, `L3` or `L4`. |
| `checks[].kind` | yes | `python-unittest`, `pytest`, `python-compile`, `npm-test` or `npm-lint`. |
| `checks[].cwd` | no | Repository-relative directory, default `.`; absolute paths and `..` are rejected. |
| `checks[].timeout` | no | 1-600 seconds, default 120. |
| `checks[].required` | no | Default `true`; a required check that did not run keeps the overall result `UNKNOWN`. |
| `checks[].claim` | no | Human-readable claim recorded in the ledger. |
| `manual[].id` / `manual[].claim` | yes | Manual claims that are always reported as unverified. |

Verification findings use the same evidence shape as the architecture contract:
`code`, `severity`, `message`, JSON `pointer`, `path` and short `evidence`.
Blocking codes include `verification-invalid-json`,
`verification-unsupported-version`, `verification-invalid-id`,
`verification-duplicate-check`, `verification-invalid-level`,
`verification-invalid-kind`, `verification-invalid-cwd`,
`verification-invalid-timeout` and `verification-invalid-manual`.

`verify_change` runs L0/L1 in-process. L2-L4 execute only when the caller passes
`allow_execute=true`; L5 is always manual. A `PASS` means every required claim has
evidence. Unrun or manual claims remain in `unverified_claims` and are never written
as passing.

## Command line

```bash
python scripts/dev_engine.py system-model .
python scripts/dev_engine.py system-model . --contract config/architecture.json
python scripts/dev_engine.py architecture-review .
python scripts/dev_engine.py impact-analysis . --changed src/core/store.py
python scripts/dev_engine.py impact-analysis . --diff-file change.patch --depth 2
python scripts/dev_engine.py impact-analysis . --symbol save
python scripts/dev_engine.py verify-change . --changed src/core/store.py
python scripts/dev_engine.py verify-change . --changed src/core/store.py --level L2 --allow-execute
python scripts/dev_engine.py self-test .
python scripts/dev_engine.py adapter . --action list
python scripts/dev_engine.py adapter . --action run --adapter import-linter --allow-execute
```
