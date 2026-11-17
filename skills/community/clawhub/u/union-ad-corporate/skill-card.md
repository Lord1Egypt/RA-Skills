## Description:

Union Ad Corporate helps agents create UnionSkill-branded corporate-blue presentation decks by analyzing source material, confirming an outline, generating full-slide images, and assembling a PPTX package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create UnionSkill-branded business presentations for B2B proposals, annual reports, roadshows, exhibitions, and customer pitches. The workflow requires outline confirmation before slide image generation and PPTX assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deliverables automatically include UnionSkill branding, watermarking, presentation metadata, and a cooperation file.

Mitigation: Install and use the skill only for intended UnionSkill-branded presentation work, and review generated decks before sharing.

Risk: The PPTX assembly path depends on a sibling ppt-generator assembler outside this skill package.

Mitigation: Run the assembler only when the sibling dependency is trusted and protected from local tampering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/union-ad-corporate)
- [Enterprise business style guide](references/style_guide.md)
- [UnionSkill website](https://www.unionskillai.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands, plus generated PPTX, PNG ZIP, text, and optional HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user outline confirmation before image generation; generated decks include UnionSkill branding, watermarking, metadata, and a cooperation file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
