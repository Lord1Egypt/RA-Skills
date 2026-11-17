## Description:

Vgl helps agents write structured VGL JSON prompts for Bria FIBO models with explicit controls for image content, composition, lighting, camera settings, style, text rendering, and edit instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galbria](https://clawhub.ai/user/galbria)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and image-generation agents use this skill to convert natural-language image requests, image edits, masked edits, captions, or refinements into deterministic VGL JSON for Bria FIBO structured prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt contents may be sent to Bria when the generated VGL JSON is used with the disclosed API example.

Mitigation: Confirm the user intends to share prompt contents with Bria and use API keys only in environments they control.

Risk: Generated image prompts can encode unintended subject attributes, text, or edit scope if accepted without review.

Mitigation: Review the VGL JSON before using it for image generation or editing, especially object details, text_render, and edit_instruction.

## Reference(s):

- [VGL Output Schema Reference](references/schema-reference.md)
- [Bria image generation API endpoint](https://engine.prod.bria-api.com/v2/image/generate)
- [ClawHub skill page](https://clawhub.ai/galbria/skills/vgl)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object matching the VGL structured_prompt schema, with concise Markdown guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes object, background, lighting, aesthetics, camera, style, text_render, and edit_instruction fields.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
