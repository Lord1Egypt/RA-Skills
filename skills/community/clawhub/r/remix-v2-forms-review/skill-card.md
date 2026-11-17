## Description:

Reviews Remix v2 form code for manual fetch() mutations, native <form> misuse, wrong useNavigation/useFetcher choice, missing pending state, unbounded uploads, and intent-pattern violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Remix v2 form and mutation code for lifecycle, pending-state, upload-validation, and multi-action route issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to consult sibling Remix v2 form-review documentation that may be absent or untrusted in a local skill set.

Mitigation: Confirm the referenced sibling documentation is installed and trusted before relying on cross-referenced patterns.

Risk: Review guidance can produce false positives if applied without route, form method, and exemption evidence.

Mitigation: Require concrete file locations, POST or non-GET method confirmation, and exemption checks before reporting findings.

## Reference(s):

- [Form vs Fetcher Misuse](references/form-vs-fetcher.md)
- [Pending State Anti-patterns](references/pending-state.md)
- [Uploads, FormData Validation & Optimistic State](references/uploads-validation.md)
- [Multi-action Routes & Method Choice](references/multi-action-routes.md)
- [Canonical Remix V2 Forms Patterns](../remix-v2-forms/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown code-review findings with optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should include file locations, exemption checks, and concise remediation guidance.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
