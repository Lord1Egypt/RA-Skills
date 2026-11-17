## Description:

Read Workday HR data (org chart, worker profiles, tasks, pay, benefits, compensation, your app menu) from a shell with the fpx CLI (@fetchproxy/cli) instead of running the workday-mcp server — fetch any *.htmld data endpoint through your own signed-in *.myworkday.com tab (SSO/Ping/Okta/Entra already cleared). Use when you want Workday data without the MCP, in a script, or on a machine where the MCP isn't installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Workday employees and developers use this skill to read tenant HR data from a shell or script when they want to use fpx without running the workday-mcp server. It guides setup and provides endpoint and jq projection examples for reading the data exposed by their signed-in Workday session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workday response envelopes contain a sessionSecureToken that could be exposed if raw responses are printed or saved.

Mitigation: Use the field-selecting jq projections in the endpoint reference; do not dump the raw response envelope.

Risk: The security review had medium confidence because some referenced materials were unavailable.

Mitigation: Review the referenced materials before installation if the incomplete review evidence is a concern.

## Reference(s):

- [Workday endpoint examples](references/endpoints.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [ClawHub skill release](https://clawhub.ai/chrischall/skills/workday-fpx)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and jq filters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only, tenant-scoped Workday data; examples project selected fields from JSON responses.]

## Skill Version(s):

1.8.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
