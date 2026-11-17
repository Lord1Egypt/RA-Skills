## Description:

Create Gemini Omni voice resources, character resources, and Flash Preview or multimodal text-to-video tasks through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or manage Gemini Omni audio voices, character resources, and video tasks through RunAPI. It supports one-off CLI execution and SDK-based application integration while preserving contract discovery, authentication, result validation, and recovery steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or using an untrusted RunAPI CLI package source could expose credentials or run unintended code.

Mitigation: Confirm the RunAPI publisher and CLI package source before installation or execution.

Risk: Prompts and media files submitted through the workflow may be sent to RunAPI and the underlying provider.

Mitigation: Use only prompts and media that are acceptable to share with RunAPI and the provider, and review applicable data handling terms.

Risk: Submitted tasks may consume paid API credits.

Mitigation: Confirm authentication, account, and billing context before submission; retry only when evidence shows no task was created and no billing occurred.

Risk: A successful task status may not guarantee that requested media deliverables are complete or valid.

Mitigation: Download every requested deliverable and verify non-empty files with the expected MIME type or media family before reporting completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-gemini-omni)
- [RunAPI Gemini Omni homepage](https://runapi.ai/models/gemini-omni)
- [Model overview, pricing, and rate limits](https://runapi.ai/models/gemini-omni.md)
- [Provider overview](https://runapi.ai/providers/google.md)
- [Full model catalog](https://runapi.ai/models.md)
- [Gemini Omni SDK integration](https://github.com/runapi-ai/gemini-omni-sdk)
- [Gemini Omni audio variant](https://runapi.ai/models/gemini-omni/audio.md)
- [Gemini Omni character variant](https://runapi.ai/models/gemini-omni/character.md)
- [Gemini Omni text-to-video variant](https://runapi.ai/models/gemini-omni/text-to-video.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce request JSON, task/result JSON, downloaded media files, SDK integration snippets, and validation notes depending on the user's task.]

## Skill Version(s):

0.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
