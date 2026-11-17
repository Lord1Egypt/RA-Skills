## Description:

Record a selected screen region on Windows with ffmpeg gdigrab, with guidance and scripts for timed capture, high-DPI coordinates, and region selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT

## Use Case:

Windows users and developers can select and record a fixed area of the primary display for demos, bug reports, or animation capture. The supplied guidance helps them account for display scaling and check the resulting video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recorded clip duration may differ from the requested duration.

Mitigation: Check the finished file's duration with ffprobe and compare it with the requested capture time before sharing it.

Risk: The security analysis was partial because a referenced local path was missing, leaving some evidence incomplete.

Mitigation: Review the complete release contents and resolve the missing path reference before relying on the scan as a complete assessment.

Risk: Running the recorder accesses screen contents and invokes ffmpeg; the security guidance also reports a diagnostic file write.

Mitigation: Review the selected region and output location, and run the scripts only in an environment where screen capture and those file writes are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catsmansion/skills/windows-region-exact-record)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown guidance with Python and Windows batch scripts and ffmpeg command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports selected screen regions and requested capture durations; captures only the primary display and does not record audio.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
