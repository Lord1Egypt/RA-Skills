## Description:

Reveal a public Shopify store's theme and detectable apps without API access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and analysts use this skill to inspect public Shopify storefronts for visible theme details and detectable app technology. It supports tech-stack audits, competitor research, and evidence-backed reporting without Shopify API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to user-supplied storefront URLs.

Mitigation: Use only public storefront URLs you trust, avoid sensitive networks, and keep the scanner's private-address blocking enabled.

Risk: Generated HTML reports may contain values derived from scanned pages.

Mitigation: Treat reports as untrusted HTML and review escaping or sanitization before sharing or opening them in sensitive browser contexts.

Risk: Theme and app identification is based on public evidence and may be incomplete or ambiguous.

Mitigation: Keep ambiguous signals as clues, require evidence for confirmed findings, and verify app or theme candidates before relying on the report.

## Reference(s):

- [Detection Principles & Evidence Reference](references/detection-principles.md)
- [ClawHub Skill Page](https://clawhub.ai/lvsao/skills/shopify-theme-apps-detector)
- [Skill Homepage](https://github.com/lvsao/shopify-skill-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, JSON]

**Output Format:** [Markdown chat summary with shell commands, JSON scan evidence, and a generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; scans public HTTP/HTTPS storefront URLs and writes an HTML report in the current working directory.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
