## Description:

Fetches public TikTok videos, creator posts, and comments as structured JSON for sentiment, brand mention, and competitor research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Marketing, research, and communications teams can retrieve public TikTok search results, creator posts, and video comments for sentiment review, brand mention tracking, topic research, and competitor monitoring. An AI agent can analyze the returned records, but the skill itself is a data source rather than a sentiment classifier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and partial coverage; 12 of 34 components, including TikTok command scripts, were only partly inspected.

Mitigation: Review the partially inspected command scripts and their outbound requests before installing or using the skill.

Risk: Search terms and TikTok links are sent to the GuaiKei API service when a request runs.

Mitigation: Use only public TikTok queries and links, and keep GUAIKEI_API_TOKEN private in the process environment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/guaikei/skills/tt-watch)
- [Publisher profile](https://clawhub.ai/user/guaikei)
- [GuaiKei API service](https://www.guaikei.com)
- [Command options and output fields](references/options.md)
- [Setup and troubleshooting](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON envelope containing search results, creator posts, or video comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty. Calls require GUAIKEI_API_TOKEN; monthly plans limit search and creator-post requests to 30 records and comments to 40 records per call.]

## Skill Version(s):

1.1.3 (source: server release metadata and artifact frontmatter/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
