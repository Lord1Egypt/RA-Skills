## Description:

Generates and edits images through usa0.top's OpenAI-compatible GPT Images API, supporting text prompts, local or remote reference images, multi-image editing, and batch output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkxs](https://clawhub.ai/user/tkxs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or edit images through usa0.top from prompts and reference images. It guides API key setup, environment preparation, image generation or editing commands, and locating saved image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and user images can be sent to arbitrary or unencrypted endpoints if a custom base URL is used.

Mitigation: Use the default HTTPS usa0.top endpoint unless the destination is fully trusted; do not use HTTP endpoints.

Risk: Prompts and reference images are sent to usa0.top for processing.

Mitigation: Do not submit sensitive content, private local files, private-network image URLs, or material the user is not authorized to process.

Risk: Windows key configuration saves USA_API_KEY persistently for the current user.

Mitigation: Use a dedicated, revocable, quota-limited API key and rotate or remove it when it is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tkxs/skills/usa-image-skill)
- [Publisher Profile](https://clawhub.ai/user/tkxs)
- [USA-零](https://usa0.top)
- [USA-零 API Documentation](https://usa0.top/docs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and MEDIA file paths; generated images are saved as PNG, JPEG, or WebP files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, and USA_API_KEY; supports up to 16 reference images, up to 10 generated outputs per run, and local or HTTP/HTTPS reference image sources.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
