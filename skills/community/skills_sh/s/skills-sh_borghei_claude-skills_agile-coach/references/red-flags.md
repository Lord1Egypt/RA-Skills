# Red Flags: Agile Coach

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just produced a maturity assessment, framework recommendation, transformation roadmap, or retrospective design, scan the red flags below before sharing. Each one names a specific failure mode and shows the *bad* version next to the *good* version. If anything in your artifact rhymes with a bad example, fix it before the artifact leaves your hands.

---

## Red Flag 1: Process Worship (ceremony over outcomes)

**Symptom.** The recommendation lists ceremonies, roles, and artifacts in detail but never connects them to a business or delivery outcome.

**Why it's bad.** Process worship is how organizations end up doing daily standups religiously while shipping nothing. The 5-level maturity model exists to measure *outcomes* (predictability, business alignment, learning), not ceremony attendance. Recommending Scrum because "the team should do Scrum" without a problem statement produces resentment and theater.

**Bad example:**
> "Team should adopt Scrum: daily standups at 9:30, sprint planning every other Monday, retrospectives every other Friday, story-point estimation, definition of done, sprint reviews."

**Good example:**
> "Problem: Team commits ~30 points/sprint but delivers ~17 (57% predictability). Recommendation: Adopt Scrum with a 2-week cadence, but the leading indicator we will track is *forecast hit rate*, not ceremony attendance. Target: 80% predictability by sprint 6."

**How to catch it.** For every ceremony you prescribe, ask: "what outcome does this improve, and how will we measure it?" If you cannot answer, do not prescribe it.

---

## Red Flag 2: ScrumBut ("we do Scrum, but...")

**Symptom.** The team adopts Scrum vocabulary but quietly removes the parts that hurt — no retrospective, no definition of done, the PO is part-time, sprints get extended when work is unfinished.

**Why it's bad.** ScrumBut keeps the cost (ceremonies, jargon, planning overhead) while removing the learning loops that justify it. The result is worse than not doing Scrum at all, because the team believes they have already tried it and "it didn't work."

**Bad example:**
> "We do Scrum, but we skip retros when sprints are busy. We do Scrum, but the PO is also the engineering manager. We do Scrum, but we extend the sprint by a few days when stories aren't done."

**Good example:**
> "We are doing Scrum with these named deviations: (1) no PO yet — EM is acting PO until Q3, (2) retros are non-negotiable, (3) unfinished work returns to backlog and is re-estimated. Each deviation has an owner and a target end date."

**How to catch it.** Make every deviation from the framework *named, owned, and time-boxed*. Anonymous ScrumBut becomes the new normal.

---

## Red Flag 3: Wrong Framework for Team Size and Complexity

**Symptom.** Recommending SAFe to a 12-person startup, or pure Kanban to a 60-engineer organization with five interdependent teams.

**Why it's bad.** Framework selection is the single highest-leverage decision in agile coaching. The size/complexity matrix in the SKILL.md exists because a framework optimized for a small simple context ships pure overhead in a large complex one, and vice versa.

**Bad example:**
> "Recommendation: SAFe 6.0 with ARTs and PI Planning." (Team: 8 engineers, 1 PM, 1 designer, single product line, single backlog.)

**Good example:**
> "Recommendation: Kanban with WIP limits of 2 per engineer, weekly cadence cycle, daily standup. Defer Scrum until team grows past 12 people or until predictability becomes a stakeholder concern."

**How to catch it.** Plot the team on the simple/complex x small/large matrix from the SKILL.md *before* recommending a framework. Justify every step away from the matrix default.

---

## Red Flag 4: Velocity as a Performance Metric

**Symptom.** Maturity report celebrates "team velocity increased from 30 to 45 points" as if that were a success metric.

**Why it's bad.** Velocity is a planning input, not a performance output. Teams that are measured on velocity inflate estimates within a single sprint. The right output metrics are *predictability* (forecast hit rate), *cycle time*, *deployment frequency*, and *change failure rate* — the DORA metrics — none of which can be inflated by re-pointing.

