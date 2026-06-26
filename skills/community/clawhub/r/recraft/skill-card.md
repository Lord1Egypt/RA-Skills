## Description: <br>
Generate, vectorize, upscale, replace background, variate, remove background, and transform images via Recraft API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nkrcrft](https://clawhub.ai/user/nkrcrft) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to call the Recraft API for image generation, image editing, vectorization, upscaling, background removal, background replacement, and image variation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Recraft API token and sends selected prompts and images to Recraft for processing. <br>
Mitigation: Use it only with content approved for Recraft processing and provide the token through the documented RECRAFT_API_TOKEN environment variable or explicit command option. <br>
Risk: Generated or transformed files are written to user-selected output paths. <br>
Mitigation: Choose output filenames deliberately and review generated files before using or sharing them. <br>
Risk: The user-info command can print account details in local command output. <br>
Mitigation: Run user-info only when account details are needed and avoid sharing logs that contain that output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nkrcrft/recraft) <br>
- [Recraft](https://www.recraft.ai/) <br>
- [Recraft API Key Page](https://www.recraft.ai/profile/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated image or SVG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image or SVG files and may print MEDIA lines for attachment by supported chat providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
