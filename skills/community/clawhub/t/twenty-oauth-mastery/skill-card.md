## Description:

Provides OAuth 2.0 implementation, troubleshooting, and token management guidance for Twenty CRM with Google and Microsoft OAuth plus email and calendar sync integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avirweb](https://clawhub.ai/user/avirweb)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when implementing, debugging, or reviewing Twenty CRM OAuth flows, including provider setup, redirect loops, domain restrictions, token refresh behavior, and Gmail or calendar sync setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes token transport guidance that could expose user sessions or OAuth credentials.

Mitigation: Keep OAuth and session tokens out of JavaScript-readable cookies and URLs; use secure, HTTP-only server-managed session handling where possible.

Risk: Troubleshooting steps may reveal secrets in logs, shell output, or copied configuration.

Mitigation: Redact client secrets, access tokens, refresh tokens, and session cookies before logging, sharing, or storing diagnostic output.

Risk: Database and container commands can change production authentication or sync behavior.

Mitigation: Run these commands only with backups, change control, environment confirmation, and rollback steps.

Risk: Package and build commands may introduce unreviewed dependency or runtime changes.

Mitigation: Pin package versions and review dependency changes before deployment.

## Reference(s):

- [Twenty CRM OAuth Mastery on ClawHub](https://clawhub.ai/avirweb/skills/twenty-oauth-mastery)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, shell, SQL, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes troubleshooting checklists and implementation patterns; guidance should be reviewed before applying to production systems.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
