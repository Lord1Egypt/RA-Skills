## Description: <br>
Adds a self-custodied crypto payment checkout to a Next.js and Supabase app for ETH, BTC, SOL, USDC, USDT, and other supported coins across multiple chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flacko2048](https://clawhub.ai/user/flacko2048) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add self-hosted crypto checkout, HD wallet address generation, blockchain polling, and fulfillment hooks to a Next.js App Router application backed by Supabase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner marks the release suspicious because the payment checker and fulfillment path need review before production use. <br>
Mitigation: Review and fix the payment confirmation path in staging before deployment, and make fulfillment idempotent. <br>
Risk: The master mnemonic controls all derived deposit wallets across chains. <br>
Mitigation: Use a dedicated mnemonic generated and stored offline or in a secrets manager, and never commit it to source control. <br>
Risk: Payment confirmation depends on external chain data and cron execution. <br>
Mitigation: Require transaction-specific confirmation evidence where appropriate, monitor the cron endpoint, and tightly control the cron secret and service-client permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flacko2048/self-hosted-crypto) <br>
- [CoinGecko price API](https://api.coingecko.com/api/v3/simple/price) <br>
- [mempool.space address API](https://mempool.space/api/address) <br>
- [Public Solana RPC endpoint](https://api.mainnet-beta.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration values, SQL migrations, TypeScript route handlers, and a React component.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration instructions and project files for an agent to adapt to the target application.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
