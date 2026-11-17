## Description:

Search and recommend real fashion products and brands across thousands of online stores via the Vistoya MCP for discovery, comparison, and shopping across clothing, shoes, bags, jewelry, and accessories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vistoya](https://clawhub.ai/user/vistoya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping-focused agents use this skill to search live fashion catalogs, compare product options, find similar products or brands, and return merchant links for purchase follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fashion search queries and product lookup requests are sent to Vistoya's public MCP service.

Mitigation: Avoid sending sensitive personal information in catalog searches; review queries before using the hosted service.

Risk: Merchant product links may send users to third-party stores outside the skill provider's control.

Mitigation: Review merchant pages, prices, availability, and store terms before purchase; the skill does not perform checkout or payments.

## Reference(s):

- [Vistoya MCP Tool Reference](references/tools.md)
- [Vistoya Workflow Patterns](references/workflows.md)
- [Vistoya homepage](https://vistoya.com)
- [ClawHub skill page](https://clawhub.ai/vistoya/skills/vistoya-fashion)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown summaries with product or brand details, prices, availability notes, and merchant links derived from JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No checkout, payment, order management, local file access, or credential handling is shown in the release evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
