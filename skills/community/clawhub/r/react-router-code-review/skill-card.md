## Description:

Reviews React Router code for proper data loading, mutations, error handling, and navigation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to evaluate React Router v6.4+ route modules, loaders, actions, error boundaries, forms, and navigation logic for framework-aligned patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unreviewed sibling review-verification-protocol skill for part of its review process.

Mitigation: Review or pin that dependency before installation and before relying on review findings.

Risk: Error-logging examples may lead reviewers to recommend sending sensitive production error details to monitoring or analytics systems.

Mitigation: Confirm production logging guidance redacts sensitive details and limits verbose stack traces to development environments.

Risk: The skill provides advisory review guidance that can produce false positives if used without code-specific evidence.

Mitigation: Require each reported finding to include a route path, line reference, or concrete code excerpt.

## Reference(s):

- [React Router Code Review on ClawHub](https://clawhub.ai/anderskev/skills/react-router-code-review)
- [Publisher profile](https://clawhub.ai/user/anderskev)
- [Data Loading](references/data-loading.md)
- [Mutations](references/mutations.md)
- [Error Handling](references/error-handling.md)
- [Navigation](references/navigation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown review findings with code references and React Router guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should be evidence-based and tied to route paths, line references, or code excerpts.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
