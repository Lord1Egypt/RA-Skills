# Example: Northwind SaaS — Coordinating a Multi-Team Black Friday Release

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Northwind SaaS (Series-B logistics + payments platform) processes 12-15x normal volume during the week of Black Friday and Cyber Monday. The 2026 BF/CM window is 2026-11-27 to 2026-12-02. The product team has three releases that need to land before the freeze on 2026-11-21:

- **Payments v3.2** — a new retry-policy engine to reduce false declines
- **Logistics v4.0** — a major rewrite of the carrier-rate cache
- **Identity v2.1** — multi-factor enrollment for merchant admin accounts

Three product teams. Three release trains. One shared incident response model. A single missed exit criterion in any one of them can blow the freeze window. The delivery-manager skill is being applied to plan the coordinated release, deployment strategies, rollback paths, and comms.

It is 2026-05-22; this is the early planning, 6 months out. The actual deploy will be 2026-11-19 (Wednesday before freeze).

## Inputs

- 3 release trains, 3 owning EMs, 3 owning PMs
- Shared on-call rotation (SRE), 4 on-call engineers
- Production traffic profile: 7M req/day baseline, projected 90-100M req/day peak BF
- Existing maturity: Level 3 (continuous delivery, push-button deploys, but no automatic rollback)
- Constraint: code freeze at 2026-11-21 00:00 UTC; no deploys 11-21 through 12-03 except security patches
- Constraint: rollback must be possible within 5 minutes for any of the three releases
- VP Eng directive: "If we are not ready, we don't ship. The cost of a bad release on Black Friday is higher than the cost of slipping."

## Applying the skill

1. **Assessed maturity per team.** Payments at Level 3, Logistics at Level 2 (still has a manual smoke test step), Identity at Level 3. Logistics' Level 2 forced a different rollout decision.
2. **Picked deployment strategy per release.** Payments and Identity get canary (Level 3). Logistics gets blue-green because the carrier-rate cache rewrite is high-risk and Level 2 maturity demands instant rollback.
3. **Wrote one shared exit-criteria checklist.** Every release uses the same checklist. No team-specific exceptions. This is the single biggest lever for coordinated releases.
4. **Defined Go/No-Go gates at T-7 and T-1.** Every team presents in the same 60-minute meeting. Any No-Go in any one team pulls the whole train.
5. **Drafted rollback runbooks per release.** Each runbook is testable; each was dry-run at least once in pre-production.
6. **Customer comms split into 3 audiences.** Merchants, internal support, internal exec.
7. **Wrote the incident response model.** During BF/CM, severity definitions shift. P3 becomes P2; P2 becomes P1. Three on-call engineers are dedicated to BF/CM volume only.

## The artifact

