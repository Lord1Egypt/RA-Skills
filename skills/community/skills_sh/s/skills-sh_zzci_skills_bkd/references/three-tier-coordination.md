# BKD Three-Tier Autonomous Coordination

Cron-driven L1/L2/L3 coordination that runs entirely inside BKD. L1, L2, and L3
are all BKD processes; all coordination, state, and loops are expressed through
BKD issues, follow-ups, and cron jobs. **Never** use subagents, external team
runners, or `sleep` waits.

Use this pattern when the user wants a long-running, self-driving pipeline where
the user-facing agent (L1) only talks to the user and reports progress, while
BKD itself owns task decomposition and dispatch (L2) and execution (L3).

**Engine-agnostic by design.** L1, L2, and L3 may each run on different agent
engines (Claude Code, Codex, or anything BKD supports). Prompts in this file
deliberately avoid slash-command shorthand (`/bkd`, `/pma-cr`, etc.) because
not every engine resolves them. State requirements as capabilities; if an
engine has a matching skill, mention it as a hint, never as the only path.

**Lightweight by design.** Cron fires often (every 30 min for L2, every hour
for L1). Each wake must do **scan + decide + act**, never **re-investigate the
codebase**. The plan is decomposed once at L2's first wake and snapshotted into
the issue log; subsequent wakes read the snapshot, not the source. See
[Context Discipline](#context-discipline-lightweight-wake-ups).

**Only L1 writes to main.** L2 and L3 are fully isolated in their own worktrees
(`useWorktree: true`): L3 merges into its L2's branch `bkd/{L2_ID}`, L2 never
touches main. When an L2 campaign is ready, **L1** reviews the L2 branch,
merges `bkd/{L2_ID}` into main, and resolves any conflicts. L2/L3 must never
write to main; L1 is the single integration point.

**Human-in-the-loop is mandatory at two boundaries.** (1) Before any L2 is
created or a continuation follow-up is sent, L1 reaches explicit agreement with
the user — no auto-dispatch. (2) Before L1 merges an L2 branch into main, L1
presents the review summary and merge plan and waits for confirmation —
merging into main is hard to reverse. The user's explicit `proceed`/`ok`/`go`
is the gate at both; without it, clarify and ask again.

## Table of Contents

- [When to Use This Pattern](#when-to-use-this-pattern)
- [Tier Map](#tier-map)
- [Campaign and DAG State](#campaign-and-dag-state)
- [Pre-Flight (every session)](#pre-flight-every-session)
- [L1 - Master Coordinator](#l1---master-coordinator-current-agent-session)
- [L2 - Scheduling Issue](#l2---scheduling-issue-one-per-task-own-worktree)
- [L3 - Subtask Issues](#l3---subtask-issues-short-lifecycle)
- [State Machine](#state-machine)
- [Loop Engine](#loop-engine)
- [Context Discipline (lightweight wake-ups)](#context-discipline-lightweight-wake-ups)
- [Idle Termination Countdown](#idle-termination-countdown)
- [Exceptions and Escalation](#exceptions-and-escalation)
- [Key Constraints](#key-constraints)

## When to Use This Pattern

Choose this over the two-tier flow in `orchestration.md` when:

- The work spans multiple sessions or many hours and you want BKD to keep
  driving while the user-facing agent is idle or offline.
- The user wants a single human-facing "coordinator" session that only does
  context gathering and progress reporting, with all dispatch logic inside BKD.
- The pipeline must run across heterogeneous engines (e.g., L1 on Claude Code,
  L2 on Codex, L3 on whatever engine BKD assigns) without depending on
  engine-specific slash commands.
- Subtasks need a real dependency DAG (not all parallel, not all serial), with
  capacity-aware scheduling on every wake.
- You explicitly want `sleep`-free orchestration driven only by `issue-follow-up`
  cron callbacks.

If the work fits in one session and a simple "create coordinator -> dispatch
subtasks -> wait -> merge" suffices, use `orchestration.md` instead.

## Tier Map

```
L1 (current agent session, any engine)
  - lives on the main worktree; the ONLY tier that writes to main
  - talks to user, gathers context, defines goal + acceptance + scope
  - owns one L2 PER INDEPENDENT TASK (not "one ever")
  - on new user request: ask "continuation of which L2?" vs "new task"
  - 60min cron pings L1's own session issue to report progress
  - BEFORE dispatching to L2: present goal/acceptance/scope, WAIT for
    confirmation (proceed/ok/go). No auto-dispatch.
  - when an L2 campaign is ready: review bkd/{L2_ID}, then (after user
    confirms) merge it into main and resolve conflicts

  v   (only after user confirms) follow-up: goal + acceptance + scope
      (reference paths, not file contents)

L2 (one dispatch issue per independent task; useWorktree: true)
  - runs in its own worktree on branch bkd/{L2_ID}
  - NEVER writes code itself — every implementation unit (even 1-line)
    becomes its own L3 BKD issue; L2 only orchestrates
  - first wake: decompose goal into L3 DAG, CREATE THE L3 BKD ISSUES,
    write a plan snapshot to its own log (snapshot with 0 L3 ids = invalid)
  - subsequent wakes: read snapshot + BKD state; no source re-reads
  - 30min self cron drives the dispatch loop
  - merges L3 branches into bkd/{L2_ID} (NEVER main); only L1 writes main
  - reports rollups + escalations back to L1
  - on done: signals L1 that bkd/{L2_ID} is ready for L1 review + merge

  v   create + follow-up (self-contained spec + acceptance + report URL)

L3 (one issue per subtask; useWorktree: true; short-lived)
  - branch bkd/{L3_ID}, merge target is bkd/{L2_ID} (L2's branch)
  - implements one assigned task using ONLY the spec it was given
  - must pass the project's own checks (lint/typecheck/test/build) before reporting
  - auto-moves to review via autoMoveToReview, then follow-ups report to L2
  - never dispatches, never merges, never re-investigates the project
```

## Campaign and DAG State

BKD issue status is limited to `todo`, `working`, `review`, and `done`. The
words `planned`, `dispatched`, `green`, `merged`, and `blocked` in this file are
**L2-internal DAG states**, not BKD `statusId` values. Never PATCH an issue to
`merged` or `blocked`.

Every three-tier campaign needs a stable `campaignId`.

- Generate one at L1 bootstrap before creating L2, e.g.
  `CAMPAIGN_ID="l1-${L1_SESSION_ID}-$(date +%Y%m%d%H%M%S)"`.
- Put it in L2 and L3 titles and tags when the API supports tags.
- If a tagged create request fails because tags are unsupported, retry without
  `tags` but keep the `campaignId` in the title and all follow-up prompts.
- Include it in every L1/L2/L3 follow-up prompt.
- L1 finds owned issues by this `campaignId`, not by guessing from status or
  recent activity.

L2 owns the DAG state. At the end of every L2 turn, emit a compact state block
in the final assistant message so the next cron wake can resume without an
external store:

```text
[dag-state campaignId={campaignId}]
subtasks:
- id={issueId} title="{title}" mode=worktree|simple deps=[...] state=planned|dispatched|green|merged|blocked retries=0
pendingEscalations=[]
[/dag-state]
```

State meanings:

- `planned`: L2 has designed the subtask but has not started it.
- `dispatched`: BKD issue was moved to `working`; L2 is waiting for completion.
- `green`: coordinator quality assessment passed; merge/integration is pending.
- `merged`: work is integrated into main. In simple mode this means the subtask
  passed assessment because it already worked on main; in worktree mode this
  means the branch merged and verification passed.
- `blocked`: L2 cannot continue this subtask without L1/user input. Keep the BKD
  issue in `review` when possible; if it is still active, cancel or let it
  finish before marking the internal state blocked.

## Pre-Flight (every session)

Do this every time L1 starts, before anything else:

1. Load BKD conventions: if your engine supports the `bkd` skill, load it;
   otherwise, treat this file plus `references/rest-api.md` as the authoritative
   reference and proceed via plain HTTP.
2. Auto-detect `$BKD_URL` and `projectId`. If either cannot be confirmed, ask
   the user. **Never guess.**
3. Run health and capacity checks; record `availableSlots`.
   ```bash
   curl -s "$BKD_URL/health" | jq
   curl -s "$BKD_URL/processes/capacity" | jq
   ```
4. If the scope of work is unclear, ask the user. **Never broaden scope on
   your own.**

## L1 - Master Coordinator (current agent session)

L1 **is** the current agent session, whichever engine is running it. It is
itself a BKD process running under some `issueId` (the session issue). The
engine identity does not matter; only BKD HTTP semantics do.

### L1 Responsibilities

- **L1 owns main integration.** L1 is the only tier that writes to the main
  worktree, and it does so **only** to integrate a completed L2 branch:
  review `bkd/{L2_ID}`, merge it into main, resolve conflicts. L1 still does
  **not** author features by hand-editing files — implementation always goes
  through L2/L3. Outside the review-and-merge step, treat main as read-only
  (`git status`/`log`/`diff` to observe). See **L2 branch review and merge**
  below for the procedure.
- **Identify the session issue** at startup: confirm or obtain the `issueId`
  that backs this session, because that is the cron callback target for L1's
  own wake-ups. If it cannot be obtained, ask the user; if the user cannot
  provide one, fall back to "user manually triggers query each time" and **do
  not register the L1 cron**.
- **Gather requirements** from the user; read code and docs for context.
  Do not write code, do not split tasks. Capture findings as **file paths +
  line ranges + brief notes**, NOT pasted file contents — the L1→L2 follow-up
  stays small that way.
- **Classify the request: new task vs continuation.** Before creating any
  L2, decide (asking the user when not obvious):
  - **New independent task** -> create a **new** L2 with its own
    `campaignId` and its own worktree. One independent task = one L2.
  - **Continuation** of an in-flight L2 (same scope, additional requirement,
    scope tweak, bug found during review) -> do not create a new one. If the L2
    is mid-turn, run stop → follow-up → start (`POST /issues/{L2_ID}/cancel`,
    wait — escalate to `terminate` only if it hangs — then follow-up, then
    `PATCH {statusId:"working"}`) so L2 picks up the change on a clean turn and
    folds it into its plan snapshot and DAG (see the rule in
    [Loop Engine](#loop-engine)).
  - **Unsure** -> ask the user. Never silently fold unrelated work into an
    existing L2 (it breaks the worktree's scope and the DAG).
- **User confirmation gate (HARD RULE — no exceptions).** L1 may NOT create an
  L2 issue, send a continuation follow-up, or otherwise hand work off to L2
  until the user has explicitly confirmed the dispatch. Steps:
  1. Draft the dispatch package: classification (new vs continuation +
     target L2 id), `{ goal, acceptance criteria, impact scope (paths),
     out-of-scope }`, and any open questions surfaced during gathering.
  2. Present the draft to the user in plain text. Resolve every open
     question by asking, not by guessing.
  3. Wait for an **explicit affirmative reply** — `proceed`, `ok`, `go`,
     `confirm`, or equivalent. Silence, an acknowledgement like "thanks",
     or a partial answer is NOT confirmation.
  4. If the user pushes back, iterate (revise the draft, re-present, wait
     again). Loop until the user explicitly confirms.
  5. Only after explicit confirmation: create the L2 issue (new task) or
     send the follow-up (continuation), passing the agreed package.
  This applies to **every** dispatch: the first L2 of a campaign, every
  continuation follow-up, and every scope-change follow-up. The cron hourly
  wake-up may report progress freely, but must not itself trigger a new
  dispatch without going through this gate first.
- For each confirmed new task, package `{ goal, acceptance criteria, impact
  scope (paths) }` and create one L2 dispatch issue **with `useWorktree: true`**
  (mandatory). Deliver the package via follow-up. Include the generated
  `campaignId`.
- L1 may own **multiple L2s concurrently** when the user has multiple
  independent tasks in flight — one campaign per L2.
- **L2 branch review and merge (L1 owns this).** When an L2 follows up with
  "campaign done, branch `bkd/{L2_ID}` ready":
  1. **Review** the L2 branch against the agreed goal/acceptance: inspect the
     diff (`git diff main...bkd/{L2_ID}`), confirm scope, run the project's
     own checks against the branch. If review fails, follow-up L2 with the
     gap and let it dispatch a fix L3; do not hand-fix.
  2. **Confirm with the user** — present the review summary + merge plan and
     wait for explicit `proceed`/`ok`/`go`. Merging into main is hard to
     reverse, so this gate is mandatory (HARD RULE).
  3. **Merge** into main: `git merge --no-ff bkd/{L2_ID}` (record the pre-merge
     HEAD first for an easy `git reset` escape). Resolve any conflicts; rerun
     the project checks on the merged result.
  4. If the merge or post-merge checks cannot be salvaged, abort
     (`git merge --abort`), report to the user, and follow-up L2 for a rebase
     or fix. Never leave main in a broken or half-merged state.
  5. After a clean merge, report the outcome to the user. Issues move to
     `done` only on the user's say-so (it triggers worktree auto-cleanup).
- **Register a 60-minute cron** of action `issue-follow-up` targeting L1's own
  session issue. On each wake:
  - Query BKD for issues matching **each** owned campaignId (every L2 plus
    their subtasks) and summarize progress to the user.
  - Handle yellow / blocked decisions escalated from any L2.
  - If a campaign is ready, perform the review-and-merge flow above (it still
    needs the user's merge confirmation — the cron must not auto-merge).
  - If the user is absent, log the snapshot and wait for the next wake.
- L1 **does not** create subtasks, build the DAG, or write code by hand. Its
  only main-branch writes are the L2→main merges described above.
- **Termination conditions:** evaluated per campaign (each L2 has its own
  idle countdown).
  - User explicitly stops -> **delete the L1 cron and every owned L2 cron**
    immediately and exit (no countdown).
  - Steady-state idle for a single campaign: that L2 is in `review`, every L3
    is in `review` with L2-internal state `merged` or `blocked`, no
    `todo`/`working` left, no pending yellow/blocked escalation. L1 runs the
    review-and-merge flow for `bkd/{L2_ID}` (review → user confirm → merge into
    main → resolve conflicts), then stops tracking the campaign.
  - Steady-state idle for ALL campaigns: enter the L1 idle countdown (see
    [Idle Termination Countdown](#idle-termination-countdown)). On the 3rd
    consecutive idle wake, produce the final report to the user, delete the
    L1 cron, and exit. L2 crons should already be gone.

### Sending Prompts (Rule 10 — never inline)

The `"prompt": "..."` blocks below (L2 dispatch, L1/L2 wake crons, L3 subtask)
are shown inline **for readability only**. These prompts contain quotes, `$`,
backticks, and newlines — inlining them into `-d '{...}'` corrupts the payload.
Render each prompt to a temp file, wrap it with `jq`, and POST the file. For a
templated prompt, use a **quoted** heredoc (keeps `$`, backticks, and quotes
literal) and substitute only the real variables:

```bash
cat > /tmp/bkd-prompt.txt <<'PROMPT'
## Role
You are the L2 dispatch issue ... merge into bkd/__L2_ID__ ...
POST __BKD_URL__/projects/{projectId}/issues/__L1_ID__/follow-up ...
PROMPT
sed -i "s|__L2_ID__|$L2_ID|g; s|__BKD_URL__|$BKD_URL|g; s|__L1_ID__|$L1_SESSION_ID|g" /tmp/bkd-prompt.txt
jq -n --rawfile prompt /tmp/bkd-prompt.txt '{prompt: $prompt}' > /tmp/bkd-body.json
curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$L2_ID/follow-up" \
  -H 'Content-Type: application/json' --data-binary @/tmp/bkd-body.json | jq
```

Cron-config prompts (the wake jobs) follow the same idea — build the whole body
with `jq --rawfile prompt ... '{name:..., config:{..., prompt:$prompt}}'`. Full
pattern: `rest-api.md` → [Sending Request Bodies Safely](rest-api.md#sending-request-bodies-safely).

### Creating the L2 Dispatch Issue

```bash
L2=$(curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d '{"title":"[L2] dispatch: {short goal} [{campaignId}]","statusId":"todo","useWorktree":true,"tags":["l2","campaign:{campaignId}"]}')
L2_ID=$(echo "$L2" | jq -r '.data.id')

curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$L2_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "## Role\nYou are the L2 dispatch issue (campaignId={campaignId}) in a three-tier BKD pattern. Decompose the goal into L3 BKD issues, dispatch, monitor, evaluate, and merge their branches into bkd/'"$L2_ID"'. Stay in BKD statusId=working. A 30-min self-cron drives you; never sleep.\n\n## Hard Rules\n- **Never write source files.** Every implementation unit — even 1-line tweaks, doc-only edits, config changes — becomes an L3 BKD issue and is implemented in that L3's worktree. You only run git (merge / revert / commit / stash) and build/test commands. No $EDITOR, sed -i, cat >, echo >, tee, or any other source-editing tool. No size exception.\n- **Never touch main.** Your worktree is bkd/'"$L2_ID"'; L3 branches merge here, not into main. After you terminate, L1 reviews bkd/'"$L2_ID"' and merges it into main — that is L1's job, never yours.\n\n## Goal\n{full goal description}\n\n## Acceptance Criteria\n- {criterion 1}\n- {criterion 2}\n\n## Scope\n- In: {paths/modules}\n- Out: {paths/modules}\n\n## End-of-Turn Markers (emit BOTH every turn)\n- `[L2-plan-snapshot vN campaignId={campaignId}]` — DAG + per-L3 self-contained spec (file paths only, no inline content; include the project's own check command each L3 must pass — lint/typecheck/test/build or the repo equivalent). Bump N only on real scope changes.\n- `[dag-state campaignId={campaignId}]` — per subtask: id / title / deps / state ∈ {planned, dispatched, green, merged, blocked} / retries. These DAG states are L2-internal; BKD statusId stays in {todo|working|review|done} — never PATCH to merged or blocked.\n\n## Bootstrap (THIS turn)\n1. Register the 30-min cron: name `l2-dispatch-'"$L2_ID"'`, action `issue-follow-up`, target self.\n2. Decompose AND CREATE each L3 as a BKD issue: `POST /projects/{projectId}/issues` with `useWorktree:true`, tags `[\"l3\",\"campaign:{campaignId}\"]`. Mental decomposition is invalid — the snapshot must reference real issue ids. No minimum task size: 1-line work still gets its own L3.\n3. Emit `[L2-plan-snapshot v1 ...]` (with the issue ids just created) + `[dag-state ...]`. End turn.\n\n## Steady-State Wakes (driven by cron)\nPull latest snapshot via `logs/filter/types/assistant-message/turn/last5` (DO NOT re-read source). Pull BKD issue states. ONE decision round per wake: capacity check → dispatch eligible L3s (upstream deps merged) → evaluate completions via logs/filter (green/yellow/red — use quality-review.md's logs-filter assessment only, skip its pma-cr section; L3s self-verify via project checks) → merge greens in dep order (`git merge bkd/{L3_ID} --no-ff`; on build/test failure `git revert -m 1 HEAD --no-edit` + return L3 to working) → escalate yellows/blocks to L1. Emit fresh `[dag-state]`. End turn.\n\n## Reports & Escalations (to L1)\nPOST '"$BKD_URL"'/projects/{projectId}/issues/'"$L1_SESSION_ID"'/follow-up — progress rollups after each batch; yellow = needs user decision; blocked = retries exceeded; final \"branch bkd/'"$L2_ID"' ready\" on termination.\n\n## References (engine permitting, load on demand)\nKeep loaded: references/three-tier-coordination.md (this pattern). Load only when the current round needs it: rest-api.md (unfamiliar endpoint), quality-review.md (only its logs-filter assessment, when triaging a completion), merge-strategy.md (when merging an L3 branch). Do NOT preload all of them every wake — it wastes context."
  }' | jq

curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$L2_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

### Registering L1's 60-minute Cron

```bash
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "l1-progress-'"$L1_SESSION_ID"'",
    "cron": "0 * * * *",
    "action": "issue-follow-up",
    "config": {
      "projectId": "{projectId}",
      "issueId": "'"$L1_SESSION_ID"'",
      "prompt": "Hourly L1 wake. Report campaign progress per your L1 instructions, then end turn. Never auto-dispatch."
    }
  }' | jq
```

## L2 - Scheduling Issue (one per task, own worktree)

The L2 issue is the dispatcher for one independent task. It runs in its own
worktree on branch `bkd/{L2_ID}` (BKD-created from `useWorktree: true`). Every
wake of L2 is driven by its 30-minute self cron. Each wake performs **one
decision round**, then ends the turn. **No `sleep`, ever. Never touch main.**

### L2 Responsibilities

**Hard rules (no exceptions):**

- **No source edits.** Every implementation unit (even 1-line) becomes an L3 BKD issue. L2's only file writes are git operations on L3 branches (`merge`/`revert`/`commit -m`/`stash`) plus build/test commands. No `$EDITOR`, `sed -i`, `cat > file`, `echo >`, `tee`, or any source-editing tool.
- **Never touch main.** All work happens in worktree `<WORKTREE_BASE>/{projectId}/{L2_ID}/` on branch `bkd/{L2_ID}`. Never `cd` to main, `git checkout main`, or `git merge` into main. After L2 terminates, **L1** reviews and merges `bkd/{L2_ID}` → main; that integration is never L2's job.
- **L3 mode is always `useWorktree: true`** (any `useWorktree: false` would write to main and break the rule above). The simple/worktree mode-selection table from `orchestration.md` does NOT apply here.

**Bootstrap (first wake, single turn):**

1. Register the 30-min self cron (`issue-follow-up` targeting self).
2. Read whatever source is needed for decomposition, then **create** each L3 as a real BKD issue (`POST /issues` with `useWorktree:true` + campaign tag) — mental decomposition is invalid; a snapshot with zero L3 ids fails validation.
3. Emit `[L2-plan-snapshot v1 campaignId={campaignId}]` (DAG + per-L3 self-contained spec referencing file paths only) and `[dag-state ...]`. End turn.

**Steady-state wake (one decision round per cron fire):**

1. Pull latest snapshot via `logs/filter/types/assistant-message/turn/last5` and BKD issue states. DO NOT re-read source.
2. Check `/processes/capacity`; `availableSlots == 0` → skip this round.
3. Dispatch eligible L3s (upstream deps in DAG state `merged`); same-stage L3s parallel subject to capacity + file-overlap.
4. Evaluate completions immediately (do not batch) via `logs/filter` — classify green/yellow/red using the logs-filter assessment in `quality-review.md` (ignore that file's pma-cr self-review section; this pattern relies on the L3's project checks instead):
   - **green** → merge phase.
   - **red** → if the L3 is still running, `POST /issues/{L3_ID}/cancel` first and wait for it to stop (escalate to `terminate` only if it hangs); then follow-up the L3 with the issue and `PATCH {statusId:"working"}` to start a fresh turn (stop → follow-up → start). Retry ≤ `N=2`; on exceed, set L2-internal DAG state `blocked` + follow-up L1.
   - **yellow** → follow-up L1 for a human decision; do not guess.
5. Emit fresh `[dag-state ...]`. End turn.

**Merge phase (into `bkd/{L2_ID}`, never main):**

1. Confirm `git branch --show-current` == `bkd/{L2_ID}`; if not, abort and escalate to L1.
2. Ensure clean tree (commit or stash any L2-side state), record `MERGE_BASE=$(git rev-parse HEAD)`.
3. `git merge bkd/{L3_ID} --no-ff -m "L2 merge: {L3 title} (bkd/{L3_ID}) [{campaignId}]"`. On conflict → `git merge --abort` + escalate to L1.
4. Build/test after each merge. On failure → `git revert -m 1 HEAD --no-edit`, follow-up the L3 with the error, return BKD status to `working`.
5. On success, set the L3's L2-internal DAG state to `merged`. Leave its BKD status in `review` — `done` is human-only and triggers worktree auto-cleanup.
6. After each batch, follow-up L1 with a progress rollup referencing branch `bkd/{L2_ID}`.

**Termination** — when every L3 has DAG state `merged` or `blocked`, no `todo`/`working` remains, and no evaluation/merge is pending, enter the idle countdown (see [Idle Termination Countdown](#idle-termination-countdown)). On the 3rd consecutive idle wake:

1. Follow-up L1 with "campaign {campaignId} complete; branch `bkd/{L2_ID}`
     ready for L1 review and merge into main".
  2. Delete the L2 self-cron (`l2-dispatch-{L2_ID}`).
  3. Move L2 itself to `review`.
  4. End turn. L2 will not wake again.

### L2 30-minute Self Cron (bootstrap)

```bash
curl -s -X POST "$BKD_URL/cron" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "l2-dispatch-'"$L2_ID"'",
    "cron": "*/30 * * * *",
    "action": "issue-follow-up",
    "config": {
      "projectId": "{projectId}",
      "issueId": "'"$L2_ID"'",
      "prompt": "L2 wake (campaignId={campaignId}). Run one Steady-State round per your dispatch prompt, then end turn."
    }
  }' | jq
```

## L3 - Subtask Issues (short lifecycle)

Each L3 issue is one short-lived process. It does exactly one assigned task and
exits.

### L3 Responsibilities

- **Work only inside the L3 worktree** on branch `bkd/{L3_ID}`. Do not touch
  main. Do not switch branches. L2 merges your branch into `bkd/{L2_ID}` (NOT
  main) after you report.
- **Spec-bounded execution.** The dispatch follow-up is **self-contained** —
  do NOT search the codebase to figure out what to do, do NOT read files
  outside the "Files In Scope" / "Files To Read For Context" lists, do NOT
  re-derive the goal. If something is missing, report back with
  `status=blocked` + reason `spec incomplete`; do not improvise.
- Implement only the assigned task; respect the acceptance criteria.
- **Mandatory project checks before reporting.** Run the project's own quality
  gate on your changes and make it pass — lint, typecheck, tests, and build, or
  whatever subset the repo defines (the dispatch payload names the exact
  command). No external code-review skill is required; passing the project's
  own checks is the bar. If a check fails, fix it and re-run until green; if it
  cannot pass for a reason outside your spec, report `status=blocked` with the
  failing command and output.
- On completion, BKD `autoMoveToReview` moves the issue `working` -> `review`
  automatically. **Do not manually change status.**
- Send a completion follow-up to L2 using the **full HTTP endpoint provided in
  the dispatch follow-up** (do not invent endpoints, do not rely on
  engine-local shorthands). Include:
  `status / changed files / key decisions / checks run + result / remaining
  issues`.
- L3 **must not** merge, create other issues, dispatch further work, or write
  to main. After reporting, exit.

### L3 Dispatch Payload (sent by L2)

```bash
SUB_TITLE="[L3] {subtask title} [{campaignId}]"

SUB=$(jq -n \
  --arg title "$SUB_TITLE" \
  --arg campaign "campaign:{campaignId}" \
  '{title:$title,statusId:"todo",useWorktree:true,tags:["l3",$campaign]}' \
  | curl -s -X POST "$BKD_URL/projects/{projectId}/issues" \
  -H 'Content-Type: application/json' \
  -d @-)
SUB_ID=$(echo "$SUB" | jq -r '.data.id')

curl -s -X POST "$BKD_URL/projects/{projectId}/issues/$SUB_ID/follow-up" \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "## Campaign\ncampaignId: {campaignId}\n\n## Worktree\nYou run in your own worktree on branch bkd/'"$SUB_ID"' (BKD-created). All work happens here. Do NOT touch main. Do NOT cd elsewhere. L2 will merge bkd/'"$SUB_ID"' into bkd/'"$L2_ID"' (NOT main) after you report.\n\n## Self-Contained Spec — do NOT re-investigate the project\nEverything you need to implement this task is in this prompt. Do NOT search the codebase to figure out what to do, do NOT read files outside the paths listed below, do NOT re-derive the goal — L2 has already done that. If a path or constraint is missing, REPORT BACK to L2 with status=blocked and reason='spec incomplete'; do not improvise.\n\n## Files In Scope (only these may be edited)\n- {path/to/file/1} {line-range if narrow}\n- {path/to/file/2}\n\n## Files To Read For Context (read-only)\n- {path/to/file/3}\n\n## Requirements\n{detailed implementation spec}\n\n## Acceptance Criteria\n- {criterion 1}\n- {criterion 2}\n\n## Design Constraints (inherited from L2 plan)\n- {constraint 1}\n- {constraint 2}\n\n## Mandatory Project Checks (before reporting)\nRun the project's own quality gate and make it pass. No external code-review skill is required.\nCheck command: {e.g. `npm run lint && npm run typecheck && npm test && npm run build`, or the repo-defined equivalent}\n1. Implement against the acceptance criteria.\n2. Run the check command above. If it fails, fix and re-run until it passes.\n3. If it cannot pass for a reason outside this spec, report status=blocked with the failing command and its output. Do not improvise beyond the files in scope.\n\n## Report Endpoint (use exactly this URL)\nPOST '"$BKD_URL"'/projects/{projectId}/issues/'"$L2_ID"'/follow-up\n\nReport JSON shape:\n{\n  \"prompt\": \"campaignId: {campaignId}\\nSubtask '"$SUB_ID"' ({title}) complete\\nStatus: success|failure|partial|blocked\\nChanged files: ...\\nKey decisions: ...\\nChecks: {command run} -> passed | {failing output}\\nRemaining issues: ...\"\n}\n\n## Strict Rules\n- Project checks MUST pass before reporting (or report blocked with the failing output).\n- Use ONLY the /follow-up HTTP endpoint above for inter-issue communication. Do not assume any engine-local slash command is available.\n- Do not merge, do not create other issues, do not dispatch.\n- Do not touch main.\n- After reporting, exit."
  }' | jq

curl -s -X PATCH "$BKD_URL/projects/{projectId}/issues/$SUB_ID" \
  -H 'Content-Type: application/json' \
  -d '{"statusId":"working"}' | jq
```

## State Machine

Aligned with BKD's built-in flow:

```
todo -> working -> (autoMoveToReview) review -> done   <- done is human-only
                                              ^
                                              |
                          L2 red evaluation pulls back:
                          review/working -> working (rework)
```

- L2 stays `working` for the whole campaign (its 30-min cron keeps waking it).
- L3 subtasks land in `review` and stay there. While they sit in `review`, L1
  reviews `bkd/{L2_ID}` and merges it into main (git-level integration, orthogonal
  to BKD status). Issues move to `done` only when the user says so — `done`
  triggers BKD worktree auto-cleanup, so it must happen after the main merge.

## Loop Engine

- **The only driver is the BKD `issue-follow-up` cron.** L1 cron: 60 min.
  L2 cron: 30 min.
- Every wake performs **one round of decisions** and then **ends the turn**.
  The next round waits for the next cron fire.
- **Never** use `sleep`. **Never** poll inside a turn.
- `follow-up` to a `working` + idle issue triggers its next turn immediately.
- If the process has exited, follow-up auto-restarts a new process.
- **Stop → follow-up → start for a changed requirement (HARD RULE).** If a
  target issue is still actively running (`working`, mid-turn) and you need to
  change what it is doing — rework, new requirement, scope change, abort the
  current direction — do NOT just follow-up (that queues behind the in-flight,
  now-discarded turn). Instead:
  1. `POST /issues/{id}/cancel` — gracefully stop the running turn; wait for it
     to stop. If it does not stop (hung / unresponsive), escalate to
     `POST /issues/{id}/terminate` to force-kill it.
  2. `POST /issues/{id}/follow-up` — send the new/changed requirement (queued
     while the issue is stopped).
  3. `PATCH /issues/{id} {statusId:"working"}` — start a fresh turn that picks
     up the queued follow-up.
  (A plain progress-neutral follow-up to an *idle* `working` issue needs none
  of this — that path triggers immediately.)

## Context Discipline (lightweight wake-ups)

Cron fires often. If each wake re-loads source files, re-reads the goal, and
re-derives the DAG, token cost grows linearly with campaign length. These
rules keep wakes O(1) in cost regardless of campaign size.

### Rules

1. **One-shot decomposition.** L2's **first** wake reads source as needed,
   builds the DAG, drafts each L3 spec, and emits a single tagged assistant
   message:
   ```
   [L2-plan-snapshot v1 campaignId={campaignId}]
   { dag: [...], modes: {...}, l3specs: [{ id, paths, acceptance, constraints }, ...] }
   [/L2-plan-snapshot]
   ```
   This block is the **only** authoritative plan. Subsequent wakes do not
   re-decompose.

2. **Snapshot retrieval.** Every L2 wake after the first opens with one
   filtered logs call to find the latest snapshot:
   ```bash
   curl -s "$BKD_URL/projects/{projectId}/issues/$L2_ID/logs/filter/types/assistant-message/turn/last5" \
     | jq '[.data[].content // "" | select(contains("[L2-plan-snapshot"))] | last'
   ```
   If the snapshot is older than `turn/last5`, widen the window once; if still
   missing, this is a bug — escalate to L1 (`yellow`).

3. **Snapshot supersedes, not appends.** A scope change arrives as a fresh
   turn (L1 stops the L2 — cancel, or terminate if hung — then follow-up +
   start, so it is never queued behind stale work). L2 re-runs the read-source
   step **once**, emits
   `[L2-plan-snapshot v2 ...]` superseding v1, and goes back to snapshot-only
   wakes. Each superseding-snapshot emission is itself a "non-idle action"
   that resets the idle counter.

4. **Reference, never inline.** All cross-tier payloads (L1→L2, L2→L3,
   L3→L2 reports) reference **file paths + line ranges**, never paste file
   contents. The receiving tier reads the file once if needed; pasted
   contents would duplicate into every wake's context.

5. **L3 spec is self-contained.** The L3 dispatch follow-up must include
   every file path L3 may touch, every constraint, the full report URL,
   and the campaignId. L3 must NOT need to re-investigate the project — if
   it does, the spec is incomplete; L3 reports `blocked: spec incomplete`
   and L2 amends the snapshot.

6. **Logs filter, never bulk logs.** Always use
   `/logs/filter/types/.../turn/...` with the narrowest slice that answers
   the question. Never fetch `/logs` without filters.

7. **No re-discovery per wake.** If a wake feels like it needs to re-read
   source, the snapshot is incomplete. Stop, amend the snapshot once
   (emit v(N+1)), then return to scan-only wakes.

### Wake Budget Heuristic

A healthy L2 wake should make on the order of:

- 1 logs/filter call (snapshot retrieval)
- 1 `GET /issues` call (campaign state)
- 1 `/processes/capacity` call
- 0–K issue mutations (PATCH / follow-up) where K = number of L3s changing
  state this round
- 0–K logs/filter calls to evaluate completed L3s (one per completion)

No source-tree reads, no `find`/`grep`, no test runs (unless verifying a merge
this round). If a wake exceeds this budget, the cause is usually a missing
snapshot field — fix the snapshot, not the wake.

## Idle Termination Countdown

L1 and L2 cron loops self-terminate after **3 consecutive idle wakes**. No external state store — the count lives in the tier's own assistant-message log.

### Idle definition

A wake is **idle** when, after the normal decision round, the tier has no actionable work left:

- **L2 idle**: no L3 in BKD `todo`/`working`; no pending evaluation, merge, or escalation; every L3 has L2-internal DAG state `merged` or `blocked`.
- **L1 idle**: every owned L2 is in `review` with all its L3s in `review` (DAG `merged`/`blocked`); no escalation queued; no user input waiting. One in-flight L2 → L1 not idle.

Any actionable step this wake (dispatch / evaluate / merge / escalate / progress report to user) resets the counter to 0 — do NOT emit `[idle-tick]`; the next idle wake starts at 1.

### Counting

End each idle wake with this marker as the FINAL assistant message (one line, on its own):

```
[idle-tick N/3]
```

Compute `N` by counting the trailing consecutive `[idle-tick` markers in the last 3 assistant turns — any non-idle turn in between breaks the streak:

```bash
PRIOR=$(curl -s "$BKD_URL/projects/{projectId}/issues/{selfIssueId}/logs/filter/types/assistant-message/turn/last3" \
  | jq '[.data[].content] | reverse | reduce .[] as $c ({n:0,stop:false}; if .stop then . elif (($c // "") | contains("[idle-tick")) then .n += 1 else .stop = true end) | .n')
N=$((PRIOR + 1))
```

### Termination action (`N == 3`)

Both tiers follow the same 4-step pattern:

1. **Final outbound message.** L2 → follow-up L1 (template below). L1 → final user report (assistant message in this turn).
2. **Delete own cron.** L2 → `DELETE /cron/l2-dispatch-$L2_ID`. L1 → `DELETE /cron/l1-progress-$L1_SESSION_ID`, plus defensively `DELETE` any owned L2 crons.
3. **L2 only**: `PATCH` self issue to `review`. (L1 leaves its session issue untouched.)
4. Emit `[idle-tick 3/3 -> {L1|L2} terminated]` and end turn.

L2's final follow-up payload:

```text
[L2 terminating campaignId=$CAMPAIGN_ID] All subtasks done; nothing to dispatch for 3 rounds.
Branch bkd/$L2_ID ready for L1 review and merge into main.
```

### Rules

- Marker MUST be the **final** assistant message of the turn — `logs/filter/turn/lastN` keys on it.
- 3 wakes ≈ 90 min for L2, 3 h for L1. To change the window, adjust the **cron interval**, not the count (kept at 3 so termination logic stays uniform).
- User explicit stop bypasses the countdown — delete crons immediately.
- Restart-safe: a new process reads the same trailing markers and continues the streak; restart alone does not reset it.

## Exceptions and Escalation

- Subtask failure / timeout / red: retry up to `N` (default 2). On exceed:
  set L2-internal DAG state `blocked` and follow-up L1.
- Changed requirement / rework / scope change for a still-running issue:
  stop → follow-up → start (`POST /issues/{id}/cancel`, wait — `terminate` only
  if it hangs — then follow-up, then `PATCH {statusId:"working"}`) — never
  follow-up a busy issue with a changed requirement (it queues behind the
  discarded turn). See [Loop Engine](#loop-engine).
- Merge conflict, ambiguous acceptance criteria, or scope changes: L2 does not
  guess. Set L2-internal DAG state `blocked` or classify the result as `yellow`
  and escalate to L1. L1 aggregates and asks the user.
- BKD unreachable / capacity exhausted long term: pause dispatch; L1 notifies
  the user.

## Key Constraints

1. **Inter-issue communication is follow-up only** -
   `POST /projects/{pid}/issues/{iid}/follow-up`.
2. **Check capacity before every dispatch** - `/processes/capacity`.
3. **`review` != `done`** - `done` is human-only and triggers worktree
   auto-cleanup.
4. **Soft delete** - project and issue deletions are soft-delete by default.
5. **No `sleep`, ever** - all waiting is expressed as cron callbacks plus
   ending the current turn.
6. **One L2 per independent task** - L1 creates a new L2 for each independent
   task and may own multiple L2s concurrently. For continuations of an
   in-flight task, follow-up the existing L2 instead of creating a new one.
   When unsure, ask the user.
7. **L2 owns the DAG** - dependencies, capacity, monitoring, evaluation, and
   L3→`bkd/{L2_ID}` merging live in L2. L1 handles user-facing progress,
   yellow/blocked decisions, and the final L2→main integration.
8. **L3 never dispatches, never merges** - one task in, one report out, exit.
9. **Idle cron self-termination** - L1 and L2 cron loops self-terminate after
   3 consecutive idle wakes; any actionable work resets the streak. See
   [Idle Termination Countdown](#idle-termination-countdown). User explicit
   stop bypasses the countdown.
10. **Only L1 writes to main** - L2 and L3 each get their own worktree
    (`useWorktree: true` mandatory); L3 merges into `bkd/{L2_ID}`, L2 never
    touches main. L1 is the single integration point: it reviews the completed
    `bkd/{L2_ID}`, merges it into main, and resolves conflicts — but only after
    the user confirms the merge (see rule 13).
11. **L3 mode is always worktree** - the simple/worktree mode-selection table
    from `orchestration.md` does not apply here, because simple mode would
    write to main and break the L2/L3 isolation in rule 10.
12. **Context discipline (lightweight wake-ups)** - L2 decomposes once and
    snapshots the plan; subsequent wakes read the snapshot, not the source.
    All cross-tier payloads reference file paths, never inline contents. See
    [Context Discipline](#context-discipline-lightweight-wake-ups).
13. **Two user-confirmation gates at L1** - both require an explicit
    `proceed`/`ok`/`go`; the hourly cron may report but never cross either gate
    on its own. (a) **Dispatch gate**: before creating any L2 or sending a
    continuation/scope-change follow-up. (b) **Merge gate**: before L1 merges a
    completed `bkd/{L2_ID}` into main (merging is hard to reverse). L1 reviews
    and merges the branch itself, but only after this confirmation.
14. **L2 never implements — all work goes through L3** - L2 only decomposes,
    dispatches, monitors, evaluates, and merges. EVERY implementation unit,
    no matter how trivial (one-line tweaks, doc-only edits, config changes),
    becomes its own L3 BKD issue with its own worktree. L2 may run `git
    merge`/`revert`/`commit`/`stash` and build/test commands, but never edits
    source files. A plan-snapshot with zero L3 issue ids is invalid. See
    L2 Responsibilities for the full rule.
15. **Stop → follow-up → start for a changed requirement** - to rework,
    redirect, or re-scope an issue that is still actively running, do all three
    in order: `POST /issues/{id}/cancel` (graceful stop, wait — escalate to
    `POST /issues/{id}/terminate` only if the turn hangs) →
    `POST /issues/{id}/follow-up` (queue the change) →
    `PATCH /issues/{id} {statusId:"working"}` (fresh turn). A bare follow-up to
    a busy issue queues behind the in-flight (now-discarded) turn instead of
    replacing it. Applies to L2→L3 rework and L1→L2 scope changes alike. See
    [Loop Engine](#loop-engine).
