## Description:

Professional Figma design analysis and asset export for extracting design data, exporting assets, auditing accessibility, analyzing design systems, and generating design documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yylgit](https://clawhub.ai/user/yylgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and design system teams use this skill to inspect Figma files, export assets and design tokens, and generate accessibility or style audit reports for handoff and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write exported assets, manifests, design tokens, and reports to local paths.

Mitigation: Run exports in a dedicated working directory and review output paths before keeping or sharing generated files.

Risk: Generated HTML reports may include content controlled by a Figma file.

Mitigation: Avoid opening HTML reports from untrusted Figma files until path containment and HTML escaping have been reviewed and fixed.

Risk: The skill requires a Figma access token and its setup guidance mentions storing the token in a .env file.

Mitigation: Use a minimally scoped token and only store it in a gitignored, permission-restricted .env file when environment variables are not sufficient.

## Reference(s):

- [Figma API Reference](references/figma-api-reference.md)
- [Design Patterns and Component Best Practices](references/design-patterns.md)
- [Accessibility Guidelines for Figma Design](references/accessibility-guidelines.md)
- [Export Formats and Specifications](references/export-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, JSON results, HTML reports, and exported asset files such as PNG, SVG, PDF, and WEBP.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Figma access token and can write generated reports, manifests, design tokens, and exported assets to local paths.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
