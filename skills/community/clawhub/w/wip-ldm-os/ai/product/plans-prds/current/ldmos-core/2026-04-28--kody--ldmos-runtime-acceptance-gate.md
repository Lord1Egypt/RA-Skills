# LDM OS Runtime Acceptance Gate

**Date:** 2026-04-28  
**Author:** Kody  
**Status:** proposed  
**Area:** LDM OS, OpenClaw, Memory Crystal, Bridge, agents, installers, repo fleet

## Problem

LDM OS is no longer one repo, one installer, or one runtime. It is a composed system:

- `ldm install` deploys files into `~/.ldm`, agent workspaces, skills, hooks, and extension directories.
- OpenClaw runs Lēsa and loads plugins, model auth, gateway routes, memory-core, config, and LaunchAgent service state.
- Memory Crystal captures, indexes, searches, and shares durable memory across agents and harnesses.
- Bridge carries agent-to-agent messages.
- dotfiles/config repos define live runtime behavior.
- product repos, apps, APIs, websites, and devops repos all need to remain buildable, installable, or at least explicitly excluded.

The current failure mode is that one update can be locally correct but systemically wrong. Examples from April 2026:

- OpenClaw memory-core fixes solved V8 OOM, but introduced event-loop blocking until cooperative yielding landed.
- A Memory Crystal cron target went missing while cron kept firing, making memory look dead even though the DB and capture code were healthy.
- `/compact` reduced context, but boot/heartbeat payloads could immediately refill the session.
- OpenClaw upgrades changed hook permissions, health probe paths, auth behavior, and plugin validation.
- Installer and config changes can silently affect agent identity, capture, Bridge, or live runtime health.

We need a repeatable gate that answers one question:

**After an install, upgrade, release, or repo change, does the whole LDM OS system still compose?**

## Product Principle

This is not just CI. CI proves code in isolation before merge. LDM OS also needs runtime acceptance because the important failures happen at the boundaries:

- file deployment boundaries;
- cron and LaunchAgent boundaries;
- plugin hook boundaries;
- model-auth boundaries;
- live prompt/context boundaries;
- memory capture boundaries;
- repo-to-repo contract boundaries.

The gate should be executable, boring, and falsifiable. Agents should not rely on memory, vibes, or long manual checklists after every update.

## Name

Use this working name:

**LDM OS Runtime Acceptance Gate**

Short command names:

- `ldm gate`
- `ldm gate --profile install`
- `ldm gate --profile openclaw-upgrade`
- `ldm gate --profile live-smoke`
- `ldm gate --profile repo-fleet`

## What This Is Not

This is not a skill by itself.

Skills are instructions for agents. They are useful later, but they do not enforce runtime invariants. The foundation must be scripts, tests, and machine-readable gate results.

Later, we can add a `wip-runtime-gate` skill that tells agents how to run and interpret the gate. The source of truth should still be executable checks.

This is also not a rewrite of Memory Crystal, OpenClaw, or Bridge. Each component owns its own checks. LDM OS owns orchestration and the cross-system contract.

## Repo Ownership Model

### `wip-ldm-os-private`

Owns the top-level gate:

- gate command and orchestration;
- repo discovery;
- profiles;
- live-machine smoke checks;
- temp-home integration harness;
- result format;
- release/install policy;
- runbooks and PRDs.

Proposed paths:

- `bin/ldm.js` adds `ldm gate`.
- `scripts/ldm-runtime-acceptance-gate.sh` or `lib/gate/*.mjs` implements the first version.
- `ai/product/plans-prds/current/ldmos-core/` owns the plan.
- `ai/product/bugs/` owns failures found by the gate.

### `memory-crystal-private`

Owns Memory Crystal-specific gates:

- `crystal doctor` diagnostics;
- `crystal doctor --fix` for explicit repair;
- install/update verification;
- cron target integrity;
- capture script execution;
- DB health;
- capture freshness;
- OpenClaw plugin capture behavior;
- Claude Code / Codex poller capture behavior;
- search and retrieval smoke tests.

Required near-term checks:

