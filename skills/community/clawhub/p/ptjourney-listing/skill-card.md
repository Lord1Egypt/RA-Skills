## Description:

Helps sellers prepare 1688 product listings, preflight batches, and manage authorized Ozon, Wildberries, and TEMU listing tasks through a locally connected PTJourney client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qique](https://clawhub.ai/user/qique)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and listing operators use this skill to prepare marketplace product data, check batches for errors, and manage listing tasks after explicit approval. It requires a separately installed, signed-in PTJourney Windows client and its official local MCP runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating or controlling listing tasks can have business consequences.

Mitigation: Review the account, store, item count, pricing, and target task; obtain explicit user approval before business-impacting actions.

Risk: The separately downloaded runtime may be untrusted or mismatched.

Mitigation: Download the official PTJourney MCP package and verify its published SHA-256 before connecting it.

Risk: Marketplace credentials or session files could be exposed to an AI chat.

Mitigation: Keep tokens and session files on the local client; do not provide them in chat.

Risk: Retrying an uncertain submission may create duplicate listings.

Mitigation: Check the platform task and product identifier before retrying; preflight corrected data and use a new idempotency key only for confirmed failures.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qique/skills/ptjourney-listing)
- [PTJourney product site](https://ptjourney.qique.cn/)
- [MCP installation and connection](references/mcp-setup.md)
- [Listing data contract](references/data-contract.md)
- [MCP tool contract](references/mcp-contract.md)
- [Platform requirements](references/platforms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured listing data, Configuration guidance]

**Output Format:** [Markdown guidance and structured product-listing data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preflight results and task statuses are obtained from the connected client; creating a task does not guarantee a successful marketplace listing.]

## Skill Version(s):

0.2.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
