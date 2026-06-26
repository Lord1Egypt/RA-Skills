## Description: <br>
Use this skill when a team, DAO, or builder wants to deploy USDC from a stablecoin treasury into LI.FI Earn vaults under explicit treasury policy limits, prepare a Composer deposit, and produce a receipt-token execution report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, DAOs, and builders use this skill to apply treasury policy before deploying USDC into LI.FI Earn vaults. It helps produce policy check results, Composer deposit preparation details, and a post-execution receipt-token report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet approvals or Composer transactions may move treasury funds if signed without review. <br>
Mitigation: Review every vault choice, quote, approval, and transaction in the connected wallet before signing. <br>
Risk: The skill calls a local StableOps backend for plan and quote preparation. <br>
Mitigation: Install and use the skill only when the local StableOps backend is trusted. <br>
Risk: Implicit invocation could run the treasury workflow when the user did not intend to use it. <br>
Mitigation: Disable implicit invocation if treasury actions should run only after explicit StableOps requests. <br>
Risk: Private keys or seed phrases could be exposed if entered into an agent conversation. <br>
Mitigation: Never paste private keys or seed phrases into the agent; use a wallet for signing. <br>


## Reference(s): <br>
- [StableOps Treasury ClawHub release](https://clawhub.ai/richard7463/stableops-lifi-treasury) <br>
- [richard7463 publisher profile](https://clawhub.ai/user/richard7463) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes policy decisions, vault details, Composer quote preparation, transaction hash, and receipt-token explanation; wallet approvals and transactions require user review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
