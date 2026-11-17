## Description:

Find viral outlier posts on TikTok, Instagram and YouTube, pull creator stats, transcribe and analyse videos, build competitor watchlists, and crawl profiles on demand. Prepaid credits, MCP or REST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matsclaes2](https://clawhub.ai/user/matsclaes2)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and social media teams use this skill to find unusually high-performing posts and creators across TikTok, Instagram, and YouTube, compare profiles, monitor competitors, and develop content ideas from public posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI example runs `npx viral-outliers` without pinning a package version, so a later install may execute a changed release. Scanner coverage was partial.

Mitigation: Review the package and use an explicitly reviewed, version-pinned release with integrity checks. Do not pass a real API key to code that has not been reviewed.

## Reference(s):

- [Viral Outliers documentation](https://viraloutliers.com/docs)
- [Getting started](https://viraloutliers.com/docs/getting-started)
- [REST API reference (OpenAPI)](https://viraloutliers.com/openapi.json)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured API data with textual analysis and content guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some operations return asynchronous job references; billable operations use prepaid credits.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
