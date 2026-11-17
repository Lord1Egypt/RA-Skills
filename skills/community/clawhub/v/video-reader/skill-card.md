## Description:

Tool-driven video question answering with frame extraction, sub-agent analysis, and audio transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiankemeng](https://clawhub.ai/user/qiankemeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-analysis users use this skill to answer questions about local or online videos by downloading media, extracting representative frame grids, transcribing audio, and coordinating sub-agent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download remote media and process local videos, which may introduce untrusted content into the agent environment.

Mitigation: Use trusted video sources, keep ffmpeg and media dependencies updated, and run the skill in a workspace where downloaded media can be reviewed and removed.

Risk: Audio transcription may upload extracted audio to a configured Whisper-compatible endpoint.

Mitigation: Review WHISPER_API_KEY, WHISPER_BASE_URL, and proxy settings before use; choose local transcription when audio should not leave the machine.

Risk: First-run and local Whisper setup can create persistent files or an auto-start service.

Mitigation: Run setup deliberately, inspect .env changes, and avoid the local Whisper auto-start path unless a persistent background service is desired.

Risk: The cleanup command can delete shared temporary image files and optional downloaded video cache.

Mitigation: Run videoarm-clean with --dry-run first and enable download cleanup only when cached videos are no longer needed.

Risk: The skill stores working memory, temporary frames, transcripts, downloads, and logs on disk.

Mitigation: Treat these artifacts as potentially sensitive, limit workspace access, and clean them after completing video analysis.

## Reference(s):

- [ClawHub Video Reader skill page](https://clawhub.ai/qiankemeng/skills/video-reader)
- [VideoARM research paper](https://arxiv.org/abs/2512.12360)
- [VideoARM-skill repository listed in artifact](https://github.com/qiankemeng/VideoARM-skill)
- [OpenClaw project listed in artifact](https://github.com/openclaw/openclaw)
- [FFmpeg project](https://ffmpeg.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON tool outputs and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary frame grids, transcripts, memory JSON, downloaded video cache, and analysis logs.]

## Skill Version(s):

4.1.1 (source: server release metadata; artifact pyproject.toml reports 4.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
