## Description:

Safe File Editor helps agents preview text file edits, create backups, commit changes, and roll back edits through a Python helper workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suda6632](https://clawhub.ai/user/suda6632)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to propose and apply simple text file edits with preview, backup, logging, and rollback support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised safety controls are not fully enforced, so the helper should not be treated as an authorization or confirmation boundary.

Mitigation: Require human review of each diff before applying changes and use the skill only as a convenience helper.

Risk: The implementation may mishandle sensitive or important files through confirmation, temporary-file, backup, metadata, or logging behavior.

Mitigation: Avoid using it on secrets, credentials, sensitive configuration, or critical files until those behaviors are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suda6632/skills/safe-file-editor)
- [Publisher profile](https://clawhub.ai/user/suda6632)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python API examples and structured edit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dry-run previews, backup paths, hash summaries, edit status messages, and rollback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
