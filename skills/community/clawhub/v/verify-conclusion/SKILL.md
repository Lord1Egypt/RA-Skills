---
name: verify-conclusion
description: "诊断结论、调研发现或推断出炉后就地开始自检：先逐环拆推理链，再换思路从零盲推；审查对象是计划/方案/变更单时第一轮就先建外部完备性基线再逐维对照，拦截过早结论、未经验证的假设与因果混淆。用户说「确认吗／再验一下／复查」也触发。"
version: 1.3.1
author: "rocketdemon"
license: MIT-0
trigger: Fires immediately after producing a diagnostic conclusion, research finding, or any inference from collected evidence; when the object is a plan/procedure/change proposal, always build the Phase 0 completeness baseline on the first review pass. Also fires when the user says `确认吗`, `再验一下`, `复查`, `肯定吗`, `你验证了吗`.
metadata:
  hermes:
    tags: [verification, reasoning, debugging, quality]
    related_skills: [systematic-debugging]
---

# Verify Conclusion

## Overview

LLM agents are prone to declaring conclusions from incomplete evidence — confusing correlation with causation, stopping at the first plausible explanation, or asserting claims that can't be verified. This skill forces a structured second pass: attack the reasoning chain, then blind re-derive. If the two passes agree, the conclusion survives scrutiny. If they don't, iterate until convergence or escalate.

## Scope

- **No runtime dependency.** Markdown only: no scripts, no database, no network. It works the
  same in any agent harness that can read a skill file.
- **Examples are real incidents from one self-hosted agent host (2026).** Every count, threshold
  and window in them is a *historical measurement*, not a recommended setting — re-measure on
  your own system before reusing a number.
- **Two harness-specific spots, both flagged in place:** the transcript-search tool named in
  trap ⑤, and the byte-size attribution recipe in trap ⑰ (a companion write-up that is *not*
  bundled). Everything else is harness-agnostic.
- **Trigger phrases are kept verbatim in Chinese** (`确认吗`, `再验一下`, …) because they are
  what the user actually types; translating them would break the trigger.
- **Read-only unless a repair is explicitly approved.** The skill itself never executes
  anything. When a conclusion implies a repair, only state-*preserving* probes are allowed;
  anything that changes state (delete, service reload/restart, `VACUUM`, config change) needs
  the user's explicit approval first. Trap ⑨ is constrained the same way.

## When to Use

**Trigger immediately after** the agent produces any of:
- A diagnostic conclusion ("X caused Y", "root cause is Z")
- A research finding or synthesis
- An inference from collected clues/evidence
- Any claim marked as `关键结论` (key conclusion) or `根因` (root cause)
- **A remediation / handling plan** ("do X", "don't do Y because it would break Z", "no action needed") — a plan is a bundle of causal claims and negative claims, and it gets the same two passes. A plan that was proposed but not yet executed is exactly when verification is cheapest.

**Also trigger when user says:**
- `确认吗` / `肯定吗` / `再验一下`
- `你确定？` / `复查一遍`
- `用SKILL检查` / `用skill验证` / `用验证结论的skill`
- Any expression of doubt about a conclusion

**Do NOT trigger on:**
- Routine status reports (infrastructure checks, health pings)
- Simple factual lookups with no inference
- Steps within an already-verified chain

## Steps

### Step 0: Classify the object — and build the baseline FIRST (mandatory for plans)

Before any chain attack, decide **what kind of object** is being reviewed. This step is triggered by
the object's type, **never by the user's wording**.

| Object type | Required additional phase |
|---|---|
| A diagnostic conclusion / root-cause claim | Step 1 + Step 2 only |
| A research finding / synthesis | Step 1 + Step 2 only |
| **A plan, playbook, checklist, procedure, change proposal (upgrade / migration / refactor / cleanup), or any deliverable another party will execute** | **Phase 0 baseline (below) is mandatory, on the first review pass** |

**Why this step exists (real failure, 2026-11-16):** an upgrade plan was reviewed on the user's first
request (`用结论核验复查`). That pass used Step 1 + Step 2, found 3 wrong statements, and declared done.
The user then said `复查遗漏和失误` and a third pass found **2 more errors and 9 dimensions the plan had
never mentioned at all** (data-schema migration, downstream consumers of removed tool names, cron
catch-up window, how the systemd unit is produced, backup duration, interpreter identity, `.env`
rewrite, backup scope). Root cause: the first pass's iteration unit was *the document's own
statements* — an absent dimension has no statement to attack, so it was invisible by construction.
Gating completeness on a user phrase is the same defect as gating it on a timer: it does not fire.

