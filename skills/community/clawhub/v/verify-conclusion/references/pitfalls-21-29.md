# Verify Conclusion · 陷阱 21–29（原文）

> 本文件由 `SKILL.md` 按需引用；条目文字与拆分前逐字节一致。

### ㉑ The observation point is not the object — a component's diagnostic string is not a verdict

**Pattern:** the agent measures a *neighbouring* object and calls it evidence.
- `/proc/<pid>/environ` is the **exec-time** environment snapshot. In-process `os.environ[...] = ...` never writes
  back to it, so "0 of N dotenv keys present in the gateway" says nothing about whether the file was loaded — the
  conclusion drawn from it ("writing to `.env` cannot work") was flatly wrong while the feature worked.
- A message produced by a **fallback branch** describes the branch, not the component that ran. A string like
  `no DISPLAY is set — X11 is not reachable` is chosen when discovery returned nothing; a different build whose
  spawn *failed* lands in the same branch, so the string is never proof of "the wrong binary is selected".

**Test:** ask "does this observation point move when the asserted object moves?" If the proxy can stay identical
across both possible states, it is not evidence. Then get an observation that *is* the object:
1. `grep` the source for the exact string and read the condition that selects it — the branch tells you what the
   message actually reports.
2. Exercise the claim in a **fresh process** rather than reasoning about a long-lived one (call the loader, then read
   the value; run the tool's own `doctor`/`status` subcommand).
3. Prefer the tool's declared self-report (`… doctor` printing the resolved path / active session) over any inference
   from side channel files.

**Corollary — the same trap in the negative direction:** "I checked the proxy and it looked consistent" is how a
wrong correction gets issued. Before retracting a working setup or contradicting your own earlier verification,
reproduce the mechanism at the real observation point; an over-correction is as costly as an over-claim.

**Corollary — "my own check came back empty" may just be the wrong field.** When a self-check reads empty or zero
off an artifact you just produced, settle the **field index** before concluding the producer emitted nothing.
Observed: a 7-column TSV verified with `awk -F'\t' '{print $9}'` returned empty → reported "the container column
is empty, the script is broken"; the data sat in `$7` and was complete. A check aimed one column off produces output
identical to a real defect, and because it is *your own* check you trust it faster than a third-party tool's.
Derive the column count from the format string itself (`awk -F'\t' '{print NF}'` on one real line), print it
beside the extracted value, and assert the expected count in the same check.

**Corollary — a probe must be able to observe the property you are asserting.** Reachability was tested by reading
an HTTP status code off ports 135/445, got `000`, and was reported as "unreachable" — those ports are not HTTP
services, so the probe could not have observed reachability in either direction. A TCP connect against the same
ports succeeded. Any probe whose output is invariant across both possible states of the claim is not evidence
(the same test as above, applied to the *measurement protocol* rather than the object). Also run a **known-positive
and a known-negative case side by side**: without a control, "no response" and "wrong protocol" are the same
observation.

### ㉒ The default preset is not the capability ceiling

**Pattern:** a tool or web UI opens on a default option (last 30 days, current period, first-level menu, default
filter). The result looks coarse — daily instead of hourly, summary instead of breakdown — so the agent declares
"this platform cannot produce X granularity" and writes it into a report. The capability was one non-default choice
away: a custom range whose start and end are the SAME day/hour yields the fine-grained rows, an "advanced/more"
branch holds the switch, the export dialog has its own granularity control.

**Fix — exercise the option surface before any "cannot" claim:**
1. Open the range/period/step selector and try the **extreme** admissible setting (single day, single hour, one
   row) rather than only the presets.
2. Open every "高级 / 更多 / 自定义" branch of the same control and of the export/save dialog.
3. Only if the finest admissible selection still returns coarse data may you state the ceiling — and say which
   option you tried, so the user can correct the path instead of just the conclusion.

This is a claim about the **option surface**, not about the data: it fails the "what command/click proves this
wrong?" test until you have actually selected the fine-grained option.

### ㉓ A known-broken instrument's silence is not evidence of inactivity

**Pattern:** telemetry for a period is missing → the agent reads "last record at T, nothing after T" as "nothing
happened after T" and reports the loss as ≈ 0. But the instrument had been down for the whole period, so its
silence carries **no information about activity**. Measured counter-example: the supposedly quiet window held a
full turn (5 assistant messages + 4 tool results) — real work, none of it recorded. The loss estimate was off by
an entire turn, and the error ran in the direction of understating.

**Root cause:** this is absence-of-evidence **inverted**. The familiar trap treats a missing observation as proof
of health; this one treats a known gap as proof of inactivity. Both use the instrument's output as if it tracked
the system, when the instrumentation is itself the thing that broke.

**Fix — in this order:**
1. Establish **when the instrument was writing at all** before interpreting any window. If it was down across the
   whole window, every claim about that window must come from a source that was up.
2. Size the gap from **measured activity in an independent ledger** (message / turn / row counts filtered by
   timestamp), never from the interval between consecutive records.
3. Express the loss in units that ledger can produce (turns, calls, rows). "≈ 0" is admissible only after that
   count comes back zero — not because the record stream was empty.

**Test:** "If activity had occurred here, would this instrument have recorded it?" When the answer is no, the
observation is not evidence in either direction.

### ㉔ Counting log lines that mention an object is not counting the event you claim

**Pattern:** `journalctl -u docker | grep -c '<container-name>'` returned 5 and 13 for two days and 1 for a third
→ reported as "the container **crash-restarted** 5 and 13 times" → built a causal story ("restart churn → memory/CPU
spike → plugin load timeout") on top of it. Every one of those lines was `sbJoin` (network endpoint rebinding); a
`grep -E 'restart|die|kill|health'` over the same window returned **zero** events. The whole explanation collapsed,
including the "why did today work" answer that was its only payload.

**Mechanism:** a container/process name appears in nearly every log category — networking, attach, exec, health,
signal. Substring-matching the name counts *mentions*, and mentions are dominated by whichever subsystem is noisiest,
not by the event under investigation.

**Fix — three checks, cheapest first:**
1. **Count the event verb or the structured field**, not the object name: `grep -E 'restart|die|kill|OOM'`, or parse
   `level=`/`msg=` fields. Never infer "restarted N times" from name matches.
2. **Sanity-check the implied rate.** A container restart count implies a restart interval; neighbouring timestamps a
   few seconds apart (observed: 14 s between "Next.js restarts") are physically impossible for that runtime. **An
   implausible derived rate is proof the event semantics are wrong**, not a surprising finding to report.
3. **Prefer the component's own counter** (`docker inspect -f '{{.RestartCount}}'`, a supervisor's restart tally, a
   status subcommand) over log archaeology. If the authoritative counter cannot reach back far enough, say the
   historical count is **unknown** rather than reconstructing it from text.

**Consequence rule:** when a causal story's *only* discriminating evidence is a count that later turns out to be a
mis-parse, the story does not degrade to "weaker" — it degrades to **cannot determine**, and any "and therefore
X" sentence built on it must be retracted explicitly.

### ㉕ "It self-healed" needs a re-measurement, not one later success

**Pattern:** `N` export failures clustered in one minute, then a successful write ~30 s later → reported as
"transient jitter, self-healed within 3 minutes, low impact". Re-reading the same counter later in the session showed
the count had risen again. The failure mode was **intermittent at low rate the whole time**; the interleaved successes
were never evidence that it had stopped.

**Mechanism:** a later success proves the code path *can* work. It says nothing about the failure rate, and
intermittent failures produce successes between them by construction — so "failure followed by success" is the normal
signature of a *still-active* low-rate fault, not of recovery.

**Fix:**
1. Report the shape as `N failures, first at A, last at B` plus the observation window — never the adjective
   "transient" on its own.
2. **Re-read the counter at the end of the session** before writing "recovered / self-healed / back to normal".
   A counter that grew across the investigation is a live defect regardless of how sparse it looks.
3. If you cannot re-read it, the honest verdict is **"intermittent; count as of T = N"** — "self-healed" is a claim
   you have not earned and it suppresses the only alarm the system was raising.

### ㉖ One measurement window is not a rate — define the window before characterising it

**Pattern:** a single 10-second sample showed a large swap-out spike → reported as "swap thrashing is continuous";
six further 10-second windows showed almost nothing → retracted to "periodic spikes"; re-reading the free-swap
counter hours later showed it had been falling steadily the whole time, which neither window had measured. Three
verdicts, each drawn from a window too short or too narrow to support it.

**Mechanism:** "steady", "periodic", "bursty", "high" are properties of a **rate**, and a rate needs a stated
denominator (window length) plus a baseline (what this metric does when nothing is wrong). A single sample supplies
neither, so whichever value it happened to land on silently becomes the characterisation — and a second sample that
disagrees just swaps one adjective for another.

**Fix:**
1. **State window and units before the adjective** (`N pages / 10 s`), take ≥3 equal-length consecutive windows, and
   report the spread (min–max or the per-window series) instead of one representative number.
2. **Prefer a monotonic counter over a windowed rate** when the question is "is this still happening": a free-space /
   total-events counter read at the start and again at the end settles it with no window-length argument at all.
3. **No baseline ⇒ no adjective.** "No historical baseline, so this level cannot be called abnormal" is a legitimate
   finding; "high" is not. When you install the sampling that would create a baseline, say that the first verdict
   is only available later.

### ㉗ A compound forecast is only as strong as its weakest factor — and every optimistic factor compounds

**Pattern:** a claim shaped `baseline × reduction-A × reduction-B ⇒ ¥Y saved per month`. The baseline came from the
**most active 5-day window** while being called "the daily average" (it was 1.8× the full-period mean), and the two
reduction percentages were never measured at all. Presented as a plan with a number attached; when re-checked, the
figure was 2–2.5× the real ceiling.

**Mechanism:** unlike pitfall ⑲ (one change, one before/after) this is a *product*, so verification must treat each
factor separately — and the failure is not symmetric. Baseline inflation and invented reductions are both biased in
the **favourable** direction (you propose a saving, so you reach for the flattering input), so they multiply instead
of cancelling. A product with one measured factor and two guessed ones is a *guess*, regardless of how many digits
it carries.

**Fix:**
1. **Decompose to the measured factors before printing any total.** For each factor write `measured / assumed`
   explicitly in the sentence that carries the number. If any factor is `assumed`, the total may not appear in a
   conclusion sentence — only as a labelled upper bound.
2. **Baseline window must match the claim's scope.** Reporting "per month" requires a full-period mean; a recent
   peak window, a best-campaign week, a post-change stretch are all **selection-biased baselines**. Then compare the
   *target* against the baseline: a target more generous than the current average means the claimed saving does not
   exist at that magnitude.
3. **Cross-check the top of the product with the bottom.** Compute the same forecast from the most pessimistic
   admissible factor values. If the plausible range spans an order of magnitude, the deliverable is the range and
   the dominant uncertainty — never the mid-point alone.
4. **Rank the levers after measuring composition, not before.** Where a total is the sum of parts with known shares,
   an improvement to a part can only move the total by `Δpart × share`. Without the shares you will order the plan
   by which lever *sounds* strongest (observed: the weakest lever, worth a 20% share, was listed first and the
   strongest, on a 42% share, third). Measure shares first; the ranking is then arithmetic rather than opinion.
5. **Apply the perturbation only to the terms it actually drives — write the driver map first.** A "−32%" applied
   uniformly across every term is a *hidden assumption* that all terms share one driver. Observed: request count
   was cut 32% and applied to both cached-input and uncached-input tokens, giving 19.8% saved; request count only
   drives the cached term (each request re-reads the context), while the uncached term is driven by *new content*
   and barely moves — the real figure was 6.4%, a 3× overestimate. Before propagating any change, list every term
   and answer "what physically produces this quantity?"; a term whose driver is not the thing you are changing
   must be held constant. Uniform perturbation is the default failure because it looks symmetric and therefore fair.

**Test:** "for each factor, which command produced this number?" Any factor with no answer is an assumption, and
it drags the whole product down to an assumption.

### ㉘ Proving a parameter took effect: compare identity, not a payload hash

**Pattern:** to test whether `&start=3` / `page=2` is honoured, hash the whole response and compare
hashes across variants. Three variants → three different hashes → "the parameter works". Reversing to
`feedbackUser.userId` + body text showed the same three records in the same order for every variant:
the parameter was being ignored. The hash differed because each item carried per-request volatile
fields (`preloadTime`, timestamps, request hints).

**Mechanism:** a whole-payload digest is sensitive to every field, including the ones the server
rewrites on each call, so it is **almost never equal** — which makes "params ignored" and "params
worked" produce the same observation ("hashes differ"). A test whose output is invariant across both
states of the claim is not evidence (see ㉑'s probe corollary).

**Fix:**
1. Pick **stable identity fields** (primary key, author id + timestamp, item URL) and compare the
   returned **sets/sequences**, not digests. Report the identity list beside each variant's verdict.
2. When a cursor field is present (`startIndex` / `nextStartIndex` / `hasMore`), read it too — but a
   cursor that stays at 0 is weak evidence on its own; the identity comparison is the decisive one.
3. A count read off the DOM or an API payload is a count of *nodes*, not of *records*. Dedupe by
   stable identity before writing "N items loaded" — container + inner-component selectors match the
   same record twice, so "3 → 6 after clicking" can mean nothing was loaded at all.

**Sibling shape — 200 with an empty payload is usually a block, not an absence.** Same schema, same
key count, no error message, but the payload collapses (observed: 72,701 → 1,505 bytes, `list: []`).
Before reporting "there is no data": compare `size` and key count against the last good response, and
state which of the two you are looking at. A silent throttle read as "empty" is how a soft block gets
reported as a negative finding.

### ㉙ Reviewing a plan or a prior claim: count, carrier, and declaration traps

**a) A count inside a plan is itself a claim — re-count it, and settle the UNIT first.**
A proposal phrased "generalize the 3 hardcoded paths" carries two assertions: the number, and the population it
counts. Grep the real file (`grep -n '<pattern>' <file>`) and print the enumeration, not the total. Observed: the
"3 places" were 1 place in the file plus 2 lines that merely contained the word (one already generic, one with no
path at all); "3" only became true when the unit was read as "3 copies × 1 place each". Different unit ⇒ different
files, different edits, different acceptance test. Restate count + unit + enumeration before touching anything.

**b) To decide "did this tool already check X?", grep the SOURCE — never one run's result file.**
A result file is one run's output, and a sibling probe's output says nothing about this probe. Observed: grepping the
second probe's result for a config key returned zero hits → "it never checked that" was reported to the user; the
first probe's source queried exactly that key and its result file had recorded the value. That is a **false
correction**, which costs as much trust as a false conclusion. Find the reporter's code (`grep -n '<key>|reg
query|Get-ItemProperty|Get-CimInstance' <script>`), then read its output.

**c) Before adding a restrictive declaration to a document, grep the body for instructions that contradict it.**
Appending "read-only checks only" to a skill whose body already requires running a minimal repair probe (a dry-run
`ALTER TABLE`, a SIGTERM reachability test) makes the document argue with itself, and the reader follows whichever
line they hit first. Either narrow the body (only state-preserving probes may run) or word the declaration to match
it ("state-changing operations require explicit user approval"). Verify by grepping the same file for the forbidden
verbs before and after the edit.

**d) Existence is not a path-test question for a file that is exclusively held.**
`Test-Path 'C:\pagefile.sys'` returns False while the file is present at full size — the memory manager holds it
open. Same family as ⑪: the probe reports the access result, not the inode. Decide existence with a directory
listing (`dir /a-d /a`, `ls -la <dir>`) and print the matched line with its size.

**e) A status field is only interpretable when its recorder was enabled.**
`BugcheckCode = 0` alongside `LogEvent = 0` and dumps disabled cannot distinguish "no crash occurred" from "a crash
occurred and nothing was written". Read the recorder's own switches first, then either state the weaker claim ("no
crash was *recorded*") or leave it unknown — never "confirmed there was none".

