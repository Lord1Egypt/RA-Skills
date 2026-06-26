## Description: <br>
Sunday gives agents a dedicated email address and end-to-end encrypted credential vault for account signup, login, inbox checks, OTP retrieval, and stored credential access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Sunday when an agent needs its own identity for signing up to services, receiving verification email, checking an inbox, and storing or retrieving service credentials without using the user's personal email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent ongoing access to an agent-owned inbox and encrypted credential vault. <br>
Mitigation: Install only after verifying the Sunday CLI and service, and limit use to tasks where the agent needs its own identity. <br>
Risk: Credentials, OTPs, and verification links may be exposed if command output is copied into logs or shared transcripts. <br>
Mitigation: Protect ~/.sunday/config.json like a password vault and avoid printing decrypted passwords, OTPs, or verification links unless the task requires it. <br>


## Reference(s): <br>
- [Sunday account setup](https://sunday.ravi.app) <br>
- [Sunday on ClawHub](https://clawhub.ai/raunaksingwi/sunday) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json when available so agents can parse structured output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
