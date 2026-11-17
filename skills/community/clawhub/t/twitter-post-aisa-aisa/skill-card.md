## Description:

Runs Twitter/X read, like, follow, reply, and OAuth-gated posting workflows through AIsa for confirmed accounts, tweets, or campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social media operators use this skill to research X/Twitter targets, request explicit engagement actions, and publish OAuth-approved posts or replies through AIsa without sharing passwords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AISA_API_KEY and the security evidence notes that authorize or post output may include the full key.

Mitigation: Run only in trusted environments, avoid sharing command output from authorize or post, and rotate any AISA_API_KEY exposed in logs.

Risk: Posting and media upload workflows send selected local media and Twitter/X action requests to AIsa and Twitter/X.

Mitigation: Only pass media files the user intentionally provided, and confirm the target account, tweet, or post content before invoking an action.

Risk: Likes, follows, replies, quotes, and posts can change public social account state.

Mitigation: Require explicit user approval for engagement and publishing actions, and do not report success until the API response confirms it.

## Reference(s):

- [AIsa Twitter OAuth](references/post_twitter.md)
- [AIsa Twitter Engagement](references/engage_twitter.md)
- [AIsa](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; posting and engagement actions depend on AIsa and Twitter/X API responses.]

## Skill Version(s):

1.0.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
