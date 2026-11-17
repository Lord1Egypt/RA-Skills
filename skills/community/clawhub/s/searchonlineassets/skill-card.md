## Description:

Online asset search tool: queries public stock libraries (Pixabay) for high-quality photos, illustrations, vectors and videos, returning result metadata and URLs for use in the current workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to find public stock photos, illustrations, vectors, and videos from Pixabay and return concise metadata and asset URLs for the current workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or runs the external @dlazy/cli npm package.

Mitigation: Review the dLazy CLI source and npm package before use, and prefer the documented npx invocation when a persistent global install is not needed.

Risk: Asset search terms are sent to dLazy and Pixabay.

Mitigation: Avoid sending sensitive search terms or confidential project details through asset searches.

Risk: A dLazy API key may be stored in the user's local configuration directory.

Mitigation: Use per-invocation DLAZY_API_KEY for less persistence when appropriate, and rotate or revoke the key from the dLazy dashboard if exposure is suspected.

## Reference(s):

- [SearchOnlineAssets on ClawHub](https://clawhub.ai/dlazyai/skills/searchonlineassets)
- [dLazy CLI source](https://github.com/dlazyai/cli)
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON result metadata with asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns total count and hits with asset IDs, tags, preview, web-format and large image URLs, dimensions, and server-enforced safesearch.]

## Skill Version(s):

1.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
