## Description:

Swap one on-camera element in an existing video while preserving the original motion, timing, camera, lighting, background, and audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to prepare Runware videoInference requests for targeted character, product, garment, or mascot replacement in existing videos while preserving the rest of the scene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source videos and reference images may be sent to the video inference provider used by the user's Runware tools.

Mitigation: Use only media that can be shared with that provider, and avoid confidential, regulated, or identifiable-person media unless rights, consent, handling, and retention terms are understood.

Risk: The workflow can recast or alter a real person's likeness.

Mitigation: Use source footage and reference images only when the caller has the necessary rights and consent, and do not recast identifiable people without consent.

Risk: Small details, extreme motion, or weak face anchors can cause identity, object, or scene drift.

Mitigation: Review outputs for unwanted changes, use clearer references and tighter preserve prompts, and use masked inpainting when pixel-perfect detail is required.

## Reference(s):

- [Replace in video: worked recipes](references/examples.md)
- [Replace In Video on ClawHub](https://clawhub.ai/runware/skills/replace-in-video)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, JSON]

**Output Format:** [Markdown with JSON request examples and polling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides asynchronous videoInference calls that return taskUUID values and final videoURL outputs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
