## Description:

Self-Correct provides a lightweight self-correction framework with retry/error tags, result verification, and snapshots before higher-risk operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerli530](https://clawhub.ai/user/jokerli530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Self-Correct to add lightweight retry tagging, command-result verification, and snapshot routines around tool and shell workflows before higher-risk actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshot handling uses a shared /tmp location, which could expose copied files.

Mitigation: Use a private per-user snapshot directory with restrictive permissions before enabling the snapshot helper.

Risk: Recursive deletion in cleanup and batch removal flows can cause data loss if targets are wrong or retention behavior is unclear.

Mitigation: Validate and confirm deletion targets, make snapshot creation fail closed, and keep cleanup out of automatic heartbeat loops until retention policy is explicit.

## Reference(s):

- [Self-Correct on ClawHub](https://clawhub.ai/jokerli530/skills/self-correct)
- [jokerli530 publisher profile](https://clawhub.ai/user/jokerli530)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash code blocks and shell script snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes autonomous-only usage metadata and snapshot cleanup behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
