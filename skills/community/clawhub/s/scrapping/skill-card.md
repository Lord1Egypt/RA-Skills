## Description:

Guides agents through retrieving public social-media data with the ScrapeCreators REST API, including profiles, posts, comments, transcripts, ad library data, and creator metrics across major platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berthelol](https://clawhub.ai/user/berthelol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to choose ScrapeCreators endpoints and compose authenticated curl and jq workflows for public social-media research. It supports lookups across profiles, posts, comments, transcripts, ads, search, trends, and creator metrics while keeping API keys in environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches, profile handles, post URLs, content IDs, filters, and similar lookup terms are sent to ScrapeCreators with the user's API key.

Mitigation: Use the skill for public, non-sensitive research and keep the API key in SCRAPECREATORS_API_KEY rather than embedding it in scripts, files, or chat history.

Risk: Saved JSON or CSV outputs may retain scraped personal or business data locally.

Mitigation: Collect only the pages and fields needed, prefer trim=true or jq extraction where appropriate, and handle saved outputs according to the user's retention and access requirements.

## Reference(s):

- [ScrapeCreators API Docs](https://docs.scrapecreators.com)
- [ScrapeCreators](https://scrapecreators.com)
- [Facebook API Endpoints](references/facebook.md)
- [Instagram API Endpoints](references/instagram.md)
- [LinkedIn API Endpoints](references/linkedin.md)
- [Other Platform Endpoints](references/other-platforms.md)
- [Reddit API Endpoints](references/reddit.md)
- [TikTok API Endpoints](references/tiktok.md)
- [Twitter/X API Endpoints](references/twitter.md)
- [YouTube API Endpoints](references/youtube.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, curl, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples, pagination guidance, jq filters, and JSON or CSV output handling.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
