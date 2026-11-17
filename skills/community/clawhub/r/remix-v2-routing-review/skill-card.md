## Description:

Reviews Remix v2 route files for naming convention violations, missing layouts, resource-route shape, and v1 holdovers. Use when reviewing files under app/routes/ in a Remix v2 codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to perform focused Remix v2 routing reviews, especially for route filenames, layouts, resource routes, root document shell behavior, and v1 migration holdovers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read relevant application source and configuration files during a routing review.

Mitigation: Use it only in workspaces where the agent is permitted to inspect Remix route, root, package, and routing configuration files.

Risk: The skill references a companion review-verification protocol that is not bundled in this artifact.

Mitigation: Verify that any companion review-protocol skill loaded with it comes from a trusted source before relying on its findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/remix-v2-routing-review)
- [Route File Naming Smells](references/route-files.md)
- [Layouts and Outlets](references/layouts-outlets.md)
- [Resource Routes](references/resource-routes.md)
- [Root Shell Smells](references/root-shell.md)
- [v1 Holdovers](references/v1-holdovers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Code review findings]

**Output Format:** [Markdown review findings with source locations, quoted evidence, exemption checks, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is documentation-only and is loaded for Remix v2 routing review contexts rather than invoked directly by users.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
