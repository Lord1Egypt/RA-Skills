# Verify Conclusion · 陷阱 11–20（原文）

> 本文件由 `SKILL.md` 按需引用；条目文字与拆分前逐字节一致。

### ⑪ Output from a restricted tool treated as fact

**Pattern:** The agent verifies whether a file exists using `sudo cat /etc/sudoers.d/X` → sudo refuses because the NOPASSWD scope does not cover `cat` → the `|| echo "FILE NOT FOUND"` fallback fires → the agent asserts "the file does not exist". The file **existed all along**; `sudo` simply lacked permission to run `cat`.

**Root cause:** A false negative caused by a tool-permission limit is taken as truth. `sudo` refusing ≠ the file does not exist — it means "you have no NOPASSWD authorization for this command". Every subsequent step of the diagnosis then rests on a false fact.

**Fix:** Any file-existence check that relies on `sudo` must first be redone with a tool that needs no sudo — `ls -la` or `stat`. File existence (an inode property) and file readability (a permission property) are **two independent propositions**; conflating them produces catastrophic misjudgments.

**Real case (2026-07-27):** Agent asserted `/etc/sudoers.d/<name>` had been deleted → inferred "the Phase 4 fix never ran" → after the user challenged it, re-inspection showed `ls -la /etc/sudoers.d/` listing the file all along, and `sudo -n journalctl --flush` returning 0. The root cause was not a missing file but the permission-limited `sudo cat`.

### ⑫ Tool output treated as a logical assertion (the `|| echo` anti-pattern)

**Pattern:** The agent checks a resource state with `cmd 2>/dev/null || echo "X NOT FOUND"` → the tool itself fails for any of many reasons (permissions, timeout, env) → `|| echo` fires → the agent asserts "X does not exist / failed". In reality `cmd` can fail for infinitely many reasons — insufficient permission, timeout, command not found, missing TTY, different PATH — and those are **completely unrelated** propositions to "X does not exist".

**Root cause:** `||` compresses two independent signals — "did the tool execute successfully" and "is the resource in a given state" — into a single boolean. That is very natural under shell-writing habits, and catastrophic for scenarios that require precise diagnosis.

**Fix:** Never use the `|| echo "NOT FOUND"` / `|| echo "FAILED"` anti-pattern in any diagnostic check. A diagnostic check must distinguish explicitly:
1. Did the tool run successfully (exit code)
2. Is the resource in the claimed state (content / return value)

Print the two separately; do not merge them with `||`. Typical wrong form vs correct form:

```
❌ sudo cat /f || echo "FILE NOT FOUND"
❌ curl -s X || echo "API DOWN"
✅ ls -la /f; echo "exit=$?"          ← first confirm the tool itself ran
✅ curl -s -w '\nHTTP:%{http_code}' X ← two lines: body + exit, independent
```

**Related trap — false independence in Step 2:** when Step 2 uses the same restricted tool as Step 1 (e.g. `sudo test -f` and `sudo cat` share the same NOPASSWD whitelist limit), both "independent" derivations in fact share one hidden premise — a single cause breaks both at once. True independence requires Step 2 to use a **different access path** (e.g. `ls -la` instead of `sudo cat`).

