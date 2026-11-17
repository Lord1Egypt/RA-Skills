## Description:

Automatically generate daily/weekly work reports from git commits, calendar events, and task lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1989tianlong](https://clawhub.ai/user/1989tianlong)

### License/Terms of Use:

MIT

## Use Case:

Employees and developers use this skill to generate concise daily or weekly work reports from local project activity, especially git commit history. It helps turn recent work activity into a shareable Markdown report with minimal manual drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command construction may allow a hostile repository path, argument, or .reportrc.json value to run unintended commands.

Mitigation: Run only in trusted repositories with reviewed .reportrc.json files until command construction is fixed.

Risk: Generated reports may expose confidential details from commit messages.

Mitigation: Review generated report contents before sharing outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1989tianlong/skills/ytlong-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown report text and generated report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily, weekly, or custom date ranges; output may include commit messages that should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
