## Description:

Retrieve real-time commodity price quotes via Octagon MCP, including current prices, day ranges, moving averages, and comparisons for metals, energy, and agricultural commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdm1136](https://clawhub.ai/user/wdm1136)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to ask an agent for current commodity quote data, compare commodity prices, and interpret day ranges, moving averages, volume, and 52-week range position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses mutable remote package execution through npx or installer commands.

Mitigation: Pin package versions where possible and review package provenance before installation.

Risk: The Octagon API key may be stored in persistent agent configuration files.

Mitigation: Use a protected secret mechanism and avoid sharing configuration files that contain credentials.

Risk: Reference setup material includes curl-to-bash style installation for Homebrew.

Mitigation: Prefer trusted package-manager installation paths and review installer scripts before execution.

Risk: Commodity quote analysis can be mistaken for trading advice.

Mitigation: Treat outputs as informational market data and require human review before financial decisions.

## Reference(s):

- [Octagon MCP Setup](references/mcp-setup.md)
- [Interpreting Commodities Quote Results](references/interpreting-results.md)
- [Octagon MCP GitHub](https://github.com/OctagonAI/octagon-mcp)
- [Octagon Documentation](https://docs.octagonagents.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with commodity quote summaries, interpretation tables, JSON MCP call examples, and shell or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Octagon MCP server and OCTAGON_API_KEY; quote data depends on upstream market-data freshness.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
