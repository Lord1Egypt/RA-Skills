## Description:

Schedules and publishes social media posts through TryPost's hosted MCP server. Use when the user wants to draft, schedule, publish, preview, or analyze posts across Instagram, Facebook, LinkedIn, LinkedIn Page, X, TikTok, YouTube, Threads, Pinterest, Bluesky, Mastodon, Telegram, or Discord, or when they mention TryPost, social accounts, signatures, labels, webhooks, or repurpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trypost](https://clawhub.ai/user/trypost)

### License/Terms of Use:

MIT-0

## Use Case:

External social media teams and operators use this skill to draft, preview, schedule, publish, and analyze posts across connected TryPost social accounts. It also guides account, media, label, signature, webhook, API key, and repurpose workflows according to TryPost role permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule live social content across connected brand or client accounts.

Mitigation: Require explicit user confirmation before publishing or scheduling, and use preview checks before any live post action.

Risk: The skill can manage persistent workspace controls such as API keys, webhooks, social account toggles, and repurpose workflows.

Mitigation: Restrict these operations to intentional administrative requests and confirm before creating keys, changing webhooks, toggling accounts, or activating repurpose workflows.

## Reference(s):

- [TryPost AI Tools Reference](https://docs.trypost.it/ai/tools-reference)
- [TryPost App](https://app.trypost.it)
- [TryPost Site](https://trypost.it)
- [ClawHub Skill Page](https://clawhub.ai/trypost/skills/trypost)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Shell commands]

**Output Format:** [Markdown guidance with MCP tool calls and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TryPost OAuth authorization and an active TryPost Cloud plan for MCP use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
