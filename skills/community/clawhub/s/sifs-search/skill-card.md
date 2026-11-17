## Description:

Use this skill when you need to find code in a local checkout or Git source by behavior, intent, symbol, file path, related implementation, or indexed chunk context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code-focused agents use this skill to search local checkouts or Git source by behavior, symbols, paths, related implementation, and indexed chunk context before reading broad sets of files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external sifs CLI package that may be unpinned.

Mitigation: Install SIFS only from a trusted package source and prefer a pinned or verified SIFS release when possible.

Risk: Code search or indexing could run against an unintended source tree.

Mitigation: Pass an explicit --source value and run SIFS only against source trees intended for indexing or inspection.

Risk: Generated agent instructions or force installs could introduce stale or incorrect guidance.

Mitigation: Preview generated agent instructions, use dry-run checks where available, and review instructions before force installing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/skills/sifs-search)
- [SIFS Command Recipes](references/commands.md)
- [SIFS MCP Rules](references/mcp.md)
- [SIFS Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local sifs binary on PATH; MCP use is optional when the tools are visible in the active agent session.]

## Skill Version(s):

0.1.0 (source: server release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
