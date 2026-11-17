## Description:

Removes watermarks from Sora 2 share-link videos by calling the NanoPhoto.AI API and returning a clean downloadable video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process authorized Sora 2 share-link videos through NanoPhoto.AI and receive a clean downloadable video URL. Users should confirm watermark removal is lawful and allowed for their use case before submitting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sora share links are submitted to NanoPhoto.AI for processing.

Mitigation: Install and use the skill only if you trust NanoPhoto.AI with submitted share links and have reviewed privacy and retention terms for the intended use case.

Risk: Watermark removal may be inappropriate if the user lacks rights or if the use case disallows it.

Mitigation: Confirm the user is authorized to process the content and that watermark removal is lawful and allowed before calling the API.

Risk: The NanoPhoto.AI API key could be exposed if pasted into chat or committed into files.

Mitigation: Configure NANOPHOTO_API_KEY through secure environment settings and avoid sharing the key in chat.

## Reference(s):

- [Sora Watermark Removal API Reference](references/api.md)
- [NanoPhoto.AI Homepage](https://nanophoto.ai)
- [NanoPhoto.AI API Key Management](https://nanophoto.ai/settings/apikeys)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a clean video URL when the external API completes successfully.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
