## Description: <br>
Clawhub Daily scans ClawHub skill listings, computes recommendation metrics, and produces concise daily skill recommendation briefs with optional Feishu or IMA delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, team leads, content creators, and ClawHub users use this skill to monitor AI Agent skill trends, identify useful skills across common pain-point categories, and receive repeatable recommendation briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use sensitive Feishu or IMA credentials for external delivery. <br>
Mitigation: Review Feishu and IMA permissions, keep references/config.json out of version control, and provide credentials only when push delivery is needed. <br>
Risk: Scheduled runs create recurring network access and external message delivery. <br>
Mitigation: Run once with --skip-push to inspect the generated report before enabling cron or Task Scheduler. <br>


## Reference(s): <br>
- [ClawHub Daily Skill Page](https://clawhub.ai/edwardwason/skill-daily) <br>
- [API Contract](references/api-contract.md) <br>
- [Source Data Schema](references/source-data-schema.md) <br>
- [Briefing Template](references/briefing-template.md) <br>
- [Pain Points](references/pain-points.md) <br>
- [Setup Wizard](references/setup-wizard.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON files, terminal status text, and optional Feishu or IMA messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public ClawHub skill data, writes dated snapshots and recommendations, and can skip external delivery with --skip-push.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and CHANGELOG, released 2026-06-05) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
