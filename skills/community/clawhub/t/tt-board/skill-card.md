## Description:

Searches public TikTok videos by keyword, retrieves creator posts and video comments, and returns structured JSON for ranking and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketing teams, and developers can use this skill to find popular TikTok videos, review public creator posts, and examine video comments for content research, competitor monitoring, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan found no AIG findings and marked the skill benign, but confidence is medium: 12 of 34 components were only partially inspected.

Mitigation: Review the partially inspected components before installation and consider the scan coverage gap when deciding whether to use the skill.

Risk: Search terms and TikTok links are sent to the Guaikei data service to retrieve results.

Mitigation: Avoid submitting sensitive information in search terms or links, and confirm the external data flow fits your use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-board)
- [Guaikei TikTok data service](https://www.guaikei.com)
- [Options and output fields](artifact/references/options.md)
- [FAQ and setup guidance](artifact/references/faq.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video search results, creator posts, or comments for the requested query; results may be empty and account plan limits apply.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