**Same family — the silent-failure aggregator.** Any loop that sums per-object reads with errors discarded undercounts while looking complete:
```
❌ for p in /proc/[0-9]*; do s=$(awk '/^Pss:/{print $2}' $p/smaps_rollup 2>/dev/null); [ -n "$s" ] && tot=$((tot+s)); done
tot=${#ok}  →  prints a total; 74 of 84 reads failed silently → total is 44% of truth
✅ count successes and failures explicitly, print both, and refuse to present the total when failures > 0
```
Rules that follow:
1. **A permission pre-check is not a readability check.** `[ -r /proc/<pid>/smaps_rollup ]` once reported "all readable" while most reads in fact failed — on `/proc`, ownership and access(2) semantics do not settle it. Only an actual read that returns a value counts.
2. **When the probe's own number disagrees with an independent total, the probe is on trial, not the total.** Here `/proc/meminfo` `AnonPages` (2.2 GB) vs the summed PSS (1.0 GB) exposed the bug; chasing the discrepancy found it. Never reconcile a gap by explaining it away.
3. **Cross-basis summing is not reconciliation.** Two aggregates measured on different definitions (container "memory usage" that includes reclaimable file cache vs host process RSS; per-process RSS that double-counts shared pages) can land within a few percent of a system total by coincidence. Agreement across mixed bases is not evidence — convert everything to ONE basis first (e.g. anon/`AnonPages`), then add.
4. **A negative claim about a system knob needs its own measurement.** "`swapoff` would OOM because swap is 80% full" is a claim; compute the actual comparison (`MemAvailable` vs swap in use) and grep the OOM history before repeating it.
5. **Printing the caveat is not compliance.** Writing "RSS double-counts shared pages, relative ranking only" and then summing RSS + swap into a "total" one line later is the standard failure shape: the caveat was emitted, so the number feels licensed, and the reader's eye lands on the total. A caveat that forbids an operation must be followed by *not doing it* — either drop the total or convert every term to one basis first. Same for any "⚠️ not exact" annotation attached to a headline figure.

### ⑬ Declaring "root cause found" on the first bug

**Pattern:** The agent finds A is problematic → asserts "the root cause is A" → the user asks about a specific scenario → the agent discovers A is in fact not the problem → then finds B is the real root cause. Between finding A and finding B, the agent had already declared "root cause found" once.

**Root cause:** Root cause is an elimination process, not a discovery process. A single anomaly ≠ root cause. Only after three steps — falsification test, elimination of alternative explanations, causal-chain verification — may it be declared.

**Fix:** A diagnostic conclusion must be explicitly labeled "candidate root cause #N" or "not yet eliminated" until the verification workflow has run to completion. Declaring "root cause found" is forbidden before every one of the following holds:
- [ ] Alternative explanations have been isolated and eliminated
- [ ] Every link in the causal chain has physical evidence
- [ ] The repair path has been verified to be feasible

**Real case (2026-07-27):** Agent found the sudoers file "missing" (actually a permission false negative) → declared "root cause found" → the user asked who deleted it → re-inspection showed the file had been there all along → the real root cause was `Restart=always` bypassing stop.

### ⑭ Still attack after two passes agree — user-driven deep review

**Pattern:** Two independent derivations agree → the agent declares "confirmed" → the user says "attack this solution" → the agent discovers a deeper hard limit.

**Root cause:** Two passes may converge on an intermediate-layer conclusion — correct but incomplete. Case from this session: the journal dirty shutdown; round 1 → `After=dbus`, round 2 → `Restart=on-failure`, round 3 agreed. After the user asked to attack the solution, the real bottleneck turned out to be the **WSL hard-coded 10s shutdown timeout** (journald flushing on an HDD can exceed 10s → exit≠0 → `on-failure` still triggers a restart).

**Fix:** Once two passes agree, automatically deep-attack before declaring "confirmed":
1. Can every premise of the fix be violated?
2. Is there a hard limit (hard-coded timeout, kernel behavior) that defeats the plan?
3. If a premise is violated, what is the consequence and what is the fallback?

#### ⑭b The deeper finding is often a *missing dimension*, not a deeper conclusion (2026-11-16)

**Pattern:** The agent reviews a plan, finds and fixes a few wrong statements, reports "结论核验完成 —— 3 处修正",
and the user has to ask again (`复查遗漏和失误`). The next pass finds that the plan never mentioned whole
required dimensions at all — 2 errors + 9 absent dimensions in the real case, while the first pass reported 3.

**Root cause (three compounding defects):**
1. **Iteration unit was the document itself.** Step 1 walks "every link in the reasoning chain", Step 2 re-derives
   "the conclusion". An absent dimension has neither a link nor a conclusion, so the traversal set excluded it **by
   construction** — no amount of blind re-derivation reaches it.
2. **Completeness was gated on the user's wording.** The phrase `复查遗漏和失误` unlocked the coverage audit; the
   phrase `用结论核验复查` did not. A rule that fires only when the user happens to name it is not a rule (same
   family as gating a check on a timer instead of on an event).
