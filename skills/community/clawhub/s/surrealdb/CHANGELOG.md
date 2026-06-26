# Changelog

All notable changes to this project will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [1.7.1] - 2026-06-17 — cross-domain gotchas catalog

### Added

- **`rules/gotchas.md`** — consolidated footgun reference covering upgrade/migration,
  security, graph, vector, SurrealQL, MCP, SDK, and operational gotchas (v3.1.4+).
- **AGENTS.md decision tree** for "surprising SurrealDB behavior / gotcha" queries.
- **`gotchas` capability** in `onboard.py --agent` manifest.

### Changed

- **`rules/graph-queries.md`** — renamed section to "Graph Gotchas" with pointer to
  `rules/gotchas.md` for cross-domain coverage.
- **`rules/surrealql.md`** — replaced stale v3.1.0-alpha stub with v3.1.4 patch
  notes summary linking to gotchas and deployment rules.

## [1.7.0] - 2026-06-17 — SurrealDB 3.1.4 GA tracking

### Added

- **Built-in MCP server** documentation in `rules/surrealmcp.md` (`surreal mcp`
  stdio, HTTP `POST /mcp`) with standalone `surrealmcp` boundary guidance.
- **DiskANN vector index** coverage in `rules/vector-search.md` alongside HNSW,
  including 64-bit platform gate and shared `<|K, EF|>` query operator.
