## Description:

so-me.studio is a multi-platform social-media scheduler. Schedule posts, manage drafts, reply to inbox messages and post comments, generate AI captions/images/UGC videos, query analytics, manage media files and biolinks, and react to webhooks across Twitter/X, LinkedIn, LinkedIn Page, Instagram, Facebook, TikTok, YouTube, Threads, WhatsApp, Pinterest, Dribbble.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yasin047](https://clawhub.ai/user/yasin047)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social-media operators use this skill to direct an agent through authenticated so-me.studio CLI workflows for scheduling posts, managing drafts, replying to inbox messages and comments, generating content, querying analytics, managing media and biolinks, and handling webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform real social-media actions, including posting, messaging, deleting content, and changing workspace resources.

Mitigation: Use a low-privilege workspace or API key where possible, review posts and replies before they are sent, and prefer drafts when intent is ambiguous.

Risk: The skill exposes account-administration workflows such as team, tenant, webhook, and API-key management.

Mitigation: Avoid allowing the agent to create API keys, webhooks, tenants, or team changes unless explicitly requested, and monitor those settings after use.

Risk: Authenticated operation depends on SOMESTUDIO_API_KEY or saved CLI credentials.

Mitigation: Never echo or disclose the API key, rotate credentials if exposed, and revoke access that is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yasin047/skills/so-me-studio)
- [so-me.studio Documentation](https://docs.so-me.studio)
- [so-me.studio CLI on npm](https://www.npmjs.com/package/@so-me/cli)
- [so-me.studio Website](https://so-me.studio)
- [Webhook Payloads](https://docs.so-me.studio/webhooks/payloads)
- [MCP Overview](https://docs.so-me.studio/mcp/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated so-me.studio access through SOMESTUDIO_API_KEY or CLI login.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
