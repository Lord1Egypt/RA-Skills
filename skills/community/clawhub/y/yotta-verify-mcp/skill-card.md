## Description:

Exposes pre-install static scanning for skills and MCP servers through tools that return verdicts, CI gate results, badges, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and MCP client users use the server to assess skills and packages before installation, enforce scan verdicts in CI, and generate findings and reports. Scan results require human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some scan targets may execute untrusted code despite the scanner's stated non-execution behavior.

Mitigation: Prefer the bundled Python scanner on existing local directories. Avoid npm or Git target retrieval until it is restricted to script-free registry downloads, and pin and review any npm version used to launch the server.

Risk: A scan result or audited badge may be treated as proof of safety even though external releases and runtime containment were not verified.

Mitigation: Review the actual scan report rather than relying on an audited badge. Preview installer changes with --dry-run and back up an existing installation.

## Reference(s):

- [Project repository](https://github.com/YottaMeta/yotta-verify-mcp)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-verify-mcp)
- [ClawHub release](https://clawhub.ai/yottameta/skills/yotta-verify-mcp)
- [Trust checklist](references/trust-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, SVG badge]

**Output Format:** [MCP tool responses, JSON and Markdown reports, and an SVG audit badge]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verdicts, findings, severity counts, and CI gate results; scan conclusions need human review.]

## Skill Version(s):

0.4.7 (source: frontmatter, CHANGELOG, package.json, server.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
