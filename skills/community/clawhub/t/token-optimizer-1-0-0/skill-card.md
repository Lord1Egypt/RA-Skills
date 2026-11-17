## Description:

Token Optimizer is a workflow controller that helps agents reduce repeated work by using pre-checks, path validation, progress checkpoints, log analysis, and fast error localization across Windows, macOS, Linux, MaxClaw, and ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smxtx](https://clawhub.ai/user/smxtx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to structure work with upfront checks, path validation, checkpoints, and error-pattern analysis so repeated troubleshooting loops consume fewer tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell diagnostic and process-management examples may be unsafe if user-supplied ports or process names are passed through without review.

Mitigation: Review or rewrite command examples before use, validate any port or process input, and require confirmation before terminating processes.

Risk: Checkpoint examples may save local task state to disk.

Mitigation: Choose an appropriate storage path, avoid sensitive content in checkpoint data, and clean up local checkpoint files according to the deployment policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smxtx/skills/token-optimizer-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/smxtx)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, command examples, and JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local checkpoint data examples and shell diagnostics that require review before execution.]

## Skill Version(s):

1.2.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
