## Description:

Generate or edit images with Volcengine Seedream (Doubao) for text-to-image, image-to-image, multi-reference fusion, sequential generation, PNG output, prompt optimization, web search, and streaming workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberkurry](https://clawhub.ai/user/cyberkurry)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative operators use this skill to generate or edit images through the Volcengine Seedream API, including multi-reference image fusion and batches of related images. Agents can choose model, size, format, watermark, prompt optimization, streaming, and web-search options based on the user's image request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include a remote installer piped directly into the shell.

Mitigation: Install uv through a trusted package manager or download and verify the installer before running it.

Risk: Prompts, reference images, and web-search context are transmitted to external Volcengine services.

Mitigation: Avoid confidential prompts or private images, and enable web search only when current external information is required.

Risk: Passing the Volcengine API key with --api-key can expose the secret through shell history or process listings.

Mitigation: Use the VOLC_API_KEY environment variable and keep credentials out of scripts and shared command logs.

Risk: Default URL responses produce image links that expire after 24 hours.

Mitigation: Persist required outputs promptly or request base64 output when a durable inline payload is more appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberkurry/skills/seedream-volcengine)
- [Seedream Reference](references/REFERENCE.md)
- [Volcengine Seedream API documentation](https://www.volcengine.com/docs/82379/1541523)
- [Volcengine Seedream tutorial](https://www.volcengine.com/docs/82379/1824121)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; script output is MEDIA_URL, MEDIA_B64, or ERROR text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return temporary media URLs valid for 24 hours or base64 image payloads when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
