## Description:

Reviews Remix v2 loaders and actions for mutations-in-loader, missing validation, leaked server fields, wrong return helpers, v1 useTransition holdovers, and revalidation traps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Remix v2 route data flows for loader/action mistakes, unsafe client data exposure, revalidation traps, and outdated v1 patterns before reporting findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some linked canonical and protocol documents live outside this package.

Mitigation: Review those external dependencies separately when they are present, and rely on the bundled reference notes for package-local review behavior.

Risk: Code-review findings could be misleading if reported without direct source evidence.

Mitigation: Require file location evidence, exemption checks, and pre-report verification before presenting findings.

## Reference(s):

- [Loader Review Reference](references/loaders.md)
- [Action Review Reference](references/actions.md)
- [Revalidation & Pending State Review Reference](references/revalidation.md)
- [Defer & Await Review Reference](references/defer-await.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/remix-v2-data-flow-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with code references and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings must include file location evidence and pass the skill's pre-report verification gates.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
