## Description: <br>
Generates and edits images with Volcengine Ark Doubao Seedream models from text prompts or input images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trylovecatch](https://clawhub.ai/user/trylovecatch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call Doubao Seedream models for text-to-image generation and image-to-image editing from command-line or interactive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and edited input images are sent to Volcengine Ark. <br>
Mitigation: Install only when this data sharing is acceptable for the intended use case. <br>
Risk: A long-lived API key may be stored in config.json. <br>
Mitigation: Prefer the VOLCENGINE_API_KEY environment variable or session-only key entry. <br>
Risk: Generated images may overwrite existing files when an output path is reused. <br>
Mitigation: Choose output paths carefully before running generation or editing commands. <br>


## Reference(s): <br>
- [Volcengine Ark Seedream API Documentation](https://www.volcengine.com/docs/82379/1541523) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>
- [ClawHub Skill Page](https://clawhub.ai/trylovecatch/sk-doubao-seedream) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated or edited image files to user-selected output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
