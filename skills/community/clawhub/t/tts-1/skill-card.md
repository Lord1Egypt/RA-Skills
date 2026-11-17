## Description:

Text-to-speech conversion using node-edge-tts for generating audio from text with multiple voices, languages, speed adjustment, pitch control, and subtitle generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[17854566382](https://clawhub.ai/user/17854566382)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to convert requested text into spoken audio, choose voices and prosody settings, and optionally generate subtitle timing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested text is sent to Microsoft Edge's online TTS service.

Mitigation: Avoid converting secrets, private messages, regulated data, or proprietary content unless that external processing is acceptable.

Risk: Generated audio and subtitle files can persist in temporary or custom output paths.

Mitigation: Choose intentional output paths for sensitive audio and clean up generated files after use.

Risk: The skill installs npm dependencies before using the bundled scripts.

Mitigation: Audit or update npm dependencies before using the skill in automation.

## Reference(s):

- [node-edge-tts Reference](references/node_edge_tts_guide.md)
- [Voice Testing](https://tts.travisvn.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline JavaScript and shell command examples; generated runtime artifacts are MP3 audio files and optional JSON subtitle files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Microsoft Edge's online TTS service through node-edge-tts, requires internet access, and may write audio to a temporary directory or a user-selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package files report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
