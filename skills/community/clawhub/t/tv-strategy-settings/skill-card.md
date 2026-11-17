## Description:

Open and modify TradingView strategy settings on the current chart page, including inputs and properties such as stop loss, take profit, periods, initial capital, commission, slippage, and order size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariuswang007](https://clawhub.ai/user/mariuswang007)

### License/Terms of Use:


## Use Case:

External users and trading strategy operators use this skill to adjust parameters for an already-loaded TradingView strategy through browser automation, using natural-language requests or exact parameter names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate an open TradingView chart UI and change strategy settings.

Mitigation: Install only when agent-driven TradingView UI automation is desired, and review requested parameter changes before relying on updated strategy results.

Risk: Changed strategy settings can affect financial analysis or trading decisions.

Mitigation: Treat recalculated strategy results as decision-support information and independently review them before making financial decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline browser automation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies to the currently open TradingView chart with a loaded strategy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
