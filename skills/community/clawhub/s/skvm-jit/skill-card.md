## Description:

Triggers `skvm jit-optimize` with post-task evidence to generate a reviewable optimization proposal for a skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lec77](https://clawhub.ai/user/lec77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after a failed or partial skill-driven task to capture concise evidence and launch `skvm jit-optimize` for a reviewable proposal to improve the underlying skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task reports or selected logs may be processed by an external optimizer model.

Mitigation: Use the concise `report.json` format when possible and redact credentials, tokens, private file contents, customer data, and sensitive paths before running the optimizer.

Risk: The artifact includes installer guidance that uses a `curl | sh` pattern.

Mitigation: Independently verify the installer source and scope before running it, or use a package-manager installation path when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lec77/skills/skvm-jit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a detached optimization command and a proposal identifier for later review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
