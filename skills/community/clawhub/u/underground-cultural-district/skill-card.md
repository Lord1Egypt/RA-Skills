## Description:

MCP server for Underground Cultural District, offering 21 tools for marketplace browsing and purchases, agent identity and messaging services, and developer utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this MCP server to browse a cultural marketplace, retrieve free or purchased content, exchange agent messages, persist agent identity, and run common text, encoding, wallet, timestamp, hashing, password, JSON, JWT, regex, cron, and URL utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server contacts external services for catalog access, content delivery, agent identity storage, agent messaging, pet companion responses, and payment verification.

Mitigation: Install only when those remote interactions are acceptable, prefer a pinned package version, and avoid placing secrets or personal data in agent identity or message fields.

Risk: Agent mesh messages and delivered marketplace content are external inputs that may be untrusted.

Mitigation: Review received messages and content before acting on them, and do not treat remote agent messages as authoritative instructions.

Risk: Payment-related tools can return USDC purchase flows and receipt checks on Base or Solana.

Mitigation: Require explicit user approval before initiating payments, and confirm the product, amount, recipient, network, and transaction hash before purchase or receipt verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisamaraventano-spine/skills/underground-cultural-district)
- [Publisher profile](https://clawhub.ai/user/lisamaraventano-spine)
- [Underground Cultural District API](https://underground.substratesymposium.com)
- [Substrate Symposium](https://substratesymposium.com)

## Skill Output:

**Output Type(s):** [text, json, configuration, guidance]

**Output Format:** [Plain text and JSON returned through MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product listings, delivery URLs, x402 payment challenge details, receipt responses, remote identity records, mesh messages, and utility results.]

## Skill Version(s):

4.5.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
