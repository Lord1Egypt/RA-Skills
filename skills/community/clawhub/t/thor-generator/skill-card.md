## Description:

Generate high-quality images locally using the ComfyUI Thor pipeline from user-provided text prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thortheai1-hash](https://clawhub.ai/user/thortheai1-hash)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to ask an agent to generate images from text prompts through a local ComfyUI Thor setup and save the resulting image file on the workstation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-provided image prompt is interpolated into a shell command, which can cause unintended local command execution.

Mitigation: Use a non-shell argument-array call or a fixed wrapper that passes the prompt as data before running the skill with untrusted prompts.

Risk: The skill runs a local image-generation pipeline and writes output to the Desktop, so installation and execution affect the local workstation.

Mitigation: Review the skill before installation, confirm the ComfyUI Thor environment and output path, and run it only in an environment where local file writes are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown or text guidance that may include a shell command for local image generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local image file saved to ~/Desktop/bring_img when the required ComfyUI Thor environment is present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
