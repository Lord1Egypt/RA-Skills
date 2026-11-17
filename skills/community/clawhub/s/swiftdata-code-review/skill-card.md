## Description:

Reviews SwiftData code for model design, queries, concurrency, and migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review SwiftData-related Swift code for model design, query performance and correctness, concurrency boundaries, and migration readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to read Swift files supplied for review.

Mitigation: Install and run it only where reviewing those project files is permitted.

Risk: Code review guidance can be incorrect or overbroad if findings are not tied to the reviewed source.

Mitigation: Use the skill's hard gates requiring SwiftData scope confirmation, matching references, and file-line citations for every finding.

## Reference(s):

- [SwiftData Model Design](references/model-design.md)
- [SwiftData Queries](references/queries.md)
- [SwiftData Concurrency](references/concurrency.md)
- [SwiftData Migrations](references/migrations.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/swiftdata-code-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown code review findings with file and line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are scoped to SwiftData surfaces and require cited evidence before reporting.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
