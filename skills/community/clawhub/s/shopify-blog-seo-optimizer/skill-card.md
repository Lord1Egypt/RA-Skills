## Description:

Audit a Shopify Article, research content and E-E-A-T gaps, generate a reviewable HTML candidate, and produce one audit-plus-storefront-preview report before any approved update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and operators use this skill to audit Shopify blog articles, research evidence-sensitive content gaps, preview proposed SEO and reading-experience changes, and apply approved body or summary updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved execution can edit live Shopify blog content.

Mitigation: Review before production installation, pin the source to a reviewed version, use least-privilege Shopify content scopes, and independently confirm the article ID plus proposed body or summary before executing an approved plan.

Risk: Credentials or broad Shopify permissions could expose store administration capability.

Mitigation: Keep skill-hub.env private and owner-readable only, avoid placing access tokens or client secrets in artifacts, and require explicit approval for missing scopes or permission updates.

Risk: SEO or E-E-A-T edits could add unsupported, misleading, or sensitive claims.

Mitigation: Use authoritative research sources, preserve uncertain claims for merchant review, require supplied evidence for experience or credentials, and avoid claims of rankings, traffic gains, or E-E-A-T passes.

Risk: Storefront previews can be inaccurate when the live storefront is blocked or password protected.

Mitigation: Label fallback previews clearly, avoid claiming a pixel-perfect theme match, and distinguish Admin HTML audit results from verified customer-facing storefront behavior.

Risk: Fetching article links or storefront pages could reach unsafe private destinations.

Mitigation: Use bounded public URL validation, reject credential-bearing URLs and private or local addresses, and record blocked or unavailable access states instead of bypassing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvsao/skills/shopify-blog-seo-optimizer)
- [Publisher profile](https://clawhub.ai/user/lvsao)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [Audit checklist](references/audit-checklist.md)
- [E-E-A-T audit methodology](references/eeat-methodology.md)
- [Onboarding guide](references/onboarding-guide.md)
- [Audit, candidate, and approval artifact contract](references/report-schema.md)
- [Storefront preview contract](references/storefront-preview.md)
- [Google helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Quality Evaluator Guidelines E-E-A-T update](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)
- [Google structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML]

**Output Format:** [Markdown guidance with shell commands, JSON audit and candidate artifacts, and a standalone HTML storefront preview report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shopify writes are limited to Article body and optional summary after explicit approval; dry-run apply and post-write verification are supported.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
