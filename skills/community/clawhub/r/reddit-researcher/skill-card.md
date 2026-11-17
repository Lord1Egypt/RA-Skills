## Description:

Search and analyze Reddit posts and comments to summarize user opinions, troubleshoot issues, and track trends across communities and topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachgodsell93](https://clawhub.ai/user/zachgodsell93)

### License/Terms of Use:


## Use Case:

External users, developers, product teams, and researchers use this skill to gather Reddit discussions, inspect posts and comments, and summarize community sentiment, troubleshooting patterns, product feedback, and trend signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and optional OAuth credentials are sent to Reddit.

Mitigation: Use a dedicated Reddit app and account, protect REDDIT_CLIENT_SECRET and access tokens, and avoid exposing credentials in logs, prompts, or version control.

Risk: Outputs can include public usernames, comments, quotes, and other personal-data-adjacent content from Reddit.

Mitigation: Review summaries before sharing, avoid sensitive personal-data research without approval, and minimize quoted user content to what is necessary for the task.

Risk: High-volume API use can exceed Reddit rate limits or violate platform terms.

Mitigation: Respect Reddit rate limits and terms, use OAuth when appropriate, throttle requests, and back off on 429 responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zachgodsell93/skills/reddit-researcher)
- [Reddit Apps configuration](https://www.reddit.com/prefs/apps)
- [Reddit OAuth access token endpoint](https://www.reddit.com/api/v1/access_token)
- [Reddit web JSON API base](https://www.reddit.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research summaries with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public Reddit usernames, comments, post links, quotes, sentiment summaries, and counts of posts or comments analyzed.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
