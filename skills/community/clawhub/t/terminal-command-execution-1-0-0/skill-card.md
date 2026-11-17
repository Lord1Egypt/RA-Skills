## Description:

Execute terminal commands safely and reliably with clear pre-checks, output validation, and recovery steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1215656](https://clawhub.ai/user/1215656)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan, run, validate, and recover from shell commands while managing files, tools, services, or command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal commands can affect files, packages, services, credentials, or system settings.

Mitigation: Review impactful commands before approval, start with non-destructive inspection, and keep operations scoped to specific files, paths, or services.

Risk: Ambiguous command targets can lead to actions in the wrong directory, service, or environment.

Mitigation: Clarify risky ambiguity, confirm working directory and required binaries, and verify observable state after each state-changing step.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pre-checks, command output interpretation, recovery steps, and concise status summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
