## Description: <br>
B2B sales pipeline manager powered by the Alibaba Iron Army methodology for daily briefings, lead management, pipeline health checks, weekly sprint planning, customer follow-up prioritization, and closing strategy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepseekCMO](https://clawhub.ai/user/deepseekCMO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales employees and business operators use this skill to maintain a local B2B pipeline, prioritize daily follow-ups, plan weekly sales sprints, and generate customer-specific outreach guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer names, deal status, activity history, and notes are stored in local plaintext markdown files. <br>
Mitigation: Install only in workspaces where plaintext sales data is acceptable; avoid storing secrets, regulated data, or sensitive customer information. <br>
Risk: Generated sales briefs or transcripts may expose customer or deal details if shared broadly. <br>
Mitigation: Review outputs before sharing and redact customer, deal, and activity details when necessary. <br>
Risk: The optional cron workflow can generate recurring morning briefs automatically. <br>
Mitigation: Enable the cron job only when recurring automatic brief generation is desired and appropriate for the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deepseekCMO/sales-rhythm-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and local shell-script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local plaintext markdown pipeline files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
