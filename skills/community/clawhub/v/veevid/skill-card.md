## Description:

Veevid API for AI video, image and audio generation. Use when the user asks to generate or edit a video (text-to-video, image-to-video, reference-to-video), generate or edit an image, make speech (TTS), music or a transcript, or run a video tool: upscale, resize, extend, edit, lip-sync, motion control, character swap, virtual try-on. Covers Veo 3.1, Kling 3.0, Seedance, Wan, MiniMax H3, Nano Banana, GPT Image, Seedream, Eleven v4, Lyria and more; also quotes prices and checks credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meigesir](https://clawhub.ai/user/meigesir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate or edit video, images, and audio, compare model options, check credit balances, and review costs before starting a generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected source media are sent to Veevid for processing; the provider's storage and retention practices were not verified in this review.

Mitigation: Tell the user where files will be sent and get their approval before uploading private or sensitive media.

Risk: Generations and some upgrades spend credits, with prices affected by model settings and input duration or quantity.

Mitigation: Quote the exact request, including relevant input counts and durations, and get the user's confirmation before generating or upgrading.

Risk: A disclosed API key could allow access to the user's Veevid account.

Mitigation: Keep the key in the protected local config file, preserve restrictive file permissions, and never ask the user to paste it into chat.

Risk: Deleting a creation permanently removes the saved result and may remove uploaded input audio.

Mitigation: Identify the specific creation and obtain explicit confirmation before deletion.

## Reference(s):

- [Veevid API Reference](references/api-reference.md)
- [Video Model Reference](references/models-video.md)
- [Image Model Reference](references/models-image.md)
- [Audio Model Reference](references/models-audio.md)
- [Video Tools Reference](references/models-tools.md)
- [Manage Veevid API Keys](https://veevid.ai/settings/api-keys)
- [Veevid Pricing](https://veevid.ai/pricing)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Media files, Guidance]

**Output Format:** [Markdown guidance with JSON API request examples and media result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model-dependent parameters, source media, and credit costs]

## Skill Version(s):

1.3.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
