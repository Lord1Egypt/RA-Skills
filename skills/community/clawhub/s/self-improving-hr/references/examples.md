# Entry Examples

Concrete examples of well-formatted HR entries with all fields. All examples are anonymized — no PII.

## Learning: Policy Gap (Remote Work Policy for International Contractors)

```markdown
## [LRN-20250415-001] policy_gap

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: compliance

### Summary
Remote work policy does not address international contractors working from non-US jurisdictions

### Details
The current remote work policy only covers US-based employees. Three contractors
working from EU countries have no guidance on data residency, tax implications,
or local employment law compliance. The company may have permanent establishment
risk in two jurisdictions.

### Impact
- **Affected population**: international contractors (estimated 12 across 4 countries)
- **Risk level**: compliance (tax), legal (permanent establishment), financial
- **Estimated scope**: all non-US contractors

### Suggested Action
Draft international remote work addendum covering: tax obligations, data residency
(GDPR), local employment law compliance, and permanent establishment risk assessment.
Engage employment counsel in each jurisdiction.

### Metadata
- Source: manager_report
- Jurisdiction: international
- Regulation: GDPR, local_employment_law
- Related Files: policies/remote-work-policy.md
- Tags: remote-work, international, contractors, compliance, permanent-establishment
- Pattern-Key: policy_gap.remote_work_international

---
```

## Learning: Compliance Risk (I-9 Re-Verification Deadline Missed)

```markdown
## [LRN-20250416-001] compliance_risk

**Logged**: 2025-04-16T09:15:00Z
**Priority**: critical
**Status**: pending
**Area**: compliance

### Summary
I-9 re-verification deadline missed for 3 employees with expiring work authorizations

### Details
Internal audit found that Section 3 of Form I-9 was not completed before the
work authorization expiry date for 3 employees on temporary work visas. Two had
H-1B extensions pending; one had an expiring EAD. The HRIS system did not trigger
alerts because the notification was configured for 30 days but the re-verification
window was 90 days for these visa types.

### Impact
- **Affected population**: 3 employees with temporary work authorization
- **Risk level**: compliance (ICE audit exposure), financial (fines up to $2,507 per violation)
- **Estimated scope**: all employees on temporary work authorizations (~25)

### Suggested Action
1. Complete Section 3 retroactively with immigration counsel guidance
2. Reconfigure HRIS alert to trigger at 90, 60, and 30 days before expiry
3. Assign immigration compliance owner to review alerts weekly
4. Add I-9 re-verification to compliance calendar

### Metadata
- Source: audit
- Jurisdiction: federal
- Regulation: INA, 8 CFR 274a.2
- Related Files: compliance/i9-procedures.md
- Tags: i9, work-authorization, immigration, compliance, visa
- Pattern-Key: compliance_risk.i9_reverification

---
```

## Learning: Onboarding Friction (IT Setup Taking 5 Days)

```markdown
## [LRN-20250417-001] onboarding_friction

**Logged**: 2025-04-17T14:00:00Z
**Priority**: medium
**Status**: pending
**Area**: onboarding

### Summary
New hire IT setup averaging 5 business days instead of target 1 day

### Details
Survey of last 8 new hires in engineering shows average time from start date to
fully functional laptop with all required access: 5.2 business days. Root causes:
hardware not pre-ordered (procurement requires manager approval 2 weeks before
start), software licenses requested after start date, building access badge takes
3 days from facilities.

### Impact
- **Affected population**: all new hires (currently ~6/month)
- **Risk level**: retention (poor first impression), productivity (lost billable days)
- **Estimated scope**: 30 lost productivity days per quarter

### Suggested Action
Implement pre-boarding checklist triggered at offer acceptance:
- T-10 days: hardware order placed by IT
- T-5 days: software licenses provisioned
- T-3 days: building access badge prepared
- T-1 day: workstation configured and tested

### Metadata
- Source: candidate_feedback
- Related Files: onboarding/new-hire-checklist.md
- Tags: onboarding, it-setup, equipment, productivity, first-impression
- Pattern-Key: onboarding_friction.it_setup_delay

---
```

## HR Process Issue: Candidate Experience (Offer Letter Delay)

```markdown
## [HRP-20250418-001] candidate_experience

**Logged**: 2025-04-18T11:00:00Z
**Priority**: high
**Status**: pending
**Area**: recruiting

### Summary
Offer letter approval process taking 7+ days, causing candidate withdrawals

### Issue Details
In Q1, 4 of 22 offer-accepted candidates withdrew before receiving the formal
offer letter. Average time from verbal offer to written offer: 7.3 business days.
Approval chain requires hiring manager, department head, compensation team, and
VP sign-off. Two approvers were consistently unavailable due to travel.

### Root Cause
Sequential approval chain with no delegation or timeout escalation. Compensation
review step adds 2-3 days because it requires manual band verification.

### Remediation
1. Implement parallel approval where possible (comp review concurrent with dept head)
2. Add 48-hour auto-escalation for pending approvals
3. Pre-approve compensation for roles within published band ranges
4. Set SLA: verbal offer to written offer within 3 business days

### Compliance Impact
- **Regulation**: N/A (internal process)
- **Exposure**: talent loss, increased cost-per-hire, reputational risk
- **Deadline**: implement before Q3 hiring surge

### Context
- Trigger: hris_alert
- Jurisdiction: N/A
- Department: engineering, product (highest volume)
- Headcount impact: 4 lost candidates in Q1

### Metadata
- Reproducible: yes
- Related Files: recruiting/offer-process.md
- See Also: LRN-20250310-002

---
```

