## Description:

自动化短视频工作流（story-to-video pipeline）：从剧本/分镜到生成、字幕 ASR、TTS、合并交付，支持 Seedance / Vidu / MiniMax 多厂商路由。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wusyu](https://clawhub.ai/user/wusyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and production operators use this skill to convert story ideas, scripts, or storyboard materials into a controlled short-video pipeline with checkpoints, provider routing, subtitles, TTS, ambience, and final delivery tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and configured media through provider endpoints or gateways.

Mitigation: Use only trusted official provider endpoints or explicitly trusted gateways, keep API keys out of chat and shared logs, and rotate any key that may have been used with an untrusted configuration endpoint.

Risk: Configured prompts, images, audio, and video may leave the local machine during generation, ASR, TTS, or download workflows.

Mitigation: Confirm that the selected providers and endpoints are approved for the media being processed before submitting private or sensitive content.

Risk: Direct-run modes can spend provider quota or incur cost when they submit media generation jobs.

Mitigation: Review configuration before execution, avoid direct-run modes unless quota use is acceptable, and rely on diagnostic runs only as probes rather than final deliverables.

Risk: Under-scoped endpoint and download controls can route work or retrieved media through unexpected services.

Mitigation: Pin provider endpoints in configuration, prefer official endpoints, and review generated download URLs before treating retrieved media as trusted delivery output.

## Reference(s):

- [Pipeline Overview](references/pipeline-overview.md)
- [Configuration Template](references/configuration-template.md)
- [Model Routing](references/model-routing.md)
- [Runtime Policy](references/runtime-policy.md)
- [Output Contract](references/output-contract.md)
- [Failure Fallbacks](references/failure-fallbacks.md)
- [Audio Policy](references/audio-policy.md)
- [Seedance Prompt Engineering Overlay](references/seedance-prompt-engineering.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and configuration snippets, shell commands, and delivery manifest descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe raw, subtitled, voiced, final, or merged clip outputs and their formal/probe status.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
