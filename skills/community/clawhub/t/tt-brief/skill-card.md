## Description:

Collects public TikTok keyword search results, creator posts, and video comments as structured JSON for reporting and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and marketing teams can collect public TikTok search results, creator posts, and video comments for daily briefs, performance reviews, trend tracking, competitor research, and weekly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence, but coverage is partial: 22 of 34 components were fully inspected and 12 were only partially interpreted, including referenced scripts.

Mitigation: Review the partially interpreted components and referenced scripts before installation; the scan guidance notes that a benign verdict does not guarantee risk-free behavior.

Risk: The API token and requested data are sent to the third-party GuaiKei service as part of data retrieval.

Mitigation: Use approved secret handling for GUAIKEI_API_TOKEN and confirm that sending the requested public TikTok data to this service fits your data-handling requirements.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/tt-brief)
- [GuaiKei TikTok data API documentation and service](https://www.guaikei.com)
- [Parameter and output field reference](artifact/references/options.md)
- [FAQ and environment setup](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON records for search results, creator posts, and comments; the agent can synthesize them into summaries and reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public TikTok data; requires Node.js 16.14+ and GUAIKEI_API_TOKEN. API usage may incur charges.]

## Skill Version(s):

1.1.3 (source: server-resolved release metadata, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
