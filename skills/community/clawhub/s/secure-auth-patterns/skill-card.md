## Description:

Provides reference guidance and code examples for implementing authentication and authorization patterns such as JWT, OAuth2/OIDC, sessions, RBAC, permissions, and resource ownership checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwise](https://clawhub.ai/user/brandonwise)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as reference material when implementing or reviewing authentication and authorization for web applications and APIs. It is most relevant for JWT token flows, OAuth2/social login, session management, role and permission checks, resource ownership, password handling, and authentication endpoint hardening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copying the OAuth callback example could expose bearer tokens in URLs.

Mitigation: Replace token-in-query redirects with secure HttpOnly cookies or a short-lived one-time code exchange before using the pattern in an application.

Risk: Session examples may be copied without additional session hardening after login or privilege changes.

Mitigation: Regenerate session identifiers after authentication and privilege changes, then review cookie, CSRF, and expiration settings before deployment.

## Reference(s):

- [Implementation Playbook](artifact/resources/implementation-playbook.md)
- [ClawHub Skill Page](https://clawhub.ai/brandonwise/skills/secure-auth-patterns)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with TypeScript and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation checklists, pattern comparisons, and security recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
