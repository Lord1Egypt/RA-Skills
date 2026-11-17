## Description:

Create new skills, modify and improve existing skills, and measure skill performance with eval-driven iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zihaofeng2001](https://clawhub.ai/user/zihaofeng2001)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create, revise, evaluate, benchmark, and package agent skills through eval-driven iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper tools can affect local processes or expose local evaluation data.

Mitigation: Review the skill before installing, avoid elevated privileges, and prefer static viewer output where possible.

Risk: The review viewer may bind to a local port.

Mitigation: Confirm port 3117 is available and appropriate before starting the server, or use static output.

Risk: Packaged skill directories could include unexpected filesystem entries.

Mitigation: Inspect skill directories for symlinks before packaging.

Risk: Description optimization may send proprietary or secret-containing skill or eval content through the external Claude CLI workflow.

Mitigation: Use the optimizer only when sending that content through the configured Claude CLI is acceptable.

## Reference(s):

- [Skill schemas](references/schemas.md)
- [Skill Creator Pro on ClawHub](https://clawhub.ai/zihaofeng2001/skills/skill-creator-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, JSON schemas, shell commands, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create eval workspaces, benchmark reports, packaged skill archives, and static HTML review pages.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
