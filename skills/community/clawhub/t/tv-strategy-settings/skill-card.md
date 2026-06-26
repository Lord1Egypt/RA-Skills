## Description: <br>
Opens and modifies TradingView strategy settings on the current chart page, including inputs and strategy properties such as stop loss, take profit, initial capital, commission, and slippage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariuswang007](https://clawhub.ai/user/mariuswang007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
TradingView users and agents use this skill to adjust settings for an already-loaded strategy on an open chart. It is intended for changing visible strategy inputs and properties through browser automation, not for creating strategies or writing Pine Script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation may change financial strategy settings on the wrong TradingView tab, strategy, parameter, or value. <br>
Mitigation: Before clicking Ok or Apply, confirm the active TradingView tab, strategy name, parameter label, and new value against the visible settings dialog. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariuswang007/tv-strategy-settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, browser automation commands] <br>
**Output Format:** [Markdown with browser automation command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step browser actions for locating a TradingView chart, opening strategy settings, modifying fields, applying changes, and verifying the result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
