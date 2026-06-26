## Description: <br>
Make x402 payments to access paid APIs and gated content. Use when a skill needs to fetch data from x402-gated endpoints (like Kaito mindshare API, Simmer premium endpoints, or any x402 provider). Handles 402 Payment Required responses automatically using USDC on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch x402-gated API data, check Base wallet balances, and make paid API or RPC calls using USDC on Base. Operators should define endpoint policy, spending caps, and wallet scope before enabling unattended use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real crypto payments automatically from the configured wallet, and on-chain transfers cannot be reversed. <br>
Mitigation: Use a dedicated low-balance wallet, set a tight X402_MAX_PAYMENT_USD value or --max cap, prefer dry-run or manual approval workflows, and restrict calls to trusted endpoints. <br>
Risk: Broad blockchain RPC access through the Quicknode command can expand what an unattended agent can query or trigger. <br>
Mitigation: Avoid generic RPC use in unattended workflows unless networks, methods, and call sites are explicitly reviewed and constrained. <br>
Risk: Wallet private keys are sensitive credentials required for payment signing. <br>
Mitigation: Store EVM_PRIVATE_KEY or WALLET_PRIVATE_KEY outside shell history, never commit secrets, use a scoped hot wallet instead of a treasury or trading wallet, and rotate keys after suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/simmer-x402) <br>
- [Publisher profile](https://clawhub.ai/user/simmer) <br>
- [Kaito x402 API documentation](https://github.com/MetaSearch-IO/KaitoX402APIDocs) <br>
- [Quicknode x402 documentation](https://x402.quicknode.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus CLI text or JSON responses from balance, fetch, and RPC commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute paid x402 requests and blockchain RPC calls when configured with wallet credentials and a funded Base wallet.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
