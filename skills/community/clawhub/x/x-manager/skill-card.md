## Description:

Manage X (Twitter) accounts: post tweets, like, reply, retweet, view timeline, search, auto-interact, and analyze data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage X/Twitter accounts through agent-invoked scripts for posting, engagement, timeline retrieval, user tweet retrieval, and search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: X/Twitter credentials may permit posting, replying, liking, retweeting, and reading account data.

Mitigation: Use a dedicated low-privilege account or token where possible, store credentials outside source control with restricted file permissions, and rotate or revoke tokens if they may have been exposed.

Risk: Public posting and engagement actions can run without strong confirmation safeguards.

Mitigation: Require human approval before posting, replying, liking, retweeting, or enabling auto-interaction workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/x-manager)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON responses from helper scripts when actions are executed.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