#### Phase 0: build the completeness baseline from independent sources

Three sources, none of them the document under review:

1. **Governing skill's gates** — the checklist of whichever skill owns this task class on that
   host: for upgrades, that host's upgrade-assessment and maintenance skills; for incidents, its
   systematic-debugging skill. Name them in your own notes, not in a published package.
2. **The target system's own authority** — source code, schema, unit files, config migrations,
   release notes at the target version, `--help` of the actual tool.
3. **The user's stated requirements** — including constraints stated in earlier turns.

Produce a table and fill every row before writing any finding:

| Dimension | Judged from (source) | In the document? (yes / **absent** / n.a.) | Evidence |
|---|---|---|---|

For change-type deliverables, start from `references/change-plan-dimensions.md` (11 lifecycle
dimensions) rather than inventing the list from the document.

**Then iterate the four quadrants — all four must appear in the report, even when empty:**

| Quadrant | Question | Typical yield |
|---|---|---|
| ① Wrong statement | Is this claim true? | what Step 1/2 catch |
| ② Absent dimension | What must exist but is not written? | **usually the majority of findings** |
| ③ Correct but downstream breaks | Who consumes this name/path/field and is not updated? | renamed tools, dead references |
| ④ Correct but will expire or is unstable | Which numbers drift, which assumptions have a shelf life? | single-sample measurements, version drift |

### Step 1: Stress-test the reasoning chain

For every link in the reasoning chain, classify it:

| Type | Definition | Action |
|------|-----------|--------|
| **Fact** | Has direct evidence (log line, file content, timestamp, exit code) | Verify the evidence source still exists and is correctly cited |
| **Assumption** | Reasonable but unverified (default behavior, common pattern) | Flag explicitly, assess risk if wrong |
| **Inference** | Derived from facts (X happened, therefore Y) | Check for alternative explanations |

Then ask:

1. **Causality check:** Did X happen before Y, and is there a mechanism connecting them? Correlation is not causation.
2. **Upstream check:** For every cause identified, ask: what caused THAT? Stop only when reaching a system boundary or already-known factor.
3. **Verifiability check:** For every diagnostic claim, ask: "What command would prove this wrong?" If no such command exists, the claim is unfalsifiable — flag as weak.
4. **Completeness check:** Were any clues seen but not incorporated? Were any investigative steps skipped?
5. **Fix feasibility check:** Does the diagnosis imply a repair action (ALTER TABLE, config change, etc.)? If yes, run the most lightweight validation that confirms the fix can be applied before declaring the diagnosis complete. **The probe must not change state.** If the only available probe would itself perform the
repair (a real `ALTER TABLE`, a service restart, a `VACUUM`, a delete), stop and ask for approval first — a feasibility check that performs the repair is no longer a check. A diagnosis whose repair path is blocked is an incomplete diagnosis — flag it and identify the blocker. Examples: before declaring "add TTL" as the fix, run ALTER TABLE with a low-timeout dry-run; before declaring "restart service X" as the fix, check that the service can respond to SIGTERM. Do NOT defer this check to the implementation phase — a fix that can't be applied invalidates or constrains the diagnosis.

Output: either "No weaknesses found" with a specific defense of each link, or a numbered list of weaknesses.

### Step 2: Blind re-derive

Start fresh. Do NOT reference your first-pass conclusion. Collect evidence from scratch, form hypotheses, test each, and arrive at a conclusion independently.

**Critical — methodological independence:** Step 2 must use a **different reasoning strategy** than Step 1. The goal is not to use different tools — it's to approach the problem from a different cognitive angle, so the same blind spot doesn't trap both passes.

**Reasoning-strategy cross-check: what Step 1 used → what Step 2 must switch to:**

