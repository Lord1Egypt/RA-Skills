## Description:

Generates three distinct UI design variations from a prompt using scenario-specific references and the Impeccable design system, then supports iteration, critique, token extraction, and export to HTML or React.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuqingnicole](https://clawhub.ai/user/yuqingnicole)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to generate divergent, working UI directions for dashboards, landing pages, mobile apps, editorial pages, e-commerce flows, education tools, and creative interfaces, then refine or export the chosen direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read nearby project files to infer brand and UI context.

Mitigation: Review the files used for context and confirm generated design-context comments before retaining them.

Risk: Generated UI code may include external font imports or design choices that are not production-ready.

Mitigation: Review generated code, external font imports, accessibility behavior, and responsive states before production use.

## Reference(s):

- [Variant design community](https://variant.com)
- [Impeccable design system](https://github.com/tychografie/impeccable)
- [Dashboard reference](references/dashboard.md)
- [Editorial reference](references/editorial.md)
- [SaaS reference](references/saas.md)
- [E-commerce reference](references/ecommerce.md)
- [Education reference](references/education.md)
- [Creative reference](references/creative.md)
- [Mobile reference](references/mobile.md)
- [Palette reference](references/palettes.md)
- [Typography reference](references/design-system/typography.md)
- [Color and contrast reference](references/design-system/color-and-contrast.md)
- [Spatial design reference](references/design-system/spatial-design.md)
- [Motion design reference](references/design-system/motion-design.md)
- [Interaction design reference](references/design-system/interaction-design.md)
- [Responsive design reference](references/design-system/responsive-design.md)
- [UX writing reference](references/design-system/ux-writing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with HTML or React code blocks and optional CSS, JSON, or Tailwind token snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include three labeled visual directions, iteration actions, critiques, alternate views, and design tokens.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
