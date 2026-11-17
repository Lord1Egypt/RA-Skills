---
name: openclaw-safe-update
description: Rehearse an OpenClaw update with exact package evidence, installation coverage, and existing Kova reports. Use before an upgrade to identify compatibility gaps and prepare a migration, rollback, and post-start verification plan.
metadata: {"openclaw":{"homepage":"https://github.com/pdurlej/openclaw-skill-safe-update","requires":{"bins":["python3","node","npm"]}}}
---

# OpenClaw Safe Upgrade Rehearsal Kit

Prepare evidence for an OpenClaw update while keeping production unchanged. Every real installation can differ through channels, plugins, MCPs, memory, providers, services, wrappers, and local customizations. This workflow is a dry run: make those dependencies explicit, find unproven risks before apply, and treat the generated verdict as input to an operator decision, never as permission to update.

## Safety Contract

- Do not run `openclaw update`, install packages globally, repair dependencies, deploy, restart services, or mutate live configuration.
- Do not execute package lifecycle scripts or code from downloaded archives.
- Do not include secrets, private conversations, live configuration values, or raw production logs in cloud reviews or artifacts.
- Package resolution uses isolated project, user, and global npm configuration plus a bounded subprocess environment; it does not forward ambient API, cloud, or npm credentials.
- When package metadata, integrity, required packages, customization checks, installation coverage, or required evidence are missing, return `blocked` and stop instead of guessing.
- Stop at `ready_for_operator_plan`. A separate, explicit operator approval is required for every live mutation.

Read [references/evidence-contract.md](references/evidence-contract.md) before changing the artifact schema or interpreting a verdict.

Resolve bundled helpers from `{baseDir}`, the installed skill directory. Keep
input and output paths in the operator's working directory. Kova and OCM are
optional external lab tools; importing their existing evidence needs neither
binary. For stateful upgrades or Kova integration, read
[references/kova-upgrade-rehearsal.md](references/kova-upgrade-rehearsal.md).

## Workflow

### 1. Inventory the Installation

Create a public-safe draft without reading configuration, credentials, conversations, or service state:

```bash
python3 "{baseDir}/scripts/openclaw_safe_update.py" inventory \
  --package-root "$(npm root -g)/openclaw" \
  --output-dir .openclaw-safe-update/inventory
```

Use `coverage.draft.json` as a prompt to enumerate every capability the operator expects to survive the update. An empty draft is not readiness evidence.

### 2. Establish Exact Inputs

Record the currently deployed OpenClaw version from read-only runtime evidence. Select an exact target version, not `latest`, for the final rehearsal.

Create a package matrix. Strings inherit the global versions; objects can pin package-specific versions:

```json
[
  "openclaw",
  {"name":"example-openclaw-plugin","current":"1.2.0","target":"1.3.0"}
]
```

Include every separately distributed package that the deployment relies on. Do not claim Signal, Matrix, MCP, provider, or harness coverage when its package or customization contract is absent.

### 3. Describe Customizations and Coverage

Create `.openclaw-safe-update/customizations.json` in the target repository:

```json
{
  "schema": "openclaw.safe_update.customizations.v1",
  "checks": [
    {
      "id": "mcp-runtime-entrypoint",
      "package": "openclaw",
      "kind": "required_member",
      "member": "package/dist/mcp/openclaw-tools-serve.js"
    },
    {
      "id": "mcporter-skill-contract",
      "package": "openclaw",
      "kind": "member_contains",
      "member": "package/skills/mcporter/SKILL.md",
      "needle": "mcporter"
    }
  ]
}
```

Use `required_member` for overlay targets, entrypoints, and integration files. Use `member_contains` only for small textual contract anchors. Prefer several narrow checks over a broad archive dump.

Create `.openclaw-safe-update/coverage.json` using `openclaw.safe_update.coverage.v1`. Declare the exact runtime Node version and every required surface. Each required surface needs at least one concrete post-update check; use `customization_checks` to bind a surface to relevant check IDs from the customization manifest.

```json
{
  "schema": "openclaw.safe_update.coverage.v1",
  "install_shape": "npm_global_linux",
  "runtime": {
    "node_version": "22.14.0",
    "os": "linux",
    "arch": "x64",
    "libc": "glibc"
  },
  "surfaces": [
    {
      "id": "signal",
      "category": "channel",
      "required": true,
      "customization_checks": ["signal-entrypoint"],
      "post_update_checks": [
        "inbound text reaches the agent",
        "outbound reply reaches Signal",
        "voice note is transcribed"
      ]
    }
  ]
}
```