| Step 1 reasoning strategy | Step 2 must switch to | Why it differs |
|----------------|----------------|-----------|
| Symptom → cause (bottom-up) | Hypothesis → elimination (top-down) | Bottom-up tends to chase the first clue; top-down forces you to enumerate every possibility first, then eliminate them one by one |
| Inside-the-component view of A | Boundary/upstream view via B | Staring inside one component → cross-component dependencies get ignored |
| Log-driven (look for errors) | State-driven (read current values) | Logs only record what happened; state tells you what actually is |
| Timeline reconstruction (order of events) | Dependency-chain reconstruction (A depends on B) | Temporal correlation ≠ causation; the dependency chain is closer to real causation |
| Single-hypothesis verification | Competing hypotheses | Once locked onto one hypothesis you tend to seek only supporting evidence and ignore counter-evidence |
| Before/after comparison of a time series | Placebo / negative-control cut points | A before/after split gives the suspected change all the credit; fake cut points show whether the series would have moved anyway |

**Decision rule:** it is not about whether the tools sit at the same layer — it is about whether the **reasoning direction** changed. Different tool, same reasoning direction → false independence.

**Typical cases of false independence:**
- Step 1 used `journalctl` to read the Gateway log (bottom-up) → Step 2 used `tail logfile` to read the Gateway log (still bottom-up) → false independence: the tool changed, the thinking did not
- Step 1 used `docker exec` to inspect ClickHouse internals (inside-the-component view) → Step 2 used `curl` against the ClickHouse HTTP endpoint (still inside-the-component view) → false independence

The two passes agree → **Conclusion confirmed** ✅. Stop.

**Coverage audit is object-triggered, not phrase-triggered.** If the object is a plan/deliverable, the
baseline of Phase 0 was already required on the *first* pass — there is no "further pass" that unlocks
it. When the user nevertheless says `复查遗漏和失误` / `再查一遍`, treat it as evidence that the earlier
pass was incomplete: **go back to Phase 0 and widen the baseline**, instead of merely re-deriving again.
Two blind passes can agree and still miss the same dimension, because both were built out of the
document's own structure.

The coverage pass must:

1. Build the checklist of what a *complete* answer to this class of task must contain from
   **independent sources** — the governing skill's gates, the target system's own source/docs/schema,
   the user's stated requirements — not from the document under review.
2. Diff that checklist against the document and report **what is absent** separately from **what is
   stated wrongly**. Absent dimensions are usually the majority of findings: a pass that only lists
   wrong statements can announce "3 corrections" while nine required dimensions were never mentioned.
3. Re-attack every number the plan will be built on, asking whether one sample is even a stable value.
   A plan's error bar is set by its worst number, not its average.

### Step 3: Re-derive again (up to 3 attempts)

If pass 2 disagrees with pass 1, record the specific difference. Then re-derive a third time, blind to both previous attempts.

If passes 2 and 3 agree with each other (but not pass 1), accept the majority result. ✅

If all three disagree with each other:
- Document: what was attempted, what each pass found, why they differ
- State: **"The conclusion is not self-consistent — human intervention required."**
- Stop.

### Completion criteria

- Every link in the reasoning chain classified as fact/assumption/inference with source
- At least two independent derivations performed
- Agreement reached OR escalation with clear documentation of divergence
- **Convergence is judged by category growth, not by "I found some issues"** — record the *set of
  finding categories* per pass. If a later pass produces a **new category** (not another instance of
  a known one), the baseline was incomplete: widen Phase 0 and re-diff. A pass that finds 3 wrong
  statements proves nothing about the 9 dimensions nobody looked at.
- **Every review report opens with a coverage header, or the review is not finished:**
  `遍历单位=<document sections | external dimension list> / 覆盖维度 n/m / 缺席 k / 单样本数字 j`.
  A report that shows only findings is indistinguishable from one that only checked the statements.
- **Numbers this turn produced are Assumptions, not Facts, until a second sample exists** (a fresh
  measurement is not corroboration of itself; name the cache/warm state of each sample).
- The four quadrants of Step 0 are all answered (① wrong ② absent ③ downstream ④ expiring),
  explicitly saying "empty" where nothing was found.

## Common Pitfalls

本条技能共 29 条陷阱，完整原文按编号分三份放在 `references/`，按需读取，避免一次性灌进上下文。

- 陷阱 1–10：`references/pitfalls-01-10.md`
- 陷阱 11–20：`references/pitfalls-11-20.md`
- 陷阱 21–29：`references/pitfalls-21-29.md`

