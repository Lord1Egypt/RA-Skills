---
title: ~/.ldm/bin ownership manifest + install-time self-heal (design pass)
date: 2026-04-28
status: design (no code yet)
component: ldm-installer
parent-ticket: ai/product/bugs/installer/2026-04-28--cc-mini--ldm-bin-overwrite-wipes-crystal-capture.md
covers-action-items: 1, 5
preceded-by: PR #714 (regression-test seam), PR #123 (Memory Crystal invariant), PR #716 (LDM doctor diagnostic)
---

# `~/.ldm/bin` ownership manifest + install-time self-heal

## Why a design pass before code

Items 1 and 5 from the parent ticket are coupled. You cannot auto-recover what you do not own, and you cannot declare ownership in code without picking where the manifest lives. The previous three PRs deliberately stopped short of this so we have working diagnostics + a regression-test seam to build on.

The 2026-04-28 outage exposed `crystal-capture.sh`. The doctor work in PR #716 exposed `process-monitor.sh` (LDM-owned, also missing). The class is broader than Memory Crystal: any package that drops a shim into `~/.ldm/bin/` and wires it into cron creates the same sticky-reference failure mode. The manifest needs to cover both LDM-owned and extension-owned files in one model.

This doc decides the model, schema, lookup, conflict policy, migration, and test seam. It does not write code. After it lands, the next PR implements it against the existing test seam from #714 + #716.

## What "ownership" has to answer

The runtime pipeline only needs three answers per file in `~/.ldm/bin/`:

1. **Who owns this file?** Memory Crystal? LDM CLI? An unknown third party who dropped it manually?
2. **Where is the canonical source?** A path on disk that this owner guarantees to keep current.
3. **What is the expected mode?** Almost always 0755 for shell scripts, but spelling it out makes the verify step trivial.