3. **Convergence was judged on "did this pass find anything", not on "did the category set grow".** The first
   pass's findings were all one category (wrong statements); the missing 9 spanned 8 brand-new categories
   (data-schema migration, downstream consumers of renamed tools, scheduler catch-up window, how the systemd unit
   is produced, backup duration, interpreter identity, `.env` rewrite, backup scope). Category growth is the
   signal that the baseline is too narrow — it was never read as one.

**Fix:**
1. An object-type gate, not a phrase gate: if the object is a plan / procedure / change proposal, build the
   external completeness baseline **on the first pass** (`references/change-plan-dimensions.md`).
2. Force all four quadrants into every report — wrong / absent / downstream-breaks / will-expire — even when a
   quadrant is empty.
3. Judge convergence on the **set of categories**. A new category ⇒ widen the baseline and re-diff; do not run
   another blind pass hoping it surfaces.
4. Print the coverage header (`遍历单位 / 覆盖维度 n/m / 缺席 k / 单样本数字 j`) at the top of the report. Without
   it, "checked only the statements" and "checked everything" are the same output.

### ⑮ Empty-string exception trap (`str(exc) == ""`)

**Pattern:** Exception is logged but `str(exc)` returns `""` — "keepalive failed: " (nothing after colon). Agent assumes benign and stops.

**Root cause:** `CancelledError()`, `ConnectionResetError("")`, and un-unwrapped `BaseExceptionGroup` all produce empty `str()`. The `_is_method_not_found_error` pattern checks `if not msg: return False` → empty exception treated as real failure → infinite reconnect loop.

**Real case (2026-07-28):** Both journal AND MCP investigations misled:
- MCP: `keepalive failed, triggering reconnect: ` — empty. Caused 6,212 process spawns in 63h. Root cause: `_is_method_not_found_error` returned False on empty `CancelledError()`
- Journal: `systemctl: D-Bus connection terminated` — an empty `ConnectionResetError` hid a Hyper-V IPC break

**Fix during diagnosis:**
1. If `str(exc) == ""`, check `type(exc).__name__` and `repr(exc)` — not just the string
2. For `BaseExceptionGroup`/`TaskGroup` errors, unwrap with `_unwrap_exception_group`
3. In verify-conclusion, classify empty-exception links as **Assumptions requiring type-level investigation**, not Facts
4. When proposing fixes, test: does the fix survive the empty-exception case?

### ⑯ Empty result ≠ unsupported parameter — trace the data the special case depends on

**Pattern:** A query returns `[]` with an optional parameter and returns rows without it → the agent declares "this version doesn't support that filter / silently matches nothing" and stops. The parameter is in fact supported, and is special-cased: it is popped out of the ordinary filter dict before validation (so it never raises the "column not allowed" error that a genuinely unknown key raises), then applied as a **data-dependent predicate** — membership windows, soft-delete flags, time bounds. The result set is empty because the boundary values in that table exclude every row, not because the parameter was ignored.

**Diagnosis rule — three checks in this order:**
1. **Grep the server source for the key**, not just the API response. Special-cased keys are handled separately from the validated filter whitelist, so "no error" tells you nothing about whether the key was understood.
2. **Read the predicate.** Whatever table the special case joins against, query it and compare its boundary columns against the row timestamps in the result set (joined-at / left-at, created-at windows, deleted-at). The empty result is explained when the boundary sits *after* the rows you expect.
3. **Find a positive case through the same parameter**, and it proves the parameter works: pick content that falls inside the window and re-run. A successful hit through the same filter kills the "unsupported parameter" hypothesis outright.

**Severity calibration:** without that positive case, the honest claim is "returns nothing for X"; "the feature is dead for everyone" is only allowed after a query inside the window also comes back empty.

**Upstream rule:** if the boundary value is suspiciously recent (equal to a process restart, a login, or an upgrade moment), the boundary is being **written** by something, not merely read — follow it to the writer (`grep` the upsert / `on_conflict` clause). A predicate whose boundary is reset on every restart silently shrinks the searchable set each time, which is a different (and worse) defect than a broken filter.

### ⑰ Plan verification: three shortcuts that fabricate a mechanism

