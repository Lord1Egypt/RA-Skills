## Description: <br>
Generates complete story videos from images, text descriptions, or both, with optional duration and style controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeng-austin](https://clawhub.ai/user/zeng-austin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to turn image or text prompts into a complete short video story, including storyboard JSON, subject reference art, frames, clips, instrumental background music, and a merged final video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated videos and temporary media files may consume significant disk space or be written outside the user's intended location. <br>
Mitigation: Confirm the output directory and available disk space before running the workflow, and keep generated files scoped to the project output folder. <br>
Risk: Installing or invoking FFmpeg and related media tools can change the local environment or execute media-processing commands. <br>
Mitigation: Ask for user confirmation before installing dependencies and review FFmpeg commands before execution. <br>


## Reference(s): <br>
- [Background Music Generation](references/bgm-generation.md) <br>
- [Frame Generation](references/frame-generation.md) <br>
- [Image Script Generation](references/image-script-generation.md) <br>
- [Subject Reference Generation](references/subject-reference.md) <br>
- [Text Script Generation](references/text-script-generation.md) <br>
- [Video Generation](references/video-generation.md) <br>
- [Video Merge](references/video-merge.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zeng-austin/story-video-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/zeng-austin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON artifacts, generated media files, and FFmpeg shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local output files under output/, including final_video.mp4; video segments are fixed at 6 seconds and 768P before final merge.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
