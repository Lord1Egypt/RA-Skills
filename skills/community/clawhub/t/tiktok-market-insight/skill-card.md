## Description:

Searches public TikTok videos, creator posts, and video comments by keyword or URL, returning structured JSON for market and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketing teams, and analysts use this skill to find public TikTok videos, review creator posts, and inspect comments for market research, competitor monitoring, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied security scan found no issues but rated confidence as medium because 12 of 32 components were only partially inspected and tool misuse analysis was degraded.

Mitigation: Review the referenced scripts before installation or use, send only public TikTok queries or URLs to the documented Guaikei API, and protect GUAIKEI_API_TOKEN.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-market-insight)
- [Guaikei service and token information](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [Release changelog](artifact/references/changelog.md)
- [Output envelope schema](artifact/assets/output_envelope.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON output envelope containing arrays of search results, creator posts, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty; the skill does not download video files.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
