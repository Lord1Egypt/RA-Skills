## Description: <br>
Automates an end-to-end workflow that turns an SRT subtitle file into a whiteboard animation video by parsing storyboard scenes, generating images, and compiling video segments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangagent](https://clawhub.ai/user/yangagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users can use this skill to convert subtitle scripts into organized whiteboard video assets and a merged MP4 output. It is intended for workflows where the user provides an SRT file and wants storyboard, image, and video generation handled in sequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends subtitle-derived prompts to RunningHub for image generation. <br>
Mitigation: Avoid confidential subtitles unless third-party image processing is acceptable, and use a revocable RunningHub API key. <br>
Risk: The workflow invokes dependency setup and relies on a separate whiteboard-animation skill. <br>
Mitigation: Review both skills before installation and run dependency setup in a sandbox or virtual environment. <br>
Risk: Generated files are written to user-selected output paths. <br>
Mitigation: Keep output paths inside the workspace and review paths before running the workflow. <br>


## Reference(s): <br>
- [Storyboard Parser](references/storyboard-parser.md) <br>
- [Banana2 Image Generator](references/image-generator.md) <br>
- [RunningHub](https://www.runninghub.cn/) <br>
- [RunningHub OpenAPI](https://www.runninghub.cn/openapi/v2) <br>
- [ClawHub skill page](https://clawhub.ai/yangagent/whiteboard-video-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [JSON result with generated storyboard, image paths, video segment paths, and merged MP4 path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RunningHub API key and may create storyboard, image, and video directories under the selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
