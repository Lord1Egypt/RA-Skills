# Lovable orchestration resilience (Guppy/Selene turns)

Large Guppy/Selene turns on Lovable can fail with "An internal error occurred"
that looks like an app crash but is actually a **task-transaction rollback**:
the platform discards every file write from the failed turn while the dev
server and prior git state remain healthy. Recognize it in <30 s and shift to
a gated workflow instead of retrying the same monolithic turn.

## Symptoms

- Toast: "An internal error occurred" (often 2–4× in a row on the same request).
- Dev server (`vite`) still alive, preview still serving the previous state.
- `git status` clean at the last stable revision; no new files on disk.
- `git log --all --grep=<feature>` shows no commit for the work you thought landed.
- `git reflog` shows a churn pattern: `checkout → edit-branch → reset → "Changes"/"Work in progress"` cycles.
- No stack trace, port conflict, Vite HMR error, or dependency error in
  `/tmp/exec-logs/*.log` from the failed turn's window.

If those five checks pass, it is a rollback, not a crash. Do **not** debug the
app code — nothing about it broke.

## 30-second diagnosis checklist

```bash
ps aux | grep -E '[v]ite'                       # dev server alive?
git status                                       # working tree clean?
git log --all --oneline --grep=<feature-tag>     # did any commit land?
git reflog | head -30                            # retry/reset churn?
ls quantum/<feature>/ 2>/dev/null                # artifacts on disk?
```

All five negative → rollback confirmed.

## Root causes observed

Turn-level context pressure is the trigger. Contributors, in rough order:

1. Parsing multi-MB PDFs inline in an implementation turn (do it in a scoped
   research turn, cache extracted facts as memory, then implement).
2. Reading `src/routeTree.gen.ts` or other generated/large files.
3. Reading `_cache_*/` sweep directories with hundreds of per-row JSONs.
4. Reading multi-hundred-line research digests like `quantum/PQP_DIGEST.md`.
5. Spawning ≥3 sub-agents concurrently, or a sub-agent whose task fans out
   ("audit the whole plan", "review every route").
6. Writing many unrelated files in one turn.

## Gated authoring protocol

One **atomic gate per turn**. Each gate ends with a `git`-visible artifact
that stands on its own; verify with `code--view` before advancing. If the
platform rolls back, you lose one gate, not the whole experiment.

Template gate sequence for a new Selene experiment:

| Gate | Deliverable |
| --- | --- |
| 0 | Dependency canary — pin/bump `quantum/requirements.txt`; end turn. |
| 1 | Classical model — `quantum/<exp>/model.py`, unit-checked at import. |
| 2 | One-cell smoke kernel — `quantum/<exp>/kernel.py` + smoke driver that compiles and runs a handful of shots. |
| 3 | Resumable driver — per-row cache under `_cache_<exp>/`, `timeout 580` friendly. |
| 4 | Cached sweep + static JSON dump to `src/data/demos/<exp>.json`. |
| 5 | Route wiring — one static `src/routes/...tsx` reading the committed JSON. |
| 6 | Browser verification via Playwright screenshot. |

## Persistence canary pattern

Start every new experiment session with a trivial write (comment in
`quantum/requirements.txt`, a version note in a changelog file) and **end the
turn immediately**. If that trivial edit persists, larger gates are safe to
attempt. If the canary itself rolls back twice in a row, stop — further code
changes won't fix a platform-side failure. Tell the user to file a Lovable
Support ticket with the "internal error" screenshot and timestamp.

## Sub-agent budget

