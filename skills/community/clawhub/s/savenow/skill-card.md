## Description:

Save durable notes from the current OpenClaw + Telegram conversation into today's memory/YYYY-MM-DD.md, with a semantic-dedupe preview/apply flow and inline Apply/Cancel buttons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chelebii](https://clawhub.ai/user/chelebii)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users on Telegram use this skill to extract durable decisions, fixes, preferences, and workflow rules from the current conversation and save them to a daily memory file after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local command execution can be risky when session identifiers, paths, or command arguments are not strictly controlled.

Mitigation: Review before installing, allow only trusted users to invoke explicit session keys, and require shell-free Node invocation with validated session and thread identifiers.

Risk: The auto mode can write persistent memory entries without the normal preview and confirmation step.

Mitigation: Prefer plain /savenow with Apply/Cancel for sensitive conversations and reserve /savenow auto for low-risk sessions.

Risk: A pending preview can become stale or differ from what the user intended to save.

Mitigation: Bind Apply to the reviewed entries snapshot or a verified digest, and reject expired or cross-topic pending previews.

## Reference(s):

- [savenow on ClawHub](https://clawhub.ai/chelebii/skills/savenow)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown preview text, JSON script output, and memory/YYYY-MM-DD.md updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode writes pending JSON only after candidate extraction; apply and auto modes can write persistent memory entries.]

## Skill Version(s):

0.1.1 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
