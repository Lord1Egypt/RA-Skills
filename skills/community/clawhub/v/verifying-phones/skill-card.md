## Description: <br>
Verifies phone numbers via SMS OTP using the Sendly Verify API. Sends codes, checks codes, handles expiry, and provides hosted verification sessions. Applies for phone verification, OTP, 2FA, or passwordless login flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sendly-live](https://clawhub.ai/user/sendly-live) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Sendly-backed phone number verification, OTP, 2FA, and passwordless login flows to applications. It provides REST and Node.js SDK examples for sending, checking, resending, expiring, and validating verification sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use of a Sendly API key and verification tokens could expose credentials or sensitive verification data if copied into prompts, logs, or client-side code. <br>
Mitigation: Keep the Sendly API key and verification tokens server-side, out of prompts and logs, and review Sendly's handling of phone numbers and tokens for the deployment. <br>
Risk: Sending or resending real SMS messages can create user impact and provider cost if run unintentionally. <br>
Mitigation: Use sandbox keys while testing and require confirmation before sending or resending real SMS messages. <br>


## Reference(s): <br>
- [Verify API docs](https://sendly.live/docs/verify) <br>
- [OTP tutorial](https://sendly.live/docs/tutorials/otp) <br>
- [Error handling guide](https://sendly.live/docs/how-to/handle-otp-errors) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API-key, sandbox testing, SMS send/resend, OTP checking, expiry, and hosted-session validation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
