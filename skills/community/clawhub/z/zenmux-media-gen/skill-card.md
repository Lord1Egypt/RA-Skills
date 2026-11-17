## Description:

Generate images & videos with ZenMux. Support multiple image models (Gemini, Qwen, Hunyuan, etc.) and video models (Veo, Seedance) via one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theopenbase](https://clawhub.ai/user/theopenbase)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to generate images and videos through ZenMux's unified API, including model selection, task creation, polling, and optional media download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference image URLs, and the ZenMux API key are sent to ZenMux APIs.

Mitigation: Use the skill only when you trust ZenMux, store the API key in an environment variable, and run it from an environment with restricted network egress where practical.

Risk: API-returned download URLs are trusted and remote media can be saved locally without size or content validation.

Mitigation: Use limited disk space and review automatic downloads until URL allowlisting, streaming size limits, and content validation are added.

## Reference(s):

- [ZenMux Homepage](https://zenmux.ai)
- [ZenMux API Base URL](https://api.zenmux.ai/v1)
- [ClawHub Skill Page](https://clawhub.ai/theopenbase/skills/zenmux-media-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash examples, Python CLI commands, JSON API responses, and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZENMUX_API_KEY and network access to ZenMux APIs; generated media may be saved to local output paths.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
