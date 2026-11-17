## Description:

Clip Editor helps agents analyze videos, plan narrated or speech-based clips, produce aligned narration, subtitles, video segments, and generate CapCut/JianYing draft JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riclinccc](https://clawhub.ai/user/riclinccc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to turn source videos into short narrated clips or jump-cut dialogue edits with synchronized media assets and CapCut/JianYing draft files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, transcripts, narration prompts, or clip metadata may be sent to external AI or media services.

Mitigation: Use only media approved for external processing, avoid confidential videos, and confirm remote-service behavior before use.

Risk: The workflow uses broad local and network authority to run media tooling, create files, and interact with editing services.

Mitigation: Run the skill in an isolated environment, review generated plans before execution, and require explicit approval before draft creation or uploads.

Risk: Runtime package installation using --break-system-packages can modify the host Python environment.

Mitigation: Install dependencies in a dedicated virtual environment or container and avoid --break-system-packages on shared systems.

## Reference(s):

- [CapCut MCP Server Reference](references/capcut-mcp.md)
- [vectcut-api Reference](references/vectcut-api.md)
- [FFmpeg Download](https://ffmpeg.org/download.html)
- [ClawHub Skill Page](https://clawhub.ai/riclinccc/skills/video-clip-editor)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, shell commands, JSON draft files, SRT subtitles, MP3 narration files, and MP4 clip files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected generated files include narration MP3s, subtitles.srt, clip MP4s, and draft_content.json with timing aligned to measured narration duration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
