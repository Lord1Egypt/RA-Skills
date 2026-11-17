## Description:

生成火山引擎豆包语音播客（PodcastTTS）。输入主题文本，自动生成双人对话式播客音频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn topic text into a two-speaker podcast audio workflow backed by Volcano Engine PodcastTTS. It supports command-line and Python use, with options for head or tail music, voice hints, streamed audio output, and optional audio post-processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Volcano Engine API credentials.

Mitigation: Use a trusted Volcano Engine account, provide credentials through environment or documented config only, and avoid exposing tokens in prompts, logs, or generated artifacts.

Risk: Podcast topics are sent to an external speech service.

Mitigation: Do not submit secrets, regulated data, or sensitive personal data as podcast topics unless the external-service use has been approved.

Risk: Security evidence flags unsafe file and endpoint handling.

Mitigation: Keep the endpoint fixed to the official Volcano Engine service and run the skill under an unprivileged account with write access limited to the intended output directory.

Risk: The QQ bot helper has higher-risk config and media-path behavior.

Mitigation: Review and document the QQ helper before deployment, and sanitize output filenames and destination paths before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/volcano-engine-podcast)
- [ClawHub publisher profile](https://clawhub.ai/user/cindypapa)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, audio files, guidance]

**Output Format:** [Markdown instructions with Python and shell examples; runtime output is JSON-like status data and generated audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated podcasts may include segment files, final MP3/WAV/PCM audio, duration, transcript text, and token usage.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
