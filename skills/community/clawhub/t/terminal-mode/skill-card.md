## Description:

Terminal Mode lets an agent provide a Linux-like terminal experience for browsing and operating on workspace files with common commands such as cd, ls, cat, grep, find, cp, mv, rm, chmod, and touch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eraycc](https://clawhub.ai/user/eraycc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interact with an agent through familiar terminal-style commands for workspace file browsing and file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad file browsing, modification, copying, permission changes, and deletion.

Mitigation: Use it only in a constrained workspace and review requests involving absolute paths, ~ paths, recursive operations, rm -f, or rm -y before use.

Risk: Loose activation phrases may enter terminal mode unintentionally.

Mitigation: Require an explicit user request before activation and exit terminal mode when the user says exit or quit.

Risk: Delete operations can bypass confirmation when -f or -y is provided.

Mitigation: Treat forced, confirmed, or recursive delete requests as high-risk actions that require extra review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eraycc/skills/terminal-mode)
- [Publisher profile](https://clawhub.ai/user/eraycc)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal-style plain text with command prompts and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May browse, create, modify, move, copy, change permissions, or delete workspace files when commands request it.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
