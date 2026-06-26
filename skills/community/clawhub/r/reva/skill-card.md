## Description: <br>
Complete Reva wallet management for passwordless authentication, PayID name claiming, multi-chain crypto transfers to PayIDs or wallet addresses, balance tracking, account information, and deposit guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pax47](https://clawhub.ai/user/pax47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Reva users use this skill to authenticate with email OTP, manage PayIDs, inspect wallet and account details, receive deposit addresses, and request cryptocurrency transfers through Reva. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cryptocurrency transfers can move funds without a clearly documented final confirmation step. <br>
Mitigation: Require the user to manually confirm recipient, token, chain, and amount immediately before each transfer request. <br>
Risk: Local authentication data in ~/.openclaw/payid/auth.json grants access to protected wallet operations. <br>
Mitigation: Install only on trusted devices, keep the auth file private, and delete it or log out when finished. <br>
Risk: Remote message handling is under-disclosed for transaction-related workflows. <br>
Mitigation: Tell users when requests are sent to Reva services and review returned transaction details before acting on them. <br>


## Reference(s): <br>
- [Reva](https://revapay.ai) <br>
- [Reva API](https://api.revapay.ai) <br>
- [ClawHub release page](https://clawhub.ai/pax47/reva) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with shell command invocations and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local authentication state in ~/.openclaw/payid/auth.json and communicates with Reva API endpoints.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
