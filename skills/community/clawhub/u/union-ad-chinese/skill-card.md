## Description:

UnionSkill国潮中国风广告PPT。图像型工作流：内容分析→大纲确认→逐页生图→PPTX装配。适合文化展示、政府汇报、高端制造。

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, business teams, and agents use this skill to turn documents, notes, or ideas into UnionSkill-branded Chinese-style advertising PPT decks. It is intended for cultural presentations, government reporting, high-end manufacturing materials, roadshows, exhibitions, client proposals, and open source release materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill adds non-optional UnionSkill branding, including watermarks, a closing slide, author metadata, and contact information.

Mitigation: Review generated presentations before sharing and use the skill only when UnionSkill branding is acceptable for the audience and deliverable.

Risk: The Python entry point runs an out-of-package PPT assembler that was not included in the reviewed artifact.

Mitigation: Audit, vendor, or otherwise review the referenced PPT assembler before running the Python entry point in a production or sensitive environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/union-ad-chinese)
- [Style Guide](references/style_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese-language outline text, image-generation prompts, shell commands, and generated PPTX, PNG, ZIP, TXT, and optional HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user outline confirmation before image generation; outputs include mandatory UnionSkill branding, watermark, closing slide, and presentation metadata.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
