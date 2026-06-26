## Description: <br>
Manage Routstr balance by checking balance, creating Lightning invoices for top-up, and checking invoice payment status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sh1ftred](https://clawhub.ai/user/sh1ftred) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Routstr users use this skill to inspect account balance and usage, create Lightning invoices for top-ups, check invoice payment status, and redeem Cashu tokens into a Routstr account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Routstr API key and account details. <br>
Mitigation: Keep ~/.openclaw/openclaw.json protected, confirm it uses a trusted HTTPS Routstr endpoint, and avoid sharing command lines, logs, or outputs that may expose account information. <br>
Risk: Lightning invoices and Cashu token redemption can move or redeem value. <br>
Mitigation: Verify invoice amounts before payment and only pass Cashu tokens you are willing to redeem. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sh1ftred/routstr-balance-management) <br>
- [Publisher profile](https://clawhub.ai/user/sh1ftred) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Terminal text and JSON responses from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Routstr base URL and API key from ~/.openclaw/openclaw.json and may print balances, usage totals, invoices, payment status, or top-up results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
