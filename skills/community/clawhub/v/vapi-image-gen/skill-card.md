## Description:

Generate images via VAPI's OpenAI-compatible Images API, supporting the nano-banana and gpt-image model series with URL output by default and optional local saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popdo](https://clawhub.ai/user/popdo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent generate or edit images through VAPI's OpenAI-compatible image endpoints, including aspect-ratio, count, resolution, and save-location options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected input images, and the VAPI API key are sent to the configured VAPI endpoint.

Mitigation: Use the skill only with a trusted HTTPS VAPI_BASE_URL and avoid sending sensitive prompts, images, or credentials.

Risk: Edit mode can upload local files or images fetched from URLs.

Mitigation: Avoid --input with sensitive local paths or untrusted URLs, and review requested edit operations before execution.

## Reference(s):

- [VAPI API](https://api.v3.cm)
- [VAPI API default endpoint](https://api.v3.cm/v1)
- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/popdo/skills/vapi-image-gen)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is MEDIA URLs or saved image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses VAPI_API_KEY and VAPI_BASE_URL; images are not saved locally by default unless save behavior is requested or a gpt-image model returns base64 data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
