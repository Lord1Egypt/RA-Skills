## Description: <br>
Provides session authentication for OpenClaw using passphrases, recovery options, lockout protection, audit logging, and SkillPay billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squallsol](https://clawhub.ai/user/squallsol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add a passphrase gate to sessions, configure recovery, and manage session authentication state. It is intended for environments where access control, timeout behavior, and billing prompts need to be handled during agent use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment behavior and pricing are inconsistent across the artifact and include an embedded billing key. <br>
Mitigation: Review the payment path before installation, rotate or remove embedded billing credentials, confirm the price shown to users, and require explicit consent before any charge. <br>
Risk: Recovery behavior can expose recovery codes through stub output or local storage when email delivery is not configured. <br>
Mitigation: Configure a real email provider, remove plaintext recovery-code output, and avoid treating the recovery flow as a security boundary until this is fixed. <br>
Risk: Broad authentication triggers may activate the skill when the user did not intend to run a paid authentication flow. <br>
Mitigation: Limit activation to explicit authentication commands and make any billing or setup action visible before it proceeds. <br>
Risk: Setup documentation and authentication files are not fully aligned across artifact files. <br>
Mitigation: Verify the setup flow against the files actually read by the authentication and recovery scripts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squallsol/session-password) <br>
- [Publisher profile](https://clawhub.ai/user/squallsol) <br>
- [SkillPay platform](https://skillpay.me) <br>
- [Feature specification](artifact/docs/FEATURE_SPEC.md) <br>
- [User manual](artifact/docs/USER_MANUAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-style text with inline shell commands and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local authentication, recovery, audit, and billing-related configuration files during setup and use.] <br>

## Skill Version(s): <br>
1.6.1 (source: evidence release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
