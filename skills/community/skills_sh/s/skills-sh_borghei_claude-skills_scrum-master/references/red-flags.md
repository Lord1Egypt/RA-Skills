# Red Flags: Scrum Master

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every sprint planning output, velocity report, retrospective summary, and team-health dashboard before sharing. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Velocity-as-Target

**Symptom.** "Our velocity must hit 38 SP every sprint." Team is rewarded / punished against the number.
**Why it's bad.** Velocity is a *capacity* signal, not a productivity target. When you target it, Goodhart's Law applies: engineers inflate story points (each story silently grows from 3 to 5), and the number rises while throughput is unchanged. Then the team commits to more than it can deliver, slips, and the trust collapses.
**Bad example:**
> "Engineering manager OKR: 'Increase team velocity from 32 to 40 SP/sprint by Q3.' Bonuses tied to delivery vs that target."
**Good example:**
> "Velocity is used only as a planning input: 'last 4 sprints averaged 28-34 SP with 80% confidence; therefore commit ~28 SP this sprint.' Performance is measured by outcomes (OKRs, customer metrics), not velocity. Documented in the team charter."
**How to catch it.** Any management OKR or bonus tied to velocity = remove. See `jira-expert/references/red-flags.md` Red Flag 6.

---

## Red Flag 2: Retro Action-Item Rot

**Symptom.** Every retro produces 4-6 action items. Next retro: 80% of last sprint's items are not done, and the team re-discusses the same problems.
**Why it's bad.** Action items that do not get executed teach the team that retros do not matter. Participation drops; the retro becomes a ritual. The original problems recur sprint after sprint.
**Bad example:**
> "Retro 5: 4 action items. Retro 6 (next sprint): 3 of 4 still open; 2 re-added as 'this time we mean it'."
**Good example:**
> "Retro process: max 2 action items per retro, each with explicit Owner + Due Date (within sprint). Sprint Review includes 1-min review of retro action-item progress. Items that slip get a root-cause analysis, not a re-add."
**How to catch it.** Same problem appears in > 2 consecutive retros = root-cause it instead of re-adding.

---

## Red Flag 3: Daily Standup as Status Report to the Manager

**Symptom.** Standup format: each person reports yesterday/today/blockers, addressed to the engineering manager who silently takes notes.
**Why it's bad.** Standup is a *coordination* meeting, not a status meeting. Reporting to the manager makes it political; engineers censor blockers and the meeting becomes performative. The team loses its coordination signal.
**Bad example:**
> "Standup: 15 engineers go around the room, each says 3 lines to the manager. Manager interrupts twice with follow-up questions. Total time: 28 min."
**Good example:**
> "Standup is 'walk the board' format: focus on tickets in progress, not on people. Discuss what is blocked, what is at risk of slipping, what needs help. Manager attends optionally; team leads coordination. < 12 min."
**How to catch it.** Standup format 'go around the room' + > 15 min = restructure to walk-the-board.

---

## Red Flag 4: Sprint Goal Missing or Generic

**Symptom.** Sprint goal: "Complete the sprint backlog." (Or absent entirely.)
**Why it's bad.** Sprint goal is the team's commitment to a coherent outcome. Without it, the sprint becomes a basket of unrelated tickets with no narrative. The team cannot trade off in-sprint scope coherently, and the sprint review has no story to tell.
**Bad example:**
> "Sprint 23 goal: 'Finish all 14 tickets.'"
**Good example:**
> "Sprint 23 goal: 'A new user can sign up, complete onboarding, and see their first useful dashboard in < 5 min, on staging. Other work (refactors, bug fixes) is in scope only if it does not block this goal.'"
**How to catch it.** Sprint goal mentions ticket count, not customer-visible outcome = rewrite.

---

## Red Flag 5: Capacity Ignores PTO / On-Call / Interviews

**Symptom.** "Team has 8 engineers x 2 weeks = 16 person-weeks capacity." Ignoring PTO (1), on-call (2), interview load (1).
**Why it's bad.** Over-estimating capacity means over-committing, which means slipping, which destroys trust. The team chronically misses sprint commitments; planning becomes meaningless.
**Bad example:**
> "Capacity: 8 engineers x 10 working days = 80 IC-days. Committed: 80 IC-days of work."
**Good example:**
> "Capacity model:
> - 8 engineers x 10 working days = 80 IC-days gross.
> - Subtract: PTO (4 days), on-call rotation (6 days), interview load (3 days), required maintenance (8 days) = 21 days.
> - Net: 59 IC-days.
> - Commit at 80% confidence: ~47 IC-days = ~22 SP at calibrated 2.1 IC-days / SP."
**How to catch it.** Capacity calc does not subtract PTO / on-call / interviews = redo.

---

## Red Flag 6: Definition of Done Drift

