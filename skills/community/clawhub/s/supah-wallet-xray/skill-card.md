## Description: <br>
Instant wallet intelligence for any EVM address. Know who you're dealing with before you interact. Wallet age, transaction history, token holdings, DeFi activity, risk flags, ENS resolution, and a Trust Score (0-100). Works across 21+ EVM chains. x402 USDC micropayments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to profile EVM wallets or ENS names before copying trades, accepting payments, interacting with contracts, or performing wallet due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet or ENS queries are sent to SUPAH and ENS Ideas. <br>
Mitigation: Avoid submitting confidential customer or investigation targets unless those providers are trusted for the use case. <br>
Risk: Scans can trigger x402 USDC charges of up to $0.05 per scan. <br>
Mitigation: Use a limited Base wallet and require manual confirmation before each scan. <br>
Risk: Broad prompts may trigger paid external lookups without a clear per-scan confirmation step. <br>
Mitigation: Configure the agent to ask for confirmation before running the wallet scan command. <br>


## Reference(s): <br>
- [SUPAH Wallet X-Ray on ClawHub](https://clawhub.ai/supah-based/supah-wallet-xray) <br>
- [Supported Chains](references/supported-chains.md) <br>
- [SUPAH API](https://api.supah.ai) <br>
- [x402 Protocol](https://www.x402.org) <br>
- [ENS Ideas API](https://api.ensideas.com/ens/resolve/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with a saved JSON response file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an address or ENS name plus an optional chain; writes the raw API response to /tmp/wallet-xray-result.json.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
