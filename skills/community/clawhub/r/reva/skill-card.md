## Description:

Reva helps agents authenticate users, manage PayID names, view account and wallet details, and transfer supported crypto assets through Reva.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pax47](https://clawhub.ai/user/pax47)

### License/Terms of Use:


## Use Case:

External Reva users use this skill to complete email OTP authentication, claim PayIDs, inspect wallet and account details, and send supported tokens after providing the required transfer details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs real crypto-wallet actions, including transfers.

Mitigation: Before any transfer, manually confirm the exact recipient, network, token, and amount.

Risk: The skill stores a local wallet access token for authenticated Reva operations.

Mitigation: Install only in trusted environments and clear the local auth file when the session should end.

Risk: OTP values and transfer details may be exposed in environments that log command output or process arguments.

Mitigation: Avoid entering OTPs or initiating transfers in shared, recorded, or heavily logged shells.

## Reference(s):

- [Reva homepage](https://revapay.ai)
- [Reva on ClawHub](https://clawhub.ai/pax47/skills/reva)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance, configuration]

**Output Format:** [Plain text and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and curl; protected actions require a locally stored Reva access token after email OTP verification.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
