## Description: <br>
Trade crypto on Weex exchange via Telegram bot, enabling agents to check prices, view balances, run DCA strategies, execute grid trading, and manage a Weex portfolio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tesseraeventures](https://clawhub.ai/user/tesseraeventures) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to connect OpenClaw agents to a Telegram-based Weex trading workflow for price checks, balance review, DCA automation, grid strategies, and portfolio monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to send live exchange API credentials to an unverified Telegram bot that can place real trades. <br>
Mitigation: Do not send credentials unless the operator is independently verified and trusted; use a restricted spot-only key with withdrawals disabled. <br>
Risk: Automated DCA, grid, or order workflows can create unintended financial exposure. <br>
Mitigation: Keep balances small, require manual confirmation before live orders or strategies, and monitor active strategies regularly. <br>
Risk: API credentials may be exposed if shared in an unsafe chat context. <br>
Mitigation: Never share API keys in group chats and remove credentials with the documented disconnect flow when no longer needed. <br>


## Reference(s): <br>
- [Weex V3 API Reference](references/weex-api.md) <br>
- [Weex API Docs](https://www.weex.com/en/api) <br>
- [Weex Trading Skill Page](https://clawhub.ai/tesseraeventures/weex-trading) <br>
- [tesseraeventures Publisher Profile](https://clawhub.ai/user/tesseraeventures) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with Telegram bot commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users through exchange API credential setup, Telegram bot commands, DCA strategies, grid trading, and Weex REST API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
