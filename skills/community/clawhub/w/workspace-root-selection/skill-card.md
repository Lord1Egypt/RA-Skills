## Description:

Decide whether a directory can serve as an OpenClaw workspace root (external dir or Windows drive) and whether to migrate: official docs, filesystem measurement, and migration verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw administrators and developers use this skill to assess workspace directory compatibility, compare filesystem behavior, decide whether to keep or migrate a workspace, and follow verification steps for a migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because scanners report instructions to retry commands after execution-approval denials; the scan is partial and runtime permissions are unknown.

Mitigation: Review the approval-denial retry guidance and unresolved local references before installation, and keep execution permissions constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyunlai/skills/workspace-root-selection)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with recommendations, shell commands, and migration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actionable assessment with filesystem measurements and post-migration verification criteria.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
