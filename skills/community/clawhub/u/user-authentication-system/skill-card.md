## Description: <br>
Role-based access control for Greek accounting firms, including login, role hierarchy, per-client permissions, session management, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Accounting firm operators and agents use this skill to manage local OpenClaw user authentication, role-based authorization, per-client access, sessions, 2FA, and security audit workflows. <br>

### Deployment Geography for Use: <br>
Greece <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers sensitive credential and account-control workflows where password, session-token, and 2FA handling require production-grade review. <br>
Mitigation: Before use in a real accounting environment, confirm the OpenClaw implementation uses bcrypt, Argon2id, or scrypt for passwords, hashes bearer tokens before lookup, avoids raw token storage, and protects 2FA secrets. <br>
Risk: Account-control actions such as all-client grants, role changes, password resets, deactivations, and session revocations can affect access to accounting data. <br>
Mitigation: Require explicit admin approval and audit logging for privileged account-control actions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/satoshistackalotto/user-authentication-system) <br>
- [Publisher profile](https://clawhub.ai/user/satoshistackalotto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, YAML, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance for local OpenClaw authentication and RBAC workflows using OPENCLAW_DATA_DIR, jq, openssl, and openclaw.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
