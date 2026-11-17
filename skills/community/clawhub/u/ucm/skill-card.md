## Description:

Provides API marketplace access for AI agents to discover and call external capabilities such as web search, image generation, code execution, text-to-speech, translation, financial data, weather, reference data, and document conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucmai](https://clawhub.ai/user/ucmai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill when an agent needs marketplace discovery and HTTP access to external API capabilities that are not available natively. It is suited for tasks that may require paid calls, credential handling, and data exchange with UCM and upstream service providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a paid-service bearer key and may expose credentials through transcripts, command output, logs, or permissive local credential storage.

Mitigation: Avoid printing or pasting full API keys, store ~/.config/ucm/credentials.json with restrictive permissions, keep UCM_API_KEY out of logs, and rotate any key that has been exposed.

Risk: The skill can send task data to UCM and upstream providers and can make paid calls without a separate built-in spending gate.

Mitigation: Use it only when external data sharing and small paid calls are acceptable; check balance and service details before calling paid endpoints.

## Reference(s):

- [UCM Skill on ClawHub](https://clawhub.ai/ucmai/skills/ucm)
- [UCM Publisher Profile](https://clawhub.ai/user/ucmai)
- [UCM Website](https://ucm.ai)
- [UCM Repository](https://github.com/ucmai/skills)
- [Service Catalog](references/service-catalog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples; service calls may return service-specific text, JSON, code, markdown, or generated asset references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, curl or an HTTP client, and UCM_API_KEY for authenticated paid service calls.]

## Skill Version(s):

1.1.1 (source: target metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
