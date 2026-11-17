## Description:

Renders a YouTube video from shot-list.json - images and clips scaled to the target resolution, voiceover, optional background music and subtitles - into an H.264/AAC MP4 using FFmpeg. Use when the user wants to assemble, render, stitch or export the final video file for a YouTube project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to assemble shot-list images and clips, voiceover, optional music, and subtitles into an H.264/AAC MP4 for a YouTube project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shot-list media paths or the output destination may refer to unintended files or locations.

Mitigation: Review the shot list's media paths and output destination, then run --check before rendering.

Risk: Replacing an existing video can invalidate its upload approval.

Mitigation: Review the existing output and approve replacement before using --overwrite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahmadhussain0335/skills/socialkit-youtube-assemble)

## Skill Output:

**Output Type(s):** [Video files, JSON]

**Output Format:** [H.264/AAC MP4 video file and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MP4 is saved in the project folder; JSON reports success, output path, and total duration.]

## Skill Version(s):

0.3.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
