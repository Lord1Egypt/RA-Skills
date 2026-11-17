## Description:

Monitors selected V2EX forum nodes and account notifications, then generates Markdown summary reports and MCP-accessible JSON text results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minglu6](https://clawhub.ai/user/minglu6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor configured V2EX nodes, retrieve account notifications, and expose V2EX lookup tools through an MCP service. It is useful for scheduled forum monitoring, report generation, and agent-assisted V2EX queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a V2EX API token and stores the token in local configuration.

Mitigation: Use a limited or revocable token, keep the configuration file out of shared workspaces and logs, and rotate the token after testing or exposure.

Risk: The security guidance warns against use on untrusted networks until TLS verification is fixed.

Mitigation: Run the skill only in a trusted network environment or review and fix TLS verification before broader deployment.

Risk: MCP tool responses or retained logs may expose V2EX account data or token-related context.

Mitigation: Limit who can access MCP output and logs, and avoid retaining sensitive execution transcripts longer than needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minglu6/skills/v2ex-monitor)
- [V2EX API base endpoint](https://www.v2ex.com/api/v2)
- [V2EX token settings](https://www.v2ex.com/settings/tokens)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown reports, JSON text returned by MCP tools, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local report and tracking files for seen topics and notifications.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
