## Description:

Monitor live campaign health and anomalies across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

External teams and ad operations practitioners use this skill to monitor live advertising campaigns, triage anomalies, rank spend risks, and prepare owner-ready mitigation and escalation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share unnecessary sensitive campaign data or owner contact details while preparing monitoring inputs.

Mitigation: Provide only the minimum campaign identifiers, incident scope, and time window needed for triage; redact owner contact details that are not needed for the handoff.

Risk: Containment recommendations such as pausing or changing campaigns can affect spend, delivery, or revenue.

Mitigation: Review proposed actions before applying them in an ad platform and use the skill's rollback or stop-loss conditions when spend risk exists.

Risk: Stale or incomplete campaign data can lead to incorrect severity ranking or mitigation guidance.

Mitigation: Validate data freshness and event completeness, and request a refresh timestamp before making a final judgment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/skills/realtime-campaign-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured status summaries, severity-ranked findings, mitigation actions, escalation ticket payloads, and monitoring checklists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed facts from assumptions and includes rollback or stop-loss conditions when spend risk exists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
