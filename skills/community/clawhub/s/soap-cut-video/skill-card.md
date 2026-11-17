## Description:

Generates short vertical ASMR soap or wax cutting videos from text prompts or public HTTPS image URLs, emphasizing clean slices, exposed cross-sections, falling powder, and cutting audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to generate 5-second, 9:16 ASMR-style videos of soap or wax cutting from either a written scene description or a public product image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public image URLs, generation metadata, and WERYAI_API_KEY may be sent to WeryAI or configured compatible endpoints.

Mitigation: Install only when this data sharing is acceptable, keep custom WeryAI endpoint variables unset unless they point to trusted HTTPS endpoints, and use a limited or revocable API key.

Risk: Video generation may consume credits or expose task metadata if the API key is misused.

Mitigation: Use a scoped or revocable WERYAI_API_KEY, monitor generated tasks, and rotate the key if endpoint configuration or usage looks unexpected.

Risk: Image-to-video mode requires a public HTTPS image URL, which can expose the referenced source image to the video service.

Mitigation: Use only images that are intended for external processing and avoid private, local, or access-controlled URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/soap-cut-video)
- [Publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command parameters and generated video links returned by the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js 18+, WERYAI_API_KEY, optional WeryAI endpoint environment variables, and public HTTPS image URLs for image-to-video generation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
