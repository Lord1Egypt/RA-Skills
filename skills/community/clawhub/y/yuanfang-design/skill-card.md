## Description:

Shared design system for yuanfang-skills that provides token CSS variables, theme overrides, and reusable layout-type HTML blocks for visually consistent rendered output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyuanfang](https://clawhub.ai/user/iyuanfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add, inspect, and maintain Yuanfang visual themes and layout blocks for social-image and presentation-style rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Locale-specific language and font defaults may be inappropriate for locale-neutral output.

Mitigation: Review the Chinese language and font defaults before using generated designs in broader or locale-neutral contexts.

Risk: The showcase generator writes local showcase files and imports a sibling yuanfang-html-image module.

Mitigation: Run the showcase generator only inside the intended Yuanfang workspace after confirming the sibling module is present.

## Reference(s):

- [Yuanfang Design Authoring Guide](references/authoring-guide.md)
- [shadcn Registry Schema](https://ui.shadcn.com/schema/registry.json)

## Skill Output:

**Output Type(s):** [guidance, code, configuration, shell commands]

**Output Format:** [Markdown guidance with CSS, HTML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces design-system changes and instructions; showcase generation writes local HTML files when run in the intended Yuanfang workspace.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
