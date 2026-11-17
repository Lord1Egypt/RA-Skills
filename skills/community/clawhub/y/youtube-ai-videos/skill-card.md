## Description:

Fetch latest AI-related YouTube videos from curated channels using YouTube Data API v3 and filter by keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjohannp](https://clawhub.ai/user/mjohannp)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and OpenClaw users use this skill to fetch recent AI-related YouTube videos from configured channels and return a concise, keyword-filtered list of links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled channel-ID helper can fetch user-supplied non-YouTube URLs.

Mitigation: Use trusted YouTube handles or channel IDs, and validate HTTPS YouTube hostnames while rejecting local and private addresses before using that helper.

Risk: A YouTube API key stored in config.json is visible in plain text.

Mitigation: Store the key in YOUTUBE_API_KEY or the documented secrets file, and restrict it to YouTube Data API v3.

## Reference(s):

- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown list of filtered YouTube video links with timestamps, channel names, and matched-keyword emphasis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTube Data API v3 key; defaults to up to 15 videos from the last 3 days.]

## Skill Version(s):

1.0.1 (source: server release metadata and README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
