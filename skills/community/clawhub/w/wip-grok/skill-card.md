## Description:

xAI Grok API. Search the web, search X, generate images, generate video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search web and X content with xAI Grok, generate or edit images, and create short videos through CLI, module, MCP, or skill interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous or untrusted prompts could trigger MCP tool calls that use a paid xAI API key.

Mitigation: Review before installing in autonomous environments, use a dedicated API key, and limit the skill to trusted agents or workflows.

Risk: Image editing can read local file paths when a path is supplied as image input.

Mitigation: Do not pass sensitive local file paths to image-editing tools, and constrain or confirm local-file behavior before use in higher-trust environments.

Risk: Automatic 1Password lookup may use a credential source that was not intended for the current environment.

Mitigation: Prefer setting XAI_API_KEY explicitly for the deployment context and use a dedicated key with appropriate permissions.

## Reference(s):

- [Wip Grok on ClawHub](https://clawhub.ai/parkertoddbrooks/skills/wip-grok)
- [xAI Web Search documentation](https://docs.x.ai/developers/tools/web-search)
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Image Generation guide](https://docs.x.ai/docs/guides/image-generations)
- [xAI Video Generation guide](https://docs.x.ai/docs/guides/video-generations)
- [Attribution: Grok on ClawHub](https://clawhub.ai/castanley/grok)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, text search summaries, citations, and JSON media-generation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an xAI API key; generated media URLs are temporary and paid API usage may apply.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
