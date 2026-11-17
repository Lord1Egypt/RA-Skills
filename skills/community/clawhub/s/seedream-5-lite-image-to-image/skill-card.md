## Description:

Uses Seedream 5.0 Lite through AI Hive to redraw authorized reference images with region delta maps that lock, modify, or rebuild specified areas while controlling edit strength.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to create controlled image-to-image edits for authorized photos, sketches, products, layout expansions, and illustration conversions while preserving specified facts and regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images and prompts are sent to AI Hive for image editing.

Mitigation: Use only authorized images and prompts that are acceptable for external processing.

Risk: The helper can store an AI Hive API key on the local filesystem.

Mitigation: Prefer environment variables or a 0600 config file, avoid shared systems with weak filesystem controls, and rotate exposed keys.

Risk: Image edits involving real people, brands, artwork, news, or evidence can mislead viewers if material changes are not disclosed.

Mitigation: Obtain authorization, preserve locked factual regions, and clearly label substantive modifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-image-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples and generated image files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one user-selected reference image and an AI Hive API key.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-08-17T13:08:25Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
