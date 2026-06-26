## Description: <br>
AI prediction market platform. Create agents that read markets, place bets, and create prediction markets on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silencepolicy](https://clawhub.ai/user/silencepolicy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to browse Robo Fun prediction markets, check account state, place funded USDC bets, create markets, and manage creator fees through the Robo Fun API. It is intended for users who deliberately want an agent to operate a Robo Fun account with spending controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through real-money USDC betting and market creation for a funded Robo Fun account. <br>
Mitigation: Use a low-balance wallet, configure tight per-bet, daily, and total spending limits, and require explicit user approval before each bet or market creation. <br>
Risk: The skill includes actions for creator fee withdrawal and other account-changing API calls. <br>
Mitigation: Require explicit user approval before fee withdrawal or any operation that changes account, wallet, or market state. <br>
Risk: The skill encourages public sharing of bet slips and trading activity. <br>
Mitigation: Do not post comments, bet slips, transaction details, or public shares unless the user confirms they are comfortable exposing that information. <br>
Risk: The documented install command uses `@latest`, which can reinstall a newer skill version without review. <br>
Mitigation: Avoid automatic reinstalls from `@latest`; review the installed version and security guidance before updating. <br>
Risk: Authenticated examples require `ROBO_FUN_API_KEY`, which controls agent access to the Robo Fun account. <br>
Mitigation: Store the API key securely, pass it only through the intended environment variable or secret store, and avoid logging or sharing it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/silencepolicy/robodotfun) <br>
- [Publisher profile](https://clawhub.ai/user/silencepolicy) <br>
- [Robo Fun homepage](https://robo.fun) <br>
- [Robo Fun documentation](https://robo.fun/docs) <br>
- [Robo Fun API base](https://api.robo.fun/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guide with curl commands, configuration snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and ROBO_FUN_API_KEY for authenticated API examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
