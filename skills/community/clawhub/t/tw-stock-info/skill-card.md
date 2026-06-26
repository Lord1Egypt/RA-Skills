## Description: <br>
Taiwan stock info using Fugle or FinMind APIs. Provides real-time quotes, historical data, financial statements, and technical indicators for Taiwan stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hans00](https://clawhub.ai/user/hans00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and market-analysis users use this skill to ask an agent for Taiwan stock data workflows, including real-time quotes, historical prices, financial statements, and technical indicators from Fugle and FinMind APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fugle API keys or FinMind tokens may be exposed if used directly in chat history, shell history, or logs. <br>
Mitigation: Use scoped or revocable credentials where possible, avoid pasting production secrets into agent prompts, and rotate credentials if exposure is suspected. <br>
Risk: Requests could be directed to unintended endpoints if API examples are modified without review. <br>
Mitigation: Confirm requests are sent only to the documented Fugle and FinMind domains before execution. <br>


## Reference(s): <br>
- [Taiwan Stock Info ClawHub release](https://clawhub.ai/hans00/tw-stock-info) <br>
- [Fugle API](https://api.fugle.tw) <br>
- [FinMind API v4](https://api.finmindtrade.com/api/v4/data) <br>
- [Fugle API Specifications](api/fugle.md) <br>
- [FinMind API Specifications](api/finmind.md) <br>
- [Usage Examples](example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline cURL commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint guidance, authentication header examples, rate-limit notes, and response examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
