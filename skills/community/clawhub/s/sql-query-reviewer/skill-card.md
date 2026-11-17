## Description:

Reviews SQL queries for correctness, security risks, and performance issues, then provides a structured report with severity ratings and optimized rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnguyen1996](https://clawhub.ai/user/lnguyen1996)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review raw SQL, ORM-generated SQL, and migration files for correctness, injection risks, performance issues, and maintainability concerns before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL text may contain secrets, production credentials, sensitive schema names, or private business logic.

Mitigation: Remove secrets and highly sensitive schema details before review.

Risk: The skill asks the agent to remember aggregate SQL review patterns between reviews.

Mitigation: Remove or ignore the self-improvement tracking instruction when aggregate pattern memory is not desired.

Risk: Optimized rewrites and review findings may be incorrect or change query behavior.

Mitigation: Review and test suggested SQL changes before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lnguyen1996/skills/sql-query-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with findings, severity ratings, corrected SQL, optimized rewrites, and summary recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include aggregate common-issue notes after repeated reviews if the agent follows the self-improvement instruction.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
