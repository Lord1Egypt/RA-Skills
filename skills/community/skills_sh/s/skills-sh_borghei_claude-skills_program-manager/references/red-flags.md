# Red Flags: Program Manager

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every program-level artifact (dependency map, RAID log, steering committee deck, cross-team status report) before publishing. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Dependency Theater

**Symptom.** Dependency map shows 47 dependencies; in the weekly sync, the PgM reads them aloud; no decisions are made.
**Why it's bad.** A dependency map is a coordination *tool*, not a status report. Reading dependencies aloud without driving decisions (re-sequence, descope, escalate) makes the meeting feel productive but changes nothing. The dependencies still slip the program.
**Bad example:**
> "Weekly sync minutes: 'Reviewed all 47 dependencies. Team A waiting on Team B; Team C waiting on Team A.' (45-min meeting; no action items.)"
**Good example:**
> "Weekly sync structure: (1) what changed in dependencies since last week (5 min); (2) which 2-3 dependencies are critical-path this week (10 min); (3) decisions / escalations needed (15 min). Output: an updated dependency map + a decision log. No dependency is read aloud unless it triggers an action."
**How to catch it.** Sync meeting > 30 min with no decisions in the log = dependency theater.

---

## Red Flag 2: RAID Log Nobody Reads

**Symptom.** RAID log (Risks / Assumptions / Issues / Dependencies) has 240 entries. The last update was 3 weeks ago. Steering committee skips the RAID section.
**Why it's bad.** A stale, oversized RAID log is worse than no RAID log. It signals risk hygiene exists but is broken, so people stop looking. Real risks are buried under noise.
**Bad example:**
> "RAID log: 240 entries. Most are 'open' indefinitely. No owner column. Steering committee skips."
**Good example:**
> "RAID log capped at ~25 active entries (closed items archived monthly). Each entry has: Owner, Status, Mitigation, Tripwire, Next Review Date. Weekly review with the program team rotates ~5 entries; quarterly review with steering committee surfaces top-5 risks only."
**How to catch it.** RAID > 30 active entries or last review > 2 weeks ago = restructure.

---

## Red Flag 3: Status Reporting Up Without Decisions

**Symptom.** Steering committee deck is 40 slides of status; ends with "any questions?"; no decisions asked of leadership.
**Why it's bad.** A steering committee exists to make decisions. Status-only meetings waste leadership time and the PgM loses the chance to unblock the program. Decisions slip because they were never explicitly surfaced.
**Bad example:**
> "Steering committee deck: 40 slides on team status. Final slide: 'Questions?' No 'asks' section. No decisions made."
**Good example:**
> "Steering committee deck: 8 slides max. Structure: (1) headline R/Y/G; (2) what changed since last meeting; (3) 3 explicit asks for the committee (e.g. 'approve $80k vendor switch', 'decide between scope option A or B', 'allocate engineer from Team C to Program X'); (4) appendix with detail. Meeting closes with decisions, not questions."
**How to catch it.** Steering deck > 15 slides or no Asks section = restructure.

---

## Red Flag 4: Cross-Team Dependencies Discovered Mid-Program

**Symptom.** Week 12 of a 16-week program: Team A discovers Team B was supposed to deliver an API that Team B never planned.
**Why it's bad.** Mid-program dependency discovery is the leading cause of program failure. By week 12 there is no slack to absorb the shock, and one team's slip cascades into 2-3 others. The program slips by months.
**Bad example:**
> "Week 12: Team A blocked. Team B: 'We never knew we owed you that API.' Estimated 4 weeks to deliver. Program slips 4 weeks."
**Good example:**
> "Week 0: dependency reconciliation workshop with all program teams. Every dependency captured in `dependency-graph.json` with owner + due date. Weeks 1, 4, 8: dependency check-ins specifically. Discovered dependency added with retrospective lesson logged."
**How to catch it.** Mid-program dependency surprise = run a week-0 reconciliation next time; see `execution/dependency-map`.

---

## Red Flag 5: Critical-Path Tracking Lost After Kickoff

**Symptom.** Kickoff identified the critical path; week 8 nobody knows what is on it.
**Why it's bad.** The critical path is the only sequence whose slip directly slips the program. Losing track of it means the PgM cannot prioritize attention. Non-critical items get equal worry; the critical items quietly slip.
**Bad example:**
> "Kickoff: critical path = task A -> task C -> task F. Week 8: PgM tracks 'all 22 tasks equally'. Task C slipped 1 week unnoticed."
**Good example:**
> "Critical path recomputed weekly using `dependency_graph.py --critical-path`. Weekly status flags 'critical-path items at risk' first. Items off the critical path get less attention; items on it get daily check-ins if at risk."
**How to catch it.** No critical-path computation in the last 2 weeks = re-run.

---

## Red Flag 6: Risk Tripwires Missing

