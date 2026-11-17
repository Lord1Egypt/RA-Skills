## Description:

Generate and edit images with GPT Image 2 through RunAPI. Use when the user asks an agent to create, edit, or transform images with GPT Image 2. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate, edit, or transform images with GPT Image 2 through RunAPI. The skill supports one-off CLI generation and SDK-oriented integration for applications, backends, workers, and pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RunAPI credentials may be exposed in shared workspaces.

Mitigation: Prefer environment authentication or saved CLI configuration, keep API keys out of shared files, and import user-provided tokens through stdin when needed.

Risk: The workflow can create paid API tasks.

Mitigation: Authenticate first, validate the request contract before submission, submit once, and retry only when evidence confirms that no task was created and no billing occurred.

Risk: Intermediate JSON files and generated images may contain sensitive task or output data.

Mitigation: Store results in an appropriate workspace, review outputs before sharing, and verify downloaded files are non-empty images with the expected MIME type.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/runapi-ai/skills/runapi-gpt-image-2)
- [RunAPI GPT Image 2 homepage](https://runapi.ai/models/gpt-image-2)
- [Model overview, pricing, and rate limits](https://runapi.ai/models/gpt-image-2.md)
- [Provider overview](https://runapi.ai/providers/openai.md)
- [Full model catalog](https://runapi.ai/models.md)
- [SDK integration](https://github.com/runapi-ai/gpt-image-2-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, JSON request and response files, and generated image files when tasks complete]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the RunAPI CLI and optional RUNAPI_API_KEY; generated media should be downloaded, checked for non-empty content, and verified against the expected image MIME type.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
