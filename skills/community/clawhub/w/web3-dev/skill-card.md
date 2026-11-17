## Description:

Helps agents build Web3 applications, scripts, CLIs, bots, mobile apps, and desktop apps that read blockchain data through the Blockscout PRO API across EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akolotov](https://clawhub.ai/user/akolotov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build direct HTTP integrations with the Blockscout PRO API for blockchain data such as transactions, blocks, addresses, tokens, NFTs, logs, contract context, internal transactions, account abstraction, and JSON-RPC contract-state reads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage broad searches of credential stores, project secret files, CI secrets, or persistent agent memory for BLOCKSCOUT_PRO_API_KEY.

Mitigation: Use this skill only when Blockscout PRO API integration is intended, provide the exact API-key location yourself, and avoid granting broad secret-store access unless you have reviewed what the agent can access.

Risk: Live API credentials could be exposed or reused without enough user awareness.

Mitigation: Keep API keys in environment variables, gitignored local secret files, or managed secret stores; never paste or log the full key, and confirm before using a key saved from a prior session.

Risk: Generated integrations can make live API calls and consume account credits or fail if request headers and authentication are wrong.

Mitigation: Review generated requests before execution, use a meaningful User-Agent and Accept header, monitor API responses and credit usage, and stop on authentication failures.

## Reference(s):

- [Blockscout for Web3 Dev on ClawHub](https://clawhub.ai/akolotov/skills/web3-dev)
- [Blockscout Agent Skills Repository](https://www.github.com/blockscout/agent-skills)
- [Blockscout Developer Portal](https://dev.blockscout.com)
- [Blockscout Support Discord](https://discord.gg/blockscout)
- [Blockscout PRO API Endpoint Index](references/pro-api-index.md)
- [Blockscout PRO API OpenAPI Specification](references/pro-api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, command snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP request examples and API-key handling guidance; live Blockscout PRO API calls require a user-provided API key.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
