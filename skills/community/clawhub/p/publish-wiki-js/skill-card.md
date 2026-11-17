## Description:

Publishes Markdown content to Wiki.js by preparing page metadata, cleaning frontmatter, and creating or updating pages through the Wiki.js GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hugogu](https://clawhub.ai/user/hugogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to publish new Wiki.js pages or update existing pages from Markdown content. It helps prepare page titles, paths, descriptions, tags, and API requests while preserving Markdown formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Wiki.js API token to read and change wiki content.

Mitigation: Use a Wiki.js token scoped to the minimum pages and actions needed, and avoid exposing WIKI_KEY in logs or shared outputs.

Risk: A misconfigured WIKI_URL could send content and credentials to an untrusted endpoint.

Mitigation: Configure WIKI_URL only to a trusted HTTPS Wiki.js GraphQL endpoint before running the skill.

Risk: Publishing to an existing path may update existing wiki content.

Mitigation: Verify the target path and page identity before publishing or updating content.

Risk: The examples and script use the zh locale unless changed.

Mitigation: Review and change the locale setting when publishing to a Wiki.js instance that uses a different locale.

## Reference(s):

- [Wiki.js GraphQL API Reference](references/wiki-js-api.md)
- [GraphQL Specification - String Type](https://spec.graphql.org/October2021/#sec-String)
- [Wiki.js API Documentation](https://docs.requarks.io/dev/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration values, and Wiki.js API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated Wiki.js API calls when WIKI_URL and WIKI_KEY are configured.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
