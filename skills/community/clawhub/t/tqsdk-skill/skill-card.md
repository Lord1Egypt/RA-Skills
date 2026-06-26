## Description: <br>
Explains, implements, and debugs TqSdk Python workflows for market data, update loops, account selection, orders, positions, simulation, backtesting, and common TqSdk errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinny-xuyida](https://clawhub.ai/user/shinny-xuyida) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to answer TqSdk questions and produce concise Python guidance or snippets for market data, trading account workflows, order lifecycle handling, simulation, backtesting, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading examples may affect a real broker account if run with live account credentials or order and cancellation calls. <br>
Mitigation: Before running generated code, confirm whether it targets local simulation, Quick simulation, backtest, or a real broker account, and execute live order code only when that account action is intended. <br>
Risk: Trading workflows can expose or misuse account credentials if copied directly into scripts or shared prompts. <br>
Mitigation: Protect TqAuth and broker credentials, keep secrets out of shared code, and review generated snippets before execution. <br>


## Reference(s): <br>
- [Account Type Matrix](references/account-type-matrix.md) <br>
- [Accounts And Trading](references/accounts-and-trading.md) <br>
- [Error FAQ](references/error-faq.md) <br>
- [Example Map](references/example-map.md) <br>
- [Market Data](references/market-data.md) <br>
- [Object Fields](references/object-fields.md) <br>
- [Order Functions And Position Tools](references/order-functions-and-position-tools.md) <br>
- [Simulation And Backtest](references/simulation-and-backtest.md) <br>
- [wait_update And The Update Loop](references/wait-update-and-update-loop.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include runnable TqSdk snippets, API call recommendations, troubleshooting steps, and account-mode cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
