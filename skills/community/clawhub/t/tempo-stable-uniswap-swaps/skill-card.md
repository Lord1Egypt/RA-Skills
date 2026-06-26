## Description: <br>
Provides agent-facing guidance for checking Tempo token balances, transferring pathUSD, and preparing Uniswap swaps on Tempo mainnet with quoting, approvals, simulation, and broadcast steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to prepare Tempo mainnet token balance checks, pathUSD transfers, and Uniswap swap workflows. It is intended for wallet-aware execution where a human reviews transaction targets, allowances, calldata, gas terms, and simulation results before broadcast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Tempo mainnet wallet-signing commands that move real funds. <br>
Mitigation: Use a dedicated low-balance wallet and review every token, recipient, spender, calldata target, gas term, and simulation result before broadcasting. <br>
Risk: The approval examples include broad token and Permit2 allowances. <br>
Mitigation: Prefer finite approvals sized to the intended swap and revoke token or Permit2 allowances after use. <br>
Risk: A stale quote or incorrect transaction field can cause failed swaps or unintended execution. <br>
Mitigation: Refresh quotes, confirm spender and swap target values, and require a successful simulation before sending any transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aviclaw/tempo-stable-uniswap-swaps) <br>
- [Tempo RPC endpoint](https://rpc.presto.tempo.xyz) <br>
- [Uniswap Trade API quote endpoint](https://trade-api.gateway.uniswap.org/v1/quote) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human review before signing or broadcasting transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
