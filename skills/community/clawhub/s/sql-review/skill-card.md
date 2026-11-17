## Description:

Pre-commit SQL code review for uncommitted database changes that detects production-risk antipatterns and reports BLOCKER/WARN/INFO findings with file:line citations and proposed fixes without editing SQL by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill before committing SQL changes to inspect changed .sql files for production-risk antipatterns and receive prioritized findings with citations and proposed fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local SQL diffs and quotes relevant SQL lines in its findings.

Mitigation: Use it only in workspaces where local SQL changes may be reviewed and included in an agent response.

Risk: Suggested SQL fixes can affect production data or deployment behavior if applied without review.

Mitigation: Review findings first and require explicit approval before applying any SQL changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisrongo/skills/sql-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with severity sections, file:line citations, quoted SQL evidence, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not edit SQL unless the user explicitly approves fixes after the review report.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
