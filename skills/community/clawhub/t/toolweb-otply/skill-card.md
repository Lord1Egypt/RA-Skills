## Description: <br>
Email OTP Service - Simple, Fast, Reliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use OTPly to integrate email-based one-time password registration, delivery, verification, and usage tracking into authentication, recovery, or sensitive transaction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys, API secrets, recipient email addresses, and OTP values are sensitive authentication data. <br>
Mitigation: Keep secrets and OTP values out of client-side code, chats, logs, screenshots, and repositories. <br>
Risk: Sending OTPs can contact real recipients and affect authentication workflows. <br>
Mitigation: Require explicit confirmation before sending OTPs and use the intended recipient, purpose, template, and expiry values. <br>


## Reference(s): <br>
- [OTPly ClawHub Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-otply) <br>
- [OTPLY API Docs](https://api.toolweb.in:8168/docs) <br>
- [OTPLY Kong Route](https://api.toolweb.in/tools/otply) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown with endpoint descriptions, JSON request examples, and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OTPLY API key and secret handling for authenticated OTP send, verification, and usage endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
