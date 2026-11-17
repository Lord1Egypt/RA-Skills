# Bugs, Tickets, and Alerts — Severity Is Not Priority

The most expensive conflation in issue triage: severity describes how bad it is when it happens; priority describes when you work on it. They correlate weakly. A crash in a feature nobody uses is high severity, P3. A wrong number on the pricing page is trivially fixed, low severity — and P0-adjacent, because every minute it stands, customers see a false price.

## Priority = Severity × Reach × Trend

Run all three; any single dimension alone misorders the queue.

**Severity ladder** (worst first): data loss or corruption > security exposure > blocked/crash with no workaround > degraded but usable > cosmetic. Data loss auto-runs the P0 test — damage accumulates every minute (SKILL.md, Priority Levels).

**Reach**: how many users or paths hit it. Duplicate reports are measured reach — link them to one canonical issue and let the count raise its priority (batch.md applies the same rule to requests). One report from one user of an edge path is not the same bug-priority as ten reports in a day, at identical severity.

**Trend**: growing beats static. And a **regression from the latest release outranks an equal-severity old bug** three times over: the cause is fresh (diff the release, cheapest moment to find it), more users hit it as the release rolls out, and "it worked yesterday" burns trust faster than "it never worked".

**Workaround modifier**: a documented, reachable workaround drops priority one level — not to zero, because the workaround charges every affected user a toll on every occurrence. No workaround + blocked = the P1 stall test is already answered.

## No Repro

An unreproducible report is not a fix task — it is a gather-info task, triaged by the claim's stakes: a customer claiming they are blocked right now makes the INVESTIGATION P1; "sometimes it flickers" makes it P3 with a request for steps. Never queue a fix you cannot verify fixed; never close a report solely because you could not reproduce it once.

## Security Reports

- Floor: P1-until-assessed, regardless of the reporter's tone or the report's polish — the cost asymmetry (SKILL.md, Core Rules #3) is at its steepest here.
- Assessed exploitable + exposed surface → P0: exploitation damage accumulates whether or not you are watching.
- The reporter's own severity claim is a feeling-word until verified (signals.md) — verify against the ladder above, not against their subject line.

## SLA Queues

An SLA is a deadline generator: each ticket's SLA clock converts to a due time, and the slack machinery takes over (deadlines.md). Sort breach-imminent tickets by ascending slack, not by arrival or by customer volume of complaint. An SLA breached in 10 minutes outranks a louder ticket breaching tomorrow.

## Alerts

- A repeated identical alert adds no information — recalibrate, don't re-page (signals.md, Source Defaults).
- A flapping or noisy alert is itself a P2 task: "fix this alert" enters the queue, because every false page erodes the P0-until-disproven default that paging depends on.
- A page you cannot map to user-visible damage within a few minutes of looking: downgrade, log it, and add it to the fix-this-alert list. Pages exist to mark accumulating damage; one that can't name its damage is noise wearing a siren.

## Communicating the Verdict

- Never argue severity with the reporter — acknowledge the impact they felt, state the assigned priority and the reason in one line: "Real, affects the export path only — queued P2, scheduled Thursday."
- The user overriding your ticket priority is training data: record it, ladder it (patterns.md).
- Boundary: this file decides WHEN a bug gets worked and whether it interrupts; running an actual incident (roles, comms, postmortem) is `incident-response` (SKILL.md, Related Skills).
