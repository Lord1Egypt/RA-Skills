## Description:

Generates polished Sora 2 video prompts from a topic or public image-guided scene idea through the NanoPhoto.AI Prompt Generator API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn short topic or scene ideas, with optional public image URLs, into production-ready text-to-video or image-to-video prompts for Sora 2 workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt topics, selected options, and public image URLs are sent to NanoPhoto.AI.

Mitigation: Submit only content you are authorized to use, and avoid private or sensitive topics and image URLs.

Risk: The skill requires a NanoPhoto API key.

Mitigation: Store NANOPHOTO_API_KEY in the platform's secure environment-variable setting and do not paste the key into chat.

Risk: Prompt generation can consume credits or hit service rate limits.

Mitigation: Confirm generation intent before calling the API, then follow the documented retry or credit top-up guidance for rate-limit and insufficient-credit errors.

## Reference(s):

- [Sora 2 Prompt Generator API Reference](artifact/references/api.md)
- [NanoPhoto.AI homepage](https://nanophoto.ai)
- [NanoPhoto API key management](https://nanophoto.ai/settings/apikeys)
- [ClawHub skill page](https://clawhub.ai/nanophotohq/skills/video-prompt-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text prompt, with Markdown guidance or shell commands when setup or troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script assembles the streaming API response into final prompt text; image-to-video mode requires one to three public image URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
