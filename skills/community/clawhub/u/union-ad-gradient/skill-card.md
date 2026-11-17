## Description:

Union Ad Gradient helps agents turn user-provided content into UnionSkill-branded gradient-style advertising presentations through outline confirmation, slide image generation, and PPTX assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing teams use this skill to create UnionSkill-branded advertising slide decks from text, documents, images, or conversation context. It is suited for creative design, brand marketing, visual presentations, business roadshows, exhibition materials, customer proposals, and open-source release promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enforces UnionSkill promotional branding in generated deliverables.

Mitigation: Use it only when branded UnionSkill presentations are intended; choose a different presentation workflow for clean or customer-specific unbranded decks.

Risk: Presentation assembly depends on a local ppt-generator assembler that runs code during deck generation.

Mitigation: Install and run the assembler only from a trusted, access-controlled, pinned environment before using the skill for production deliverables.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/timo2026/skills/union-ad-gradient)
- [UnionSkill website](https://www.unionskillai.com)
- [Style guide](artifact/references/style_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with slide outline text, image-generation prompt requirements, shell command examples, and generated presentation file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected deliverables include a PPTX deck, slide image ZIP, cooperation note text file, and optional HTML full-screen presentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
