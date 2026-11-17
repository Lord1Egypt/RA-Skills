## Description:

Generate images, video, speech, music, 3D and LLM output with Wiro AI models through the Wiro MCP server or REST API, including finding a model, checking its price, running it and collecting the result. Use when the user wants generative media or LLM calls through an API, or mentions Wiro, wiro.ai or a Wiro API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Wiro AI models through MCP tools or HTTP APIs to find models, check prices, submit generation tasks, and collect generated media or LLM responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local MCP setup runs the unpinned @wiro-ai/wiro-mcp package.

Mitigation: Review the package and pin a version you have assessed before running it.

Risk: Prompts or conversation context sent through Wiro services may contain sensitive information.

Mitigation: Limit shared content to what the task needs and review Wiro's applicable data handling terms before sending sensitive material.

Risk: Hosted Wiro agents keep conversation memory and can connect to outside services.

Mitigation: Deploy a hosted agent only when needed, and review its memory, connected services, and plan before deployment.

## Reference(s):

- [Wiro AI ClawHub release](https://clawhub.ai/wiroai/skills/wiro-ai)
- [Wiro API introduction](https://wiro.ai/docs/introduction)
- [Authentication](https://wiro.ai/docs/authentication)
- [Run a model](https://wiro.ai/docs/run-a-model)
- [Wiro models catalog](https://wiro.ai/models)
- [Pricing](https://wiro.ai/docs/pricing)
- [Wiro MCP server](https://wiro.ai/docs/wiro-mcp-server)
- [LLM gateway](https://wiro.ai/docs/completions-api)

## Skill Output:

**Output Type(s):** [Images, Video, Audio and speech, 3D assets, Text]

**Output Format:** [Generated media files or text responses, with task results returned as structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected model and its parameters.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
