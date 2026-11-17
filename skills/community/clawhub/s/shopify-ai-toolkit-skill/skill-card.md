## Description:

Search Shopify developer docs and validate GraphQL, Liquid, Hydrogen, and other Shopify code for app, theme, or storefront development tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jtcchan](https://clawhub.ai/user/jtcchan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when building Shopify apps, themes, storefronts, functions, customer account flows, and admin extensions. It guides the agent to search Shopify documentation, generate code, and validate supported GraphQL, Liquid, Hydrogen, and related Shopify outputs before returning them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default telemetry can send validation inputs, searches, filenames, paths, metadata, and submitted code outside the local environment.

Mitigation: Review the skill before installation and set OPT_OUT_INSTRUMENTATION=true before use when working with proprietary or sensitive Shopify code.

Risk: The optional Shopify Dev MCP setup uses an npx command that resolves a package at runtime.

Mitigation: Prefer pinned, reviewed dependencies and run optional MCP tooling only after confirming the package source and version.

## Reference(s):

- [Shopify Developer Documentation](https://shopify.dev/)
- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [Shopify Storefront API](https://shopify.dev/docs/api/storefront)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Shopify documentation search results, validation feedback, and generated Shopify code or configuration guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
