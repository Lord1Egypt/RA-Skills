## Description:

Search, analyze, and trade on Manifold Markets prediction markets. Use when the user wants to look up prediction market odds, place bets, check their portfolio, or discuss Manifold markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverstone-louis](https://clawhub.ai/user/silverstone-louis)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Manifold Markets odds, check account and portfolio state, and operate Manifold bets, positions, and limit orders through the Manifold API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place bets, sell shares, and cancel orders using the user's Manifold API key.

Mitigation: Treat bet, sell, and cancel as live account actions and require explicit user confirmation of the exact market ID, order ID, amount, outcome, and answer ID before execution.

Risk: Bet placement supports live execution without an enforced confirmation step.

Mitigation: Use the documented dry-run option first for bet requests and only proceed after the user confirms the returned order details.

Risk: The skill requires access to MANIFOLD_API_KEY for authenticated actions.

Mitigation: Install and run it only when the user accepts agent access to their Manifold account, and avoid exposing the API key in prompts, logs, or shared files.

## Reference(s):

- [Manifold API endpoint](https://api.manifold.markets/v0)
- [ClawHub skill page](https://clawhub.ai/silverstone-louis/skills/silk-manifold)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON from command-line tool calls, with Markdown command examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and MANIFOLD_API_KEY for authenticated account actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
