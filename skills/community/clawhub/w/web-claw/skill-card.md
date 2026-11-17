## Description:

Web dashboard for OpenClaw, providing a browser-based UI for installed skills with schema-driven rendering, JWT authentication, RBAC, AI chat, real-time updates, user management, SSL setup, and web administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:

MIT-0

## Use Case:

Administrators use Web Claw to install and operate a browser dashboard for OpenClaw skills, manage dashboard users and sessions, configure HTTPS, and restart or inspect web services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches code and package dependencies during installation and then configures privileged persistent services.

Mitigation: Install only on a dedicated host or VM, review the fetched release contents, dependency manifests, templates, nginx changes, and service units before running the installer.

Risk: Installation and maintenance actions use sudo and can modify nginx, systemd services, SSL certificates, and local service state.

Mitigation: Run the skill only where the operator is comfortable granting those privileges, and review proposed service or web server changes before applying them.

Risk: User creation and password reset actions can emit temporary or chosen passwords into chat or logs.

Mitigation: Share reset passwords through a secure channel, rotate temporary passwords promptly, and avoid storing credentials in chat transcripts or operational logs.

## Reference(s):

- [Web Claw on ClawHub](https://clawhub.ai/mailnike/skills/web-claw)
- [Webclaw project homepage](https://www.erpclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installer and management actions can change local services, nginx configuration, SSL certificates, users, sessions, and the local SQLite database.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
