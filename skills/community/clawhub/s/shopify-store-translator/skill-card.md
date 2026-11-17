## Description:

Translate Shopify store resources into a target language with preview-first review, market checks, approved writes, direct API translation, outdated translation audits, and Shopify CSV translation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants and their agents use this skill to check locale and market readiness, translate selected store resources, review audit CSVs, and write approved translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Shopify locale, market, and translation scopes can affect store-facing configuration and content.

Mitigation: Use the skill only with a Shopify store the user controls, prefer read-only or task-specific scopes where possible, and approve missing scopes explicitly before retrying.

Risk: Translation writes, locale publication, and market changes can alter live storefront behavior.

Mitigation: Review generated audit files and require clear approval before any locale publication, market change, or translation write.

Risk: Private Shopify connection values may expose store access if stored or shared unsafely.

Mitigation: Keep environment files and runtime credentials private with restrictive permissions, out of chat, logs, and source control.

Risk: Automatic updates or permission releases could broaden behavior without sufficient review.

Mitigation: Disable or manually review self-updates and require a clear approval step for permission-release workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvsao/skills/shopify-store-translator)
- [Publisher profile](https://clawhub.ai/user/lvsao)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [Connect Your Store](references/onboarding-guide.md)
- [Translation API Reference](references/translation-api.md)
- [Market & Language Setup Reference](references/market-lang-setup.md)
- [Shopify Store Translator Business Field Map](references/business-field-map.md)
- [Shopify translatable resources query](https://shopify.dev/docs/api/admin-graphql/latest/queries/translatableresources)
- [Shopify translationsRegister mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/translationsRegister)
- [Shopify TranslatableResourceType enum](https://shopify.dev/docs/api/admin-graphql/latest/enums/TranslatableResourceType)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, CSV files]

**Output Format:** [Markdown guidance with shell commands, JSON reports, and CSV or JSON translation review files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-first workflow; Shopify writes require explicit approval.]

## Skill Version(s):

2.1.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
