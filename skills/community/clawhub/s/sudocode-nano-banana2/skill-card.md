## Description:

Generate or edit images with Sudocode's nano-banana2 remote image service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengy983](https://clawhub.ai/user/shengy983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate images from prompts or edit local images through Sudocode's remote image-generation API. It also helps agents initialize required credentials and deliver generated image files to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional input images, and the API key are sent to the configured Sudocode endpoint.

Mitigation: Use the skill only with a trusted Sudocode HTTPS endpoint and avoid private images or sensitive prompts unless sending them to that service is acceptable.

Risk: The configurable SUDOCODE_BASE_URL can direct requests away from the intended service.

Mitigation: Keep SUDOCODE_BASE_URL set to the real Sudocode HTTPS endpoint before running the image-generation script.

Risk: Credentials and run logs may remain on local disk.

Mitigation: Protect ~/.openclaw/.env with owner-only permissions and review or delete generated log files when outputs may contain sensitive information.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/shengy983/skills/sudocode-nano-banana2)
- [Publisher profile](https://clawhub.ai/user/shengy983)
- [Sudocode service](https://sudocode.us)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files and per-run logs are written to local disk near the chosen output path.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