Valid categories are `channel`, `plugin`, `mcp`, `memory`, `persona`, `provider`, `service`, `attachment`, `voice`, and `other`.

### 4. Fetch Immutable Package Evidence

```bash
python3 "{baseDir}/scripts/openclaw_safe_update.py" fetch \
  --current-version 2026.6.11 \
  --target-version 2026.7.1 \
  --packages-json '["openclaw"]' \
  --output-dir artifacts/input
```

`fetch` uses `npm view`, `npm pack`, and an isolated `npm install --package-lock-only --ignore-scripts` resolver. It records registry integrity metadata, downloads archives without installing them, and binds the exact OpenClaw transitive, peer, optional, platform, Node, and npm closure into a candidate root.

Before simulation, translate the v1.1 manifests into the capability/component
graph:

```bash
python3 "{baseDir}/scripts/openclaw_safe_update.py" contract \
  --customizations .openclaw-safe-update/customizations.json \
  --coverage .openclaw-safe-update/coverage.json \
  --output artifacts/installation-contract.json
```

The contract preserves all declared checks. Components may have several roles;
application phases are descriptive and never prove isolation.

### 5. Compose, Attest, and Rerun

```bash
python3 "{baseDir}/scripts/openclaw_safe_update.py" simulate \
  --input-dir artifacts/input \
  --customizations .openclaw-safe-update/customizations.json \
  --coverage .openclaw-safe-update/coverage.json \
  --installation-contract artifacts/installation-contract.json \
  --output-dir artifacts/safe-update

python3 "{baseDir}/scripts/openclaw_safe_update.py" attest \
  --candidate-lock artifacts/safe-update/installation-candidate-lock.json \
  --observation .openclaw-safe-update/installation-observation.json \
  --output artifacts/installation-attestation.json

python3 "{baseDir}/scripts/openclaw_safe_update.py" simulate \
  --input-dir artifacts/input \
  --customizations .openclaw-safe-update/customizations.json \
  --coverage .openclaw-safe-update/coverage.json \
  --installation-contract artifacts/installation-contract.json \
  --installation-attestation artifacts/installation-attestation.json \
  --conservative-inputs .openclaw-safe-update/conservative-inputs.json \
  --cache-dir .openclaw-safe-update/cache \
  --archive-workers 4 \
  --output-dir artifacts/safe-update
```

The first simulation deliberately blocks while still writing the candidate lock. The local attestation step emits only sanitized names, types, and digests; it never emits local paths or opens configuration/personalization contents. The second rehearsal can become ready only with a fresh, complete attestation bound to the current composed root and hash-bound rollback evidence in the conservative inputs. Missing or non-reproducible closure data, floating external artifacts, unexplained local residue, undeclared service config pointers, stale attestation, lossy authority input, environment drift, incompatible or unproven Node requirements, and changed package lifecycle scripts block the rehearsal.

For a genuinely vanilla deployment, `--allow-no-customizations --allow-no-coverage --runtime-node-version <exact-version> --runtime-os <os> --runtime-arch <arch> --runtime-libc <libc>` may be used only after explicitly confirming that there are no local overlays, patches, wrappers, plugin contracts, or runtime-specific integrations. Do not silently add either flag to automation.

### Import Existing Kova Evidence

Use the importer only to validate existing Kova artifacts against an explicit
policy. It never runs or installs Kova:

```bash
python3 "{baseDir}/scripts/openclaw_safe_update.py" kova-evidence \
  --receipt <kova-receipt.json> \
  --candidate-lock <installation-candidate-lock.json> \
  --policy <kova-evidence-policy.json> \
  --output <kova-evidence.json>
```

Start from `{baseDir}/examples/kova-evidence-policy.example.json`. A `PASS` adds evidence
only to the policy's named gates; it cannot mutate a rehearsal status or
verdict. A current Kova result without an exact candidate identity is
`incomplete` and exits `2`. The imported output contains only identifiers,
statuses, and hashes, never logs, paths, configuration, messages, or secrets.
The binding covers the core npm artifact only. Kova's `platform` describes the
lab process, not the target runtime toolchain. An explicit
`environment-matched-rehearsal` request remains `incomplete`; the bundled
policy makes only scenario-specific lab claims. Installation parity, full
state restoration, and live admission require separate evidence.