```
================================================================
  NORTHWIND BLACK FRIDAY 2026 — COORDINATED RELEASE PLAN
  Window:    Deploy 2026-11-19 (Wed); freeze 11-21 to 12-03
  Owner:     Delivery Manager
  Sponsors:  VP Eng, VP Product
  Last update: 2026-05-22
================================================================


PART 1 — SCOPE PER RELEASE

[1] PAYMENTS v3.2 — Retry Policy Engine
    Team:           Payments (5 eng, 1 PM, 1 EM)
    PM:             Priya Rao
    EM:             Marcus Lee
    Risk:           MEDIUM. Touches the hot path; well-tested.
    Goal:           Reduce false declines by 4-6%.
    Strategy:       Canary
    Feature flag:   pmt.retry_v3.2.enabled (default off)
    Rollback:       Flag off + revert deploy (~3 min)

[2] LOGISTICS v4.0 — Carrier-Rate Cache Rewrite
    Team:           Logistics (8 eng, 1 PM, 1 EM)
    PM:             Tomas Lewandowski
    EM:             Yusuf Diallo
    Risk:           HIGH. Schema change + cache layer rewrite.
                    Last attempt 2 quarters ago was rolled back.
    Goal:           Carrier rate calculation latency p99
                    from 380ms -> <80ms.
    Strategy:       Blue-Green
    Feature flag:   N/A (architecture-level, not flaggable)
    Rollback:       Switch traffic blue<->green (<1 min)

[3] IDENTITY v2.1 — Merchant Admin MFA Enrollment
    Team:           Identity (4 eng, 1 PM, 1 EM)
    PM:             Maria Chen
    EM:             Sara Kim
    Risk:           LOW. Additive; no path removed.
    Goal:           Enable MFA enrollment for ~800 merchants.
    Strategy:       Canary
    Feature flag:   id.mfa_v2.1.enabled (default off, opt-in)
    Rollback:       Flag off (~30 sec)


PART 2 — SHARED EXIT CRITERIA CHECKLIST

EVERY release must satisfy ALL of the following before Go.
No release-specific exceptions.

  Code & test
  [ ] All P1/P2 bugs in scope resolved
  [ ] Unit test coverage maintained or improved
  [ ] Integration test suite passing on main
  [ ] Load test at 10x baseline passed
  [ ] Soak test (4 hours) passed on staging
  [ ] Security scan clean (no new high/critical)

  Operational
  [ ] Runbook reviewed by SRE on-call
  [ ] Rollback procedure dry-run within last 14 days
  [ ] Monitoring + alerting wired before deploy
  [ ] Dashboards published on shared SRE channel
  [ ] On-call EM signed off on deploy plan

  Comms
  [ ] Release notes drafted
  [ ] Customer notification drafted (if customer-visible)
  [ ] Support team briefed (mandatory walkthrough)
  [ ] Exec stakeholders notified (T-7 + T-1)

  Compliance
  [ ] PCI-DSS impact assessed (Payments only)
  [ ] Data residency unchanged
  [ ] Audit log entries for the deploy itself enabled

This is the SAME checklist for every team. If it does not
fit your release, the release is changing, not the checklist.


PART 3 — DEPLOYMENT STRATEGIES IN DETAIL

[1] PAYMENTS v3.2 — CANARY

  Stage 1   1% traffic (5 selected non-merchant test accounts)
            Monitor 60 min
            Watch: payment_success_rate, decline_rate, p99 latency
            Block if: any metric moves >0.5%

  Stage 2   5% traffic (random selection across customer tiers)
            Monitor 2 hours
            Block if: payment_success_rate drops >0.2%

  Stage 3   25% traffic
            Monitor 4 hours
            Block if: any metric breach

  Stage 4   100% traffic
            Soak for 24 hours before BF freeze begins

  Total canary window: ~32 hours from start
  Start time: 2026-11-17 02:00 UTC (Tuesday off-hours)
  Full at:    2026-11-18 10:00 UTC

[2] LOGISTICS v4.0 — BLUE-GREEN

  Blue:    v3.9 (current, all traffic)
  Green:   v4.0 (deployed in parallel)

  Step 1   Deploy v4.0 to Green env, NO traffic
  Step 2   Smoke test Green via internal load generator
  Step 3   Shift 1% production traffic to Green
           Monitor 30 min
  Step 4   Shift 10% to Green
           Monitor 60 min
  Step 5   Shift 50% to Green
           Monitor 2 hours
  Step 6   Shift 100% to Green
           Blue remains warm for 24 hours
  Step 7   Decommission Blue after 24 hours soak

  Rollback: any breach -> shift all traffic Green->Blue <1 min

  Start time: 2026-11-18 02:00 UTC
  Full at:    2026-11-18 14:00 UTC

[3] IDENTITY v2.1 — CANARY

  Stage 1   Flag on for 3 internal Northwind staff merchants
            Monitor 24 hours
            Acceptance: zero auth-flow incidents
  Stage 2   Flag on for first 50 opt-in merchants
            Monitor 24 hours
  Stage 3   Flag on for all 800 merchants who opted in
  Stage 4   Make MFA available (still opt-in) to all merchants

  Start time: 2026-11-15 (gives 6-day soak window)
  Full at:    2026-11-19


PART 4 — COORDINATED TIMELINE

T-30 (2026-10-20)  Scope finalized for all 3 releases
T-21 (2026-10-29)  Load + soak testing completed for all 3
T-14 (2026-11-05)  Rollback dry-runs completed for all 3
T-7  (2026-11-12)  GO/NO-GO meeting #1 (90 min)
                   Each team presents exit criteria status.
                   Any No-Go pulls that release (or all if
                   inter-dependent).
T-2  (2026-11-17)  Identity canary begins (early start —
                   needs longest soak)
                   Payments canary begins
T-1  (2026-11-18)  GO/NO-GO meeting #2 (60 min)
                   Logistics blue-green begins after meeting
T-0  (2026-11-19)  All three releases at 100% by EOD
T+1  (2026-11-20)  Soak day; no other changes; war room open
T+2  (2026-11-21)  Code freeze begins 00:00 UTC


PART 5 — ROLLBACK CRITERIA & PROCEDURE

A rollback is triggered if ANY of the following observed:

  - payment_success_rate drops >0.5% sustained 10 min
  - carrier_rate_p99 exceeds 200ms sustained 5 min
  - auth_success_rate drops >0.2% sustained 10 min
  - any new error rate >1% in deploy-related code paths
  - on-call EM judgment call (single-person authority)

Rollback decision authority:
  Tier 1: On-call EM of the affected team can rollback their
          OWN release without escalation.
  Tier 2: If rollback of one release affects another (unlikely
          but possible), delivery manager makes the call.
  Tier 3: VP Eng informed within 15 minutes either way.

Rollback comms template (pre-written, fill-in-blanks):
  - Internal Slack #incidents announce within 5 minutes
  - Status page update within 15 minutes if customer-visible
  - Exec page if Tier 2 or higher within 30 minutes


PART 6 — INCIDENT RESPONSE MODEL (BF/CM WINDOW)

During BF/CM, severity definitions ELEVATE by one level:

  Normal time     BF/CM time
  P1 critical     P0 - full-org war room
  P2 major        P1 - SRE + EM page
  P3 minor        P2 - business hours triage
  P4 low          P3 - backlog

Why: a "minor checkout glitch" in normal time is a brand
incident on Black Friday.

On-call structure:
  - SRE lead (primary, paged first)
  - Payments EM secondary
  - Logistics EM secondary
  - Identity EM secondary
  - Delivery manager on-call for cross-team coordination
  - VP Eng on call for executive decisions

Comms cadence during incident:
  Internal Slack:      every 15 min until resolved
  Status page:         every 30 min until resolved
  Customer email:      only if P0 sustained >2 hours


PART 7 — CUSTOMER COMMS

[A] PRE-RELEASE EMAIL TO MERCHANTS — 2026-11-12 (T-7)
    To:      All 12,400 active merchants
    From:    product@northwind.com
    Subject: Improvements landing before Black Friday

    Body:
    Three updates roll out before our Black Friday freeze:
      1. Smarter payment retries (no merchant action needed).
      2. Faster carrier rate calculations on checkout.
      3. New optional MFA for your admin accounts -- you
         can enroll any time at /security/mfa.
    Window: Nov 17-19. No expected downtime. Status page:
    status.northwind.com.

[B] PRE-RELEASE BRIEF TO SUPPORT — 2026-11-13
    Live walkthrough of all three releases, 90 minutes.
    Includes: what changes for the merchant, what tickets
    might increase, escalation path.

[C] EXEC PRE-RELEASE NOTE — 2026-11-18
    1-page summary, what is shipping, what is at risk, what
    the go/no-go decision was.


PART 8 — POST-FREEZE PROCEDURE

  2026-12-03 00:00 UTC  Freeze ends
  2026-12-03            Post-mortem schedule sent
  2026-12-05            BF/CM retro (cross-team)

  Three required post-mortems regardless of incidents:
    1. What worked in the coordinated release
    2. What worked in incident response
    3. What we should change for 2027

  Even with zero incidents, the retro happens. The lessons
  from a smooth release are as valuable as the lessons from
  a bad one.


PART 9 — RISK REGISTER

  R1  Logistics v4.0 fails for the same reason as last time.
      Mitigation: blue-green strategy, instant rollback. Plus
      a 4-hour soak in pre-production with synthetic peak load.

  R2  Identity MFA opt-in surge floods support.
      Mitigation: stage 1 only enables for opt-in merchants;
      support briefed; FAQ pre-published.

  R3  Payments retry policy creates duplicate transactions
      in edge case.
      Mitigation: idempotency key enforced at API layer;
      canary watches duplicate-charge metric specifically.

  R4  All three teams "Go" at T-7 but one slips at T-1.
      Mitigation: explicit policy that releases CAN ship
      independently; releases NOT inter-dependent by design.
      A late Logistics does not block Payments.

  R5  On-call burnout pre-BF.
      Mitigation: no SRE on-call for non-BF work the week
      of release; backup roster doubled for BF week.


PART 10 — SUCCESS CRITERIA

  - All three releases at 100% by 2026-11-19 EOD
  - Zero customer-visible incidents during BF/CM (11-27 to 12-02)
  - Payment false-decline rate measurably reduced
  - Carrier-rate p99 measurably reduced
  - MFA enrollment available to all merchants
  - No emergency security patches during freeze
  - Cross-team retro yields >=3 actionable improvements for 2027
```

