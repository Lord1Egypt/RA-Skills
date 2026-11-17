## Description:

Fetch and display the top trending YouTube videos globally or by country/category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunovu20](https://clawhub.ai/user/brunovu20)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current YouTube trending video lists by global chart, country, result count, or category, then present the returned ranking and video metadata to a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a user-provided YouTube Data API key, and persistent shell profile configuration can expose that key to future terminal sessions.

Mitigation: Use a restricted Google API key limited to the YouTube Data API, keep normal key hygiene, and only persist the environment variable in trusted environments.

Risk: API requests may fail if the key is invalid, the quota is exhausted, or the network request fails.

Mitigation: Handle the documented API and network error messages, and ask the user to verify the key, quota, and connection before retrying.

Risk: Trending results are live API data and may be unavailable, localized, or biased by YouTube's default ranking behavior.

Mitigation: Present results as API-returned current rankings, include the requested region or global setting, and avoid fabricating titles, counts, or rankings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brunovu20/skills/youtube-trending)
- [Google Cloud Console](https://console.cloud.google.com/)
- [YouTube Data API v3 videos endpoint](https://www.googleapis.com/youtube/v3/videos)
- [YouTube Data API most popular chart endpoint](https://www.googleapis.com/youtube/v3/videos?chart=mostPopular)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with inline shell commands and YouTube links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a user-provided YOUTUBE_API_KEY; fetches at most 50 videos per request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
