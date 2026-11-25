## Description:

Fetches public TikTok keyword search results, creator posts, and video comments as structured JSON for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

TikTok creators, marketers, researchers, and agent developers use the skill to retrieve public videos, creator posts, and comments for trend research, content benchmarking, and audience feedback analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign with medium confidence but partial: 12 of 34 components were only partially inspected, including executable scripts.

Mitigation: Review the partially inspected executable scripts and consider an additional security scan before installation.

Risk: The skill sends search terms or TikTok links and the API token to the Guaikei service to retrieve data.

Mitigation: Use only queries and public links that are appropriate to share with that service, and keep the API token private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/tt-teardown)
- [Guaikei TikTok data service](https://www.guaikei.com)
- [CLI options](references/options.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data; an agent can use it to produce summaries, comparison tables, and audience feedback analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public TikTok data; result counts depend on request limits and the account plan. Requires Node.js 16.14 or later and GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.1.3 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
