## Description:

Generate images via VVMAI's OpenAI-compatible Images API, supporting nano-banana and gpt-image model series with URL output by default and optional local saves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leevigoo](https://clawhub.ai/user/leevigoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate or edit AI images through VVMAI from natural-language prompts, with options for model choice, aspect ratio, image count, and save location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, API credentials, and optional edit images to the configured VVMAI-compatible endpoint.

Mitigation: Use the skill only with a trusted VVMAI endpoint, keep VVMAI_BASE_URL pinned to the intended HTTPS service, and avoid sensitive prompts or images.

Risk: Remote --input URLs and local edit inputs can expose user content or local files during image editing.

Mitigation: Avoid remote --input URLs and review any local image path before running edit mode.

Risk: Custom filenames and save paths need review because weak destination validation can create unexpected local writes.

Mitigation: Avoid path components in --filename and use explicit, trusted output directories until destination validation and download limits are improved.

## Reference(s):

- [VVMAI API](https://api.vvmai.com)
- [ClawHub Skill Page](https://clawhub.ai/leevigoo/skills/vvmai-image-gen)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration guidance]

**Output Format:** [MEDIA URL or local MEDIA path lines, with optional saved image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, VVMAI_API_KEY, and a VVMAI-compatible HTTPS base URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
