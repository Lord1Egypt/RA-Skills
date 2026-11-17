## Description:

Generates a new image that imitates the style of a reference image while updating content based on user intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a new image that keeps the style and layout of a reference image while replacing the subject matter with requested content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User images and prompts may be sent to configured SN or third-party AI providers.

Mitigation: Use only images and prompts suitable for the configured providers, and review provider handling before deployment.

Risk: Generated work files may remain in temporary storage and retries or thresholds may be insufficiently bounded.

Mitigation: Keep retry counts small, clean intermediate artifacts, and prefer a version that uses private temporary directories with hard retry and threshold limits.

Risk: The skill depends on sn-image-base for recognition, text optimization, and image generation.

Mitigation: Verify that sn-image-base is trusted and configured with the intended credentials before installing or running this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-image-imitate)
- [README](artifact/README.md)
- [Image annotation prompt](artifact/prompts/image_annotate.md)
- [Caption rewrite prompt](artifact/prompts/caption_rewrite.md)
- [Layout review prompt](artifact/prompts/layout_review.md)
- [SenseNova Token Plan](https://platform.sensenova.cn/token-plan)

## Skill Output:

**Output Type(s):** [text, image, json, markdown, guidance]

**Output Format:** [Generated image plus concise text or a verbose structured run summary with JSON process artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected image path, rewritten caption, layout blueprint, attempt scores, deviations, and timing; pixel-level fidelity to the reference is not guaranteed.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
