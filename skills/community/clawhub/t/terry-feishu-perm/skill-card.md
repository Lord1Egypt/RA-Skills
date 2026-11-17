## Description:

Guidance-only playbook for planning and reviewing Feishu document and folder permission management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace administrators use this skill to plan least-privilege Feishu document, folder, and workspace sharing, audit existing access, and produce repeatable access review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Permission guidance could recommend broad access, external sharing, or elevated privileges that are inappropriate for a specific document.

Mitigation: Have a document owner verify full-access, external-sharing, and expiration recommendations before applying changes in Feishu.

Risk: The skill provides advisory output only and cannot confirm the live state of Feishu collaborators or inherited folder permissions.

Mitigation: Compare the recommendation against current Feishu access settings and keep an audit trail of who received access, why, and when.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terry-feishu-perm)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with permission matrices, risk findings, and remediation plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only output; does not execute Feishu changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
