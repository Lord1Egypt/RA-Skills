## Description: <br>
Video Stitcher helps agents combine video clips into a finished video with optional transitions, background music, subtitles, resolution, frame rate, and export format settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OliviaPp8](https://clawhub.ai/user/OliviaPp8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to prepare FFmpeg or Remotion-based video stitching workflows for promotional, demo, short-form, or platform-specific exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided clip URLs or paths may expose private media or internal network locations. <br>
Mitigation: Use trusted local files or trusted URLs, and avoid internal or private URLs unless the environment is approved for that access. <br>
Risk: Generated output paths may overwrite existing files. <br>
Mitigation: Set output paths inside a dedicated render folder and review the target path before executing FFmpeg or Remotion. <br>
Risk: Large or high-resolution video renders may be slow or resource intensive, and automatic scaling can affect quality. <br>
Mitigation: Preview complex or 4K jobs at 1080p first, then render the final version after checking resolution, timing, and transition settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OliviaPp8/video-stitcher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with YAML examples and inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces media-rendering guidance and command/configuration patterns; rendered video files are created only when the agent or user executes the generated workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