**Symptom.** Team's DoD says "tested + reviewed + deployed". In reality, half the sprints close with tickets marked Done but no tests, or with deploys pending.
**Why it's bad.** When DoD drifts, "Done" stops meaning anything. Bugs leak to production; reviewers find regressions weeks later; rework destroys velocity. The honest velocity is much lower than reported.
**Bad example:**
> "DoD: tested, reviewed, deployed. Actual: 60% of closed tickets have no tests; 40% have not deployed."
**Good example:**
> "DoD is enforced by automation: tickets cannot move to Done unless (1) PR is merged, (2) CI passed including the test runner, (3) the deployment status check is green. Manual checks: code-review approval, design review where relevant. Drift surfaces in sprint review."
**How to catch it.** Sample 10 closed tickets from last sprint; check each against DoD. > 20% gap = enforce via automation.

---

## Red Flag 7: Estimation by the Loudest Voice

**Symptom.** Story points are set by whoever speaks first in planning poker, not by the median of the group.
**Why it's bad.** Loudest-voice estimation drifts toward optimism (the optimist speaks first) or pessimism (the senior engineer speaks first). The team's collective wisdom is lost; estimates become unreliable.
**Bad example:**
> "Planning poker: 'I think this is a 3.' Team: 'OK, 3.' (No reveal; no discussion of divergent estimates.)"
**Good example:**
> "Planning poker with simultaneous reveal: cards down, all reveal together. If estimates diverge by > 2 points, low + high voices each explain reasoning; re-vote. Final = median (not average; outliers ignored)."
**How to catch it.** Watch a planning poker session. If estimates converge without reveal-then-discuss, restructure.

---

## Red Flag 8: Retro Without Data

**Symptom.** Retro is "how did people feel this sprint?". No metrics on cycle time, throughput, escaped bugs, sprint goal completion.
**Why it's bad.** Feelings-only retros surface the loudest concerns but miss systematic patterns (cycle-time creeping up, escaped-bug rate doubling, planning accuracy declining). The team treats anecdotes as systemic.
**Bad example:**
> "Retro: 'I felt overwhelmed.' 'I felt the work was fragmented.' 'I felt good.' Action: 'try to focus more.'"
**Good example:**
> "Retro starts with a 5-minute data review: sprint goal completion, throughput, cycle time, escaped-bug count, capacity vs committed vs done. Discussion grounded in patterns. Action items address what the data shows, not just what was felt."
**How to catch it.** Retro has no data slide = use `retrospective_analyzer.py` to generate one.

---

## Red Flag 9: Scrum Master Owns the Backlog

**Symptom.** Scrum master grooms the backlog, prioritizes items, writes acceptance criteria.
**Why it's bad.** Scrum master is a *facilitator*, not the product owner. Owning the backlog blurs roles and short-circuits the PM. The team trains around the SM's preferences, not the customer's needs.
**Bad example:**
> "Scrum master ranks the backlog in collaboration with engineering. PM is not involved in refinement."
**Good example:**
> "Scrum master facilitates the refinement ritual but does not own ranking. PM (or PO) owns: priority order, acceptance criteria, the WHY in WWAS. Engineering owns: technical approach, estimation, the HOW. Scrum master owns: the process working smoothly."
**How to catch it.** PM is absent from refinement = restore role boundary.

---

## Red Flag 10: Sprint Review Without the Customer Outcome

**Symptom.** Sprint review = demo of what shipped. Audience: engineering manager. No discussion of whether the sprint goal was met, no customer / stakeholder present.
**Why it's bad.** Sprint review is meant to inspect the increment with stakeholders -- to validate that what shipped achieves the outcome. A demo without outcome discussion is a show-and-tell with no learning loop.
**Bad example:**
> "Sprint review: 30 min of demos. Engineering manager nods. No discussion of sprint goal."
**Good example:**
> "Sprint review structure: (1) restate sprint goal; (2) demo against the goal; (3) discuss whether the goal was met (with the metric, where measurable); (4) stakeholder Q&A; (5) implications for next sprint. Audience includes PM, design, and ideally a customer-success rep."
**How to catch it.** Sprint review attendance = engineering only = invite stakeholders + restructure.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Velocity-as-target | Any OKR / bonus tied to velocity? |
| 2 | Retro action-item rot | Same problem in > 2 retros = root-cause |
| 3 | Standup as status to manager | Walk-the-board format used? |
| 4 | Generic sprint goal | Goal mentions customer outcome, not tickets |
| 5 | Capacity ignores PTO / on-call | Capacity calc explicit |
| 6 | DoD drift | 10-ticket sample passes all DoD checks |
| 7 | Loudest-voice estimation | Simultaneous reveal in planning poker |
| 8 | Retro without data | Data slide opens every retro |
| 9 | SM owns the backlog | PM owns priority + WHY |
| 10 | Review without outcome | Sprint goal restated at review |

## Related Reading

- `SKILL.md` -- scrum master role + analytics
- `scripts/sprint_capacity_calculator.py --help` -- capacity model
- `scripts/velocity_analyzer.py --help` -- velocity as a planning signal
- `scripts/sprint_health_scorer.py --help` -- 6-dimension sprint health
- `scripts/retrospective_analyzer.py --help` -- data-driven retro
- Sibling skill: `sprint-retrospective/` -- the retro skill itself
- Sibling skill: `agile-coach/` -- broader agile-transformation patterns
- Sibling skill: `jira-expert/` -- the tooling for tracking
