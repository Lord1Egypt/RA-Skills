## Description:

Read Voidly's internet-censorship index answer for one country, search recent incident records with evidence links, follow new records for a country, domain or incident type through a pull feed, and start a self-owned Voidly relay identity whose keys stay on the local machine. Uses plain curl GETs or the hosted MCP server at api.voidly.ai/mcp. Use when someone asks what Voidly shows for a country, which censorship or disruption incidents it has recorded, or wants to follow new incident records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emperormew](https://clawhub.ai/user/emperormew)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking internet-censorship measurements use Voidly to review country-level OONI anomaly signals and cited incident records, or to follow new records through a pull feed. Developers can also set up a self-owned relay identity and inbox for watch events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Country index signals and incident records can be misread as proof of a current block or deliberate disruption.

Mitigation: Include the data-as-of time and evidence links, describe the index as a 7-day OONI anomaly signal, distinguish disruption and suspected records, and do not claim current reachability.

Risk: Watch and relay features use an agent key; Voidly can read inbox watch notices, and the security scan did not fully assess the referenced local key-header file.

Mitigation: Use keyed features only when requested, keep key files readable only by the person, never expose keys in prompts or tool arguments, and explain that inbox notices are not end-to-end encrypted.

## Reference(s):

- [Voidly agent documentation](https://voidly.ai/agents)
- [Voidly hosted MCP server](https://api.voidly.ai/mcp)
- [Voidly A2A agent card](https://api.voidly.ai/v1/a2a/agent-card.json)
- [Voidly identity protocol](https://api.voidly.ai/v1/agents/start)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text or Markdown summaries with dates and evidence links; optional setup commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports recorded observations and their data-as-of time; does not assess current site reachability.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
