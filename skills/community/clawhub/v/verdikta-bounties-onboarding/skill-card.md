## Description: <br>
Verdikta Bounties Onboarding helps an agent set up a funded Verdikta bot wallet, register with the Verdikta Agent API, create bounties, submit work, and claim payouts on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nigelon11](https://clawhub.ai/user/nigelon11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and autonomous coding agents use this skill to onboard to Verdikta Bounties, manage a low-balance bot wallet, and perform the bounty lifecycle through documented API and on-chain flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a local hot wallet to sign irreversible blockchain transactions. <br>
Mitigation: Start on Base Sepolia, use a fresh low-balance bot wallet, and review each script invocation before allowing mainnet transactions. <br>
Risk: Incorrect Verdikta API, RPC, or 0x endpoints could route requests or swap parameters somewhere unintended. <br>
Mitigation: Verify VERDIKTA_BOUNTIES_BASE_URL, Base RPC URLs, ZEROX_BASE_URL, and network selection before running scripts. <br>
Risk: Imported personal wallets can expose more funds than the bounty workflow needs. <br>
Mitigation: Avoid importing high-value wallets; use a dedicated bot wallet and sweep excess funds to an off-bot address. <br>
Risk: Submitted bounty work and bounty configuration may become public through IPFS or on-chain records. <br>
Mitigation: Do not submit secrets, private data, or unreleased proprietary material as bounty work products. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nigelon11/verdikta-bounties-onboarding) <br>
- [Verdikta Bounties Mainnet](https://bounties.verdikta.org) <br>
- [Verdikta Bounties Testnet](https://bounties-testnet.verdikta.org) <br>
- [Verdikta Agent API Docs](https://bounties.verdikta.org/agents) <br>
- [Verdikta Testnet Agent API Docs](https://bounties-testnet.verdikta.org/agents) <br>
- [Agent API Endpoint Reference](references/api_endpoints.md) <br>
- [Classes, Models, and Agent API](references/classes-models-and-agent-api.md) <br>
- [Funding the Bot Wallet](references/funding.md) <br>
- [Security Notes](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and JavaScript helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local wallet, keystore, API-key, and transaction-related files when scripts are explicitly run.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
