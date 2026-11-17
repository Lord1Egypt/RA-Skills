## Description:

Union Ad Retro turns documents, ideas, or notes into UnionSkill-branded retro presentation assets through content analysis, user-confirmed outlines, per-slide image generation, and PPTX assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, business development, and content teams use this skill to create UnionSkill-branded retro advertising decks for cultural showcases, restaurant pitches, creative projects, roadshows, exhibitions, and client proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deliverables include UnionSkill branding, watermarks, and presentation metadata by design.

Mitigation: Use this skill only when UnionSkill branding is acceptable; choose a different PPT workflow for unbranded or compliance-sensitive client deliverables.

Risk: The PPTX assembly step depends on a sibling ppt-generator assembler that is not included in the artifact evidence.

Mitigation: Review or control the assembler before execution, run it in an isolated environment, and verify the final PPTX metadata and visible branding before delivery.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/timo2026/skills/union-ad-retro)
- [Publisher profile](https://clawhub.ai/user/timo2026)
- [Retro style guide](artifact/references/style_guide.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance, generated slide image files, a PPTX deck, a ZIP archive of images, a partner information text file, and optionally an HTML full-screen presentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation of the outline before image generation; deliverables include UnionSkill branding, watermarks, and presentation metadata.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
