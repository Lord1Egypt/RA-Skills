## Description:

Layers AI images and video in depth (soft foreground, sharp subject, hazy background) and fixes flat frames. Prompts for H3, Seedance, Kling, FLUX, GPT Image, Nano Banana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xnirlin](https://clawhub.ai/user/0xnirlin)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use the skill to write layered prompts for AI image and video models, check prompts for depth cues, and revise flat shots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The depth checker relies on English keyword patterns, so prompts in other languages may receive incomplete depth feedback.

Mitigation: Treat the checker score as a reminder and inspect the generated frame directly; adapt the prompt or review it manually when writing in another language.

## Reference(s):

- [Depth recipes](artifact/references/depth-recipes.md)
- [Model templates with the depth stack](artifact/references/model-templates.md)
- [Ziztu](https://getziztu.com)
- [Ziztu connector](https://getziztu.com/mcp)
- [ClawHub skill page](https://clawhub.ai/0xnirlin/skills/ziztu-cinematic-depth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Prompt text, depth-check guidance, Markdown recipes and model templates, with optional Python CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The depth checker reports per-shot scores and notes; its score is a reminder, and the generated frame remains the final check.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
