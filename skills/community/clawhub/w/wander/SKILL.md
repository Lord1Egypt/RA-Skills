---
name: wander
description: "Close the loop on long-running remote work: pick the right completion signal per platform (CI, EAS, deploy, releases), run monitoring in the background, notify on finish, and never treat trigger as success. Includes GitHub Actions via the Wander scripts when applicable."
---

# Wander

Follow the requested remote job to its authoritative terminal result. A trigger,
job ID, uploaded artifact or launched watcher is not completion.

Resolve the owning platform and exact job/run ID, repository/project, branch/head
and trigger. Monitor an existing job without starting another. A recent success
at the same commit does not identify this dispatch; CI proves a downstream deploy
only when its contract actually includes that result.

Use the platform's supported status API/CLI or sufficient existing monitor. Wait
in the foreground when requested, otherwise use a background process while useful
work continues. Set a finite wait budget and keep the task open through its required
outcome. On timeout retain identity/status as incomplete or unknown, not failure.
A detached monitor may survive terminal closure, not host shutdown; promise only
notification routes actually configured. Recurring automation needs a separate
recurring request and must not replace following this finite job.

For the optional GitHub adapter, read [its guide](references/github-actions.md).
Resolve `WANDER_HOME`, `gh` and `jq`; select the unique workflow/branch/exact-head
run or inspect dispatch identity and set `WANDER_RUN_ID`. Use `WANDER_HEAD_SHA`
for an explicitly verified head different from local HEAD, and resolve anew after
a push. Registry timing hints are not identity evidence.

Foreground codes are 0 verified success, 1 non-success/error, 124 budget exhausted;
background/detached 0 means launch only. Defaults are 120 polls × 10 seconds plus
API latency; alternative `WANDER_MAX_POLLS`/`WANDER_POLL_SECONDS` must be positive.

Read terminal state and relevant artifacts. Investigate the exact failed/cancelled
job and fix within scope; on success continue the already authorized next step.
Success grants no new merge/deploy/paid-rerun/message permission. Report the job,
result, useful links, actions and remaining limits.
