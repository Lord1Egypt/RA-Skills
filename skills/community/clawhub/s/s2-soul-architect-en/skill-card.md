## Description:

Generate and customize AI agent characters using a 16-class system with physical embodiment support, including branded AI companions and local SOUL.md prompt output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate English SOUL.md persona profiles with class archetypes, embodiment parameters, and SVG visual code for AI companions or embodied agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SOUL.md persona text is designed to influence an agent's style and identity across later use.

Mitigation: Review the generated text before pasting it into a persistent system prompt, and keep required safety or policy rules outside generated persona content.

Risk: Generated SVG and embodiment blocks may be copied into downstream profiles or files without review.

Mitigation: Inspect generated JSON and SVG text before reuse, especially when adapting it for branded companions or physical embodiments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-soul-architect-en)
- [Project homepage](https://taohuayuan.world)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)
- [Space2 EAM Protocol Whitepaper 2026 EN](artifact/docs/Space2_EAM_Protocol_Whitepaper_2026_EN.md)
- [S2 Visual cyber-feline sample](artifact/sample/cat_companion_S2_Visual.svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown containing JSON and SVG code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local CLI text for review and manual use; generated SOUL.md content should be reviewed before being used as a persistent system prompt.]

## Skill Version(s):

3.0.0 (source: server release metadata, manifest.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