**何时必须读**：命中下面任何一条的情形时，先读对应 reference 再下结论。

- ① Temporal correlation mistaken for causation → `references/pitfalls-01-10.md`
- ② Stopping at the first plausible explanation → `references/pitfalls-01-10.md`
- ③ Unverifiable diagnostic assertions → `references/pitfalls-01-10.md`
- ④ Reflexive attribution to recent changes → `references/pitfalls-01-10.md`
- ⑤ Intermediate state reported as final conclusion → `references/pitfalls-01-10.md`
- ⑥ Apologize first, investigate later → `references/pitfalls-01-10.md`
- ⑦ Agent forgets to auto-trigger verification → `references/pitfalls-01-10.md`
- ⑧ Testing with fake credentials produces false results → `references/pitfalls-01-10.md`
- ⑨ Diagnosis complete but fix blocked — verification stopped too early → `references/pitfalls-01-10.md`
- ⑩ User asks to run the SKILL check = execute the full Step 1 + Step 2 → `references/pitfalls-01-10.md`
- ⑪ Output from a restricted tool treated as fact → `references/pitfalls-11-20.md`
- ⑫ Tool output treated as a logical assertion (the `|| echo` anti-pattern) → `references/pitfalls-11-20.md`
- ⑬ Declaring "root cause found" on the first bug → `references/pitfalls-11-20.md`
- ⑭ Still attack after two passes agree — user-driven deep review → `references/pitfalls-11-20.md`
- ⑮ Empty-string exception trap (`str(exc) == ""`) → `references/pitfalls-11-20.md`
- ⑯ Empty result ≠ unsupported parameter — trace the data the special case depends on → `references/pitfalls-11-20.md`
- ⑰ Plan verification: three shortcuts that fabricate a mechanism → `references/pitfalls-11-20.md`
- ⑱ A skipped assertion reads exactly like a passing one — prove the exercised branch fired → `references/pitfalls-11-20.md`
- ⑲ Before/after comparison without a control group proves nothing about the change → `references/pitfalls-11-20.md`
- ⑳ An alert describes the trigger condition, not the outcome → `references/pitfalls-11-20.md`
- ㉑ The observation point is not the object — a component's diagnostic string is not a verdict → `references/pitfalls-21-29.md`
- ㉒ The default preset is not the capability ceiling → `references/pitfalls-21-29.md`
- ㉓ A known-broken instrument's silence is not evidence of inactivity → `references/pitfalls-21-29.md`
- ㉔ Counting log lines that mention an object is not counting the event you claim → `references/pitfalls-21-29.md`
- ㉕ "It self-healed" needs a re-measurement, not one later success → `references/pitfalls-21-29.md`
- ㉖ One measurement window is not a rate — define the window before characterising it → `references/pitfalls-21-29.md`
- ㉗ A compound forecast is only as strong as its weakest factor — and every optimistic factor compounds → `references/pitfalls-21-29.md`
- ㉘ Proving a parameter took effect: compare identity, not a payload hash → `references/pitfalls-21-29.md`
- ㉙ Reviewing a plan or a prior claim: count, carrier, and declaration traps → `references/pitfalls-21-29.md`
## Verification Checklist

- [ ] Every link in the reasoning chain has a type (fact/assumption/inference) and source
- [ ] At least one alternative explanation was considered and tested
- [ ] Every diagnostic claim passes the "what command verifies this?" test — **including every "don't do X" rationale**
- [ ] No delta-of-two-counts was used to infer a mechanism; insertion order or two snapshots was used instead
- [ ] The upstream chain was traced at least one level deeper than the initial finding
- [ ] No recent-change attribution was made without isolation testing
- [ ] Session_search results were confirmed against session endings, not mid-session snapshots
- [ ] Any "X does not work / returns nothing" claim was either localized to a data window or proven global by finding a positive case through the same parameter
- [ ] For every "tests pass" claim: an explicit check proves the exercised branch actually ran (not merely that it exited 0)
- [ ] For every "X changed M, so X had an effect" claim: a placebo/negative-control cut test was run, and the verdict is one of `attributable / cannot determine / data does not cover` — never "no effect" without positive evidence
- [ ] Every alert / crash notification was checked against the authoritative ledger **before** any causal explanation was written, and its outcome classified as `completed` / `failed` / `unknown` (never collapsed into "failed")
- [ ] Any long log line that carries the chained root cause was read untruncated, not filtered through `cut` / `head -c`
- [ ] Every "I measured it and it says X" link was checked against "does this proxy change when X changes?" — exec-time
      snapshots, fallback-branch message strings, and cached/derived files are not the object itself
