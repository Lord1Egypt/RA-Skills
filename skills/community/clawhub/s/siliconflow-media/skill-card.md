## Description:

SiliconFlow multimodal media service for image generation with FLUX and Qwen models, video generation with Wan models, text-to-speech synthesis, and automatic speech recognition using voucher-based payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axdlee](https://clawhub.ai/user/axdlee)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to call SiliconFlow multimodal APIs from an agent workflow for image and video generation, speech synthesis, and speech-to-text transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media are sent to SiliconFlow using the user's SILICONFLOW_API_KEY.

Mitigation: Use only approved prompts and media, and avoid sensitive or regulated inputs unless the transfer to SiliconFlow has been approved.

Risk: The skill saves generated images, audio, and video files locally.

Mitigation: Run the skill in a constrained environment and review requested output paths before regular use.

Risk: Runtime dependencies are declared inline and no reviewed lockfile was provided in the evidence.

Mitigation: Pin dependencies or use a reviewed lockfile before sustained or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axdlee/skills/siliconflow-media)
- [Publisher profile](https://clawhub.ai/user/axdlee)
- [SiliconFlow image generation endpoint](https://api.siliconflow.cn/v1/images/generations)
- [SiliconFlow video generation endpoint](https://api.siliconflow.cn/v1/video/generations)
- [SiliconFlow text-to-speech endpoint](https://api.siliconflow.cn/v1/audio/speech)
- [SiliconFlow transcription endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; runtime outputs include generated media files and transcription text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SILICONFLOW_API_KEY. Media-producing scripts print MEDIA lines for generated image, audio, and video files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
