## Description: <br>
Send and receive compliant B2B payments via the Ra Pay CLI, and onboard a counterparty agent so both sides can transact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greendlt224](https://clawhub.ai/user/greendlt224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide agents through business-to-business USD payment setup, fee preview, explicit user approval, payment execution, and counterparty onboarding with the Ra Pay CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help move real money through a B2B payment workflow. <br>
Mitigation: Review every fee preview, independently confirm recipient acct_ IDs, and approve --confirm only for legitimate business transactions the user recognizes. <br>
Risk: Payment setup and execution depend on the Ra Pay CLI and local account state. <br>
Mitigation: Verify the Ra Pay CLI source before installation and use the CLI status commands to confirm account setup before transacting. <br>


## Reference(s): <br>
- [Ra Pay Skill Instructions](https://rapay.ai/skill.md) <br>
- [ClawHub Release Page](https://clawhub.ai/greendlt224/rapay) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires fee preview and explicit user confirmation before payment execution.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
