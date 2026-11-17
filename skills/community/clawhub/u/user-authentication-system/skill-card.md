## Description:

Role-based access control for Greek accounting firms. Login, role hierarchy, per-client permissions, session management, audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satoshistackalotto](https://clawhub.ai/user/satoshistackalotto)

### License/Terms of Use:


## Use Case:

Developers and operators of Greek accounting firm workflows use this skill to add local user authentication, role hierarchy, per-client authorization, session management, and audit logging to OpenClaw environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials, sessions, and account authority in a shared local filesystem.

Mitigation: Use strong filesystem isolation and restrictive permissions for authentication data before relying on the skill.

Risk: Authorization and path-safety flaws could expose or modify sensitive account data.

Mitigation: Require username and path validation, and handle OPENCLAW_DATA_DIR consistently across all examples and runtime paths.

Risk: Administrative actions such as session revocation, account deactivation, or government submissions can be disruptive.

Mitigation: Require explicit confirmation for disruptive admin actions and senior approval for government submissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/satoshistackalotto/skills/user-authentication-system)
- [Publisher Profile](https://clawhub.ai/user/satoshistackalotto)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML examples, and Python-style reference code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, openssl, openclaw, and OPENCLAW_DATA_DIR; outputs local authentication and authorization guidance for OpenClaw.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
