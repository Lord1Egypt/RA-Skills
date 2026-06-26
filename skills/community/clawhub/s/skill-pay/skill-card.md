## Description: <br>
Add credit-based payments to OpenClaw skills so builders can register paid skills, charge users per call, track earnings, and withdraw USDC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adjusternwachukwu-bot](https://clawhub.ai/user/adjusternwachukwu-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use SkillPay to add credit-based monetization to OpenClaw skills, including buyer registration, deposits, per-call charging, builder registration, paid-skill registration, earnings checks, and withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through deposits, user charges, paid-skill registration, and withdrawals. <br>
Mitigation: Require explicit user approval before every deposit, withdrawal, paid-skill registration, or user charge. <br>
Risk: Buyer and builder API keys and wallet details are sensitive payment credentials. <br>
Mitigation: Store keys and wallet details in a secret store and avoid exposing them in prompts, logs, or shared skill outputs. <br>
Risk: Payment-provider details, fee model, wallet destination, and recovery process may be misunderstood or change outside the skill. <br>
Mitigation: Verify the SkillPay provider, platform fee, wallet destination, and recovery process before enabling monetized workflows. <br>


## Reference(s): <br>
- [SkillPay ClawHub release page](https://clawhub.ai/adjusternwachukwu-bot/skill-pay) <br>
- [SkillPay API base](https://skillpay.gpupulse.dev/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoint examples and payment-flow guidance; users must supply their own SkillPay API keys and wallet details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
