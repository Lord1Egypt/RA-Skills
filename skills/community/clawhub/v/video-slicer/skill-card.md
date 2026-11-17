## Description:

Video Slicer helps agents turn long videos into topic-focused 3-5 minute clips by sampling key frames, transcribing Chinese speech with local Whisper, planning clip boundaries, and cutting clips with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abill6688](https://clawhub.ai/user/abill6688)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, and developers use this skill to extract social-video clips, course chapters, meeting highlights, podcast segments, or personal archive clips from long recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated outputs may overwrite existing files in the selected output directory.

Mitigation: Run the skill in a fresh output directory and review planned paths before executing ffmpeg or the bundled script.

Risk: Local Whisper execution downloads and caches model files and creates frames, audio extracts, transcripts, and clips on disk.

Mitigation: Use a dedicated virtual environment and a workspace with adequate storage, then remove temporary media artifacts when no longer needed.

Risk: Package installation commands can affect the host Python environment.

Mitigation: Install Python dependencies in a dedicated virtual environment and avoid elevated privileges unless required by the OS package manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abill6688/skills/video-slicer)
- [README.md](README.md)
- [scripts/video_slicer.py](scripts/video_slicer.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell and Python snippets, JSON clip plans and transcripts, text transcripts, sampled JPEG frames, audio segments, and MP4 clips.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local media-processing outputs in the selected output directory, including frames, transcripts, audio extracts, clip plans, and video clips.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
