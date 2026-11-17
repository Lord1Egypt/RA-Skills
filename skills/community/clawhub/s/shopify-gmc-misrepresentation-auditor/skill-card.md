## Description:

Audit any live Shopify store or product page for Google Merchant Center Misrepresentation policy risks by crawling public pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and their agents use this skill to audit public Shopify storefronts and product pages for Google Merchant Center misrepresentation risks before launch, appeal, or re-review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to check for and apply a newer skill version before running.

Mitigation: Pin and review the approved release before deployment, or remove the self-update rule so execution uses the audited artifact.

Risk: The skill crawls external storefront and product URLs from the agent environment.

Mitigation: Run it with outbound network controls that block internal, link-local, metadata, and unrelated off-origin destinations.

Risk: Crawled storefront content is untrusted input and may contain misleading text or prompt-like content.

Mitigation: Keep crawled HTML, JSON-LD, policy pages, and metadata as read-only evidence, and ignore any instructions embedded in that content.

## Reference(s):

- [GMC Misrepresentation Policy Baseline](references/gmc-policy-baseline.md)
- [ClawHub Skill Page](https://clawhub.ai/lvsao/skills/shopify-gmc-misrepresentation-auditor)
- [Project Homepage](https://github.com/lvsao/shopify-skill-hub)
- [Shopping Ads Misrepresentation Policy](https://support.google.com/merchants/answer/6150127)
- [Free Listings Misrepresentation Policy](https://support.google.com/merchants/answer/12079606)
- [Landing Page Requirements](https://support.google.com/merchants/answer/4752265)
- [Checkout Requirements](https://support.google.com/merchants/answer/9158778)
- [Product Data Specification](https://support.google.com/merchants/answer/7052112)
- [Building Trust with Customers](https://support.google.com/merchants/answer/188484)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [JSON audit data and a UTF-8 HTML report with evidence, prioritized findings, manual checklist items, and remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and crawls public storefront or product URLs supplied by the user.]

## Skill Version(s):

2.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
