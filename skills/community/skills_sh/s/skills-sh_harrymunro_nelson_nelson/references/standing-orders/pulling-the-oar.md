# Standing Order: Pulling the Oar

A senior agent (admiral or captain) MUST NOT absorb a failed subordinate's work into its own context. When a dispatched subagent fails, the senior fixes the brief and re-dispatches.

**Trigger:** A dispatched subagent (Explore, captain, marine, crew) returns an error, hits a prompt-length limit, returns insufficient or malformed output, or times out.

**Anti-pattern:** The senior agent absorbs the subagent's intended work into its own context — reads the files the Explore was meant to summarise, runs the tests the marine was meant to run, builds the artifact the captain was meant to deliver. The senior's context fills with raw inputs that should have been pre-digested.

**Symptoms of a violation:**
- Senior reasons over raw file contents that a subagent could have summarised.
- Senior says some variant of "I'll just do this directly — faster."
- Context consumption spikes immediately after a subagent failure.
- The same dispatch is not re-attempted with a fixed brief.

**Remedy — fix the brief, don't take the oar:**
1. Stop. Do not absorb the work.
2. Diagnose the failure: brief too broad, prompt too long, output format ambiguous, wrong agent type, tool unavailable.
3. Re-brief — split into multiple focused subagents, tighten scope, or change agent type. For Explore failures, prefer several narrow Explores over one laundry-list dispatch; require structured summaries, not raw file contents.
4. Re-dispatch.
5. After two failed re-briefs on the same task, escalate to the user — do not absorb on the third attempt.

**Not a violation:** Read-only recombination of subagent results already in context (covered by `admiral-at-the-helm.md`).

**Related orders:** `admiral-at-the-helm.md` (admiral does implementation), `captain-at-the-capstan.md` (captain does crew work).
