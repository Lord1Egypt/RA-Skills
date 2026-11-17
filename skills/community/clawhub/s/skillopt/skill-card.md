## Description:

SkillOpt helps agents train, evaluate, and improve reusable skill files through rollout scoring, validation gates, and best_skill.md export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use SkillOpt to optimize agent skill documents against train and validation task suites, compare baseline and candidate rollouts, and export the best accepted skill with a report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark task files and agent-command templates can cause local shell commands to run with the user's privileges.

Mitigation: Use trusted task suites, review command scorers and agent-command templates before running them, prefer non-command scorers, and run the harness in a restricted workspace or container.

Risk: Secrets exposed in the local environment could be reachable to commands launched by the harness.

Mitigation: Avoid exposing secrets in the environment when running SkillOpt and isolate runs from sensitive files or credentials.

## Reference(s):

- [SkillOpt Evaluation Reference](references/evaluation.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces run directories containing candidate skill files, rollout records, summary JSON, reports, and best_skill.md when exported.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
