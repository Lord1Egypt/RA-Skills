## Description:

Converts a section of a live website into a Shopify Liquid theme section using MiroMiro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soraiabarroso](https://clawhub.ai/user/soraiabarroso)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants and theme developers use this skill to turn a selected website section into a Liquid section and add it to a Shopify theme.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The target URL and requested section are sent to MiroMiro using the user's API key.

Mitigation: Confirm the URL and intended section before sending them, and keep the API key private.

Risk: Generated Liquid may need review, and saving it to a theme may overwrite an existing section.

Mitigation: Inspect the code and destination filename before saving; review the result before pushing or publishing the theme.

Risk: Copied text and images may belong to the source website.

Mitigation: Replace third-party copy, logos, and images with content the store is permitted to use before publishing.

## Reference(s):

- [MiroMiro website-to-Shopify-section API](https://miromiro.app/api/website-to-shopify-section-api)
- [MiroMiro API documentation](https://miromiro.app/api/docs)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Shopify Liquid section code with Markdown setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the generated code as a .liquid file in a local theme's sections directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
