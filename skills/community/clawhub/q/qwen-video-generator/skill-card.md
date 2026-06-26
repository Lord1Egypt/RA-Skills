## Description: <br>
Generates short videos from text prompts using Alibaba Cloud DashScope wan2.2-t2v-plus, with configurable resolution, duration, and prompt extension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imnull](https://clawhub.ai/user/imnull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to turn text scene descriptions into short MP4 videos through DashScope. It supports configuring output resolution, clip duration, model selection, timeout, and prompt extension through environment variables or CLI arguments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Alibaba Cloud DashScope for video generation. <br>
Mitigation: Avoid confidential, personal, regulated, or secret content in prompts unless external processing through DashScope is approved. <br>
Risk: Generated MP4 files are written to a configured local output directory. <br>
Mitigation: Use a controlled VIDEO_OUTPUT_DIR or workspace videos directory with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imnull/qwen-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown usage guidance with shell commands; the script emits terminal status text and a VIDEO_PATH line for the generated MP4.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are saved as MP4 files in VIDEO_OUTPUT_DIR or the default workspace videos directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
