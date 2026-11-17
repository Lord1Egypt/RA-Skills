## Description:

Create product, advertisement, and style-replication videos through the ShortVideo API using product images, source videos, prompts, and polling commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thecur](https://clawhub.ai/user/thecur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate product videos, create ad videos from images, replicate an existing video style with new assets, and poll for completed ShortVideo results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary media URLs supplied by a user.

Mitigation: Do not provide internal, localhost, private-network, cloud metadata, or otherwise sensitive URLs as media inputs.

Risk: Media files, prompts, product details, source videos, and API credentials may be sent to the configured ShortVideo service.

Mitigation: Install only when the publisher is trusted, keep SHORTVIDEO_BASE_URL pinned to the legitimate HTTPS ShortVideo API, and use a service-scoped API key.

## Reference(s):

- [Product to Video reference](references/product-to-video.md)
- [Image to Ad Video v2 reference](references/image-to-ad-video-v2.md)
- [Replicate Video reference](references/replicate-video.md)
- [ShortVideo API site](https://shortvideo.ai)
- [ClawHub skill page](https://clawhub.ai/thecur/skills/shortvideo-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ShortVideo task identifiers, upload summaries, polling status, errors, and final video URLs.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