A remediation plan ("clean up X", "don't touch Y", "no action needed") is where these three bite hardest.

**a) Never derive a mechanism by subtracting counts measured over different scopes.**
The classic: "row count rose by N, but only M rows carry a timestamp inside the reporting window, therefore N−M rows are re-inserted history." That subtraction is invalid whenever (i) the window's upper bound is earlier than *now* — everything written after the last measurement falls outside it; (ii) timestamps are not monotonic (backfills, imports, queued writes). Both are common.
**Fix:** use **insertion order** (the autoincrement PK / rowid that already existed in the older snapshot) or **two snapshots of the same table**, then test the claimed mechanism directly — does any new row match an existing row on the natural key? Zero matches kills "re-insert" outright.

**b) Separate stock from flow: measure the same quantity in an older snapshot and now.**
An anomaly is either pre-existing stock (already there before the window) or new flow (grew during it). One snapshot gives only the current level. Subtract the historical snapshot's measure and the two separate. Before blaming X for growth: if X already held ~97% of its current value in the last backup, X is not what grew this window.

**c) Negative claims carry the same evidence burden as positive ones.**
"Why we must not do Y" is a claim; unverified it hardens into a permanent false constraint. Two prohibitions that each collapsed under a single query: "deleting rows would desync the search index" (the table had insert/delete/update triggers — it would have stayed in sync); "VACUUM needs an equal amount of free space" (hundreds of GB free; the real cost was an exclusive lock, not space). Verify the mechanism behind a prohibition exactly like a proposed fix; if it fails, keep the recommendation only if a *different* verified reason supports it — and say which reason survived.

**Domain note:** for byte/disk-size anomalies the concrete attribution recipe (per-object deltas, index amplification factor, reconciliation across independent measures) lives in that host's own host-maintenance skill (its SQLite store-monitoring reference).

### ⑱ A skipped assertion reads exactly like a passing one — prove the exercised branch fired

**Pattern:** the verification harness reports `24 checks, 0 failed` while the assertions that matter never executed. Two shapes, both silent:
- **Nested under a guard on the artifact.** `if output.strip(): check(...)` — the detector short-circuited (e.g. "insufficient history, skip detection") and produced no output, so the output-dependent checks simply did not run. The suite is green and the feature is untested.
- **Fixture violates a precondition of the code path.** A rule like `if std > 0 and delta > mean + k·sigma` can never fire when the fixture's deltas are perfectly constant (std = 0), and `if len(baseline) >= MIN_DAYS + 1` can never fire on a fresh fixture. Both produce empty output, which the harness counts as nothing happening.

**Fix — in this order:**
1. Assert **reachability first, unconditionally**: a top-level check that the artifact is non-empty / the branch was entered, placed before any content assertion and never nested under `if output:`. Its failure message must carry the raw output and stderr.
2. Make the fixture satisfy every precondition of the path — enough history rows, and **variation** where the rule divides by or thresholds on a variance term. A fixture with constant increments disables every sigma-style rule.
3. Distinguish "no signal because clean" from "no signal because the path did not run" **in the product itself**: have the code emit which rule fired (threshold value, rule name). Then the absence of a rule label is itself evidence the branch was skipped.

**Unit-label corollary:** a derived metric labelled `KB` while computed in bytes passes every "contains the word KB" style check and is wrong by 1024×. Assert the **magnitude**, not the presence of the unit string (`float(seg) < 100`), and re-read one real run's output rather than trusting the test to have covered it.

**Related trap:** a whole-suite green from a project-wide test runner only proves each script exited 0. If a script's own assertions are conditional, the suite inherits the silence.

### ⑲ Before/after comparison without a control group proves nothing about the change

Any claim shaped "metric M moved after change X, therefore X worked" is an **inference with a confounder**, not a fact.
Time-series averages drift on their own, so slicing at almost any date produces a visible "shift".

