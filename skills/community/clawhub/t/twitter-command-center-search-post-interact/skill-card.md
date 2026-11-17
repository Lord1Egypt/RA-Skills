## Description:

Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa for Twitter research, monitoring, or approved engagement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill to research X/Twitter profiles, tweets, trends, and conversations, then prepare or run OAuth-gated posting and engagement workflows with user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says normal command output may expose the user's API key.

Mitigation: Use a low-privilege AIsa key, avoid the status command, and treat command output as sensitive until the exposure is patched.

Risk: The security summary says sensitive account actions can run through a relay with weak destination controls.

Mitigation: Do not set TWITTER_RELAY_BASE_URL unless the endpoint is fully trusted, and require confirmation of exact posts and engagement actions before execution.

## Reference(s):

- [Twitter Engagement Workflow](references/engage_twitter.md)
- [Twitter OAuth Posting Workflow](references/post_twitter.md)
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/twitter-command-center-search-post-interact)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON command output with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; posting, follow, unfollow, like, and unlike actions should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
