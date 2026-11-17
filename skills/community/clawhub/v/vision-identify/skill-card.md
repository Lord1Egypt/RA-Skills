## Description:

拍照识万物 is a Chinese-language vision identification assistant that identifies visible content in uploaded images, analyzes scene context, and provides practical buying or compatibility guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanggz11](https://clawhub.ai/user/zhangyanggz11)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with uploaded images to identify objects, plants, animals, products, text, places, and scene conditions. It is especially oriented toward repair and shopping decisions where compatible parts, purchase keywords, or practical next steps are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images may contain IDs, faces, private documents, confidential workplace content, or other sensitive information.

Mitigation: Avoid submitting sensitive images unless the user is comfortable having them processed by the model; review organizational data handling requirements before use.

Risk: Broad image-recognition trigger phrases may invoke the skill whenever an image is present, including cases where routing was not intended.

Mitigation: Review the generated response when routing seems unexpected, especially before relying on identification, buying, repair, or compatibility advice.

Risk: Image identification and inferred purchase guidance can be uncertain for blurry images, mixed scenes, rare items, or compatibility-sensitive parts.

Mitigation: Use the skill's confidence notes and confirmation prompts, and verify critical specifications such as model numbers, sizes, sockets, or standards before purchase or repair.

## Reference(s):

- [Multimodal technical reference](references/multimodal.md)
- [ClawHub skill page](https://clawhub.ai/zhangyanggz11/skills/vision-identify)
- [Publisher homepage](https://wtmvw.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown response with image identification, scene analysis, shopping guidance, compatibility warnings, and confidence notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search keywords and purchase channel suggestions; does not execute tools or shell commands.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
