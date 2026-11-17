## Description:

Reviews Remix v2 error-handling code for the unified ErrorBoundary, isRouteErrorResponse narrowing, throw-vs-return behavior, root boundary scaffolding, and v1 holdovers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review TypeScript Remix v2 route modules for correct error boundaries, thrown response handling, root boundary scaffolding, and migration holdovers from Remix v1.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The final reporting process depends on an unbundled external verification protocol outside the reviewed artifact.

Mitigation: Review or vendor the external review-verification-protocol dependency before relying on this skill.

## Reference(s):

- [ErrorBoundary Shape - Export, Hook, Narrowing](references/boundary-shape.md)
- [Root ErrorBoundary - Document Scaffolding](references/root-boundary.md)
- [Throw vs Return - Responses, Errors, and handleError](references/throw-response.md)
- [v1 Holdovers - CatchBoundary, useCatch, v2_errorBoundary](references/v1-holdovers.md)
- [Remix v2 ErrorBoundary docs](https://remix.run/docs/en/main/route/error-boundary)
- [Remix v2 error handling guide](https://remix.run/docs/en/main/guides/errors)
- [Remix v2 entry.server handleError docs](https://remix.run/docs/en/main/file-conventions/entry.server)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings with code examples and checklist-style guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity labels, file and line evidence requirements, and Remix v2 references.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
