## Description:

Audit failure states, retries, validation, and idempotency in the code under review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to audit code for missing or weak error paths, boundary validation, timeout and retry behavior, observability, and idempotency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review guidance may be incomplete or misleading if the agent does not inspect the actual error paths, callers, and retry behavior.

Mitigation: Require findings to cite concrete evidence such as files, lines, confirmed checks, and explicit assumptions.

Risk: The optional Ritual CLI path introduces external tooling risk if the user chooses to install it.

Mitigation: Use local mode when sufficient; if installing the CLI, review the npm package, avoid administrator privileges, and prefer a pinned or sandboxed install.

## Reference(s):

- [Review Error Handling on ClawHub](https://clawhub.ai/ritual/skills/review-error-handling)
- [Ritual homepage](https://ritual.work)
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text review findings with optional file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concrete gaps, confirmed checks, assumptions, and optional reusable knowledge notes when approved by the user.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
