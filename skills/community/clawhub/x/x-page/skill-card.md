## Description:

X Twitter helps agents manage X/Twitter activity by constructing PowerShell-based X API calls for posting, replying, searching, liking, retweeting, and basic analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent operate an X/Twitter account through the X API, including creating posts, replies, engagement actions, lookups, timelines, media posts, and basic analytics checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored X/Twitter account credentials to make public account changes without built-in explicit confirmation guardrails.

Mitigation: Require explicit user confirmation before posts, deletes, follows, retweets, bookmarks, list changes, or other account-changing actions.

Risk: The credential file contains long-lived app and account secrets.

Mitigation: Use a dedicated X Developer app with minimum Read and Write permissions, protect the credentials file permissions, and rotate account tokens periodically or immediately after host compromise.

Risk: Media upload uses upload.twitter.com in addition to api.twitter.com.

Mitigation: Review and allow only the X/Twitter API and media upload endpoints needed for the requested action.

## Reference(s):

- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
- [X API v2 base URL](https://api.twitter.com/2)
- [X media upload endpoint](https://upload.twitter.com/1.1/media/upload.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell code blocks and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize API responses and should require explicit confirmation before account-changing actions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
