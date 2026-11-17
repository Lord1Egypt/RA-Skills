## Description:

iFlytek Ultra-Realistic TTS synthesizes natural, expressive speech from text using iFlytek's ultra-realistic voice synthesis API, with selectable voices, audio formats, speed, volume, and pitch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert text, files, or stdin into generated speech audio through iFlytek's TTS API. It supports narration, voice content generation, and scripted audio production with configurable voice and audio parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text and API-authenticated requests are sent while TLS certificate and hostname checks are disabled.

Mitigation: Enable normal TLS certificate and hostname validation before using the skill with secrets, regulated data, or confidential text.

Risk: Generated audio is stored locally and may contain sensitive source text.

Mitigation: Choose output locations intentionally and handle generated audio files according to the sensitivity of the input text.

## Reference(s):

- [iFlytek Console](https://console.xfyun.cn)
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/xfyun-tts)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [Audio files with command-line status text and an absolute output path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports mp3, pcm, speex, and opus output; generated audio is written locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
