## Description: <br>
Trade stocks, options, and crypto on brokerages, including Robinhood, ETrade, Charles Schwab, Webull, Public, Tastytrade, Coinbase, and Kraken, via the Trade It API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanmauro](https://clawhub.ai/user/deanmauro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users connect brokerages, inspect account data, draft stock, options, and crypto orders, and execute trades after explicit confirmation through Trade It. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive brokerage data and help submit real trades. <br>
Mitigation: Install it only when brokerage access is intended, use hosted Trade It review flows where practical, and revoke the access token when finished. <br>
Risk: Order-creating or order-executing commands can affect live brokerage accounts. <br>
Mitigation: Require explicit user confirmation before every order-creating or order-executing action, avoid immediate-placement modes, and review order details before submission. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deanmauro/trade-it) <br>
- [Publisher Profile](https://clawhub.ai/user/deanmauro) <br>
- [Trade It Homepage](https://tradeit.app) <br>
- [Trade It API Reference](artifact/references/api-reference.md) <br>
- [Trade It Enums and Constants](artifact/references/enums.md) <br>
- [Integration Patterns for AI Agents and Chatbots](artifact/references/integration-patterns.md) <br>
- [Trade It Security](artifact/references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TRADEIT_ACCESS_TOKEN; helper output redacts sensitive-looking fields by default.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence, created 2026-03-24T04:07:56Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
