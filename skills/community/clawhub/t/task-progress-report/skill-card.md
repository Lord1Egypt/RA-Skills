## Description:

Task Progress Report helps agents provide periodic status updates for long-running tasks and write detailed Markdown progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheffly](https://clawhub.ai/user/cheffly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep users informed during long-running work such as model training, data processing, crawlers, and multi-stage analysis tasks. It produces concise chat updates and maintains a detailed local Markdown progress report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Progress reports may include sensitive task details in local Markdown files.

Mitigation: Confirm what information may be written before enabling the skill, and delete or archive report files when they are no longer needed.

Risk: Timer-based progress reporting may continue longer than intended for a task.

Mitigation: Confirm the reporting interval and timer behavior before use, and clean up scheduled reporting when the task completes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheffly/skills/task-progress-report)
- [Publisher profile](https://clawhub.ai/user/cheffly)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text status updates and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append local progress reports and final summaries under the configured reports directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