**Bad example:**
> "Q2 results: velocity up 50% (30 -> 45 story points). Team is performing exceptionally."

**Good example:**
> "Q2 results: cycle time down from 9 to 5 days (p50), deployment frequency 2x/week up from 1x/2-weeks, predictability 82% (target 80%). Velocity was stable at ~30 points; the improvement came from smaller stories and fewer rollbacks."

**How to catch it.** If velocity appears in a report to leadership without DORA or predictability alongside it, rewrite.

---

## Red Flag 5: Tuckman Stage Misdiagnosis

**Symptom.** Coaching stance is wrong for the team's actual development stage — directing a Performing team or coaching a Forming team that just needs role clarity.

**Why it's bad.** The four-stages model (Forming, Storming, Norming, Performing) is in the skill because intervention style must match stage. Coaching open-ended questions to a Forming team produces paralysis; directing a Performing team produces resentment and attrition.

**Bad example:**
> "Team is in conflict (Storming). Recommendation: Schedule open-ended retrospectives and ask 'what does great look like for us?' to surface the team's vision."

**Good example:**
> "Team is in Storming. Recommendation: Coach (not direct). Run a *working agreement* session to make implicit conflicts explicit. Use 1:1s to surface specific interpersonal frictions. Defer vision work until Norming."

**How to catch it.** Name the stage explicitly. Reference the stage-to-stance mapping (Directing/Coaching/Supporting/Delegating). If your intervention does not match the mapping, revise.

---

## Red Flag 6: Maturity Score Inflation

**Symptom.** Self-assessment puts the team at Level 4 across all six dimensions when, by evidence, they are at Level 2.

**Why it's bad.** A maturity score that flatters the team is worthless: it produces no improvement actions and gives leadership false confidence. The validation checkpoint in the SKILL.md exists to require *evidence* for every score.

**Bad example:**
> "Technical Excellence: 4/5. The team values quality and has good engineers."

**Good example:**
> "Technical Excellence: 2/5. Evidence: no CI on main branch (1/5 indicator), partial unit test coverage (~40%), no production monitoring beyond uptime, two of last three releases required hotfixes within 24 hours. Target Level 3 in two quarters."

**How to catch it.** Require a one-sentence evidence statement for every dimension score. No evidence, no score.

---

## Red Flag 7: Transformation Roadmap with No Sequencing Logic

**Symptom.** The roadmap is a bullet list of practices to adopt with no rationale for order — "Q1: Scrum, OKRs, CI/CD, Lean Portfolio, SAFe."

**Why it's bad.** Practices have prerequisites. CI/CD without trunk-based development creates merge hell. SAFe without team-level Scrum produces planning theater. Sequencing failure is the most common reason transformations stall.

**Bad example:**
> "Q1: Adopt Scrum, OKRs, DevOps, and product trios."

**Good example:**
> "Q1: Stabilize team-level Scrum (predictability gate: 70%). Q2: Introduce product trios and CD pipeline (prereq: Q1 predictability). Q3: Roll up to org-level OKRs (prereq: stable team backlogs). Each quarter has a gate; if the gate is missed, the next quarter slips."

**How to catch it.** For every practice in the roadmap, name its prerequisite and its gate. If practices can be reordered without consequence, the sequencing is fake.

---

## Red Flag 8: Retrospective as Complaint Session

**Symptom.** Retro output is a list of grievances with no owned actions, or the same three actions appear retro after retro with no closure.

**Why it's bad.** The retrospective is the team's main learning loop. If it produces no committed actions or no follow-through, it converts into theater and the team stops believing in it. Continuous Improvement (the sixth maturity dimension) flatlines.

**Bad example:**
> "What went wrong: too many meetings, unclear requirements, ops keeps interrupting us. Actions: 'reduce meetings', 'better requirements'."

**Good example:**
> "Action 1: PM and EM block 9-11am as deep-work no-meeting window starting next sprint. Owner: EM. Done when: calendar reflects it by Friday. Action 2: PRD must include 'definition of done' before story is pulled. Owner: PM. Done when: next 3 PRDs reviewed. Carryover from last retro: 'requirements clarity' — closed; replaced by Action 2."

