## Description:

Manage X (Twitter) accounts to post tweets, like, reply, retweet, view timelines, search, auto-interact, and analyze data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage authorized X/Twitter accounts from an agent workflow, including posting, engagement actions, timeline and user retrieval, search, and keyword-based auto-replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable X/Twitter credentials may be stored in plaintext credential files.

Mitigation: Keep tokens outside the package or in a secure secret store, restrict credential file permissions, and rotate any exposed tokens.

Risk: Unchecked user-selected credential files can be used before public account actions.

Mitigation: Use only in a trusted single-user environment unless credential loading is hardened and user IDs are validated.

Risk: Posting, replying, liking, retweeting, or automation can create public account activity.

Mitigation: Require explicit confirmation before account-changing actions and before enabling automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/storyclaw-x-manager)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X/Twitter API credentials; account actions can create public posts, replies, likes, and retweets.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