- [ ] A "job/worker has not run" claim was re-checked against `last_run_at` + output artifact, not inferred from a
      sliding `next_run_at` or a single watchdog timeout line
- [ ] Every "this tool/platform cannot produce X" claim names the **non-default** option that was actually tried
      (custom range with start = end, advanced branch, export dialog), not just the default preset
- [ ] Every "nothing happened during this window" / "the loss was ≈ 0" claim was cross-checked against an
      independent ledger, after confirming the instrument was actually live across that window
- [ ] Every count presented as an event count (restarts, failures, reconnects) was matched on the **event verb or a
      structured field**, not on the object's name appearing in a log line — and the implied rate was sanity-checked
- [ ] Every "recovered / self-healed / transient" verdict was backed by **re-reading the same counter later in the
      session**, not by a success that merely followed a failure
- [ ] No total was summed across mixed bases; a printed "do not add these" caveat was followed by not adding them
- [ ] Every "steady / periodic / bursty / high" characterisation names the sampling window, the number of equal
      windows compared, and the baseline it was judged against — or states that no baseline exists
- [ ] Every probe's output was shown to differ between the claim's true and false states, with a known-positive and
      a known-negative case run side by side
- [ ] Every compound forecast (`baseline × %→ amount`) lists each factor as **measured** or **assumed**, uses a
      baseline window matching the claim's scope, and appears as a range rather than a single number when any factor
      is assumed
- [ ] Every propagated change names the **driver** of each term it touches; terms whose driver is not the thing
      being changed were held constant rather than perturbed by the same percentage
- [ ] Every "this parameter is / is not honoured" claim compared **stable identity** across variants
      (not whole-payload hashes, which differ on every call because of volatile fields), and any count
      quoted as "N items" was deduped by identity first (nested wrapper nodes double-count)
- [ ] Every "there is no data" claim was checked against a size/key-count delta versus the last good
      response, so a 200-with-empty-payload throttle is not reported as an empty result
- [ ] Where the data carries a **redundant encoding** of the classification you applied (a price tier that implies
      peak/off-peak, a status field that implies success, an index that implies ordering), your rule-derived split was
      cross-checked against it and matched to the unit — agreement validates the classifier for free, and a mismatch
      exposes it before the finding goes out
- [ ] Every count quoted from a plan or an earlier claim was re-derived by grep and printed with its **unit and
      enumeration** (file:line), not accepted as given
- [ ] A "this script/tool never checked X" claim was grounded in the script's **source**, not in one run's result file
- [ ] Any restrictive declaration added to a document was cross-checked against instructions in the same document
      that demand the opposite action — body and declaration edited together or not at all
- [ ] File existence was decided by a **directory listing**, not a path test, for files that may be exclusively held open
- [ ] Any status field used as evidence was first validated against the switches of the recorder that writes it
- [ ] When the task was "review this plan/document for omissions", the pass was driven by an **independently built object checklist** diffed against the document, and missing dimensions were reported separately from wrong statements
- [ ] Every duration / size / throughput figure the plan will be built on came from **at least two samples whose cache or warm-state is named**, or is stated as a range with the worst case — a single sample is never quoted as "the measured value"
- [ ] Any "the file/library is corrupt" error raised by an inspection tool was first checked against **whether that tool loads the same extensions the runtime does** — a checker with a narrower extension set reports a channel gap as damage
- [ ] If the object was a plan / playbook / change proposal: the **Phase 0 baseline was built from independent sources on the first pass**, and the report's coverage header states the iteration unit, `n/m` dimensions covered, and how many dimensions were absent
- [ ] Every finding was assigned to one of the four quadrants (wrong statement / absent dimension / downstream consumer breaks / will expire), and each quadrant was reported even when empty
- [ ] Convergence was judged on the **set of finding categories**; a new category in a later pass triggered a baseline re-widening rather than another blind re-derivation
- [ ] Numbers produced during this very turn were labelled **assumption** until a second, differently-conditioned sample existed — a fresh measurement never corroborates itself
