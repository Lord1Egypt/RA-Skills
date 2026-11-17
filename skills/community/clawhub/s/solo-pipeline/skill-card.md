## Description:

Launch automated multi-skill pipeline that chains skills into a loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and builders use this skill to coordinate research or development workflows by confirming a pipeline and then running staged skills such as research-to-PRD or scaffold-to-build.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate multi-step research or development workflows that trigger other skills after confirmation.

Mitigation: Confirm the listed pipeline stages before starting and use it only when a multi-stage workflow is intended.

Risk: Pipeline runs may create local .solo state and log files, and deleting a state file cancels that pipeline run.

Mitigation: Review the expected state and log locations before running, and treat state-file deletion as an irreversible cancellation for that run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fortunto2/skills/solo-pipeline)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate multi-stage skill execution after user confirmation and may create local .solo pipeline state and log files.]

## Skill Version(s):

1.4.0 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
