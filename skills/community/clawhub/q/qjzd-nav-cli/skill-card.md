## Description:

Use when the task involves QJZD Nav CLI, including managing links, categories, tags, backups, settings, or authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nqdy666](https://clawhub.ai/user/nqdy666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this routing skill to select the right QJZD Nav CLI area for authentication, content management, backup, restore, settings, and related command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an existing qjzd-nav CLI binary and shell completion eval commands execute output from that binary in the user's shell.

Mitigation: Install and use the skill only when the local qjzd-nav binary is trusted, and review shell completion output before enabling it.

Risk: Force operations can bypass interactive safeguards during QJZD Nav CLI workflows.

Mitigation: Use --force only after confirming the target operation, selected profile, and recovery plan.

## Reference(s):

- [Qjzd Nav Cli ClawHub page](https://clawhub.ai/nqdy666/skills/qjzd-nav-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes users to QJZD Nav CLI domain skills and recommends command help, JSON output, profile selection, and cautious force usage.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
