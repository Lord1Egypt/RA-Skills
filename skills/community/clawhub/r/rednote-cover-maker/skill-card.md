## Description:

Turns a photo, topic idea, or accepted draft into a vertical 3:4 REDnote (Xiaohongshu) cover or post image with clean backgrounds, focal composition, and text-safe areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketers use this skill to plan and generate one Xiaohongshu/REDnote cover image from a source photo, concrete topic, or accepted draft, then review the resulting artifact and billing details before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad Beatra account permissions through a shared Beatra token that can access more than image-cover generation.

Mitigation: Review the Beatra approval scope before authorizing, keep the credential private, and revoke the device from the Beatra Console when the skill is no longer trusted or needed.

Risk: Automatic package updates are enabled by default, so package code can change without a separate approval prompt.

Mitigation: Disable automatic updates with `python3 scripts/mcp_client.py update --auto off` when review-gated changes are required, and rely on the documented checksum and rollback controls for accepted updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/rednote-cover-maker)
- [REDnote Cover Maker homepage](https://beatra.ai/skills/rednote-cover-maker)
- [Cover routing](references/cover-routing.md)
- [Cover craft](references/cover-craft.md)
- [Workflow](references/workflow.md)
- [Review and recovery](references/review-and-recovery.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Installation and authentication](references/installation-and-auth.md)
- [MCP connection](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API calls]

**Output Format:** [Markdown guidance with inline shell commands, JSON tool arguments, task details, billing details, and generated image artifact links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to one vertical 3:4 cover image per approved request and reports task ID plus billing.net_charged_credits.]

## Skill Version(s):

0.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
