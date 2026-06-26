## Description: <br>
Run autonomous multi-agent OKX trading competitions where five AI agents use real-time market data, evolutionary selection, and exchange-level stop-losses to compare algorithmic trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peti0402](https://clawhub.ai/user/peti0402) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading researchers use this skill to set up autonomous multi-agent OKX trading competitions with real-time market data, strategy rotation, position sizing controls, and exchange-side stop-losses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run trading code with exchange credentials. <br>
Mitigation: Inspect the full trading code before installation, start in OKX demo mode, and use restricted API keys with withdrawals disabled. <br>
Risk: Autonomous trading and restart automation can continue placing or managing orders after an unexpected failure. <br>
Mitigation: Set exchange-side limits, verify stop-loss behavior, and define a clear monitoring and stop procedure before enabling any restart task. <br>
Risk: Telegram alerts may expose sensitive trading details. <br>
Mitigation: Avoid sending sensitive trading or credential-adjacent information through Telegram. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peti0402/trading-tournament) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with setup steps, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied OKX API credentials and local trading code review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
