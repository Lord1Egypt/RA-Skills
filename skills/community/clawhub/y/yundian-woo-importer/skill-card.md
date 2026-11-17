## Description:

Import products from Shopify, Wix, WordPress, and Amazon directly into WooCommerce via natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colaliang](https://clawhub.ai/user/colaliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, store operators, and commerce teams use this skill to queue product imports from Shopify, Wix, WordPress, and Amazon into WooCommerce, then check import status by request ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill can modify WooCommerce catalog data on a live store.

Mitigation: Review source products and target-store behavior before bulk imports.

Risk: The skill handles a Yundian API key.

Mitigation: Use a narrowly scoped, revocable API key and avoid exposing it in prompts, logs, or shared configuration.

Risk: The MCP configuration can call an API URL and startup packages at runtime.

Mitigation: Keep the API URL set to the intended trusted HTTPS origin, pin dependencies, use a lockfile, and prefer a local installed tsx binary over npx -y.

## Reference(s):

- [Yundian+ Homepage](https://ydplus.net)
- [ClawHub Skill Page](https://clawhub.ai/colaliang/skills/yundian-woo-importer)

## Skill Output:

**Output Type(s):** [text, json, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YUNDIAN_WOO_IMPORTER_API_KEY plus node, npm, and npx.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
