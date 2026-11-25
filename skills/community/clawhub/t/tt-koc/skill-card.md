## Description:

A read-only TikTok data skill that searches public videos, retrieves creator video lists, and collects video comments as structured JSON for creator research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

TikTok creators, agencies, brands, and research or growth teams can use the skill to find public videos, compare creator content and engagement, and summarize video comments for creator sourcing, competitor research, and topic discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports medium confidence because 12 of 34 components were only partially inspected.

Mitigation: Review the skill and its declared scope before installation; a benign scan result does not establish that the skill is risk-free.

Risk: Search terms and TikTok links are sent to the Guaikei data service, and API requests may incur usage charges.

Mitigation: Avoid sending sensitive terms or links, confirm external data sharing is appropriate, and use request limits that fit the account plan and budget.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-koc)
- [Guaikei TikTok data service](https://www.guaikei.com)
- [Options and output fields](artifact/references/options.md)
- [Frequently asked questions](artifact/references/faq.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON response envelope containing video search results, creator videos, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public TikTok data; results may include video, creator, engagement, or comment fields. API usage is subject to account plan limits and may incur charges.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
