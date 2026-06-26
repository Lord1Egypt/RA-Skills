## Description: <br>
Search, list, and resolve xStocks tokenized-stock mints on Solana, with guidance for using Jupiter and wallet tools to buy supported tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manu-xmint](https://clawhub.ai/user/manu-xmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify xStocks tokens, retrieve Solana mint addresses, and prepare standard Jupiter swap flows for supported tokenized stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading instructions may cause an agent to treat a casual confirmation or amount as permission to execute real-money blockchain purchases too quickly. <br>
Mitigation: Keep wallet-level confirmations enabled and independently verify the token mint, amount, payment token, quote, fees, slippage, destination wallet, and network before approving any transaction. <br>
Risk: The hardcoded xStocks catalog may become stale as new tokens launch or token data changes. <br>
Mitigation: Check the latest xStocks token API before relying on a mint address for a transaction. <br>


## Reference(s): <br>
- [Jupiter agent-skills](https://github.com/jup-ag/agent-skills) <br>
- [xStocks token API](https://api.xstocks.fi/api/v1/token) <br>
- [ClawHub skill page](https://clawhub.ai/manu-xmint/xstocks-beta) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return token names, symbols, Solana mint addresses, transaction-preparation guidance, or script output.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
