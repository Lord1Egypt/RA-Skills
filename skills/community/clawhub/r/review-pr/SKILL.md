---
name: review-pr
description: Review a GitHub pull request from a PR number, repo-qualified reference, or URL; reconcile the current content against all earlier review comments so fixes do not regress; post one consolidated PR comment; and watch for the PR author's "addressed" responses until a clean review, at no/low token cost while nothing changes. Use when the user asks to review, babysit, re-check, or continuously monitor a PR until no blocking issues remain, with bounded convergence across follow-up cycles.
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["gh", "jq"] } } }
---

# Review PR

Review one pull request repeatedly until it has no blocking issues within the agreed
review scope. Use GitHub comments as the durable review ledger and a background watch (see
`../WAITING.md`) for the polling loop.

## Scope and autonomous actions (read before invoking)

Invoking this skill authorizes it to, without pausing for a per-step confirmation: post
one top-level GitHub PR comment per completed review cycle, and create or reactivate a
background watch that keeps running GitHub reads (and, on a qualifying author response,
another review cycle plus another comment) after this invocation ends — potentially
across sessions, depending on which host mechanism `../WAITING.md` selects for your
runtime. It never pushes code, edits or deletes comments, resolves threads, approves,
merges, labels, or closes the PR, and never modifies the PR branch. If you need to know
exactly how to list, pause, or permanently stop a watch this skill armed, see the "Arm
the Watch" section below and `../WAITING.md`'s host-mapping table before invoking it in
an environment where an unattended background job would be unexpected.

## Inputs

Require one of:

- a PR number, resolved against the current Git repository;
- `owner/repo#number`; or
- a GitHub pull-request URL.

If a number cannot be resolved unambiguously from the current repository, ask for the
repository. Do not guess.

Support two modes:

- `start` (default): perform an immediate review, post the result, and start monitoring if
  issues remain;
- `monitor`: poll for a qualifying author response and re-review only when triggered.

## Invariants

- Treat the exact remote head OID as the review unit. Never rely on a stale local checkout.
- Keep the user's worktree read-only. Prefer GitHub reads or a disposable checkout.
- Review the complete current PR, not only commits since the last pass.
- Read all prior top-level comments, submitted reviews, inline review threads, replies, resolution state, and outdated state with pagination.
- Treat earlier actionable feedback as requirements. Verify each requirement against the current head even when its thread is resolved or outdated.
- Prefer current code and tests over an author's assertion that feedback was addressed.
- Invoking this skill authorizes its one permitted top-level PR comment for each completed review cycle. Post that comment without asking for a second confirmation; the unattended loop depends on this standing authorization.
- The only permitted GitHub mutation is one new top-level PR comment per completed review cycle.
- Make retries within the owned task idempotent for the same PR head and triggering author item. Never knowingly run two workflows for the same repository, PR, and reviewer in different tasks.
- Do not push code, submit a formal review, edit or delete comments, resolve threads, approve, request changes, merge, label, close, or modify the PR branch.
- While waiting for the author, do not post polling or reminder comments on GitHub.
- Stop successfully only after a fresh review finds no blocking issues under the bounded-convergence discipline below. Treat a closed, merged, explicitly cancelled, or persistently blocked PR as a distinct non-success terminal state.

## Resolve GitHub Context

1. Resolve the repository, PR number, PR URL, PR author login, current head OID, and authenticated reviewer login.
2. Confirm GitHub authentication before relying on CLI results.
3. Prefer the signed-in `gh` CLI for all GitHub reads and writes, including `gh pr comment --body-file` for the cycle's top-level comment. Use a connected GitHub integration only where it provides data the CLI cannot, and use the signed-in browser only as the final fallback after both authenticated API paths fail.
4. Use `gh api graphql` or the bundled GitHub review-comment workflow for `reviewThreads`, `isResolved`, `isOutdated`, anchors, and replies. Flat comment reads are not a complete history.
5. Fetch every page of comments, reviews, threads, files, and commits needed for the review.
6. Compute the workflow ID and resolve the host's watch ownership before the first GitHub write. See `../WAITING.md`'s host mapping: on OpenClaw a `cron` job with a `trigger.script` gate, on Codex a heartbeat (inspect active and paused automations by the immutable marker; reuse a same-task match; treat a foreign or ambiguous match as a conflict), on Claude Code a `Monitor` task ID retained for this session. A durable GitHub marker proves review state, never that this task owns a watch.

