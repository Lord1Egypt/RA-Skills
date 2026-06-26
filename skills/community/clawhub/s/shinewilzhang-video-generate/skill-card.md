## Description: <br>
Generates videos from a text prompt with optional first-frame image input using the bundled video_generate.py script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinewilzhang](https://clawhub.ai/user/shinewilzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate an MP4 video from a prompt, optionally conditioning the first frame with an image URL or local image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional first-frame images are sent to the Ark/Volcengine service. <br>
Mitigation: Use a dedicated API key and avoid sensitive prompts, local images, private URLs, or internal content. <br>
Risk: The script downloads the generated video to the requested output path, which may overwrite an existing file. <br>
Mitigation: Choose an output path where replacement is acceptable or verify that the destination file does not already exist. <br>
Risk: The skill depends on an external SDK and service availability. <br>
Mitigation: Install dependencies from trusted sources and handle service or credential failures before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinewilzhang/shinewilzhang-video-generate) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is console text and an MP4 file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ark/Volcengine credentials and sends prompts and optional first-frame images to the external generation service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
