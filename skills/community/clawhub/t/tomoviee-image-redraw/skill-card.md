## Description:

Redraw image content using Tomoviee Image Redrawing API (`tm_redrawing`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Tomoviee image redrawing for inpainting, localized replacement, object removal, and mask-based image edits. It provides Python client usage, authentication guidance, endpoint references, and prompt guidance for image-editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The credential workflow can expose reusable Tomoviee app keys, app secrets, and Basic tokens through command-line arguments, terminal output, CI logs, or agent transcripts.

Mitigation: Handle Tomoviee credentials as secrets, avoid the documented token helper in shared terminals or logs, and prefer a credential flow that does not print reusable tokens.

Risk: Image redrawing sends source images, masks, prompts, and optional callback URLs to the Tomoviee/Wondershare service.

Mitigation: Submit only images, prompts, masks, and callback URLs that are approved for the external service and do not contain sensitive content unless that transfer is acceptable.

## Reference(s):

- [Tomoviee Image APIs](references/image_apis.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)
- [Tomoviee Developer Portal (Global)](https://www.tomoviee.ai/developers.html)
- [Tomoviee API Documentation (Global)](https://www.tomoviee.ai/doc/)
- [Tomoviee Developer Portal (Mainland)](https://www.tomoviee.cn/developers.html)
- [Tomoviee API Documentation (Mainland)](https://www.tomoviee.cn/doc/)
- [ClawHub Skill Release](https://clawhub.ai/wondershare-boop/skills/tomoviee-image-redraw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; client calls return task data and generated image URLs from the Tomoviee service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates asynchronous image redrawing tasks, polls task status, and parses service results for generated image paths.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
