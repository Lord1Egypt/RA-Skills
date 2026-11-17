## Description:

Post content to social media via the Publer API for scheduling or publishing posts to TikTok, Instagram, Facebook, Twitter/X, or any Publer-supported platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imamark](https://clawhub.ai/user/imamark)

### License/Terms of Use:


## Use Case:

Developers and social media operators use this skill to upload media, schedule posts, publish TikTok carousels or videos, and check Publer job status from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload media and schedule or publish live content to connected social accounts.

Mitigation: Use --dry-run first and require explicit human approval before any upload, schedule, or publish command.

Risk: Publer workspace credentials are required for API access.

Mitigation: Do not store PUBLER_API_KEY in TOOLS.md or source control; use a least-privileged key and rotate it if exposed.

Risk: The security verdict requires review because safeguards around invocation scope and live posting are weak.

Mitigation: Install only for agents that should manage the target Publer workspace and review commands before execution.

## Reference(s):

- [Publer API Reference](references/api.md)
- [Publer API Base URL](https://app.publer.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/imamark/skills/publer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API payload or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PUBLER_API_KEY and PUBLER_WORKSPACE_ID; live upload, schedule, and publish actions should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
