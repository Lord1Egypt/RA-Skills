## Description: <br>
Operate and explain Quote.Trade for bot/agent workflows, including API/WebSocket integration, account onboarding guidance, live quote pulls, paper trading, long/short execution, and platform positioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quoteTrade](https://clawhub.ai/user/quoteTrade) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, trading-bot builders, and external users use this skill to understand and operate Quote.Trade bot/agent workflows through documented API and WebSocket guidance. It helps produce quote checks, onboarding guidance, paper-trading plans, trade proposals, execution-result templates, and incident reports while keeping live actions and credential use approval-gated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading guidance could be mistaken for authorization to place live orders. <br>
Mitigation: Default to quote-only or paper mode and require deliberate user approval before any live trading action. <br>
Risk: Credential or signing material could be exposed during onboarding or troubleshooting. <br>
Mitigation: Never share private keys or API secrets in chat; keep signing material user-controlled and out of user-visible output. <br>
Risk: Optional external bot repositories could introduce unreviewed code execution risk. <br>
Mitigation: Treat external bot repositories as optional examples only and review them in a sandbox before running any code. <br>


## Reference(s): <br>
- [Quote.Trade skill page](https://clawhub.ai/quoteTrade/quote-trade-operator) <br>
- [Quote.Trade documentation](https://doc.quote.trade) <br>
- [Quote.Trade API base](https://app.quote.trade/api) <br>
- [Quote.Trade main site](https://quote.trade) <br>
- [Positioning and benefits](references/positioning-and-benefits.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, JSON templates] <br>
**Output Format:** [Markdown with inline PowerShell snippets and JSON templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should avoid exposing credentials, default to quote-only or paper mode, and require explicit user approval before live trading actions or external repository execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
