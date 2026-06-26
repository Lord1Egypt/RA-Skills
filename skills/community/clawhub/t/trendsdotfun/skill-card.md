## Description: <br>
Creates a coin on trends.fun and deploys a Meteora DBC liquidity pool on Solana mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poploli2](https://clawhub.ai/user/poploli2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate token creation on trends.fun, upload token media and metadata, and create a Meteora DBC pool using a local Solana wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill signs Solana mainnet transactions with a local wallet and can spend real SOL, including an optional first buy. <br>
Mitigation: Use a dedicated low-balance wallet, confirm the wallet address and balance before execution, and review the --first-buy value before running commands. <br>
Risk: Unsafe setup wording could lead an agent or user to reveal private key material. <br>
Mitigation: Never print, paste, upload, or share the Solana keypair or private key; only confirm that the keypair file exists and is readable locally. <br>
Risk: Token images, metadata, and created pools are public and may be difficult or impossible to undo. <br>
Mitigation: Review name, symbol, description, image, URL, pool configuration, and RPC endpoint before submitting any transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poploli2/trendsdotfun) <br>
- [Publisher profile](https://clawhub.ai/user/poploli2) <br>
- [Pinata file upload API](https://docs.pinata.cloud/api-reference/endpoint/files/upload) <br>
- [trends.fun](https://trends.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pnpm; optionally uses SOLANA_RPC_URL and TRENDS_POOL_CONFIG.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
