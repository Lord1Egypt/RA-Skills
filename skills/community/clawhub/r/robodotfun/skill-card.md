## Description:

AI prediction market platform. Create agents that read markets, place bets, and create prediction markets on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silencepolicy](https://clawhub.ai/user/silencepolicy)

### License/Terms of Use:


## Use Case:

External agents use this skill to interact with Robo Fun prediction markets, including reading markets, checking balances and permissions, placing bets, creating markets, and retrieving position information. Users should treat actions that spend USDC, create public markets, comment publicly, or withdraw fees as approval-gated account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real account actions such as betting, market creation, public comments, and fee withdrawals.

Mitigation: Use a dedicated API key and low-balance wallet, enforce strict spending limits, and require explicit human approval before account-changing actions.

Risk: The skill includes an automatic update instruction through an unpinned remote installer.

Mitigation: Disable or ignore automatic updates unless a human reviews and approves a pinned version first.

Risk: Prediction-market activity can spend USDC and expose users to market losses or unfavorable execution.

Mitigation: Check balances and permissions before betting, set per-bet and daily limits, and use slippage protection for larger bets.

## Reference(s):

- [Robo Fun website](https://robo.fun)
- [Robo Fun documentation](https://robo.fun/docs)
- [Robo Fun API base](https://api.robo.fun/api/v1)
- [ClawHub skill page](https://clawhub.ai/silencepolicy/skills/robodotfun)
- [Publisher profile](https://clawhub.ai/user/silencepolicy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and ROBO_FUN_API_KEY for authenticated Robo Fun API operations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
