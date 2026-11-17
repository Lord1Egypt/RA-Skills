## Description:

Turn video/audio transcripts into original screenplays. Faster-whisper to LLM story DNA to screenplay (.md and .fountain). Supports 6 LLM providers and CPU/GPU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyldmh](https://clawhub.ai/user/hyldmh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn SRT transcripts or audio/video files into story DNA and original screenplay drafts. It can produce human-readable Markdown, Fountain screenplay files, transcripts, and extracted story elements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input transcripts or media may be sent to the selected external LLM provider.

Mitigation: Use only transcripts or media that are acceptable to share with the chosen provider, and redact sensitive content before processing.

Risk: The dependency install path is unpinned.

Mitigation: Install in a dedicated virtual environment and pin or review dependencies before operational use.

Risk: The current Google-provider branch contains a Python syntax error.

Mitigation: Fix and test the Google-provider path before use, or select another supported provider until it is corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyldmh/skills/video-to-screenplay)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; generated artifacts include transcript text, story DNA JSON, screenplay Markdown, and Fountain files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports transcript-only extraction, genre and target-duration controls, provider/model selection, and CPU/GPU transcription settings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
