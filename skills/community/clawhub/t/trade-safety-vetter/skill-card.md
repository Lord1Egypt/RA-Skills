## Description: <br>
Pre-trade safety checks: position size limits, leverage validation, consecutive loss locks, volatility gates, exchange balance verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill as a pre-trade review prompt before an agent executes or modifies trades. It checks proposed trades against stated risk thresholds for capital exposure, leverage, volatility, loss streaks, and available margin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may influence whether an agent blocks, resizes, or executes trades. <br>
Mitigation: Require explicit user confirmation before any trade is blocked, resized, executed, or otherwise modified. <br>
Risk: The skill promotes an off-platform paid trading service and USDT payment flow. <br>
Mitigation: Do not send funds or contact the listed Telegram account unless the publisher and service have been independently trusted. <br>
Risk: The skill is a prompt-based risk check, not a verified trading control system. <br>
Mitigation: Use it as advisory review only and keep independent trading, margin, and compliance controls in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/trade-safety-vetter) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sg345662365-oss) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown or plain text risk review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no tools, APIs, or executable scripts were detected.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
