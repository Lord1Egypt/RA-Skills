## Description: <br>
On-chain yield discovery, transaction building, and portfolio management via the Yield.xyz API across 80+ networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apurvmishra](https://clawhub.ai/user/apurvmishra) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and agent developers use this skill to discover on-chain yield opportunities, inspect yield schemas, prepare unsigned transactions for wallet review, and manage yield positions through the Yield.xyz API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with approvals, swaps, deposits, claims, withdrawals, rebalances, broadcasts, and other fund-affecting DeFi workflows. <br>
Mitigation: Require wallet review and explicit user approval before every fund-affecting step, and treat generated transactions as proposals until the user approves them. <br>
Risk: Changing an unsigned transaction returned by the API can cause incorrect execution or permanent loss of funds. <br>
Mitigation: Pass unsigned transactions to the wallet unchanged; if an amount, fee, address, encoding, or other field is wrong, request a new action from the API instead of editing the transaction. <br>
Risk: Using shared API keys, scheduled checks, or multi-wallet tracking can expose activity to local storage and third-party services. <br>
Mitigation: Use a dedicated Yield.xyz API key, limit wallet tracking to the minimum needed, and avoid scheduled or multi-wallet automation unless the user accepts the privacy exposure. <br>


## Reference(s): <br>
- [Yield.xyz API Documentation](https://docs.yield.xyz) <br>
- [Yield.xyz Dashboard](https://dashboard.yield.xyz) <br>
- [Yield.xyz API Recipes](https://github.com/stakekit/api-recipes) <br>
- [OpenAPI specification](references/openapi.yaml) <br>
- [Safety checks and guardrails](references/safety.md) <br>
- [Chain transaction formats](references/chain-formats.md) <br>
- [Wallet integration](references/wallet-integration.md) <br>
- [Agent conversation examples](references/examples.md) <br>
- [Advanced yield workflows](references/superskill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; fund-affecting actions produce unsigned transactions for separate wallet review and signing.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and skill manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
