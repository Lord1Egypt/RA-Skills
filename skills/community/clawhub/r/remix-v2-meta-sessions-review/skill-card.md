## Description:

Reviews Remix v2 code for v1-shape meta exports, cookie security gaps, auth gates in the wrong layer, and missing CSRF protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Remix v2 code for SEO metadata regressions, session and cookie security gaps, misplaced authentication gates, and missing CSRF protections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect security-sensitive Remix application files and git history while reviewing auth, session, cookie, meta, and CSRF code.

Mitigation: Use it only in repositories where reviewers are authorized to expose that code to the agent, and review findings before applying changes.

Risk: Companion-document links can mislead reviewers if they point outside trusted review material.

Mitigation: Rely on the bundled references and server-resolved ClawHub release page when checking the review guidance.

## Reference(s):

- [Auth Gates - Anti-Patterns](references/auth-gates.md)
- [Cookie Security - Anti-Patterns](references/cookie-security.md)
- [CSRF - Anti-Patterns](references/csrf.md)
- [Meta v2 Shape - Anti-Patterns](references/meta-v2-shape.md)
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/remix-v2-meta-sessions-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing review guidance; no executable payload is included in the release evidence.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
