## Description: <br>
Manage B2B sales pipelines by tracking deals, forecasting revenue, logging activity, alerting on stale deals, qualifying leads, and drafting outreach while storing data locally in JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cunningham050503-ops](https://clawhub.ai/user/cunningham050503-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams, founders, and revenue operators use this agent to maintain a local B2B pipeline, inspect forecasts, track deal activity, qualify leads, and draft sales outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deleting a deal permanently removes that record from the local pipeline database. <br>
Mitigation: Back up pipeline.json before using delete commands and verify deal IDs before updates or deletion. <br>
Risk: Deal notes and contact fields could contain secrets or regulated customer data. <br>
Mitigation: Avoid storing secrets or regulated customer data in deal notes or contact records. <br>


## Reference(s): <br>
- [Sales Methodology Reference](artifact/references/sales_methodology.md) <br>
- [Outreach Templates by Stage](artifact/references/outreach_templates.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/cunningham050503-ops/sales-pipeline-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, drafted outreach text, and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates a local pipeline JSON database under ~/.openclaw/workspace/sales-pipeline-agent/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
