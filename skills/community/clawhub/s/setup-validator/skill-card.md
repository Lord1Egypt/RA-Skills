## Description:

Validate OpenClaw installation safety by checking for common security misconfigurations and setup issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusy2k](https://clawhub.ai/user/marcusy2k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw installations for common setup issues such as broad file permissions, missing plugin manifests, absent configuration, sandboxing notes, and outdated OpenClaw versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate validation coverage and should not be treated as a complete security validator.

Mitigation: Use its findings as diagnostic prompts and confirm important results with manual review or an approved security process.

Risk: Suggested fixes can include destructive or broad local changes such as plugin removal, configuration reset, or global package updates.

Mitigation: Review each generated command before running it, especially commands that include plugin names or paths discovered from the local filesystem.

Risk: Periodic execution through cron creates recurring local checks and command activity.

Mitigation: Enable scheduled validation only after confirming the paths, commands, and cadence are appropriate for the target environment.

## Reference(s):

- [Setup Validator page](https://clawhub.ai/marcusy2k/skills/setup-validator)
- [Setup Validator Checks](references/CHECKS.md)
- [Example Fixes for Common Issues](references/EXAMPLE_FIXES.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts report local diagnostic findings and suggested fixes for review before execution.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