**Symptom.** Every risk in the RAID log has a description but no tripwire (the specific signal that means "we are now in trouble").
**Why it's bad.** Without tripwires, risks fire silently. By the time the PgM realizes risk R has materialized, mitigation is more expensive. Tripwires are the early-warning system; without them, the program is reactive only.
**Bad example:**
> "Risk: 'Vendor delivery may slip.' Mitigation: 'Stay in touch with vendor.' (No tripwire.)"
**Good example:**
> "Risk: 'Vendor delivery may slip.' Tripwire: 'Vendor weekly status shows red OR Vendor misses a milestone OR Vendor's primary engineer changes.' Mitigation: 'If tripwire fires, switch to Plan B (in-house build with descoped functionality).' Owner: <name>. Review weekly."
**How to catch it.** Any risk without a tripwire column = add or move to issue.

---

## Red Flag 7: Program Charter Was Never Written

**Symptom.** The program has been running for 6 months; no document defines its scope, success criteria, sponsor, or constraints.
**Why it's bad.** Without a charter, the program drifts. New requests get accepted because there is no documented basis for refusal. Success at close is contested ("did we achieve the goal?") because the goal was never written down.
**Bad example:**
> "Program 'Enterprise Readiness' has been running since November. No charter. Scope reinterpreted in every steering meeting."
**Good example:**
> "Program Charter (1-2 pages) covers: (1) goal + success metrics; (2) scope -- what is and is not in; (3) sponsor + steering committee; (4) participating teams; (5) budget + timeline; (6) decision rights (DACI); (7) explicit out-of-scope list. Signed by sponsor at kickoff."
**How to catch it.** Program > 4 weeks old without a written charter = pause and write.

---

## Red Flag 8: Single PgM as Bottleneck for All Cross-Team Decisions

**Symptom.** Every decision flows through the PgM; teams cannot move forward until the PgM is available.
**Why it's bad.** A bottlenecked PgM is a slow program. Worse, the PgM cannot scale to the level of detail teams need, so decisions slip in quality. The right model is decentralized decisions with a coordinating PgM.
**Bad example:**
> "All cross-team decisions: 'Wait for next PgM sync.' Teams idle 3-5 days waiting."
**Good example:**
> "Decision rights documented per area (DACI matrix in the charter). Most decisions are made by the responsible team lead, with the PgM informed. PgM-driven decisions are reserved for cross-team trade-offs (scope swaps, resource reallocations). Async-by-default; sync only for genuine forks."
**How to catch it.** Team-lead-level decisions queued behind PgM = re-clarify DACI.

---

## Red Flag 9: Cross-Team Communication Sent Once

**Symptom.** Major decision communicated in one Slack channel at one moment; the program assumes everyone read it.
**Why it's bad.** Cross-team communications need multiple channels, multiple times, with confirmation. Single-broadcast decisions get missed by the team that was in a deep-work block. Two weeks later, a team is acting on the old assumption.
**Bad example:**
> "Decision: switch vendor. Sent once in #program-channel. Three teams missed it; one team built against the old vendor's API for 2 weeks."
**Good example:**
> "Decision communication policy: (1) Slack #program-decisions thread with the decision; (2) email summary to team leads; (3) update the program charter / decision log; (4) confirmation read-receipts from each team lead. Decisions affecting > 2 teams get a brief sync to ensure shared interpretation."
**How to catch it.** Major decision communicated only once = communicate twice with confirmation.

---

## Red Flag 10: Program Close Without a Retro

**Symptom.** Program ships; team disbands; no retro is scheduled.
**Why it's bad.** A program is the org's biggest learning opportunity. Skipping the retro means the same dependency snags, the same RAID failures, the same scope creep recur in the next program.
**Bad example:**
> "Program shipped 2 weeks ago. Team disbanded. No retro held."
**Good example:**
> "Program retro held within 3 weeks of close, with all team leads. Three artifacts: (1) what worked; (2) what failed (with root causes, not blame); (3) 3-5 concrete changes for the next program. Outputs feed the program-management playbook. PgM publishes within 1 week of the retro."
**How to catch it.** Program closed without a scheduled retro = schedule it now.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Dependency theater | Sync meeting produces decisions, not readouts |
| 2 | RAID log nobody reads | < 30 active entries, weekly review |
| 3 | Status without decisions | Steering deck has explicit Asks |
| 4 | Mid-program dependency surprises | Week-0 reconciliation workshop |
| 5 | Critical path lost | Recomputed weekly |
| 6 | Risks without tripwires | Every risk has a tripwire column |
| 7 | No program charter | Charter signed at kickoff |
| 8 | PgM as decision bottleneck | DACI clarifies decision rights |
| 9 | Single-broadcast comms | Multi-channel with read confirmation |
| 10 | No close retro | Retro within 3 weeks of close |

## Related Reading

- `SKILL.md` -- program management framework
- `references/charter-template.md` -- the charter document
- `references/raid-template.md` -- the RAID log structure
- Sibling skill: `execution/dependency-map/` -- the dependency graph tool
- Sibling skill: `execution/daci-framework/` -- decision rights matrix
- Sibling skill: `execution/status-update-generator/` -- program-level status reporting
- Sibling skill: `senior-pm/` -- stakeholder mapping for the steering committee
- Sibling skill: `delivery-manager/` -- release coordination within the program