If a file in `~/.ldm/bin/` cannot be answered against (1)+(2)+(3), it is foreign. `ldm install` and `ldm doctor` must leave it strictly alone (the regression test from PR #714 already enforces this). Foreigners are not a bug; they are a permissible state.

## Decision: decentralized declarations

Two reasonable shapes:

**A. Central registry.** A single `~/.ldm/state/bin-manifest.json` maintained by `ldm install`. Each package install/update writes to it.

**B. Decentralized declarations.** Each package declares its own bin files in its own manifest. `ldm install` and `ldm doctor` aggregate at runtime.

I recommend **B**. Reasons:

- A central registry needs all packages to know how to write to it. That is a coupling none of them want, and the ones we do not control (e.g. third-party plugins someone might write later) cannot.
- B is symmetric with how MCP servers, skills, and hooks are already discovered: walk extension dirs, read their plugin manifests, aggregate. No new state file, no new write contract.
- B fails open: a package that does not declare its bin files is just unknown-owner. The fix is "declare them," not "rebuild a registry."
- Conflict detection (see below) is free in B because aggregation is the only place ownership is materialized.

## Schema

Each declarer adds a `binFiles` array to its manifest:

```jsonc
{
  "id": "memory-crystal",            // existing
  "name": "Memory Crystal",          // existing
  "binFiles": [
    {
      "name": "crystal-capture.sh",
      "source": "dist/crystal-capture.sh",
      "executable": true,
      "purpose": "cron capture target"
    }
  ]
}
```

Field semantics:

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Basename written to `~/.ldm/bin/<name>`. Must be unique across all declarers (see conflict policy). |
| `source` | yes | Path relative to the declarer's installed root. For extensions, that root is `~/.ldm/extensions/<plugin>/`. For the LDM CLI, that root is `node_modules/@wipcomputer/wip-ldm-os/` (or whichever path npm resolved). |
| `executable` | optional, default `true` | If `true`, install/heal applies `chmod 0755` after copy. Doctor verifies the executable bit. |
| `purpose` | optional | Free-form. Goes to verbose doctor output and helps an operator decide if a missing file actually matters. |

## Where each declarer puts the array

**Extensions** declare in `openclaw.plugin.json`. That file is already read by every plugin-handling path (skill discovery, MCP registration), so adding one more field is the minimum-change move. Memory Crystal's `binFiles` would name `crystal-capture.sh` with `source: "dist/crystal-capture.sh"`.

**LDM CLI** declares in its own `package.json` under a new `wipLdmOs.binFiles` namespace (we already use `claudeCode` in package.json for hook config; same pattern). LDM CLI's bin files today: `process-monitor.sh`, `ldm-backup.sh`, `ldm-restore.sh`, `ldm-summary.sh`, `backfill-summaries.sh`. Each `source` is a path relative to the package root, e.g. `bin/process-monitor.sh` or `scripts/ldm-backup.sh`.

The `imsg` binary at `~/.ldm/bin/imsg` is deployed by an unrelated path. It can be declared once we know which package owns it. Until then it stays a known-foreigner and doctor reports "owner unknown."

## Aggregation pseudocode

At install time and doctor time, the LDM CLI builds an in-memory manifest:

```ts
type BinEntry = {
  name: string;        // crystal-capture.sh
  destPath: string;    // /Users/.../.ldm/bin/crystal-capture.sh
  sourcePath: string;  // /Users/.../.ldm/extensions/memory-crystal/dist/crystal-capture.sh
  executable: boolean;
  declarer: string;    // "memory-crystal" | "wip-ldm-os"
  purpose?: string;
};

function aggregateManifest(): BinEntry[] {
  const entries: BinEntry[] = [];

  // 1. LDM CLI's own declarations.
  const cliPkg = readPackageJson(LDM_CLI_ROOT);
  for (const decl of cliPkg.wipLdmOs?.binFiles ?? []) {
    entries.push(makeEntry(decl, LDM_CLI_ROOT, 'wip-ldm-os'));
  }

  // 2. Each registered extension's declarations.
  for (const [name, info] of Object.entries(registry.extensions)) {
    const extDir = join(LDM_EXTENSIONS, name);
    const plugin = readJSON(join(extDir, 'openclaw.plugin.json'));
    for (const decl of plugin.binFiles ?? []) {
      entries.push(makeEntry(decl, extDir, name));
    }
  }

  return entries;
}
```

## Conflict policy

If two declarers claim the same `name`, that is a real bug, not a stylistic choice. Aggregation should:

1. Detect the collision.
2. Refuse to act (no install, no heal). Doctor reports it.
3. Print both declarers and both source paths so the operator can pick.

We do *not* pick a winner. Today there is one real near-collision: both `memory-crystal-private/scripts/ldm-backup.sh` and `wip-ldm-os-private/scripts/ldm-backup.sh` exist. This work surfaces that as a conflict and forces a decision. Best guess: LDM CLI keeps it, MC stops shipping its copy. That decision belongs in the implementation PR, not here.

## Self-heal: what runs when

| Trigger | Default behavior | With `--fix` |
|---|---|---|
| `ldm install` | Aggregate manifest. After `deployScripts()`, for each entry: if `destPath` exists and matches mode, leave alone. If missing or mode mismatched, restore from `sourcePath`, log `+ Restored <name> from <source> (declarer: <declarer>)`. If `sourcePath` is also missing, log `! <name> declared by <declarer> but source <sourcePath> is absent`. | Same as default. `ldm install` should always converge. |
| `ldm doctor` | Aggregate manifest. Walk crontab as today. Cross-reference cron targets against manifest. Report ok / cron target missing / not executable / unknown owner. **Read-only.** | Restore missing or broken files from manifest. |

The default-behavior change for `ldm install` is the substantive part of item #5. Because the test seam from #714 already exercises real install in a temp HOME, we can extend it directly.

The split with `ldm doctor` matches the policy from PR #716 and PR #123: detect-and-report by default, side effects only behind `--fix`.

## Backwards compatibility / migration

- **Existing extensions** that have not added `binFiles` keep working. They contribute zero entries. `ldm doctor` reports their cron targets as "owner unknown" exactly as today. `ldm install` does not touch their files. No regression.
- **Memory Crystal** gets `binFiles` declared in `openclaw.plugin.json` in a separate small PR (memory-crystal-private). After that PR, `crystal-capture.sh` becomes manifest-driven everywhere; the hard-coded entry in `ldm.js` (PR #716, `knownSources`) is removed.
- **LDM CLI** gets its own `wipLdmOs.binFiles` block declared in this same repo's `package.json` as part of the implementation PR. Once declared, `process-monitor.sh` and friends auto-recover too.
- **Foreigners** like the test seam's sentinel shim or any operator-dropped script remain untouched. The regression test from PR #714 continues to enforce that.

The migration sequence:

1. Implementation PR on `wip-ldm-os-private`: aggregator, install-time self-heal, doctor switch from hard-coded `knownSources` to manifest. Adds `wipLdmOs.binFiles` for the CLI.
2. Follow-up PR on `memory-crystal-private`: add `binFiles` to `openclaw.plugin.json`. Drop the duplicate `ldm-backup.sh` from MC's scripts (or keep, with conflict resolution decided).
3. Optional: declare `binFiles` for any other extension that drops shims. None known today besides the two named.

## Test seam (extends what already exists)

The existing scripts in this repo are sufficient:

- `scripts/test-ldm-install-preserves-foreign-bin.mjs` (PR #714) ... still passes; foreigners stay untouched.
- `scripts/test-doctor-cron-target.mjs` (PR #716) ... still passes; doctor's per-file classification stays correct, but the "known sources" list becomes manifest-driven.

New test cases to add in the implementation PR:

- Plugin with `binFiles` declaration; install removes nothing; install-time self-heal restores a deleted shim.
- LDM CLI's own `binFiles` block; missing `process-monitor.sh` auto-restores during install.
- Conflict: two declarers claim the same `name`. Aggregator throws; install aborts; doctor reports the conflict.
- Source missing: declarer claims a file but the source is gone. Doctor reports `source absent`; install logs the loud `!` line.

## Open questions

1. **Where does LDM CLI declare?** `package.json` `wipLdmOs.binFiles` is my recommendation (mirrors `claudeCode.hook` already there). Alternative: a separate `ldm-bin-manifest.json` next to `package.json`. Slight preference for `package.json` because it is one less file and is already the contract for `bin` (npm-managed binaries).

2. **`source` resolution for the LDM CLI.** The CLI's package root is wherever npm installed it, which the running process can find via `__dirname`. Aggregation uses that as the source root for any `source` value in `wipLdmOs.binFiles`. Solid.

3. **`imsg` binary.** Currently in `~/.ldm/bin/imsg`. Owner is unclear from the install path. Decision deferred until owner is identified. Until then it stays a known foreigner.

4. **Mode beyond 0755.** Not needed today; all known shims are scripts. The schema makes `executable` boolean rather than an octal mode for that reason. If a future bin file needs other modes, the schema can grow a `mode` field. Don't pre-design.

5. **What about `~/.openclaw/bin/`?** Same problem, smaller surface. Not in scope for this PR. File a separate ticket if it bites.

6. **Doctor heal vs install heal.** Should `crystal doctor --fix` know about LDM-owned files too? Today it only restores `crystal-capture.sh`. After this design lands, `crystal doctor --fix` keeps its narrow scope (Memory Crystal-owned only) and `ldm doctor --fix` covers the full manifest. They do not need to overlap.

## Decisions locked (2026-04-28, post-review)

All six open questions resolved:

| Q | Decision | Reason |
|---|---|---|
| Q1 Where LDM CLI declares | `package.json` `wipLdmOs.binFiles` | Package-local metadata belongs with the package. No new loose manifest file. |
| Q2 Conflict policy | **Fail loudly.** No last-write-wins. | Last-write-wins is the bug class. A conflict means the system cannot safely decide who should restore. |
| Q3 `ldm-backup.sh` ownership | **LDM CLI owns it.** Memory Crystal stops shipping its copy in the follow-up PR. | Backup is core LDM infrastructure, not memory-specific. |
| Q4 `imsg` ownership | Leave foreign in this work. File a separate owner-resolution ticket. | Do not block the manifest design on unknown ownership. |
| Q5 `crystal doctor --fix` scope | Stays MC-only. `ldm doctor --fix` owns cross-system bin repair. | Scope boundaries. Crystal should not repair LDM-owned files. |
| Q6 Migration order | LDM CLI implementation first, then MC declaration cleanup. | Declarations are only useful once the aggregator/enforcer exists. |

## Release-blocker requirement (added 2026-04-28, post-review)

Conflict detection at install time is necessary but insufficient. **Duplicate ownership must fail CI before either package can publish.** Catching conflicts only on the operator's machine means at least one bad release ships before anyone notices.

Three layers of enforcement, in order of when they fire:

1. **Per-package self-validation (release time, every release).** Every package that declares `binFiles` runs a validator as part of its release pipeline. The validator:
   - Asserts each `source` path exists on disk in the published artifact (no declaring a file that the npm package does not actually contain).
   - Asserts no two entries within the same declarer share the same `name`.
   - Asserts each `name` is a basename, not a path (no `../` etc).

   For Memory Crystal, this validator hooks into `npm run prepublishOnly`. For the LDM CLI, same. A failed validator blocks `wip-release` from publishing.

2. **Cross-package conflict gate (LDM CLI CI, every release of the LDM CLI).** The `wip-ldm-os-private` CI runs a job that:
   - Reads the LDM CLI's own `wipLdmOs.binFiles`.
   - Fetches the latest published `openclaw.plugin.json` for each known extension (start with: memory-crystal; expand as more declare).
   - Aggregates the same way the runtime does.
   - Fails if any two declarers share the same `name`.

   This catches the case where MC and LDM CLI both claim `ldm-backup.sh`. If MC ships first with the new declaration, the LDM CLI's next release CI fails. If the LDM CLI ships first, MC's prepublish validator (layer 1) catches it when MC tries to redeclare.

3. **Runtime enforcement (every install).** `ldm install` aggregates as designed. On conflict it aborts with the same diagnostic. This is the safety net for any case the CI gates miss (e.g. a third-party extension nobody added to layer 2's known list).

The implementation PR adds layer 1 to `wip-ldm-os-private` (its own validator + `prepublishOnly` hook) and layer 3 (runtime). Layer 2 (cross-package CI gate) lands as a follow-up GitHub Actions workflow once a registry of known extensions exists; for now, layer 1 + layer 3 catch the realistic cases (the only known declarer besides LDM CLI is Memory Crystal, and its conflict will be visible immediately when its follow-up PR runs CI against an installed LDM CLI).

## Recommendation

Land this design doc as-is. Then implement in one PR on `wip-ldm-os-private`:

1. Aggregator helper in `lib/` that produces `BinEntry[]`.
2. `cmdInstallCatalog()` change: walk manifest after `deployScripts()`, restore missing/broken files. Abort on conflict.
3. `cmdDoctor()` change: replace hard-coded `knownSources` map (PR #716) with manifest lookup. Keep the same diagnostic classes.
4. `package.json` declaration of LDM CLI's own `binFiles`.
5. **Per-package validator** wired into `prepublishOnly` so `wip-release` cannot publish a broken declaration (source missing, internal duplicate, non-basename name).
6. Tests for the new cases (manifest-driven self-heal, conflict abort, source-missing, plus the validator's failure modes).

Then a follow-up PR on `memory-crystal-private` to add MC's `binFiles` and resolve the `ldm-backup.sh` conflict.

After both land, parent ticket items 1 and 5 close. The 2026-04-28 failure class has install-time prevention, doctor-time detection, and `--fix` recovery, with the ownership model explicit instead of implicit.
