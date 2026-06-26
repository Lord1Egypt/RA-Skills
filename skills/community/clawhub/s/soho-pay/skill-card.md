## Description: <br>
Initiate payments on the SOHO Pay credit layer using EIP-712 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[max-clinch](https://clawhub.ai/user/max-clinch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare and execute SOHO Pay credit-layer USDC payments with explicit merchant addresses and user-controlled EIP-712 signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request wallet signatures and submit blockchain payments. <br>
Mitigation: Install only from a trusted publisher, require explicit user confirmation, and verify the payment amount and merchant address before execution. <br>
Risk: Signing credentials or private keys could be exposed or over-scoped. <br>
Mitigation: Use a trusted remote MPC or HSM signer with tightly scoped credentials, and avoid real private keys unless absolutely necessary. <br>
Risk: The security scan reported packaging and import gaps that matter before use with funds. <br>
Mitigation: Confirm the packaging and import issues are fixed before using the skill for real payments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/max-clinch/soho-pay) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces payment execution guidance and CLI output that can include transaction details such as transaction hash and block number.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
