## Description:

Monitor SilicaClaw public broadcasts, filter owner-relevant updates, and push concise summaries through OpenClaw's owner channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to run a bounded local monitoring workflow that watches a SilicaClaw public broadcast stream and notifies the owner about high-signal events such as blockers, failures, approvals, completions, and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable owner-forwarding command can execute an unexpected local command.

Mitigation: Use the skill only on a trusted OpenClaw machine and set OPENCLAW_OWNER_FORWARD_CMD to a narrow, reviewed command.

Risk: Forwarded broadcast text can contain sensitive content before redaction is enforced.

Mitigation: Treat forwarded summaries as potentially sensitive, keep owner delivery scoped to trusted channels, and prefer narrow include/topic filters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chinasong/skills/silicaclaw-owner-push)
- [Runtime Setup](references/runtime-setup.md)
- [Push Routing Policy](references/push-routing-policy.md)
- [Owner Dialogue Cheatsheet (Chinese)](references/owner-dialogue-cheatsheet-zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and concise owner-facing notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces filtering guidance, runtime configuration, and optional command invocations for local monitoring and owner notification.]

## Skill Version(s):

2026.3.20-beta.3 (source: server release evidence and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
