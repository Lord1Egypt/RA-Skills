## Description:

A skill for sending notifications via WeChat Work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yc-weichao](https://clawhub.ai/user/yc-weichao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send text, image-linked, and Markdown notifications to WeChat Work group chats from agent workflows or OpenClaw CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs can expose sensitive credentials if logs or command outputs are visible to other users.

Mitigation: Use secret-managed or placeholder webhook values, avoid sharing command logs, and rotate any webhook that may already have appeared in logs.

Risk: Caller-supplied webhook URLs can make the skill act as a general network request proxy from the host.

Mitigation: Restrict allowed webhook hosts or configure a fixed trusted webhook before use outside a trusted, single-user context.

Risk: The skill depends on the package manager resolving an unpinned axios version range.

Mitigation: Pin dependencies before deployment and review dependency updates as part of release intake.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yc-weichao/skills/qywx-notify)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Text]

**Output Format:** [JSON status objects and WeChat Work text or Markdown message payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked webhook values; user-supplied content can be sent to configured webhook endpoints.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, and index.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
