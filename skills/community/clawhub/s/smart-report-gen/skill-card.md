## Description:

Daily Report Generator helps agents create daily, weekly, monthly, project, sprint, incident, and customer reports from available work logs, memory files, Git history, project files, or user-provided notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wskflf](https://clawhub.ai/user/wskflf)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and delivery teams use this skill to summarize work activity into status reports for standups, weekly updates, project reviews, incident postmortems, or customer communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may gather broad memory, repository, workspace, task-note, or optional API data when generating reports, which can expose confidential, customer, personal, or proprietary information.

Mitigation: Limit source paths and date ranges before generation, preview candidate inputs, redact sensitive content, and require separate confirmation before creating Feishu or other externally shareable output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wskflf/skills/smart-report-gen)
- [Publisher profile](https://clawhub.ai/user/wskflf)
- [Report templates](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Feishu cards, plain text, or custom report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce Chinese, English, or bilingual reports and can use date-range helper commands for daily, weekly, and monthly summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
