## Description:

Multi search engine integration with 17 engines (8 CN + 9 Global), advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dnaxxx-hub](https://clawhub.ai/user/dnaxxx-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to construct web search requests across Chinese and international search engines, apply advanced operators and time filters, and route knowledge-style queries to WolframAlpha without API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be sent to external engines that log or process queries under their own policies.

Mitigation: Avoid secrets, private project names, personal data, and credentials in search queries; use privacy-oriented engines when the query itself is sensitive.

Risk: Advanced search examples can surface outdated, misleading, or sensitive public content.

Mitigation: Cross-check important findings across multiple sources and use advanced operators responsibly before acting on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dnaxxx-hub/skills/ultimate-search-engine)
- [International Search Guide](references/international-search.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls]

**Output Format:** [Markdown with inline JavaScript web_fetch examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; generated searches send query text to external search providers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
