## Description:

Generate and translate video subtitles using WhisperX and LLM translation for video files, with multilingual transcription, target-language translation, and bilingual subtitle generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianhua-cui](https://clawhub.ai/user/jianhua-cui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media teams use this skill to guide an agent through generating timestamped subtitles from video files, translating subtitles through a configurable LLM API, and producing bilingual subtitle outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The translation path can send subtitle text to a remote LLM provider and incur token charges when an API key is configured.

Mitigation: Run transcription separately for sensitive videos, keep OPENAI_API_KEY unset unless translation is intended, and confirm the provider, base URL, and cost before translating.

Risk: Dependency installation and model downloads can consume substantial disk space and bandwidth.

Mitigation: Install in an isolated virtual environment, pin dependencies where practical, and confirm storage and download impact before installing packages or models.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jianhua-cui/skills/video-subtitle-generator)
- [WhisperX](https://github.com/m-bain/whisperX)
- [FFmpeg](https://ffmpeg.org/)
- [Python Downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are SRT subtitle files and JSON transcription metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source-language subtitles, transcription metadata, bilingual subtitles, and target-language subtitles when the corresponding scripts are run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
