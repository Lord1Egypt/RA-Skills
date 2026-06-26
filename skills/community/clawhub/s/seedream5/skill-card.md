## Description: <br>
Seedream5 helps an agent generate or edit images with Volcengine Doubao Seedream 5.0, including text-to-image, single-image and multi-image editing, grouped images, and optional web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zealman2025](https://clawhub.ai/user/zealman2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to call Volcengine Seedream 5.0 from an agent workflow, sending prompts and optional reference images and receiving locally saved generated images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to Volcengine for generation or editing. <br>
Mitigation: Avoid sending confidential images, secrets, or regulated personal data unless the provider terms and internal policy allow it. <br>
Risk: The script writes generated image files to the filename or path supplied by the user. <br>
Mitigation: Choose output filenames deliberately and review the destination path before execution. <br>
Risk: The skill requires a Volcengine API key in configuration or environment variables. <br>
Mitigation: Store the key in the supported credential configuration or environment variable and avoid exposing it in prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub Seedream5 Listing](https://clawhub.ai/zealman2025/seedream5) <br>
- [Volcengine Seedream API Documentation](https://www.volcengine.com/docs/82379/1541523) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and local image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved to the requested local path and emitted as MEDIA paths for compatible OpenClaw chat channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
