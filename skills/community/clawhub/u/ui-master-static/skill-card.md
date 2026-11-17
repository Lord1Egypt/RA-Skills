## Description:

Ui Master Static guides agents building production-grade user interfaces with native CSS and BEM, including token architecture, layout patterns, modern effects, accessibility, and performance checks for projects that avoid CSS frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to create or improve static HTML/CSS interfaces without Tailwind, CSS-in-JS, or a utility framework. It supports plain Vite and static-site work involving headers, dashboards, landing layouts, token systems, BEM structure, modern CSS effects, and accessibility/performance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UI code can misuse optional animation, localStorage theme toggles, or Houdini Paint API snippets.

Mitigation: Review generated code before use, especially motion behavior, browser support fallbacks, and client-side storage snippets.

Risk: Effects such as scroll animation, parallax, 3D transforms, and Paint API usage can reduce accessibility or fail in unsupported browsers.

Mitigation: Require prefers-reduced-motion handling and progressive-enhancement fallbacks for advanced CSS effects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anjasta-tarigan/skills/ui-master-static)
- [Publisher Profile](https://clawhub.ai/user/anjasta-tarigan)
- [CSS Architecture: Tokens + BEM](references/css-architecture-bem.md)
- [Layout Patterns: Native CSS](references/layout-patterns.md)
- [Modern Effects Catalogue: Native CSS](references/modern-effects.md)
- [Accessibility & Performance: Production Floor](references/accessibility-performance-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline HTML, CSS, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated output should be reviewed for accessibility, reduced-motion behavior, browser support fallbacks, and maintainable BEM/token structure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
