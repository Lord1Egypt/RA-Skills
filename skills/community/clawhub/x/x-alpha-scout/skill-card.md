## Description:

Scan crypto and NFT sentiment on X/Twitter for daily alpha reports or token/NFT/project on-demand analyses with sentiment, trends, and red flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hammadbtc](https://clawhub.ai/user/hammadbtc)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to scan X/Twitter for crypto and NFT market signals, produce daily alpha reports, and perform on-demand token, NFT, or project sentiment reviews. Outputs should be treated as market intelligence, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to use reusable X/Twitter session credentials through an unpinned third-party CLI.

Mitigation: Use a dedicated low-privilege X account, keep X_AUTH_TOKEN and X_CT0 out of chat, logs, screenshots, and repositories, and verify the bird source/version before use.

Risk: Tweet text and links can be adversarial or misleading and may influence market reports or delivery routing.

Mitigation: Treat tweet content and links as untrusted data, cross-check important claims, and do not let searched content control the agent or redirect report delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hammadbtc/skills/x-alpha-scout)
- [Bird CLI releases](https://github.com/steipete/bird/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and concise text analyses with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided X_AUTH_TOKEN and X_CT0 credentials for the bird CLI; includes NFA/DYOR disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