If GitHub reads or writes fail, do not infer state and do not post a partial review. A 404 can mean missing access rather than a missing PR. Leave an existing watch armed and report the failed run unless reliable authenticated metadata proves a terminal state.

## Build the Historical Constraint Ledger

Before inspecting for new issues:

1. Find every prior actionable review comment, including top-level follow-ups and inline threads.
2. Give special weight to comments by the authenticated reviewer because these are the constraints this workflow previously requested.
3. Reduce each finding to a testable invariant with its source comment URL, original anchor, and most recent disposition.
4. Fingerprint it by normalized invariant, path or symbol, and nearby behavioral context rather than an old line number.
5. Classify every invariant at the current head as `addressed`, `partial`, `unaddressed`, `regressed`, or `superseded-with-reason`.
6. Keep resolved and outdated threads in the ledger. Thread UI state never proves that the underlying requirement still holds.
7. Detect contradictions between new changes and prior requirements before adding unrelated findings.

Do not copy old comments blindly. Re-establish each issue from current evidence.

## Bounded Convergence Discipline

Make the first review cycle the broad discovery pass. Inspect the complete PR across correctness, security, data loss, races, compatibility, tests, operability, and user-facing behavior; use independent parallel lenses when useful so material blockers are found together rather than serially. The first posted review establishes the baseline threat model, architecture, acceptance criteria, and blocking-invariant ledger.

After that baseline, keep the review scope frozen unless the user explicitly expands it or the PR materially changes its stated objective or architecture. On a follow-up cycle, post a new blocking finding only when it is one of:

1. an earlier blocking invariant that remains unaddressed, partial, or regressed;
2. a concrete regression introduced by the author's fix; or
3. a concrete high-impact correctness, security, or data-loss path that existed on the previously reviewed frozen head but was missed.

For category 3, require specific evidence and explain why the path is blocking; do not use it as a license to reopen general discovery indefinitely. Do not turn design preferences, speculative concerns, theoretical edge cases, or merely underspecified operational details into new blockers. Treat useful operational detail as non-blocking P2/follow-up work and do not keep the watch armed solely for it.

Do not require a new architecture, trust boundary, or threat model during a follow-up cycle by default. If fixing a genuine blocker requires such an expansion, stop and ask the user to choose rather than silently moving the goalposts. In each follow-up result, classify every prior blocker and identify which allowed category justifies any newly reported blocker. A cycle is clean when no blocking finding remains under this frozen scope, even if optional P2 follow-ups could improve implementation polish.

## Perform a Review Cycle

1. Capture the head OID immediately before the review.
2. Read the PR description, changed files, complete changed-file contents where needed, relevant callers and consumers, tests, configuration, migrations, workflows, and user-facing contracts.
3. Check the historical ledger first. On the initial cycle, perform the broad discovery pass; on follow-up cycles, apply the bounded-convergence categories before retaining any new finding.
4. Run safe read-only checks or tests when useful. State what was and was not verified.
5. Re-read the PR head immediately before posting. If it changed, discard the draft and review the new head.
6. Keep only evidence-backed findings that meet the cycle's blocking bar. Avoid speculative concerns, duplicates, and non-blocking implementation polish in the GitHub findings.

Use priority labels such as `[P1]` when they help the author triage. Include exact paths, lines, behavior, and the required outcome. Keep optional P2/follow-up notes out of an `issues` verdict; mention them only in the chat handoff when materially useful.

## Durable State Marker

Append one hidden marker to every comment posted by this skill. Compute `workflow_id` first. Compute `cycle_key` only from stable cycle inputs, and derive `batch_id` as the first 16 lowercase hexadecimal characters of `cycle_key`. Then render the visible body, including `codex-addressed:BATCH_ID`, and compute `body_digest` from those exact UTF-8 visible-body bytes. The body digest is validation metadata and is deliberately excluded from `cycle_key`.

```html
<!-- review-pr-state
schema=1
repo=OWNER/REPO
pr=NUMBER
workflow_id=SHA256(OWNER/REPO#NUMBER|REVIEWER)
cycle_key=SHA256(WORKFLOW_ID|REVIEWED_HEAD|TRIGGER_KIND|TRIGGER_NODE_ID)
batch_id=FIRST_16_HEX(CYCLE_KEY)
cycle=N
reviewed_head=FULL_OID
trigger_kind=initial|manual|issue_comment|review|review_reply
trigger_node_id=INITIAL_OR_GLOBAL_GRAPHQL_NODE_ID
verdict=issues|clean
reviewer=LOGIN
body_digest=SHA256(EXACT_VISIBLE_BODY_UTF8)
-->
```

