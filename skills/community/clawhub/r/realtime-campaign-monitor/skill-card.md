## Description: <br>
Monitor live campaign health and anomalies across Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, and DSP/programmatic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Advertising operations teams and marketers use this skill to monitor live campaign health, triage anomalies, rank mitigation actions, and prepare escalation tickets across major ad platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign guidance may be treated as confirmed platform state when data is stale, incomplete, or missing critical identifiers. <br>
Mitigation: Require entity IDs, incident or audit scope, and a time window; validate data freshness before final judgement; separate observed facts from assumptions. <br>
Risk: Recommendations can affect spend, billing, policy status, or tracking behavior. <br>
Mitigation: Prioritize containment for high-severity risk, include rollback or stop-loss conditions, and escalate policy, billing, or tracking breakage with a structured handoff payload. <br>
Risk: Requests may include campaign IDs, logs, thresholds, or owner contact details. <br>
Mitigation: Provide only the operational data intended for the agent to use and avoid unnecessary sensitive logs or contact details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/realtime-campaign-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown with structured summaries, findings, mitigation steps, ticket payloads, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should separate observed facts from assumptions, include measurable actions, and provide rollback or stop-loss conditions when spend risk exists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
