---
name: realtime-campaign-monitor
description: Monitor live campaign health and anomalies across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic.
---

# Ads Campaign Monitor

## Purpose
Core mission:
- real-time thresholding, anomaly triage, alert playbook

This skill is specialized for advertising workflows and should output actionable plans rather than generic advice.

## When To Trigger
Use this skill when the user asks for:
- ad execution guidance tied to business outcomes
- growth decisions involving revenue, roas, cpa, or budget efficiency
- platform-level actions for: Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, DSP/programmatic
- this specific capability: real-time thresholding, anomaly triage, alert playbook

High-signal keywords:
- ads, advertising, campaign, growth, revenue, profit
- roas, cpa, roi, budget, bidding, traffic, conversion, funnel
- meta, googleads, tiktokads, youtubeads, amazonads, shopifyads, dsp

## Input Contract
Required:
- entity_ids: account, campaign, adset, or ad identifiers
- incident_or_audit_scope
- time_window

Optional:
- logs_or_events
- policy_flags
- alert_thresholds
- owner_contacts

## Output Contract
1. Operational Status Summary
2. Severity-ranked Findings
3. Mitigation Actions
4. Escalation Ticket Payload
5. Monitoring Checklist

## Workflow
1. Confirm operational scope and impacted entities.
2. Validate data freshness and event completeness.
3. Detect anomalies, policy flags, or setup gaps.
4. Rank fixes by spend risk and recovery speed.
5. Emit owner-ready action and ticket payload.

## Decision Rules
- If data is stale, block final judgement and request refresh timestamp.
- If high-severity risk is found, recommend containment action first.
- If root cause is uncertain, provide top hypotheses with validation order.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, DSP/programmatic

Platform behavior guidance:
- Keep recommendations channel-aware; do not collapse all channels into one generic plan.
- For Meta and TikTok Ads, prioritize creative testing cadence.
- For Google Ads and Amazon Ads, prioritize demand-capture and query/listing intent.
- For DSP/programmatic, prioritize audience control and frequency governance.

## Constraints And Guardrails
- Never fabricate metrics or policy outcomes.
- Separate observed facts from assumptions.
- Use measurable language for each proposed action.
- Include at least one rollback or stop-loss condition when spend risk exists.

## Failure Handling And Escalation
- If critical inputs are missing, ask for only the minimum required fields.
- If platform constraints conflict, show trade-offs and a safe default.
- If confidence is low, mark it explicitly and provide a validation checklist.
- If high-risk issues appear (policy, billing, tracking breakage), escalate with a structured handoff payload.

## Code Examples
### Incident Ticket Example

    ticket_id: INC-ads-001
    severity: high
    impact: spend_waste_risk
    owner: media-ops
    next_check_at: 2026-03-03T10:00:00Z

### Health Rule Example

    rule: delivery_drop
    condition: impressions_down_pct > 40
    action: alert_and_pause_review

## Examples
### Example 1: Pixel breakage before launch
Input:
- Purchase event missing
- Campaign start in 24h

Output focus:
- severity ranking
- immediate mitigation
- relaunch checklist

### Example 2: Account health audit
Input:
- Multiple platform accounts
- Unknown policy or billing status

Output focus:
- readiness scorecard
- blocking risks
- owner-level actions

### Example 3: Live anomaly handling
Input:
- Spend spikes with no conversion lift
- Multiple campaigns impacted

Output focus:
- anomaly triage path
- containment actions
- incident ticket payload

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
