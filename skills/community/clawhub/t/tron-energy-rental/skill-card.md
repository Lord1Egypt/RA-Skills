## Description: <br>
Automates TRON energy rental and fee optimization through the TRXDO resource-pool API for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itfers](https://clawhub.ai/user/itfers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw bot operators and developers use this skill to query TRXDO account/resource information and submit TRON energy-rental orders that may reduce USDT and smart-contract transaction fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat commands can use configured TRXDO API credentials to submit cost-affecting energy-rental orders. <br>
Mitigation: Require explicit confirmation before order submission and limit access to authorized users. <br>
Risk: The artifact does not include built-in wallet-address validation, quantity limits, spending limits, or audit logging. <br>
Mitigation: Add address validation, per-user quantity and spending limits, and persistent audit logs before shared or production use. <br>
Risk: TRXDO user IDs and secret keys are loaded from local configuration. <br>
Mitigation: Store credentials in a secrets manager or protected environment variables rather than checked-in or shared config files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itfers/tron-energy-rental) <br>
- [TRXDO website](https://www.trxdo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text agent responses with configuration examples and API-backed status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit cost-affecting TRON energy-rental orders using configured TRXDO credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
