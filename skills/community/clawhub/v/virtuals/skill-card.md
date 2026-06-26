## Description: <br>
Virtuals Protocol integration for OpenClaw. Create, manage and trade tokenized AI agents on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rojasjuniore](https://clawhub.ai/user/rojasjuniore) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use this skill to inspect Virtuals Protocol market data, check token balances, and access CLI guidance for creating and trading tokenized AI agents on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI asks users to provide and persist a raw wallet private key. <br>
Mitigation: Do not enter a main wallet private key; use a fresh disposable wallet with minimal funds and treat ~/.openclaw/virtuals/config.json as containing a recoverable wallet secret. <br>
Risk: The documentation warns testnet-only, while the implementation points to Base mainnet. <br>
Mitigation: Verify the configured network before using funded wallet operations or relying on balance and trading behavior. <br>
Risk: Crypto trading and agent creation workflows can require funds and external services. <br>
Mitigation: Review commands before execution, confirm costs and contract addresses independently, and avoid using funds beyond a disposable testing amount. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rojasjuniore/virtuals) <br>
- [Virtuals homepage](https://virtuals.io) <br>
- [Virtuals app](https://app.virtuals.io) <br>
- [Virtuals agent creation app](https://fun.virtuals.io) <br>
- [Virtuals whitepaper](https://whitepaper.virtuals.io) <br>
- [GAME SDK](https://github.com/game-by-virtuals/game-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and Markdown documentation with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call external Virtuals, CoinGecko, and Base RPC endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