## Why this works

- **One shared exit-criteria checklist.** Three teams, three releases, one checklist. This is what prevents "we cleared it for our team" failure modes that doom coordinated releases.
- **Deployment strategy chosen by maturity, not by preference.** Logistics is at Level 2 and the change is high-risk — blue-green is the only acceptable strategy. Payments and Identity are at Level 3 with lower risk — canary is appropriate. The skill's maturity-to-strategy mapping is doing the work.
- **Releases independent by design.** Risk register R4 is the most important entry: the three releases are deliberately not interlocked. If Logistics slips, Payments and Identity still ship. Tightly-coupled releases are how multi-team programs fail.
- **Severity elevation during BF/CM.** Reclassifying P1 to P0, P2 to P1, P3 to P2 for the BF window is the operational discipline that distinguishes a delivery manager from a project manager. The same severity rubric does not work across all calendar moments.
- **Rollback dry-runs at T-14, not T-1.** Dry-runs at T-1 always reveal a step you forgot to test. Done at T-14 there is still time to fix the rollback procedure itself.
- **Mandatory post-mortem even with zero incidents.** Most teams only run a post-mortem after a bad release. The lessons from a smooth release are how you make the next release smoother.
- **VP Eng has a written "slip > bad ship" directive.** This is the political cover for the on-call EM who has to make a No-Go call at T-1. Without it, the call becomes career-risky.

## What's next

- The post-release retros at T+14 use [`../sprint-retrospective/`](../sprint-retrospective/) for the structure.
- Any incidents that occur use [`../execution/post-mortem/`](../execution/post-mortem/) for blameless RCA.
- Customer-facing communications use [`../execution/release-notes/`](../execution/release-notes/) and [`../execution/launch-playbook/`](../execution/launch-playbook/).
- Feature flag strategy details for Payments and Identity are anchored in [`../execution/feature-flag-strategy/`](../execution/feature-flag-strategy/).
- For Logistics' next release after Black Friday, escalate to [`../agile-coach/`](../agile-coach/) to bring the team's maturity from Level 2 to Level 3.
- Cross-team dependency tracking pre-release uses [`../execution/dependency-map/`](../execution/dependency-map/).
