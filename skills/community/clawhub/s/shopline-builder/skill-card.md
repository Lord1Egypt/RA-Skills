## Description: <br>
SHOPLINE store-building assistant that guides an agent through SHOPLINE registration, storefront setup, theme selection, payment and shipping configuration, and migration from Shopify, WooCommerce, or Shoplazza. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangsicong-debug](https://clawhub.ai/user/zhangsicong-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants and operators use this skill to have an agent assist with opening and configuring a SHOPLINE store, including onboarding forms, homepage setup, first-product setup, payment and shipping configuration, and data migration from supported commerce platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a live SHOPLINE admin session and make storefront, checkout, shipping, and migration changes. <br>
Mitigation: Run it only in an isolated browser session and require user approval of exact values before publishing or saving live changes. <br>
Risk: The security summary says the skill contradicts its browser-isolation promise. <br>
Mitigation: Stop execution if the agent attempts to attach to a personal browser profile or access unrelated tabs, cookies, or sessions. <br>
Risk: Migration and payment-related flows may involve platform secrets or credentials. <br>
Mitigation: Do not paste payment or platform secrets into chat; enter secrets directly in the relevant admin UI and revoke temporary migration credentials after use. <br>


## Reference(s): <br>
- [Shopline Builder npm package](https://www.npmjs.com/package/shopline-builder) <br>
- [Shopline Builder ClawHub listing](https://clawhub.ai/zhangsicong-debug/shopline-builder) <br>
- [Official links summary](references/links.md) <br>
- [Path A - new store setup flow](references/flow-newbie.md) <br>
- [Path B - migration flow](references/flow-migrate.md) <br>
- [Common FAQ](references/faq-common.md) <br>
- [SHOPLINE FAQ - English](references/faq-en.md) <br>
- [SHOPLINE FAQ - Chinese](references/faq-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with browser automation steps, inline code blocks, shell commands, and user-facing messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct browser actions that modify live SHOPLINE store settings and may prompt users to handle sensitive credentials outside chat.] <br>

## Skill Version(s): <br>
2.2.1 (source: frontmatter, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
