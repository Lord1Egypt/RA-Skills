## Description:

Using volcengine image_generate.py script to generate image, need to provide clear and specific `prompt`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warm-wm](https://clawhub.ai/user/warm-wm)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent operators use this skill to generate images from text prompts through Volcengine/Ark and save the resulting image files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Volcengine/Ark API credentials through environment variables.

Mitigation: Install only for intended Volcengine/Ark image generation use and provide appropriately scoped credentials through the documented environment variables.

Risk: Generated image files are downloaded to a local directory that may default to the current working directory.

Mitigation: Set IMAGE_DOWNLOAD_DIR to a dedicated folder so generated files are written to an expected location.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions]

**Output Format:** [Console text with generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved locally; credentials and output directory are configured through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
