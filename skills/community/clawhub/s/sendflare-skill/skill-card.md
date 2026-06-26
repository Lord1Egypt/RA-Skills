## Description: <br>
Sendflare sends email through the Sendflare SDK and supports basic contact-list workflows with API-token authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepchen](https://clawhub.ai/user/keepchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to send Sendflare emails from natural-language commands and to access contact-management workflows when the required Sendflare configuration is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real emails from parsed natural-language commands without a separate confirmation step. <br>
Mitigation: Verify the recipient, subject, and body before issuing send commands, and use human approval for workflows that send outbound email. <br>
Risk: The skill requires a Sendflare API token. <br>
Mitigation: Use a limited or revocable token where possible, store it only in secure configuration, and rotate it if exposure is suspected. <br>
Risk: The configured sender must be valid for the Sendflare account and verified domain. <br>
Mitigation: Confirm the sender domain and account settings in Sendflare before relying on successful delivery. <br>
Risk: Contact management is experimental and attachments are not supported. <br>
Mitigation: Avoid relying on contact changes or attachment workflows in critical usage unless those behaviors are separately verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keepchen/sendflare-skill) <br>
- [Sendflare](https://Sendflare.com) <br>
- [Sendflare Node.js SDK documentation](https://docs.Sendflare.com/docs/sdk/nodejs/) <br>
- [Sendflare API documentation](https://docs.Sendflare.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Plain text status messages and suggested actions from Sendflare email or contact operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sendflare API token; email sending is stable, contact management is experimental, and attachments are not supported.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
