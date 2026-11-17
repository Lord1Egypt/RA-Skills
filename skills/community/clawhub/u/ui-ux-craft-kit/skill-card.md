## Description:

UI/UX CraftKit provides searchable UI/UX design intelligence for web and mobile interfaces, including styles, color palettes, font pairings, product recommendations, UX guidelines, chart guidance, and stack-specific implementation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hardikamal](https://clawhub.ai/user/hardikamal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and AI coding assistants use this skill to retrieve ranked UI/UX recommendations while planning, building, reviewing, or improving web and mobile interfaces. It is suited for interface structure, visual design decisions, accessibility checks, typography, color systems, charts, responsive behavior, and design-system generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --persist can create or overwrite Markdown design-system files, including outside the intended folder when paths are crafted.

Mitigation: Keep output paths inside the current project, avoid untrusted project or page names, and review generated files before treating them as authoritative instructions.

Risk: Design recommendations may be incomplete or mismatched for a specific product, audience, accessibility requirement, or brand system.

Mitigation: Use the skill output as design guidance, then validate contrast, keyboard access, responsive behavior, and product-specific requirements during implementation review.

## Reference(s):

- [UI/UX CraftKit README](artifact/README.md)
- [UI/UX CraftKit Skill Instructions](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/hardikamal/skills/ui-ux-craft-kit)
- [ClawHub Publisher Profile](https://clawhub.ai/user/hardikamal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or ASCII text, with optional persisted Markdown design-system files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are ranked from bundled CSV data. Optional persistence can create or overwrite Markdown files under a design-system directory.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact manifest lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
