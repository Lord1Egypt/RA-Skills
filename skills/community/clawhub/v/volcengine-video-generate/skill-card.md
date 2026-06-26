## Description: <br>
Generates videos with Volcengine Ark from a text prompt and optionally a first-frame image, then prints the generated video URL and downloads the video file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warm-wm](https://clawhub.ai/user/warm-wm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users can use this skill to call Volcengine Ark video generation from the command line, supplying a filename, prompt, and optional first-frame image URL or local file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and any provided first-frame images are sent to Volcengine/Ark for cloud processing. <br>
Mitigation: Avoid confidential prompts, sensitive images, and internal-only URLs unless that third-party processing is acceptable. <br>
Risk: The script downloads the generated video to the requested local output path. <br>
Mitigation: Choose an output path where creating or overwriting a video file is safe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/warm-wm/volcengine-video-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Console text with a downloaded video file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Volcengine Ark API key environment variable and may send prompts and optional first-frame images to a third-party cloud service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
