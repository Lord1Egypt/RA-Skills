## Description:

Auto-generate masks for objects/regions in images. Use when users request image_recognition operations or related tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Tomoviee's image recognition API for generating masks of objects or regions in supplied images. The generated masks can support downstream image editing, redrawing, and segmentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs and prompts are sent to a third-party Wondershare/Tomoviee API.

Mitigation: Avoid submitting sensitive images or private URLs unless the user has approved the data handling and external API use.

Risk: The documented token helper accepts reusable API credentials on the command line and prints the resulting access token.

Mitigation: Use protected environment variables or a secret manager, avoid shared terminals and CI logs, and rotate credentials that may have been exposed.

Risk: The bundled references include broader Tomoviee image generation guidance beyond the skill's stated image-mask purpose.

Mitigation: Keep agent use scoped to image recognition and mask generation unless the user explicitly asks for related Tomoviee image generation workflows.

## Reference(s):

- [Tomoviee Image APIs](references/image_apis.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html)
- [Tomoviee API Documentation](https://www.tomoviee.ai/doc/)
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/tomoviee-image-recognition)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; API results are JSON-like task and mask URL payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an asynchronous third-party API workflow with task polling and returned mask URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
