## Description:

Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa for approved account, tweet, and campaign workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Twitter/X context, request explicit engagement actions, and publish approved posts or replies through AIsa without sharing passwords or browser credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that normal authorize or post commands can expose the full AISA API key in terminal output, agent transcripts, or logs.

Mitigation: Review command output before sharing logs, avoid retaining transcripts that include secrets, and rotate any AISA_API_KEY that may have been exposed.

Risk: The skill sends post content, attached media, and Twitter/X engagement requests to AIsa's relay service.

Mitigation: Install only when the user trusts AIsa with those actions and confirm target accounts, tweets, media, and post text before execution.

## Reference(s):

- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa Twitter OAuth](references/post_twitter.md)
- [AIsa](https://aisa.one)
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/twitter-post-aisa-aisa-one)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return authorization links, Twitter/X action status, tweet links or IDs, and API error details.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
