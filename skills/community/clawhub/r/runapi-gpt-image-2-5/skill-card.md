## Description:

Generate and edit images with GPT Image 2.5 through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate, edit, or transform image deliverables through RunAPI, choosing the CLI for one-off work and SDK references for application or backend integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party RunAPI CLI and Homebrew tap that may handle selected local media files and RunAPI credentials.

Mitigation: Use a narrowly scoped API key, avoid exposing unrelated secrets, and pin or verify the CLI release in stricter environments.

Risk: A malformed request or contract mismatch could submit an unintended remote image task.

Mitigation: Inspect the installed CLI help and current API reference before execution, validate request JSON, submit exactly once, and stop on unresolved contract mismatches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-gpt-image-2-5)
- [RunAPI GPT Image 2.5 homepage](https://runapi.ai/models/gpt-image-2.5)
- [RunAPI GPT Image 2.5 model documentation](https://runapi.ai/models/gpt-image-2.5.md)
- [RunAPI OpenAI provider overview](https://runapi.ai/providers/openai.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI GPT Image 2.5 SDK integration](https://github.com/runapi-ai/gpt-image-2.5-sdk)
- [RunAPI GPT Image 2.5 Flare variant](https://runapi.ai/models/gpt-image-2.5/flare.md)
- [RunAPI GPT Image 2.5 Sunburst variant](https://runapi.ai/models/gpt-image-2.5/sunburst.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown instructions with shell command snippets and JSON request and response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded image files after successful RunAPI task completion.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
