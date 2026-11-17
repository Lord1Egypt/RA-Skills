## Description:

Generate Seedance videos, Seedream images, TTS speech, and OpenAI-compatible chat via the Xiaozhi AI (xzai.me) API. Use when the user asks to generate AI video, AI images, text-to-speech, or short video for e-commerce, short drama, or marketing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taotaojt9988](https://clawhub.ai/user/taotaojt9988)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to request AI video, image, speech, and chat generation through Xiaozhi AI for marketing, e-commerce, and creative workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance asks for a reusable XIAOZHI_API_KEY to be shared in chat.

Mitigation: Enter the key through a protected local secret-entry method rather than chat, and rotate any key already shared.

Risk: Submitted prompts and media are sent to xzai.me, and generation consumes account credits.

Mitigation: Review content before submitting and confirm generation parameters because jobs spend credits.

## Reference(s):

- [Xiaozhi AI service](https://xzai.me)
- [Xiaozhi AI API reference](artifact/references/api.md)
- [Xiaozhi AI Media on ClawHub](https://clawhub.ai/taotaojt9988/skills/xiaozhi-media)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated video, image, and WAV audio files; text responses; Markdown guidance and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video and image jobs may take several minutes; result URLs expire, and image dimensions may differ slightly from the requested aspect ratio.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
