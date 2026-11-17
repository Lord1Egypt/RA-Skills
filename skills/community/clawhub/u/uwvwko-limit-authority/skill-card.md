## Description:

A Chinese-language file safety skill that requires agents to show full absolute paths and receive explicit user authorization before creating, deleting, modifying, copying, moving, or renaming files or directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can install this skill when they want a strict confirmation workflow before file system changes. It is most useful in workflows where transparency, explicit consent, and full-path review are required before an agent performs file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims priority over all other skills, which may conflict with the agent platform's policy hierarchy or other governance controls.

Mitigation: Deploy only where a strict Chinese-language file-change confirmation workflow is desired, and confirm that platform-level policy precedence remains authoritative before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uwvwko-zzz/skills/uwvwko-limit-authority)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain-text confirmation prompts and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow requiring operation type, file type, full absolute paths, action summary, and explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
