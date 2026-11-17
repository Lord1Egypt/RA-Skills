## Description:

Who Is Actor is a zero-install Git repository collaboration-pattern analysis skill that produces aggregate repository-level reports on commit cadence, churn, rework, conventional-commit compliance, and bus-factor risk without personnel evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review aggregate Git repository collaboration patterns for repositories they are authorized to analyze. It supports workflow retrospectives and repository-level risk review, not performance management or individual contributor evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository analysis can expose raw repository paths and Git history during local collection.

Mitigation: Use dry-run first, analyze only repositories you are authorized to inspect, and require aggregation or hashing before file-path-derived data reaches the model.

Risk: Command-scoping gaps can make unsafe paths or branch names risky.

Mitigation: Reject commands with unquoted paths or branch names beginning with `-`, and keep execution limited to reviewed, read-only Git commands.

Risk: Sensitive repositories may contain confidential commit subjects, paths, ticket IDs, or internal references.

Mitigation: Avoid sensitive repositories unless raw commit text and paths remain local-only and only aggregate metrics are used in model-bound context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/who-is-actor)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with optional dry-run command preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository-level aggregate metrics only; no contributor display names, per-contributor scores, rankings, or personnel recommendations.]

## Skill Version(s):

1.0.15 (source: server release metadata, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
