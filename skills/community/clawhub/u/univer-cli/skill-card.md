## Description:

Terminal-native spreadsheet engine for Excel-compatible .xlsx operations: read, write, format, formula, charts, and multidimensional tables via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, edit, convert, and automate Excel-compatible .xlsx workflows from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a global npm CLI package can execute package lifecycle code and grant broad local access.

Mitigation: Verify that univer-cli is the intended package, prefer a pinned reviewed version or project-local install, and avoid elevated privileges unless the package has been separately reviewed.

Risk: Spreadsheet automation may change workbook formulas, formatting, charts, or exported data in ways that affect downstream decisions.

Mitigation: Review generated commands and inspect resulting workbook or export changes before using them in production workflows.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wuritu/skills/univer-cli)
- [Publisher profile](https://clawhub.ai/user/wuritu)
- [univer-cli npm package](https://www.npmjs.com/package/univer-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and the unv binary from the univer-cli npm package.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
