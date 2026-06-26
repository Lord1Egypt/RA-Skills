## Description: <br>
Exchange cryptocurrencies via kyc.rip aggregator API. Use when swapping, converting, or exchanging crypto assets. Supports 700+ coins, no KYC, best rates across 10+ providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbtoshi](https://clawhub.ai/user/xbtoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for agent guidance when estimating cryptocurrency swaps, creating trades, validating wallet addresses, and checking trade status through the kyc.rip swap aggregator API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides real cryptocurrency transfers, which may be irreversible once funds are sent. <br>
Mitigation: Before creating a trade or sending funds, independently verify the provider, asset, network, amount, rate, destination address, refund address, memo or tag, minimums, and deposit address. <br>
Risk: Wallet and transaction metadata may be shared with third-party swap providers. <br>
Mitigation: Review provider privacy, KYC, and logging policies before using a route, especially when selecting no-KYC or privacy bridge options. <br>


## Reference(s): <br>
- [KYC.RIP API base URL](https://api.kyc.rip) <br>
- [ClawHub release page](https://clawhub.ai/xbtoshi/swap-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, JSON, Shell commands] <br>
**Output Format:** [Markdown with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cryptocurrency swap parameters, provider routes, wallet addresses, memos, and trade status fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
