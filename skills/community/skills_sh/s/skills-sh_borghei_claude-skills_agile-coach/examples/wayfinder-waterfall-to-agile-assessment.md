# Example: Wayfinder Analytics — Maturity Assessment for a Series-B Waterfall-to-Agile Transition

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Wayfinder Analytics is a Series-B B2B analytics platform (180 employees, ~$22M ARR) that grew up on waterfall delivery. Engineering ships every six weeks against a tightly scoped quarterly release plan owned by a PMO. Roadmaps are committed 12 months out. Three engineering teams (Platform, Insights, Connectors) and one product-led team (Activation) have been quietly running "Scrum-ish" two-week sprints for the last quarter but with no formal coaching, inconsistent ceremonies, and no shared definition of done.

The new VP Engineering, hired six weeks ago, wants an honest maturity assessment before he commits to a transformation budget. He has explicitly asked: "Don't sell me SAFe. Tell me where we actually are, and what the next 90 days should look like." This is exactly the work the agile-coach skill exists for.

## Inputs

- Five teams: 4 engineering (avg 6 engineers each) + 1 product/design pod
- Self-reported survey from 23 engineers, 5 EMs, 4 PMs, 2 designers (34 respondents, 89% response rate)
- Sprint metrics for the last six sprints from Jira (cycle time, velocity variance, escaped defect rate)
- Three observed ceremonies per team (standup, planning, retro) over two weeks
- VP Engineering constraint: 90-day proof of progress, no SAFe, pilot must be opt-in
- Cultural reality: middle managers cautiously supportive, senior leadership skeptical after a failed 2024 "agile rollout" that was really a Jira rollout

## Applying the skill

1. **Assess current state.** Scored the six maturity dimensions using the standard 1-5 model with evidence pulled from survey, ceremonies, and Jira data. The team would not have survived a generic 1-5 self-rating — the agent forced evidence per dimension.
2. **Identify the framework gap.** Wayfinder is already attempting Scrum without coaching. The decision was not "Scrum vs. Kanban vs. SAFe" — it was "fix the Scrum we already have." This is the key insight the framework selection grid surfaces: never recommend SAFe below maturity Level 2, and recommend Kanban only if the work is operational. Wayfinder's work is product development, so Scrum stays.
3. **Design a Foundation phase plan.** Because the previous transformation failed, the agent did NOT recommend launching all teams at once. Instead: two volunteer pilot teams, 12 weeks, success criteria defined up front. This maps directly to the Foundation -> Pilot phase boundary in the transformation roadmap.
4. **Match coaching stance to team stage.** Three of the four engineering teams are in Tuckman "norming"; one (Connectors) is still "storming" due to a tech-lead conflict. The agent flagged that Connectors needs facilitative + conflict-resolution coaching first, not Scrum coaching.
5. **Set 90-day metrics.** Picked one metric from each of the four categories (outcome, process, quality, team) — not all of them. The VP got a one-page scorecard, not a 40-row spreadsheet.

## The artifact

