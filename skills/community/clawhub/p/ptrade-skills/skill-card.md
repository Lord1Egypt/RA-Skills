## Description: <br>
Provides three PTrade quantitative trading strategies for small-cap selection, factor and ATR risk control, and sector rotation through deployable Python strategy files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martin-sh-ni](https://clawhub.ai/user/martin-sh-ni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Quantitative developers and trading operators use this skill to review, adapt, and deploy PTrade strategy code for small-cap equity selection, multi-factor momentum selection with ATR controls, and sector ETF rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains live-trading strategy code with credible safety defects that could cause unintended financial exposure. <br>
Mitigation: Do not run it against a live brokerage account until order semantics and black-swan protection are fixed and tested in paper trading. <br>
Risk: Automated order submission could create unwanted or duplicate positions if controls are incomplete. <br>
Mitigation: Use explicit position limits, a kill switch, duplicate-order protection, and manual approval before live order submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/martin-sh-ni/ptrade-skills) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, guidance] <br>
**Output Format:** [Markdown guidance with Python strategy files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for review and testing before any live brokerage use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
