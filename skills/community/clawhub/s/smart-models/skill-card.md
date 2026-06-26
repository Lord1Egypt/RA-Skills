## Description: <br>
Intelligent multi-model router that selects an OpenAI-compatible model for vision, image generation, video generation, audio, reasoning, code, and general chat tasks, with @alias shortcuts for direct model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samstone908](https://clawhub.ai/user/samstone908) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route prompts and media tasks to configured external AI models through an OpenAI-compatible API. It supports automatic category selection, explicit @alias model selection, fallback within a category, and provider model discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, generated media requests, code, or documents may be sent to the configured external API provider. <br>
Mitigation: Use only approved OpenAI-compatible endpoints and avoid routing secrets, regulated data, private code, screenshots, or sensitive documents unless that provider is approved. <br>
Risk: Generated media and provider model-list outputs may be written under /tmp on the local machine. <br>
Mitigation: Review and remove temporary Smart Router output files when they may contain sensitive generated content or provider metadata. <br>


## Reference(s): <br>
- [ClawHub Smart Router release](https://clawhub.ai/samstone908/smart-models) <br>
- [samstone908 ClawHub profile](https://clawhub.ai/user/samstone908) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown or plain text responses, with shell commands and generated media URLs or local output paths when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured OpenAI-compatible provider credentials and may return external model responses, image URLs, async task results, or local /tmp file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