**Fix — run the specificity test before printing any verdict:**
1. Take several **fake cut dates** besides the real one, spanning both sides of it.
2. Compute the same statistic (e.g. mean-before ÷ mean-after) at every cut.
3. If fake cuts yield an **equal or larger** shift — especially cuts that fall **before** the change, where it cannot possibly be the cause — the shift is not specific ⇒ the only honest verdict is **cannot determine**. Not "worked", and not "didn't work".
4. **Use equal-length windows on both sides of every cut, not whole-period means.** On a drifting series a whole-period before/after ratio lands below 1 at *every* cut, so every cut "looks like an improvement" and none is specific. Take the same number of data points immediately before and after each cut (e.g. 5 vs 5) and compare those. Then judge the **shape** at the real cut: a step/level break that never returns to the old level is the only shape that survives scrutiny; a slow monotone drift gives near-identical ratios at neighbouring fake cuts and settles nothing.
5. **Report one verdict per metric, never one verdict for the change.** A single change routinely yields mixed evidence: one metric bottoms out exactly at the real cut (suggestive) while another metric's minimum sits on a placebo cut (cannot determine). Collapsing them into one sentence either invents a success or destroys a real effect — print each metric's ratio, its verdict, and the confounder you could not exclude (e.g. a metric that also moves with session structure or traffic composition, not only with the change).

**"No effect" is a positive claim and needs positive evidence** (the distribution's ceiling/mode unchanged, the counter unmoved). It cannot be inferred from "the average did not drop" — an average can stay flat while a real effect exists, or drop for unrelated reasons.

**Companion trap — ratios whose numerator and denominator share a driver.** `total spend ÷ run count = cost per run` looks like a decomposition but both terms are functions of daily activity, so the ratio is near-constant by construction (observed: spend −15% and runs −15% simultaneously, giving 0.999, which "proved" that savings came from running less — a synthesised conclusion, not a measurement). Either find a denominator from an independent instrument, or report "both moved together, they cannot be separated".

**Same family — proving nothing changed requires checking the right object.** Before asserting "the count/size/total did not change", confirm the object you measured is the live one: leftover stores from before an upgrade keep old data and stop at the upgrade date, which reads exactly like "the writer stopped". Liveness = a 2xx write request in the access log + rows carrying the current period + only one instance of its kind. Two of three is a hypothesis, not a fact.

### ⑳ An alert describes the trigger condition, not the outcome

**Pattern:** a monitor fires `Job 'X' failed` / `worker exited with status 1` / `task crashed` → the agent adopts the alert's
framing and starts explaining *why it failed*. The system of record shows the same execution as `completed` and
delivered, with the full artifact produced. The alert described a **process event** (a supervisor watched its child
exit before the terminal record landed), not the task's result.

**Fix — in this order:**
1. Resolve the **outcome** from the authoritative ledger before writing any causal sentence: job store, execution
table, delivery table, and the produced artifact. Classify as `completed` / `failed` / `unknown`. **`unknown` is its
own state, not a synonym for `failed`.**
2. The alert line usually names only the detected event. The **real exception is chained into a different, longer
line emitted the same second** (`… paused with unverified admission: … : <root cause>` sits at the *tail*). Read that
line whole — `| cut`, `head -c`, or a viewer's column limit silently deletes the root cause and leaves you
explaining a wrapper message.
3. All-quantifier claims ("it fails every time", "it never succeeds") must be **counted in the ledger**, with the
retention window stated. These stores rotate (observed: only the last four rows survived), so "always" may rest on
a sample of one.
4. When alert and ledger contradict, the deliverable is **"this alert is a false positive — the run completed, here
is the artifact"**. Never manufacture a causal story for a failure that did not happen.
5. A **scheduler that keeps advancing `next_run_at` while `last_run_at` stays frozen** looks like a stuck job but is
not proof of one: dispatch attempts can miss their ack window and the job still runs minutes later. Decide from the
ledger + the produced artifact + the job's output directory, and re-read `last_run_at` before reporting "it hasn't
run". A watchdog line `worker did not acknowledge within Ns` coexisting with `status=completed` for the same window
is the same trap in a different coat.

**Related trap — evidence with a short half-life.** Worker stderr captures and reconcile/admission files are consumed
or unlinked once the task finishes; re-deriving later finds empty directories and a truthful "cannot determine".
Copy the on-disk evidence to a scratch directory during the *first* pass, before analysing it.