- ≤2 concurrent, read-only, narrow tasks per turn.
- Give each sub-agent a specific question, not a scope ("find the exact
  Hamiltonian constants in this section" — not "audit the QPDE plan").
- Never ask a sub-agent to read `src/routeTree.gen.ts`, `_cache_*/`, or
  uploaded PDFs > 1 MB; the fan-out returns into your context.

## What NOT to read in an active experiment turn

- `src/routeTree.gen.ts`
- `quantum/pqp_frontier/_cache_*/` (any file inside)
- `quantum/PQP_DIGEST.md`
- Any uploaded PDF > 1 MB (parse in a separate scoped turn, cache facts to
  `mem://features/...` before returning to implementation)

## Escalation

Canary rolls back twice → stop coding, ask the user to file a Lovable Support
ticket with the "internal error" screenshot + timestamp. Continuing to edit
project code cannot repair an orchestration-service failure.

## Confirmed root cause: unignored `.pydeps/` (2026-07-30)

Lovable Support confirmed the dominant trigger for the repeated rollback loop:
the vendored `.pydeps/` tree (hundreds of MB, thousands of files) was **not in
`.gitignore`**, so every turn-save tried to snapshot it and timed out. The
timeout surfaced as "An internal error occurred" with a clean tree afterwards.

Fix, in one atomic gate:

```bash
echo '.pydeps/' >> .gitignore
python -m pip install --target .pydeps --no-cache-dir -r quantum/requirements.txt
PYTHONPATH=.pydeps python -c "import guppylang, selene_sim; print('ok')"
```

After that, multi-file gates (kernel factory + sweep + validate + route) landed
without rollback. Rules going forward:

- Any generated/vendored directory an experiment writes (`.pydeps/`,
  `_cache_*/`, `/tmp` mirrors) must be gitignored **before** it is populated.
- Context pressure (§Root causes above) is still a secondary trigger; keep the
  sub-agent budget and gated protocol.
- The persistence canary remains the cheapest way to confirm the environment is
  healthy at the start of a session.

## Writing and pruning this skill

Skill files are retrieved by description match, so authoring hygiene decides whether the
content is ever loaded:

- **Trigger-led description.** The `description` says *when to load*, not what the author
  knows: name the tasks, tools and file areas that should fire it. A description that reads
  like a topic label never triggers.
- **One job per skill.** Running quantum experiments and building the site are separate
  skills. A skill that covers both matches everything and helps nothing.
- **State the boundary.** An explicit "not for …" clause is as load-bearing as the trigger;
  without it the skill is pulled into unrelated work and its rules get applied wrongly.
- **Always-on rules are not a skill.** Anything that must hold on *every* message (project
  framing, forbidden vocabulary, the evidence discipline) belongs in project/workspace
  knowledge. Skills fire on task type; rules that fire always must not depend on retrieval.
- **Concrete values over adjectives.** Real thresholds, real error strings, real commands.
  "Be careful with angles" teaches nothing; "`angle(x)` is halfturns" does.
- **Review and prune.** Each revision deletes what is superseded. A card kept "just in case"
  competes with the current one for attention and eventually contradicts it.

## Close with a checklist, not a claim

End a multi-rule build by reporting each convention as pass/fail — framing, numbers traced to
committed artefacts, mock/real toggles, receipts, no secrets in generated code, evidence
honesty (withdrawals and shot-scaling verdicts respected), contracts intact. If any line
fails, list the failures in priority order and **do not claim done**. A summary that asserts
completion while a convention is unmet is the failure mode this checklist exists to catch.

For the full Lovable build hygiene protocol — the project brain, the certified/forbidden-language
table, the 8 conventions, and the re-ingest rule — see `references/lovable-output-hygiene.md`.


## Sandbox-reset recovery

A long cloud sweep will outlive its sandbox. A reset wipes `.pydeps`, `/tmp` (logs and PID
files included), and `~/.qnx/auth/token.json` — while background worker processes may survive
and keep looping against a dead session. Treat it as expected, and recover in this order:

1. **Kill the surviving workers.** `ps -ef | grep <driver>` then `kill`. Doing this after
   re-authentication just hands them a live session to spend on.
2. **Reinstall the toolchain** into `.pydeps` (`guppylang`, `selene-sim`, `qnexus`, `pytket*`,
   numpy/scipy). `.pydeps/` must already be in `.gitignore` — see pitfall #11.
3. **Re-authenticate** with a background device-login poller; give the user the code and wait.
4. **Purge guard-failure and dry-run rows** from the per-row cache.
5. **Re-attach every billed job** (`quantum/resume.py`, or the driver's `submitted`-row path)
   and confirm the recovered count against what the Nexus console shows.
6. **Only then submit new cells.**

Never let a reset turn into a resubmission. The console is the source of truth for what has
been paid for; the local cache is a mirror that can lag it, never the other way round.
