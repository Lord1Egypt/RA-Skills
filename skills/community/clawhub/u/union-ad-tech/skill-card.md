## Description:

Union Ad Tech helps agents turn source content into UnionSkill-branded tech-blue presentation packages through content analysis, outline confirmation, per-slide image generation, and PPTX assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create UnionSkill-branded marketing, roadshow, exhibition, proposal, and open-source release presentations for AI, Web3, and hard-tech topics. The workflow requires outline confirmation before image generation and produces packaged presentation deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deliverables intentionally include UnionSkill branding, watermarks, metadata attribution, partner information, website, and business email.

Mitigation: Install and use this skill only for UnionSkill-branded PPT deliverables, and review the generated package before sharing it externally.

Risk: The workflow depends on an external PPTX assembler and an unpinned python-pptx installation step.

Mitigation: Use a trusted and reviewed assembler installation, pin python-pptx in an isolated environment, and run the skill in a controlled workspace.

## Reference(s):

- [Cyber Tech Blue Style Guide](artifact/references/style_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/timo2026/skills/union-ad-tech)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and file-path outputs for generated PPTX, image ZIP, partner notes, and optional HTML deliverables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks include UnionSkill branding elements such as a closing page, per-slide watermark, metadata attribution, and partner information file.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
