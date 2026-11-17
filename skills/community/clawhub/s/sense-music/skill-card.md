## Description:

Music perception for AI entities - hear BPM, key, structure, genre, mood, and lyrics in any audio file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to analyze local or URL-based audio files and produce structured music observations, lyrics, visualizations, JSON, and HTML exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files and generated lyrics, transcripts, HTML, JSON, or images may contain sensitive user content.

Mitigation: Treat inputs and exports as private data, disable lyrics for private recordings when transcription is unnecessary, and delete generated outputs when they are no longer needed.

Risk: The release depends on the current PyPI package and audio-analysis dependencies.

Mitigation: Pin and review the package version in controlled environments before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vveerrgg/skills/sense-music)
- [OpenClaw Homepage](https://github.com/HumanjavaEnterprises/huje.sensemusic.OC-python.src)
- [PyPI Package](https://pypi.org/project/sense-music/)
- [huje.tools](https://huje.tools)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python examples, structured JSON/HTML exports, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include tempo, key, structure, genre, mood, lyrics, energy curves, spectrograms, waveforms, analysis.json, and analysis.html.]

## Skill Version(s):

0.1.5 (source: frontmatter, metadata.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