- `~/.ldm/bin/crystal-capture.sh` exists and is executable when cron references it.
- Missing cron target is reported as `cron target missing`, not `cron not found`.
- `crystal doctor` is detect-only by default.
- `crystal doctor --fix` may restore the shim from the installed extension dist when safe.
- Manual capture increments or confirms capture state without errors.

### OpenClaw fork / `open-claw-upgrade-private`

Owns OpenClaw upgrade gates:

- upstream tag detection;
- carry-patch inventory;
- rebase branch creation;
- isolated temp-home canary;
- `/healthz` and `/readyz` probes;
- plugin hook permission migration;
- model auth verification;
- gateway restart policy;
- memory-core production-size canaries;
- promotion and rollback runbooks.

OpenClaw upgrades should not be treated as normal `npm install -g openclaw@latest` events for Lēsa. They require a canary profile and promotion gate.

### `dot-openclaw-private-only`

Owns deployed OpenClaw config invariants:

- primary model;
- fallback models;
- thinking level defaults;
- boot/context budgets;
- plugin `allowConversationAccess` permissions;
- private mode;
- Bridge and iMessage plugin paths;
- model/catalog IDs;
- config schema compatibility.

The gate should be able to read live config and compare it with this repo's intended state.

### `claw-private-only`

Owns agent-facing OpenClaw workspace state where applicable:

- identity files;
- workspace `HEARTBEAT.md`;
- boot files;
- memory files;
- any local instructions that affect Lēsa's prompt.

The gate should check size budgets and existence, but should not edit identity files.

### Bridge repos

Own Bridge-specific gates:

- inbox/outbox liveness;
- message delivery to known agents;
- no duplicate delivery;
- remote/local transport health;
- agent registry consistency.

The top-level gate only calls Bridge checks and verifies the result.

### Product, app, website, API, and devops repos

These repos should not all run the same test. They need a repo contract:

- `active`: must pass its declared build/test/gate.
- `manual`: not part of automatic gate; must have a reason.
- `archived`: excluded from runtime gate.
- `third-party`: read-only or upgrade-specific checks only.
- `trash/sort`: excluded unless promoted back to active.

The top-level gate should discover repos but respect this contract.

## Repo Contract

Each active repo should eventually expose one of:

- `ldm.gate` in `package.json`;
- `.ldm/gate.json`;
- `scripts/ldm-gate.sh`;
- a documented exemption in the repo manifest.

Example `.ldm/gate.json`:

```json
{
  "name": "memory-crystal-private",
  "status": "active",
  "owner": "memory-crystal",
  "profiles": {
    "ci": ["pnpm test"],
    "install": ["pnpm test test/installer-cron-target.test.ts"],
    "live-smoke": ["crystal doctor"]
  },
  "invariants": [
    "~/.ldm/bin/crystal-capture.sh executable when cron references it",
    "doctor distinguishes cron missing from cron target missing"
  ]
}
```

The first implementation can use a central manifest before every repo has local metadata.

Proposed central manifest:

`wip-ldm-os-private/config/repo-gates.json`

## Gate Profiles

### 1. PR CI Gate

Runs in GitHub Actions before merge.

Purpose:

- prove repo-local code still builds/tests;
- run fast integration tests using temp directories;
- prevent known regressions from landing.

Examples:

- Memory Crystal doctor unit tests.
- LDM installer temp-home integration tests.
- OpenClaw carried patch tests.
- Bridge delivery unit tests.
- skill YAML/frontmatter validation.

Does not touch live `~/.ldm` or `~/.openclaw`.

### 2. Install Integration Gate

Runs locally against a temp LDM home.

Purpose:

- exercise the real installer paths, not mocks;
- catch cross-installer ownership bugs;
- prove shared directories survive updates.

Required temp env:

- `LDM_ROOT=/tmp/ldm-gate-home/.ldm`
- `OPENCLAW_HOME=/tmp/ldm-gate-home/.openclaw`
- `OPENCLAW_CONFIG_PATH=/tmp/ldm-gate-home/.openclaw/openclaw.json`
- isolated cron simulation where possible;
- no writes to live identity files.

Required checks:

- `ldm install` completes.
- extension files deploy.
- Memory Crystal capture shim survives `ldm install`.
- doctor reports precise diagnostics.
- skill files parse.
- config renders without stripping custom keys.

