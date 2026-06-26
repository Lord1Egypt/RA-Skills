## Description: <br>
Helps an agent discover RedotPay services, inspect pricing and parameters, and make confirmed RedotPay CLI requests for MPP-style 402/x402 workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbo-wang](https://clawhub.ai/user/turbo-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search RedotPay service listings, inspect service details and pricing, handle RedotPay login, and run paid or session-gated requests only after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable paid RedotPay CLI requests from broad discovery or request prompts. <br>
Mitigation: Confirm the selected service, endpoint, exact USD cost, request purpose, and spend cap with the user before any paid redotpay request. <br>
Risk: RedotPay login and wallet state require sensitive local credentials and session handling. <br>
Mitigation: Use the documented QR login flow, avoid exposing OAuth tokens or wallet configuration, and check redotpay wallet whoami before chargeable requests. <br>
Risk: Persistent PATH setup can leave the redotpay CLI available for future agent invocations. <br>
Mitigation: Verify the CLI binary source before use, avoid broad auto-invocation, and remove the ~/.local/bin/redotpay symlink when the integration is no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/turbo-wang/redotpay-payment) <br>
- [RedotPay CLI installer](https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.1/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and CLI workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in RedotPay CLI calls that require wallet login, explicit payment confirmation, and spend-cap handling.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
