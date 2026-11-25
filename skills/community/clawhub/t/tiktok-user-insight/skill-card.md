## Description:

Retrieves public TikTok search results, creator posts, and video comments as structured JSON for audience and product opportunity research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, product teams, and researchers use the skill to retrieve public TikTok search results, creator posts, and video comments for audience research, competitor review, content planning, and product opportunity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and TikTok URLs are sent to the Guaikei service, and the API token is included with requests.

Mitigation: Submit only inputs approved for that service and keep GUAIKEI_API_TOKEN private.

Risk: Public comment text and usernames may still identify individuals when results are shared.

Mitigation: Keep analysis within its intended audience and redact usernames before external sharing.

Risk: The security evidence reports a benign verdict with medium confidence, but inspection was partial and some behavior was not fully assessed.

Mitigation: Review the skill and its runtime permissions before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-user-insight)
- [Guaikei service and token access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON response envelope containing TikTok search results, creator posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or later and GUAIKEI_API_TOKEN; returned data and request limits depend on the service plan.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
