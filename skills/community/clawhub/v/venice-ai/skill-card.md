## Description:

Complete Venice AI platform access for text generation, vision/image analysis, web and X/Twitter search, embeddings, text-to-speech, speech-to-text, image generation, background removal, video creation, music generation, upscaling, and AI editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonisjongithub](https://clawhub.ai/user/jonisjongithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and external users use this skill to call Venice AI services from an agent workflow for multimodal generation, analysis, transcription, embeddings, search-enabled chat, and media processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied URLs can be fetched and their contents sent to Venice AI.

Mitigation: Do not pass internal, localhost, cloud metadata, or sensitive URLs; use sandboxing or network egress rules in shared or agent-autonomous environments.

Risk: Local or fetched media can be uploaded to Venice AI and, depending on selected model features, related model or search providers.

Mitigation: Use the skill only with data approved for those services, and review commands before execution when handling private files or secrets.

Risk: The security verdict recommends review before shared, enterprise, or autonomous-agent installation.

Mitigation: Perform operator review, scan the artifact before deployment, and restrict URL inputs where they are not required.

## Reference(s):

- [Venice AI API Reference](references/api.md)
- [Venice AI documentation](https://docs.venice.ai)
- [Venice AI homepage](https://venice.ai)
- [Venice AI status](https://veniceai-status.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, text or JSON API responses, and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and VENICE_API_KEY; generated images, video, audio, transcriptions, embeddings, and related outputs may be streamed or saved to user-specified paths.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
