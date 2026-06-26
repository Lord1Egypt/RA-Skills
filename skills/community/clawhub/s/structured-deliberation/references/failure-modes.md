# Failure Modes — What to Watch For

Multi-agent deliberation has predictable failure modes. This catalog names them, gives detection signals, and prescribes responses.

Use this document during running deliberations (to detect emerging failures) and during retrospectives (to diagnose what happened).

---

## FM-1: Sycophancy Cascade

**What it is**: Agents converge on a position not because the position is well-grounded, but because each agent updates toward the others' apparent confidence. Over rounds, disagreement vanishes; consensus looks robust but is hollow.

**Detection signals**:

- B1 (sycophancy resistance) trending negative: disagreement slope ≤ -0.2 across rounds
- All verifications return ROBUST in a string of rounds (no BROKEN flips)
- Critic's attacks shift from "challenges to specific decisions" to "rhetorical concerns about general principles"

**Why it's dangerous**: from outside, sycophantic consensus looks identical to genuine convergence. The deliberation looks productive, but the conclusions don't survive contact with reality.

**Response**:

1. Escalate Critic pressure: tighten the Critic schema to require ≥1 specific target per round (not "general concerns")
2. Insert a STRESS-CRITIC round (Critic absent) — see if other roles produce adversarial work, or whether the system relaxes
3. Audit recent decisions: do they cite specific evidence (claims with `testable_*` status), or do they cite general agreement?

---

## FM-2: All-BROKEN Performative Adversariality

**What it is**: Critic role over-produces BROKEN verdicts. Every claim is challenged, every architecture is fragile, every decision is suspect. Looks like rigorous criticism but is performative — Critic is performing the role rather than identifying real failures.

**Detection signals**:

- ≥80% of verifications return BROKEN over multiple rounds
- BROKEN verdicts don't reproduce: the same kind of attack later doesn't reproduce
- Critic's `confidence` ratings are consistently 4-5 even on attacks that yielded UNCLEAR

**Why it's dangerous**: the deliberation produces a lot of "concerns" but none lead to actionable changes. Decisions either ignore the BROKENs (which then accumulate as drag on every future discussion) or change in arbitrary directions to placate the adversary.

**Response**:

1. Add Critic safety valve enforcement: when an attack finds no real weakness, REQUIRE explicit ROBUST verdict with evidence (no pro-forma BROKEN)
2. Audit recent BROKENs: pick 5 random ones; for each, ask "did this lead to a decision change?" If <2 of 5 led to changes, Critic is performing
3. In severe cases, swap the Critic for a fresh Critic instance with a different specialty

---

## FM-3: Drift (Silent Goal-Departure)

**What it is**: The deliberation slowly wanders from its original anchoring. No single round drifts noticeably, but over 5-10 rounds the topic shifts from the original question to something adjacent and easier.

**Detection signals**:

- Drift check (every K rounds, typically K=5) returns FAIL
- Topic of late rounds doesn't reference the original product anchor or design goal
- Decisions in late rounds don't cite decisions from early rounds

**Why it's dangerous**: by the time drift is detected, the deliberation has spent rounds on the wrong question. Conclusions are valid for the drifted topic, useless for the original.

**Response**:

1. Pause the deliberation; surface the original anchor to all agents
2. Re-frame the next round around the anchor's load-bearing question
3. If drift was structural (e.g., "the original question was actually two questions and we drifted to the easier one"), explicitly split into sub-deliberations

---

## FM-4: Single-Agent Domination

**What it is**: One agent leads most rounds and shapes most decisions. The "multi-agent" deliberation is effectively single-agent with heckling.

**Detection signals**:

- C1 (contribution balance, Shannon entropy) low — typically below 0.6
- One agent's lead frequency > 50%
- Decisions consistently cite the dominant agent's framing/wording

**Why it's dangerous**: structural diversity is decorative. The conclusions are no more robust than they would be from the dominant agent alone, but the apparent multi-agent process gives false confidence.

**Response**:

1. Force lead rotation in the round budget: assign leads explicitly rather than letting them emerge
2. Stress-test the dominant agent's role (forced absence) — see what the system produces without them
3. If domination persists post-stress-test, audit whether the dominant agent's contributions are actually more substantive (in which case the others are the issue) or whether the dominant agent is taking up airtime (in which case schema enforcement is needed)

---

## FM-5: Claim Inflation (or Claim Starvation)

**What it is**: Either too many or too few claims are being raised. Inflation: every observation becomes a claim, claim-status updates can't keep up. Starvation: agents avoid raising claims because they're untested-on-purpose.

