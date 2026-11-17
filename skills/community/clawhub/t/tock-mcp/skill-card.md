## Description:

Find Tock restaurants, view their bookable experiences and availability, and look up or verify reservations through the ContextMint Bridge browser extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Tock users and developers can find restaurants, compare bookable experiences and availability, and review or verify reservations. Restaurant discovery can work signed out; account lookups require a signed-in exploretock.com browser tab.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account tools can expose the user's Tock profile and reservations to the agent.

Mitigation: Use signed-out restaurant discovery when it is sufficient; connect a signed-in tab only for account lookups.

Risk: Pairing persists, and the external browser extension and server runtime are not verified by this review.

Mitigation: Review and pin the server version, verify the extension download, and approve only expected domains and capabilities.

## Reference(s):

- [tock-mcp npm package](https://www.npmjs.com/package/tock-mcp)
- [tock-mcp source repository](https://github.com/chrischall/tock-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Structured restaurant, experience, availability, reservation, and profile data with concise summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only data; account lookups require a signed-in exploretock.com browser tab.]

## Skill Version(s):

1.2.1 (source: evidence.json release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
