## Description:

Generates a single chat-ready Chinese meme image from speech-recognition text or polished text, with automatic tone-based styling and optional caption templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn dictated or polished Chinese chat text into one meme or sticker image for messaging interfaces and input-method integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dictated or polished user text is sent to an external image-model endpoint.

Mitigation: Use only trusted model endpoints and avoid sending sensitive, confidential, or regulated dictated text.

Risk: The image download path follows URLs returned by the image service.

Mitigation: Prefer b64_json image responses, or add URL allowlisting, content-type validation, size limits, and timeout controls before use in networked or corporate environments.

Risk: Dependencies are declared with broad lower bounds.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hei-maom/skills/voice-text-to-meme)
- [图片模型接入说明](artifact/references/api_cn.md)
- [输入法接入说明](artifact/references/integration_cn.md)

## Skill Output:

**Output Type(s):** [image file, json, text]

**Output Format:** [JPEG image file plus JSON metadata containing the selected source text, tone, mode, prompt, image path, and caption or caption template.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to a single JPEG output; template mode returns suggested top, bottom, or single-caption text for downstream overlay.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