**How to catch it.** Every retro action must have an owner, a date, and a "done when" condition. Track carryovers explicitly; if an action appears in three retros, escalate or kill it.

---

## Red Flag 9: Coach as Decision-Maker

**Symptom.** The coach is making product, technical, or staffing decisions on behalf of the team — "I decided we will move to Kanban" rather than "I helped the team decide."

**Why it's bad.** Agile coaching is a facilitative discipline. A coach who makes decisions creates dependency and undermines the team's ownership. The team will revert the moment the coach leaves.

**Bad example:**
> "I have decided that this team will adopt Scrum and that the EM will be the new Scrum Master."

**Good example:**
> "I facilitated a 90-minute working session where the team reviewed the framework selection matrix and chose Scrum 8-1. The EM volunteered as Scrum Master with a 6-month sunset to a rotating role."

**How to catch it.** Read your recommendation document. Search for "I decided" or "I will". If the team is not the subject of those sentences, rewrite.

---

## Red Flag 10: Ignoring the Andon Cord (Stop-the-Line Discipline)

**Symptom.** Recommendations include continuous improvement language but never empower the team to *halt* work when quality is broken.

**Why it's bad.** Maturity Level 4 and above (Managed, Optimizing) requires stop-the-line discipline — the team's right and obligation to halt progress when a quality issue surfaces. Continuous improvement without stop-the-line is just slogans.

**Bad example:**
> "Recommend the team adopt continuous improvement practices and discuss quality issues in retro."

**Good example:**
> "Recommend an explicit andon policy: any engineer can halt the deployment pipeline by tagging #andon in the team channel. Halt is automatic; restart requires team agreement and a 15-minute root cause. Track andon-pulls per quarter as a leading indicator of psychological safety."

**How to catch it.** A continuous improvement system must have a named mechanism for *stopping*, not just for *talking about* quality.

---

## Red Flag 11: Framework Selection without Looking at the Work

**Symptom.** The framework recommendation is based on team size and self-described complexity, but never on the actual *type of work* (predictable feature delivery vs unpredictable incident response vs research).

**Why it's bad.** Kanban beats Scrum for support/ops work; Scrum beats Kanban for feature delivery with a quarterly horizon; XP overlays on either when engineering practices are the bottleneck. Skipping a look at the work mix produces framework mismatches.

**Bad example:**
> "Team is 8 people with moderate complexity. Recommend Scrum."

**Good example:**
> "Team is 8 people. Work mix: 60% planned feature work, 30% interrupt-driven support, 10% R&D. Recommendation: Scrum for the feature track (separate backlog, 2-week sprints) and a Kanban swim lane for support (WIP limit 2). R&D handled as time-boxed spikes during sprint planning."

**How to catch it.** Estimate the work mix (% planned vs interrupt vs research) before recommending. Mixed-mode work usually wants mixed-mode frameworks.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Process Worship | Does every ceremony map to a measurable outcome? |
| 2 | ScrumBut | Are deviations named, owned, and time-boxed? |
| 3 | Wrong Framework for Size/Complexity | Did you justify departures from the size/complexity matrix? |
| 4 | Velocity as Performance Metric | Are DORA + predictability alongside any velocity number? |
| 5 | Tuckman Stage Misdiagnosis | Does your stance match the named stage? |
| 6 | Maturity Score Inflation | Is there a one-sentence evidence statement per dimension? |
| 7 | Roadmap with No Sequencing | Does every Q have a prereq and a gate? |
| 8 | Retro as Complaint Session | Does every action have owner + date + done-when? |
| 9 | Coach as Decision-Maker | Is the team the subject of decision sentences? |
| 10 | No Andon Cord | Is there a named mechanism for stopping work? |
| 11 | Framework without Work Mix | Did you estimate planned vs interrupt vs research? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/maturity-model.md (for the 5-level scoring rubric, if present)
- references/retrospective-formats.md (for retro variety beyond start-stop-continue, if present)
