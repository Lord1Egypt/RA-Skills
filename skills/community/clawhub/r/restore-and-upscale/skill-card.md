## Description:

Improves degraded or low-resolution images by deblurring, denoising, dehazing, restoring defects, and enlarging them while preserving the original content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select an appropriate restoration or upscaling workflow for degraded, blurry, noisy, hazy, compressed, or low-resolution still images. It helps agents choose between faithful and detail-generating models, set expectations for faces and documents, and inspect results before returning them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes video-upscaling workflow guidance even though server security evidence notes video belongs in a separate skill.

Mitigation: Route video requests through the dedicated video-upscale workflow and review whether video handling is in scope before installation.

Risk: Sensitive personal photos or videos may be processed by external media providers during restoration or upscaling.

Mitigation: Review provider data-handling terms before submitting sensitive media and use approved workflows for personal or confidential content.

Risk: Diffusion-based restoration can invent detail in faces, documents, text, or other fidelity-sensitive content.

Mitigation: Prefer faithful non-diffusion paths for fidelity-sensitive inputs, state the face-restoration limitation clearly, and inspect full-resolution outputs before returning them.

## Reference(s):

- [Worked Recipes](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/runware/skills/restore-and-upscale)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with JSON API payload examples and returned media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce synchronous image results or asynchronous video result guidance depending on the selected model path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
