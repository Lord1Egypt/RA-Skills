## Description:

SHOPLINE store-building assistant that helps users register and configure a SHOPLINE independent store, including registration forms, basic store settings, theme setup, and migration guidance from Shopify, WooCommerce, or Shoplazza.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangsicong-debug](https://clawhub.ai/user/zhangsicong-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and ecommerce operators use this skill to set up a SHOPLINE store, configure storefront basics, add initial products, prepare payments and shipping, and receive migration guidance from supported commerce platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive store credentials, API tokens, or payment keys could be exposed if entered into chat or untrusted pages.

Mitigation: Enter credentials only in verified first-party or trusted app pages, avoid pasting secrets into chat, and revoke temporary keys after use.

Risk: Live store changes could affect products, prices, images, payment, shipping, app installation, or migration state.

Mitigation: Require explicit user approval before applying each material store change and review changes before publication or migration.

Risk: Using a personal browser profile could expose unrelated tabs, cookies, or account sessions.

Mitigation: Use an isolated browser session for execution and avoid granting access to a personal browser profile.

## Reference(s):

- [Shopline Builder package homepage](https://www.npmjs.com/package/shopline-builder)
- [SHOPLINE Help Center FAQ - English](references/faq-en.md)
- [SHOPLINE Help Center FAQ - Chinese](references/faq-zh.md)
- [Common FAQ](references/faq-common.md)
- [New store setup flow](references/flow-newbie.md)
- [Migration flow](references/flow-migrate.md)
- [Official links summary](references/links.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured instructions and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation steps, user confirmation prompts, setup checklists, and configuration guidance.]

## Skill Version(s):

2.2.1 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
