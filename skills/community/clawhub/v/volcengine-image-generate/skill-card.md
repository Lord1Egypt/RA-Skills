## Description: <br>
Using volcengine image_generate.py script to generate image, need to provide clear and specific `prompt`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warm-wm](https://clawhub.ai/user/warm-wm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images from text prompts through Volcengine Ark and save the generated PNG files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Volcengine/Ark for remote image generation. <br>
Mitigation: Do not include secrets, confidential data, or sensitive personal information in prompts. <br>
Risk: The skill uses API credentials and may consume Volcengine/Ark quota. <br>
Mitigation: Set only the intended API key environment variables and confirm quota and billing expectations before use. <br>
Risk: Generated PNG files are downloaded to a local directory. <br>
Mitigation: Run the script from a directory where generated files are acceptable, or set IMAGE_DOWNLOAD_DIR to an intended output location. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with generated image download paths or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated PNG files are downloaded to the current directory by default, or to IMAGE_DOWNLOAD_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
