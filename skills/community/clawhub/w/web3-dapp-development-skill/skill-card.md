## Description:

Industry-standard Web3 DApp architecture skill covering account abstraction, embedded wallets, gasless approvals, on-chain indexing, testing, RPC failover, vault key management, event-driven architecture, and multi-chain EVM/Solana patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanpoldark](https://clawhub.ai/user/stanpoldark)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to scaffold, review, and implement production-oriented Web3 DApp architecture across frontend, backend, smart contracts, indexing, wallets, authentication, deployment, and security workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-token guidance may lead to reusable JWTs in URLs for SSE.

Mitigation: Prefer same-site HttpOnly cookies or short-lived, single-use SSE tickets.

Risk: Private-key and environment setup guidance could be misapplied with funded mainnet keys or committed secrets.

Mitigation: Use placeholder values only, keep .env out of source control, and use hardware wallets or managed secret storage for mainnet deployment.

Risk: Automated trading, signing, deployment, and strategy-worker behavior can perform high-impact actions if implemented without explicit limits.

Mitigation: Require user controls, spending limits, slippage bounds, and human review before enabling automated on-chain actions.

## Reference(s):

- [Web3-Dapp-Master on ClawHub](https://clawhub.ai/stanpoldark/skills/web3-dapp-development-skill)
- [Alchemy](https://alchemy.com)
- [Infura](https://infura.io)
- [ZeroDev](https://zerodev.app)
- [Pimlico](https://pimlico.io)
- [Privy](https://privy.io)
- [Dynamic](https://dynamic.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, Solidity, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project scaffolds, environment-variable templates, smart-contract patterns, and security checklists; review before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
