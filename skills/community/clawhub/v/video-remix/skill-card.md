## Description:

YouTube video processing assistant for Gemini-assisted analysis, download, clipping, voiceover, hard-subtitle composition, and local-network HTTP sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoyta](https://clawhub.ai/user/zhaoyta)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and automation users use this skill to turn a YouTube video into short-form Chinese commentary clips with generated narration, subtitles, and shareable video outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can install system packages and Python dependencies.

Mitigation: Review setup commands before execution, avoid sudo-driven setup from the skill itself, and install dependencies manually in an isolated environment.

Risk: The workflow can use a logged-in browser profile and external AI or TTS services.

Mitigation: Process only material suitable for external services and review generated scripts, transcripts, and narration before sharing outputs.

Risk: The workflow downloads videos and may process copyrighted or private material.

Mitigation: Use only videos the operator has the right to download, transform, and redistribute.

Risk: The workflow serves generated files on the local network.

Mitigation: Disable or restrict LAN HTTP sharing unless operating on a trusted network.

Risk: The workflow creates and cleans temporary working files.

Mitigation: Keep VR_TEMP_DIR pointed at a dedicated disposable folder and inspect paths before running cleanup behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoyta/skills/video-remix)
- [Publisher profile](https://clawhub.ai/user/zhaoyta)
- [Google Gemini](https://gemini.google.com/)
- [YouTube](https://www.youtube.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON examples, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Gemini metadata JSON, edited MP4 video, MP3 voiceover, SRT subtitles, and a local HTTP sharing address when executed.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