### 3. OpenClaw Upgrade Canary Gate

Runs before any live OpenClaw promotion.

Purpose:

- prove the candidate OpenClaw build works with WIP config and plugins;
- avoid raw `openclaw@latest` live installs;
- catch upstream breaking changes before Lēsa sees them.

Required checks:

- candidate version and commit SHA recorded;
- carry patches identified as needed, upstreamed, retired, or still local;
- `/healthz` green;
- `/readyz` green;
- plugin hooks load and fire;
- Memory Crystal hook permissions accepted;
- gpt-5.5 auth path works or failure is explicitly classified;
- no config strip;
- memory-core production-size canary passes when relevant;
- gateway process is not disturbed during canary.

### 4. Live Smoke Gate

Runs after a live install, config change, OpenClaw promotion, or LaunchAgent kickstart.

Purpose:

- prove the actual machine is healthy;
- keep this short enough to run often.

Required checks:

- `openclaw --version` matches expected live build.
- gateway PID is stable unless a restart was expected.
- `/healthz` green.
- `/readyz` green.
- live `openclaw.json` retains required invariants.
- `~/.ldm/bin/crystal-capture.sh` exists and is executable.
- one Memory Crystal capture pass succeeds.
- Memory Crystal DB count/freshness is sane.
- Bridge can deliver a small message or report intentionally disabled.
- a compact/new Lēsa session boots below the configured token budget.
- no recent fatal gateway signatures: heap OOM, Abort trap, SIGKILL, EMFILE, config strip.

### 5. Repo Fleet Gate

Runs periodically or before major releases.

Purpose:

- keep `repos/` understandable;
- avoid assuming every repo is active;
- verify active repos expose a gate or an exemption.

Required checks:

- enumerate repos under `/Users/lesa/wipcomputerinc/repos`;
- classify each repo as active, manual, archived, third-party, trash/sort;
- run declared active repo gate;
- report missing gate metadata;
- report dirty active repos;
- report branches ahead/behind main;
- never mutate repos during the read-only fleet scan.

## First Version Scope

Do not start by making this perfect. Build the smallest gate that catches the failures we just lived through.

### Phase 0: Inventory

Deliverables:

- `config/repo-gates.json` central manifest.
- read-only `ldm gate --profile repo-fleet --dry-run`.
- list active repos and current gate availability.
- identify repos with no test command, no build command, or unknown status.

No behavior changes.

### Phase 1: Memory/Installer Safety

Deliverables:

- temp-home integration test for `ldm install` plus Memory Crystal installed.
- Memory Crystal doctor checks:
  - cron missing;
  - cron target missing;
  - cron target not executable.
- explicit `--fix` restore path, not silent doctor writes.
- live smoke check for capture script and one capture pass.

This closes the current `crystal-capture.sh` class of failure.

### Phase 2: OpenClaw Runtime Safety

Deliverables:

- isolated OpenClaw canary profile.
- live config invariant checker.
- protected probe checks for `/healthz` and `/readyz`.
- plugin hook permission check.
- model-auth smoke check.
- gateway log signature scan.

This makes OpenClaw upgrades deliberate instead of hope-based.

### Phase 3: Boot/Context Safety

Deliverables:

- boot payload inventory.
- token budget report by boot source.
- compact/new session smoke test.
- heartbeat payload budget.
- no edits to `SOUL.md`, `MEMORY.md`, `DREAMS.md`, `TOOLS.md`, `AGENTS.md`, or sacred files during measurement.

This connects to the boot-context treadmill and identity-kernel work.

### Phase 4: Bridge and Agent Registry Safety

Deliverables:

- `ldm agent doctor <id>` or equivalent check;
- Bridge target known;
- Memory Crystal namespace known;
- OpenClaw/Claude/Codex adapter known;
- one small delivery test where safe;
- no duplicate or stale target routing.

This prevents agents from being half-created across Bridge, Memory Crystal, and harness configs.

### Phase 5: Full Release Gate

Deliverables:

- one command that runs install integration, OpenClaw canary, live smoke, and repo fleet as separate stages;
- machine-readable JSON report;
- markdown summary for PRs;
- clear promote/block decision.