Accept a marker only when its containing top-level comment was authored by the authenticated reviewer and its schema, repository, PR, reviewer, workflow hash, cycle hash, batch ID, and visible-body hash all recompute correctly. Ignore malformed or forged markers.

Before posting, find the latest valid marker for the same repository, PR, and reviewer. Search for the exact `cycle_key`; if it already exists, do not post again, even if a retry produced different wording. This makes API retries idempotent inside the serialized task and handles a comment call that succeeded even when its response was lost. GitHub comment creation has no transactional idempotency key, so refuse a start when another owned task is already monitoring this workflow; do not claim protection against two brand-new concurrent starts that race before either is discoverable.

Increment `cycle` only when posting a new review result. Use `trigger_kind=initial` and `trigger_node_id=INITIAL` only when no valid marker exists. On a later manual invocation, first reconcile the latest marker and watch. If the current head is unchanged and there is no new qualifying author response, do not post again. If the head changed, use `trigger_kind=manual` and the latest valid state-comment's global node ID as `trigger_node_id`.

## Post the Review Result

If blocking issues exist:

1. Post one top-level comment containing the reviewed head, status of prior findings, and the consolidated current findings.
2. Give the batch a short acknowledgement token such as `codex-addressed:BATCH_ID` and ask the PR author to include it when the complete batch is addressed. Also accept an unambiguous natural-language acknowledgement under the rules below.
3. Append the durable state marker with `verdict=issues`.
4. Arm the watch described below.

If no blocking issues exist under the bounded-convergence discipline:

1. Post a top-level comment whose visible text starts exactly with `No issues to fix.` and may include the reviewed head after that sentence.
2. Append the durable state marker with `verdict=clean`.
3. Immediately re-read the PR head. If it changed, the clean comment remains scoped to the old OID; do not stop and instead review the new head.
4. If the head is unchanged, stop the matching watch and report that watching stopped.

If the initial review is clean, arm no watch.

## Arm the Watch

After an `issues` verdict, tell the user you are watching the PR for the author's response.

Wait the way `../WAITING.md` prescribes for your host — a background watch that costs
nothing/near-nothing while the PR is quiet, rather than a scheduler that re-runs this
whole skill on a timer to learn nothing. That file carries the reference loop, the host
mapping (OpenClaw `cron` + `trigger.script`, Claude Code `Monitor`, Codex heartbeat), the
emit-on-terminal-state rule, the filter-on-content rule, and the filter-verification step;
do not restate them here.

**One watch per PR.** Keep whatever identifies it (task id, automation ID, or cron job
id) — it's what stopping needs, and it's how you know a watch for this PR is already armed
rather than arming a second on top of it.

**The predicate is a CANDIDATE filter, not the trigger rule.** The marker regex must cover
every response shape **Monitor Mode** below promises to accept — the token *or* an
unambiguous natural-language acknowledgement:

```
MARKER='codex-addressed|addressed|fixed|handled'
EXCLUDE='<!-- review-pr-state'
```

`EXCLUDE` drops your own batches, which otherwise wake you on your own writing — the
reviewer and the author can post under the same GitHub login, so content is the only thing
that separates them. It must be the HTML comment, never the bare string — a bare
`review-pr-state` is just a word that shows up in any reply discussing the watch,
including yours.

This filter is deliberately looser than the trigger rule, and it wakes on `not addressed`
too. That is the design and not a defect: the predicate cannot judge negation, quoting or
scope, **Monitor Mode step 5 can and must**, and a wasted wake costs one model run while a
missed one costs the whole review loop. Confirm every candidate against Monitor Mode
before acting.

**Keep it armed while the latest durable marker has `verdict=issues`; stop it when the
marker goes `clean`, when the PR leaves `OPEN`, or when the user says to stop.** Every stop
goes through your host's own mechanism (see `../WAITING.md`'s table), whatever the reason
for stopping — a watch that outlives its purpose on a durable host (Codex heartbeat,
OpenClaw cron job) bills every tick until someone notices; on Claude Code the `Monitor`
dies with the session anyway, so say plainly that it stops when the session does and
re-arm on the next invocation.