### 6. Review and Stop

Inspect these artifacts:

- `runtime-truth.json`
- `core-candidate-lock.json`
- `installation-candidate-lock.json`
- `installation-attestation.json`
- `conservative-gates.json`
- `impact-shadow.json` (non-authoritative and removable)
- `analysis-cache.json` (non-authoritative input digest and cache provenance)
- `archive-execution.json` (non-authoritative concurrency and timing telemetry)
- `synthetic-update.json`
- `customization-compatibility.json`
- `coverage-report.json`
- `post-upgrade-e2e.json`
- `evidence-bundle.json`
- `verdict.json`
- `summary.md`
- `operator-plan.md`
- `operator-view.md` (non-authoritative workflow summary)

If the verdict is `blocked`, report the failed evidence, affected surface, and what must be proven; do not invent a repair. If it is `ready_for_operator_plan`, review the generated plan, add the verified backup, exact rollback, maintenance window, and scoped mutation command. `post-upgrade-e2e.json` remains `not_run` until a separately approved update has happened. Stop before apply.

The reusable GitHub workflow renders one `operator-view.md` from the strict
`verdict.json`. It shows the preflight phase, candidate root, baseline
evidence, deterministic gate IDs, non-authoritative shadow observations, and
evidence/progress links. It cannot override the verdict and does not claim
live channel, MCP, memory, migration, rollback, or post-activation proof.
The bundled `references/shadow-runs-index.json` also exposes the bounded v1.3
completion percentages and conservative exit decision. It is evaluation-only
and cannot enable selective omission.

`impact-shadow.json` can only describe hypothetical additional checks and
risks. It must never remove a baseline check, enter the evidence bundle, or
change `decision_content`, `decision_digest`, required evidence, or verdict.
Use `--disable-impact-shadow` to verify that parity.

`--cache-dir` stores only pure archive, contract, deterministic policy, and
shadow analyses. Cache entries bind exact inputs plus analyzer and policy
versions. Cache entries are private to the current user and authenticated with
a cache-local integrity key; unsafe permissions or symlinks disable reuse.
Ignore and recompute corrupt, tampered, or partial entries. Never treat cache
provenance, timing, hit rate, or advisory model output as evidence.

Use `--archive-workers 1..8` only to parallelize independent deterministic
archive inspection. Results and errors are reassembled in input order, and
`--archive-timeout-seconds` kills a slow inspection subprocess and makes the
unit an explicit failure. Concurrency
and timing never enter canonical evidence or verdicts; `1` preserves the full
sequential path.

For an independent model review, prepare a digest-bound public-safe input:

```bash
python3 "{baseDir}/scripts/openclaw_advisory.py" prepare \
  --status artifacts/safe-update/verdict.json \
  --evidence-bundle artifacts/safe-update/evidence-bundle.json \
  --installation-candidate-lock artifacts/safe-update/installation-candidate-lock.json \
  --synthetic-update artifacts/safe-update/synthetic-update.json \
  --customization-compatibility artifacts/safe-update/customization-compatibility.json \
  --impact-shadow artifacts/safe-update/impact-shadow.json \
  --output artifacts/advisory-input.json

python3 "{baseDir}/scripts/openclaw_advisory.py" render-prompt \
  --input artifacts/advisory-input.json \
  --output artifacts/advisory-prompt.md
```

After a reviewer returns one JSON object, validate it with
`openclaw_advisory.py validate`. The result is an optional attachment only.
Workers may add namespaced hypotheses, checks, risks, and review requests.
They may not establish an unaffected surface, waive evidence, emit a verdict,
mutate canonical status, or enter the analysis cache. Missing, malformed,
timed-out, conflicting, or digest-mismatched output has no status effect.
Agreement between workers is not confidence. Do not send raw package prose,
private configuration, conversations, secrets, or production logs.

## GitHub Workflow

Copy [assets/github-workflows/openclaw-safe-update.yml](assets/github-workflows/openclaw-safe-update.yml) into the target repository's `.github/workflows/` directory. Configure the package matrix and customization file in that repository, then invoke the workflow with exact current and target versions.

The workflow uploads evidence even when the rehearsal blocks, performs no deploy or notification, and fails the job unless the result is `ready_for_operator_plan`.
