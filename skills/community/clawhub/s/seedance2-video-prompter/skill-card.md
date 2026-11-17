## Description:

Generates structured English prompts for Seedance 2.0 video generation from Chinese user requests, including modes for text-only, frame-guided, and multi-reference workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wild-river2016](https://clawhub.ai/user/wild-river2016)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to turn Chinese video concepts into concise Seedance 2.0 prompts with asset mapping, timed scene beats, sound layers, negative constraints, and generation settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes copyright and platform-review avoidance guidance that could be used to imitate protected brands, characters, or styles.

Mitigation: Review or remove that guidance before deployment, and use only original or properly licensed references.

Risk: Broad trigger terms may cause the skill to activate for ordinary video, storyboard, or product-promo requests.

Mitigation: Scope activation terms or route usage through reviewer-approved video-prompt workflows.

## Reference(s):

- [Seedance 2.0 video prompter on ClawHub](https://clawhub.ai/wild-river2016/skills/seedance2-video-prompter)
- [Seedance 2.0 prompt recipe library](references/recipes.md)
- [Camera language and visual style glossary](references/camera-and-styles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown text prompt with mode, asset mapping, final prompt, negative constraints, and generation settings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are intended to follow the Seedance limits documented in the skill, including a 2000-character prompt cap and 4-15 second single-segment duration.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
