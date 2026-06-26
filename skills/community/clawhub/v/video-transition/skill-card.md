## Description: <br>
Video Transition helps agents create smooth transitions and fade effects for local video clips using FFmpeg xfade and related filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation agents use this skill to merge local video segments, apply named transition effects, and add batch fade-in or fade-out effects through a Python interface backed by FFmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The FFmpeg commands write to user-specified output paths and may overwrite existing files. <br>
Mitigation: Use explicit output filenames in a safe working directory and avoid pointing outputs at files that must be preserved. <br>
Risk: Batch operations can create or replace multiple files in the selected output directory. <br>
Mitigation: Review input and output directories before running batch processing. <br>
Risk: The helpers depend on local FFmpeg and FFprobe behavior. <br>
Mitigation: Use a trusted FFmpeg/FFprobe installation before processing local videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/systiger/video-transition) <br>
- [Publisher profile](https://clawhub.ai/user/systiger) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and FFmpeg command patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video files through FFmpeg when the provided Python helpers are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
