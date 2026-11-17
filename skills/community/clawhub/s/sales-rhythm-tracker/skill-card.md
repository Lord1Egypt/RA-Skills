## Description:

B2B sales pipeline manager that helps an OpenClaw agent produce daily sales briefings, lead management updates, pipeline health checks, weekly sprint plans, follow-up priorities, and closing guidance using the Alibaba Iron Army methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekcmo](https://clawhub.ai/user/deepseekcmo)

### License/Terms of Use:

MIT

## Use Case:

Sales teams, founders, and account owners use this skill to keep a local B2B pipeline current, prioritize daily follow-up, diagnose stalled deals, and generate weekly sales sprint plans. It is most useful when the agent can read and update local markdown CRM records for active leads, activity history, and closed deals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sales and customer notes are stored in local markdown files and may contain sensitive customer or deal information.

Mitigation: Keep the workspace private, avoid recording unnecessary sensitive data, and review files before sharing, committing, or syncing them.

Risk: Pipeline records are read back into the agent for briefings and reports, so untrusted customer-provided text could influence agent behavior.

Mitigation: Do not paste customer instructions or untrusted text directly into CRM notes without sanitizing them, and inspect pipeline files for embedded instructions before reports are generated.

Risk: Scheduled briefs or follow-up automations can cause actions to run without close user attention.

Mitigation: Confirm cron setup, write operations, and follow-up actions before enabling automation or letting the agent update records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekcmo/skills/sales-rhythm-tracker)
- [README](artifact/README.md)
- [Sample pipeline template](artifact/templates/sample-pipeline.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, local markdown CRM records, shell-command output, and concise sales action guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts initialize, append to, and read local markdown files under ~/.openclaw/workspace/sales.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
