## Description:

Tvs Review guides an agent to perform strict Chinese-language code reviews over a user-specified scope, prioritizing correctness, security, regressions, tests, maintainability, and architecture issues while withholding fixes or code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill when they want a strict code review of a clear file, directory, diff, PR, commit range, or code snippet. It is intended to surface concrete review findings in a sharp Chinese style without providing fixes, sample code, or direct edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an intentionally sharp Chinese review style that may be unsuitable for teams expecting neutral feedback.

Mitigation: Use it only when that tone is desired and acceptable for the review context.

Risk: The skill refuses to provide fixes or code changes, so it may not complete remediation workflows on its own.

Mitigation: Pair the review findings with a separate implementation step when fixes are required.

Risk: The skill requires an explicit review scope and will not proceed when the scope is unclear.

Mitigation: Provide a specific file, directory, diff, PR, commit range, or code snippet before requesting review.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown code review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language review output; requires a clear review scope before analysis]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
