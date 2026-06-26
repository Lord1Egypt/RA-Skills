## Description: <br>
Binance Spot request using the Binance API. Authentication requires API key and secret key. Supports testnet and mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Awessh](https://clawhub.ai/user/Awessh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to query Binance Spot market and account endpoints and prepare authenticated Spot API requests against testnet or mainnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Binance Spot trading actions using API credentials. <br>
Mitigation: Use testnet first, use restricted API keys with withdrawals disabled and IP allowlisting, and require explicit confirmation before order, cancel, amend, or cancel-replace actions. <br>
Risk: Binance API keys or secret keys could be exposed through chat or saved markdown. <br>
Mitigation: Do not paste production secrets into chat or markdown files; mask credentials when displaying account information. <br>


## Reference(s): <br>
- [Binance Authentication](references/authentication.md) <br>
- [Binance Spot API](https://api.binance.com) <br>
- [Binance Spot Testnet](https://testnet.binance.vision) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with endpoint tables, inline shell commands, and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports authenticated and unauthenticated Binance Spot endpoints with testnet and mainnet base URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact metadata version 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
