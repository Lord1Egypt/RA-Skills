## Description:

Plan a calendar, write, design pictures for, schedule, change, review, list, cancel and measure social media posts, including the person's own videos, plan, write and publish blog articles, and write marketing emails and product listings, through Skryvo's API with a Skryvo API key. Use in agents that run shell commands but have no Skryvo MCP connection (OpenClaw, Hermes, NanoClaw, Paperclip, Grok Bot, scripts) when the person asks to post or schedule for their brand, write a blog article, check what is scheduled, or see how posts performed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skryvo](https://clawhub.ai/user/skryvo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and brand operators use the skill in shell-capable agents to draft and manage brand marketing content, check performance, and publish approved content to connected channels through Skryvo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes that Google Ads copy generation and new-brand voice training extend beyond the skill's core described scope, and that scan evidence is incomplete.

Mitigation: Use those capabilities only when requested, and review the generated copy and brand setup before relying on them.

Risk: The skill can schedule or publish content to connected brand accounts.

Mitigation: Review the exact content, destination channels, and time before approving publication or scheduling.

Risk: The skill requires a Skryvo API key to access brand and publishing functions.

Mitigation: Store the key in the documented secret location and never print, log, or paste it into chat.

## Reference(s):

- [Skryvo API](https://api.skryvo.ai/api/v1/agent)
- [Skryvo API key settings](https://app.skryvo.ai/settings/agents)
- [Skryvo on ClawHub](https://clawhub.ai/skryvo/skills/skryvo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Content plans]

**Output Format:** [Social posts, articles, emails, ads, product listings, calendars, performance summaries, and generated images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is produced for the selected brand and channels; scheduling or publishing requires review and approval of the exact content, channels, and time.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
