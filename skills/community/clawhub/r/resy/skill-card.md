## Description:

Manage Resy restaurant reservations via MCP — search venues, book tables, list and cancel reservations, manage favorites, and subscribe to Priority Notify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find restaurants and available tables, review their reservations, manage favorites and availability alerts, and book or cancel tables with confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration accesses a Resy account and may store an authentication token.

Mitigation: Use a reviewed, pinned server version, check the extension's requested permissions, and protect the token cache or disable it with RESY_TOKEN_CACHE=false.

Risk: Bookings and cancellations can involve fees or have uncertain outcomes.

Mitigation: Keep confirmations enabled, review the action preview and any fee, and check the reservation list before retrying an unknown result.

## Reference(s):

- [resy-mcp package](https://www.npmjs.com/package/resy-mcp)
- [Repository linked in the skill documentation](https://github.com/chrischall/resy-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)

## Skill Output:

**Output Type(s):** [Text, Structured reservation data, Account actions]

**Output Format:** [Natural-language responses and structured reservation data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reservation details, account information, booking or cancellation results, and confirmation prompts.]

## Skill Version(s):

1.4.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
