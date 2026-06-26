## Description: <br>
Adjusts tradebot parameters incrementally to improve tradability based on market regime and diagnostic signals while preserving risk controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[motivationationdaily](https://clawhub.ai/user/motivationationdaily) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to tune trading-bot parameters when diagnostics show persistent gate failures or long periods without trades. It supports stepwise adjustments with logging, risk caps, halt conditions, and verification after each change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-bot parameter changes can affect real money if applied directly to live trading. <br>
Mitigation: Use the skill only with a clearly identified bot, confirmed daily loss caps, max-trade limits, and halt controls; prefer backtesting or paper trading before live use. <br>
Risk: Autonomous tuning could change strategy behavior without adequate human oversight. <br>
Mitigation: Require explicit approval for each parameter change and log before-and-after values for every tuning cycle. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/motivationationdaily/tradebot-tuning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instructional tuning ladder with safety checks and verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
