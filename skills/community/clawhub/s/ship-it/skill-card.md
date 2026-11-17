## Description:

Ship It helps agents audit a feature, release, branch, or module against a fixed operational-readiness checklist and produce an evidence-backed PASS / GAP / N/A report before launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill before shipping code to check operational readiness across logging, error handling, telemetry, feature flags, migrations, rollback, secrets, local-first storage, auth, and update strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational readiness findings may be incomplete if the shipping scope is ambiguous or unavailable.

Mitigation: Require the agent to name and echo the release scope before auditing, then cite named probes and file:line evidence for PASS findings.

Risk: Users may apply the skill to diff-level quality, tests, dead code, or refactoring questions instead of operational readiness.

Mitigation: Use this skill for release-readiness checks and route code-quality review requests to a normal code-review skill.

Risk: Recommendations could be acted on without human review.

Mitigation: Keep the skill read-only by default; ask before drafting fixes and review proposed changes before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with grouped findings and inline file:line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; PASS findings require named probes and file:line evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