```
================================================================
  Wayfinder Analytics — Agile Maturity Assessment
  Date: 2026-05-22
  Coach: Agile Coach (skill)
  Sponsor: VP Engineering
================================================================

OVERALL MATURITY SCORE: 2.2 / 5.0   (Level 2: Repeatable)

EXECUTIVE SUMMARY
-----------------
Wayfinder is at the low end of Level 2. Teams have adopted Scrum
ceremonies but the underlying mindset, technical practices, and
outcome-orientation are still Level 1-2. The 2024 transformation
failure was not an agile failure — it was a tool rollout
masquerading as a transformation. Engineers correctly remember
it as "they renamed our Gantt chart Jira." Re-using the word
"transformation" will fail. Re-frame as "fixing the Scrum we
already have."

DIMENSION SCORES (with evidence)
--------------------------------

1. Values & Mindset                                  2 / 5
   Evidence: 71% of engineers said "agile = sprints"; only 18%
   could name a value from the Agile Manifesto without prompting.
   Daily standups are status reports to EMs, not team coordination.

2. Team Practices                                    3 / 5
   Evidence: Ceremonies happen on cadence across all 4 teams.
   However, retros average 22 minutes (too short for real
   reflection) and only 1 of 4 teams has a written Definition
   of Done.

3. Technical Excellence                              2 / 5
   Evidence: CI exists but takes 47 minutes; integration tests
   are flaky (8% spurious failure rate over last 4 weeks);
   no trunk-based development; production deploys gated by a
   manual change-advisory board on Wednesdays.

4. Product Ownership                                 2 / 5
   Evidence: PMs ship features, not outcomes. 0 of 11 PRDs
   reviewed in the last quarter listed a measurable outcome.
   Quarterly OKRs at the company level do not connect to
   sprint goals.

5. Leadership Support                                3 / 5
   Evidence: New VP Engineering is a strong sponsor. Middle EMs
   are supportive but burned by 2024. CEO neutral. CFO concerned
   about velocity tracking changing — sees it as a control loss.

6. Continuous Improvement                            1 / 5
   Evidence: Retro action items tracked in a Confluence page
   no one reads. Of 47 action items in Q1, 6 were completed (13%).
   Most action items are vague ("communicate better").

FRAMEWORK RECOMMENDATION
------------------------
KEEP Scrum. Do NOT introduce SAFe (we are below the L2
threshold for scaled frameworks and have only 4 product teams).
Do NOT switch to Kanban (work is product development with
discrete features, not ops flow).

The framework is not the problem. The execution is.

90-DAY PILOT PLAN (FOUNDATION PHASE)
------------------------------------
Pilot teams: Insights, Activation
  (Both teams volunteered. Connectors NOT included — see
   below. Platform NOT included — too central; failure
   blast radius too large.)

WEEK 1-2: Baseline
  - Capture current sprint metrics (cycle time p50/p85,
    velocity variance, escaped defects, retro action close rate)
  - Run a "why agile" workshop framed as "fix the Scrum we
    already have" (avoid the word transformation)
  - Define a single team-level Definition of Done per pilot team
  - Establish one outcome OKR per pilot team for the quarter

WEEK 3-8: Coaching cadence
  - 1 hour/week embedded coach time per pilot team
  - Stance: facilitative for Insights (norming);
            teaching+advising for Activation (still forming
            after recent re-org)
  - Re-shape retros: 60 minutes, Sailboat format every other
    sprint, 4Ls on alternates, hard cap of 3 action items
    per retro with named owners and due dates
  - Reserve 15% sprint capacity for improvement items

WEEK 9-12: Demonstrate quick wins
  - Publish a one-page scorecard to the engineering all-hands
  - Run a cross-team show-and-tell where pilot teams share
    what changed
  - Decide go/no-go on expanding to Connectors and Platform

CONNECTORS TEAM — SEPARATE TRACK
--------------------------------
Connectors is in Tuckman storming due to an unresolved
tech-lead conflict. Doing Scrum coaching there now will fail.
Recommend a 4-week conflict-resolution intervention first:

  1. Acknowledge — joint session with both leads
  2. Understand — separate 1:1s, surface underlying interests
  3. Explore — facilitated team chartering session
  4. Agree — written team agreement, 30-day check-in

Re-evaluate Connectors for Scrum coaching at the 60-day mark.

90-DAY SUCCESS METRICS (ONE PER CATEGORY)
-----------------------------------------
Outcome   Each pilot team has 1 outcome OKR tied to NSM;
          progress reported in week 12 review

Process   Cycle time p85 reduced by 20% on pilot teams
          (baseline: Insights 9.2 days, Activation 11.4 days)

Quality   Escaped defect rate cut by 30% on pilot teams
          (baseline: 4.1 escaped defects / 100 stories)

Team      Team NPS improves by +10 on quarterly survey
          (baseline: Insights -8, Activation +4)

RISKS & MITIGATIONS
-------------------
R1  CFO sees velocity tracking change as control loss.
    -> VP Eng to co-present the scorecard format with CFO
       before week 1; preserve velocity reporting alongside
       new metrics for the first quarter.

R2  Engineers compare this to the failed 2024 rollout.
    -> Open the "why agile" workshop by NAMING the 2024
       failure. Do not pretend it didn't happen.

R3  Connectors team conflict spills into pilot teams.
    -> Separate track (see above). Brief EMs across all
       teams not to discuss Connectors situation cross-team.

R4  Pilot success looks like cherry-picked teams.
    -> Publish pilot selection criteria up front. Make
       criteria for inviting next 2 teams explicit.

GO / NO-GO DECISION GATE (END OF WEEK 12)
-----------------------------------------
Advance to Pilot expansion only if all of these are true:
  - At least 2 of 4 success metrics moved in the right
    direction with statistical significance
  - Retro action item close rate exceeds 60% on pilot teams
  - VP Eng, CFO, and at least one pilot EM rate progress as
    "on track or better"
  - At least one engineer per pilot team volunteers to coach
    the next wave (the seed of internal coaches)
```

## Why this works

- **Honest scoring with evidence.** The maturity score is anchored in survey data, observed ceremonies, and Jira metrics — not vibes. A weaker coach would have scored Wayfinder a 3 because "they have sprints."
- **Refused to recommend SAFe.** Wayfinder is below Level 2 in three dimensions. The framework selection grid is unambiguous: never SAFe below L2. A consulting firm trying to sell capacity would have pitched SAFe Essential here.
- **Named the 2024 failure.** Most maturity reports gloss over prior failed attempts. Surfacing it explicitly is what makes the "fix the Scrum we already have" reframe credible to skeptical engineers.
- **Connectors gets a different intervention.** Coaching stance must match team development stage. Storming teams do not benefit from Scrum mechanics; they need conflict resolution. This is straight from the GROW model + Tuckman stage matching.
- **One metric per category, not forty.** The four-category scorecard is the framework. The instinct to track everything is the anti-pattern.

## What's next

- After week 12 go/no-go, hand off team-level execution to [`../scrum-master/`](../scrum-master/) for the two pilot teams.
- Use [`../sprint-retrospective/`](../sprint-retrospective/) to instrument Sailboat and 4Ls retros with data-driven follow-up.
- For the CFO conversation, pair this assessment with a portfolio-level view from [`../senior-pm/`](../senior-pm/) so engineering and finance share a single picture.
- When Connectors is ready for Scrum coaching at the 60-day mark, run a fresh maturity scoring for that team in isolation.
- For the "why agile" workshop, draw facilitation patterns from `references/facilitation.md`.
