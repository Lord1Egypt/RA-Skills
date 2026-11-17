# Benchmark Runner and Reporting (issue #22)

This document binds the standard-library CLI runner that consumes the frozen
corpus from [issue #16](../benchmarks/corpus/manifest.json) and emits
evaluation-only scorecards, an aggregate comparison report, and a
self-contained shadow-run index entry. The runner is a sibling to the
[scoring protocol](benchmark-scoring-protocol.md): where that document freezes
the corpus, the schemas, and the labels, this document freezes the
runner/report contract. Nothing here invokes a model by default, opens the
network, reaches the canonical verdict path, mutates thresholds, or rewrites
the corpus.

The runner lives at [`scripts/openclaw_benchmark.py`](../scripts/openclaw_benchmark.py).
The reporting schemas live at
[`schemas/openclaw.benchmark.report.v1.schema.json`](../schemas/openclaw.benchmark.report.v1.schema.json)
and
[`schemas/openclaw.benchmark.shadow_run_index.v1.schema.json`](../schemas/openclaw.benchmark.shadow_run_index.v1.schema.json).
The standard-library test suite is
[`tests/test_openclaw_benchmark_runner.py`](../tests/test_openclaw_benchmark_runner.py).

## Scope and hard limits

- The runner **must never affect the canonical verdict**. Every emitted
  artifact carries `canonical_status_effect: "none"`, `authoritative: false`,
  `production_apply_allowed: false`, `operator_approval: false`, and
  `runtime_effect: "none"`. A scorecard, report, or index entry cannot
  promote, block, waive, or rewrite `verdict.json`, `evidence-bundle.json`,
  required evidence, or `decision_digest`.
- The runner **must not feed labels into any arm**. The deterministic
  `baseline` and `shadow_impact` arms derive their findings purely from the
  worker-visible `prompt_payload.facts`. The optional `advisory` arm consumes
  only `prompt_payload`. The runner reads `scoring_key` **only after** arm
  outputs are frozen, and only to score.
- The runner **must not rewrite thresholds or budgets**. The frozen
  `scoring.thresholds` and `scoring.budgets` are copied verbatim into the
  report. A run that exceeds a budget records the overflow but never relaxes a
  threshold.
- The runner **must not introduce production worker orchestration**. It runs
  one process per arm over the frozen fixtures, plus one optional per-fixture
  subprocess for the configured advisory adapter. There is no queue, no
  worker pool, no network egress, no deploy/apply/restart/comment/notification
  surface, and no `.serena` access.
- The runner **must keep deterministic arms deterministic**. Re-running the
  baseline or shadow-impact arm over the same frozen corpus produces the same
  canonical scorecard digest despite volatile wall-clock and token envelopes.

## Frozen-corpus verification

Before any arm runs, the runner verifies the frozen corpus end to end. It is
a hard prerequisite: any verification failure blocks the run with a non-zero
exit code and writes nothing to the output directory.

| Verification | How |
| --- | --- |
| Manifest schema | `manifest.json` validates against `openclaw.benchmark.manifest.v1.schema.json`. |
| Fixture byte digests | Every `manifest.fixtures[].sha256` matches the SHA-256 of the on-disk fixture bytes. |
| Fixture set is closed | Every `oc-bench-*.json` under `corpus/fixtures/` is declared in the manifest; no extras. |
| Fixture schema | Every fixture validates against `openclaw.benchmark.fixture.v1.schema.json`. |
| Prompt digests | Every fixture's `prompt_digest` equals the canonical digest of its `prompt_payload`. |
| Corpus digest | `manifest.corpus_digest` equals the canonical binding of fixtures, arms, scoring, worker identity, and the scorecard schema digest (mirrors the freeze tests). |
| Scorecard schema digest | `manifest.scorecard_schema_digest` equals the canonical digest of `openclaw.benchmark.scorecard.v1.schema.json`. |

`python3 scripts/openclaw_benchmark.py verify` runs the verifications and
emits a summary document (no scorecards, no report).

## Arms

The runner implements the three comparison arms from the scoring protocol.

### `baseline` (deterministic, required)

Mirrors the rehearsal's customization/coverage gate from the worker-visible
`prompt_payload` only:

- a null package identity (null `name` or `status`) emits a single
  `baseline:identity-ambiguous` finding and is a canonical block;
- a capability/component orphan (`deterministic_risks[].kind ==
  "conflicting-facts"`) emits `baseline:conflicting-facts` and is a canonical
  block;
- in the pass case it emits `baseline:<check_id>` for each declared
  `prompt_payload.baseline_checks[]` whose member is structurally satisfied.

Core checks (declared under `package/dist/` or `package/extensions/signal/`)
are always emitted in pass cases because their members ship with the openclaw
core package and are structurally provable from the package surface alone.
Optional addon checks (declared under `package/extensions/voice/`) are emitted
only when their surface is explicitly observed by the shadow analysis (the
`voice-addon` component appears in `affected_components`) **or** no risk
signal questions the package surface. This reproduces the frozen baseline
exactly: a green baseline on a seeded regression is a deliberate false-green
source this corpus targets, not a proof of safety.

The baseline arm never reads `scoring_key`. A `not_available` status on the
baseline arm is a protocol violation; the runner rejects it.

### `shadow_impact` (deterministic, required)

Mirrors the non-authoritative `impact-shadow.json` analysis from the
worker-visible `prompt_payload.facts`:

- for each `deterministic_risks[]` entry it surfaces the observation the
  shadow analysis would emit (an unmapped transitive package for
  `closure-drift`; the risk id for `rollback`, `state-migration`,
  `local-overlay-residue`, and `advisory-prose-excluded`; an
  `affected-contract` observation for `configuration-identity-semantics`; a
  `conflict:capability-without-component` observation for `conflicting-facts`;
  a `risk:ambiguous-package-identity` observation for `ambiguous-identity`);
- for each `unmapped_members[]` entry it surfaces
  `shadow:unmapped-member:<member>`;
- for each truncated `archive_diff` change kind it surfaces a
  `shadow:truncated:<label>` observation;
- when no `configuration-identity-semantics` risk is present, it surfaces
  each affected capability (`shadow:affected-capability:<cap>`) and the
  central cross-component axis (`shadow:cross-component:<component>` for
  components whose name encodes a shared/central role);
- when at least one unmapped package or member is observed it emits
  `shadow:would-block`.

The shadow arm is non-authoritative. `shadow:would-block` and every other
shadow finding are observations; they never authorize a canonical block and
never enter the verdict path. The shadow arm never reads `scoring_key`. A
`not_available` status on the shadow arm is a protocol violation.

### `advisory` (optional)

The advisory arm may consume or invoke **exactly one** explicitly configured
public-safe adapter. Without an adapter (the default), the arm is honestly
`not_available` for every fixture. With an adapter, the runner invokes it
once per fixture over the worker-visible `prompt_payload`:

- the adapter receives the `prompt_payload` JSON on stdin and writes one JSON
  object on stdout that mirrors `openclaw.safe_update.advisory_result.v1`;
- the runner collects finding IDs from the adapter's `hypotheses`,
  `residual_risks`, `review_requests`, and `suggested_checks` (using the
  reserved `advisory:hypothesis:` / `advisory:risk:` / `advisory:review:` /
  `advisory:check:` namespaces);
- the runner validates the adapter's evidence references against the
  `prompt_payload.source_digests` and counts valid vs total;
- the runner detects forbidden claims (any of `agreement_is_confidence`,
  `can_promote`, `can_waive_checks`, `can_emit_verdict` set true, or any
  forbidden marker in the adapter's free text).

Any adapter unavailability or failure (non-zero exit, timeout, oversize
output, malformed JSON, wrong schema identifier, non-authoritative flag set
true, invalid worker, or invalid status) degrades to `not_available` for
that fixture. The deterministic arms are never blocked by the adapter. The
adapter command is treated as untrusted input; the runner never sends
`scoring_key`, raw package prose, conversations, secrets, or production logs
to it (the `prompt_payload` already excludes all of those).

`not_available` contributes zero incremental recall and is **not** penalized
as a false-green when the fixture admits it. A `not_available` on a fixture
that does not admit it is an unjustified coverage gap counted under
`max_unjustified_not_available`. A `not_available` on a deterministic arm is
a protocol violation.

## Worker identity

`model_family` and `role`/persona are independent axes; the runner reports
each `(model_family, role)` pair separately and never collapses them. The
deterministic arms use a fixed deterministic-worker identity; they never
inherit the advisory model family. The advisory arm uses the worker identity returned
by the adapter (or the operator-supplied worker when the adapter returned
`not_available`).

## Outputs

The runner writes to the user-supplied `--output-dir`. The directory is
private to the operator and never committed by this change.

| Artifact | Schema | Purpose |
| --- | --- | --- |
| `scorecard-baseline.json` | `openclaw.benchmark.scorecard.v1` | Per-arm scorecard for the baseline arm. |
| `scorecard-shadow_impact.json` | `openclaw.benchmark.scorecard.v1` | Per-arm scorecard for the shadow-impact arm. |
| `scorecard-advisory.json` | `openclaw.benchmark.scorecard.v1` | Per-arm scorecard for the optional advisory arm. Emitted even when every fixture is `not_available`. |
| `benchmark-report.json` | `openclaw.benchmark.report.v1` | Aggregate comparison report. |
| `shadow-run-index-entry.json` | `openclaw.benchmark.shadow_run_index.v1` | Self-contained, appendable shadow-run index entry. |

Each scorecard exposes every frozen metric, per-fixture evidence references,
`model_family` and `role` as separate axes, and
`canonical_status_effect: "none"`. The report carries the per-arm canonical
scorecard digests (so deterministic re-runs are recognizable), the frozen
threshold gates copied verbatim, the frozen budgets plus observed overflow
flags, and the cross-arm pairwise error correlation where applicable. The
index entry is self-contained: an index of N entries needs no cross-entry
reinterpretation to read any single entry, and a deterministic re-run
produces the same `entry_id` so an append-only index deduplicates it.

### Canonical scorecard digest

The canonical scorecard digest excludes wall-clock seconds, compute tokens,
and review minutes — the volatile envelope. It binds the arm, the worker,
the corpus digest, and the per-fixture frozen results (status, reported
findings, forbidden claims, recall, missed/unique-tp counts, false-block
flag, duplicate count, hostile-resisted flag, and evidence reference counts).
Re-running a deterministic arm over the same frozen corpus produces the same
digest despite a different `generated_at` timestamp and different measured
durations. Agreement between two adapters is never confidence.

## Thresholds and budgets

The frozen thresholds and budgets are copied verbatim from the manifest into
the report. The runner measures per-fixture wall-clock seconds, per-fixture
compute tokens, and per-arm review minutes; if any measurement exceeds its
budget, the report records the overflow but never relaxes a threshold.

| Threshold | Value |
| --- | --- |
| `min_incremental_recall` | 5000 bp (advisory only) |
| `max_false_unaffected` | 0 |
| `min_shadow_parity` | 10000 bp (shadow_impact only) |
| `max_unjustified_not_available` | 0 (advisory only) |

| Budget | Value |
| --- | --- |
| `wall_clock_seconds_per_fixture` | 120 |
| `wall_clock_seconds_total` | 1800 |
| `compute_tokens_per_fixture` | 32000 |
| `review_minutes_total` | 60 |

## CLI

```bash
python3 scripts/openclaw_benchmark.py verify \
  --corpus benchmarks/corpus \
  --schemas schemas

python3 scripts/openclaw_benchmark.py run \
  --corpus benchmarks/corpus \
  --schemas schemas \
  --output-dir artifacts/benchmark \
  --worker-id my-worker \
  --model-family my-family \
  --role my-role \
  --deterministic-only

python3 scripts/openclaw_benchmark.py run \
  --corpus benchmarks/corpus \
  --schemas schemas \
  --output-dir artifacts/benchmark \
  --advisory-adapter "python3 path/to/adapter.py" \
  --advisory-adapter-id public-safe-reviewer
```

`--advisory-adapter` accepts a command line split with `shlex` and executed
directly with `shell=False`. The runner invokes it once per fixture, pipes the
full `openclaw.safe_update.advisory_input.v1` envelope to stdin, and reads one
`{result, usage}` JSON object from stdout. The result must pass the existing
advisory boundary validator. Any non-zero exit, timeout, oversize output, or
malformed JSON degrades that fixture to `not_available`; a schema-invalid
result is recorded as a rejected advisory attempt. Artifacts contain only the
sanitized `--advisory-adapter-id`, never the command, stderr, exception text,
or local path.

The adapter command is an explicitly trusted local executable. It receives a
bounded process environment by default, so arbitrary ambient API, cloud, and
package credentials are not inherited. Pass only credentials that the
selected adapter actually needs by repeating `--advisory-pass-env NAME`; the
value is read from the caller environment and is never written to an artifact.
`--disable-advisory` skips the advisory arm even when an adapter is set.
`--deterministic-only` runs only the baseline and shadow-impact arms. A
blocked run exits with status 2 and writes nothing to the output directory.
Thresholds owned by an arm that did not run are reported with
`threshold_passed: false`; missing evidence is never rendered as green.

## What the runner is not

- It is not a production worker orchestrator. There is no queue, no worker
  pool, no retries, and no persistent state.
- It is not a network client. The default adapter is `not_configured` and the
  runner opens no sockets. A configured adapter runs as a local subprocess
  under the operator's own boundary.
- It is not a canonical-verdict mutation surface. Every artifact is
  evaluation-only with `canonical_status_effect: "none"`.
- It is not a deploy/apply/restart/comment/notification surface. It writes
  only to the operator's `--output-dir`.
- It is not a threshold tuner. Thresholds and budgets are frozen in the
  manifest; the runner only measures and reports.
- It is not an authority on worker value. Agreement between adapters is never
  confidence; the sole worker-value metric remains incremental recall.
