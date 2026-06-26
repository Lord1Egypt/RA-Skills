## Description: <br>
Fetch token swap quotes and executable calldata from the spanDEX API. Use when a user wants to swap tokens, get best price or fastest routing, and receive wallet-ready EVM transaction payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougalcantara](https://clawhub.ai/user/dougalcantara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch swap quotes, inspect routes, and prepare wallet-ready transaction payloads for token swaps on Base. Execution workflows use Privy wallets and should be paired with calldata verification for stronger safety. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare and submit real crypto transactions, and one fallback path may execute with reduced calldata verification. <br>
Mitigation: Prefer quote-only or dry-run mode first, install onchain-verify-transaction before execution, and manually review the wallet, tokens, amounts, recipient, spender, slippage, API endpoint, and transaction details before any swap. <br>
Risk: A compromised or unexpected API endpoint could return unsafe transaction payloads. <br>
Mitigation: Use a pinned SPANDEX_URL value, avoid changing it unless directly instructed by the user, and verify transaction effects before signing. <br>
Risk: Autonomous wallet execution can move real assets from the selected account. <br>
Mitigation: Use a limited Privy wallet with spending controls and confirm wallet ownership before sending transactions. <br>


## Reference(s): <br>
- [spanDEX skill page](https://clawhub.ai/dougalcantara/spandex-agentic-swap) <br>
- [spanDEX](https://spandex.sh) <br>
- [spanDEX docs](https://docs.spandex.sh) <br>
- [Privy](https://privy.io) <br>
- [Privy Interop Notes](references/privy.md) <br>
- [Token Reference - Base](references/tokens.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JSON transaction payloads, and transaction status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces quote summaries, dry-run execution steps, wallet-ready EVM calldata, approval and swap transaction guidance, and Basescan transaction links.] <br>

## Skill Version(s): <br>
0.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
