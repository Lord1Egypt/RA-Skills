## Description:

Provides agent guidance for layered shell-command safety checks, including injection detection, destructive-operation warnings, sensitive-path protection, and refusal messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizlzzzz](https://clawhub.ai/user/lizlzzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assess shell commands before execution, reject injection patterns, require confirmation for destructive operations, and protect sensitive files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits some destructive shell and git operations after confirmation rather than blocking them outright.

Mitigation: Review the destructive-command policy before deployment and require explicit confirmation for force pushes, hard resets, recursive deletion, and recursive file removal.

Risk: The skill may be consulted for many command-related tasks as an agent-wide shell safety checklist.

Mitigation: Install it only where agent operators want this broad shell-safety behavior, and pair it with existing execution approval controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text, shell commands]

**Output Format:** [Markdown guidance with command examples and decision rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; intended as an agent safety checklist for command review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
