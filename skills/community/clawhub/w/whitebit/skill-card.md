## Description:

Build, install, update, and use a WhiteBIT trading guidance and training skill through ClawHub for OpenClaw, including trading workflow training, API behavior validation, and MCP-first execution planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zonder](https://clawhub.ai/user/zonder)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and trading workflow trainers use this skill to install or manage the ClawHub WhiteBIT skill, teach WhiteBIT spot trading workflows, validate API request requirements, and prepare documented execution plans for a separate reviewed executor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake documentation-based planning for live exchange execution or account verification.

Mitigation: State that the skill is documentation-only with whitebit-docs, require a separate reviewed executor for live trading, and require explicit human approval before any live trade.

Risk: API keys or local credentials could be exposed during external executor setup or ClawHub publishing.

Mitigation: Keep API keys out of skill files, exclude local credential artifacts before publishing, and rotate keys immediately if exposure occurs.

Risk: Unverified global CLI installation or bulk updates could introduce unwanted skill or dependency changes.

Mitigation: Verify or pin the ClawHub CLI package before global installation and use dry-run for bulk ClawHub operations.

Risk: Incorrect symbols, order size, slippage, or retry handling could lead to harmful trades if copied into an execution system.

Mitigation: Validate endpoint requirements through WhiteBIT documentation, require symbol, side, order type, size, and constraints, and reconcile uncertain order status before any retry.

## Reference(s):

- [ClawHub WhiteBIT Skill Homepage](https://clawhub.ai/zonder/whitebit)
- [ClawHub WhiteBIT Skill Page](https://clawhub.ai/zonder/skills/whitebit)
- [WhiteBIT Docs MCP Server](https://docs.whitebit.com/mcp)
- [MCP Setup](references/mcp-setup.md)
- [ClawHub CLI Reference](references/clawhub-cli.md)
- [WhiteBIT API Basics](references/whitebit-api-basics.md)
- [Trade Checklist](references/trade-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, API request details, and operator checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only for WhiteBIT access unless a separate execution system is configured; outputs should not claim live order placement or account verification.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
