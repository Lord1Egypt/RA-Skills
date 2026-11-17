## Description:

Reviews Swift code for concurrency safety, error handling, memory management, and common mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift changes for concurrency, Observation framework usage, error handling, memory management, and common Swift correctness issues before reporting findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow expects a separate review-verification-protocol skill; if that dependency is unavailable, reviews may be less complete.

Mitigation: Confirm the verification protocol is available before relying on reported findings, or manually enforce full-symbol reading, usage search, caller checks, severity calibration, and file-line evidence.

## Reference(s):

- [Swift Code Review ClawHub Page](https://clawhub.ai/anderskev/skills/swift-code-review)
- [Swift Common Mistakes](references/common-mistakes.md)
- [Swift Concurrency](references/concurrency.md)
- [Swift Error Handling](references/error-handling.md)
- [Swift Observation Framework](references/observable.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown review findings with file and line references, severity labels, and concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, credential handling, or unrelated data access was identified in the security evidence.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
