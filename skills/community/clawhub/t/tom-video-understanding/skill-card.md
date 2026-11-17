## Description:

Local video comprehension skill. Use ffmpeg to extract audio and frames, FunASR for speech recognition, and qwen3-vl for image understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect video content by extracting audio, sampling frames, transcribing Chinese speech locally, and combining transcript and frame observations into an analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises local processing while allowing optional cloud LLM analysis of transcript and frame information.

Mitigation: Treat cloud analysis as explicit opt-in and avoid sending private, regulated, or sensitive video-derived content to a remote provider unless approved.

Risk: Model and package setup depends on external sources such as Ollama, FunASR, ModelScope, and conda or pip packages.

Mitigation: Install dependencies only from trusted sources, avoid arbitrary mirrors, and review model/package provenance before processing sensitive videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomuiv/skills/tom-video-understanding)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local transcripts, frame descriptions, and optional combined analysis derived from extracted video content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
