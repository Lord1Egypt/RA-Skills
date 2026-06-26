## Description: <br>
Automated high-quality video generation for text-to-video and image-to-video workflows via a local jimeng-api Docker service with native OpenClaw image interception that lets users send chat images directly for video generation without a UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahuamld](https://clawhub.ai/user/jiahuamld) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to generate short videos from prompts and local images through a local Jimeng API service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process chat-supplied images and prompts through a local Jimeng service, which may expose user content or generated video links. <br>
Mitigation: Use only images and prompts the user intentionally wants processed, avoid sensitive content, and confirm how the local service stores or forwards submitted data. <br>
Risk: The bundled script includes a cached session token and can install a dependency during normal execution. <br>
Mitigation: Remove the embedded token, require an explicit user-provided session, and install dependencies through a normal pinned setup step before running the skill. <br>
Risk: Broad automation over local image files may process unintended files if paths are not reviewed. <br>
Mitigation: Limit inputs to intended temporary files, review file paths before execution, and run the skill in a constrained workspace. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated video result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local jimeng-api service, a user-provided session token, a local image path for image-to-video use, and sufficient Jimeng credits.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