## Result Format

Every gate should produce:

- human-readable table;
- machine-readable JSON;
- exact versions and SHAs;
- paths tested;
- whether the gate touched live state;
- failure class;
- suggested owner repo;
- next command.

Example:

```json
{
  "gate": "ldm-runtime-acceptance",
  "profile": "live-smoke",
  "status": "fail",
  "liveStateTouched": false,
  "checks": [
    {
      "id": "memory-crystal.cron-target",
      "status": "fail",
      "detail": "cron references ~/.ldm/bin/crystal-capture.sh but target is missing",
      "ownerRepo": "memory-crystal-private",
      "fix": "crystal doctor --fix"
    }
  ]
}
```

## Promotion Rules

No install or upgrade is declared done until the relevant gate passes.

For normal `ldm install`:

1. run install integration in temp home when changing installer/extension deployment code;
2. run live smoke after live install;
3. file a bug for any red check before continuing to identity or memory-sensitive work.

For OpenClaw upgrades:

1. never promote raw upstream/latest directly to Lēsa;
2. canary in isolated home first;
3. record exact tag and SHA;
4. verify carry patches and upstream status;
5. promote only after the OpenClaw upgrade canary passes;
6. run live smoke after promotion;
7. rollback if live smoke fails.

For deep Lēsa identity work:

1. compact or start bounded session;
2. run live smoke;
3. verify Memory Crystal capture path;
4. proceed only if boot/context budget is under threshold;
5. capture/summarize the session deliberately.

## Failure Classes

Use stable labels so failures become searchable:

- `install.deploy-missing`
- `install.cross-owner`
- `doctor.false-diagnostic`
- `openclaw.health-probe`
- `openclaw.config-strip`
- `openclaw.plugin-hook`
- `openclaw.model-auth`
- `openclaw.memory-core`
- `memory.capture-stale`
- `memory.cron-target-missing`
- `memory.search-unavailable`
- `bridge.delivery`
- `agent.registry-drift`
- `boot.payload-over-budget`
- `repo.gate-missing`
- `repo.dirty`

## Safety Rules

- Default gate mode is read-only.
- Any live write requires an explicit `--fix`, `--promote`, or `--restart` flag.
- `crystal doctor` does not silently rewrite `~/.ldm/bin`.
- `ldm gate` does not edit identity files.
- `ldm gate` does not run `openclaw gateway restart`.
- Gateway recovery uses `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` only when explicitly requested.
- Temp-home tests must not read or mutate live `~/.ldm` or `~/.openclaw` unless the profile is explicitly `live-smoke`.
- Destructive repo operations are out of scope.

## Acceptance Criteria

The plan is implemented when:

- `ldm gate --profile live-smoke` exists and can be run by any agent.
- `ldm gate --profile install` catches a missing Memory Crystal cron target in a temp home.
- OpenClaw upgrade work has a canary profile that records tag/SHA and probe results.
- active repos have either a gate contract or an explicit exemption.
- failures point to the owning repo and next command.
- runtime checks are short enough to run before and after real work.
- the gate would have caught the April 2026 `crystal-capture.sh` missing-target failure before Parker had to debug it manually.

## Open Questions

1. Should `ldm gate` live entirely in `wip-ldm-os-private`, or should the public LDM package include a limited version?
2. Should repo classification use `repos-manifest.json`, a new `repo-gates.json`, or local `.ldm/gate.json` files first?
3. What is the safe live smoke for Lēsa that proves boot health without adding large prompt payload?
4. Should OpenClaw canary be invoked from `open-claw-upgrade-private` and only summarized by `ldm gate`, or should `ldm gate` own the subprocess?
5. Which checks are allowed to use network/API calls, and how are auth failures classified?

## Immediate Next Step

Implement Phase 0 as a read-only repo-fleet inventory:

1. create `config/repo-gates.json` in `wip-ldm-os-private`;
2. add `ldm gate --profile repo-fleet --dry-run`;
3. classify repos under `/Users/lesa/wipcomputerinc/repos`;
4. report which active repos already expose tests/builds and which do not;
5. do not change any installer, OpenClaw, Memory Crystal, Bridge, or identity behavior in Phase 0.