The GitHub marker remains the durable source of truth — it is what makes re-arming safe
and idempotent — and the watch is only an optimisation over the user telling you a reply
landed.

Reconcile on every manual start:

- On a durable host (Codex, OpenClaw), run the ownership lookup first. If an `issues`
  marker exists, keep an active owned watch, reactivate a paused one, or create exactly
  one only when no match exists. Never infer absence from this session's local state.
- If the watch could not be armed after the issues comment posted, report that watching is
  blocked; the marker makes a later retry safe.
- If the latest valid marker is `clean`, arm nothing and delete only the matching owned
  watch. Never search for an older `issues` marker or review stale acknowledgements.

## Monitor Mode

On each wake (a watch event, or a manual invocation):

1. Read the newest valid state marker of either verdict. If it is `clean`, stop the watch (this host's mechanism) and perform no review. If no valid marker exists, report a blocked state rather than guessing.
2. For an `issues` marker, fetch PR comments, reviews, and review replies whose `createdAt` is later than the containing review comment. Maintain processed `kind:node_id` values separately for each stream; numeric database IDs are not globally ordered. An edit to an older item does not qualify—require a new comment or reply.
3. Exclude this workflow's own marked comments, even when the authenticated reviewer and PR author are the same GitHub login.
4. Qualify a trigger only when all are true:
   - the commenter login equals the PR author login;
   - the comment is ordered after the latest review result;
   - it includes that batch's acknowledgement token, or unambiguously claims the complete latest feedback was addressed, fixed, or handled;
   - its global GraphQL node ID has not already appeared as `trigger_node_id` in a state marker.
5. Strip quoted text and fenced or inline code before interpreting natural language. Reject negated, partial, future, or ambiguous forms such as `not addressed`, `partly addressed`, `will address`, questions, plans, reactions, commits alone, thread resolution alone, and bot comments.
6. If no qualifying response exists, make no GitHub write and leave the watch armed.
7. If more than one qualifying response exists, process the newest one and treat earlier ones as superseded.
8. Run a complete review cycle against the current head, using the qualifying item's kind and global node ID as `trigger_kind` and `trigger_node_id`. The acknowledgement is only a trigger, never proof. Apply the frozen baseline and bounded-convergence categories before retaining any new blocker.
9. Post `issues` and leave the watch armed, or post `clean`, verify the head is still unchanged, and stop the watch (this host's mechanism) as the final tool action.

If two candidates have the same `createdAt`, use the GitHub timeline order when available; otherwise do not guess and wait for an unambiguous newer response.

When woken by the watch rather than by hand, do not send ordinary progress commentary. An
unchanged poll should be a quiet no-op wherever your host allows it: do not post, report
normal progress, or create another watch. A processed response, terminal stop, or
important blocker may notify.

An author response may resolve a concern by explanation without a new commit. Re-review the evidence even when the head OID is unchanged.

## Terminal and Exceptional States

- If the PR is merged or closed before a clean verdict, stop the watch **through this host's own mechanism**, make no `No issues to fix.` claim, and report the terminal PR state to the user.
- If the user asks to stop, stop the matching watch **through this host's own mechanism** without changing GitHub. Do not claim a stop happened through a mechanism this host doesn't have.
- If GitHub is temporarily unavailable, authorization fails, or rate limits prevent a reliable snapshot, make no GitHub write. Count consecutive failures and emit once the watch has been blind for a duration appropriate to your poll interval (three ticks is a reasonable threshold at a 30-minute cadence). A silent watch must never be able to mean "I cannot see", and an access failure must never cause a replacement watch or deletion of the durable GitHub review state.
- If arming or stopping the watch itself fails, report the exact reconciliation still needed and do not claim the watch is active, stopped, or recovered.
- A later manual invocation may re-arm a blocked watch only after a successful GitHub snapshot.
- If a required author choice blocks review, ask in the chat and leave the watch armed. Do not manufacture a clean verdict.
- A later commit after a verified clean termination is outside this workflow. A new invocation is required.

## Final Handoff

After every manual or watch-woken run, report concisely:

- PR and reviewed head;
- whether a GitHub comment was posted and its URL;
- whether monitoring is active, waiting, stopped cleanly, blocked, or stopped because the PR closed or merged;
- any verification limitation or tool failure.