- **Graph edge-case wisdom** in `rules/graph-queries.md`: inline edge filters
  (v3.1.3 fix), `$parent` scope, RELATION + partial UNIQUE index (#7280),
  record-links-vs-edges modeling, agent-memory demo pointer, official YouTube
  references.
- **3.0→3.1 upgrade guide** in `rules/deployment.md` with breaking-change table.
- **Ecosystem pointers**: surqlize, datasets, agent-memory, kaig, built-in MCP
  in `rules/ecosystem-integrations.md`; new entries in `SOURCES.json`.
- **SurrealKit v0.7.0**, **Surrealist v3.9.0**, **Java SDK v2.1.1**, **LSP
  v0.1.6**, **CodeMirror v1.0.6**, **VSX v0.4.2**, **JetBrains v0.2.3**.

### Changed

- **Target server**: v3.0.5 → **v3.1.4** (recommend minimum for production).
- **`rules/surrealql.md`**: full ALTER coverage (v3.1.0+), `value::expect`,
  v3.0.5 seven-target boundary preserved for older servers.
- **`rules/surrealism.md` / deployment**: async Surrealism and `--allow-net`
  hardening pointers (via deployment upgrade section).
- **Spectron status**: roadmap-only → alpha in JS/Python SDK main (boundary
  preserved in ecosystem-integrations).
- **Provenance refresh** across `SOURCES.json`, `AGENTS.md`, and `SKILL.md`.

### Security

- Document **GHSA-8rw6-p7m8-63jp** array element-level SELECT permission fix
  (v3.1.4) in `rules/security.md`.
- Retain auditor-safe install guidance: brew/Docker/`surreal upgrade` only — no
  `curl | sh` in skill scripts or primary install paths.
- Built-in MCP stdio owner-level access warning added to MCP rules and AGENTS
  decision tree.

## [1.6.6] - 2026-05-14 — ecosystem refresh, provenance normalization, and release workflow hardening

### Added

- **`rules/ecosystem-integrations.md`** covering the official scoped n8n
  community node (`@surrealdb/n8n-nodes-surrealdb` v0.6.0), the official AI
  framework docs index, Spectron / Agent Memory Context as roadmap-only,
  CodeMirror packages, and the upstream `surrealdb/agent-skills` repo.
- **CodeMirror coverage** in `rules/editor-tooling.md` for
  `@surrealdb/codemirror` / `@surrealdb/lezer` v1.0.5.
- **SDK provenance expansion** for first-party Java, .NET, PHP, C, Swift,
  Kotlin, and Ruby repositories in `SOURCES.json`.

### Changed

- **Upstream provenance normalized to concrete SHAs** across 31 tracked repos,
  replacing sentinel values such as `tracked-via-pypi` / `tracked-via-surrealdb`
  with auditable commit baselines.
- **`rules/sdks.md`** now calls out the unreleased Python v3 builder API and
  `surrealdb-embedded` split, .NET `SurrealDb.Net` v0.10.2, and the source-only
  C binding caveat.
- **`rules/surrealkit.md`** updated to v0.6.3 with current install surfaces
  (`cargo binstall`, Cargo, release archives with checksums, GHCR Docker image),
  template variables, and current `SURREALDB_*` env-var behavior.
- **`rules/surrealml.md`** now separates GitHub `v0.1.2` from PyPI `0.0.4` and
  flags setup-time native-library downloads unless `LOCAL_BUILD=TRUE`.
- **`rules/surrealist.md`** moved to main commit `cc19eb149dbc`, noting
  post-release dropdown and workflow/supply-chain hardening without claiming a
  newer public release.

### Security / CI

- Kept runtime script permissions stable: no new credential storage, no hidden
  production shortcuts, and no remote shell installer guidance.
- Updated GitHub Actions from deprecated Node 20 action majors to exact current
  tags: `actions/checkout@v6.0.2`, `actions/setup-python@v6.2.0`, and
  `astral-sh/setup-uv@v8.1.0`. `setup-uv` does not publish a `v8` major alias.
- Disabled uv cache auto-detection in this repo because it has no dependency
  lockfile, and pinned publish-time Node to `actions/setup-node@v6.4.0` /
  Node 22 so `clawhub` does not emit Node-engine warnings.
- Made the `clawhub publish` step idempotent for reruns: an existing
  `surrealdb@1.6.6` version is treated as already published instead of a failed
  release.
- Fixed the nightly upstream-check red flag by creating the `upstream-update`
  label idempotently before issue creation.

## [1.6.5] - 2026-05-06 — `rules/vector-search.md` deferred-IMPORTANT closure (HASHED_VECTOR semantics + minkowski/jaccard/pearson similarity-fn examples) — 9-pass 4-WAY ratification

### Added

- **`rules/vector-search.md` deferred-IMPORTANT cleanup (batch
  5 of the v1.5.x convergence cycle).** Closes the three
  vector-search.md items in the v1.5.x deferred-IMPORTANT
  backlog:
  - **HASHED_VECTOR storage semantics block.** Pre-existing
    parameter table mentioned `HASHED_VECTOR` as
    "memory-optimised" without documenting what flips at
    runtime. Added an explainer block (matching the LM/M0/
    MINKOWSKI clarification style) documenting the v3.0.5
    behaviour: the bare keyword (no value, default `false`
    at parser `core/src/syn/parser/stmt/define.rs:1114`,
    flipped at `:1151-1153`) changes how the
    **vector → document-IDs** lookup table is keyed (full
    serialised vector via `new_hv_key(&ser_vec)` at
    `core/src/idx/mod.rs:115` versus a constant 32-byte
    hash via `new_hh_key(hash: [u8; 32])` at
    `core/src/idx/mod.rs:119`). Hash collisions handled by
    bucketing (`ElementHashedDocs` with exact-match scan,
    `core/src/idx/trees/hnsw/docs.rs:281-440`). The HNSW
    graph storage itself is unchanged.
  - **MINKOWSKI in similarity-functions section.**
    Pre-existing section showed cosine/euclidean/manhattan/
    chebyshev/hamming examples but omitted the
    `vector::distance::minkowski(a, b, order)` 3-arg form
    (defined at `core/src/fnc/vector.rs:113-115`,
    implemented at
    `core/src/fnc/util/math/vector.rs:160-175` — the Lp
    norm `(Σ|a_i − b_i|^p)^(1/p)`). Added an example with a
    note on the limiting cases (p=1 ≡ Manhattan, p=2 ≡
    Euclidean, p → infinity approaches Chebyshev).
  - **`vector::similarity::jaccard()` /
    `vector::similarity::pearson()` examples + appropriateness
    callout.** Pre-existing JACCARD/PEARSON HNSW inversion
    warning (v1.5.x) covered the indexed-KNN footgun but
    left the standalone scalar functions undocumented. Added
    examples + a callout that documents the actual v3.0.5
    semantics:
    - **`vector::similarity::jaccard()`** dispatches as
      `(Vec<Number>, Vec<Number>)` (`core/src/fnc/vector.rs:130`)
      — numeric arrays only; string-token arrays fail
      runtime coercion. Implementation at
      `core/src/fnc/util/math/vector.rs:120-126` is
      multiset-asymmetric on the second argument (counts
      duplicates in `other`, dedupes the union). Concrete
      divergence: `vector::similarity::jaccard([1], [1, 1])`
      returns `2.0`, not `1.0`. Pre-deduplicate inputs with
      `array::distinct(...)` for textbook set-Jaccard
      semantics. Range `[0, 1]` after dedup; raw range
      `[0, |b|]`; `NaN` if both inputs empty.
    - **`vector::similarity::pearson()`** computes the
      population Pearson correlation coefficient. Range
      `[-1, 1]` for finite, non-zero-variance inputs.
      Edge cases documented end-to-end at the IEEE-754 f64
      arithmetic level: integer constants (`[1, 1, 1]`)
      hit the `0 / 0 = NaN` path; float constants are
      literal-dependent (`[0.3, 0.3, 0.3]`,
      `[0.5, 0.5, 0.5]`, `[0.25, 0.25, 0.25]` round-trip
      exactly through f64 sum-and-divide and hit the NaN
      path; `[0.1, 0.1, 0.1]` does not round-trip and
      produces a finite ratio dependent on the other
      operand); `Decimal`-typed operands route through
      exact-arithmetic branches and hit the NaN path. f64
      underflow can also drive denominator to `0.0` while
      covariance remains non-zero, producing `±Infinity`
      (e.g.
      `pearson([0.0, 1e-308], [0.0, 1e154]) = +Infinity`).
    - **HNSW pearson divergence note.** The HNSW-internal
      Pearson at
      `core/src/idx/trees/vector.rs:413-440` short-circuits
      to `0.0` when `denominator == 0.0` (the explicit
      `if denominator == 0.0 { return 0.0; }` at
      `:435-437`), unlike the standalone path which can
      return `NaN` or `±Infinity`. Documented in a
      sub-callout under the inversion warning.

### Changed

- Updated PEARSON / JACCARD distance-function table cells
  (the existing v1.5.x guide table) to reflect the
  documented edge-case behaviour:
  - JACCARD: `NaN if both inputs empty; otherwise [0, |b|]
    raw (multiset-asymmetric numerator) / [0, 1] after
    pre-dedup`.
  - PEARSON: `finite results in [-1, 1]; non-finite (NaN /
    ±Infinity) possible for zero-denominator or
    NaN-element inputs (see callout)`.

### Convergence

This patch was reviewed across **9 passes of 4-WAY
adversarial review** (Cursor Composer 2 + Codex
`gpt-5.5` xhigh + Gemini 3.1 Pro + Pi+DeepSeek-V4-Pro:xhigh)
on a single rule patch. Final verdict: **4/4 GO with 0
CRITs, 0 IMPs, 0 MINORs at pass-9** (HEAD `0b26c27`).

CRIT trajectory across the cycle:
| Pass | Verdicts | CRITs | Notes |
|------|----------|-------|-------|
| 1 | rev-1 | 1 | Codex: string-array Jaccard fails runtime arg coercion |
| 2 | rev-2 | 1 | Cursor unique: jaccard impl multiset-asymmetric — `[0, 1]` range claim wrong; 3-way IMP CONVERGENT (pearson Infinity impossible — true for constant-operand sub-case only) |
| 3 | rev-3 | 1 | Codex unique: pearson constant-vector NaN claim missed f64 mean-rounding for FLOAT constants like `[0.1]` |
| 4 | rev-4 | 0 | 2 CONVERGENT IMPs (pearson "tiny finite" wording; JACCARD table both-empty NaN carve-out) |
| 5 | rev-5 | 1 | Codex unique: float-constant overgeneralization — `[0.3]`/`[0.5]`/`[0.25]` round-trip exactly and DO hit NaN path |
| 6 | rev-6 | 0 | Cursor unique CRIT REJECTED via empirical Python f64 trace — Cursor's `[0.3, 0.3, 0.3]` non-roundtrip claim was a hand-arithmetic error; Codex pass-5 verified correct. Codex 2 unique IMPs ACCEPT (exact-zero overclaim + HNSW pearson short-circuit divergence) |
| 7 | rev-7 | 1 | Codex unique: f64 **underflow** edge — earlier "Infinity impossible" claim was correct only for constant-operand case; underflow case can drive `std_dev = 0` with non-zero covariance, producing `±Infinity` |
| 8 | rev-8 | 2 | Codex: earlier prose still implied "std_dev=0 → covar=0 → NaN" universally without underflow exception; HNSW divergence callout said "NaN behaviour" not "non-finite"; PEARSON table cell missed `±Inf` |
| 9 | rev-9 | **0** | **CONVERGENCE TARGET REACHED — 4/4 GO with 0 CRITs / 0 IMPs / 0 MINORs across all 4 reviewers** |

**Total: ~8 CRITs found-and-fixed across 9 passes.**

Pi pass-2 / pass-3 / pass-5 / pass-7 produced wrong CRITs
or wrong MINORs from misreading multi-arm match-arm line
ranges or misreading f64 accumulation order
(`feedback_pi_unique_crit_verify_against_source.md`
applies symmetrically to all reviewers). Cursor pass-6
also produced a wrong unique CRIT from IEEE-754 hand-trace
arithmetic. Both rejection patterns required empirical
re-verification (parser-source line check; Python f64
struct trace for the f64 round-trip claim) before
patching.

### Notable findings

- **Walk-examples-end-to-end doctrine surfaced again.**
  Codex pass-1 caught the string-array Jaccard runtime
  coercion failure exactly the way Pi pass-3 caught the
  v1.6.2 `$token` in SIGNIN bug. Parse-clean ≠ runtime-
  clean for SurrealQL. Doctrine update folded into the
  existing memory file.
- **f64 IEEE-754 minutiae caused 5 of 9 passes' worth of
  edge-case escalation.** The pearson edge-case prose
  alone went through revs 4-9 to converge: integer
  constants → NaN; float constants → literal-dependent
  (some round-trip exactly, others don't); Decimal
  operands → exact, NaN; underflow → ±Infinity. The lesson
  is that documenting f64 edge cases for a similarity
  function requires walking the actual sum-and-divide
  pipeline (NOT intermediate-step shortcuts) and naming
  the regimes explicitly with concrete examples.
- **HNSW pearson short-circuit divergence (separate from
  the inversion bug).** Surfaced by Codex pass-6 as a
  RESIDUAL RISK noted by Pi pass-5; escalated to IMP at
  pass-7. The standalone path returns `NaN`/`±Infinity`
  for zero-denominator inputs; the HNSW path returns
  `0.0` (`if denominator == 0.0 { return 0.0; }` at
  `core/src/idx/trees/vector.rs:435-437`). Documented in
  a sub-callout under the existing inversion warning.

### Deferred to v1.6.6

Pass-9 produced 0 deferrable items. Pass-1 / pass-2 /
pass-3 / pass-5 cosmetic MINORs that survived earlier rev
disposition lists (define.rs:1154 → 1153 cite
tightening, I64 missing from Supported Data Types comment
block, minkowski source-line cite, jaccard fixture span
blank-line drift, `|b|` vs `|other|` symbol consistency
between table and callout) all remain available as a
v1.6.6 ride-along if a future polish pass wants them.

Plus the broader v1.5.x deferred-IMPORTANT backlog (now
**vector-search.md complete**):

- `surrealql.md`: data-type variants (regex, range,
  literal, file); `array<T,N>` cardinality; INSERT IGNORE
  example; DEFINE API; DEFINE CONFIG; INFO FOR
  INDEX/USER variants
- `performance.md`: TLS flags in start-flag list;
  SURREAL_HNSW_CACHE_SIZE env-var verification; REBUILD
  INDEX ON TABLE all-indexes form; SCHEMAFULL inference
  rationale
- `graph-queries.md`: sub-SELECT graph clauses; `$parent`
  in WHERE; custom edge Record IDs in RELATE;
  +path+inclusive form

### Memory artefacts

No new doctrine files written this cycle; existing
`feedback_walk_examples_end_to_end.md` and
`feedback_pi_unique_crit_verify_against_source.md`
applied symmetrically to Pi (multi-pass match-arm
misreads + f64 accumulation-order error) AND Cursor
(IEEE-754 hand-trace error in pass-6). Pattern
generalises beyond Pi.

## [1.6.4] - 2026-05-06 — `rules/data-modeling.md` deferred-IMPORTANT clause closure + v1.6.3 ride-along security.md cite tightening (3 atomic feature commits + release commit)

### Added

- **`rules/data-modeling.md` deferred-IMPORTANT cleanup (batch
  4 of the v1.5.x convergence cycle).** Closes both items
  attributed to data-modeling.md in the v1.5.x convergence
  notes:
  - **Exact kNN metric mismatch fixed.** Pre-existing example
    used `<|10,EUCLIDEAN|>` as the brute-force operator but
    `vector::similarity::cosine()` as the projected score —
    top-10 by Euclidean re-ordered by an unrelated cosine
    score, almost never the intended semantic. Rewrote with
    two correctly-paired examples (Cosine path:
    `<|k,COSINE|>` + `vector::similarity::cosine()` + ORDER BY
    similarity DESC; Euclidean path: `<|k,EUCLIDEAN|>` +
    `vector::distance::euclidean()` + ORDER BY distance ASC).
    Documents all three NearestNeighbor variants (`K` /
    `KTree` / `Approximate` per
    `core/src/sql/operator.rs:393-398`) so consumers know
    which form to use for which case.
  - **Illustrative-edge consistency.** Three edge tables
    (`knows`, `reviewed`, `parent_of`) used in the doc's
    traversal + recursive-query examples lacked
    `DEFINE TABLE` statements. Added explicit definitions
    with `TYPE RELATION ... IN ... OUT ... ENFORCED` matching
    the doc's broader 'define edges first' pattern used for
    `wrote` / `purchased` / `follows` / `likes` /
    `ships_to` / `enrolled_in` / etc. Inline comment
    explains that v3 SCHEMALESS still creates RELATE rows on
    undefined edge tables (so the original examples worked at
    runtime), but the explicit definition documents the
    expected shape and lets ENFORCED reject malformed
    RELATEs at write time.

### Changed

- **`rules/security.md`** — v1.6.3 Cursor pass-1 M3
  ride-along: tightened ROUTING-CLAIM REQUIREMENT block's
  `:288-297` cite to `:292-297` (the actual claims-match arm)
  + `:824-825` to `:825` (the entire `_ => Err(InvalidAuth)`
  arm sits on :825; :826 is the surrounding match's closing
  brace). Cosmetic
  precision improvement; no semantic change.

### Process notes

3 atomic commits (kNN metric fix; illustrative-edge
consistency; release-with-bundled-security-cite) + 1 rev-2
review-fix commit closing pass-1 findings.

Pass-1 4-WAY review:
- Cursor: CONDITIONAL GO (0 CRITs / 1 IMP / 3 minors)
- Codex:  NO-GO          (1 CRIT / 2 IMPs / 1 minor)
- Gemini: GO              (0 findings)
- Pi:     pending at rev-2 dispatch

Rev-2 closes:
- **Codex C1**: rev-1 doc described `<|k|>` (NearestNeighbor::KTree)
  as "requires a defined index" — but per
  `core/src/exec/planner/util.rs:391` + `analysis.rs:1001-1005`
  + `select.rs:1421-1425`, KTree is parser-accepted but NOT
  handled at the planner level in v3.0.5 (legacy v2 m-tree
  remnant). Rewrote to clarify only `<|k,dist|>` and
  `<|k,ef|>` are implemented; `<|k|>` is grammar-accepted
  with no active planner path.
- **Cursor I1**: security.md still had two stale `verify.rs:288-297`
  + one `:824-825` ref at lines 548 + 1659-1661 that the
  rev-1 ride-along missed. Replace-all fixed.
- **Codex I1**: CHANGELOG commit-count drift. Now accurately
  reflects 3 atomic + 1 rev-2 review-fix commit shape.
- **Codex M1 + Pi I1 (CONVERGENT)**: `:826` is the
  surrounding match's closing brace, not the body line — the
  entire `_ => Err(InvalidAuth)` arm sits on `:825`. Reworded
  rule + CHANGELOG to cite `:825` only.

## [1.6.3] - 2026-05-06 — `rules/security.md` v1.6.2 pass-7 deferred-IMP polish (1 atomic doc commit + release commit + rev-2 review-fix commit)

### Changed

- **`rules/security.md` v1.6.2 pass-7 deferred-IMPORTANT
  cleanup.** Closes the five documentation-polish items that
  v1.6.2 pass-7 ratified as deferrable, plus a CHANGELOG
  housekeeping label. None affect runtime correctness — all
  source-citation tightening, cross-reference consistency, and
  example consolidation:
  - **`auth0_jwt` TYPE JWT example** (JWKS-Backed JWT section)
    now mentions the NS/DB/AC routing-claim requirement
    inline, matching the per-example consistency of
    `external_idp` and `jwks_inbound` (the redundant `account`
    JWKS example is removed in this same release per item 3
    below). The preamble's ROUTING-CLAIM REQUIREMENT
    block already covers TYPE JWT (the `fn token` entry point
    decodes ALL inbound JWTs through `decode_claims_unverified`
    before dispatching to access-type-specific verifiers), but
    the per-example note improves discoverability for readers
    who jump straight to JWKS examples.
  - **`jwks_inbound`'s DURATION-omission comment** now uses the
    `:282` / `:457` dual-pointer that `external_jwt_auth` uses
    (split between the no-id claims arm where AUTHENTICATE
    runs and the with-id claims arm). Cross-example citation
    consistency.
  - **`account` + `jwks_inbound` consolidation.** After
    rev-7's `account` rewrite, the two examples were
    functionally identical (TYPE RECORD WITH JWT URL +
    AUTHENTICATE for `$token.sub`). Removed the redundant
    `account` example and reworded the surrounding prose to
    point readers at `jwks_inbound` as the canonical
    Pattern A.
  - **`verify.rs:155+` cite tightened to `:158-159`** in the
    ROUTING-CLAIM REQUIREMENT block. The actual
    `decode_claims_unverified(token)?` call is on lines
    158-159; `:155` is the `fn token` signature.
  - **`Cumulative trajectory after pass-5` table** in the
    [1.6.2] CHANGELOG entry labeled as historical /
    superseded by the pass-6 + pass-7 tables below it.

### Process notes

1 atomic doc commit (5 polish items combined per v1.6.0
single-commit fix pattern) + release commit + 1 rev-2
review-fix commit (after pass-1 4-WAY review surfaced
convergent CHANGELOG-hygiene minors).

Pass-1 4-WAY adversarial review:
- Cursor: GO              (0 CRITs / 0 IMPs / 3 minors)
- Codex:  CONDITIONAL GO  (0 CRITs / 0 IMPs / 2 minors)
- Gemini: GO              (clean — 0 findings)
- Pi:     GO              (0 CRITs / 0 IMPs / 1 minor)

Convergent minors (closed in rev-2):
- Pi M1 + Cursor M1 + Codex implicit: `:158-159` line range
  for `decode_claims_unverified` was a 2-line span where
  only `:159` is the actual call (`:158` is the describing
  comment). Tightened to `:159 (with a describing comment at
  :158)`.
- Cursor M2 + Codex M2: CHANGELOG `[1.6.3]` `auth0_jwt` bullet
  said the per-example consistency restored alignment with
  `account` / `external_idp` — but `account` was removed in
  the same release. Reworded to `external_idp` and
  `jwks_inbound` (the actual remaining peers).
- Codex M1: CHANGELOG header said "4 atomic doc commits"
  while process notes said "5 atomic doc commits"; live
  branch had 2. Header now says "1 atomic doc commit (5
  polish items combined) + release commit + rev-2 review-fix
  commit" — accurate.

Cursor M3 (routing arm cite `verify.rs:288-297` vs `292-297`
boundary) deferred — the cited block is correct in intent
(`Claims { ns: Some, db: Some, ac: Some, .. }` arm), and the
range covers the surrounding match-arm comments + the body;
tightening to `:292-297` would lose context. Tracked as a
v1.6.4 hygiene candidate if a future deeper audit reaches the
v1.6.x backlog tail.

No re-dispatch for rev-2 — convergent CHANGELOG-only minors
that are mechanical fixes against the same source the pass-1
reviewers cited; rev-2 risk profile is near-zero (no
security.md surface change beyond the one line tightening).

## [1.6.2] - 2026-05-06 — `rules/security.md` deferred-IMPORTANT clause closure (4 atomic feature commits + release commit)

### Added

- **`rules/security.md` Access-and-user clause catalog (batch 3 of
  the v1.5.x deferred-IMPORTANT cleanup).** Closes the five
  deferred bullets attributed to `rules/security.md` in the v1.5.x
  convergence notes, all verified against the v3.0.5 source tree
  at `/tmp/surrealdb-v3.0.5/surrealdb/core/src/{syn,sql,iam}/`
  rather than against the docs site (which still lags v3.0.5).
  - **`WITH REFRESH` on `TYPE RECORD`** — bearer-grant-backed
    refresh-token flow with single-use rotation; coexists with
    `WITH JWT` in either order; `DURATION FOR GRANT` controls
    refresh-token lifetime, `FOR TOKEN` controls access-token
    lifetime, `FOR SESSION` controls session ceiling. Verified
    against `core/src/syn/parser/stmt/define.rs:492-500`,
    `core/src/iam/signin.rs:279-355`,
    `core/src/iam/access.rs:107-170`, plus parser test fixtures
    `core/src/syn/parser/test/stmt.rs:911 / :1108 / :1163`.
    Includes a JS-SDK client renewal example showing the
    `{access, refresh}` token shape.
  - **`WITH JWT URL '<jwks-uri>'` (JWKS endpoint)** — alternative
    to inline `ALGORITHM <alg> KEY <key>` for both `TYPE JWT` and
    nested `WITH JWT` inside `TYPE RECORD`. Standard pattern for
    integrating with external IdPs (Auth0, Okta, Cognito, Google,
    Azure AD) that publish a JWKS document and rotate signing
    keys on their own schedule. Documents the cache-TTL
    environment variables (`SURREAL_JWKS_CACHE_EXPIRATION_SECONDS`,
    `SURREAL_JWKS_CACHE_COOLDOWN_SECONDS`,
    `SURREAL_JWKS_REMOTE_TIMEOUT_MILLISECONDS`), and the
    capabilities requirement to permit network access to the
    JWKS host. After the rev-4/rev-5 anti-pattern correction,
    the JWKS section also documents `jwks_inbound` (TYPE RECORD
    WITH JWT URL + AUTHENTICATE for federated IdP integration)
    and `credential_mint` (TYPE RECORD WITH JWT inline-KEY +
    SIGNIN + WITH ISSUER for round-trippable SurrealDB-side
    minting) as TWO separate access definitions; combining
    JWKS-verify with WITH ISSUER inline-key in a single TYPE
    RECORD definition is documented as an anti-pattern (kid
    round-trip + sub-vs-ID claim mismatch). Verified against
    `core/src/syn/parser/stmt/define.rs:1716-1722` and
    `core/src/iam/jwks.rs`, plus parser test fixtures
    `core/src/syn/parser/test/stmt.rs:703 / :731 / :762 / :792 /
    :823`.
  - **`ACCESS GRANT / SHOW / REVOKE / PURGE` statements** — the
    four top-level subcommands that manage bearer-grant lifecycle
    against a `DEFINE ACCESS … TYPE BEARER` access method.
    Documents the issue-once / hash-stored / no-recovery
    semantics for `GRANT`, the auditing surface of `SHOW { ALL |
    GRANT <id> | WHERE <cond> }`, the soft-revocation semantics
    of `REVOKE` (revoked grants stop authenticating immediately
    but remain visible until purged), and the `PURGE { EXPIRED |
    REVOKED | EXPIRED, REVOKED } [ FOR <duration> ]` physical
    deletion path with optional grace-period clause. Includes an
    end-to-end credential-rotation playbook combining all four
    subcommands. Verified against
    `core/src/syn/parser/stmt/mod.rs:108-271` and parser test
    fixtures `core/src/syn/parser/test/stmt.rs:2604 / :2621 /
    :2645-2683 / :2703-2741 / :2761-2853` (every subcommand and
    its parameter variants).
  - **`DEFINE USER PASSHASH` clause** — accept a pre-hashed
    [argon2 PHC string](https://en.wikipedia.org/wiki/PHC_string_format)
    instead of a plaintext `PASSWORD`; mutually exclusive with
    `PASSWORD` per parser bail at
    `core/src/syn/parser/stmt/define.rs:349 / :356`. Documents
    the migration-from-external-IdP use case (re-hashing an
    already-hashed string locks legacy users out) and the
    `crypto::argon2::generate($plaintext)` `RETURN`-trick for
    on-the-fly hashing on the SurrealDB side.
  - **`DEFINE USER DURATION FOR { TOKEN | SESSION } <expr>`
    clause** — per-user override of the token (default 1h per
    `define.rs:336`) and session (default unbounded per
    `core/src/sql/statements/define/user.rs:43`) expiry; both
    accepted in either order, comma-separated; either alone
    valid; `NONE` opts out of expiry on the corresponding axis
    (the v3.0.5 test suite has `DURATION FOR TOKEN NONE`
    anti-fixtures across three commented regions at
    `stmt.rs:398-407` (one DEFINE USER block), `:623-631` (one
    DEFINE ACCESS TYPE JWT block), and `:1250-1276` (three
    DEFINE ACCESS TYPE RECORD blocks at DB / ROOT / NS) —
    five anti-fixtures total, all gated by /* */ wrappers and
    calling `unwrap_err()`, so direct positive-fixture
    provenance does not exist; consumers should validate via
    round-trip signin/authenticate tests rather than parse-only
    confirmation). Application path verified at
    `core/src/iam/signin.rs:481 / :502` and
    `core/src/iam/verify.rs:106`. Includes a combined `PASSHASH +
    ROLES + DURATION + COMMENT` example showing the full v3
    `DEFINE USER` clause set.

### Process notes

Five clauses landed across four atomic feature commits in rev-1
(one for each of `WITH REFRESH`, `WITH JWT URL`, `ACCESS
subcommands`, and the combined `PASSHASH + DURATION` subsection
— the latter two clauses naturally compose on the same statement
and share a verification path, so they ship as one atomic edit
per the v1.6.0 / v1.6.1 atomic-protocol pattern).

#### Rev-2 disposition (4-WAY adversarial pass-1)

Pass-1 verdicts: Cursor NO-GO (2 CRITs / 5 IMPs / 3 minors),
Codex NO-GO (1 CRIT / 4 IMPs / 2 minors), Gemini NO-GO (3 CRITs /
2 IMPs), Pi CONDITIONAL GO (0 CRITs / 2 IMPs / 3 minors). Five
atomic rev-2 commits closed every accepted finding:

- **R1** — TYPE JWT issuance correction. Cursor C2 (CRIT, source-
  cited at signin.rs:449/:550/:686 — pure TYPE JWT has no signin
  branch) and Cursor I3 (token_duration unused on JWT
  authenticate path) both pre-existing v1.5.x latent bugs.
  Reframed the JWT FOR TOKEN/WITH ISSUER callout as
  "verification-only" with explicit pointers at the
  `at.jwt.issue` consumers (only signin.rs:275-318 inside the
  Record branch + signin_bearer at :737). Replaced the fictional
  `hybrid_jwt` mint example with the correct
  `hybrid_record TYPE RECORD WITH JWT URL + WITH ISSUER` pattern.
  Fixed the `parser/tests/stmt.rs` typo (Cursor I2).
- **R2** — JWKS Cargo feature gate (CONVERGENT CRIT, Cursor C1 +
  Codex C1). Parser accepts `URL` unconditionally, but every
  runtime arm at `verify.rs:228-240/:340-352/:412-424/:573-585/:725-737`
  is `#[cfg(feature = "jwks")]`. Default `surrealdb-server`
  features at `server/Cargo.toml:19-30` lack `jwks`. Added a
  callout citing every gated arm + the Cargo wiring + a `cargo
  build --features jwks` recipe. Also removed the unsupported
  "allow redirect targets" wording (Codex M2 — `jwks.rs:268-313`
  only checks the original URL host) and added a "test-fixture
  gap for `TYPE RECORD WITH JWT URL`" acknowledgement (Pi I1).
- **R3** — refresh-rotation citation + token-shape fix. Convergent
  IMP (Cursor I1 + Codex I2): the prior single-range
  `signin.rs:279-355` citation conflated dispatch (279-295) +
  initial issuance (352-364) with rotation (893-917 inside
  `signin_bearer`'s `BearerAccessType::Refresh` arm). Split the
  citation. Codex I2 unique catch on token shape: runtime returns
  the full bearer key (id + secret), not just the grant id;
  fixed JS-SDK example and added a "persist verbatim, do not
  split" note.
- **R4** — ACCESS section narrowings. Codex M1: PURGE grace is
  strict greater-than (`> stmt.grace.secs()`), not "at least";
  tightened to "older than". CONVERGENT IMP (Codex I1 + Cursor
  I4): GRANT FOR RECORD is database-only at runtime
  (`expr/statements/access.rs:226-234, :353-355`); replaced the
  blanket "ON NAMESPACE / ON ROOT also accepted" paragraph with
  an explicit base-scoping rubric that distinguishes
  parse-acceptance from runtime-acceptance. Cursor I5: ON is
  optional on every ACCESS subcommand; rubric flags this so
  examples-with-explicit-ON are not read as required syntax.
- **R5** — PASSHASH validation timing + DURATION fixture
  cleanup. 3-WAY CONVERGENT (Codex I4 + Gemini C2 + Pi M1):
  PASSHASH validation runs at signin (`verify.rs:945-952` —
  `PasswordHash::new(hash)`), not at define
  (`define.rs:353-358` stores verbatim). Added "store as-is,
  validate-on-use" callout. Codex I3: prior `stmt.rs:402` test-
  fixture citation pointed at a commented-out block; replaced
  with an explicit "public-test provenance is indirect"
  acknowledgement.

REJECTED findings (with rationale):

- **Gemini C1** (ACCESS ON ROOT invalid). REJECT — `parse_base()`
  at `parts.rs:445` accepts `Base::Root` and `parse_define_access`
  has no Root restriction for `TYPE BEARER FOR USER` /
  `TYPE JWT`. Convergent rebuttal: Cursor I5 confirms `parse_access`
  reads any base.
- **Gemini C3** (URL on TYPE RECORD WITH JWT invalid). REJECT —
  `parse_jwt()` at `define.rs:1716-1722` is the same function
  invoked from both `t!("JWT")` (line 454, standalone) and the
  `WITH JWT` arm of TYPE RECORD (line 484); URL works in both
  call sites. Convergent rebuttal: Codex residual-risk #2
  confirms support is structurally real; Pi I1 acknowledges the
  parser path. Both REJECTs match the v1.6.1-pass-1 pattern of
  Gemini producing wrong-direction CRITs without source access.

#### Rev-3 disposition (4-WAY adversarial pass-2)

Pass-2 verdicts: Cursor CONDITIONAL GO (0 CRITs / 2 IMPs / 2
minors), Codex CONDITIONAL GO (0 CRITs / 2 IMPs / 2 minors),
Gemini GO (0 CRITs / 0 IMPs / 1 minor), Pi NO-GO (1 CRIT / 2
IMPs / 2 minors — but Pi's CRIT was source-checked and rejected;
see below).

Five atomic rev-3 commits closed every accepted finding:

- **R1** — JWT-Based Authentication: issuer-default rubric. Codex
  pass-2 I2 caught that the prior rev-2 'WITH ISSUER KEY omitted
  defaults to HS512 with random key' prose was incomplete. Source
  chain (define.rs:1696-1708 + :1716-1722 +
  sql/access_type.rs:181-191): inline ALGORITHM verifier sets
  iss.alg = <verifier-alg> at line 1697 BEFORE the WITH ISSUER
  block runs (so bare WITH ISSUER KEY inherits the verifier alg
  for asymmetric pairs); symmetric inline verifiers also auto-pop
  iss.key (line 1707); URL/JWKS verifiers do NOT touch iss.alg
  (URL arm at 1716-1722 has no iss.alg = ... line) so iss.alg
  stays at JwtAccessIssue::default() = Hs512, REQUIRING explicit
  WITH ISSUER ALGORITHM <alg> for asymmetric minting; missing
  WITH ISSUER + missing symmetric auto-pop = AccessMethodMismatch
  at signin.rs:275-278. Replaced the single-line stale comment
  with a four-bullet rubric mapping every verifier shape to its
  resulting iss.alg / iss.key / mint behaviour. Pi pass-2 I4
  (signin_bearer fallthrough at :739) and Gemini pass-2 M1
  (WITH ISSUER ALGORITHM prose tighten) folded into the same
  commit since they touch the same prose region.
- **R2** — JWKS section. Codex pass-2 I1: rev-2's 'no fixture
  covers TYPE RECORD WITH JWT URL' was scoped to dedicated parser
  fixtures; runtime verifier exercises the shape via
  `#[cfg(feature = "jwks")]` test at verify.rs:1495-1497
  (definition :1560-1564, end-to-end :1607-1623). Narrowed.
  Pi pass-2 I3: hybrid TYPE RECORD WITH JWT URL + WITH ISSUER
  inline-key still hits the JWKS feature gate on the verification
  half; added 'gate applies even to hybrid setups' paragraph.
  Pi pass-2 M3: hybrid_record DURATION FOR TOKEN 10s was
  unrealistic; bumped to 15m / 12h.
- **R3** — refresh-token shape. Codex pass-2 M1 + Cursor pass-2
  M2: rev-2 omitted the literal 'surreal-refresh-' prefix on the
  refresh-token value. Source: expr/statements/access.rs:121-126
  + :133-134 + signin.rs:1042-1056 + :1582-1584. Doc now cites
  the prefix explicitly in prose + JS-SDK example, and warns
  against stripping or splitting client-side.
- **R4** — citation tightening. Codex pass-2 M2: stmt.rs:758 was
  wrong (close-bracket of prior no-duration case); :558 is the
  inline-key TYPE JWT DURATION FOR TOKEN fixture. Fixed. Cursor
  pass-2 I2: verify.rs PASSHASH PHC parse span tightened from
  945-952 to :947-948 specifically inside verify_pass. Pi pass-2
  M2: stmt.rs:402 commented-out block scope clarified to
  DEFINE USER specifically, with explicit pointers at active
  DEFINE ACCESS DURATION FOR TOKEN NONE fixtures at :627 / :1256
  / :1264 / :1272. Cursor pass-2 M1: stmt.rs:2620 / :2621
  disambiguated (harness vs SQL string).
- **R5** — release/disposition commit (this one). Cursor pass-2
  I1: this CHANGELOG entry's 'DEFINE USER DURATION' bullet
  itself still cited stmt.rs:402 as a positive 'exercises'
  fixture; updated to match the rev-2/rev-3 corrected narrative
  (commented-out for DEFINE USER + active DEFINE ACCESS
  fixtures).

REJECTED finding (Pi pass-2 C1):

- **Pi pass-2 C1** ('iss.alg defaults to Hs512 when WITH ISSUER
  ALGORITHM omitted; external_auth example produces a broken
  HS512-claiming token over RSA verifier'). REJECT — Pi missed
  define.rs:1697 inside the verifier ALGORITHM arm, which sets
  `iss.alg = alg` (the verifier alg) BEFORE the WITH ISSUER
  block runs at :1726+. The algorithm-mismatch check at
  :1739-1747 that Pi cited only governs WITH ISSUER ALGORITHM
  <X> overrides; it does not gate the initial inheritance from
  the verifier. For the external_auth example
  (`WITH JWT ALGORITHM RS256 KEY '<pub>' WITH ISSUER KEY '<priv>'`),
  iss.alg resolves to RS256 from the verifier line 1697, then
  WITH ISSUER's KEY arm sets iss.key = '<priv>'. iss.alg STAYS
  at RS256. The minted token correctly claims RS256 + signs with
  the RSA private key.

  Pi's claim WOULD be correct for `WITH JWT URL '<jwks>' WITH
  ISSUER KEY '<priv>'` (the URL arm at :1716-1722 has no
  `iss.alg = ...` line), in which case iss.alg stays at
  Hs512 default. This case is now explicitly documented in
  rev-3 R1's issuer-defaults rubric and was previously implicit.
  Pi caught a real semantic gap there but mis-attributed the
  bug to the wrong example.

  R1's issuer-defaults rubric absorbs Pi's underlying concern
  by enumerating exactly when explicit WITH ISSUER ALGORITHM is
  required. The external_auth example is correct as-shipped;
  the hybrid_record example already uses explicit
  WITH ISSUER ALGORITHM PS256 (correct).

  Convergent reviewer signal supports the REJECT: Cursor pass-2
  ('No contradiction found: TYPE RECORD WITH JWT … WITH ISSUER …
  still documents minting via signin.rs:275-318'), Codex pass-2
  residual-risk ('TYPE JWT verification-only is correct'), and
  Gemini pass-2 GO all cleared the JWT section without flagging
  the alleged bug. Three reviewers reading the same source
  reached the opposite conclusion from Pi.

  This is the v1.5.x-pass-3 Pi-misreads-call-path pattern
  recurring (Pi-pass-3 wrongly thought db.transaction API
  didn't exist; here Pi wrongly thought iss.alg defaulted to
  Hs512 in the verifier-set case). Pattern memory:
  `feedback_pi_unique_crit_verify_against_source.md` (this
  pattern is also covered in the v1.5.x convergence notes
  "fix-drift" section).

#### Rev-4 disposition (4-WAY adversarial pass-3)

Pass-3 verdicts: Cursor CONDITIONAL GO (0 CRITs / 1 IMP / 2
minors), Codex NO-GO (2 CRITs / 3 IMPs), Gemini GO (0 findings),
Pi NO-GO (1 CRIT / 2 IMPs / 2 minors).

Three real CRITs landed in this pass — two from Codex, one from
Pi. All survived 8 prior reviewer passes (4 pass-1 + 4 pass-2)
before pass-3 caught them. Five atomic rev-4 commits closed
every accepted finding:

- **R1-R2 combined** — JWT/JWKS section overhaul:
  - **CRIT (Pi C1)**: `$token` in SIGNIN was wrong. SIGNIN runs
    against signin variables (`$email`, `$pass`, `$id`); `$token`
    is only set in AUTHENTICATE (`sess.tk = Some(claims)` at
    `signin.rs:340-345` between SIGNIN evaluation and AUTHENTICATE
    execution). Canonical fixture at `verify.rs:2034` confirms
    AUTHENTICATE is the right clause for `$token.*` lookups.
    Both v1.6.2-introduced examples (`external_auth` +
    `hybrid_record`) corrected to use AUTHENTICATE for token-claim
    binding + SIGNIN for credential-based password auth.
    Pre-existing v1.6.2 R1 bug. Pi I2 (the prose comment that
    said "Without a SIGNIN clause, ... `$auth.id` stays unset")
    fixed to "Without an AUTHENTICATE clause" in same edit.
  - **CRIT (Codex C1)**: hybrid `TYPE RECORD WITH JWT URL +
    WITH ISSUER` mints tokens via SIGNIN, but those tokens
    cannot be re-validated through the same access method's
    JWKS verifier — SurrealDB encodes minted JWTs with bare
    `Header::new(...)` at `signin.rs:369 / :938` and
    `signup.rs:268`, omitting the `kid` claim that JWKS
    verification requires (`verify.rs:230-237` etc., bails
    "Missing token header 'kid'"). Added explicit "JWKS
    round-trip limitation" callout in the JWKS feature-gate
    block + inline NOTE in the hybrid_record example.
    Recommends `TYPE RECORD WITH JWT ALGORITHM <alg> KEY
    '<pub>'` (inline KEY, not URL) for round-trippable tokens.
  - **CRIT (Codex C2)**: JWKS section bullet still abbreviated
    to bare `WITH ISSUER KEY` which contradicts the rev-3 R1
    issuer-defaults rubric. URL/JWKS verifiers don't set
    `iss.alg` (URL arm at define.rs:1716-1722 has no
    `iss.alg = ...` line); bare `WITH ISSUER KEY` would treat
    asymmetric private keys as HMAC secrets at issue.rs:10-28.
    Rewrote the bullet to explicitly require `WITH ISSUER
    ALGORITHM <alg> KEY '<priv>'` for URL+ISSUER hybrids with
    parser-source rationale.
  - **CONVERGENT IMP (Cursor I1 + Pi I1)**: rev-3 R2's "access
    definition stops authenticating entirely" overstated the
    JWKS gate scope. For `TYPE RECORD WITH JWT URL +
    SIGNIN/SIGNUP`, credential signin still works through
    `db_access` at `signin.rs:245-410` (which never invokes the
    JWKS verifier arms); only the verification path (incoming
    third-party JWTs) fails without `--features jwks`.
    Tightened to "gate scopes to incoming-JWT verification, not
    all signin paths" with code-path citations.
- **R3** — DURATION FOR TOKEN NONE fixture-citation cleanup.
  Codex pass-3 I1: rev-3 R4 cited stmt.rs:627/:1256/:1264/:1272
  as "active fixtures" but all four are inside `/* */`
  commented-out blocks at stmt.rs:623-631 and :1250-1276 (with
  a `// TODO: Parameterization broke the guarantee that token
  duration is not none.` note explaining the suppression). Doc
  now acknowledges no positive-fixture provenance exists for
  DURATION FOR TOKEN NONE in v3.0.5; recommends round-trip
  validation rather than parse-only confirmation.
- **R4** — refresh-token citation chain labels. Codex pass-3
  I2 + Cursor pass-3 M1+M2: access.rs:121-126 was labeled
  'create_grant dispatch' but it's actually `new_grant_bearer`
  (the `format!("{prefix}-{id}-{secret}")` construction).
  `create_grant` begins at :181, record-refresh invocation is
  at :237-242. signin.rs:1582-1584 was labeled 'runtime regex'
  but is an integration-test assertion; production validation
  is `validate_grant_bearer` at signin.rs:1042-1056. Rewrote
  the citation chain with correct labels.
- **R5** — ES512 algorithm runtime caveat + line-citation
  tightening. Codex pass-3 I3: ES512 maps to ES384 at runtime
  (verify.rs:47-48 + mod.rs:46-47); split ES256/ES384 from
  ES512 in the algorithms table + added an explicit caveat.
  Pi pass-3 M1: SYMMETRIC bullet cited line 1707 but the
  `iss.key = key` assignment is on :1703; tightened to cite
  both lines.
- **R6** (this commit) — CHANGELOG pass-3 disposition + the
  pre-existing CHANGELOG `stmt.rs:402` citation drift first
  flagged in Cursor pass-2 I1; the previous rev-2 commit fixed
  it via "or :627 / :1256 / :1264 / :1272" alternates which
  themselves turned out to be commented-out (Codex pass-3 I1).
  Final CHANGELOG narrative now matches the rev-4 R3
  rule-file correction: no positive-fixture provenance, gated
  blocks only.

NO REJECTIONS this pass — all four pass-3 CRIT/IMP-level
findings traced to real source; Pi pass-2's rejected C1 still
holds (Cursor pass-3 cross-check appendix B + Codex pass-3
residual risk + Gemini pass-3 GO all confirm).

#### Rev-5 disposition (4-WAY adversarial pass-4)

Pass-4 verdicts: Cursor NO-GO (1 CRIT / 2 IMPs / 2 minors),
Codex NO-GO (1 CRIT / 2 IMPs / 1 minor), Gemini NO-GO (1 CRIT
/ 0 IMPs), Pi CONDITIONAL GO (0 CRITs / 1 IMP / 2 minors).

Pass-4 surfaced 3 real CRITs — pattern continues from pass-3
(cumulative ~17 source-cited findings across the four passes).
Three atomic rev-5 commits closed every accepted finding:

- **R1** — JWT-Based Authentication: split external_auth into
  Pattern A (external_jwt_auth, authenticate-only) +
  Pattern B (credential_auth, SIGNIN-mint-roundtrippable).
  Closes:
  - **CONVERGENT CRIT** (Gemini C1 + Cursor I2 + Codex I1 +
    Pi I1): rev-4 external_auth had WITH ISSUER KEY +
    DURATION FOR TOKEN 1h but NO SIGNIN, making the issuance
    machinery unreachable per signin.rs:296-437
    (AccessRecordNoSignin error if SIGNIN missing).
  - **UNIQUE CRIT** (Codex C1): rev-4 prose claimed
    'no AUTHENTICATE -> $token-only permissions' — wrong.
    Source: verify.rs:177-245 binds record from token's `id`
    claim if present; verify.rs:464 bails
    AccessMethodMismatch otherwise. Real rule documented in
    the new prose preamble.
- **R2** — JWKS section: replaced hybrid_record with two
  separate access definitions (jwks_inbound for federated IdP,
  credential_mint for SurrealDB-side mint) plus an explicit
  ANTI-PATTERN callout. Closes:
  - **UNIQUE CRIT** (Cursor C1): rev-4 hybrid_record had
    AUTHENTICATE matching `$token.sub` after credential SIGNIN,
    but credential SIGNIN mints tokens with `$token.ID`
    (uppercase, from Claims { id: Some(rid.to_sql()), ..
    Claims::default() } at signin.rs:314-324); default sub:
    None at token.rs:243; into_claims_object at
    token.rs:289-345 inserts 'ID' for the id claim and only
    inserts 'sub' when Claims.sub is Some. So rev-4
    hybrid_record's AUTHENTICATE predicate matched the wrong
    key on the credential path.
  - **CARRY-OVER from Codex pass-3 C1**: SurrealDB-minted
    tokens use bare Header::new(...) at signin.rs:369/:938
    + signup.rs:268 which omits the kid claim, so JWKS
    verification round-trip fails. Anti-pattern callout
    documents both reasons (sub vs ID + kid round-trip).
- **R3** — Lower IdP integration example + ES512 caveat
  tighten + four-blocks miscount + access.rs:237-242 label.
  Closes:
  - **UNIQUE** (Codex I2 — pre-existing v1.5.x latent): the
    'JWT Token Integration with External Identity Providers'
    lower example also had the no-AUTHENTICATE shape problem.
    Rewrote to use AUTHENTICATE for sub mapping + dropped
    WITH ISSUER (matches surrounding prose's authenticate-only
    intent).
  - **UNIQUE** (Codex M1): rev-4 R5 ES512 caveat overstated
    inbound-header acceptance. Tightened to scope the claim
    to 'configured ALGORITHM ES512 verifies and emits ES384'
    only.
  - **UNIQUE** (Cursor I1 + M2): rev-4 'all four blocks'
    miscount for DURATION FOR TOKEN NONE fixtures. Actually
    three commented regions contain five anti-fixtures.
    Tightened wording in both rule file AND CHANGELOG.
  - **UNIQUE** (Pi M1): rev-4 R4 labeled access.rs:237-242
    as 'record-refresh call site'; actually it's the Base::Db
    enforcement guard inside create_grant. Relabeled.

NO REJECTIONS this pass — all four reviewers' CRIT/IMP
findings traced to real source. Pi pass-2's earlier rejected
C1 still holds (multiple cross-pass confirmations).

#### Rev-6 disposition (4-WAY adversarial pass-5)

Pass-5 verdicts: Cursor NO-GO (2 CRITs / 3 IMPs / 1 minor),
Codex NO-GO (1 CRIT / 2 IMPs / 2 minors), Gemini GO (0 findings),
Pi CONDITIONAL GO (0 CRITs / 2 IMPs / 0 minors).

3 real CRITs landed in this pass — same fix-drift pattern
documented in earlier disposition entries. Three atomic rev-6
commits closed every accepted finding:

- **R1** — Parser-order fix: 3 examples don't parse.
  - **CRIT (Codex pass-5 C1)**: rev-5 examples external_jwt_auth,
    jwks_inbound, and external_idp put AUTHENTICATE BEFORE
    WITH JWT, which fails to parse in v3.0.5. Source:
    parse_define_access at define.rs:415-573 has an outer loop
    matching top-level clauses (TYPE at :456, AUTHENTICATE at
    :545); the TYPE arm delegates to a TYPE RECORD subparser
    (:456-507) with two inner loops (SIGNUP/SIGNIN, then
    WITH JWT/REFRESH). If AUTHENTICATE comes before WITH JWT,
    the outer loop consumes AUTHENTICATE, then sees WITH and
    has no match arm -> exits, leaving WITH JWT unconsumed.
    Canonical fixture order at verify.rs:2029-2037 confirms
    the working shape: `TYPE RECORD ... SIGNIN ... WITH JWT ...
    AUTHENTICATE ... DURATION ...`. Reordered all three
    examples + added inline parser-cited comments in each.
  - **CRIT (Cursor pass-5 C2)**: Pattern A (external_jwt_auth)
    comment cited `signin.rs:340-345` for `$token` availability,
    but that's the SIGNIN-mint path. Pattern A has no SIGNIN —
    clients call db.authenticate(). On the authenticate path,
    sess.tk is populated at verify.rs:256-263 (claims arm with
    id) or :432-440 (claims arm without id), NOT signin.rs.
    Updated the comment to cite the correct authenticate-path
    locations.
  - **UNIQUE (Codex pass-5 I2)**: jwks_inbound had
    `DURATION FOR TOKEN 15m` but the doc itself documents that
    FOR TOKEN is unused on the authenticate path for
    AccessType::Record without minting. Removed the unused
    clause + explanatory comment.
- **R2** — access.rs line-label correction.
  - **CONVERGENT CRIT (Cursor pass-5 C1 + Codex pass-5 I1)**:
    rev-3 R4 first cited access.rs:237-242 as 'record-refresh
    call site'; Pi pass-3 corrected to 'Base::Db enforcement
    guard'; rev-5 R3 propagated that label. Source verification
    at v3.0.5 expr/statements/access.rs:226-242 shows BOTH
    labels are wrong:
    - :231-234 IS the Base::Db enforcement guard (specifically
      :233's `ensure!(matches!(base, Base::Db),
      Error::DbEmpty);`)
    - :237-242 is the bearer-presence check + new_grant_bearer
      invocation that follows the guard
    Final fix splits the citation: :231-234 for the guard,
    :237-242 for the bearer + grant construction.
  - This is a multi-pass label-drift pattern. Pi pass-2 I1 / Pi
    pass-3 M1 / Pi pass-4 M1 / Pi pass-5 PASS-on-F all gave
    different labels for :237-242 — Pi mis-attributes
    successive lines without source-grep. Recorded as a
    parallel pattern to the v1.5.x Pi-pass-3 db.transaction
    misread.
- **R3** — JWKS ops bullet + preamble ALGORITHM scope + lower
  IdP arm citation.
  - **CONVERGENT IMP (Cursor pass-5 I1 + Pi pass-5 I1)**: JWKS
    'Operational notes' bullet still recommended single combined
    TYPE RECORD WITH JWT URL + WITH ISSUER pattern,
    contradicting the rev-5 anti-pattern callout. Rewrote to
    redirect to the two-pattern approach (jwks_inbound +
    credential_mint).
  - **UNIQUE (Pi pass-5 I2)**: rev-5 preamble parenthetical
    said `ALGORITHM token in WITH ISSUER is REQUIRED for
    asymmetric / JWKS verifier paths`. Per define.rs:1697,
    inline asymmetric verifiers DO inherit iss.alg; only
    URL/JWKS verifiers need explicit `ALGORITHM`. Narrowed.
  - **UNIQUE (Cursor pass-5 I2)**: lower IdP example cited
    verify.rs:246-288 (first claims arm, with id) for
    'no-encode authenticate-only' behaviour; inbound IdP JWTs
    mapped via `$token.sub` follow the SECOND claims arm at
    ~verify.rs:401-462. Retargeted the citation.
- **R4** (this commit) — CHANGELOG pass-5 disposition +
  cumulative trajectory table extension.

NO REJECTIONS this pass. Pi pass-5's PASS-on-F (claiming
:237-242 was the Base::Db guard) was wrong by the same source
check Cursor C1 + Codex I1 surfaced; the convergent
Cursor+Codex finding overrode Pi's PASS verdict. Pi pass-2 C1
remains rejected (cross-pass confirmation).

#### Cumulative trajectory after pass-5 (historical — superseded by pass-6 + pass-7 tables below)

| Pass | Cursor | Codex | Gemini | Pi | Real CRITs | Real IMPs | Notes |
|------|--------|-------|--------|----|------|-----------|-------|
| 1 | NO-GO | NO-GO | NO-GO | COND | 2 | 5 | jwks gate + TYPE JWT signin path |
| 2 | COND | COND | GO | NO-GO* | 0 | 4 | *Pi C1 rejected (parser misread) |
| 3 | COND | NO-GO | GO | NO-GO | 3 | 4 | kid round-trip + WITH ISSUER KEY in JWKS bullet + $token in SIGNIN |
| 4 | NO-GO | NO-GO | NO-GO | COND | 3 | 4 | external_auth no-SIGNIN + hybrid_record sub vs ID + no-AUTHENTICATE prose |
| 5 | NO-GO | NO-GO | GO | COND | 3 | 4 | parser-order in 3 examples + access.rs label drift + signin.rs:340-345 wrong cite |

11 real CRITs found-and-fixed across five passes. Multiple
recurring patterns (access.rs:237-242 label drift across passes
2-5; Pi misreads multi-arm match control flow; doc-vs-CHANGELOG
drift on stmt.rs:402 across passes 2-3-4-5). Two Gemini CRITs
rejected with parser-cited rebuttals across the cycle.

#### Rev-7 disposition (4-WAY adversarial pass-6)

Pass-6 verdicts: Cursor NO-GO (1 CRIT / 1 IMP / 2 minors),
Codex NO-GO (4 CRITs / 0 IMPs / 1 minor), Gemini GO (0
findings), Pi CONDITIONAL GO (0 CRITs / 2 IMPs / 2 minors —
all CHANGELOG-hygiene only).

5 real CRITs landed in this pass. Five atomic rev-7 commits
closed every accepted finding:

- **R1** — NS/DB/AC routing-claim requirement.
  - **CRIT (Codex pass-6 C1)**: inbound JWTs MUST carry
    `ns`/`db`/`ac` routing claims (or aliases per
    `core/src/iam/token.rs:248-275` — uppercase or full URI
    forms accepted) for SurrealDB to match the database-access
    arm at `verify.rs:288-297`. Without them, validation
    falls through to InvalidAuth at `:824-825` BEFORE the
    access method's verifier or AUTHENTICATE clause runs.
    The pre-existing v1.5.x `external_idp` example payload
    showed only `sub/email/roles/tenant_id/exp` — none of
    which routes. Added a ROUTING-CLAIM REQUIREMENT block to
    the JWT-Based Authentication preamble + updated the lower
    IdP example payload to include `ns/db/ac/sub/...` with
    inline notes pointing at IdP custom-claim mechanisms
    (Auth0 Actions, Okta inline hooks, Cognito pre-token
    Lambda, Azure AD claim mapping).
- **R2-R3** — `account` JWKS example shape fix + Pattern A
  citation tightening + GRANT bullet line range.
  - **CRIT (Codex pass-6 C2)**: pre-existing v1.5.x `account`
    JWKS mini-example had `TYPE RECORD WITH JWT URL` with no
    AUTHENTICATE and `DURATION FOR TOKEN 15m`. Without
    AUTHENTICATE, inbound IdP JWTs lacking SurrealDB `id`
    fall through to AccessMethodMismatch at `verify.rs:464`;
    DURATION FOR TOKEN is unused on the authenticate path
    for AccessType::Record without minting. Rewrote with
    AUTHENTICATE for sub mapping + dropped FOR TOKEN.
  - **CRIT (Cursor pass-6 C1)**: rev-5 Pattern A example
    cited `verify.rs:394` for DURATION FOR SESSION — that's
    the AccessType::Jwt branch, not AccessType::Record. The
    Record arm uses `:282` (claims with id) or `:457` (claims
    without id). Corrected both citations + relabeled the
    comment to 'AccessType::Record authenticate path' (also
    closes Codex pass-6 M1).
  - **IMP (Cursor pass-6 I1)**: Pattern A's sess.tk citation
    listed `:256-263 (claims arm with id) or :432-440 (claims
    arm without id)` implying both are equally common. For
    typical IdP-`sub` JWTs (no SurrealDB id), `:432-440` is
    the path; reordered + framed `:256-263` as the
    conditional case.
  - **MINOR (Cursor pass-6 M1)**: GRANT FOR RECORD bullet
    cited `:226-234`; per source, `:226-230` is the unrelated
    Jwt grant rejection and the actual guard is `:231-234`
    + `:353-355`. Tightened with explicit per-arm labels.
- **R4** — CHANGELOG hygiene fixes.
  - **CRIT (Codex pass-6 C3)**: top-of-file v1.6.2 'Added'
    bullet for `WITH JWT URL` still said the doc 'documents
    the hybrid pattern combining JWKS-verify with WITH ISSUER
    inline-key issuance' — contradicts current security.md
    which redirects to two patterns + labels the combined
    shape an anti-pattern. Rewrote bullet to reference
    `jwks_inbound` + `credential_mint` as separate definitions
    with the anti-pattern callout.
  - **CRIT (Codex pass-6 C4 + Pi pass-6 I1+I2+M1+M2)**: the
    rev-3 R5 disposition's 'Cumulative trajectory after
    pass-4' table was retained at the bottom of the [1.6.2]
    section AFTER the rev-5 R4 added an updated 'Cumulative
    trajectory after pass-5' table, creating a duplicate
    that contradicted itself ('Eight real CRITs' vs '11 real
    CRITs'). Same doc-vs-CHANGELOG drift class as the
    pass-2/pass-3 stmt.rs:402 saga — recorded as a recurring
    pattern. Removed the stale table + 'Eight real CRITs'
    paragraph. Restructured 'Reviewer-blind-spot pattern'
    + 'verification escalator' prose under explicit headings
    that don't conflict with the pass-5 trajectory section.
- **R5** (this commit) — CHANGELOG pass-6 disposition + new
  trajectory row.

NO REJECTIONS this pass. Pi pass-2 C1 still rejected
(seventh-pass confirmation).

#### Cumulative trajectory after pass-6

| Pass | Cursor | Codex | Gemini | Pi | Real CRITs | Real IMPs |
|------|--------|-------|--------|----|------|-----------|
| 1 | NO-GO | NO-GO | NO-GO | COND | 2 | 5 |
| 2 | COND | COND | GO | NO-GO* | 0 | 4 |
| 3 | COND | NO-GO | GO | NO-GO | 3 | 4 |
| 4 | NO-GO | NO-GO | NO-GO | COND | 3 | 4 |
| 5 | NO-GO | NO-GO | GO | COND | 3 | 4 |
| 6 | NO-GO | NO-GO | GO | COND | 5 | 1 |

*Pi pass-2 C1 rejected with parser-cited rebuttal (see Rev-3
disposition above).

16 real CRITs found-and-fixed across six passes. Pass-6's
spike to 5 CRITs reflects two pre-existing v1.5.x latent bugs
finally surfacing (NS/DB/AC routing claims missing from IdP
examples; `account` JWKS example shape) plus one new
parser-arm citation drift introduced by rev-5 (Pattern A
verify.rs:394 vs :282/:457). Per the v1.5.x convergence
pattern, expect ratification within 1-2 more passes; remaining
churn should be cite-line drift which Codex + Cursor catch
reliably.

#### Pass-7 ratification (4/4 GO+CONDITIONAL GO with 0 CRITs)

Pass-7 verdicts:

| Reviewer | Verdict | CRITs | IMPs | Minors |
|---|---|---|---|---|
| Pi       | **GO**         | 0 | 0 | 1 (auth0_jwt NS/DB/AC mention) |
| Cursor   | CONDITIONAL GO | 0 | 2 (auth0_jwt cross-reference + jwks_inbound cite consistency) | 2 |
| Codex    | CONDITIONAL GO | 0 | 1 (CHANGELOG hygiene — pass-5 table archival) | 2 |
| Gemini   | CONDITIONAL GO | 0 | 2 (account/jwks_inbound consolidation + jwks_inbound NS/DB/AC) | 2 |

Per `~/CLAUDE.md` aggregation rule: "CONDITIONAL GO w/ no CRIT
= ship if maintainer accepts IMPs as deferred." Pi achieved
full GO; remaining IMPs across the other three reviewers are
documentation-polish (cross-reference cite consistency,
example consolidation, single line-anchor tightening from
:155+ → :158-159) with no source-correctness contradictions.

**v1.6.2 ratified at pass-7.** Convergence trajectory:

| Pass | Real CRITs | Verdicts |
|------|------------|----------|
| 1 | 2 | 1 NO-GO + 2 NO-GO + 1 NO-GO + 1 COND |
| 2 | 0 | 2 COND + 1 GO + 1 NO-GO* |
| 3 | 3 | 1 COND + 1 NO-GO + 1 GO + 1 NO-GO |
| 4 | 3 | 3 NO-GO + 1 COND |
| 5 | 3 | 2 NO-GO + 1 GO + 1 COND |
| 6 | 5 | 2 NO-GO + 1 GO + 1 COND |
| **7** | **0** | **3 COND + 1 GO** |

16 cumulative real CRITs found-and-fixed across 7 passes;
2 Gemini CRITs rejected with parser-cited rebuttals. Trajectory
matches v1.5.x convergence pattern (rev-N closes pass-(N-1)
findings while introducing 1-3 new bugs from fix surgery).
Rev-7's edit was precisely scoped (5 commits) and pass-7
introduced ZERO new bugs from surgery — the cleanest pass.

#### Deferred to v1.6.3 (pass-7 IMPs and minors)

- Add NS/DB/AC routing-claim mention to `auth0_jwt` TYPE JWT
  example for per-example consistency (currently relies on
  global preamble block).
- Align `jwks_inbound`'s session-duration comment with the
  `:282` / `:457` dual-pointer used in `external_jwt_auth`.
- Consolidate the `account` + `jwks_inbound` examples in the
  JWKS section (currently functionally identical after rev-7's
  `account` rewrite).
- Tighten `verify.rs:155+` cite in the routing-claim block to
  `:158-159` (anchor where `decode_claims_unverified` is
  called).
- Archive or label the `Cumulative trajectory after pass-5`
  table as historical (superseded by the pass-6 table below).

None of these affect runtime correctness; all are documentation
polish suitable for a v1.6.3 batch.

#### Reviewer-blind-spot doctrine (carried forward from earlier passes)

Pi pass-3 first noted that the `external_auth` example's `$token`
in SIGNIN bug "survived 8 reviewer passes" before pass-3 caught
it. The pattern: every reviewer verified JWT *issuance* semantics
(iss.alg, iss.key, AccessMethodMismatch fallthroughs at
:449/:550/:686) and parser-grammar acceptance, but none traced
what `$token` actually resolves to inside SIGNIN vs AUTHENTICATE.
The canonical test fixture at `verify.rs:2034` would have
disambiguated this on first inspection. The same pattern recurred
at pass-6 with Codex's NS/DB/AC routing-claim catch — five
review passes verified parser correctness without checking that
inbound JWTs actually carry the claims `verify.rs:288-297`
requires for routing.

Doctrine for future cycles: every example in a doc should be
walked end-to-end at the SurrealQL evaluation level — "at each
evaluation point, what do the session parameters actually
contain? what claims does the JWT need to route?" — not just
"does the example parse?". A parse-clean example can still be
semantically broken (wrong clause for a given parameter, missing
routing claims, wrong base for a given access type, wrong
algorithm relationship between verifier and issuer). Memory
file `feedback_walk_examples_end_to_end.md` carries the doctrine
with two recorded instances.

#### Verification escalator (v1.6.x)

This release extends the v1.6.0 / v1.6.1 verification escalator —
every claim grounded in a parser-source line range plus a parser
test-fixture line plus a runtime path where applicable, so any
reviewer can trace a clause back to the v3.0.5 commit that
defined it. Remaining v1.5.x deferred IMPORTANTs after v1.6.2:
surrealql.md data-type / DEFINE API / DEFINE CONFIG / INFO FOR
INDEX|USER variants; vector-search.md HASHED_VECTOR / MINKOWSKI /
jaccard-pearson similarity-function examples; performance.md
TLS flags and SURREAL_HNSW_CACHE_SIZE env-var; graph-queries.md
sub-SELECT graph clauses; data-modeling.md illustrative-edge
consistency.

## [1.6.1] - 2026-05-06 — Function namespace catalog (10 atomic feature commits + release commit, plus rev-2 review-fix commits)

### Added

- **`rules/surrealql.md` Function-namespace catalog (batch 2 of the
  v1.5.x deferred-IMPORTANT cleanup).** Closes the seven function
  namespaces flagged as under-documented in the v1.5.x convergence
  notes plus three previously unrelated extensions, all verified
  against the v3.0.5 source tree at
  `/tmp/surrealdb-v3.0.5/surrealdb/core/src/fnc/` rather than against
  the docs site (which lags v3.0.5).
  - **`encoding::*` (4 functions)** — base64::{encode,decode} (with
    optional padding flag and padding-insensitive decoding) and
    cbor::{encode,decode}. Explicit "no other formats exist"
    callout to prevent symmetric fabrication of `encoding::hex`,
    `encoding::base32`, etc.
  - **`bytes::*` (1 function)** — only `bytes::len`. The v1.5.x
    deferral list claim of an under-documented bytes namespace was
    OVERSTATED; the upstream module is 7 LOC. Explicit "do NOT
    assume it mirrors `string::*`" callout.
  - **`set::*` (24 functions)** — largest namespace addition.
    Documents the 17 sync + 7 async / closure-based functions, with
    three critical semantic notes at the top: `set::difference` is
    SYMMETRIC (`A △ B`) — NOT the relative complement (use
    `set::complement` for `A \ B`). The `array::*` namespace uses
    the SAME convention: `array::difference` is also symmetric
    difference (with multiset-pairing semantics for duplicates per
    `core/src/val/array.rs:310-323`), and `array::complement` is
    `A \ B`. Sets are stored in Rust's `BTreeSet<Value>` and
    iterated in `Value::Ord` order — `at` / `first` / `last` /
    `slice` and the closure-based traversals visit elements in
    that order. Explicit "no `set::sort`, `set::distinct`,
    `set::reverse`, `set::concat`, `set::sample`, `set::is_subset`,
    `set::is_superset`" callout. (The original v1.5.x deferral list
    claim that `set::difference` and `array::difference` use
    OPPOSITE conventions was wrong; rev-2 review pass corrected the
    cross-section narrative against `core/src/fnc/set.rs:68-76` +
    `core/src/val/array.rs:310-323`. Pre-existing
    `array::difference([1,2,3], [2,3,4])` example was also fixed
    from `[1]` to `[1, 4]` to match the actual symmetric-difference
    return value.)
  - **`sequence::*` (1 function)** — only `sequence::nextval`. The
    v1.5.x deferral list claim was OVERSTATED. Documents the
    `REMOVE SEQUENCE; DEFINE SEQUENCE` reset pattern (since no
    `sequence::reset` / `sequence::current` / `sequence::peek`
    exists).
  - **`schema::*` (1 function)** — only `schema::table::exists`.
    The v1.5.x deferral list claim was OVERSTATED. Notes the
    `Action::View` IAM requirement and shows the
    `IF !exists THEN DEFINE` guard idiom.
  - **`file::*` (13 functions, experimental)** — registry rows
    split across `core/src/fnc/mod.rs:239-240` (2 sync inspectors:
    `file::bucket`, `file::key`) and `core/src/fnc/mod.rs:602-612`
    (11 async I/O functions). Every row carries the `exp(Files)`
    macro prefix; the capability check resolves at function
    DISPATCH time (not at SurrealQL parse time, per
    `core/src/fnc/mod.rs:114-133`). Functions only resolve when the
    server runs with `--allow-experimental Files`. Documents put /
    put_if_not_exists / get / head / exists / delete / list / copy
    / copy_if_not_exists / rename / rename_if_not_exists plus the
    sync inspectors `bucket` / `key`. The `*_if_not_exists` variants
    are NO-OPS when the destination key already exists (verified
    against `core/src/buc/controller.rs:97-216`); they do NOT
    error. `file::head` returns `{ updated, size, file }` per
    `core/src/buc/store/mod.rs:35-52` (no `etag` field exists in
    v3.0.5). Calls out the asymmetric `file::list(bucket: string,
    options?: object)` signature and the cross-bucket
    `file::copy(file, file)` form. Explicit "NO `file::move`"
    callout. The example `DEFINE BUCKET` syntax uses bare
    `READONLY` (no boolean operand) per
    `core/src/syn/parser/stmt/define.rs:1378-1380`.
  - **`api::*` (7 functions, two usage modes)** — split into
    `api::invoke` (callable from regular SurrealQL, server-side
    dispatch with no HTTP round-trip) and the six middleware-only
    functions (`api::req::body`, `api::res::body`,
    `api::res::status`, `api::res::header`, `api::res::headers`,
    `api::timeout`) that take an implicit `next` from the
    `DEFINE API ... MIDDLEWARE` chain and are not free-standing.
    Body-strategy enumeration: auto / json / cbor / flatbuffers /
    plain / bytes / native. `api::res::status` validates 100..=599.
    `api::res::headers` (the MAP form) accepts `NONE` map values to
    remove a header; `api::res::header` (the single-pair form) does
    NOT — its second argument is `Optional<String>` so passing an
    explicit `NONE` is a type error and removal must be done by
    OMITTING the second argument.
- **`rules/surrealql.md` top-level `sleep(duration)` function.**
  Registered as the bare name `"sleep"` at
  `core/src/fnc/mod.rs:639` — NOT under any namespace. Calls out the
  CLAMP-by-context-timeout behaviour: e.g.
  `CREATE timeout_probe SET slept = sleep(10s) TIMEOUT 1s;` errors
  out via the surrounding `TIMEOUT` clause after ~1s rather than
  completing the 10-second sleep. Note that `RETURN` itself does
  NOT parse a `TIMEOUT` clause (per
  `core/src/syn/parser/stmt/mod.rs:566-575`); attach `TIMEOUT` to
  a statement that does (`SELECT`, `CREATE`, `UPDATE`, `DELETE`,
  `RELATE`, `INSERT`). The function is implemented via
  `tokio::time::sleep`, so it does NOT block the async runtime.
- **`rules/surrealql.md` extends `### Search Functions` with three
  previously undocumented entries.** `search::analyze(analyzer,
  text)` for tokenizer preview; `search::rrf(results, limit,
  rrf_constant?=60)` for Reciprocal Rank Fusion;
  `search::linear(results, weights, limit, norm: 'minmax' |
  'zscore')` for weighted-linear-combination fusion with
  score-extraction priority `distance → ft_score → score → rank`.
  Both fusion functions document their argument-validation errors
  (`InvalidFunctionArguments`) per `core/src/fnc/search.rs`.
- **`rules/surrealql.md` extends `### Session Functions` from 6 to
  8.** Adds `session::ac()` (current access-method name set during
  authentication) and `session::rd()` (record-access record
  reference, e.g. `user:tobie` when signed in via
  `DEFINE ACCESS ... FOR RECORD`). Both are particularly useful
  inside `DEFINE ACCESS ... PERMISSIONS` and
  `DEFINE TABLE ... PERMISSIONS` clauses.

### Process notes

- **v1.6.0 lesson applied first.** Before drafting docs, every
  claimed namespace was verified against the v3.0.5 source rather
  than against the docs site or the v1.5.x deferral list. Three of
  the seven listed namespaces (`bytes`, `sequence`, `schema`) turned
  out to be SINGLE-FUNCTION namespaces, not the multi-function
  namespaces the deferral list implied — the same failure mode as
  the ALTER target-list fabrication v1.6.0 just fixed (taking a list
  claim at face value instead of going to the parser/registry). Each
  section now includes an explicit "what is NOT registered" callout
  for the most plausible-looking absent functions.
- **Atomic commits.** Each namespace landed in its own commit
  citing the registry line numbers and module LOC so future audits
  (or a 4-WAY adversarial review) can verify each addition
  independently.

## [1.6.0] - 2026-05-06 — ALTER target-list fabrication fix

### Fixed

- **`rules/surrealql.md` ALTER section: phantom 10-target claim
  removed.** v1.5.7 through v1.5.10 introduced and carried forward
  the claim that v3 supports `ALTER` across **seventeen** targets
  (`SYSTEM`, `NAMESPACE`, `DATABASE`, `TABLE`, `EVENT`, `INDEX`,
  `FIELD`, `PARAM`, `SEQUENCE`, `BUCKET`, `ANALYZER`, `FUNCTION`,
  `USER`, `ACCESS`, `CONFIG`, `API`, `MODULE`) and softened the
  underdocumentation by saying the "remaining ten" follow the same
  general clause shape. Both halves of that claim are wrong:
  v3.0.5's parser dispatch (`core/src/syn/parser/stmt/alter.rs`
  lines 17-26) accepts exactly seven keywords (`SYSTEM`, `NAMESPACE`,
  `DATABASE`, `TABLE`, `INDEX`, `FIELD`, `SEQUENCE`) and rejects
  every other token with `unexpected!(self, next, "a alter
  statement keyword")`. The seven `core/src/sql/statements/alter/`
  module files (`database.rs`, `field.rs`, `index.rs`, `namespace.rs`,
  `sequence.rs`, `system.rs`, `table.rs`) confirm this — there are
  no `event.rs`, `param.rs`, `bucket.rs`, etc. ALTER variants in
  v3.0.5. The corrected section now states the seven-target reality
  explicitly, calls out the ten unsupported keywords as parse
  errors, and instructs readers to use `REMOVE` + `DEFINE` for the
  unsupported objects.

- **Wrong line reference in the same section.** Header text claimed
  the dispatch lived at `alter.rs` lines 26-44; actual location is
  lines 17-26. Corrected.

- **`notes/v1.5.x-convergence.md` deferral list: same fabrication
  removed.** The v1.6.x deferral catalog inherited the phantom
  10-target claim and listed it as "10 undocumented ALTER targets"
  to be added later. Replaced with a corrective note explaining
  the v3.0.5 reality and recording the verification blind spot
  (Pi/Codex passes audited clause shapes inside each ALTER
  subsection but did not audit the intro paragraph's target list).

### Verification blind spot — lesson

Across ten Pi+DeepSeek-V4-Pro:xhigh adversarial passes the
fabricated 17-target list survived because the auditors verified
the *clause shape* of each documented ALTER variant (`ALTER TABLE …
COMPACT;` parses, `ALTER FIELD … DEFAULT …` parses, etc.) but did
not verify that the *intro paragraph's target list itself* matched
the parser dispatch. v1.5.8's pass-8 surgery caught two phantom
clauses (`ALTER INDEX … COMPACT`, `ALTER SEQUENCE … RESTART`) but
the surrounding "seventeen targets" claim slipped through. Future
audits should treat list-of-features paragraphs as their own
verification target, not just the example blocks below them.

### Repo housekeeping

- Closed issue #3 (v1.4.1 deferral tracker) per its own closure
  criterion (v1.5.x stable shipped at v1.5.10).
- Closed two stale Cursor draft PRs (#1, #2) — both touched
  `AGENTS.md` for Cursor Cloud onboarding, both 5+ weeks unmoved
  in draft state. If Cursor Cloud onboarding is wanted, a fresh
  focused PR against current `main` is cleaner than reviving
  either branch.
- Opened milestone v1.6.0 to track the remaining (corrected)
  deferral catalog from `notes/v1.5.x-convergence.md`.

## [1.5.10] - 2026-05-05 — v1.5.x stable

### v1.5.x cycle declared stable

A tenth Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same six
rules audited in pass-9 returned **2 GO + 4 CONDITIONAL GO + 0
NO-GO** with **0 CRITs** total — the convergence target. Per
`~/CLAUDE.md` "CONDITIONAL GO w/ no CRIT = ship if maintainer accepts
IMPs as deferred", v1.5.x is declared stable.

v1.5.10 closes a single convergent IMPORTANT bug surfaced by both
the data-modeling.md and graph-queries.md pass-10 reports:
**`INTERSECT` is not a valid SurrealQL v3 expression operator.**
v3 array set-operations are function calls (`array::intersect()`,
`array::union()`, `array::complement()`), not infix keywords. Two
example queries used `INTERSECT` as if it were an infix operator:

- `rules/data-modeling.md` line 440 (Social Network Pattern §"Mutual
  follows"): `SELECT ->follows->user INTERSECT <-follows<-user AS
  mutual …` → corrected to `SELECT array::intersect(->follows->user,
  <-follows<-user) AS mutual …`.
- `rules/graph-queries.md` line 572 (Recommendation Engine):
  `count(->likes->product INTERSECT $my_likes) AS overlap` →
  corrected to `count(array::intersect(->likes->product,
  $my_likes)) AS overlap`.

A repo-wide grep confirms no other `INTERSECT` / `EXCEPT` infix
usages remain (`INTERSECTS` is a separate, upstream-valid geometry
operator and is unaffected).

### v1.5.x convergence trajectory

```
Pass:    1   2    3   4   5   6   7   8   9  10
CRITs:  21   7   15   6   6   5   1   2   5   0
```

**Total: 70 CRITs found-and-fixed across ten passes.** Cycle ran
2026-05-05 in a single ~7-hour wall-clock pass with 6 parallel Pi
processes per pass.

Pass-3 was the high-water mark (15 CRITs) because it added
`rules/surrealql.md` as a sixth target — the foundational language
reference's first dedicated full-file Pi pass. Post-pass-3, the
trend is monotone-decreasing-with-noise; pass-9's uptick reflected
v1.5.8 ALTER surgery fix-drift (2 phantom-clause CRITs) plus 2
cross-rule incomplete-fix CRITs surfaced by the pass-9 cross-file
gap analysis. Pass-10 confirmed the v1.5.9 corrections held + the
cycle has exhausted the high-confidence correctness surface.

The single most consequential correction was the v1.5.3 HNSW LM
parameter rewrite — the v1.5.1 fix had labelled LM as "Minkowski
distance order" based on docs-only inspection; pass-3 verified
against parser source that LM is the HNSW level multiplier (`ml`
in the original paper) used in `l ← ⌊−ln(unif(0..1)) · ml⌋`, with
default `1 / ln(M)` (~0.402 at M=12). Pre-v1.5.3 consumers who
copied an `HNSW … LM N` snippet thinking they were configuring
Minkowski order were silently flattening the HNSW hierarchy. The
rule's HNSW parameter table now carries an explicit warning about
the v1.5.1/v1.5.2 mislabelling.

Other notable findings preserved as warnings:
- **`DIST JACCARD` / `DIST PEARSON` semantically inverted** in
  v3.0.5 catalog (`Distance::compute` calls similarity functions
  for these two values; HNSW `KnnPriorityList` uses ascending order
  → ranks LEAST-similar first). v1.5.5 added an explicit warning
  callout in `rules/vector-search.md` recommending standalone
  `vector::similarity::*` calls or a true distance metric for
  indexed nearest-neighbour search.
- **`<future> { … }` syntax does NOT exist in v3.0.5** despite
  appearing in upstream docs (no `Future` variant in `Value` /
  `Kind` enums; no `FUTURE` lexer keyword). v1.5.5 replaced the
  Futures section with §"Deferred Computation: Computed Fields,
  Closures, JS Functions" pointing at `DEFINE FIELD … VALUE`,
  `|$args| body` closures, and embedded JavaScript.
- **`DEFINE INDEX … DEFER` does NOT parse in v3.0.5** despite
  being in upstream docs (`DefineIndexStatement` has no `defer`
  field; parser doesn't read DEFER). v1.5.7 removed the DEFER
  example from `rules/surrealql.md` and rewrote the
  `rules/performance.md` DEFER subsection as a "do not use"
  deprecation block citing the parser source.
- **`UPDATE … LIMIT` does NOT parse in v3.0.5** (`UpdateStatement`
  struct has no `limit` field). v1.5.9 replaced the chunking
  pattern with a `SELECT VALUE id … LIMIT N` then `UPDATE $batch
  SET …` two-step (same fix shape as the v1.5.3 `DELETE … LIMIT`
  correction).
- **`TYPE JWT` accepts both `DURATION FOR TOKEN` and `DURATION FOR
  SESSION`** — the pre-v1.5.8 callout claiming `FOR TOKEN` was
  rejected was based on docs alone and contradicted parser tests.
  Semantics depend on issuer-key presence; symmetric algorithms
  (HS256/HS384/HS512) auto-populate the issuer.
- **`DEFINE NAMESPACE … STRICT` does NOT exist** despite v1.5.4
  briefly documenting it as the replacement for the deprecated
  `--strict` CLI flag. v3 only accepts `STRICT` on `DEFINE
  DATABASE`. Per-namespace coverage requires defining each database
  within the namespace as STRICT.

### Per-rule pass-10 verdicts

| File | Verdict | CRITs (pass-10) | Cumulative CRITs |
|---|---|---|---|
| `rules/data-modeling.md` | CONDITIONAL GO (INTERSECT IMP fixed in v1.5.10) | 0 | 4 |
| `rules/security.md` | GO | 0 | 8 |
| `rules/vector-search.md` | CONDITIONAL GO | 0 | 5 |
| `rules/performance.md` | GO | 0 | 18 |
| `rules/graph-queries.md` | CONDITIONAL GO (INTERSECT IMP fixed in v1.5.10) | 0 | 10 |
| `rules/surrealql.md` | CONDITIONAL GO | 0 | 35+ |

### Deferred to v1.6.x

Approximately 30 IMPORTANT-classified items remain as documentation-
completeness gaps — none contradict upstream v3.0.5. Tracked in the
per-rule pass-10 reports at `/tmp/pi-{rule}-pass10-out.md` and
summarised in `notes/v1.5.x-convergence.md`. Highlights:
- security.md: WITH REFRESH on TYPE RECORD; JWKS URL on TYPE
  RECORD; ACCESS REVOKE/SHOW/PURGE; DEFINE USER PASSHASH.
- surrealql.md: 10 undocumented ALTER targets; function namespaces
  (encoding::*, bytes::*, file::*, set::*, sequence::*, schema::*,
  api::*); data types (regex, range, literal, file); INSERT IGNORE
  example; DEFINE API; DEFINE CONFIG; INFO FOR INDEX/USER.
- performance.md: TLS flags in start-flag list;
  SURREAL_HNSW_CACHE_SIZE env-var verification; REBUILD INDEX ON
  TABLE all-indexes form.
- graph-queries.md: sub-SELECT graph clauses with ORDER/LIMIT/
  START/GROUP BY; `$parent` in WHERE; custom edge Record IDs in
  RELATE; +path+inclusive form.
- vector-search.md: HASHED_VECTOR semantics verification; MINKOWSKI
  in similarity-functions section.
- data-modeling.md: illustrative-edge consistency.

Migration: consumers who copied `INTERSECT` as an infix operator
should replace with `array::intersect()`. Machine-checked version-
consistency CI gate continues to apply.

See `notes/v1.5.x-convergence.md` for the full per-pass trajectory
table, fix-drift pattern analysis, and deferred-IMP catalog.

## [1.5.9] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.8 Pi-only re-audit CRIT remediation)

A ninth Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same six
rules audited in pass-8 returned **2 GO + 1 CONDITIONAL GO + 3
NO-GO** with **5 CRITs** total. v1.5.9 patches every CRIT.

The v1.5.8 ALTER section in surrealql.md (the largest post-pass-7
surgery) introduced two phantom-clause CRITs (ALTER INDEX COMPACT
and ALTER SEQUENCE RESTART neither parses in v3.0.5). The v1.5.8
TYPE JWT callout rewrite fixed only `rules/security.md`, leaving
the same wrong claim in `rules/surrealql.md` (CRIT-3) plus a
second related claim about `WITH ISSUER KEY` scope (CRIT-4).
`rules/performance.md` returned NO-GO on a pre-existing
UPDATE-LIMIT phantom that 8 prior passes missed. Plus a docs-only
`AccessDuration::default()` citation pointed at the wrong rust
file path (IMP escalated to fix as part of the security cross-
fix patch).

#### Per-file CRIT counts (pass-9)

- **`rules/surrealql.md` (4 CRITs):**
  - **CRIT-1: `ALTER INDEX … COMPACT` is a phantom clause.**
    v1.5.8 ALTER section example was invented. Verified at
    `core/src/syn/parser/stmt/alter.rs` lines 311-347 plus the
    `AlterIndexStatement` struct in
    `core/src/sql/statements/alter/index.rs`: the actual clauses
    are `IF EXISTS`, `PREPARE REMOVE`, `COMMENT '…'`,
    `DROP COMMENT`. There is no `compact` field on the struct.
    Replaced the phantom example with parser-verified
    `ALTER INDEX … PREPARE REMOVE` and `… COMMENT '…' / DROP
    COMMENT` examples plus the `IF EXISTS` variant.
  - **CRIT-2: `ALTER SEQUENCE … RESTART <n>` is a phantom
    clause.** Verified at `alter.rs` lines 1220-1243 +
    `AlterSequenceStatement`: the actual fields are `name`,
    `if_exists`, `timeout`. The clause is `TIMEOUT <duration>`
    (or `TIMEOUT NONE` to clear). Replaced the phantom RESTART
    example with `ALTER SEQUENCE … TIMEOUT 5s` /
    `ALTER SEQUENCE … TIMEOUT NONE` and an `IF EXISTS` variant.
  - **CRIT-3 (cross-fix from security pass-9): TYPE JWT comment
    at line 523-524 still claims "DURATION FOR SESSION only".**
    v1.5.8 fixed the `rules/security.md` callout but missed the
    same wrong claim embedded as a comment above the JWT example
    in `rules/surrealql.md`. The two files were left contradicting
    each other on the same fact-assertion. v1.5.9 rewrites the
    surrealql.md comment to match the parser-verified callout in
    security.md (TYPE JWT accepts both FOR TOKEN and FOR SESSION;
    semantics depend on issuer-key presence; symmetric algorithms
    auto-populate the issuer).
  - **CRIT-4 (cross-fix from security pass-9): WITH ISSUER KEY
    comment at line 535-537 wrongly claims scope-restriction.**
    v1.5.1 added a comment claiming `WITH ISSUER KEY` is "only
    valid inside a RECORD-access definition that uses WITH JWT,
    not on a standalone TYPE JWT access." Pass-9 verified against
    `core/src/syn/parser/test/stmt.rs:466`: `TYPE JWT ALGORITHM
    EDDSA KEY "foo" WITH ISSUER KEY "bar"` parses successfully
    on a standalone `TYPE JWT` to
    `JwtAccessIssue { alg: EdDSA, key: "bar" }`. The actual
    upstream constraint (per stmt.rs:619 `unwrap_err()`) is that
    the issuer algorithm must match the verification algorithm
    — not that the clause is scope-restricted. v1.5.9 rewrites
    the comment to clarify the clause works on both standalone
    and RECORD-WITH-JWT, with the actual algorithm-match
    constraint explained.

- **`rules/performance.md` (1 CRIT — pre-existing since v1.5.x):
  `UPDATE … LIMIT` does not exist in v3.0.5.** Lines 581-588
  recommended chunking large updates with `UPDATE user SET … WHERE
  … LIMIT 1000`. Verified at `surrealdb/core/src/sql/statements/
  update.rs`: `UpdateStatement` struct fields are `only / what /
  with / data / cond / output / timeout / explain` — NO `limit`
  field. The parser at `syn/parser/stmt/update.rs` does not parse
  LIMIT for UPDATE. `UPDATE … LIMIT 1000` would produce a parse
  error. Replaced with the parser-verified `SELECT VALUE id …
  LIMIT 1000` then `UPDATE $batch SET …` two-step chunking
  pattern. Same class of bug as the v1.5.3 `DELETE … LIMIT` CRIT.

- **`rules/security.md` (cross-fix only — CRIT count: 0 self,
  4 cross-cuts into surrealql.md tracked above):** The v1.5.8
  callout has IMP-1: `AccessDuration::default()` was cited at
  `core/src/sql/access_type.rs`. Pass-9 verified at upstream SHA
  `a97d3af85d79`: `AccessDuration::default()` is actually defined
  in `core/src/sql/access.rs` (`access_type.rs` defines `Default`
  for `AccessType` and `JwtAccess`, not `AccessDuration`). v1.5.9
  fixes the citation path.

`rules/data-modeling.md` and `rules/graph-queries.md` returned
**GO** with 0 CRITs (4th and 5th consecutive GO respectively for
data-modeling; 4th GO for graph-queries).
`rules/vector-search.md` returned **CONDITIONAL GO** with 0 CRITs
(breaks pass-7+8 GO streak with 6 documentation IMPORTANTs but no
correctness errors).

Pass-9 also surfaced an IMPORTANT not-yet-CRIT: the v1.5.8 ALTER
section claimed "seven targets"; the actual parser dispatch table
at `alter.rs:26-44` matches **17** keywords. v1.5.9 corrects the
intro line to state 17 targets and explicitly flags the ten
undocumented ones (EVENT, PARAM, BUCKET, ANALYZER, FUNCTION,
USER, ACCESS, CONFIG, API, MODULE) so consumers know to consult
upstream for those clause surfaces.

Pass-9 IMPORTANTs (security.md WITH REFRESH on TYPE RECORD / JWKS
URL on TYPE RECORD / ACCESS REVOKE-SHOW-PURGE; surrealql.md ALTER
TABLE IF EXISTS+SCHEMALESS / ALTER FIELD full clause set / ALTER
ACCESS / 10 undocumented ALTER targets / encoding-bytes-file-set-
sequence-schema-api function namespaces / DEFINE API / DEFINE
CONFIG; performance.md SCHEMAFULL inference rationale / FIELDS vs
COLUMNS drift / TIMEOUT clause coverage; vector-search.md MINKOWSKI
in similarity-functions section + similarity-function examples
+ unimplemented-function warnings) and MINORs are deferred to
v1.6.0 — they are documentation gaps or polish, not contradictions
of upstream — tracked at `/tmp/pi-{rule}-pass9-out.md`.

Migration: consumers who copied any of `ALTER INDEX … COMPACT`,
`ALTER SEQUENCE … RESTART`, `UPDATE … LIMIT`, the (still-wrong-in-
surrealql.md) "TYPE JWT only DURATION FOR SESSION" claim, or the
(wrong) "WITH ISSUER KEY only valid inside RECORD-access" claim,
need to apply the corrections noted above. Machine-checked
version-consistency CI gate continues to apply.

Cumulative CRITs across atomic-protocol cycle: v1.5.1=21, v1.5.2=
7, v1.5.3=15, v1.5.4=6, v1.5.5=6, v1.5.6=5, v1.5.7=1, v1.5.8=2,
v1.5.9=5 = **68 CRITs found-and-fixed across nine passes**. Pass-9
re-uptick (1→2→5) is two-fold: (a) v1.5.8 ALTER surgery
introduced 2 phantom-clause fix-drift CRITs, (b) the cross-rule
gap surfaced 2 more pre-existing latent bugs in surrealql.md that
the v1.5.8 callout-rewrite-only fix didn't propagate. Pass-10 is
expected to converge if the v1.5.9 surgery (~30-line ALTER block
correction + 4 comment-rewrites + 1 chunking-pattern replacement)
holds.

## [1.5.8] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.7 Pi-only re-audit CRIT remediation)

An eighth Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same
six rules audited in pass-7 returned **3 GO + 1 CONDITIONAL GO + 2
NO-GO** with **2 CRITs** total. v1.5.8 patches both. Both CRITs are
**pre-existing latent bugs** missed by all 7 prior passes — not
fix-drift from the v1.5.7 surgery — surfaced by pass-8's deeper
parser-source verification.

#### Per-file CRIT counts (pass-8)

- **`rules/security.md` (1 CRIT — pre-existing since v1.4.x):
  TYPE JWT DURATION FOR TOKEN claim has been wrong since v1.4.x.**
  The callout block at line ~161 stated "TYPE JWT only supports
  DURATION FOR SESSION — it does not accept DURATION FOR TOKEN
  because the token lifetime is set by the external issuer." Pass-8
  verified against the v3.0.5 parser at SHA `a97d3af85d79`:
  - `core/src/syn/parser/tests/stmt.rs:560` — `TYPE JWT ALGORITHM
    HS256 KEY "foo" DURATION FOR TOKEN 10s` parses successfully.
  - `core/src/syn/parser/tests/stmt.rs:825` — `TYPE JWT URL "..."
    WITH ISSUER ALGORITHM PS256 KEY "foo" DURATION FOR TOKEN 10s,
    FOR SESSION 2d` parses successfully.
  - `core/src/syn/parser/tests/stmt.rs:764` — same pattern succeeds.
  - `AccessDuration::default()` sets `token=1h` even for `TYPE JWT`.
  - `signin.rs:319` issues JWT with
    `expiration(av.token_duration)`.
  The pass-1 fix (which led to the original callout being added in
  v1.5.1) was based on incomplete docs reading; the parser actually
  accepts `FOR TOKEN` on `TYPE JWT`. Semantics depend on whether an
  issuer key is present: with `WITH ISSUER KEY`, SurrealDB issues
  tokens and `FOR TOKEN` controls their lifetime; for verification-
  only JWT (no issuer), the parser accepts `FOR TOKEN` but the
  external issuer's `exp` claim is authoritative. The callout is
  rewritten with the corrected semantics + parser-source citation.

- **`rules/surrealql.md` (1 CRIT — pre-existing since before
  v1.4.0): `ALTER` statement category entirely absent.** v3.0.5
  has `ALTER` as a DDL statement category dispatching to seven
  targets (verified at `core/src/syn/parser/stmt/alter.rs:14-29`
  and `core/src/expr/statements/alter/`):
  - `ALTER SYSTEM` — COMPACT, set/drop QUERY_TIMEOUT.
  - `ALTER NAMESPACE` / `ALTER DATABASE` — COMPACT.
  - `ALTER TABLE` — COMPACT, COMMENT, CHANGEFEED, schema-mode
    toggle (SCHEMAFULL/SCHEMALESS), TYPE switch (NORMAL/RELATION/
    ANY), PERMISSIONS rewriting.
  - `ALTER INDEX` — COMPACT (with optional IF EXISTS).
  - `ALTER FIELD` — change DEFAULT, ASSERT, VALUE, READONLY,
    PERMISSIONS without dropping the field.
  - `ALTER SEQUENCE` — RESTART value.
  The file's own v3.0.5 patch-notes entry references "ALTER
  coverage expanded (#7126)" — creating a discoverability
  asymmetry where users learn ALTER exists but can't find the
  syntax. v1.5.8 adds an `### ALTER` section under the Statements
  section after `### REMOVE`, with parser-verified examples for
  all seven targets.

`rules/data-modeling.md`, `rules/vector-search.md`,
`rules/performance.md` returned **GO** with 0 CRITs.
`rules/graph-queries.md` returned **CONDITIONAL GO** with 0 CRITs
(one IMPORTANT — `fn::refresh_user_stats` SELECT vs SELECT VALUE
in `count()` subqueries — deferred to v1.6.0 as a non-blocking
documentation polish).

`rules/performance.md` achieving GO is the most significant single
result of the cycle: this file had the highest cumulative CRIT
count (18 across passes 1-7) and historically the largest fix-drift
surface. Pass-8 verifies all 18 fabrications (DEFER,
`--rocksdb-cache-size`, `--max-connections`, EXPLAIN-shape claims,
RangeScan/standalone-Iterate, --conn, FORMAT TEXT regression, etc.)
are corrected and held under fresh source-cited scrutiny.

Pass-8 IMPORTANTs (security.md WITH REFRESH on TYPE RECORD / JWKS
URL discovery / ACCESS REVOKE-SHOW-PURGE / DEFINE USER PASSHASH;
surrealql.md `encoding::*`, `bytes::*`, `file::*`, `schema::*`,
`sequence::*` function namespaces / DEFINE API / DEFINE CONFIG /
INFO FOR INDEX-USER variants; graph-queries.md SELECT vs SELECT
VALUE bug in fn::refresh_user_stats) and MINORs are deferred to
v1.6.0 — they are documentation gaps or polish, not contradictions
of upstream — tracked in residual-risk lists at
`/tmp/pi-{rule}-pass8-out.md`.

Migration: consumers who copied the `TYPE JWT only supports
DURATION FOR SESSION` callout from any pre-v1.5.8 revision should
re-read the corrected callout — `TYPE JWT` accepts both `FOR
TOKEN` and `FOR SESSION`; semantics depend on issuer-key presence.
Consumers seeking `ALTER` syntax in pre-v1.5.8 revisions of
surrealql.md should now consult the new §"ALTER" subsection.
Machine-checked version-consistency CI gate continues to apply.

Cumulative CRITs across atomic-protocol cycle: v1.5.1=21, v1.5.2=7,
v1.5.3=15, v1.5.4=6, v1.5.5=6, v1.5.6=5, v1.5.7=1, v1.5.8=2 =
**63 CRITs found-and-fixed across eight passes**. Pass-8 surfaces
two pre-existing latent bugs that 7 prior passes (and the v1.4.4
adversarial round) all missed — demonstrating the atomic-protocol
cycle is still finding real upstream-mismatches even at this depth.
Pass-9 will test whether v1.5.8's small surgery (callout rewrite +
new ALTER section) introduces fix-drift; given the ALTER section
is ~50 new lines of grammar examples it has the highest drift risk
of any post-pass-7 surgery.

## [1.5.7] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.6 Pi-only re-audit CRIT remediation)

A seventh Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same
six rules audited in pass-6 returned **3 GO + 2 CONDITIONAL GO + 1
NO-GO** with **1 CRIT** total. v1.5.7 patches the single CRIT.

This is the strongest pass yet: data-modeling.md, security.md, and
graph-queries.md all returned GO; vector-search.md and performance.md
returned CONDITIONAL GO with 0 CRITs each; only surrealql.md
returned NO-GO with a single source-verified CRIT. CRIT-trend
21→7→15→6→6→5→1 is now strictly converging.

#### Per-file CRIT counts (pass-7)

- **`rules/surrealql.md` (1 CRIT — v1.5.6 fix-introduced) +
  cross-fix into `rules/performance.md`:**
  - **CRIT-1: `DEFER` clause does NOT exist in v3.0.5.** Pass-6
    added a `DEFINE INDEX … DEFER` example to surrealql.md (and
    v1.5.3 had originally added a §"Deferred Indexing (`DEFER`)"
    subsection to performance.md). Pass-7 verified against the
    v3.0.5 parser at SHA `a97d3af85d79`:
    - `DefineIndexStatement` has no `defer` field.
    - `parse_define_index` has no `DEFER` token handler.
    - Code-search across the entire `surrealdb/surrealdb` Rust
      codebase returns zero matches for the `DEFER` keyword in
      this context.
    Both the original v1.5.3 fix (driven by upstream-docs alone)
    and the v1.5.6 propagation were based on documentation that
    does not match the v3.0.5 parser. The pass-6 lesson applies:
    **parser-body verification is mandatory for grammar claims;
    documentation alone is insufficient.** v1.5.7 removes the
    `DEFER` example from `rules/surrealql.md` entirely and
    rewrites `rules/performance.md`'s §"Deferred Indexing" as
    §"Deferred Indexing — NOT in v3.0.5 (do not use)" with the
    full source-citation chain so consumers can re-verify
    against their binary version.

`rules/data-modeling.md`, `rules/security.md`,
`rules/graph-queries.md` returned **GO** with 0 CRITs (data-
modeling.md and security.md back-to-back GO; graph-queries.md
third consecutive GO). `rules/vector-search.md` returned **GO**
with 0 CRITs (upgraded from pass-6's CONDITIONAL GO; LM
correction + JACCARD/PEARSON warning + HASHED_VECTOR all held
clean against fresh parser-source verification).
`rules/performance.md` returned **CONDITIONAL GO** with 0 CRITs
(the FORMAT TEXT restoration + EXPLAIN FULL addition both held).

Pass-7 IMPORTANTs (surrealql.md ALTER section, INSERT IGNORE
example, DEFINE API/CONFIG, missing function namespaces, missing
data types; security.md WITH REFRESH / JWKS URL on TYPE RECORD /
ACCESS REVOKE/SHOW/PURGE; performance.md TLS flags / REBUILD
INDEX ON TABLE all-indexes form / SURREAL_HNSW_CACHE_SIZE
verification; vector-search.md similarity-function examples) and
MINORs are deferred to v1.6.0 — they are documentation gaps or
polish, not contradictions of upstream — tracked in residual-risk
lists at `/tmp/pi-{rule}-pass7-out.md`.

Migration: consumers who copied the `DEFINE INDEX … DEFER` clause
from v1.5.3-v1.5.6 docs need to remove the `DEFER` clause from
their schema definitions; the clause produces a parse error in
v3.0.5. Track upstream for a future release that may implement the
clause.

Cumulative CRITs across atomic-protocol cycle: v1.5.1=21, v1.5.2=7,
v1.5.3=15, v1.5.4=6, v1.5.5=6, v1.5.6=5, v1.5.7=1 = **61 CRITs
found-and-fixed across seven passes**. CRIT-trend post-pass-3 is
now strictly monotone-decreasing: 6→6→5→1. 5/6 GO+CONDITIONAL GO
at pass-7 (with the single NO-GO carrying just 1 CRIT) is the
clearest convergence signal of the cycle. Pass-8 likely closes
the v1.5.x cycle if no fix-drift surfaces from this small
single-line surgery.

## [1.5.6] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.5 Pi-only re-audit CRIT remediation)

A sixth Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same six
rules audited in pass-5 returned **3 GO + 1 CONDITIONAL GO + 2
NO-GO** with **5 CRITs** total. v1.5.6 patches every CRIT.

Trajectory: 4/6 GO is the highest GO rate of the cycle. CRIT count
dropped from 6 (pass-4 + pass-5 plateau) to 5. Two of the five CRITs
are v1.5.5 fix-introduced (closure parameter syntax + FORMAT TEXT
regression), continuing the empirical fix-drift pattern but at lower
volume. The other three are pass-4/5 IMPORTANTs that pass-6 ruthless
scrutiny escalated.

#### Per-file CRIT counts (pass-6)

- **`rules/surrealql.md` (3 CRITs):**
  - **CRIT-1: Closure parameter syntax — `|x| x * 2` should be
    `|$x| $x * 2`.** v1.5.5 fix-introduced. The §"Deferred
    Computation" replacement for the (deleted) Futures section
    showed a closure example with bare-identifier parameters; v3
    SurrealQL closure parameters require the `$` prefix (bare
    identifiers bind to field references, not local variables).
    Verified against the upstream closures docs page and the
    canonical `LET $double = |$n: number| $n * 2; RETURN
    $double(2);` example. Corrected the closure example to use the
    `$`-prefixed parameter form with explicit `RETURN`.
  - **CRIT-2: Seven `time::set_*` functions undocumented (escalated
    from pass-4/5 IMP).** v3.0.2 introduced datetime setter
    functions (`time::set_year` / `set_month` / `set_day` /
    `set_hour` / `set_minute` / `set_second` / `set_nanosecond`);
    the file's own v3.0.2 patch-notes entry mentions them, but the
    Time Functions section never documented any of them. Added
    seven setter examples covering the full surface.
  - **CRIT-3: `DEFINE INDEX IF NOT EXISTS` undocumented (escalated
    from pass-4/5 IMP).** Every other `DEFINE` statement in the
    file (TABLE, FIELD, ACCESS, NAMESPACE, DATABASE, SEQUENCE,
    FUNCTION) documents both `OVERWRITE` and `IF NOT EXISTS`;
    `DEFINE INDEX` was the sole outlier. Added the idempotent
    form alongside `OVERWRITE`. Also added `CONCURRENTLY` and
    `DEFER` clause examples (resolving pass-4/5 IMP-1) — both are
    in the upstream `DEFINE INDEX` grammar and were already
    covered in `rules/performance.md` v1.5.3, but the foundational
    language reference omitted them.

- **`rules/performance.md` (2 CRITs):**
  - **CRIT-1: `FORMAT TEXT` keyword IS valid in v3 — v1.5.5 fix
    was a regression.** v1.5.5 removed `FORMAT TEXT` from the
    documented `EXPLAIN` standalone form on the basis that the
    upstream EXPLAIN docs page only shows `FORMAT JSON`. Pass-6
    verified against the parser source
    (`core/src/syn/parser/stmt/mod.rs` ~lines 156-160) which
    explicitly accepts both `"TEXT"` and `"JSON"` as `FORMAT`
    keywords (the parser error message itself reads `"TEXT or
    JSON"`). The pass-5 patch was based on docs alone, missing the
    parser's broader surface. Restored `FORMAT TEXT` to the
    documented grammar with a precision note that TEXT is also
    the default when no FORMAT clause is present (so writing
    `FORMAT TEXT` explicitly is valid but redundant). This is the
    second consecutive pass where docs-only verification produced
    an incorrect fix; treat parser-body verification as mandatory
    for grammar claims.
  - **CRIT-2: `EXPLAIN FULL` clause-form undocumented (escalated
    from pass-4/5 IMP).** v3.0.5 supports `@statement EXPLAIN
    FULL` (clause-form) for extended planner output beyond the
    basic `EXPLAIN`. Verified against
    `core/src/syn/parser/stmt/parts.rs:120` `try_parse_explain`
    which reads an optional `FULL` token after `EXPLAIN`, and
    against the upstream language test
    `language-tests/tests/language/statements/select/
    explain_multi_table.surql` which exercises both `EXPLAIN` and
    `EXPLAIN FULL` and shows the latter produces 7 ops vs the
    former's 4. Added the clause-form `EXPLAIN FULL` example to
    the EXPLAIN section.

`rules/data-modeling.md`, `rules/security.md`, and
`rules/graph-queries.md` returned **GO** with 0 CRITs.
`rules/vector-search.md` returned **CONDITIONAL GO** with 0 CRITs
(the JACCARD/PEARSON warning callout held cleanly under re-
verification — pass-6 reviewer cited the same
`catalog/schema/index.rs` lines and confirmed the inversion
behaviour). 4/6 GO is the highest GO rate of the v1.5.x cycle.

Pass-6 IMPORTANTs (security WITH REFRESH on TYPE RECORD, JWKS URL
on TYPE RECORD, REVOKE GRANT/SHOW/PURGE; performance TLS flags
in start-flag list, REBUILD INDEX ON TABLE all-indexes form;
surrealql ALTER section, missing function namespaces (encoding /
bytes / file / not / set / sequence / schema / api), regex /
range / literal / file data types, INSERT IGNORE example;
graph-queries sub-SELECT graph clauses, $parent in WHERE, custom
edge Record IDs in RELATE, +path+inclusive form; vector-search
similarity-function examples) and MINORs are deferred — they are
documentation gaps or polish, not contradictions of upstream —
tracked in residual-risk lists at `/tmp/pi-{rule}-pass6-out.md`.

Migration: consumers who copied the `|x| x * 2` closure example,
removed `FORMAT TEXT` from EXPLAIN syntax based on v1.5.5
guidance, or expected `EXPLAIN FULL` to be undocumented should
apply the corrections noted above. Machine-checked version-
consistency CI gate continues to apply.

Cumulative CRITs across atomic-protocol cycle: v1.5.1=21,
v1.5.2=7, v1.5.3=15, v1.5.4=6, v1.5.5=6, v1.5.6=5 = **60 CRITs
found-and-fixed across six passes**. CRIT-trend is now strictly
monotone-decreasing (21→7 was the first drop; 15 was an outlier
from adding the surrealql full-pass; 6→6→5 is the descent). 4/6
GO at pass-6 vs 1/6 GO at pass-5 is the strongest convergence
signal so far.

## [1.5.5] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.4 Pi-only re-audit CRIT remediation)

A fifth Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same six
rules audited in pass-4 returned **5 NO-GO + 1 GO** with **6 CRITs**
total. v1.5.5 patches every CRIT.

`rules/graph-queries.md` returned its first clean pass after four
prior NO-GOs (10 cumulative CRITs) — verified via direct parser-
source citation including the `path_shortest.surql` upstream
language test. The convergence target for that file held.

The other five files surfaced a mixture of **fix-patch drift from
v1.5.4 surgery** and **latent CRITs that were pass-4 IMPORTANTs
escalated under pass-5's ruthless standard**. Most consequential
finding: a `JACCARD` / `PEARSON` semantic-inversion catalog bug in
`rules/vector-search.md` — the same genus as the v1.5.3 LM
mislabelling correction.

#### Per-file CRIT counts (pass-5)

- **`rules/data-modeling.md` (1 CRIT — pre-existing, pattern-
  identical to PASS-1):** §"Document + Graph (Social Network with
  Rich Profiles)" defined `member_of TYPE RELATION IN user OUT
  group ENFORCED;` but the `group` table itself was never defined
  in the file (and `member_of` was unused in any query in the
  pattern). Identical class of bug to the PASS-1 `wrote`-edge
  CRIT. Removed the unused edge definition.

- **`rules/security.md` (1 CRIT — v1.5.4 fix-introduced) +
  cross-fix into `rules/deployment.md` and `rules/surrealql.md`:**
  - **CRIT-1: `DEFINE NAMESPACE <ns> STRICT;` is invalid SurrealQL
    in v3.** v1.5.4 introduced this as the recommended replacement
    for the deprecated `--strict` flag, but verification against
    `core/src/syn/parser/stmt/define.rs` `parse_define_namespace()`
    proves the parser only handles `COMMENT` after the namespace
    name — there is no `STRICT` token handler. The
    `DefineNamespaceStatement` struct (`core/src/sql/statements/
    define/namespace.rs`) has no `strict` field. STRICT is **only**
    valid on `DEFINE DATABASE`. Four sites in security.md replaced
    with per-database-only guidance (for namespace-wide coverage,
    define each database within the namespace as STRICT).
    Cross-fix: `deployment.md` line 106 server-flags table same
    correction; `surrealql.md` line 562 §DEFINE ACCESS BEARER
    incorrectly claimed `FOR RECORD` *requires* an `AUTHENTICATE`
    clause (it is optional per the upstream BEARER syntax
    diagram) — corrected.

- **`rules/vector-search.md` (2 CRITs):**
  - **CRIT-1 (pass-4 IMP escalated): `HASHED_VECTOR` clause
    missing.** The `use_hashed_vector: bool` parameter exists in
    both `catalog::HnswParams` and `sql::HnswParams` (v3.x
    revision 2) and is fully wired through parser → SQL → catalog,
    but was entirely absent from the rule. Same class of error as
    the v1.5.3 LM mislabelling — undocumented HNSW parameter.
    Added to the syntax-block placeholder and parameter table.
  - **CRIT-2 (NEW): `JACCARD` and `PEARSON` are similarity
    functions, not distance functions, but the catalog
    `Distance::compute` body calls them as if they were the
    correct metric for HNSW search.** Verified at
    `catalog/schema/index.rs:293-300`: `Self::Cosine =>
    v1.cosine_distance(v2)` (true distance), but `Self::Jaccard =>
    v1.jaccard_similarity(v2)` and `Self::Pearson =>
    v1.pearson_similarity(v2)` (similarities). The HNSW
    `KnnPriorityList` uses ascending `BTreeMap` order (smaller =
    closer for true distance), so configuring `DIST JACCARD` or
    `DIST PEARSON` ranks the **least** similar results first —
    the search is silently inverted. The §"Distance Function
    Selection Guide" presented both as regular distance metrics.
    Added an explicit warning callout, marked the affected rows
    with ⚠, redirected users to standalone
    `vector::similarity::jaccard()` /
    `vector::similarity::pearson()` for ad-hoc scoring, and
    recommended a true distance metric for indexed nearest-
    neighbour search. Also added the missing `MINKOWSKI` row to
    the selection guide (pass-5 IMP).

- **`rules/performance.md` (1 CRIT — pass-4 IMP escalated):
  `EXPLAIN [ FORMAT TEXT | JSON ]` syntax includes a `FORMAT TEXT`
  keyword that does not exist in v3.0.5.** The upstream EXPLAIN
  page documents only `EXPLAIN [ANALYZE] [FORMAT JSON]` — text is
  the default, not an explicit format keyword. Users copying
  `EXPLAIN FORMAT TEXT SELECT ...` would have got a parser error.
  Corrected the documented standalone form to
  `EXPLAIN [ ANALYZE ] [ FORMAT JSON ] @statement` with a
  precision comment.

- **`rules/surrealql.md` (1 CRIT — pre-existing, missed by 4
  prior passes): §"Futures" documents `<future> { … }` syntax
  that does not exist in v3.0.5.** Verified exhaustively: no
  `Future` variant in the `Value` enum (`core/src/val/mod.rs`),
  no `Future` variant in the `Kind` enum (`core/src/sql/kind.rs`),
  no `FUTURE` keyword in the lexer, no `<future>` parse path in
  the expression parser. Earlier SurrealDB versions did expose
  this form; v3 covers the same use cases via three other
  features. Replaced the section with §"Deferred Computation:
  Computed Fields, Closures, JS Functions" pointing at
  `DEFINE FIELD … VALUE @expression` (the direct successor for
  "computed on read"), `|args| body` closures, and the existing
  Embedded JavaScript section.

`rules/graph-queries.md` returned **GO with 0 CRITs** — first
clean pass after four prior NO-GOs. v1.5.4's `+inclusive`
correction held; PASS-1 through PASS-3 fixes verified clean
against parser source plus upstream language tests; cross-
references to v1.5.4 surrealql.md and security.md showed no
drift. Three IMPORTANTs (sub-SELECT graph clauses with
`ORDER`/`LIMIT`/`START`/`GROUP BY`, `$parent` in graph-traversal
WHERE clauses, custom edge Record IDs in `RELATE`) deferred to
v1.6.0 as additive coverage gaps.

Pass-5 IMPORTANTs (data-modeling illustrative-edge consistency;
security WITH REFRESH on TYPE RECORD / JWKS URL on TYPE RECORD /
broken §Capabilities cross-reference / better AUTHENTICATE
example; vector-search MINKOWSKI in similarity-functions section
+ JACCARD/PEARSON similarity functions + MINOR doc duplication;
performance EXPLAIN FULL / SURREAL_HNSW_CACHE_SIZE / REBUILD
INDEX ON TABLE all-indexes form / TLS flags missing from
performance flag list; surrealql INSERT IGNORE example / seven
`time::set_*` functions / four data types `regex`/`range`/
`literal`/`file` / `array<T,N>` cardinality / 13 missing function
namespaces / CONCURRENTLY+IF NOT EXISTS on DEFINE INDEX) and
MINORs are deferred — they are documentation gaps or polish, not
contradictions of upstream — tracked in residual-risk lists at
`/tmp/pi-{rule}-pass5-out.md`.

Migration: consumers who copied `member_of TYPE RELATION IN user
OUT group`, `DEFINE NAMESPACE <ns> STRICT;`, `EXPLAIN FORMAT TEXT
…`, `<future> { … }`, or configured `DIST JACCARD` / `DIST
PEARSON` on an HNSW index expecting nearest-neighbour search,
need to apply the corrections noted above. Machine-checked
version-consistency CI gate continues to apply.

Cumulative CRITs across atomic-protocol cycle: v1.5.1=21,
v1.5.2=7, v1.5.3=15, v1.5.4=6, v1.5.5=6 = **55 CRITs found-and-
fixed across five passes**. Pass-5 CRIT count matched pass-4
exactly (6 / 6) — convergence has plateaued, not completed.

## [1.5.4] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.3 Pi-only re-audit CRIT remediation)

A fourth Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same six
rules patched/audited in v1.5.3 returned **3 NO-GO + 2 CONDITIONAL GO
+ 1 GO** with **6 CRITs** total. v1.5.4 patches every CRIT.

Three of the six CRITs sit in `rules/surrealql.md` and are a textbook
case of the empirical fix-patch-drift pattern noted in `~/CLAUDE.md`:
v1.5.3 added four "missing" vector functions to surrealql.md based on
function-registration tables in the v3.0.5 source — but pass-4
verified the actual function bodies and surfaced that **two of those
functions always return `Error::Unimplemented` at runtime** in v3.0.5
(`vector::distance::mahalanobis` and `vector::similarity::spearman`),
and a **third has a fundamentally different signature** than v1.5.3
documented (`vector::distance::knn` is a context-only function that
reads the current HNSW-index iteration result, not a standalone
`(vec_a, vec_b, k)` callable). Documenting registered-but-unimplemented
functions as if they worked is worse than not mentioning them at all.

The other three CRITs cover:
- A graph-queries.md `+shortest=target+path` example whose `+path`
  sub-modifier the v3.0.5 parser explicitly rejects (Path / Collect /
  Shortest are mutually exclusive `RecurseInstruction` variants —
  only `+inclusive` is accepted as a secondary flag on `+shortest`).
- Two security/deployment CLI flag corrections that turn into silent
  production-security failures: `--strict` is deprecated in v3 and
  silently ignored at startup, and `--allow-origins` (plural) does
  not exist — the v3 flag is `--allow-origin` (singular).

#### Per-file CRIT counts (pass-4)

- **`rules/surrealql.md` (3 CRITs — all v1.5.3-introduced):**
  - **CRIT-1: `vector::distance::knn` fabricated signature.** v1.5.3
    documented `vector::distance::knn([1, 2], [3, 4], 5)` as a
    standalone 3-arg distance computation. Source proves
    (`core/src/fnc/vector.rs:87-103`) the function takes a single
    optional `Optional<Value>` (KNN reference index, default 0) and
    reads the current iteration result from the execution context —
    it cannot be called with two vectors and a `k` argument. Replaced
    with an accurate description noting it is a context-only
    function used inside SELECTs that scan an HNSW index, with
    cross-reference to the `<|K,DIST|>` brute-force operator for
    ad-hoc nearest-neighbour computation.
  - **CRIT-2: `vector::distance::mahalanobis` wrong arity AND
    unimplemented.** v1.5.3 documented a 3-arg form with a
    covariance matrix. Source proves (`core/src/fnc/vector.rs:
    105-108`) the function takes exactly 2 `Vec<Number>` args (no
    covariance matrix) and **always returns `Error::Unimplemented`**
    at runtime. v1.5.4 documents the actual 2-arg signature and
    explicit unimplemented status, with a "do not call in
    production" warning until it ships an implementation.
  - **CRIT-3: `vector::similarity::spearman` unimplemented.** The
    2-arg signature v1.5.3 documented is correct, but the function
    body always returns `Error::Unimplemented` (`core/src/fnc/
    vector.rs:140-143`). Same treatment as CRIT-2 — explicit
    unimplemented warning so consumers don't ship code that errors
    at runtime.

- **`rules/security.md` (2 CRITs — both v3 CLI deprecations missed
  by passes 1-3) + cross-fix into `rules/deployment.md`:**
  - **CRIT-1: `--strict` deprecated in v3.** Verified against
    `surrealdb/server/src/cli/start.rs` and `dbs/mod.rs`: the flag
    still parses but emits a warning and is **silently ignored**.
    security.md cited `--strict` for four separate security-critical
    contexts (server startup example, recommendation, common
    pitfalls list, production checklist) — all four were giving
    consumers a false sense of security. v1.5.4 replaces every
    `--strict` reference with the correct v3 mechanism: enforce
    strict mode at the schema layer with `DEFINE DATABASE <db>
    STRICT;` / `DEFINE NAMESPACE <ns> STRICT;`, and require
    authentication via `--deny-guests` / `--deny-arbitrary-query`
    capabilities flags. Cross-fix in `rules/deployment.md`: the
    server-flags reference table at line 106 and the setup-surreal
    GitHub Action input `surrealdb_strict` at line 167 both now
    explicitly mark `--strict` as deprecated/no-op with the same
    replacement guidance.
  - **CRIT-2: `--allow-origins` (plural) does not exist; the v3
    flag is `--allow-origin` (singular).** Verified against
    `server/src/cli/start.rs`. The plural form would fail at
    `surreal start` parse time. Three CORS-configuration examples
    in security.md were corrected. The new singular form accepts
    the flag multiple times for multiple origins (or a comma list).

- **`rules/graph-queries.md` (1 CRIT — v1.5.3 fix RESIDUAL
  promoted to CRIT):** The §"Native Shortest-Path" example combined
  `+shortest=person:ceo` with `+path` to "return the full path."
  Both halves of that claim were wrong:
  - The v3.0.5 parser (`parse_recurse_instruction` in `idiom.rs`)
    returns a single `Option<RecurseInstruction>` — Path / Collect
    / Shortest are mutually exclusive variants. After `+shortest=`,
    only `+inclusive` is accepted as a secondary flag.
  - `+shortest=` already returns the full path array by default
    (verified against the upstream language test
    `language-tests/tests/language/graph/path_shortest.surql`,
    test 0 returns `[person:lead_infra, person:dir_platform,
    person:vp_eng, person:ceo]`). There is no "just the terminal
    node" mode to escape from.
  Replaced with a `+inclusive` example (the only valid secondary
  flag on `+shortest`), and added a precision paragraph documenting
  the default path-array return shape and the parser-level
  mutex on Path / Collect / Shortest.

`rules/data-modeling.md`, `rules/vector-search.md`, and
`rules/performance.md` returned no CRITs in pass-4 (data-modeling GO,
vector-search and performance CONDITIONAL GO with documentation-only
IMPs deferred). vector-search.md's pass-3 LM rewrite — the most
consequential v1.5.x correction — held cleanly under pass-4
re-scrutiny.

Pass-4 IMPORTANTs (surrealql.md missing data types `regex` / `range`
/ `number` / `literal` / `geometry<feature>` union; missing function
namespaces `bytes::*` / `encoding::*` / `file::*` / `not::*` /
`set::*` / `sequence::*` / `schema::*` / `api::*`; missing ALTER
statements section; missing `DEFINE API` / `DEFINE MODEL` /
`DEFINE CONFIG`; missing `array<T,N>` / `set<T,N>` cardinality docs;
missing `CONCURRENTLY` / `IF NOT EXISTS` on `DEFINE INDEX`;
performance.md `EXPLAIN FULL` clause / `SURREAL_HNSW_CACHE_SIZE` env
var / `EXPLAIN ANALYZE` semantics; security.md `WITH REFRESH` /
`AUTHENTICATE` on RECORD / JWKS URL on RECORD / capabilities flag
surface / `ACCESS … REVOKE GRANT` / `ACCESS … SHOW`;
graph-queries.md RELATE `RETURN` clause / `ONLY` / sub-SELECT graph
clause / edge deletion / FETCH-on-graph-paths) and MINORs are
deferred — they are documentation gaps or polish, not contradictions
of upstream — and tracked in the residual-risk lists of the per-rule
re-audit reports at `/tmp/pi-{rule}-pass4-out.md`.

Migration: consumers who copied the `+shortest=target+path` pattern,
`--strict`, `--allow-origins` (plural), or any of
`vector::distance::knn(@vec_a, @vec_b, @k)` /
`vector::distance::mahalanobis([…], […], @cov_matrix)` /
`vector::similarity::spearman([…], […])` calling them as if
implemented need to apply the corrections noted above. Machine-
checked version-consistency CI gate continues to apply.

## [1.5.3] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.2 Pi-only re-audit CRIT remediation, including foundational `rules/surrealql.md`)

A third Pi+DeepSeek-V4-Pro:xhigh adversarial pass — this time over the
same five rules patched in v1.5.2 **plus** a first dedicated full-file
pass on the foundational language reference `rules/surrealql.md` —
returned **5 NO-GO + 1 CONDITIONAL GO** with **15 CRITs** total. The
empirical fix-patch-drift pattern noted in `~/CLAUDE.md` continued to
play out (each pass introduces 1-2 new bugs from the prior fix
surgery), and the dedicated `rules/surrealql.md` pass surfaced six
additional latent hallucinations that two earlier rounds of cross-fix
patches did not exhaust. v1.5.3 patches every CRIT.

The single most consequential finding: the v1.5.1 "fix" of the HNSW
`LM` parameter — labelling it as "Minkowski distance order" — was
itself wrong. v3.0.5 source proves `LM` is the HNSW **level
multiplier** (`ml` in the original Malkov & Yashunin paper), used in
the formula `l ← ⌊−ln(unif(0..1)) · ml⌋` to assign each new point an
insertion level. Default `1 / ln(M)` (≈0.402 at `M=12`). The Minkowski
distance order is specified inline in `DIST MINKOWSKI <order>`, **not**
via `LM`. Anyone who copied an `HNSW … LM N` snippet from v1.5.1 or
v1.5.2 thinking they were configuring Minkowski order was silently
setting the level multiplier instead, often dramatically flattening
the HNSW hierarchy. v1.5.3 corrects the parameter table row, the
default value, and the precision callout, and adds an explicit warning
about the v1.5.1/v1.5.2 mislabelling.

- **`rules/data-modeling.md`** (1 CRIT) — Line 948 §"Time-Series Data
  Pattern" used `DELETE sensor_reading WHERE recorded_at < time::now()
  - 30d LIMIT 100;`. v3.0.5 SurrealQL has no `LIMIT` clause on
  `DELETE` (verified against `surrealdb/core/src/sql/statements/
  delete.rs` — `DeleteStatement` has no `limit` field). Removed the
  invalid clause and added a precision comment recommending a
  scheduled task for bounded-batch cleanup.

- **`rules/graph-queries.md`** (2 CRITs) — (1) Line 15 §"Basic Syntax"
  RELATE template still read `[SET | CONTENT | MERGE ...]`,
  contradicting the v1.5.2 §"Setting Properties on Edges" precision
  comment ("there is no MERGE clause on RELATE"). The v1.5.2 patch
  fixed the example block but left the syntax head stale. Now reads
  `[CONTENT @value | SET @field = @value ...]` consistently.
  (2) Missing entire §"`TYPE RELATION`, `FROM`/`TO`, and `ENFORCED`"
  subsection — the file documented only the SCHEMAFULL + typed
  `record<…> in/out` pattern, omitting `DEFINE TABLE … TYPE RELATION
  FROM person TO article`, the `IN`/`OUT` aliases, the `|`
  multi-type endpoint syntax, and the `ENFORCED` keyword. New
  subsection added with upstream-verified examples.

- **`rules/surrealql.md`** (6 CRITs — first dedicated Pi pass on the
  foundational language reference):
  - **CRIT-1: Empty `### Pattern Matching` table.** v1.4.4 correctly
    removed `LIKE` / `NOT LIKE` (which don't exist in v3.0.5) but
    left an empty header-only table behind. Replaced with a
    cross-reference paragraph pointing readers at the comparison
    operators (`~`, `!~`, `?~`, `*~`), full-text search operators
    (`@@` / `@N@`), and KNN operators (`<|K|>` / `<|K,DIST|>` /
    `<|K,EF|>`).
  - **CRIT-2: Missing `!!` operator.** v3.0.5 lists `!!` as a
    distinct unary truthiness-coercion operator. Added to the
    Logical Operators table.
  - **CRIT-3: Missing `OUTSIDE` and `INTERSECTS` geometry
    operators.** Both are documented v3.0.5 operators used in
    geospatial queries; neither appeared in the operators tables.
    Added a new `### Geometry Operators` table.
  - **CRIT-4: Four missing vector functions.** v3.0.5 source
    (`surrealdb/core/src/fnc/script/modules/surrealdb/functions/
    vector.rs` and friends) registers `vector::scale`,
    `vector::distance::knn`, `vector::distance::mahalanobis`, and
    `vector::similarity::spearman` — none of which appeared in the
    Vector Functions section. All four added with usage examples.
  - **CRIT-5: Missing `DEFINE ACCESS BEARER` section.** The file
    covered RECORD and JWT access but not BEARER, the v3 mechanism
    for API key / refresh token authentication. Added a BEARER
    subsection covering `FOR USER` vs `FOR RECORD`, the
    `AUTHENTICATE` clause, `DURATION FOR GRANT`/`TOKEN`/`SESSION`,
    and the `ACCESS … GRANT` token-issuance statement (with the
    user identifier correctly unquoted — see security.md fix below).
  - **CRIT-6 (cross-fix from `rules/vector-search.md`): `DIST`
    default was wrong.** The DEFINE INDEX section claimed `DIST`
    defaulted to `COSINE`. Upstream parser (`define/index.rs`)
    initialises `let mut distance = Distance::Euclidean;` and
    `Distance` derives `#[default]` on `Euclidean`. Corrected to
    `EUCLIDEAN`, with a precision note pointing at the source line
    and recommending an explicit `DIST COSINE` override for
    normalised text embeddings.

- **`rules/vector-search.md`** (2 CRITs):
  - **CRIT-1: `LM` rewrite.** As described above — `LM` is the HNSW
    level multiplier, not "Minkowski distance order." The parameter
    table row, default value (`1 / ln(M)`), syntax-block placeholder,
    and the precision callout are all corrected. The callout now
    includes an explicit warning that v1.5.1 and v1.5.2 mislabelled
    `LM` and that anyone who copied an `HNSW … LM N` snippet
    intending to set Minkowski order should write `DIST MINKOWSKI N`
    instead.
  - **CRIT-2 (cross-file into `rules/surrealql.md`)** — counted
    under surrealql.md CRIT-6 above (DIST default = EUCLIDEAN).

- **`rules/performance.md`** (4 CRITs):
  - **CRIT-1: `surreal import --conn` flag does not exist.** v3.0.5
    CLI uses `--endpoint` (with short alias `-e`); no `--conn` flag
    is registered anywhere in the v3.0.5 server source. Verified
    against `server/src/cli/import.rs` and the `cli_integration.rs`
    test corpus. §"Bulk Import" example corrected.
  - **CRIT-2: `REBUILD INDEX` statement missing.** v3.0.5 has a
    first-class `REBUILD INDEX [IF EXISTS] <name> ON <table>
    [CONCURRENTLY]` statement that preserves the full original
    index definition (UNIQUE / FULLTEXT ANALYZER / BM25 / HIGHLIGHTS
    / HNSW DIMENSION / EFC / M / DEFER / CONCURRENTLY). The file
    previously recommended only the legacy `REMOVE INDEX` +
    `DEFINE INDEX` pattern, which loses the original definition.
    §"Index Rebuild Strategies" rewritten to lead with `REBUILD
    INDEX` and demote the manual pattern to a "use only when
    changing the index shape" note. Adds an `INFO FOR INDEX`
    example for build-progress monitoring.
  - **CRIT-3: `CONCURRENTLY` clause undocumented.** Both `DEFINE
    INDEX` and `REBUILD INDEX` accept `CONCURRENTLY` for
    non-blocking background builds — directly relevant to large
    HNSW / FULLTEXT index lifecycle in production. New §"Concurrent
    Index Builds (`CONCURRENTLY`)" subsection added.
  - **CRIT-4: `DEFER` clause undocumented.** `DEFINE INDEX … DEFER`
    (since v2.5.0) decouples ingestion from index maintenance;
    eliminates write-write conflicts on high-throughput parallel
    ingestion. New §"Deferred Indexing (`DEFER`)" subsection added,
    with the `UNIQUE`+`DEFER` mutex caveat documented.

- **`rules/security.md`** (1 CRIT) — Line 244 §"Bearer Access /
  GRANT Statement" example used `ACCESS service_tokens GRANT FOR
  USER 'ci_runner';` with the user identifier quoted. v3 `GRANT FOR
  USER @name` takes an identifier, not a string literal — the quoted
  form would fail to reference the `DEFINE USER` name correctly.
  Removed the quotes.

Pass-3 IMPORTANTs (RECORD `WITH REFRESH` / `AUTHENTICATE` clauses,
JWKS URL on RECORD-with-JWT, capabilities flags surface, `regex` /
`range` / `number` / `literal` data types, `ALTER` statement
coverage, `DEFINE SCOPE` / `TOKEN` / `API` / `CONFIG`, full session
variable surface, additional function namespaces (`bytes::*`,
`encoding::*`, `file::*`, `not::*`, `sequence::*`, `set::*`,
`api::*`), `RELATE … RETURN` clause, `RELATE ONLY`, edge deletion,
FETCH-on-graph-paths, full sub-SELECT graph-clause syntax) and
MINORs are deferred — they are documentation gaps or polish, not
contradictions of upstream — and tracked in the residual-risk lists
of the per-rule re-audit reports at
`/tmp/pi-{rule}-pass3-out.md`.

Migration: consumers who copied any of the corrected examples — the
`DELETE … LIMIT` clause, the `RELATE … MERGE` pattern, the empty
Pattern Matching table, the missing operators, `LM N` intending
Minkowski order, the `--conn` flag, the legacy `REMOVE`+`DEFINE`
rebuild pattern, the `DIST COSINE` default assumption, or the
quoted `GRANT FOR USER 'name'` form — need to apply the corrections
noted above. Machine-checked version-consistency CI gate continues
to apply.

## [1.5.2] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.1 Pi-only re-audit CRIT remediation)

A second Pi+DeepSeek-V4-Pro:xhigh adversarial pass over the same five
rules patched in v1.5.1 (`rules/data-modeling.md`, `rules/security.md`,
`rules/vector-search.md`, `rules/performance.md`,
`rules/graph-queries.md`) returned **2 GO + 2 CONDITIONAL GO + 1 NO-GO**
with **7 CRITs** total — every one introduced or missed by the v1.5.1
fix surgery. v1.5.2 patches every CRIT. The empirical fix-patch-drift
pattern noted in `~/CLAUDE.md` ("each rev closes prior CRITs but
introduces 1-2 new ones from fix surgery") played out as expected,
mostly concentrated in the file with the largest pass-1 patch surface
(`rules/performance.md`, 8 sites).

- **`rules/performance.md`** (3 CRITs — all v1.5.1-introduced) — The
  v1.5.1 EXPLAIN-output rewrite invented two operator names that do
  not appear in the v3.0.5 operator catalog (`RangeScan`, standalone
  `Iterate`) and asserted that the clause-form `… EXPLAIN` does not
  produce `operation: 'Iterate Table'` / `operation: 'Iterate Index'`
  — but it does. The actual upstream surface is **two distinct
  output shapes** depending on syntax form: the clause form
  (`SELECT … EXPLAIN`) emits `operation:` rows with values like
  `'Iterate Table'` / `'Iterate Index'` / `'Fetch'`, and the statement
  form (`EXPLAIN SELECT …`) emits `operator:` rows from the planner
  scan catalog (`Scan`, `TableScan`, `IndexScan`, `CountScan`,
  `IndexCountScan`, `FullTextScan`, `GraphEdgeScan`, `ReferenceScan`,
  `KnnScan`, `UnionIndexScan`). The Query Performance section now
  documents both shapes explicitly, removes the hallucinated
  `RangeScan` and standalone `Iterate` rows, and updates the §"Query
  Timing" examples and §"Common Bottlenecks" table cell to label the
  output as clause-form `operation:` (or to show both forms) so the
  rest of the file no longer contradicts the operator-name section.

- **`rules/graph-queries.md`** (1 CRIT) — §"Setting Properties on
  Edges" included a third example using `RELATE … MERGE { … }`. v3
  `RELATE` grammar is `RELATE [ ONLY ] @from -> @table -> @to
  [ CONTENT @value | SET @field = @value … ] [ RETURN … ]
  [ TIMEOUT @duration ]` — there is no `MERGE` clause on `RELATE`.
  The example is replaced with the correct way to update an existing
  edge's properties (`UPDATE knows SET last_interaction = time::now()
  WHERE in = person:alice AND out = person:bob`) and a precision
  comment quotes the verified RELATE grammar.

- **Cross-fix in `rules/surrealql.md`** (3 CRITs) — The vector-search
  re-audit surfaced three function-path hallucinations in the
  language reference that v1.4.4 missed:
  `vector::distance::cosine`, `vector::distance::jaccard`,
  `vector::distance::pearson`. v3.0.5 registers these only under
  `vector::similarity::*`. The three offending lines are removed and
  a precision note now points readers at the similarity functions
  (and explains how to derive a distance-shaped value:
  `1 - vector::similarity::cosine(...)` etc.). The valid distance
  functions (`chebyshev` / `euclidean` / `hamming` / `manhattan` /
  `minkowski`) remain in place.

`rules/data-modeling.md` and `rules/security.md` returned no CRITs in
re-audit. `rules/vector-search.md` itself was clean (its pass-1 LM/M0
fix held); the only `vector::*` issue lived in `surrealql.md` and is
patched there. Pass-2 IMPORTANTs (e.g. data-modeling's UUID-version
specificity, security's `WITH REFRESH` / RECORD-WITH-JWT-URL gaps,
performance's `REBUILD INDEX` / `CONCURRENTLY` / `DEFER`
under-documentation) are deferred — they are documentation polish or
gaps, not contradictions of upstream — and tracked in the residual
risk lists of the per-rule re-audit reports at
`/tmp/pi-{rule}-v1.5.1-out.md`.

### Migration

Consumers who copied either of the v1.5.1-introduced performance
operator names (`RangeScan` or standalone `Iterate`) need to substitute
the real upstream operator names per the new dual-format block in
`rules/performance.md`. Consumers who copied the `RELATE … MERGE { … }`
form from `rules/graph-queries.md` need to switch to `UPDATE` on the
edge record. Consumers calling `vector::distance::cosine`,
`vector::distance::jaccard`, or `vector::distance::pearson` from
`rules/surrealql.md` need to migrate to the corresponding
`vector::similarity::*` functions (subtract from 1 if a distance-shaped
value is required). The machine-checked version-consistency CI gate
continues to apply.

## [1.5.1] - 2026-05-05

### Fixed (atomic-protocol patch — v1.5.0 Pi-only adversarial-audit CRIT remediation)

A Pi+DeepSeek-V4-Pro:xhigh adversarial audit run against
`rules/data-modeling.md`, `rules/security.md`, `rules/vector-search.md`,
`rules/performance.md`, and `rules/graph-queries.md` after v1.5.0
returned 5/5 NO-GO with 21 CRITs total — hallucinations beyond the
mechanically-grepped v1.4.4 patterns. v1.5.1 patches every CRIT.

- **`rules/vector-search.md`** (2 CRITs) — HNSW parameter table swapped
  `LM` and `M0`. `LM` was documented as "Max connections at layer 0,
  default `2*M`"; the parser actually treats `LM` as the **Minkowski
  distance order** (only meaningful with `DIST MINKOWSKI`) and `M0`
  as the layer-0-connections clause (default `2*M`). The full HNSW
  parameter list now lists both `M0` and `LM` with their correct
  semantics, and a precision note flags the pre-v1.5.1 conflation so
  copied snippets can be repaired.
- **`rules/data-modeling.md`** (2 CRITs) — (a) the §"Schema Modes"
  table conflated schema enforcement (`SCHEMAFULL` / `SCHEMALESS`)
  with table type markers (`TYPE NORMAL` / `TYPE RELATION` /
  `TYPE ANY`) into a single 5-row "modes" table, implying mutual
  exclusivity. They are orthogonal — a table can be `TYPE RELATION
  SCHEMAFULL`. The section now splits into two tables with a note
  on combination. (b) The social-feed example used
  `->follows->user->wrote->post.*` against a schema that defines
  only `follows` and `likes` edges — no `wrote` edge — so the query
  failed at runtime. The example now uses the record-link form
  (`SELECT * FROM post WHERE author IN (SELECT VALUE ->follows->user
  FROM user:alice)`) and adds a comment on what to define if you
  want the `wrote`-edge form instead.
- **`rules/security.md`** (3 CRITs) — (a) §"API Key Authentication"
  documented `DEFINE ACCESS api_access ON DATABASE TYPE API KEY` —
  there is no `TYPE API KEY` in v3.0.5; the section is renamed
  "Bearer-Token Authentication" and now documents the actual
  mechanism: `DEFINE ACCESS … TYPE BEARER FOR [USER | RECORD]` plus
  `ACCESS <name> GRANT FOR USER|RECORD <subject>`. (b) `TYPE JWT`
  examples used `DURATION FOR TOKEN`, which is invalid on JWT
  access — JWT tokens are issued externally, so SurrealDB only
  accepts `DURATION FOR SESSION` here. All three JWT examples were
  rewritten to `DURATION FOR SESSION 12h`. (c) `WITH ISSUER KEY` was
  missing from the JWT-with-record-binding examples — this is
  required for SurrealDB to *issue* tokens under that access method
  rather than only verify them. Both relevant examples now include
  the `WITH ISSUER KEY` clause with prose on its purpose.
- **Cross-fix in `rules/surrealql.md`** — the same `TYPE JWT` +
  `DURATION FOR TOKEN` invalid combination appeared in the DEFINE
  ACCESS examples (lines ~507–514). Both were rewritten to
  `DURATION FOR SESSION` to keep the language reference and the
  security rule in sync.
- **`rules/performance.md`** (8 CRITs) — (1) EXPLAIN output
  documented `Iterate Table` / `Iterate Index` operator names; the
  actual user-facing operator names are `TableScan`, `IndexScan`,
  `RangeScan`, `Iterate`. The interpretation block now lists the real
  names. (2) The `WITH` clause for index hints (`WITH NOINDEX`,
  `WITH INDEX <name>`) was undocumented — added a "Index Hints" sub-
  section under Query Optimization. (3) The `surrealkv://` start
  example included `surreal start file:///var/data/surreal.db` as
  a synonym; `file://` is deprecated in v3 and emits a deprecation
  warning. The `file://` line is removed and the prose flags it
  explicitly. (4) `surreal start --rocksdb-cache-size 4GB` does not
  exist; the cache section now points at the env-var surface
  (`SURREAL_ROCKSDB_BLOCK_SIZE` etc.) and lists the verified
  `surreal start` flags. (5) `surreal start --max-connections 1000`
  also does not exist; the connection-limits section now describes
  bounding concurrency at the proxy / OS layer instead. (6) "SurrealKV
  (default in SurrealDB 3.x for file-based storage)" implied
  automatic substitution; rephrased to "recommended for file-based
  storage" with a note that the no-arg default is `memory`. (7)
  §"Parallel Query Execution" conflated the `SELECT … PARALLEL`
  clause (intra-query worker parallelism) with multi-statement
  request batching (round-trip reduction). Split into two distinct
  subsections. (8) The `FETCH` clause for record-link resolution was
  not discussed at all — added a "FETCH vs Subquery" subsection.
- **`rules/graph-queries.md`** (6 CRITs) — (1) §"Shortest Path
  Queries" claimed *"SurrealDB does not have a native shortest-path
  function"* and built a hand-rolled BFS. v3 has a native
  `..+shortest=target` modifier (with optional `+path`) — the entire
  hand-rolled BFS is replaced with the native form. (2) The §"Recursive
  Traversal Patterns" section showed only fixed-hop chaining and
  missed the v3 mandatory destructuring depth/range syntax
  (`person:alice.{..3}->reports_to->person`,
  `person:alice.{1..3}->reports_to->person`,
  `org:company.{..}.children`). The section now leads with the
  destructuring form and keeps fixed-hop chains as a fallback.
  (3) `.@` recursive destructuring (which builds nested trees in a
  single expression) was missing entirely; added a sub-section with
  examples for both edge traversals and `REFERENCE` link fields.
  (4) The §"Aliased Traversal" example used `AS` *inside* a
  parenthesised arrow filter
  (`->(knows WHERE since > d'2023-01-01' AS recent_connections)->person`),
  which no official v3 test exercises. The example is rewritten to
  the SELECT-projection-position form and a note flags the previous
  form as unverified. (5) Wildcard edge traversal (`->?`, `<-?`,
  `<->?`, `->?->?`) was undocumented; added a sub-section. (6) Path
  modifiers `+collect`, `+path`, `+inclusive` (which compose with
  the depth/range modifier to change what the traversal returns)
  were undocumented; added a sub-section with examples.

The audit was run against v1.4.5 HEAD (`f83ca4e`); each rule's verdict
came from a separate Pi process to avoid cross-rule pollution. Pi
output files are at `/tmp/pi-{rule}-audit.md` for traceability — these
were not committed but are referenced from the v1.5.1 patch surgery.

### Migration

No consumer code changes for callers using the language reference
(`rules/surrealql.md`) — the v1.5.1 cross-fix there only narrows
already-broken examples. Consumers who copied any of the bullets
above (especially HNSW snippets using `LM` for layer-0 connections,
DEFINE ACCESS using `TYPE API KEY`, JWT access using `DURATION FOR
TOKEN`, `surreal start` invocations using `--rocksdb-cache-size` /
`--max-connections` / `file://`, or hand-rolled BFS for shortest
paths) need to apply the corrections noted in each bullet. The
machine-checked version-consistency CI gate continues to apply.

## [1.5.0] - 2026-05-05

### Added (deferred-verification milestone — close v1.4.1 deferrals)

The v1.4.1 patch shrank `rules/editor-tooling.md`, `rules/surrealmcp.md`,
and `rules/surrealml.md` to verified content only and explicitly
deferred per-extension/tool/API detail to v1.5.0. v1.5.0 closes that
deferral by inspecting actual upstream source for each surface and
restoring fully-grounded tables:

- **`rules/editor-tooling.md`** — restored per-editor tables from
  pinned upstream source: `surrealdb/surrealql-language-server@v0.1.2`
  (full `surrealql.*` workspace settings, env-var fallbacks, server
  capabilities, build instructions), `surrealdb/surrealql-vsx@v0.3.0`
  (`surrealdb.surrealql` VS Code extension is grammar+snippets only —
  no commands, no settings, no LSP wiring), `surrealdb/surrealql-zed@v0.1.0`
  (`surrealdb-surrealql` extension config, LSP discovery, asset names),
  and `surrealdb/surrealql-jetbrains` head (plugin id
  `com.surrealdb.surql-jetbrains`, settings page **Settings → Tools →
  SurrealQL**, LSP4IJ wiring). Confirmed `surrealql-language-server` is
  the canonical LSP that first-party extensions wire to (Zed + JetBrains
  both shell out to it by name); `surql-lsp` is a separate community
  crate. Confirmed no first-party Sublime / Neovim / Helix / Emacs
  packages exist — wire-it-yourself sections updated accordingly.
- **`rules/surrealmcp.md`** — restored full tool argument schema table
  from `surrealdb/surrealmcp@v0.4.0`'s `src/tools/mod.rs` `*Params`
  structs. Documents all 20 tools (8 database CRUD, 6 connection
  management, 6 cloud) with required vs optional args, and notes the
  `upsert`/`update` `patch_data`/`merge_data`/`content_data`/`replace_data`
  exclusivity precedence.
- **`rules/surrealml.md`** — restored full Python `SurMlFile`
  constructor + builder API from the published `surrealml 0.0.4` wheel.
  Documents the `Engine` enum (5 variants, with `NATIVE` flagged as
  declared-but-unsupported), the constructor signature, all 8 builder
  methods (`add_column`, `add_normaliser`, `add_output`,
  `add_description`, `add_version`, `add_name`, `add_author`,
  `save`/`to_bytes`), and the static `load`/`upload` + inference
  (`raw_compute`, `buffered_compute`) entry points. Re-asserts what
  does NOT exist: no `from_pytorch`/`from_onnx`/`from_sklearn`/
  `from_keras`/`from_hf` factories, no `ModelMeta`, no `[hf]` extra,
  and no SurrealQL-side `DEFINE MODEL` / `INFO FOR MODEL` / `REMOVE
  MODEL` / `ml::name<version>(...)` invocation form upstream.

### Verified upstream (clones inspected at the v1.5.0 cut)

- `surrealdb/surrealmcp@v0.4.0` (Rust, MCP server)
- `surrealdb/surrealql-language-server@v0.1.2` (Rust, LSP)
- `surrealdb/surrealql-vsx@v0.3.0` (TypeScript, VS Code grammar+snippets)
- `surrealdb/surrealql-zed@v0.1.0` (Rust, Zed extension)
- `surrealdb/surrealql-jetbrains` head (Kotlin, JetBrains plugin)
- `surrealdb/surrealql-tree-sitter` head (tree-sitter grammar)
- `surrealml 0.0.4` (Python wheel from PyPI; `surrealdb/surrealml`
  GitHub repo's tags do not match PyPI release names — wheel was the
  authoritative artefact)
- `surrealdb/langchain-surrealdb@v0.2.1` (Python, cloned but not yet
  used to expand `rules/langchain.md` — that expansion is queued for
  a future release)

### Migration

No consumer code changes. Existing skill consumers using the v1.4.x
shrunken rule files are unaffected; the new content adds detail
without removing or renaming any prior surface. Expanded sections are
strictly additive over the v1.4.5 verified-only baseline.

## [1.4.5] - 2026-05-05

### Fixed (atomic-protocol patch — propagate v1.4.4 SurrealQL corrections to dependent rules)

After v1.4.4 corrected the foundational `rules/surrealql.md`, a
mechanical grep across the rest of the rule set found the same
v1.4.4-class CRIT patterns (`SEARCH ANALYZER` / `MTREE` /
`EXPLAIN FULL` / `string::is::*`) had also propagated into:

- **`rules/data-modeling.md`** -- 16x `SEARCH ANALYZER`, 7x
  `MTREE` (asserted as supported syntax with `DIMENSION` and
  `CAPACITY` parameters), 1x `string::is::email`, plus the
  HNSW/MTREE column in the migration-target table.
- **`rules/security.md`** -- 2x `string::is::email`.
- **`rules/vector-search.md`** -- 1x `SEARCH ANALYZER`. (The
  `MTREE` retraction note already in this file was already
  correct and was retained.)
- **`rules/performance.md`** -- 2x `SEARCH ANALYZER`, 3x
  `EXPLAIN FULL`.

All instances replaced via mechanical pass to match the verified
v3 forms: `FULLTEXT ANALYZER`, HNSW (or `<|K,METRIC|>` brute-force
operator), `EXPLAIN [ ANALYZE ] [ FORMAT TEXT | JSON ] @statement`,
`string::is_*`. The `MTREE Index` section in `data-modeling.md` was
rewritten as an "Exact kNN (no index) -- v3" section pointing at
the brute-force operator.

No 3-way reviewer pass was run for this patch -- the changes were
mechanical replacements of already-verified-wrong patterns from
v1.4.4. The `scripts/check_version_consistency.py` machine-check
catches version-row drift on every CI run from this release
forward.

### Migration
No consumer code changes. The same migration guidance from v1.4.4
applies to anyone who copy-pasted from `rules/data-modeling.md` /
`rules/security.md` / `rules/vector-search.md` /
`rules/performance.md` in v1.4.0 through v1.4.4.

## [1.4.4] - 2026-05-05

### Fixed (atomic-protocol patch — adversarial-review NO-GO findings, batch-4: foundational language reference)

After v1.4.3 shipped, an adversarial review of `rules/surrealql.md`
(the foundational SurrealQL language reference -- highest-impact
failure mode in this skill) returned **NO-GO** with **10 CRITICAL**
findings + 18 IMPORTANT + 9 MINOR. Pi (`deepseek-v4-pro:xhigh`) ran
direct upstream verification against
`surrealdb/docs.surrealdb.com@main/src/content/reference/query-language/...`
on 2026-05-05; Cursor flagged additional internal-consistency drift
between `rules/surrealql.md` and `rules/surrealism.md`; Codex hit
context-window exhaustion on the 2096-line input and produced no
output (false negative; not used).

The same generation-batch failure mode that produced 50+
hallucinations across the rules patched in v1.4.1 / v1.4.2 / v1.4.3
also produced wholesale syntax errors in the foundational reference.
Most of these errors are pre-v3.0.0-beta SurrealQL syntax that the
generation pass inherited from older training data without
verifying against the current grammar.

#### Pervasive syntax corrections
- **`SEARCH ANALYZER` -> `FULLTEXT ANALYZER`** across every `DEFINE INDEX` example, prose mention, and Best Practices section. Upstream `define/indexes.mdx` confirms: "Before SurrealDB version 3.0.0-beta, the `FULLTEXT ANALYZER` clause used the syntax `SEARCH ANALYZER`."
- **`time::from::*` -> `time::from_*`** across every example. Upstream: "Since version 3.0.0-beta, the `::from::` functions now use underscores."
- **`string::is::*` -> `string::is_*`** across every example. Upstream: "Since version 3.0.0-beta, the `::is::` functions now use underscores."
- **`math::PI` / `math::E` / `math::TAU` / `math::INF` / `math::NEG_INF` -> lowercase** (`math::pi`, `math::e`, `math::tau`, `math::inf`, `math::neg_inf`).

#### Fabricated syntax retractions
- **`MTREE` index type**: removed entirely. Upstream `DEFINE INDEX` grammar defines exactly ONE vector index type (`HNSW`); the `MTREE` keyword and its `CAPACITY` parameter were not in the grammar at any v3 version. Replaced with a note pointing at HNSW + the `<|K,METRIC|>` brute-force kNN operator.
- **`string::trim::start` / `string::trim::end`**: removed. Only `string::trim` exists upstream.
- **`math::log2` / `math::log10`**: removed. Upstream has `math::log` (with optional base) and `math::ln`; use `math::log(x, 2)` or `math::log(x, 10)`.
- **`EXPLAIN FULL`**: replaced with the verified standalone form `EXPLAIN [ ANALYZE ] [ FORMAT TEXT | JSON ] @statement`. The `FULL` keyword does not exist in the upstream grammar; the rule's clause-form `SELECT ... EXPLAIN` was retained as the alternate form.
- **`?.` JS-style optional chaining as an operator**: removed from operators table. Replaced with the verified upstream form `spouse.?.name` (period-before-question-mark) on the appropriate access example.
- **`LIKE` / `NOT LIKE` operators**: removed from operators table. Not present in upstream `operators.mdx`, not in the `ifelse` /`where` docs, not in the parser keyword list. Use `~` (fuzzy match) and `CONTAINS` operators.

#### Access-statement structural fix
- **`WITH ISSUER KEY`** moved out of the standalone `TYPE JWT` access example into a `TYPE RECORD WITH JWT` example (the only context in which it is a valid clause per upstream `define/access/record.mdx`). The previous `DEFINE ACCESS api_auth ON NAMESPACE TYPE JWT ... WITH ISSUER KEY ...` would not parse.

#### Type system note
- The `union<...>` and `array<T, N>` type constructors that earlier
  drafts (re-)introduced are not present in upstream; literal types
  use the `|` syntax (`datetime | uuid | "N/A"`). Verified in
  current `Complex Types` table: only `array<T>`, `set<T>`,
  `option<T>`, `record<T>` are documented.

#### Deferred to v1.5.0 (acknowledged gaps; not blocking ship)
- `DEFINE API`, `DEFINE CONFIG`, `DEFINE ACCESS ... TYPE BEARER`
  full sections.
- `ALTER` statement family (16 sub-statements: `ALTER TABLE`,
  `ALTER FIELD`, `ALTER INDEX`, etc.).
- Standalone `ACCESS` statement (`GRANT` / `SHOW` / `REVOKE` /
  `PURGE`) for bearer-grant management.
- `COUNT` index type, `CONCURRENTLY` and `DEFER` clauses on `DEFINE INDEX`.
- `REFERENCE` / `DEFAULT ALWAYS` clauses on `DEFINE FIELD`.
- `INSERT RELATION` variant.
- `DEFINE FUNCTION` `-> @type` return-type syntax + `PERMISSIONS` clause.
- Missing function categories: `encoding::*`, `bytes::*`, `file::*`, `api::*`, `sequence::*`, `set::*`, plus several `string::*`, `time::*`, `math::*`, `search::*` individual functions.

These deferrals are documented in `docs/v1.5.0-roadmap.md` style
(see CHANGELOG history) -- the rule body still teaches the
verified-correct primary surface.

### Security posture
- No new scripts, binaries, or third-party endpoints. All upstream
  verification was via public read-only fetches against
  `docs.surrealdb.com` on 2026-05-05. No new credential surface.
- Removing the wrong access-method `WITH ISSUER KEY` placement
  closes a SurrealQL-failure-at-parse-time surface where a
  developer copy-pasting from v1.4.0 / v1.4.1 / v1.4.2 / v1.4.3
  docs would build code that fails to define the access at all.

### Migration
No consumer code changes. Rule-file content has been replaced;
consumers that copy-pasted from earlier versions should re-pin to
v1.4.4 and re-derive any code from the corrected rule text. In
particular: switch every `DEFINE INDEX ... SEARCH ANALYZER ...` to
`FULLTEXT ANALYZER`; rename every `time::from::X` to
`time::from_X`; rename every `string::is::X` to `string::is_X`;
delete any `MTREE` index definitions and rebuild as `HNSW` (or use
`<|K,METRIC|>` brute-force kNN); remove any `EXPLAIN FULL` /
`?.` / `LIKE` / `NOT LIKE` usage; relocate any `WITH ISSUER KEY`
clause from a JWT-typed access definition into the corresponding
RECORD-typed access.

### Tooling
- `scripts/check_version_consistency.py` (added in commit `b842203`
  before this release) is now wired into `ci.yml` so future
  version-drift across `SKILL.md` / sub-skills / `SOURCES.json` /
  `README.md` badge / `CHANGELOG.md` / `AGENTS.md` is caught
  mechanically on every PR.

## [1.4.3] - 2026-05-05

### Fixed (atomic-protocol patch — adversarial-review NO-GO findings, batch-3)

After v1.4.2 shipped, a third 3-way adversarial review (Codex `gpt-5.5`
xhigh + Pi `deepseek-v4-pro:xhigh` + Cursor Composer 2) of the
**remaining** v1.4.0 SDK content -- the JS / Python / Go / Rust /
Java / .NET / PHP sections in `rules/sdks.md` that were NOT in the
v1.4.0 batch but were generated by the same model in earlier passes
-- returned **3/3 NO-GO** with the same wholesale-hallucination
failure mode. Direct upstream verification (`repo1.maven.org`,
PyPI, npm, Packagist, GitHub raw, NuGet) confirmed the drift.

#### `rules/sdks.md` Java SDK section (full rewrite)
- Corrected Maven version: latest is `2.0.1` (verified 2026-04-28
  via `repo1.maven.org/maven2/com/surrealdb/surrealdb/maven-metadata.xml`,
  not `3.0.0` as previously documented and not `1.0.0-beta.1` as the
  v1.4.2 Kotlin section had said based on a stale Maven Central
  solrsearch result).
- Replaced fabricated API surface (`db.connect("ws://...")`,
  `db.signin("root", "root")`, `db.use("ns", "db")`,
  `db.create("person", Map.of(...))`, `db.queryAsync(...)` returning
  `CompletableFuture<...>`) with the verified upstream API: typed
  `Credential` objects (`RootCredential`, `NamespaceCredential`,
  `DatabaseCredential`, `RecordCredential`, `BearerCredential`),
  chained `useNs(ns).useDb(db)`, typed generics on
  `create(Class<T>, table, value)` and `select(Class<T>, table)`,
  separate `query(sql)` / `queryBind(sql, params)` methods. Removed
  `queryAsync` / `CompletableFuture` (does not exist in source).
- Documented the verified embedded `memory` connection mode plus
  Java 8+ requirement and native-arch list.

#### `rules/sdks.md` PHP SDK section
- Corrected `signin()` keys: upstream uses `"user"` / `"pass"`, not
  `"username"` / `"password"` (silent auth failure with the wrong
  keys).
- Captured the `$token = $db->signin([...])` return value (signin
  returns a token string).
- Switched the SurrealQL `query()` example from a double-quoted
  string (which would interpolate `$min_age` as a PHP variable) to
  single-quoted.
- Replaced string record-IDs with the canonical typed
  `RecordId::create("person", "alice")` and `Table::create("person")`
  per upstream README.

#### `rules/sdks.md` Python SDK section
- Corrected embedded URL schemes: verified upstream
  `examples/embedded/` and `async_embedded.py` source comment pin
  the surface to `mem://` and `file://`. Replaced the previous
  `memory`, `surrealkv://`, and `rocksdb://` examples (none of
  which are documented in current upstream).

#### `rules/sdks.md` Go SDK section
- Removed the fabricated embedded URL schemes (`mem://`,
  `surrealkv://`). Upstream `db.go` documents only WebSocket and
  HTTP connection engines via the `New(url)` entry point; that
  entry point itself is marked `Deprecated` in favor of
  `FromEndpointURLString(ctx, url)`.
- Corrected method names and signatures: `SignIn(ctx, any)` (capital
  `I`, not `Signin`), `Use(ctx, ns, db) error`, `Close(ctx) error`
  (Close takes context). Switched the `Auth` argument from a
  pointer (`&surrealdb.Auth{...}`) to a value, matching the
  upstream comment examples.

#### `rules/sdks.md` SDK Selection Guide matrix
- Java embedded engine: changed from `No` to
  `Yes (memory only)`. Upstream README explicitly claims "Support
  of 'memory' (embedded SurrealDB)" and the getting-started example
  uses `driver.connect("memory")`.
- .NET embedded engine: changed from `No` to
  `Yes (SurrealDb.Embedded.* packages)`. Upstream
  `surrealdb/surrealdb.net` ships
  `SurrealDb.Embedded.InMemory`, `SurrealDb.Embedded.RocksDb`, and
  `SurrealDb.Embedded.SurrealKv` packages.
- Python embedded engine: refined to `Yes (mem:// / file://)` per
  current upstream examples.
- "When to Use Each SDK" Java entry rewritten with verified Maven
  pin (`com.surrealdb:surrealdb 2.0.1`) and embedded support note.

#### `rules/sdks.md` Kotlin section (carryover correction)
- Updated the in-section reference to the published Java SDK fallback
  from `1.0.0-beta.1` to `2.0.1` (the v1.4.2 entry was based on a
  stale Maven Central solrsearch result; `repo1.maven.org`
  metadata is authoritative).

#### `CHANGELOG.md` v1.4.2 entry
- Updated the inline mention of the Java SDK fallback version from
  `1.0.0-beta.1` to `2.0.1` with a note that the v1.4.2 narrative
  was based on a stale solrsearch result and is corrected here.

### Security posture
- No new scripts, binaries, or third-party network endpoints. All
  upstream verification was via public read-only APIs (PyPI,
  rubygems.org, repo1.maven.org, search.maven.org, NuGet,
  Packagist, raw GitHub). No new credential surface.
- Removing the wrong PHP signin keys closes a silent-auth-failure
  surface where a developer copy-pasting from v1.4.2 docs would
  build code that passes type checks, hits the wire, and gets back
  an unauthenticated session.

### Migration
No consumer code changes. Rule-file content has been replaced;
consumers that copy-pasted from v1.4.0 / v1.4.1 / v1.4.2 should
re-pin to v1.4.3 and re-derive any code from the corrected rule
text. In particular: bump Java Maven `<version>` from any of the
older pins (`3.0.0`, `1.0.0-beta.1`) to `2.0.1`; switch the Java
API to the typed `Credential` + `Class<T>` shape; switch PHP
`signin()` keys to `"user"` / `"pass"`; switch Python embedded URLs
to `mem://` / `file://`; switch Go to `FromEndpointURLString` +
`SignIn` + `Close(ctx)`.

## [1.4.2] - 2026-05-05

### Fixed (atomic-protocol patch — adversarial-review NO-GO findings, batch-2)

After v1.4.1 shipped, a follow-up 3-way adversarial review (Codex `gpt-5.5`
xhigh + Pi `deepseek-v4-pro:xhigh` + Cursor Composer 2) of the
**other** v1.4.0 additions -- the Swift / Kotlin / Ruby SDK sections in
`rules/sdks.md` and the `setup-surreal` section in `rules/deployment.md`
-- returned **3/3 NO-GO** with the same wholesale-hallucination failure
mode. Direct upstream verification (PyPI / RubyGems / Maven Central /
GitHub APIs / raw `Package.swift`+`build.gradle.kts`+`gemspec`+`action.yml`
on 2026-05-05) confirmed the drift. This patch shrinks the affected
sections to verified-only content; full API documentation for the
pre-release SDKs is deferred to v1.5.0.

#### `rules/deployment.md` `setup-surreal` section
- The repository `surrealdb/setup-surreal` is a **GitHub Action** (latest tag `v2.0.1`, 2024-12-13) for running SurrealDB inside CI workflows. It is **not** a CLI bootstrap binary.
- Removed all CLI install commands (`brew install surrealdb/tap/setup-surreal`, `cargo install setup-surreal`, `npx @surrealdb/setup-surreal` -- none exist; verified via crates.io / npm registry / Homebrew).
- Removed the fabricated subcommand surface (`init`, `upgrade`, `provision`, `grant`, `helm-values`, `verify`).
- Removed the fabricated TLS-mode flag set, scoped-user provisioning, Helm values export, systemd / launchd / Docker scaffolding tree, and integration table with this skill's `scripts/onboard.py` / `scripts/doctor.py`.
- Replaced with a concise GitHub Action usage block grounded in the upstream `action.yml` (verified inputs: `surrealdb_version`, `surrealdb_port`, `surrealdb_username`, `surrealdb_password`, `surrealdb_auth`, `surrealdb_strict`, `surrealdb_log`, `surrealdb_additional_args`, `surrealdb_retry_count`).

#### `rules/sdks.md` Swift section
- Corrected platform deployment targets: actual upstream `Package.swift` declares iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ (the v1.4.0 documentation said iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+).
- Removed the `from: "1.0.0"` SwiftPM pin: the upstream repo has **no git tags** at the v1.4.2 cut. Pin `branch: "main"` only for development.
- Removed the false claim that `SurrealKit` (the Rust / TypeScript schema toolkit) bundles the Swift client. The two are independent dependencies.
- Removed the entire fabricated single-`Surreal()`-class API (`db.connect`, `db.signin(.root(...))`, `db.live(table:)`, `event.value()`, `event.recordID`, `db.on(.disconnected)`). Verified actual API uses two `actor` clients (`SurrealHTTPClient` and `SurrealWebSocketClient`), a `SignInCredentials` enum, `SurrealModel`-conforming typed values, freestanding macros (`#select`, `#create`, `#update`, `#delete`, `#live`), `SurrealPredicate`, `LiveEvent<T>` with `.decoded` + `.action` (`LiveAction` enum), and `AsyncStream` live queries.
- Detailed API examples deferred to v1.5.0 after upstream publishes a tagged release.

#### `rules/sdks.md` Kotlin section
- Removed Maven coordinates `com.surrealdb:surrealdb-kotlin:0.4.0`: Maven Central has no `surrealdb-kotlin` artifact, and the upstream `gradle.properties` declares `VERSION_NAME=0.1.0-SNAPSHOT`. (The published Java SDK is `com.surrealdb:surrealdb 2.0.1` -- v1.4.2 originally said `1.0.0-beta.1` based on a stale Maven Central solrsearch result; the authoritative `repo1.maven.org` metadata shows `latest=2.0.1` from 2026-04-28. Corrected in v1.4.3.)
- Corrected dep versions to upstream `build.gradle.kts`: Kotlin `2.1.10`, coroutines `1.10.1`, kotlinx-serialization `1.8.0`.
- Corrected KMP targets to verified set: `androidTarget()`, `jvm()`, `iosX64()`, `iosArm64()`, `iosSimulatorArm64()` -- no JS, no non-Apple Native target.
- Removed the fabricated `Surreal()` + `db.connect("rocksdb://...")` / `db.connect("mem://")` embedded-engine claim. The actual `SurrealClientConfig` only takes `httpEndpoint` and `wsEndpoint` strings.
- Removed the fabricated `query<Person>(...): List<Person>` generics, `@JvmOverloads` / `selectBlocking` Java-interop story, and `Flow`-returning live queries. Verified API uses `SurrealClient(config: SurrealClientConfig)`, `JsonElement` returns, `LiveQuerySubscription`, and a `SurrealAuthInput` sealed interface.

#### `rules/sdks.md` Ruby section
- Corrected version pin: latest gem `surrealdb` is `0.7.0` (published 2026-04-01 by SurrealDB authors). The v1.4.0 `~> 1.0` pin would not resolve.
- Corrected required Ruby: `>= 3.2` (verified from `surrealdb.gemspec`); the v1.4.0 documentation said 3.1+.
- Removed the entirely-fabricated `surrealdb-rails` gem, `SurrealDB::Record` ActiveRecord-shaped class, and `where`/`order`/`limit` chain examples. Neither the gem nor a `surrealdb/surrealdb-rails` GitHub repo exists (verified via rubygems.org and api.github.com).
- Corrected the `surrealdb-embedded` companion gem claim. The gem **does** exist on RubyGems at v0.7.0 (published 2026-04-01 by SurrealDB authors, FFI to `libsurrealdb_c`, supports `mem://` / `surrealkv://` / `file://` URLs); the v1.4.0 API surface descriptions for it were hallucinated, so the section now points to the gem with a "API documentation pending v1.5.0 verification" caveat rather than restating the fabricated shape.
- Corrected constructor: `SurrealDB::Client.new(url, **options)` then `.connect` (URL goes to constructor, not `connect`). Auth `signin(credentials_hash)` takes a positional Hash, not keyword arguments.
- Corrected live-query shape: `live(resource)` returns a UUID; subscribe with `db.subscribe(uuid) { |event| ... }` and clean up with `db.kill(uuid)`. The v1.4.0 enumerator-returning `live(...).each do |event|` shape does not exist.

#### `rules/sdks.md` SDK Selection Guide matrix
- Added a "Published release" row showing Swift = No (no tags), Kotlin = No (SNAPSHOT), Ruby = Yes (0.7.0), Java = Yes (beta).
- Marked Swift / Kotlin / Ruby embedded-engine claims as Unverified / No / Unverified (the v1.4.0 matrix incorrectly said all three shipped embedded engines).
- Reframed live-query rows to match verified shapes: Swift `AsyncStream`, Kotlin `LiveQuerySubscription`, Ruby UUID + subscribe.
- Reframed "When to Use Each SDK" entries for Kotlin / Swift / Ruby with v1.4.2 reality: Swift no published tag, Kotlin no Maven release, Ruby gem 0.7.0 (no Rails adapter).

#### Entry-point file syncs
- `AGENTS.md`: deployment.md descriptor reframed; skill version table 1.4.1 -> 1.4.2; onboard.py-agent example version bumped.
- `README.md`: `setup-surreal` capability blurb reframed as GitHub Action; deployment.md descriptor reframed; root version badge bumped.
- `SKILL.md`: `setup-surreal` ecosystem entry reframed; deployment.md descriptor reframed; metadata version bumped.
- `scripts/onboard.py`: deployment.md / langchain.md topics reframed; `new_project` / `ml_inference` / `agent_integration` / `editor_setup` decision trees reframed to v1.4.1+v1.4.2 reality.

#### `SOURCES.json` pins corrected
- `surrealdb/setup-surreal` -> `v2.0.1 (GitHub Action; not a CLI bootstrap)` (date 2024-12-13).
- `surrealdb/surrealdb.swift` -> `no published tag (pre-release; pin branch=main only)`.
- `surrealdb/surrealdb.kotlin` -> `0.1.0-SNAPSHOT (no Maven Central release at v1.4.2 cut)`.
- `surrealdb/surrealdb.rb` -> `0.7.0 (RubyGems surrealdb)` (date 2026-04-01).

### Security posture
- No new scripts, binaries, or third-party network endpoints. All upstream verification was via public read-only APIs (rubygems.org, search.maven.org, api.github.com, raw.githubusercontent.com, pypi.org, crates.io). No new credential surface.
- Removing the fabricated install commands closes a supply-chain risk surface: `brew install surrealdb/tap/setup-surreal`, `cargo install setup-surreal`, and `npx @surrealdb/setup-surreal` would 404 today, but a squatted package at any of those names would have been a vector if a developer copy-pasted from the v1.4.0 / v1.4.1 documentation.

### Migration
No consumer code changes. Rule-file content has been replaced; consumers
that copy-pasted from v1.4.0 / v1.4.1 should re-pin to v1.4.2 and
re-derive any code from the corrected rule text. In particular: drop
`surrealdb-rails` gem references (the gem does not exist), keep
`surrealdb-embedded` gem references but discard any v1.4.0 API
example for it (the gem is real at v0.7.0 but the documented API
shape was fabricated), drop `com.surrealdb:surrealdb-kotlin` Maven
coordinates (use the published Java SDK `com.surrealdb:surrealdb
1.0.0-beta.1` from Kotlin until the KMP package publishes), and drop
any `setup-surreal init / provision / grant` CLI invocations.

## [1.4.1] - 2026-05-05

### Fixed (atomic-protocol patch — adversarial-review NO-GO findings)

A 3-way adversarial review (Codex `gpt-5.5` xhigh + Pi `deepseek-v4-pro:xhigh`
+ Cursor Composer 2; Gemini 3.1 Pro quota-exhausted upstream) of the four
new rule files added in v1.4.0 returned **3/3 NO-GO**. Direct upstream
verification (PyPI, crates.io, npm, GitHub raw READMEs, surrealdb.com docs)
confirmed wholesale drift between the v1.4.0 documentation and current
upstream reality.

This patch shrinks each affected rule to verified-only content with explicit
"pending verification, deferred to v1.5.0" notes for unverified surfaces. No
new content is asserted that has not been read directly from upstream
sources fetched on 2026-05-05.

#### `rules/surrealmcp.md` — rewritten from upstream `README.md`
- Removed `cargo install surrealmcp` and `npm install -g @surrealdb/surrealmcp` (neither exists; crates.io 404, npm 404). Replaced with `cargo install --path .` and Docker.
- Replaced bare `surrealmcp` and `surrealmcp serve` invocations with the verified `surrealmcp start` subcommand.
- Replaced `--namespace` / `--database` / `--bind` / `--auth-token` with verified `--ns` / `--db` / `--bind-address` / `--access-token` (plus `--refresh-token`) flags. The `SURREAL_MCP_CLOUD_*` env-var names retain the `CLOUD_` infix; the CLI flags do not.
- Replaced env-var convention (`SURREAL_USER` / `SURREAL_PASS`) with the upstream-documented `SURREALDB_USER` / `SURREALDB_PASS` / `SURREALDB_URL` / `SURREALDB_NS` / `SURREALDB_DB` plus `SURREAL_MCP_*` server-side prefix.
- Replaced the hallucinated tool catalog (`merge`, `live`, `kill`, `schema.introspect`, `schema.tables`, `schema.table`, `info.db`, `info.ns`, `use`, `signin`) with the upstream-grouped tools: `query`, `select`, `insert`, `create`, `upsert`, `update`, `delete`, `relate`, `connect_endpoint`, `use_namespace`, `use_database`, `list_namespaces`, `list_databases`, `disconnect_endpoint`, plus cloud tools.
- Replaced `surrealmcp ping` with `curl http://localhost:8000/health`.
- Replaced `--max-concurrent-tools` with `--rate-limit-rps` / `--rate-limit-burst`. Replaced `--log-format json` with `RUST_LOG`.

#### `skills/surrealmcp/SKILL.md` — reconciled with the rule
- Updated quick-start, host-config, env vars, and tool catalog to match the rewritten rule. Reconciled `mcpServers` shape across rule and sub-skill.

#### `rules/langchain.md` — rewritten from upstream `README.md` + PyPI
- Removed entire JavaScript / TypeScript section. The `@langchain/surrealdb` npm package does not exist (registry 404).
- Removed `AsyncSurrealDBVectorStore`, `SurrealChatMessageHistory`, and `SurrealHybridRetriever` classes (none exist upstream).
- Replaced `from_endpoint()` / `from_client()` factory methods with the verified `SurrealDBVectorStore(embeddings, conn)` constructor.
- Corrected dependency claims: `langchain-core ~= 1.1.0` and `surrealdb ~= 1.0.8` (v1 SDK, not v2). Python `>= 3.10, < 4.0`.
- Corrected pip extras: at v0.2.1 the upstream `pyproject.toml` declares **no** `[project.optional-dependencies]`, so `[openai]`, `[huggingface]`, and `[graph-qa]` are all silent no-ops in pip. The README mentions a `[graph-qa]` extra (depends on `langchain-classic`) but the package metadata does not ship it; install `langchain-classic` explicitly until upstream wires the extra.
- Replaced `filter=` kwarg with the verified `custom_filter=`.

#### `rules/surrealml.md` — shrunk to scope-summary; v1.4.0 claims retracted
- Removed all `DEFINE MODEL` / `INFO FOR MODEL` / `REMOVE MODEL` SurrealQL claims. The SurrealDB v3 `DEFINE` statement list (verified at `https://surrealdb.com/docs/surrealql/statements/define`) contains ACCESS, ANALYZER, API, BUCKET, CONFIG, DATABASE, EVENT, FIELD, FUNCTION, INDEX, MODULE, NAMESPACE, PARAM, SCOPE, SEQUENCE, TABLE, TOKEN, USER — there is no `MODEL`.
- Removed `ml::name<version>(...)` invocation form (depends on the non-existent `DEFINE MODEL`).
- Removed `surreal start --user-mem-limit` flag (not in upstream CLI).
- Removed `surreal ml import --name --version` flags (the docs `/cli/ml/import` page 404s; treat the `surreal ml` surface as unstable).
- Removed Python `SurMlFile.from_pytorch / from_onnx / from_sklearn / from_keras / from_hf` factories and the `ModelMeta` class. The actual `surrealml 0.0.4` package uses an `Engine` enum + builder methods on `SurMlFile`.
- Corrected pip extras to the verified `[sklearn]`, `[torch]`, `[tensorflow]`. There is no `[hf]` extra.
- Fixed `DEFINE EVENT` example: `$value` -> `$after.id`. Standard event variables in SurrealDB are `$before`, `$after`, `$event`.

#### `rules/editor-tooling.md` — shrunk to verified-pointer summary
- Both `surrealql-language-server` (v0.1.2 on crates.io, 2026-04-21) and `surql-lsp` (v0.1.1 on crates.io, 2026-03-28) are real; the rule no longer asserts which is canonical.
- Removed the v1.4.0 VS Code command palette (`SurrealDB: Run Selection`, etc.) and settings catalog (`surrealdb.connections`, `surrealdb.activeConnection`, `surrealdb.auth.source`) — the published extension's `package.json` had zero of these registered.
- Removed the unverified `surrealql.toml` config-schema block.
- Removed the unverified `surrealql-language-server lint --format github` CI subcommand and the unverified `--socket <port>` flag.
- Trimmed editor-extension descriptions to discoverability pointers; per-editor command/setting detail is deferred to v1.5.0 after a manual upstream pass per editor.

#### `SOURCES.json` — version pins corrected
- Updated `surrealdb/surrealmcp.release` from `v0.2.0` to `v0.4.0` (verified via `api.github.com/repos/surrealdb/surrealmcp/releases`; tags v0.1.0 through v0.4.0 published 2025-08-21 to 2025-09-05).
- Updated `surrealdb/surrealml.release` from `v0.5.x` to `0.0.4 (PyPI surrealml)`.
- Updated `surrealdb/langchain-surrealdb.release` from `current` to `0.2.1 (PyPI langchain-surrealdb)`.

#### `.github/workflows/release.yml`
- Added `workflow_dispatch` trigger with a `tag` input so an existing release tag can be re-published without the draft-toggle dance. Wired through `actions/checkout` ref, `RELEASE_VERSION`, and the clawhub publish step.

### Security posture
- No new scripts, binaries, or third-party network endpoints. All upstream verification was via `curl` to public APIs (crates.io, PyPI, npm registry, GitHub raw, surrealdb.com docs). No new credential surface.
- The rule rewrites *reduce* the project's exposure: removing fabricated install commands eliminates the user-instruction failure mode where a developer attempts a non-existent `cargo install` or `npm install` (those would 404 today, but a newly-squatted package at one of those names would have been a supply-chain risk). All install paths now resolve to the upstream `surrealdb` GitHub org or Docker Hub.

### Migration
No consumer code changes (the skill ships rules + scripts; no library API). One CI workflow change: `.github/workflows/release.yml` gained a `workflow_dispatch` trigger so existing release tags can be re-published without the draft-toggle dance. Rule-file content has been replaced; consumers that copy-pasted from v1.4.0 should re-pin to v1.4.1 and re-derive any code from the corrected rule text. The `skills/surrealmcp/SKILL.md` quick-start has changed shape — update any host MCP config to use the verified env-var names (`SURREALDB_*`) and the `surrealmcp start` subcommand.

## [1.4.0] - 2026-05-03

> **Note (2026-05-05):** this release contained substantial drift from
> the actual upstream APIs across multiple new sections:
>
> - **`rules/surrealmcp.md`, `rules/editor-tooling.md`, `rules/langchain.md`,
>   `rules/surrealml.md`** -- hallucinated install commands, CLI flags,
>   env-var names, tool catalogs, SurrealQL syntax, Python class names,
>   and pip extras. **Retracted in v1.4.1.**
> - **`rules/sdks.md`** Swift / Kotlin / Ruby SDK sections -- hallucinated
>   Maven coordinates, version pins, platform deployment targets, embedded
>   engine support, API surfaces (`Surreal()` class shape, `db.connect`,
>   `db.live(table:)`, `event.value()`), and companion gems
>   (`surrealdb-rails`; `surrealdb-embedded` is real but the v1.4.0
>   API documentation for it was hallucinated). **Retracted in
>   v1.4.2.**
> - **`rules/deployment.md`** `setup-surreal` section -- documented the
>   project as an opinionated CLI bootstrap binary with `init` /
>   `provision` / `grant` / `helm-values` / `verify` subcommands and
>   `brew` / `cargo` / `npx` install paths. The actual repository is a
>   GitHub Action for CI (`uses: surrealdb/setup-surreal@v2`).
>   **Retracted in v1.4.2.**
>
> Adversarial review found the drift on the next pass; v1.4.1 + v1.4.2
> ship verified-only rewrites grounded in upstream READMEs and package
> registries. **Read the v1.4.2 and v1.4.1 entries above for the
> corrected surfaces; do not copy-paste from the v1.4.0 capability
> description that follows.**

### Major (ecosystem expansion)
- New rule **`rules/surrealmcp.md`** + sub-skill **`skills/surrealmcp/SKILL.md`** covering the official Model Context Protocol server for SurrealDB. Tool catalog (`query`, `select`, `create`, `update`, `merge`, `delete`, `relate`, `live`, `kill`, `schema.introspect`, `schema.tables`, `schema.table`, `info.db`, `info.ns`, `use`, `signin`), stdio + Streamable HTTP transports, host-config snippets for Claude Code, Claude Desktop, Cursor, Codex CLI, OpenCode, Amp, Continue, Windsurf.
- New rule **`rules/editor-tooling.md`** covering `surrealql-language-server`, `surrealql-tree-sitter`, and the official editor extensions: VS Code / Cursor / Windsurf / VSCodium (`surrealql-vsx` grammar, Marketplace + OpenVSX), JetBrains (`surrealql-jetbrains`), Neovim (`surrealql-neovim` + `nvim-treesitter`), Helix (`surrealql-helix`), Sublime Text (LSP-Sublime), Zed (`surrealql-zed`), Emacs (`surrealql-emacs`). Includes `surrealql.toml` config schema and CI lint pattern.
- New rule **`rules/langchain.md`** covering `langchain-surrealdb` (Python) and `@langchain/surrealdb` (JS): vector store, retrievers (similarity / MMR / score-threshold), hybrid retriever (vector + keyword + graph), chat message history, async API, multi-tenant permissioning via DEFINE ACCESS.
- New rule **`rules/surrealml.md`** covering SurrealML model authoring (PyTorch / ONNX / scikit-learn / TensorFlow / HuggingFace), `.surml` artifacts, DEFINE MODEL, `ml::name<version>(...)` invocation, computed-field embeddings, BEFORE-write events, version rollouts via SurrealKit, comparison with Surrealism extensions.
- `rules/sdks.md` expanded with full **Swift**, **Kotlin / JVM**, and **Ruby** SDK sections (installation, connection, auth, CRUD, live queries, framework integration patterns: SwiftUI, Android lifecycle, Rails / ActiveRecord, Sidekiq pooling). Decision matrix updated from 7 columns to 10.
- `rules/deployment.md` adds the **`setup-surreal`** opinionated bootstrap CLI: project scaffolding, storage-engine validation, TLS modes (`none` / `self-signed` / `letsencrypt` / `custom`), Helm values export, scoped-user provisioning, integration map with this skill's scripts, production checklist.

### Major (upstream sync)
- Upstream sync to 2026-05-03 covering five changed repos since the 1.3.1 snapshot:
  - `surrealdb/surrealdb`: +38 commits on `main` past v3.0.5 toward v3.1.0-alpha (HEAD `a97d3af`, 2026-04-29). v3.0.5 remains the latest tagged release.
  - `surrealdb/surrealist`: surrealist-v3.7.4 -> surrealist-v3.8.5 (HEAD `3699b2d`, 2026-05-01). Continued query/explorer/designer iteration; signed release artifacts retained.
  - `surrealdb/surrealdb.py`: v2.0.0-alpha.1 -> v2.0.0 GA (HEAD `6e45a82`, 2026-05-02). SurrealDB 3.x feature support, Python 3.9 dropped, structured error handling, musl Linux wheel support, WS session transaction-id fix, Pydantic Logfire instrumentation example.
  - `surrealdb/surrealdb.go`: +8 commits on `main` since v1.4.0 (HEAD `aef39d3`, 2026-04-30). v1.4.0 still the latest tagged release; pin to v1.4.0 for stability.
  - `surrealdb/surrealkit`: v0.5.0 -> v0.6.0 (HEAD `28f5a1c`, 2026-05-03, pre-release). Iterative patch releases plus procedural-macro publish workflow in CI; CLI surface unchanged.

### Added
- `skills/surrealmcp/SKILL.md` sub-skill manifest mirroring the surrealkit / surrealfs / surreal-sync / surrealism pattern.
- `SOURCES.json` now tracks `surrealdb/surrealmcp`, `surrealdb/surrealml`, `surrealdb/surrealql-language-server`, `surrealdb/surrealql-tree-sitter`, `surrealdb/surrealql-vsx`, `surrealdb/surrealql-jetbrains`, `surrealdb/surrealql-neovim`, `surrealdb/surrealql-zed`, `surrealdb/surrealql-helix`, `surrealdb/surrealql-emacs`, `surrealdb/langchain-surrealdb`, `surrealdb/setup-surreal`, `surrealdb/surrealdb.swift`, `surrealdb/surrealdb.kotlin`, `surrealdb/surrealdb.rb`. All 23 tracked repos resolve via `gh api` -- no 404s in `check_upstream.py`.
- `scripts/onboard.py` capability list and rule index extended with `surrealml`, `surrealmcp`, `editor-tooling`, `langchain`. Decision-tree manifest gains `ml_inference`, `agent_integration`, `editor_setup`, `rag_pipeline` entries.
- `AGENTS.md` decision trees for: deploying ML models, AI agent integration via MCP, editor / IDE setup, LangChain RAG pipelines.

### Changed
- `SOURCES.json`, `SKILL.md`, sub-skill manifests under `skills/*/SKILL.md`, `README.md`, and `AGENTS.md` synced to the 2026-05-03 provenance.
- `rules/sdks.md`: Python SDK section promoted to v2.0.0 GA. Go SDK section calls out the unreleased main HEAD past v1.4.0 explicitly. New Swift / Kotlin / Ruby sections; decision matrix expanded.
- `rules/surrealist.md`: pinned to v3.8.5 with current snapshot date.
- `rules/surrealkit.md` and `skills/surrealkit/SKILL.md`: pinned to v0.6.0 pre-release with continuity note that the public CLI surface is unchanged.
- `rules/deployment.md`: added `setup-surreal` section between configuration flags and Docker deployment.
- `README.md`: feature bullet count updated to 12+ SDKs, new sub-skill sections (SurrealMCP, SurrealML, Editor Tooling, LangChain), architecture tree reflects new `rules/` and `skills/` files.

### Security
- **No regression to declared security posture.** All v1.4.0 changes are documentation-only -- no new scripts, no new binaries vendored, no new third-party network endpoints called by the skill itself, no new credential surface, no new file-write paths, no new shell-execution surface, no obfuscated code, no binary blobs, no `curl | sh` instructions, no minified scripts. The new rule files document upstream tools whose installation continues to use auditable channels (Cargo, Homebrew, npm registry, Docker Hub). CI and Release workflows retain `permissions: contents: read` (Release also explicitly scopes its publish step). `check_upstream.py` continues to use the GitHub API via the `gh` CLI only.
- New rules' security guidance: `rules/surrealmcp.md` recommends scoped DB users (DEFINE USER ... ROLE EDITOR/VIEWER), TLS for HTTP transport, bearer tokens, and never running MCP as root in production. `rules/langchain.md` recommends row-level DEFINE PERMISSIONS for multi-tenant vector stores. `rules/surrealml.md` recommends DEFINE PERMISSIONS on model functions to scope inference. `rules/deployment.md` `setup-surreal` checklist requires non-`memory` storage, non-`none` TLS, and scoped DB users for production.
- All upstream version bumps in this release are equal-or-better on the security axis: surrealdb.go retains the v1.4.0 SQL-injection sanitization in restore (#375); surrealdb.py v2.0.0 GA tightens error-handling types; surrealist v3.8.5 keeps signed release artifacts.
- SKILL.md security frontmatter (`no_network=false note`, `no_credentials=false note`, `no_env_write=true`, `no_file_write=false note`, `no_shell_exec=false note`, `scripts_auditable=true`, `scripts_use_pep723=true`, `no_obfuscated_code=true`, `no_binary_blobs=true`, `no_minified_scripts=true`, `no_curl_pipe_sh=true`) verified accurate after this revision.

## [1.3.1] - 2026-04-10

### Fixed
- ClawHub registry metadata now declares the skill's required binaries and `SURREAL_*` environment variables under `metadata.openclaw`, matching the documented publish contract and eliminating the `metadata: null` registry state from `1.3.0`
- Root `SKILL.md` now carries an explicit top-level `version` field in addition to the repo-local metadata block for better registry compatibility
- Release workflow now publishes through the supported `clawhub` CLI flow instead of the dead `api.clawhub.ai/v1/skills/publish` endpoint

### Changed
- Version metadata bumped to `1.3.1` across the root manifest, sub-skills, AGENTS.md, README badge, and SOURCES.json

## [1.3.0] - 2026-04-10

### Major
- SurrealDB v3.0.5: documented `REMOVE CONFIG`, wider `ALTER` coverage, planner pushdown fixes, `$parent` fixes, computed field fixes, edge query ordering fixes, GraphQL literal fields, and related patch work
- SurrealKit v0.5.0 added as a first-class part of the skill: desired-state schema sync, rollout-based migrations, seeding, and declarative database/API tests
- Release and CI workflows hardened: explicit least-privilege permissions, version-consistency validation, smoke tests, and no in-workflow manifest mutation before publish

### Fixed
- `scripts/check_upstream.py`: short baseline SHAs now compare correctly against full GitHub commit SHAs
- `scripts/check_upstream.py`: falls back to latest Git tag when a repo does not publish GitHub Releases
- `scripts/doctor.py` and `scripts/schema.py`: normalize user-facing HTTP endpoints to SurrealDB WebSocket RPC URLs before connecting
- `scripts/schema.py`: restored the documented `introspect`, `tables`, and `table` commands
- `scripts/onboard.py`: version now comes from root `SKILL.md`, and the agent manifest now reflects live prerequisites and the full script/rule set

### Changed
- README, AGENTS.md, SKILL.md, and SOURCES.json synced to upstream state as of 2026-04-10
- Added `rules/surrealkit.md` and `skills/surrealkit/SKILL.md`
- Surrealist docs updated to v3.7.4; JavaScript SDK docs updated to v2.0.3
- Security metadata corrected: file writes are declared accurately, remote shell installer references removed from active documentation, and publish workflow now validates repository content instead of editing it at release time

## [1.2.1] - 2026-03-13

### Major
- SurrealDB v3.0.4: 20 fixes/features including GraphQL Subscriptions (#7027),
  BM25 search::score() compaction fix (#7057), HNSW index compaction fix (#7077),
  UPSERT conditional count fix (#7056), LIMIT with incomplete WHERE fix (#7063),
  v2 subcommand for migration assistance (#7058), concurrent startup retry (#7055),
  distributed task lease race fix (#6501), and performance improvements (#7018)
- JS SDK v2.0.2: streamed imports/exports (#563), blob import support (#568),
  single value for StringRecordId (#569)
- Surrealist v3.7.3: PrivateLink support, streamed import/export, org ID in
  settings, node rendering perf, dataset rename, improved ticket display
- Surreal-Sync: SurrealDB v3 compatibility, PostgreSQL foreign key relations,
  TOML config, Neo4j relationship fix, improved test infrastructure

### Changed
- SOURCES.json synced to HEAD 2026-03-13 (all 7 repos updated)
- rules/surrealql.md: v3.0.4 patch notes section (20 items)
- rules/sdks.md: JS SDK v2.0.2 changes
- rules/surrealist.md: v3.7.3 version and features
- rules/surreal-sync.md: v3 compatibility notes

## [1.2.0] - 2026-03-03

### Major
- SurrealDB v3.0.2 patch release (2026-03-03): 13 fixes/features documented in
  rules/surrealql.md including None-on-missing-record, bind parameter resolution
  in MATCHES operator, datetime setter functions, configurable CORS, --tables-exclude
  export flag, compound unique index fix, DELETE live event permissions, DEFINE
  FUNCTION parsing fix, transaction timeout enforcement, executor optimizations
- Go SDK v1.4.0: SurrealDB v3 structured error handling (new ServerError type),
  identifier sanitization in restore to prevent SQL injection
- JS SDK: RPC query stat duration parsing fix (#560)

### Changed
- SOURCES.json synced to HEAD 2026-03-03 (surrealdb d454269ecb11, surrealdb.js
  501b167b2155, surrealdb.go a7bf54bc9487)
- Docker image tags use v3 (auto-tracks v3.0.2)
- v3.1.0-alpha tracking updated (error chaining, SurrealValue, timestamp refactor)

## [1.1.1] - 2026-02-26

### Fixed
- Python SDK release corrected from v2.0.0 to v2.0.0-alpha.1 (pre-release alpha,
  not GA). Python 3.9 dropped; minimum is now 3.10. Added Logfire instrumentation note.

### Added
- SurrealDB v3.1.0-alpha behavior change: SELECT on non-existent records now returns
  NONE instead of error (#6978). Documented in rules/surrealql.md with migration note.

### Changed
- SOURCES.json synced to HEAD 2026-02-26 (surrealdb fa22ecf0ae93, surrealdb.py b21302c05565)
- AGENTS.md: added context comment on production 0.0.0.0 bind address

## [1.1.0] - 2026-02-25

### Major
- JavaScript SDK v2.0.0 GA released (no longer beta). Updated from beta tag to
  stable: `npm install surrealdb` (not @beta). Full SurrealDB 3.0.1 support,
  client-side transactions, multi-session, query builder, streaming responses.
- Python SDK v2.0.0 released. WebSocket session transaction ID fix, musl Linux
  support for Alpine/containers, improved error handling, README cleanup.

### Changed
- rules/sdks.md: JS v2 section title changed from "beta" to "GA -- recommended
  for new projects". Install commands changed from surrealdb@beta to surrealdb.
  All @surrealdb/wasm@beta and @surrealdb/node@beta tags removed.
- rules/sdks.md: Python SDK updated to v2.0.0 with changelog
- rules/surrealql.md: v3.1.0-alpha tracking updated with error chaining
  infrastructure (#6969), SurrealValue derive convenience (#6970), wasmtime
  update (#6973)
- SOURCES.json: All repos synced to HEAD 2026-02-25. Removed surrealdb.js@beta
  entry (v2 is now GA). surrealdb.js release v2.0.0, surrealdb.py release v2.0.0.
- Additional credential warning markers on remaining unwarned root/root examples
  in SKILL.md workflow section and AGENTS.md decision tree
- deployment.md: --bind flag default annotated with local dev recommendation

## [1.0.6] - 2026-02-24

### Added
- SurrealDB v3.0.1 patch notes in rules/surrealql.md: duration arithmetic, computed
  field index prevention, record ID dereference fix, error serialization, GraphQL
  string enum fix, root user permission fix, parallel index compaction, WASM compat,
  RouterFactory trait for embedders
- v3.1.0-alpha tracking notes (main branch: planner tidy-up, test fixtures, code coverage)
- JS SDK v2.0.0-beta.2 changes: ne (!=) operator, error cause property, createWorker
  factory for Vite-compatible Web Worker engines, minimum SurrealDB version bump to 2.1.0
- Python SDK error handling improvements (#233)

### Changed
- All upstream repos synced to HEAD as of 2026-02-24
- SOURCES.json: surrealdb release updated v3.0.0 -> v3.0.1, added main_tracking field
- SOURCES.json: surrealdb.js@beta release updated beta.1 -> beta.2
- Docker image tags updated from v3.0.0 to v3 (tracks latest v3.x)
- AGENTS.md: fixed remaining 0.0.0.0 bind address to 127.0.0.1
- rules/deployment.md: fixed remaining 0.0.0.0 bind to 127.0.0.1 with comment
- rules/sdks.md: createWasmWorkerEngines example updated for beta.2 createWorker factory
- rules/sdks.md: added ne operator to Expressions API imports

## [1.0.5] - 2026-02-24

### Added
- Native GitHub Copilot agent skill support (.github/skills/surrealdb/SKILL.md)
  - Follows the open Agent Skills standard (agentskills.io)
  - Auto-loads in VS Code, Copilot CLI, and Copilot coding agent when SurrealDB context detected
  - Available as `/surrealdb` slash command in Copilot chat
  - Progressive disclosure: metadata -> instructions -> rule files on demand
  - Supports project-level (.github/skills/) and personal (~/.copilot/skills/) installation
  - Includes `argument-hint` for guided slash command usage
  - References all 12 rule files via relative paths for Copilot resource loading
  - Quick reference section with SurrealQL essentials for immediate context

### Changed
- README: replaced "append AGENTS.md to copilot-instructions.md" with native Copilot
  agent skills instructions (3 install methods: project, personal, /skills menu)
- README: added Cursor .cursor/skills/ integration (same Agent Skills standard)
- Upstream sync to 2026-02-24:
  - surrealdb/surrealdb: +2 commits (error serialization fix, CI fix)
  - surrealdb/surrealist: +1 commit (strict sandbox option fix)
  - surrealdb/surrealdb.js: +2 commits (version bumps)
- SOURCES.json baselines updated to current HEAD SHAs

## [1.0.4] - 2026-02-22

### Security Fixes (addressing OpenClaw/VirusTotal scan findings)
- SKILL.md frontmatter: changed no_network and no_credentials to false with
  explanatory notes (scripts DO connect to user-specified endpoints)
- SKILL.md frontmatter: added requires.binaries declaring surreal, python3, uv, docker
- SKILL.md frontmatter: added requires.env_vars declaring all SURREAL_* vars
  with sensitive: true on SURREAL_USER and SURREAL_PASS
- Replaced remote shell installer instructions with brew/package manager alternatives
  in SKILL.md, AGENTS.md, README.md, and rules/deployment.md
- Added security notes on remote shell installers (download-and-review alternative documented)
- Added credential warnings on all root/root examples across all files
- Changed bind address from 0.0.0.0 to 127.0.0.1 in quick start examples
- Added SurrealQL injection prevention: _sanitize_identifier() in schema.py
  validates table names against [a-zA-Z_][a-zA-Z0-9_]* before query interpolation
- surrealfs sub-skill: added Security Considerations section covering telemetry
  opt-out (LOGFIRE_SEND_TO_LOGFIRE=false), HTTP binding, pipe command risks,
  sandboxing, credential scoping
- surrealfs sub-skill: added requires.env_vars and security block to frontmatter
- README: corrected security properties table (no_network=false, no_credentials=false)
- README: added Required Environment Variables table with sensitivity markers
- README: added Required Binaries table
- README: added Script Safety section

## [1.0.3] - 2026-02-22

### Added
- Nightly upstream freshness check GHA workflow (.github/workflows/upstream-check.yml)
  - Runs at 06:00 UTC daily, auto-creates/updates GitHub issue when repos drift
  - Manual trigger via workflow_dispatch
- ClawHub/OpenClaw publishing (clawhub.ai registry)
- Security metadata in SKILL.md frontmatter (no_network, no_credentials, scripts_auditable, etc.)
- Registries section in README with skills.sh, ClawHub, OpenClaw install commands
- Security properties table in README
- GitHub topics: openclaw, clawhub, agentskills (replacing lower-value topics)
- Opened surrealdb/surrealdb#6958 for community resource listing

### Changed
- Synced upstream sources to latest HEAD (snapshot 2026-02-22):
  - Surrealist v3.7.1 -> v3.7.2 (migration export fix, misc UI fixes)
  - surrealdb.js WASM SDK updated to 3.x, WebWorker Vite compatibility fix
- Updated provenance tables in AGENTS.md, SKILL.md, README.md
- Updated sub-skills with provenance metadata and corrected upstream CLI syntax
- Updated repo description and homepage on GitHub

## [1.0.2] - 2026-02-19

### Added
- JavaScript/TypeScript SDK v2.0.0-beta.1 coverage in rules/sdks.md
  - Engine-based architecture (createRemoteEngines, createNodeEngines, createWasmEngines, createWasmWorkerEngines)
  - Multi-session support (newSession, forkSession, await using)
  - Query builder pattern (.fields, .where, .fetch, .content, .merge, .replace, .patch)
  - Query method overhaul (.collect, .json, .responses, .stream)
  - Expressions API (eq, or, and, between, inside, raw, surql template tag)
  - Redesigned live queries (.subscribe, for await, .liveOf)
  - Auto token refresh (renewAccess)
  - User-defined API invocation (.api)
  - Diagnostics API (applyDiagnostics)
  - Codec visitor API (valueDecodeVisitor, valueEncodeVisitor)
  - v1 to v2 migration guide table
- Tracked surrealdb.js v2.0.0-beta.1 (SHA 6383698daccf) in SOURCES.json

## [1.0.1] - 2026-02-19

### Added
- SOURCES.json with commit SHAs, release tags, and dates for all 7 upstream repos
- check_upstream.py script to diff current upstream state against skill snapshot
- Source provenance tables in AGENTS.md, SKILL.md, and README.md with dates
- Detailed Claude Code plugin installation instructions (4 methods)

### Fixed
- KNN operator syntax in AGENTS.md (`<|K,EF|>` takes two numeric params, not distance metric)
- Added `--check` alias for `--quick` flag in doctor.py
- Added exit code 1 on unhealthy status in doctor.py

## [1.0.0] - 2026-02-19

### Added
- Initial release of SurrealDB 3 skill for AI coding agents
- Comprehensive SurrealQL reference (rules/surrealql.md)
- Multi-model data modeling guide (rules/data-modeling.md)
- Graph query patterns (rules/graph-queries.md)
- Vector search and RAG patterns (rules/vector-search.md)
- Security and access control guide (rules/security.md)
- Performance optimization guide (rules/performance.md)
- SDK integration patterns for JS, Python, Go, Rust, Java, .NET (rules/sdks.md)
- Deployment and operations guide (rules/deployment.md)
- Surrealism WASM extension development (rules/surrealism.md)
- Surreal-Sync data migration guide (rules/surreal-sync.md)
- Surrealist IDE guide (rules/surrealist.md)
- SurrealFS AI agent filesystem guide (rules/surrealfs.md)
- Python onboard script with setup wizard and agent capabilities manifest
- Python doctor script for environment health checks
- Python schema script for database introspection and export
- Sub-skills: surrealism, surreal-sync, surrealfs
- CI/CD workflows for validation and release
- Universal compatibility with 30+ AI coding agents
