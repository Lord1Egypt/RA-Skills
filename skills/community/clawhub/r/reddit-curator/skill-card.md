## Description:

Curates and summarizes top Reddit posts from selected subreddits into a daily digest delivered through configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoffguides](https://clawhub.ai/user/geoffguides)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Reddit digests, filter subreddit content by engagement or keywords, summarize selected posts, and deliver the results by Telegram, email, or Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation shows Reddit client secrets, usernames, and passwords in a plain JSON configuration while also claiming credentials are encrypted.

Mitigation: Use environment-backed secrets or OAuth tokens, restrict local file permissions, keep credential files out of version control, and rotate any credentials that were stored or shared in plaintext.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geoffguides/skills/reddit-curator)
- [ClawHub publisher profile](https://clawhub.ai/user/geoffguides)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown digest with configuration examples and delivery instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include subreddit lists, filter settings, post summaries, links, and delivery-channel formatting.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
