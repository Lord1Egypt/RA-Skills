## Description:

WebClaw installs and administers a browser-based OpenClaw dashboard with schema-driven skill rendering, JWT authentication, RBAC, AI chat, real-time updates, user management, and SSL configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailnike](https://clawhub.ai/user/mailnike)

### License/Terms of Use:

MIT

## Use Case:

Developers and administrators use WebClaw to install and operate a web dashboard for OpenClaw skills, manage dashboard users and sessions, configure HTTPS, and check or restart dashboard services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation pulls remote code and installs persistent services with broad host privileges.

Mitigation: Install only on a dedicated host or VM, verify the upstream release tag before installation, and review service and package changes before use.

Risk: The installer can modify nginx, certbot, systemd services, local package state, and dashboard accounts through sudo-backed operations.

Mitigation: Back up nginx configuration first, review generated service files and certificates, and limit installation to hosts where WebClaw should control the dashboard stack.

Risk: Passwords may be exposed when users provide reset passwords through chat or command-line arguments.

Mitigation: Prefer generated temporary passwords, share credentials out of band, and avoid passing reusable passwords through chat or shell history.

## Reference(s):

- [ClawHub WebClaw Skill Page](https://clawhub.ai/mailnike/skills/webclaw)
- [WebClaw Homepage](https://www.erpclaw.ai)
- [Repository URL Listed by Artifact](https://github.com/avansaber/webclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated temporary passwords and local service, SSL, user, session, and configuration status details.]

## Skill Version(s):

2.1.3 (source: server release metadata; artifact frontmatter lists 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
