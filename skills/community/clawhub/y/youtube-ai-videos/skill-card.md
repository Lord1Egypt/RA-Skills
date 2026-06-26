## Description: <br>
Fetch latest AI-related YouTube videos from curated channels using YouTube Data API v3 and filter by keywords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjohannp](https://clawhub.ai/user/mjohannp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and OpenClaw users use this skill to fetch recent AI-related YouTube videos from configured channels and filter them by keywords, age, and result count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a YouTube Data API key and can expose the key if stored directly in config.json or a synced shell profile. <br>
Mitigation: Use a restricted YouTube Data API v3 key stored in ~/.openclaw/secrets/youtube_api_key.txt with tight file permissions, or provide it via YOUTUBE_API_KEY for the current shell session. <br>
Risk: The skill makes requests to Google and YouTube APIs and depends on external service availability, quotas, and configured channel data. <br>
Mitigation: Review the configured channels, keywords, and maxAgeDays before use, and monitor YouTube Data API quota usage when running the fetcher regularly. <br>


## Reference(s): <br>
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com) <br>
- [ClawHub skill page](https://clawhub.ai/mjohannp/youtube-ai-videos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown-style numbered list of YouTube video links with publication age, highlighted keyword matches, and channel names.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided YouTube Data API v3 key and uses configured channels, keywords, maximum video count, and maximum video age.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
