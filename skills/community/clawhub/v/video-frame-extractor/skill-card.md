## Description:

Guides agents to extract video frames with FFmpeg for keyframe sequences, interval thumbnails, or analysis-ready image sets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanghaoyu1997](https://clawhub.ai/user/huanghaoyu1997)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to have an agent plan and run FFmpeg-based extraction of JPEG frames from video files for thumbnails, keyframe review, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates and user-provided paths or numeric parameters could lead an agent to run unsafe shell commands or write outside the intended workspace.

Mitigation: Validate paths and numeric parameters, invoke FFmpeg through structured arguments instead of shell strings, and keep output inside the intended workspace.

Risk: Package installation commands can make system-level changes.

Mitigation: Run FFmpeg installation commands only after explicit user approval.

## Reference(s):

- [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance may produce FFmpeg commands that write sequential JPEG frames to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
