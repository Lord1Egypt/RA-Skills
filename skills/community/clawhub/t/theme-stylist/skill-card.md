## Description:

主题样式师 helps agents recommend and apply visual themes for presentations, documents, reports, and HTML pages, including palettes, fonts, CSS variables, and consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to improve the visual consistency of business presentations, documents, data reports, and HTML landing pages. It can generate reusable theme guidance such as color palettes, font pairings, CSS variables, and style-check reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports broad command, file, browser, and credential-related authority with unclear limits.

Mitigation: Run the skill in a constrained workspace and require explicit approval for output paths, overwrites, dependency installs, browser actions, and any shell commands.

Risk: The skill may read or write presentation, document, report, and HTML assets while applying themes.

Mitigation: Use copies or version control for source files and review generated theme files, CSS variables, and style changes before applying them to production materials.

Risk: Optional font, CDN, CSS toolchain, or integration steps may require network access or credentials.

Mitigation: Prefer local or trusted dependencies, avoid providing API keys unless a specific trusted integration requires them, and keep credentials out of generated theme configuration.

## Reference(s):

- [ClawHub skill page: theme-stylist](https://clawhub.ai/thcjp/skills/theme-stylist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, CSS, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local theme files such as theme.json, variables.css, previews, and style reports when the host agent has file-write authority.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
