## Description:

Shopify Theme Pro helps agents build, refactor, optimize, and deploy Shopify themes using Liquid, Online Store 2.0 patterns, Shopify CLI workflows, and design system guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avmw2025](https://clawhub.ai/user/avmw2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents supporting Shopify merchants use this skill to create Liquid templates, manage Online Store 2.0 theme architecture, optimize performance and accessibility, and prepare theme deployments. It is also useful for maintaining theme design systems and reviewing Shopify theme code before store pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment commands can expose write-capable Shopify theme tokens if environment files or command output are handled carelessly.

Mitigation: Do not print `.env.local` token values and review deployment steps before allowing an agent to execute them.

Risk: Pushing or publishing a live Shopify theme can immediately affect customer-facing storefront pages.

Mitigation: Require explicit approval before any live `theme push` or `theme publish`, and prefer tested development-theme deployments first.

Risk: Mutable project-controlled commands or npm tooling can change deployment behavior.

Mitigation: Prefer direct, reviewed Shopify CLI commands and pin or preinstall npm tooling in a controlled environment.

## Reference(s):

- [Shopify Theme Deployment](artifact/references/deployment.md)
- [Design System for Shopify Themes](artifact/references/design-system.md)
- [Liquid Patterns Reference](artifact/references/liquid-patterns.md)
- [Shopify Theme Performance Optimization](artifact/references/performance.md)
- [Shopify Theme Documentation](https://shopify.dev/docs/themes)
- [Shopify Liquid Reference](https://shopify.dev/docs/api/liquid)
- [Shopify Theme Check](https://shopify.dev/docs/storefronts/themes/tools/theme-check)
- [Shopify CLI Reference](https://shopify.dev/docs/themes/tools/cli)
- [Shopify Ajax API](https://shopify.dev/docs/api/ajax)
- [Shopify Theme Best Practices](https://shopify.dev/docs/themes/best-practices)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Liquid, JSON, CSS, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment checklists and review prompts before live Shopify pushes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
