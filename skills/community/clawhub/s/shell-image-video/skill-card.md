## Description: <br>
Integrates RunningHub AI workflows for face swap, motion transfer, dance video generation, digital human video, mouth-sync, lip-sync, and image comparison tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lygjoey](https://clawhub.ai/user/lygjoey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to guide agents through RunningHub media workflows that transform images, faces, voices, and videos into generated image or video outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill evidence includes an exposed RunningHub API key. <br>
Mitigation: Remove and rotate the exposed key before release, and require users to provide their own credential through an environment variable or secret store. <br>
Risk: The skill asks agents to run referenced local scripts that are not included in the artifact evidence. <br>
Mitigation: Provide the scripts for review and scan them before installation or execution. <br>
Risk: The workflows process sensitive face, voice, image, and video media. <br>
Mitigation: Use only media that the user has rights and consent to process, and add explicit privacy and consent guidance before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lygjoey/shell-image-video) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lygjoey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides calls to external RunningHub workflows that may return JSON containing generated media URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
