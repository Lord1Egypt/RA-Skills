## Description:

Searches and analyzes tender and award notices, early-stage projects, company records, and procurement market data, with Guangdong as the default search region.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, sales, and market research users use the skill to find tender opportunities and analyze project, company, supplier, and pricing data. Guangdong is the default search region, while users can specify other regions.

### Deployment Geography for Use:

Global (Guangdong, China is the default search region)

## Known Risks and Mitigations:

Risk: Automatic signup sends a stable MAC-address hash that can link registrations to a device.

Mitigation: Use an existing API key or manual signup to avoid device fingerprinting; obtain consent before automatic signup.

Risk: Optional supplemental web searches share research terms with external services.

Mitigation: Keep confidential terms out of supplemental searches.

Risk: The available evidence does not establish how the provider retains or reuses submitted data.

Mitigation: Avoid submitting confidential or sensitive information.

Risk: Queries can consume service credits, and saved API keys or temporary login links grant account access.

Mitigation: Limit queries to the requested scope, check credit usage, and protect API keys and temporary links.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bailianai/skills/tender-guangdong)
- [Zhiliaobiaoxun service](https://ai.zhiliaobiaoxun.com/?ch=s150)
- [Tender search guide](artifact/references/api-search.md)
- [Company data guide](artifact/references/api-company.md)
- [Market analysis guide](artifact/references/api-market.md)
- [Business registry guide](artifact/references/api-registry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Text or Markdown summaries, tables, and analysis based on retrieved data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected query, available data, and account credits.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
