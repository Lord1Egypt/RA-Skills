## Description:

Re-theme your OpenClaw dashboard with 104 curated design seeds from SeedFlip. Fonts, colors, shadows, radii. One command, instant transformation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bockenstette1](https://clawhub.ai/user/bockenstette1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dashboard builders use this skill to fetch SeedFlip design seeds and apply the returned CSS variables, console snippets, or themes.json entries to an OpenClaw dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form theme queries and result metadata may be sent to SeedFlip when get_design_seed is used.

Mitigation: Avoid confidential project, customer, or unreleased product details in theme queries unless that telemetry is acceptable.

Risk: Unversioned npx installation can execute a package version that has not been reviewed.

Mitigation: Pin seedflip-mcp to an exact reviewed version in MCP configuration.

Risk: Generated CSS, console snippets, or theme entries may change the dashboard appearance in unintended ways.

Mitigation: Preview theme changes before applying or saving them to the dashboard.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bockenstette1/skills/seedflip-theme)
- [SeedFlip homepage](https://seedflip.co)
- [SeedFlip MCP npm package](https://www.npmjs.com/package/seedflip-mcp)
- [Publisher profile](https://clawhub.ai/user/bockenstette1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with CSS variables, JSON theme entries, console snippets, and MCP setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the SeedFlip MCP server to return one or more design seeds in tokens, CSS, Tailwind, shadcn, or OpenClaw formats.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
