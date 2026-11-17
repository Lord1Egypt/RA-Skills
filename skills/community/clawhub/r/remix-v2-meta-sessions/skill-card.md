## Description:

Provides Remix v2 guidance for meta/SEO, links, cookie sessions, auth gates, and CSRF protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to update Remix v2 applications with correct document head exports, cookie session handling, loader/action auth gates, and CSRF protections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-sensitive snippets for sessions, auth, and CSRF may be copied without adapting cookie names, session duration, SameSite policy, or app-specific values.

Mitigation: Treat snippets as templates and review those settings against the target application's deployment and threat model before use.

Risk: Incomplete application of auth, session, or CSRF guidance can leave protected routes or mutating actions exposed.

Mitigation: Require project review of loader/action auth gates, Set-Cookie handling, and CSRF validation before deploying changes based on the skill.

## Reference(s):

- [Meta v2 Reference](references/meta-v2.md)
- [Links Reference](references/links.md)
- [Sessions Reference](references/sessions.md)
- [Auth and CSRF Reference](references/auth-csrf.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with TypeScript and TSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; snippets must be adapted to the target Remix application.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
