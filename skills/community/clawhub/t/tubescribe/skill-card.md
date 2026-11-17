## Description:

YouTube video summarizer with speaker detection, formatted documents, and audio output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matusvojtek](https://clawhub.ai/user/matusvojtek)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use TubeScribe to turn YouTube videos into local transcript documents, summaries, key quotes, timestamped references, viewer-comment summaries, and optional audio summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can install persistent executable dependencies from the internet without strong verification.

Mitigation: Review before installing and prefer installing required tools yourself through trusted package managers.

Risk: YouTube captions, metadata, and comments are untrusted content processed by a tool-capable agent workflow.

Mitigation: Review generated summaries, transcripts, quotes, and comments before relying on or redistributing them.

Risk: Generated transcripts and audio summaries are saved locally under the user's account.

Mitigation: Use an appropriate output folder and delete generated files when the video content or transcript is sensitive.

## Reference(s):

- [TubeScribe ClawHub Skill Page](https://clawhub.ai/matusvojtek/skills/tubescribe)
- [Kokoro TTS](https://github.com/hexgrad/kokoro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local document or audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts may include DOCX, HTML, Markdown, MP3, or WAV files saved locally.]

## Skill Version(s):

1.1.8 (source: evidence.release and changelog, released 2026-02-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
