## Description:

Trace removed or relocated config files across source, releases, migration code, and local state without mistaking relocation for deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate configuration, workspace, or instruction files that appear to disappear after an upgrade and to determine whether the files were deleted, relocated, merged, or left unsupported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local configuration or instruction files may contain private project details when the skill is used for migration analysis.

Mitigation: Review the agent's findings before sharing them and redact project-specific or sensitive configuration details.

Risk: A missing legacy file can be misread as data loss when the file was relocated or merged.

Mitigation: Check the destination, backup, timestamps, migration code, and active instruction files before reporting a final conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/trace-configuration-file-migrations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown investigation report with concise findings and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conclusions, timeline, migration behavior, recovery path, verified local outcome, and unknowns.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
