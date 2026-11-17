## Description:

Earn and spend Nano (XNO) with other agents. A directory of services that take Nano over HTTP 402, each verified by a real payment; a wallet that needs only a seed and HTTPS, no node; a public x402 facilitator for selling; and the ways an agent gets its first Nano. Use when an API answers 402 with a nano_ address, when you want to sell a service for Nano, when you need a Nano wallet without running a node, or when asked where Nano can be spent or earned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pursekeeper](https://clawhub.ai/user/pursekeeper)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers and operators use Pursekeeper to set up a Nano wallet, find Nano-accepting services, pay HTTP 402 requests, or offer services for Nano. Operators can also use its localhost proxy to fund supported model calls from a capped wallet balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An uncertain payment failure followed by an automatic retry can result in paying twice.

Mitigation: Check the original block hash and reconcile the pending payment before attempting another payment; require durable pending-payment reconciliation for unattended use.

Risk: Anyone with the wallet seed can control its funds.

Mitigation: Use a dedicated wallet funded only with an amount you can afford to spend, and keep the seed private.

Risk: Requests can send content to external service providers.

Mitigation: Send only approved content to external providers and review dependency versions.

## Reference(s):

- [Pursekeeper website](https://pursekeeper.dev)
- [Nano wallet guide](artifact/references/no-node.md)
- [Nano seller directory guide](artifact/references/sellers.md)
- [Buying inference with Nano](artifact/references/buy-from-nanogpt.md)
- [Inference proxy guide](artifact/references/inference-proxy.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JavaScript code, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and JavaScript scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional wallet and localhost-proxy scripts; Nano payments are irreversible.]

## Skill Version(s):

0.3.13 (source: SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
