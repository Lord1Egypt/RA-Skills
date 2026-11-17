## Description:

Transforms reference images or text descriptions into interactive UI prototypes, generating self-contained HTML by default and Figma-compatible design artifacts only when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhappy](https://clawhub.ai/user/zhappy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to turn screenshots or UI descriptions into browser-previewable prototypes for review, iteration, testing, or design handoff. Figma output is optional and requires an explicit request and a Figma access token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Figma path reads local access-token files from multiple locations.

Mitigation: Use a dedicated, revocable Figma token with minimal scope, and prefer HTML-only use when Figma output is not required.

Risk: The packaging script could accidentally include credential files if real auth profiles are kept inside the skill package directory.

Mitigation: Keep real auth-profiles.json files outside the skill package tree and inspect packaged contents before distribution.

Risk: Generated output paths can be risky if requested names are not controlled.

Mitigation: Use trusted output directories and review generated files before opening, sharing, or committing them.

## Reference(s):

- [Design Tokens](references/DESIGN_TOKENS.md)
- [HTML Components](references/HTML_COMPONENTS.md)
- [Figma Components](references/FIGMA_COMPONENTS.md)
- [Examples](references/EXAMPLES.md)
- [Figma API Documentation](https://www.figma.com/developers/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML/CSS/JavaScript files by default; optional Figma JSON or Figma file URL with setup guidance when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default HTML use requires no external token; optional Figma generation depends on a user-provided Figma access token.]

## Skill Version(s):

1.0.0 (source: package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
