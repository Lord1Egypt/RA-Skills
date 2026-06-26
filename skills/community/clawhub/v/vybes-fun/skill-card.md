## Description: <br>
vybes.fun is a Solana token launchpad skill for launching tokens, generating AI logos, creating prediction markets, building token websites, and checking earnings through APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aicre8dev](https://clawhub.ai/user/aicre8dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to interact with Vybes APIs for Solana token launches, logo generation, prediction-market creation and betting, token website publication, and earnings review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can use Vybes and aicre8.dev APIs to create public token and prediction-market content. <br>
Mitigation: Require explicit human confirmation before token launches, prediction creation, website payments, SOL bets, or project linking. <br>
Risk: The artifact includes an undisclosed admin reserve-setting page capable of submitting reserve-changing wallet transactions. <br>
Mitigation: Do not treat the skill as routine user-facing until the publisher removes the page or gates it separately. <br>
Risk: Prediction bets and website deployment can require SOL transfers. <br>
Mitigation: Verify recipient, amount, memo, and transaction signature before submitting or confirming any transaction. <br>


## Reference(s): <br>
- [vybes.fun](https://vybes.fun) <br>
- [aicre8.dev](https://aicre8.dev) <br>
- [ClawHub listing](https://clawhub.ai/aicre8dev/vybes-fun) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with HTTP examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wallet addresses and explicit user confirmation for token launches, website payments, SOL bets, and project linking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