## HR Process Issue: Retention Signal (Team Attrition Spike)

```markdown
## [HRP-20250420-001] retention_signal

**Logged**: 2025-04-20T16:00:00Z
**Priority**: high
**Status**: pending
**Area**: performance

### Summary
3 senior engineers resigned from the same team within one quarter

### Issue Details
Between January and March, 3 of 8 senior engineers (L5+) on Team Alpha resigned.
All cited similar themes in exit interviews: lack of career growth path, unclear
promotion criteria, and dissatisfaction with project direction. Team's engagement
survey scores dropped 22 points from prior quarter.

### Root Cause
No formal career ladder documented for the engineering track above L5.
Promotion decisions perceived as inconsistent. Team reassigned from product work
to maintenance without explanation.

### Remediation
1. Document engineering career ladder L5-L8 with clear competency criteria
2. Conduct skip-level meetings with remaining team members within 2 weeks
3. Review and communicate project roadmap with team
4. Implement quarterly career growth conversations as mandatory manager duty
5. Conduct stay interviews with remaining senior ICs across engineering

### Compliance Impact
- **Regulation**: N/A
- **Exposure**: institutional knowledge loss, project delays, recruitment costs (~$45K per hire)
- **Deadline**: immediate (retention risk for remaining team)

### Context
- Trigger: exit_interview
- Department: engineering (Team Alpha)
- Headcount impact: 3 departures, 5 remaining at risk

### Metadata
- Reproducible: unknown (monitoring other teams)
- Related Files: hr/exit-interview-summaries-q1.md
- See Also: LRN-20250215-003

---
```

## Feature Request: Automated Compliance Deadline Tracking

```markdown
## [FEAT-20250419-001] compliance_deadline_tracker

**Logged**: 2025-04-19T13:00:00Z
**Priority**: high
**Status**: pending
**Area**: compliance

### Requested Capability
Automated tracking and alerting system for all HR compliance deadlines: I-9
re-verification, EEO-1 filing, OSHA 300A posting, state-specific notice
requirements, benefits enrollment windows, and COBRA notification timelines.

### User Context
Currently tracked in a spreadsheet maintained by one HR generalist. Two deadlines
were missed in the past year (I-9 re-verification and state posting update).
Single point of failure if the owner is unavailable.

### Complexity Estimate
medium

### Suggested Implementation
1. Build compliance calendar in HRIS with automated alerts at 90/60/30/7 days
2. Assign primary and backup owners for each deadline category
3. Daily digest email for deadlines within 30 days
4. Weekly report to HR Director for deadlines within 90 days
5. Integration with Slack/Teams for urgent (7-day) alerts
6. Annual calendar review in December for upcoming year's federal and state deadlines

### Metadata
- Frequency: recurring (multiple deadlines missed)
- Related Features: HRIS calendar module, notification system

---
```

## Learning: Promoted to Onboarding Checklist

```markdown
## [LRN-20250410-003] onboarding_friction

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: onboarding checklist (new-hire-preboarding.md)
**Area**: onboarding

### Summary
Pre-boarding checklist prevents day-one equipment and access issues

### Details
After tracking onboarding delays for 3 months (LRN-20250117-001, LRN-20250215-004,
LRN-20250310-002), established that a pre-boarding checklist triggered at offer
acceptance eliminates 90% of day-one friction. Piloted with engineering team for
6 hires — all had fully functional setup on day one.

### Suggested Action
Roll out pre-boarding checklist to all departments. Add to HRIS workflow as
automated task list triggered by offer acceptance.

### Metadata
- Source: candidate_feedback
- Related Files: onboarding/new-hire-preboarding.md
- Tags: onboarding, pre-boarding, checklist, equipment, access
- See Also: LRN-20250117-001, LRN-20250215-004, LRN-20250310-002
- Recurrence-Count: 4
- First-Seen: 2025-01-17
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill

```markdown
## [LRN-20250412-001] compliance_risk

**Logged**: 2025-04-12T15:00:00Z
**Priority**: critical
**Status**: promoted_to_skill
**Skill-Path**: skills/i9-reverification-tracker
**Area**: compliance

### Summary
Systematic approach to tracking and managing I-9 re-verification deadlines

### Details
Developed a repeatable compliance workflow after encountering I-9 re-verification
failures in 3 consecutive quarters. The pattern is consistent: HRIS alerts are
misconfigured, no backup owner is assigned, and the compliance window is too short
for the visa type.

### Suggested Action
Follow the compliance playbook:
1. Configure HRIS alerts at 90/60/30 days before work authorization expiry
2. Assign primary and backup compliance owners
3. Weekly review of upcoming expirations
4. Engage immigration counsel at 30 days if no renewal documentation
5. Complete Section 3 on or before expiry date

### Metadata
- Source: audit
- Jurisdiction: federal
- Regulation: INA, 8 CFR 274a.2
- Related Files: compliance/i9-procedures.md
- Tags: i9, immigration, compliance, work-authorization, visa
- See Also: LRN-20250416-001, HRP-20250120-002, HRP-20250305-001

---
```
