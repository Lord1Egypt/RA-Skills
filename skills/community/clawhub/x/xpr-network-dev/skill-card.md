## Description:

Comprehensive knowledge for XPR Network blockchain development - smart contracts, CLI, web SDK, DeFi, NFTs, and infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgnz](https://clawhub.ai/user/paulgnz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill as a reference for building XPR Network smart contracts, dApps, backend services, DeFi/NFT integrations, payments, and node operations. It helps agents produce guidance, code examples, shell commands, and configuration patterns for XPR Network workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples involving blockchain signing can expose private keys if copied into shell arguments, environment variables, logs, or agent memory.

Mitigation: Use the documented CLI keychain, KMS-backed signing, or tightly scoped secret-manager keys; keep private keys out of shell arguments and environment variables.

Risk: Generated transaction, permission, cron, or node-setup commands may affect real assets or privileged infrastructure.

Mitigation: Require human review before execution, verify target accounts and contracts, and test on XPR testnet before mainnet use.

Risk: Payment and event examples can become unsafe if webhooks are unauthenticated or processed more than once.

Mitigation: Authenticate webhook payloads, de-duplicate events by transaction or event identifier, and reconcile payments before fulfillment.

Risk: Smart contract schema changes can make deployed table data unreadable.

Mitigation: Do not modify existing table structures with live data; add new tables or migrate intentionally after review and testnet validation.

Risk: Using an incorrect DEX deposit memo can make funds unrecoverable.

Mitigation: Verify DEX transfer memo requirements before signing; for Metal X DEX deposits, use the documented empty memo.

Risk: Infrastructure setup examples may download packages or expose node services if run without hardening.

Mitigation: Pin and verify packages and npm dependencies, restrict node services behind hardened networking, and review firewall and service settings before launch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulgnz/skills/xpr-network-dev)
- [XPR Network documentation](https://docs.xprnetwork.org)
- [XPR Network explorer](https://explorer.xprnetwork.org)
- [XPR Network resources portal](https://resources.xprnetwork.org)
- [Metal X API documentation](https://api.dex.docs.metalx.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, command examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference-oriented outputs should be reviewed before executing transactions, deployment commands, or infrastructure changes.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
