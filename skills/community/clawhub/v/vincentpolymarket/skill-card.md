## Description: <br>
Polymarket prediction market trading for agents that can create wallets, browse markets, place bets, manage positions, and withdraw funds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to set up a Vincent Polymarket wallet, inspect markets and order books, place or manage trades, redeem resolved positions, and withdraw USDC.e under configured owner policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents real-money Polymarket trading and withdrawal authority. <br>
Mitigation: Review carefully before installing, claim the wallet before funding it, configure strict spending limits, mandatory approvals, and withdrawal controls, and only use funds you can afford to lose. <br>
Risk: The initial wallet flow can have weak controls until the wallet owner claims it and sets policies. <br>
Mitigation: Use the claim URL promptly, fund the wallet only after owner policies are configured, and revoke or rotate agent access when needed. <br>
Risk: Re-link tokens and unpinned CLI execution can expose account access or supply-chain risk. <br>
Mitigation: Avoid sharing re-link tokens in ordinary chat when possible and prefer pinned or otherwise reviewed CLI versions instead of relying on @latest. <br>


## Reference(s): <br>
- [Vincent homepage](https://heyvincent.ai) <br>
- [ClawHub skill page](https://clawhub.ai/glitch003/vincentpolymarket) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses @vincentai/cli commands and declared local credential paths for the agent wallet.] <br>

## Skill Version(s): <br>
1.0.70 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
