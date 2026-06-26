## Description: <br>
TOTP-based OTP verification for sensitive operations (env vars, gateway restarts, backup deletions, critical config changes). Uses otplib with window:2 (1 minute tolerance). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diegofcornejo](https://clawhub.ai/user/diegofcornejo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add TOTP checks before sensitive OpenClaw operations such as reading environment variables, restarting gateways, deleting backups, changing critical configuration, or handling external API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TOTP setup output and qr.png can enroll an authenticator if exposed. <br>
Mitigation: Keep setup output private, send the QR through a secure channel, and delete qr.png immediately after enrollment. <br>
Risk: A valid OTP confirms possession of the configured authenticator but does not by itself confirm intent for destructive actions. <br>
Mitigation: Confirm destructive actions separately after a valid OTP before proceeding. <br>
Risk: Disclosure of TOTP_SECRET would allow unauthorized OTP generation. <br>
Mitigation: Protect TOTP_SECRET and install the skill only in a trusted workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diegofcornejo/totp) <br>
- [Publisher profile](https://clawhub.ai/user/diegofcornejo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text verifier status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The verifier emits OTP_VALID or OTP_INVALID and exits with status 0 or 1.] <br>

## Skill Version(s): <br>
1.0.2 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
