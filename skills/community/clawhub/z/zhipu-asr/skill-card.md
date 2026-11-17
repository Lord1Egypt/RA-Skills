## Description:

Automatic Speech Recognition (ASR) using Zhipu AI (BigModel) GLM-ASR model. Use when you need to transcribe audio files to text. Supports Chinese audio transcription with context prompts, custom hotwords, and multiple audio formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to transcribe short Chinese audio files through Zhipu AI's GLM-ASR model, with optional context prompts and hotwords to improve recognition. It is suitable for meeting snippets, lectures, voice memos, subtitles, and call recording transcription within the documented file limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files, prompt text, and hotwords are sent to Zhipu AI for transcription.

Mitigation: Use only recordings and context that are approved for sharing with Zhipu AI; avoid confidential or regulated audio unless authorization and data handling requirements are satisfied.

Risk: The ZHIPU_API_KEY may be briefly visible in local curl process arguments.

Mitigation: Prefer a hardened execution path that passes the API key through a protected curl configuration or equivalent secret handling mechanism instead of command-line arguments.

Risk: Inputs outside the documented audio limits may fail or need preprocessing.

Mitigation: Keep audio requests within the 25 MB and 30 second limits, and split longer recordings before transcription.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/zhipu-asr)
- [Zhipu AI API key console](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)
- [Zhipu AI audio transcription API endpoint](https://open.bigmodel.cn/api/paas/v4/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON transcription response with transcribed text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, curl, ffmpeg, and ZHIPU_API_KEY; sends audio, optional prompt text, and hotwords to Zhipu AI; documented limits are 25 MB and 30 seconds per audio request.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json and package.json report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
