## Description:

Super Admapix helps agents search ad creatives, analyze apps, explore rankings, track download and revenue estimates, and produce market intelligence through the AdMapix API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing analysts use this skill to query AdMapix ad intelligence, app ranking, download, revenue, distribution, and market data from natural-language prompts. It can return quick search summaries or route complex comparisons and strategy questions to hosted deep research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AdMapix API keys may be stored in OpenClaw configuration or forwarded to hosted AdMapix services.

Mitigation: Use a scoped or revocable API key, avoid pasting secrets into chat, and rotate the key if it is exposed.

Risk: Complex queries and conversation context may be processed by AdMapix-hosted deep research.

Mitigation: Avoid confidential strategy prompts or sensitive business data unless the service's data handling is acceptable.

Risk: Deep research can return externally hosted, shareable report links.

Mitigation: Review report contents and access expectations before sharing links outside the intended audience.

Risk: The security summary flags unsafe shell-command patterns around setup and execution.

Mitigation: Review commands before execution, prefer a pinned installer or release, and install only if the security posture is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-admapix)
- [AdMapix Website](https://www.admapix.com)
- [Creative Search API](references/api-creative.md)
- [Product & Company API](references/api-product.md)
- [Ranking API](references/api-ranking.md)
- [Download & Revenue API](references/api-download-revenue.md)
- [App Distribution API](references/api-distribution.md)
- [Market Analysis API](references/api-market.md)
- [Parameter Mapping Reference](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with API-derived summaries, tables, links, and shell command snippets; complex analyses may include hosted HTML report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ADMAPIX_API_KEY. Download and revenue figures are third-party estimates. Deep research reports may be externally hosted and shareable by link.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
