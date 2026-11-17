## Description:

General speech-recognition skill that transcribes audio files in formats such as ogg, mp3, wav, and m4a using the SiliconFlow SenseVoice API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demo112](https://clawhub.ai/user/demo112)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to convert user-supplied voice messages or audio files into text. It is intended for transcription workflows that can send audio to SiliconFlow for cloud processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio content is uploaded to SiliconFlow for cloud transcription.

Mitigation: Use only with recordings approved for that service, and avoid confidential audio unless organizational approval is in place.

Risk: Example temporary-file handling can leave converted audio in predictable temporary paths.

Mitigation: Use unique private temporary files and delete converted audio after transcription.

Risk: API credentials are needed for transcription calls.

Mitigation: Store the API key securely, prefer environment-based injection, and avoid hardcoding secrets in skill examples or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/demo112/skills/speech-recognition)
- [SiliconFlow audio transcription API endpoint](https://api.siliconflow.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code and shell command examples; transcription output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SILICONFLOW_API_KEY and FFmpeg for audio conversion.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter and skill.json list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
