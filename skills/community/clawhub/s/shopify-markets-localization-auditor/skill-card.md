## Description:

Audit Shopify international setup across Markets, languages, shipping coverage, storefront localization, international SEO basics, and category-fit expansion opportunities with a plain-language HTML report and approval-based fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants, ecommerce operators, and developers use this skill to audit international market readiness, language coverage, shipping coverage, storefront localization signals, and growth opportunities. The skill can also prepare approval-only fixes for supported locale and market-currency settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require broad Shopify store administration access for audits and supported fixes.

Mitigation: Use the smallest practical Shopify grant for the task, prefer read-only access for audits, and review requested scopes before connecting a store.

Risk: Long-running Shopify credentials increase exposure if they are stored or shared carelessly.

Mitigation: Use long-running credentials only when needed, keep secrets in private runtime configuration, and never paste tokens or client secrets into chat.

Risk: The security review flags generated HTML report handling as a concern.

Mitigation: Open generated reports only when the audit data is trusted, and review the report output before sharing it with others.

Risk: Approved fixes can change Shopify locale publication or local-currency settings.

Mitigation: Preview the fix bundle, get explicit approval, execute only supported actions, and verify changed locales or markets after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvsao/skills/shopify-markets-localization-auditor)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [API Surfaces](references/api-surfaces.md)
- [Audit Rules](references/audit-rules.md)
- [Business Research Method](references/business-research-method.md)
- [Onboarding Guide](references/onboarding-guide.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Plain-language guidance with shell commands, JSON audit and fix-plan files, and an HTML report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supported fixes are previewed first and executed only after approval.]

## Skill Version(s):

2.1.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
