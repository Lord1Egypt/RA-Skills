## Description:

Manage SocialConductor AI comment automation bots from chat apps across Facebook, Instagram, YouTube, and TikTok, including bot status, reply control, comment logs, leads, analytics, prompts, drafts, approvals, and account safety controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcecchino](https://clawhub.ai/user/dcecchino)

### License/Terms of Use:

MIT-0

## Use Case:

External social media account owners and administrators use this skill to manage SocialConductor automation bots from chat apps for Facebook, Instagram, YouTube, and TikTok. It supports setup, pausing or resuming automation, reviewing logs and leads, posting or regenerating replies, blocking users, analytics, prompts, drafts, approvals, and platform settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive commands can post replies, block or unblock users, enable automation, turn off simulation mode, approve drafts in bulk, or change settings on live social media accounts.

Mitigation: Install only for accounts you own or administer, keep simulation mode enabled during setup, review sensitive changes before execution, and use explicit platform-prefixed commands.

Risk: Ambiguous cross-platform commands may affect the wrong connected social account.

Mitigation: Use platform-prefixed commands for Facebook, YouTube, or TikTok when posting replies, blocking users, changing live settings, or approving content.

## Reference(s):

- [SocialConductor homepage](https://podium.socialconductor.ai)
- [Facebook and Instagram OpenClaw API base](https://podium.socialconductor.ai/api/openclaw/)
- [YouTube OpenClaw API base](https://studio.socialconductor.ai/api/openclaw/)
- [TikTok OpenClaw API base](https://violin.socialconductor.ai/api/openclaw/)
- [SocialConductor on the App Store](https://apps.apple.com/us/app/socialconductor/id6764723628)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with chat commands and API route references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may affect live social media accounts and should use explicit platform prefixes.]

## Skill Version(s):

1.7.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