**Detection signals**:

- Inflation: >10 claims/round; pending fraction > 60%
- Starvation: <2 claims/round; some agents (especially Action) raise zero across multiple rounds

**Why it's dangerous**: inflation makes the deliberation appear productive while actually losing track; starvation hides disagreement that should be testable.

**Response**:

For inflation:
- Tighten `testable_as` requirement: claims must specify a **single observable outcome**, not "more research is needed"
- Cap claims per agent per round (e.g., 1-2 max)

For starvation:
- Mandate ≥1 claim per agent per round (with Critic role required ≥1)
- Audit why agents aren't raising claims: typically schema fatigue or incentive mismatch

---

## FM-6: Verification Bypass

**What it is**: Verifications get produced (the file is non-empty) but they're shallow: `evidence_refs` point to section headers, `notes` are paraphrase, no claim status changes occur.

**Detection signals**:

- Average `evidence_refs.length` < 2 across recent verifications
- Verifications with `claim_status_changes: []` (the verification didn't actually move any claim)
- "I reviewed both artifacts" phrasings instead of specific quotes

**Why it's dangerous**: the verifications look complete but are inspection-only. The deliberation has the *form* of cross-validation without the *substance*.

**Response**:

1. Reject verifications with <2 evidence_refs at the validation step (block Phase E completion)
2. Audit the next round's verifications manually — paste 3 random ones and ask "do they actually engage with the artifacts they cite?"
3. If verification bypass is systemic, the cross-validation procedure is too easy to satisfy — tighten the rules

---

## FM-7: Stress Test Avoidance

**What it is**: Stress tests (forced agent absence) are scheduled but the system finds ways to avoid them — e.g., a "wrap-up round" gets inserted instead, or the absent agent's output is silently filled in by another agent.

**Detection signals**:

- Plan called for STRESS-{ROLE} rounds but the round was renamed/repurposed
- A stress round's artifacts include all 4 agent outputs (the absent agent's output got produced anyway)
- `verifications.jsonl` for stress rounds shows 4 entries (when 2-3 expected because some checks are NOT_APPLICABLE)

**Why it's dangerous**: without real stress tests, you can't verify any agent's role is load-bearing. The deliberation could be 4-agent in name and 1-agent in effect.

**Response**:

1. Enforce stress test schedule: if R5 is planned as STRESS-CRITIC, the Critic must NOT produce an artifact in R5
2. The artifacts directory should have exactly 3 files for stress rounds, not 4
3. If the team produces 4 artifacts in a stress round anyway, treat that as a process failure and re-run

---

## FM-8: Round Budget Overrun

**What it is**: The deliberation runs past its planned round count without converging. Each new round adds claims and tensions but the stop signals (see [stopping-criteria.md](stopping-criteria.md)) don't satisfy.

**Detection signals**:

- Past planned round count, ≤3 of 6 stop signals satisfied
- Pending claim fraction not declining
- New tensions raised faster than old ones resolved

**Why it's dangerous**: more rounds without convergence means the question is mis-scoped. Adding rounds increases artifact accumulation without resolution; the deliberation becomes harder to summarize.

**Response**:

1. Stop adding rounds. Run a synthesis round (no new claims, only resolution attempts on pending claims).
2. Diagnose the non-convergence: was the original question too broad? Were the agents miscast? Was a stress test never run?
3. Document the non-convergence as a finding in retrospective. Plan a follow-up deliberation with adjusted scope.

A non-converging deliberation is a finding, not a failure. Documenting why it didn't converge is more valuable than running 5 more rounds and pretending it did.

---

## Cross-failure interactions

Some failure modes amplify each other:

- **FM-1 (sycophancy) + FM-6 (verification bypass)**: agents agree, verifications confirm shallowly, claims don't get refuted. The system looks productive but is hollow.
- **FM-4 (single-agent dom) + FM-3 (drift)**: the dominant agent's interests pull the deliberation toward their topic, drift goes undetected because the dominant agent doesn't drift-check themselves.
- **FM-2 (all-BROKEN) + FM-5 (claim inflation)**: every observation becomes a BROKEN claim, the system drowns in adversarial work without grounding.

When you detect one failure mode, audit for the others — they often travel together.

---

## Use during retrospectives

After the deliberation completes, run through the FM catalog:

1. For each failure mode, did detection signals fire at any point?
2. If yes, was it caught in time? What was the response?
3. If the response worked, document it for the next deliberation
4. If the response didn't work, the catalog needs updating for your domain

The catalog improves with each deliberation. Treat it as a living document, not a fixed checklist.
