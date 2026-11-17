## Description:

Raise AI Media helps agents use the RaiseAI service to generate images, generate videos, create video scripts, and extract prompts or scripts from media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobluxj](https://clawhub.ai/user/jacobluxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route media-generation requests to RaiseAI, including text-to-image, image editing, text-to-video, video script generation, and prompt or script extraction from supplied media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reusable RaiseAI API key may be exposed if pasted into chat or stored insecurely.

Mitigation: Configure RAISE_AI_API_KEY through a secure configuration path, avoid sharing it in conversation, and rotate the key if exposure is suspected.

Risk: Generated media and output links may include sensitive user content or temporary signed URLs.

Mitigation: Avoid submitting sensitive media unless the RaiseAI service is approved for that data, and share generated links only with intended recipients before they expire.

## Reference(s):

- [RaiseAI homepage](https://ai.micrease.com)
- [ClawHub skill page](https://clawhub.ai/jacobluxj/skills/raise-ai-media)
- [API setup](references/api-setup.md)
- [Image generation API](references/image-generation.md)
- [Video generation API](references/video-generation.md)
- [Video script generation API](references/script-generation.md)
- [Prompt extraction API](references/prompt-extraction.md)
- [Polling and error handling](references/polling-and-errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown responses with generated media links, structured script content, extracted prompts, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAISE_AI_API_KEY and returns asynchronous RaiseAI task results, including temporary signed media URLs when generation succeeds.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
