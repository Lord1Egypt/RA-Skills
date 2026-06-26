## Description: <br>
WebClaw provides a browser-based OpenClaw dashboard for installed skills, with schema-driven UI rendering, JWT authentication, RBAC, AI chat, real-time updates, SSL setup, and web user administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw administrators and developers use WebClaw to install and operate a browser dashboard, manage web users and sessions, configure HTTPS, and inspect dashboard service status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation and runtime actions can make sudo-level changes to nginx, systemd services, SSL certificates, and dashboard users. <br>
Mitigation: Install only on an administrator-controlled server, back up nginx configuration before use, and review proposed service or certificate changes before execution. <br>
Risk: Installation can fetch application source and package dependencies from the internet. <br>
Mitigation: Verify the fetched source tag and dependency inputs before installation. <br>
Risk: Session, configuration, and user listings may expose administrative operational data. <br>
Mitigation: Restrict WebClaw access to trusted administrators and treat these listings as admin-only data. <br>
Risk: Chosen passwords passed on the command line may be exposed through shell or process history. <br>
Mitigation: Prefer generated reset passwords or secure password handling and avoid passing chosen passwords as command-line arguments. <br>


## Reference(s): <br>
- [WebClaw ClawHub Release](https://clawhub.ai/mailnike/webclaw) <br>
- [WebClaw Homepage](https://www.erpclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include administrative status, user/session listings, generated credentials, SSL configuration results, and service management guidance.] <br>

## Skill Version(s): <br>
2.1.3 (source: ClawHub release metadata; artifact frontmatter and install tag reference 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
