## Description:

Look up Redfin listings, property details, market reports, and saved homes or searches through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Home buyers, sellers, and homeowners can search Redfin listings, review property and market details, check climate risks, view saved homes or searches, and estimate mortgage payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Redfin's private web-app endpoints through a signed-in browser and a browser bridge, so availability can change and the bridge is part of the trusted setup.

Mitigation: Review the bridge release and its published checksum before installing it, and confirm listing, market, and climate details with Redfin before relying on them.

Risk: The security review is incomplete because a local path-like configuration reference could not be resolved; its benign verdict is not a safety guarantee.

Mitigation: Inspect the MCP configuration reference and setup files before enabling the integration.

## Reference(s):

- [redfin-mcp npm package](https://www.npmjs.com/package/redfin-mcp)
- [redfin-mcp project page (listed in the skill documentation)](https://github.com/chrischall/redfin-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, Structured data, Guidance]

**Output Format:** [Natural-language summaries and structured property, listing, market, and saved-item data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on Redfin availability; saved homes and searches require an authenticated Redfin browser session.]

## Skill Version(s):

1.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
