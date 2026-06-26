## Description: <br>
Web dashboard for OpenClaw with browser-based UI for installed skills, schema-driven rendering, JWT authentication, RBAC, AI chat, real-time updates, SSL setup, and web user administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and administrators use Web Claw to install and operate an OpenClaw web dashboard, manage dashboard users and sessions, configure HTTPS, and inspect service status for installed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent OpenClaw web dashboard and integrates with nginx and systemd using privileged operations. <br>
Mitigation: Install only on a server you administer, review the release and dependency sources before installation, and treat service and SSL changes as administrator actions. <br>
Risk: Dashboard user, password, session, SSL, and service-restart actions can change access or availability. <br>
Mitigation: Restrict who can invoke Web Claw actions, review account-management requests before execution, and verify service status after privileged changes. <br>
Risk: Install-time setup fetches application code and dependencies from external sources. <br>
Mitigation: Verify the pinned release, dependency sources, and installation environment before running the installer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mailnike/web-claw) <br>
- [ERPClaw website](https://www.erpclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON action results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local administration guidance and action outputs for a Linux-hosted OpenClaw dashboard.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter lists 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
