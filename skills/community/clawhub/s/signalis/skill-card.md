## Description:

Signalis helps agents access cross-domain intelligence digests and AI-business narrative tracking through free API endpoints and paid x402 calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to integrate Signalis API endpoints for current intelligence digests, historical lookups, and Pulse narrative data. It guides agents to test free response shapes before making paid x402 requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 examples can spend real USDC on Base Mainnet.

Mitigation: Use the free endpoints first to verify response shapes and use a dedicated low-balance wallet for paid calls.

Risk: Wallet private keys could be exposed through shared logs or agent environments.

Mitigation: Keep PRIVATE_KEY out of shared logs and avoid placing production wallet keys in general-purpose agent environments.

Risk: Model-generated intelligence and narrative analysis may be imperfect or stale.

Mitigation: Check each response's createdAt provenance and freshness indicators before relying on the information.

## Reference(s):

- [ClawHub Signalis Skill](https://clawhub.ai/jcislo/skills/signalis)
- [Publisher Profile](https://clawhub.ai/user/jcislo)
- [Signalis Website](https://signalis.dev)
- [Signalis API](https://api.signalis.dev)
- [OpenAPI Specification](https://api.signalis.dev/openapi.json)
- [x402 Payment Manifest](https://api.signalis.dev/.well-known/x402)
- [A2A Agent Card](https://api.signalis.dev/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint tables, curl examples, and TypeScript x402 client code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes free endpoint guidance, paid endpoint pricing, Base Mainnet payment requirements, and response freshness notes]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
