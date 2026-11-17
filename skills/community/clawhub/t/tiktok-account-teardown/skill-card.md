## Description:

Retrieves public TikTok search results, creator posts, and video comments as structured data for account and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, researchers, and agent developers use this skill to review public TikTok content, compare accounts, and summarize engagement or comment patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was benign with medium confidence, but 12 of 32 components were only partially inspected and tool-misuse analysis was degraded.

Mitigation: Review the skill and its behavior before installation or execution; the benign verdict is not a guarantee of safety.

Risk: Queries send keywords or TikTok links to www.guaikei.com, and results can contain public account names and engagement data.

Mitigation: Use only public data you are authorized to analyze, and avoid sending sensitive search terms or links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-account-teardown)
- [GUAIKEI service and support](https://www.guaikei.com)
- [Options and parameters](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON results for TikTok search, creator posts, or video comments; the agent can summarize them in text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Array-based results; available fields and counts depend on the request and API plan.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
