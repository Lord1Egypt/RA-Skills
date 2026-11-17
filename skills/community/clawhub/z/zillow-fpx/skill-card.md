## Description:

Use the fpx CLI and a signed-in browser tab to retrieve Zillow listings, property details and histories, photos, market reports, and saved data without the Zillow MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External developers can use this skill to retrieve Zillow listing, property, price and tax history, photo, market report, and signed-in saved-home data from a shell when they do not want to use the Zillow MCP server.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Some setup references could not be resolved, so installation details may be incomplete.

Mitigation: Review the setup instructions and verify the ContextMint Bridge release before installing.

## Reference(s):

- [ClawHub release](https://clawhub.ai/chrischall/skills/zillow-fpx)
- [Zillow pages and data fields](references/pages.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Zillow property and market data summarized as text or structured JSON, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields depend on the Zillow page; saved searches and saved homes require a signed-in Zillow tab.]

## Skill Version(s):

1.3.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
