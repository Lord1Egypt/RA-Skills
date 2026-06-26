## Description: <br>
Manage AIUSD trading, staking, withdrawals, balance checks, gas top-ups, and transaction history via authenticated backend calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChaunceyLiu](https://clawhub.ai/user/ChaunceyLiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let a personal assistant check AIUSD account state and perform trading, staking, withdrawal, gas top-up, deposit guidance, and transaction-history workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate financial actions including trades, staking, withdrawals, and gas top-ups. <br>
Mitigation: Require manual confirmation of amount, asset, chain, destination, fees or slippage, and final action before execution. <br>
Risk: Installer scripts run local code, extract packages, install dependencies, and may replace an existing aiusd-skill directory. <br>
Mitigation: Inspect the extracted package and back up any existing aiusd-skill directory before running installer scripts. <br>
Risk: Authentication setup and re-authentication can change local credential state. <br>
Mitigation: Install only from a trusted publisher and use a controlled local environment for OAuth tokens and cached credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ChaunceyLiu/trade-with-aiusd) <br>
- [AIUSD Official Website](https://aiusd.ai) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with inline shell commands and JSON-like tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated AIUSD access before account or trading operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence; artifact build metadata states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
