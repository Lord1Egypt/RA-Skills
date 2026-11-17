# Guard PreToolUse dispatcher: design + assessment

Status: DESIGN / ASSESSMENT (not implemented)
Author: Claude Code (cc-mini, Opus 4.8)
Date: 2026-07-04
Part of: CC speedup master plan (`ai/product/bugs/master-plans/2026-07-04--cc-mini--cc-speedup-master-plan.md`), Task 3 (reduce per-tool-call hook fan-out).
Related: wip-branch-guard v1.9.93 "git-free Read/Glob fast path" (wip-ai-devops-toolbox-private PR #419) is the shipped part of Task 3.

## TL;DR

A single PreToolUse dispatcher process that runs the Edit/Write guards in-process (one node boot instead of several) is **NOT clean to build today** and, given how Claude Code actually executes hooks, **buys much less than the master plan assumed**. Recommendation: do NOT build the dispatcher now. Instead:

1. Ship the Read/Glob fast path (done, PR #419) ... real, measured per-Read win.
2. Fix the `wip-repo-permissions-hook` matcher misregistration (separate, low-risk, high-value; details below) ... removes a wasted process from every Edit/Write AND re-enables a currently-disabled security guard.
3. Defer the dispatcher until/unless `wip-branch-guard` is refactored to expose a pure, importable decision function (the invasive part), tracked by this ticket.

## The fan-out today (deployed 1.9.91)

Per `~/.claude/settings.json`, the PreToolUse hook entries and what each spawns:

- Edit / Write: `wip-file-guard` + `wip-repo-permissions-hook` + `wip-branch-guard` = 3 node processes
- Bash: `wip-branch-guard` + `wip-license-guard` = 2 node processes
- Read / Glob / NotebookEdit: `wip-branch-guard` = 1 node process

Subprocess call sites in each guard's source (execSync/execFileSync):

- `wip-branch-guard`: 14 (git rev-parse, remote get-url, worktree list, status, branch, rev-list, etc.)
- `wip-file-guard`: 0 (pure node: basename/regex/existsSync)
- `wip-repo-permissions-hook`: 0 (pure node; core.mjs)
- `wip-license-guard`: 0 (pure node)

### Measured per-guard wall time (deployed 1.9.91)

Synthetic PreToolUse payloads, `spawnSync('node', [guard])`, cwd = a real git repo, median of n=25 (3 warmup):

- `branch-guard` Read: 67.5 ms
- `branch-guard` Glob: 46.1 ms
- `branch-guard` Edit: 107.0 ms  (the long pole; full git detection + onboarding + pattern checks)
- `branch-guard` Bash: 77.1 ms
- `file-guard` Edit: 44.5 ms  (pure node boot)
- `repo-permissions` Edit: 42.7 ms  (pure node boot, and does NOTHING useful here ... see misregistration below)
- `license-guard` Bash: 44.4 ms  (pure node boot)

Node-boot floor on this machine is ~43-46 ms (the three pure-node guards all land there). So for a pure-node guard, essentially the entire cost IS the node boot.

## Why the dispatcher buys less than assumed: Claude Code runs hooks in PARALLEL

Confirmed against the official Claude Code hooks docs (hooks.md, hooks-guide.md):

- When multiple PreToolUse hook entries match one tool call, "all matching hooks run in parallel," each runs to completion, and identical handlers are deduplicated.
- One hook returning `deny` does NOT short-circuit sibling hooks. After all finish, Claude Code combines outputs and the most-restrictive decision wins (`deny` > `defer` > `ask` > `allow`).
- Timeouts are per-hook.

Implication for Edit/Write: the three guards already run concurrently. The wall-time of the fan-out is bounded by the SLOWEST guard (`branch-guard` Edit, ~107 ms), not the sum (~194 ms). `file-guard` (44 ms) and `repo-permissions` (43 ms) finish well inside branch-guard's window and add ~0 to wall time.

Therefore a dispatcher that folds file-guard + repo-permissions into branch-guard's process does NOT meaningfully reduce per-call wall time: branch-guard is the unavoidable long pole and stays. The dispatcher's only real gains are:

- Fewer process spawns per Edit/Write (3 -> 1): less CPU/memory/FD contention under load, which the parallel-spawn model does inflate somewhat beyond the serial medians above, but not by a full node boot.
- Slightly lower peak memory during the tool call.

These are real but modest, and they trade against a large, security-sensitive refactor (below).

## Assessment: NOT clean to build today

The master plan's "clean" bar: each guard exposes (or trivially can) an importable pure check function via the entry-point guard pattern, without changing standalone CLI behavior, and the dispatcher preserves each guard's exact deny semantics, ordering, timeout budget, and stdout contract. Against that bar:

### 1. `wip-branch-guard` (2113 lines) is the blocker

- Not import-safe. The module executes CLI subcommand handling at top level on load (`--version`, `approve`, `approvals`, `onboard`, `--check`, `doctor`; guard.mjs lines ~410-500+) and calls `main().catch(...)` unconditionally at the end (line 2159). Importing it today would consume stdin, run CLI dispatch, and exit.
- No pure decision function exists. `main()` interleaves the decision with side effects and process control across ~30 sites: it calls `deny()` (writes JSON to stdout) and `process.exit(0)` inline, interleaved with `appendAudit()`, `appendDenial()`, `writeSessionState()`, `markOnboarded()`, and stateful reads. Extracting `evaluate(input, state) -> { decision, reason, sideEffects }` is not mechanical; it is an untangling of control flow in a security-critical guard with 162 CLI-pinned tests.
- Adding the entry-point guard pattern (`if (isMain) main()`) is trivial, but by itself it does NOT yield an importable pure function ... the logic still has to be lifted out of `process.exit`/stdout/side-effect calls. That lift is the invasive part.
- Dual code path. branch-guard must ALSO run on Read|Glob|Bash|NotebookEdit as its own process (the dispatcher would only cover Edit|Write). So the same guard would be reachable two ways (in-process via dispatcher for Edit/Write, standalone for everything else), doubling the surface that must stay behavior-identical. Any drift between the two silently weakens a security guard.

### 2. `wip-repo-permissions-hook` is not actually an Edit/Write guard (misregistration)

- Its code only acts when `tool_name === 'Bash'` (it guards `gh repo edit --visibility public`). On Edit/Write it boots node and immediately exits 0. Its own README documents `PreToolUse:Bash` / `matcher: "Bash"`.
- It is nonetheless registered on `Edit|Write` because it ships NO `claudeCode.hook(s)` manifest, so the installer's detector (`wip-ldm-os-private/lib/detect.mjs`, the bare-`guard.mjs` fallback, ~lines 96-102) defaults it to `PreToolUse` / `Edit|Write`.
- Consequence: the visibility guard is effectively DISABLED (never runs on the Bash commands it targets) AND it wastes one process on every Edit/Write. This is a correctness bug independent of the dispatcher, and it means the "three Edit/Write guards" premise is really "two" (file-guard + branch-guard). Contract is unclear until this is fixed.

### 3. `wip-file-guard` is the only easy one

- Pure logic (basename/regex/existsSync), no stdin dependency beyond the parsed input object, uniform `deny()` -> stdout schema. It still runs `main().catch()` unconditionally and uses `process.exit()` throughout, so it needs the same entry-point-guard + pure-function extraction, but the untangling is small and low-risk. On its own it is not worth a dispatcher.

## The refactor each repo would need (if the dispatcher is pursued later)

`wip-file-guard` (small):
- Add entry-point guard: run `main()` only when invoked directly.
- Extract `export function evaluate(input) -> { decision: 'allow'|'deny', reason?: string }` containing the current isProtected/Write/Edit logic with no `process.exit`/stdout. `main()` becomes a thin wrapper that reads stdin, calls `evaluate`, and emits the JSON.

`wip-repo-permissions-hook` (small, but FIRST fix its matcher):
- Add `claudeCode.hook = { event: 'PreToolUse', matcher: 'Bash', timeout: 5 }` to package.json so the installer registers it on Bash (where its logic lives) and drops the Edit|Write entry. Note: the installer already re-homes owned entries in place (`deploy.mjs` finds by extension-dir tag and rewrites matcher/command/timeout), so this manifest change alone moves it cleanly on next `ldm install`.
- Then, if dispatching Bash, add entry-point guard + `export function evaluate(input)` around `parseVisibilityCommand` + `checkPrivateCounterpart` (already factored into core.mjs, so this is easy).

`wip-branch-guard` (large, the real cost):
- Add entry-point guard so import does not run CLI dispatch or `main()`.
- Lift the decision out of `main()` into `export function evaluate(input, sessionState) -> { decision, reason, audit?: [...], stateMutations?: {...} }`. Side effects (`appendAudit`, `appendDenial`, `writeSessionState`, `markOnboarded`) must be returned as data and applied by the caller, so the dispatcher can decide ordering and the standalone path stays byte-identical.
- Preserve all 162 tests green against the standalone CLI, and add tests that the in-process `evaluate` produces identical decisions and side effects for the same inputs.
- Keep the Read|Glob|Bash|NotebookEdit standalone registration; only Edit|Write would route through the dispatcher.

## Dispatcher shape (if built)

- New tiny package `wip-guard-dispatcher` (or a `dispatcher.mjs` door in the toolbox) registered as the SINGLE `Edit|Write` PreToolUse hook. It imports `file-guard`'s and `branch-guard`'s `evaluate`, runs them in a fixed order, short-circuits on the first `deny` (safe: the dispatcher is ONE hook entry emitting ONE decision; Claude Code's cross-entry most-restrictive aggregation is unaffected), applies branch-guard's returned side effects, and emits the deny JSON or exits 0.
- Installer wiring stays confined to package manifests + `lib/deploy.mjs` hook registration: register the dispatcher on `Edit|Write`, and change branch-guard's manifest so its own registration covers `Read|Glob|NotebookEdit|Bash` only (no Edit|Write, to avoid double-running branch-guard's logic). file-guard's Edit|Write registration is removed (folded into the dispatcher). Do NOT touch `src/boot/` or `bin/ldm.js` doctor sections.

## Projected saving (dispatcher)

Given parallel hook execution, the per-call WALL-TIME saving on Edit/Write is small: branch-guard's ~107 ms remains the long pole; folding in the two ~44 ms pure-node guards (which already overlap it) removes process spawns, not the critical path. Estimated wall-time win: near-zero to low tens of ms under contention, not the 0.2-0.5 s the master plan hoped for (that figure assumed serial execution). The measurable win is process count: 3 -> 1 spawn per Edit/Write, i.e. ~2 fewer node boots (~85-90 ms of aggregate CPU) freed for other work, valuable mainly under heavy parallel tool use or on constrained hardware.

Weigh that against the risk of refactoring a 2113-line security-critical guard with a dual code path. The risk/reward does not favor building it now.

## Recommendation

1. DONE: Read/Glob fast path (PR #419) ... the one clearly-worth-it per-call win in Task 3 (Read 67.5 -> 46.7 ms, -31%).
2. DO NEXT (separate small PR, not this ticket): fix `wip-repo-permissions-hook` to register on `Bash` via a `claudeCode.hook` manifest. Removes a dead process from every Edit/Write and re-enables the public-visibility guard on the Bash commands it is supposed to police. This is a correctness fix that also trims fan-out, with no guard refactor.
3. DEFER: the dispatcher, until `wip-branch-guard` exposes a pure importable `evaluate`. Track here. Only pursue if profiling on real hardware shows the parallel-spawn contention actually hurts, since the parallel model caps the wall-time upside.

## Measurements appendix (raw)

Deployed 1.9.91, median ms (n=25):
- branch-guard Read 67.5 / Glob 46.1 / Edit 107.0 / Bash 77.1
- file-guard Edit 44.5
- repo-permissions Edit 42.7
- license-guard Bash 44.4

Fast-path before/after (n=40), branch-guard on origin/main vs the v1.9.93 branch:
- Read 67.6 -> 46.7 (-31%); Glob 46.2 -> 46.8 (unchanged); Edit 107.0 -> 107.0 (unchanged).

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, GPT-5.5), Claude Code (cc-mini, Opus 4.8), Codex (GPT 5.5).
