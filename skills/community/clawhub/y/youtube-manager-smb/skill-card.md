## Description:

Comprehensive YouTube channel management with video publishing, data analytics, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chao980](https://clawhub.ai/user/chao980)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and social media managers use this skill to prepare YouTube video metadata, inspect channel and video performance data, and generate analytics reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload helper can return a success response from a mock path, which may mislead users about whether a video was actually published.

Mitigation: Treat upload output as a stub result unless a reviewed, authenticated YouTube publishing workflow is added and confirmed by the user.

Risk: The skill relies on YouTube API keys, OAuth client secrets, and refresh tokens for private data or account-changing workflows.

Mitigation: Store credentials in a protected secret manager, restrict OAuth scopes, and require explicit user confirmation before publishing or account-changing actions.

Risk: The skill description claims broad end-to-end YouTube automation that is not fully implemented by the artifact scripts.

Mitigation: Review capabilities before installation and rely only on verified analytics, reporting, and metadata preparation behavior.

## Reference(s):

- [YouTube Data API v3 Guide](references/youtube_api_guide.md)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helper scripts and JSON report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided YouTube API credentials and channel identifiers for API-backed workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; source skill frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
