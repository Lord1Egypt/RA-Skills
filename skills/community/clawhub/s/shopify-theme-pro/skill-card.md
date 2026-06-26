## Description: <br>
Shopify Theme Development Pro supports Shopify theme development, deployment, and design system management for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avmw2025](https://clawhub.ai/user/avmw2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, review, optimize, and deploy Shopify Online Store 2.0 themes, Liquid templates, storefront sections, and theme design systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment guidance may expose a write-capable Shopify theme token if token checks print secret values. <br>
Mitigation: Use redacted existence checks for SHOPIFY_CLI_THEME_TOKEN and never print, log, or paste the token into agent-visible output. <br>
Risk: Shopify push or publish commands can change a customer-facing storefront. <br>
Mitigation: Verify the target store and theme ID, test on a development theme first, and require explicit approval before push, publish, or analytics changes go live. <br>
Risk: Pushing config/settings_data.json can overwrite merchant customizations. <br>
Mitigation: Ignore config/settings_data.json by default unless the operator explicitly intends to reset theme editor state. <br>


## Reference(s): <br>
- [Shopify Theme Pro on ClawHub](https://clawhub.ai/avmw2025/shopify-theme-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/avmw2025) <br>
- [Liquid Patterns](references/liquid-patterns.md) <br>
- [Theme Deployment](references/deployment.md) <br>
- [Design System](references/design-system.md) <br>
- [Performance Optimization](references/performance.md) <br>
- [Shopify Themes Documentation](https://shopify.dev/docs/themes) <br>
- [Shopify Liquid Reference](https://shopify.dev/docs/api/liquid) <br>
- [Shopify Theme Check](https://shopify.dev/docs/storefronts/themes/tools/theme-check) <br>
- [Shopify CLI](https://shopify.dev/docs/themes/tools/cli) <br>
- [Shopify Ajax API](https://shopify.dev/docs/api/ajax) <br>
- [Shopify Theme Best Practices](https://shopify.dev/docs/themes/best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Liquid, JSON, CSS, JavaScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Shopify CLI commands, Liquid templates, section schemas, theme settings, CSS design tokens, and deployment checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
