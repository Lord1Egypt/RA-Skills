## Description:

Deploy MISP threat intelligence platform on any Docker-ready Linux host with the official misp-docker project, automatic MariaDB memory tuning, API key generation via cake CLI, and credential management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to deploy a MISP threat intelligence platform on an existing Docker-ready Linux host. It is suited for SOC automation workflows that need MISP setup, MariaDB sizing, admin provisioning, and API credential output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs high-impact remote deployment and can expose credentials through defaults, logs, or plaintext files.

Mitigation: Use it only on an isolated Docker host you control, replace default admin credentials, avoid printing or storing secrets in plaintext, and lock credential files to owner-only permissions.

Risk: The deployment uses unsafe TLS patterns such as self-signed certificates, MISP_VERIFY_SSL=false, or curl -k.

Mitigation: Use verified TLS certificates or place MISP behind a properly configured reverse proxy before production use.

Risk: The setup retrieves mutable MISP Docker code during deployment.

Mitigation: Pin the MISP Docker repository and image versions before deployment.

## Reference(s):

- [Gotchas: MISP Deployment](references/gotchas.md)
- [MISP .env template](references/env-template.env)
- [MISP Docker project](https://github.com/MISP/misp-docker.git)
- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/soc-deploy-misp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Code]

**Output Format:** [Markdown with inline bash commands, configuration values, and credential output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated MISP access details, API key handling steps, Docker Compose status checks, and operational warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
