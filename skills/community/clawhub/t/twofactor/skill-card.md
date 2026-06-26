## Description: <br>
This skill provides guidance and enforcement rules for implementing secure two-factor authentication (2FA) using Better Auth's twoFactor plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StevenFengLi](https://clawhub.ai/user/StevenFengLi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement Better Auth two-factor authentication flows for web applications, including TOTP, OTP delivery, backup codes, trusted devices, session handling, and recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration or configuration changes for two-factor authentication can affect account access and authentication behavior. <br>
Mitigation: Review Better Auth migration output in development or staging before applying the examples to production. <br>
Risk: Passwords, OTPs, TOTP setup URIs, backup codes, and trusted-device settings are sensitive account-security material. <br>
Mitigation: Handle these values as secrets, avoid exposing them in logs or long-lived client state, and review recovery flows before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StevenFengLi/twofactor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers sensitive account-security material such as passwords, OTPs, TOTP setup URIs, backup codes, and trusted-device settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
